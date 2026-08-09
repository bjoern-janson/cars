#!/usr/bin/env python3
"""Exploratory A0 criterion-validity diagnostics for Pilot 0 I1.

This script does not alter the causal assay or reinterpret Runs 1/2. It mines
already-generated records to ask whether I1 = 1 - P(correct) carries observable
correction-related information.

For each supplied run it uses:
  * the full, unselected pre-treatment pool for calibration/discrimination;
  * only E0 branches from initially-wrong eligible prestates for behavioral
    criteria, collapsed to one record per frozen prestate/block.

Behavioral criteria per frozen prestate:
  revision_rate      = (# E0 branches changing the initial answer) / # E0
  self_correct_rate  = (# E0 branches reaching the benchmark key) / # E0
  instability        = 1 if the E0 branches disagree, else 0

The two E0 branches are never treated as independent observations. Relationship
summaries are descriptive: Spearman rho with block/prestate bootstrap intervals,
plus exact bottom/top-quarter means using an outcome-blind deterministic tie
breaker. No hypothesis-test p-values are produced.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Callable, Iterable, Sequence


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            try:
                rows.append(json.loads(raw))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    if not rows:
        raise ValueError(f"{path}: no rows")
    return rows


def mean(values: Sequence[float]) -> float:
    if not values:
        raise ValueError("mean of empty sequence")
    return sum(values) / len(values)


def rankdata(values: Sequence[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda i: values[i])
    ranks = [0.0] * len(values)
    pos = 0
    while pos < len(order):
        end = pos + 1
        value = values[order[pos]]
        while end < len(order) and values[order[end]] == value:
            end += 1
        avg_rank = (pos + 1 + end) / 2.0
        for j in range(pos, end):
            ranks[order[j]] = avg_rank
        pos = end
    return ranks


def pearson(x: Sequence[float], y: Sequence[float]) -> float | None:
    if len(x) != len(y) or len(x) < 2:
        return None
    mx = mean(x)
    my = mean(y)
    sx = sum((v - mx) ** 2 for v in x)
    sy = sum((v - my) ** 2 for v in y)
    if sx <= 0.0 or sy <= 0.0:
        return None
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return cov / math.sqrt(sx * sy)


def spearman(records: Sequence[dict], outcome: str) -> float | None:
    x = [float(row["i"]) for row in records]
    y = [float(row[outcome]) for row in records]
    return pearson(rankdata(x), rankdata(y))


def auc_for_wrong(records: Sequence[dict]) -> float | None:
    """AUROC for I1 predicting initial wrongness, with tied scores handled exactly."""
    positives = [row for row in records if int(row["wrong"]) == 1]
    negatives = [row for row in records if int(row["wrong"]) == 0]
    if not positives or not negatives:
        return None
    concordance = 0.0
    total = 0
    for pos in positives:
        for neg in negatives:
            pi = float(pos["i"])
            ni = float(neg["i"])
            total += 1
            if pi > ni:
                concordance += 1.0
            elif pi == ni:
                concordance += 0.5
    return concordance / total


def percentile(sorted_values: Sequence[float], q: float) -> float:
    if not sorted_values:
        raise ValueError("percentile of empty sequence")
    if len(sorted_values) == 1:
        return float(sorted_values[0])
    position = (len(sorted_values) - 1) * q
    lo = math.floor(position)
    hi = math.ceil(position)
    if lo == hi:
        return float(sorted_values[lo])
    frac = position - lo
    return float(sorted_values[lo] * (1 - frac) + sorted_values[hi] * frac)


def stratified_bootstrap_ci(
    records: Sequence[dict],
    metric: Callable[[Sequence[dict]], float | None],
    *,
    seed: int,
    n_boot: int,
    stratum_field: str = "run",
) -> dict:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in records:
        grouped[str(row[stratum_field])].append(row)

    rng = random.Random(seed)
    values: list[float] = []
    for _ in range(n_boot):
        sample: list[dict] = []
        for group in grouped.values():
            sample.extend(rng.choice(group) for _ in range(len(group)))
        value = metric(sample)
        if value is not None and math.isfinite(float(value)):
            values.append(float(value))

    values.sort()
    if not values:
        return {"low": None, "high": None, "valid_bootstraps": 0}
    return {
        "low": percentile(values, 0.025),
        "high": percentile(values, 0.975),
        "valid_bootstraps": len(values),
    }


def stable_tie_key(seed: int, key: str) -> str:
    return hashlib.sha256(f"{seed}::{key}".encode("utf-8")).hexdigest()


def exact_tail_summary(records: Sequence[dict], outcome: str, tie_seed: int) -> dict:
    n = len(records)
    q = n // 4
    if q < 1:
        return {
            "tail_records": 0,
            "low_mean": None,
            "high_mean": None,
            "high_minus_low": None,
        }
    ranked = sorted(
        records,
        key=lambda row: (float(row["i"]), stable_tie_key(tie_seed, str(row["key"]))),
    )
    low = ranked[:q]
    high = ranked[-q:]
    low_mean = mean([float(row[outcome]) for row in low])
    high_mean = mean([float(row[outcome]) for row in high])
    return {
        "tail_records": q,
        "low_i_min": min(float(row["i"]) for row in low),
        "low_i_max": max(float(row["i"]) for row in low),
        "high_i_min": min(float(row["i"]) for row in high),
        "high_i_max": max(float(row["i"]) for row in high),
        "low_mean": low_mean,
        "high_mean": high_mean,
        "high_minus_low": high_mean - low_mean,
        "tie_seed": tie_seed,
    }


def fixed_calibration_bins(records: Sequence[dict]) -> list[dict]:
    edges = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0000000001]
    out: list[dict] = []
    for lo, hi in zip(edges[:-1], edges[1:]):
        rows = [row for row in records if lo <= float(row["i"]) < hi]
        if not rows:
            continue
        out.append(
            {
                "i_interval": f"[{lo:.1f},{min(hi, 1.0):.1f}{']' if hi > 1.0 else ')'}",
                "n": len(rows),
                "mean_i": mean([float(row["i"]) for row in rows]),
                "observed_wrong_rate": mean([float(row["wrong"]) for row in rows]),
            }
        )
    return out


def prepare_pre_records(label: str, path: Path) -> list[dict]:
    rows = read_jsonl(path)
    out: list[dict] = []
    for line_no, row in enumerate(rows, 1):
        if "i" not in row or "initial_correct" not in row:
            raise ValueError(f"{path}:{line_no}: requires i and initial_correct")
        task_id = str(row.get("id", line_no))
        out.append(
            {
                "run": label,
                "key": f"{label}::{task_id}",
                "task_id": task_id,
                "i": float(row["i"]),
                "wrong": 0 if bool(row["initial_correct"]) else 1,
            }
        )
    return out


def prepare_e0_blocks(label: str, path: Path) -> list[dict]:
    rows = read_jsonl(path)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        if str(row.get("arm")) != "E0":
            continue
        block = str(row.get("stratum", row.get("task_id", "")))
        if not block:
            raise ValueError(f"{path}: E0 row missing stratum/task_id")
        grouped[block].append(row)

    out: list[dict] = []
    for block, branches in sorted(grouped.items()):
        if len(branches) != 2:
            raise ValueError(
                f"{path}: block {block!r} has {len(branches)} E0 branches; expected exactly 2"
            )
        i_values = {round(float(row["i"]), 12) for row in branches}
        initial_answers = {str(row["initial_answer"]).strip().upper() for row in branches}
        benchmark_answers = {str(row["benchmark_answer"]).strip().upper() for row in branches}
        if len(i_values) != 1 or len(initial_answers) != 1 or len(benchmark_answers) != 1:
            raise ValueError(f"{path}: block {block!r} does not share one frozen prestate")

        initial = next(iter(initial_answers))
        benchmark = next(iter(benchmark_answers))
        finals = [str(row["final_answer"]).strip().upper() for row in branches]
        revision_rate = sum(final != initial for final in finals) / 2.0
        self_correct_rate = sum(final == benchmark for final in finals) / 2.0
        instability = 1.0 if finals[0] != finals[1] else 0.0

        out.append(
            {
                "run": label,
                "key": f"{label}::{block}",
                "block": block,
                "i": float(branches[0]["i"]),
                "revision_rate": revision_rate,
                "self_correct_rate": self_correct_rate,
                "instability": instability,
            }
        )
    if not out:
        raise ValueError(f"{path}: no E0 blocks")
    return out


def calibration_summary(records: Sequence[dict], seed: int, n_boot: int) -> dict:
    wrong = [row for row in records if row["wrong"] == 1]
    correct = [row for row in records if row["wrong"] == 0]
    observed_auc = auc_for_wrong(records)

    def mean_i_gap(sample: Sequence[dict]) -> float | None:
        w = [float(row["i"]) for row in sample if row["wrong"] == 1]
        c = [float(row["i"]) for row in sample if row["wrong"] == 0]
        if not w or not c:
            return None
        return mean(w) - mean(c)

    return {
        "n_prestates": len(records),
        "n_wrong": len(wrong),
        "n_correct": len(correct),
        "wrong_rate": len(wrong) / len(records),
        "mean_i_wrong": mean([float(row["i"]) for row in wrong]) if wrong else None,
        "mean_i_correct": mean([float(row["i"]) for row in correct]) if correct else None,
        "mean_i_wrong_minus_correct": mean_i_gap(records),
        "mean_i_gap_bootstrap_95": stratified_bootstrap_ci(
            records, mean_i_gap, seed=seed + 1, n_boot=n_boot
        ),
        "auc_i_predicting_wrong": observed_auc,
        "auc_bootstrap_95": stratified_bootstrap_ci(
            records, auc_for_wrong, seed=seed + 2, n_boot=n_boot
        ),
        "brier_score_for_p_wrong_equals_i": mean(
            [(float(row["i"]) - float(row["wrong"])) ** 2 for row in records]
        ),
        "fixed_calibration_bins": fixed_calibration_bins(records),
    }


def behavior_summary(records: Sequence[dict], outcome: str, seed: int, n_boot: int) -> dict:
    observed_rho = spearman(records, outcome)
    return {
        "n_blocks": len(records),
        "overall_mean": mean([float(row[outcome]) for row in records]),
        "spearman_rho_i_vs_criterion": observed_rho,
        "spearman_bootstrap_95": stratified_bootstrap_ci(
            records,
            lambda sample: spearman(sample, outcome),
            seed=seed,
            n_boot=n_boot,
        ),
        "exact_tail_descriptive": exact_tail_summary(records, outcome, seed),
    }


def run_subset(records: Sequence[dict], label: str) -> list[dict]:
    return [row for row in records if row["run"] == label]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run",
        action="append",
        nargs=3,
        metavar=("LABEL", "PRE_RAW", "COMPLETED"),
        required=True,
        help="Run label, full pre-treatment JSONL, and completed branch JSONL. Repeat per run.",
    )
    parser.add_argument("--bootstrap", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260809)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    if args.bootstrap < 0:
        raise ValueError("--bootstrap must be >= 0")

    labels: list[str] = []
    all_pre: list[dict] = []
    all_e0: list[dict] = []
    inputs: list[dict] = []
    for label, pre_name, completed_name in args.run:
        if label in labels:
            raise ValueError(f"duplicate run label: {label}")
        labels.append(label)
        pre_path = Path(pre_name)
        completed_path = Path(completed_name)
        pre_records = prepare_pre_records(label, pre_path)
        e0_records = prepare_e0_blocks(label, completed_path)
        all_pre.extend(pre_records)
        all_e0.extend(e0_records)
        inputs.append(
            {
                "label": label,
                "pre_raw": str(pre_path),
                "completed": str(completed_path),
                "n_pre": len(pre_records),
                "n_e0_blocks": len(e0_records),
            }
        )

    report = {
        "schema_version": 1,
        "study": "Pilot 0 Localization A0: criterion validity of I1 = 1 - P(correct)",
        "status": "exploratory localization using existing data; not a new confirmatory test",
        "inputs": inputs,
        "unit_rules": {
            "calibration": "one unselected pre-treatment response = one observation",
            "behavior": "one frozen prestate/block = one observation; two E0 branches are collapsed",
            "revision_rate": "number of E0 branches changing initial answer divided by 2",
            "self_correct_rate": "number of E0 branches reaching benchmark key divided by 2",
            "instability": "1 if the two E0 final answers disagree, else 0",
        },
        "pooled": {
            "calibration_discrimination": calibration_summary(all_pre, args.seed, args.bootstrap),
            "e0_revision": behavior_summary(all_e0, "revision_rate", args.seed + 10, args.bootstrap),
            "e0_self_correction": behavior_summary(
                all_e0, "self_correct_rate", args.seed + 20, args.bootstrap
            ),
            "e0_instability": behavior_summary(all_e0, "instability", args.seed + 30, args.bootstrap),
        },
        "by_run": {},
        "interpretation_guardrails": [
            "Calibration/discrimination uses the full unselected pre-treatment pools, not the initially-wrong confirmatory subset.",
            "E0 criteria are defined only on initially-wrong eligible frozen prestates represented in completed branch files.",
            "The two E0 branches within a prestate are collapsed and are not treated as independent observations.",
            "These diagnostics assess local criterion validity of I1 for observable behavior; they do not identify a latent construct called correction capacity.",
            "A0 is exploratory localization after the failed operational hypothesis and does not replace or rewrite Runs 1 or 2.",
            "No p-values are reported; bootstrap intervals summarize descriptive uncertainty only.",
        ],
    }

    for offset, label in enumerate(labels):
        pre = run_subset(all_pre, label)
        e0 = run_subset(all_e0, label)
        report["by_run"][label] = {
            "calibration_discrimination": calibration_summary(
                pre, args.seed + 1000 + offset * 100, args.bootstrap
            ),
            "e0_revision": behavior_summary(
                e0, "revision_rate", args.seed + 1010 + offset * 100, args.bootstrap
            ),
            "e0_self_correction": behavior_summary(
                e0, "self_correct_rate", args.seed + 1020 + offset * 100, args.bootstrap
            ),
            "e0_instability": behavior_summary(
                e0, "instability", args.seed + 1030 + offset * 100, args.bootstrap
            ),
        }

    text = json.dumps(report, indent=2, sort_keys=False) + "\n"
    print(text, end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

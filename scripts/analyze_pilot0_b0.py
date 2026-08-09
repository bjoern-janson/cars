#!/usr/bin/env python3
"""Analyze Pilot 0 Localization B0 manipulation validation.

Unit of analysis is one frozen prestate/block. Two matched replicates are first
averaged within each signal. The primary manipulation statistic is
M_s = P_post(s) - P_pre with prespecified ordering M_E0 >= M_EU >= M_EV.

No final-answer correctness, H1 moderation, B1 outcome, or mechanism inference
is used here. Bootstrap intervals resample whole frozen prestates.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Callable, Sequence

SIGNALS = ("E0", "EU", "EV")


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


def stdev(values: Sequence[float]) -> float | None:
    if len(values) < 2:
        return None
    m = mean(values)
    return math.sqrt(sum((x - m) ** 2 for x in values) / (len(values) - 1))


def percentile(sorted_values: Sequence[float], q: float) -> float:
    if not sorted_values:
        raise ValueError("percentile of empty sequence")
    if len(sorted_values) == 1:
        return float(sorted_values[0])
    pos = (len(sorted_values) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return float(sorted_values[lo])
    frac = pos - lo
    return float(sorted_values[lo] * (1.0 - frac) + sorted_values[hi] * frac)


def validate_and_collapse(rows: Sequence[dict], config: dict) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for line_no, row in enumerate(rows, 1):
        required = {
            "task_id",
            "replicate",
            "signal",
            "pre_state_sha256",
            "p_pre",
            "i",
            "p_post",
            "m",
            "matched_generation_seed",
        }
        missing = required - row.keys()
        if missing:
            raise ValueError(f"row {line_no}: missing {sorted(missing)}")
        signal = str(row["signal"])
        if signal not in SIGNALS:
            raise ValueError(f"row {line_no}: unsupported signal {signal!r}")
        grouped[str(row["task_id"])].append(row)

    expected_reps = int(config["design"]["replicates_per_signal"])
    expected_per_block = expected_reps * len(SIGNALS)
    blocks: list[dict] = []

    for task_id, block_rows in sorted(grouped.items()):
        if len(block_rows) != expected_per_block:
            raise ValueError(
                f"block {task_id!r}: expected {expected_per_block} rows, got {len(block_rows)}"
            )
        p_pre_values = {round(float(row["p_pre"]), 12) for row in block_rows}
        i_values = {round(float(row["i"]), 12) for row in block_rows}
        sha_values = {str(row["pre_state_sha256"]) for row in block_rows}
        if len(p_pre_values) != 1 or len(i_values) != 1 or len(sha_values) != 1:
            raise ValueError(f"block {task_id!r}: rows do not share one frozen prestate")
        p_pre = float(block_rows[0]["p_pre"])

        by_signal_rep: dict[str, dict[int, dict]] = {signal: {} for signal in SIGNALS}
        for row in block_rows:
            signal = str(row["signal"])
            rep = int(row["replicate"])
            if rep in by_signal_rep[signal]:
                raise ValueError(f"block {task_id!r}: duplicate {signal} replicate {rep}")
            by_signal_rep[signal][rep] = row
            expected_m = float(row["p_post"]) - p_pre
            if not math.isclose(float(row["m"]), expected_m, rel_tol=0.0, abs_tol=1e-12):
                raise ValueError(f"block {task_id!r}: stored M does not equal P_post-P_pre")

        expected_rep_ids = set(range(1, expected_reps + 1))
        for signal in SIGNALS:
            if set(by_signal_rep[signal]) != expected_rep_ids:
                raise ValueError(
                    f"block {task_id!r}: {signal} replicates are {sorted(by_signal_rep[signal])}; "
                    f"expected {sorted(expected_rep_ids)}"
                )

        for rep in expected_rep_ids:
            seeds = {
                int(by_signal_rep[signal][rep]["matched_generation_seed"])
                for signal in SIGNALS
            }
            if len(seeds) != 1:
                raise ValueError(
                    f"block {task_id!r} replicate {rep}: signal arms do not share one RNG seed"
                )

        record = {
            "task_id": task_id,
            "p_pre": p_pre,
            "i": float(block_rows[0]["i"]),
            "pre_state_sha256": str(block_rows[0]["pre_state_sha256"]),
        }
        for signal in SIGNALS:
            p_posts = [
                float(by_signal_rep[signal][rep]["p_post"])
                for rep in sorted(expected_rep_ids)
            ]
            p_post_mean = mean(p_posts)
            record[f"p_post_{signal}"] = p_post_mean
            record[f"m_{signal}"] = p_post_mean - p_pre
        blocks.append(record)

    if not blocks:
        raise ValueError("no complete B0 blocks")
    return blocks


def summarize(blocks: Sequence[dict]) -> dict:
    signals: dict[str, dict] = {}
    for signal in SIGNALS:
        p_posts = [float(row[f"p_post_{signal}"]) for row in blocks]
        ms = [float(row[f"m_{signal}"]) for row in blocks]
        signals[signal] = {
            "n_blocks": len(blocks),
            "mean_p_post": mean(p_posts),
            "mean_m": mean(ms),
            "sd_m_across_blocks": stdev(ms),
            "min_m": min(ms),
            "max_m": max(ms),
        }

    contrasts = {
        "E0_minus_EU": mean([float(row["m_E0"]) - float(row["m_EU"]) for row in blocks]),
        "EU_minus_EV": mean([float(row["m_EU"]) - float(row["m_EV"]) for row in blocks]),
        "E0_minus_EV": mean([float(row["m_E0"]) - float(row["m_EV"]) for row in blocks]),
    }
    return {"signals": signals, "contrasts": contrasts}


def bootstrap_intervals(
    blocks: Sequence[dict],
    *,
    seed: int,
    n_boot: int,
) -> dict:
    rng = random.Random(seed)
    values: dict[str, list[float]] = defaultdict(list)
    n = len(blocks)

    for _ in range(n_boot):
        sample = [rng.choice(blocks) for _ in range(n)]
        s = summarize(sample)
        for signal in SIGNALS:
            values[f"mean_m_{signal}"].append(float(s["signals"][signal]["mean_m"]))
        for name, value in s["contrasts"].items():
            values[name].append(float(value))

    out: dict[str, dict] = {}
    for name, xs in values.items():
        xs.sort()
        out[name] = {
            "low": percentile(xs, 0.025),
            "high": percentile(xs, 0.975),
            "valid_bootstraps": len(xs),
        }
    return out


def gate_status(summary: dict, intervals: dict) -> dict:
    c1 = float(summary["contrasts"]["E0_minus_EU"])
    c2 = float(summary["contrasts"]["EU_minus_EV"])
    c1_low = float(intervals["E0_minus_EU"]["low"])
    c2_low = float(intervals["EU_minus_EV"]["low"])

    if c1 <= 0.0 or c2 <= 0.0:
        status = "FAIL_ORDER"
        reason = "At least one adjacent mean contrast is non-positive."
    elif c1_low > 0.0 and c2_low > 0.0:
        status = "PASS"
        reason = (
            "Both adjacent mean contrasts are positive and both 95% block-bootstrap "
            "intervals lie strictly above zero."
        )
    else:
        status = "UNRESOLVED"
        reason = (
            "Adjacent means are ordered, but at least one 95% block-bootstrap interval "
            "includes zero."
        )

    return {
        "status": status,
        "reason": reason,
        "required_order": "mean(M_E0) >= mean(M_EU) >= mean(M_EV)",
        "pass_rule": (
            "PASS iff E0-EU > 0 and EU-EV > 0 and the 95% block-bootstrap lower "
            "bounds for both adjacent contrasts are > 0"
        ),
        "b1_allowed": status == "PASS",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("experiments/PILOT0_B0_CONFIG.json"),
    )
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    rows = read_jsonl(args.input)
    blocks = validate_and_collapse(rows, config)
    summary = summarize(blocks)
    n_boot = int(config["analysis"]["bootstrap"])
    boot_seed = int(config["analysis"]["bootstrap_seed"])
    intervals = bootstrap_intervals(blocks, seed=boot_seed, n_boot=n_boot)
    gate = gate_status(summary, intervals)

    report = {
        "schema_version": 1,
        "study": config["study"],
        "status": "B0 manipulation validation only; not B1 and not a test of H1",
        "input": str(args.input),
        "n_blocks": len(blocks),
        "replicates_per_signal": int(config["design"]["replicates_per_signal"]),
        "measurement": config["measurement"],
        "signal_summary": summary["signals"],
        "paired_block_contrasts": {
            name: {
                "mean": float(value),
                "bootstrap_95": intervals[name],
            }
            for name, value in summary["contrasts"].items()
        },
        "mean_m_bootstrap_95": {
            signal: intervals[f"mean_m_{signal}"] for signal in SIGNALS
        },
        "gate": gate,
        "interpretation_guardrails": [
            "P_PRE is reused from the frozen prestate and is never regenerated in B0.",
            "P_POST is measured before any answer reconsideration or revision opportunity.",
            "Two matched replicates are averaged within signal before across-block analysis.",
            "Bootstrap resampling uses whole frozen prestates/blocks.",
            "Final correctness and I1-by-signal moderation are not used to validate the manipulation.",
            "B0 PASS means only that the signal contrast is behaviorally instantiated; it does not support B, C, or H1.",
            "If B0 is UNRESOLVED or FAIL_ORDER, B1 must not run under this frozen contract.",
        ],
    }

    text = json.dumps(report, indent=2) + "\n"
    print(text, end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

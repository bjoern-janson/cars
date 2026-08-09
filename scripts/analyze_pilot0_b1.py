#!/usr/bin/env python3
"""Analyze frozen Pilot 0 Localization B1.

Primary B estimand:
    Gamma_B = Delta_V - Delta_U
where
    Delta_U = [tau_U(high) - tau_U(low)]
    Delta_V = [tau_V(high) - tau_V(low)]
and tau_s(tail) is the causal effect of signal s versus E0 within an exact I1
tail. The only primary p-value is a two-sided blocked randomization-inference
p-value for Gamma_B. Arm labels are shuffled only within frozen-prestate blocks,
preserving the observed exact 2/2/2 assignment counts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Sequence

ARMS = ("E0", "EU", "EV")


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            row = json.loads(raw)
            required = {
                "id", "task_id", "stratum", "arm", "i", "v",
                "randomization_seed", "post_base_generation_seed",
                "post_generation_seed", "signal_text",
            }
            missing = required - row.keys()
            if missing:
                raise ValueError(f"line {line_no}: missing {sorted(missing)}")
            unit_id = str(row["id"])
            if unit_id in seen:
                raise ValueError(f"line {line_no}: duplicate id {unit_id}")
            seen.add(unit_id)
            rows.append(row)
    if not rows:
        raise ValueError("no B1 rows")
    return rows


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def mean(xs: Sequence[float]) -> float:
    if not xs:
        raise ValueError("mean of empty sequence")
    return sum(xs) / len(xs)


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


def stable_seed(base_seed: int, label: str) -> int:
    digest = hashlib.sha256(label.encode("utf-8")).digest()
    offset = int.from_bytes(digest[:8], "big") % 1_000_000_000
    return (base_seed + offset) % 2_147_483_647


def stable_tie_key(seed: int, stratum: str) -> str:
    return hashlib.sha256(f"{seed}::{stratum}".encode("utf-8")).hexdigest()


def validate_rows(rows: Sequence[dict], config: dict) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    expected_randomization_seed = int(config["assignment"]["randomization_seed"])
    base_seed = int(config["invariants"]["generation_base_seed"])
    retries = int(config["invariants"]["parse_retries"])
    signals = config["signals"]

    for row in rows:
        task_id = str(row["task_id"])
        if str(row["stratum"]) != task_id:
            raise ValueError(f"branch {row['id']}: stratum != task_id")
        arm = str(row["arm"])
        if arm not in ARMS:
            raise ValueError(f"branch {row['id']}: unsupported arm {arm!r}")
        if row["signal_text"] != signals[arm]:
            raise ValueError(f"branch {row['id']}: signal text differs from frozen B1 contract")
        if int(row["randomization_seed"]) != expected_randomization_seed:
            raise ValueError(f"branch {row['id']}: wrong randomization seed")
        v = float(row["v"])
        if v not in (0.0, 1.0):
            raise ValueError(f"branch {row['id']}: V must be binary")
        expected_base = stable_seed(base_seed, f"post::{row['id']}")
        if int(row["post_base_generation_seed"]) != expected_base:
            raise ValueError(f"branch {row['id']}: post RNG base seed is not branch-id-fixed")
        used = int(row["post_generation_seed"])
        if not (expected_base <= used <= expected_base + retries):
            raise ValueError(f"branch {row['id']}: post generation seed outside allowed parse-retry range")
        grouped[task_id].append(row)

    expected_total = int(config["assignment"]["branches_per_block"])
    expected_each = int(config["assignment"]["branches_per_arm_per_block"])
    for task_id, block_rows in grouped.items():
        if len(block_rows) != expected_total:
            raise ValueError(f"block {task_id}: expected {expected_total} rows, got {len(block_rows)}")
        counts = Counter(str(row["arm"]) for row in block_rows)
        expected = {arm: expected_each for arm in ARMS}
        if dict(counts) != expected:
            raise ValueError(f"block {task_id}: arm counts {dict(counts)} != {expected}")
        i_values = {round(float(row["i"]), 12) for row in block_rows}
        if len(i_values) != 1:
            raise ValueError(f"block {task_id}: multiple I1 values")
    return dict(grouped)


def collapse_blocks(grouped: dict[str, list[dict]]) -> list[dict]:
    blocks: list[dict] = []
    for task_id, rows in sorted(grouped.items()):
        record = {"task_id": task_id, "i": float(rows[0]["i"])}
        for arm in ARMS:
            values = [float(row["v"]) for row in rows if str(row["arm"]) == arm]
            if len(values) != 2:
                raise ValueError(f"block {task_id}: expected exactly two {arm} outcomes")
            record[f"v_{arm}"] = mean(values)
        blocks.append(record)
    return blocks


def exact_tails(blocks: Sequence[dict], tie_seed: int) -> dict:
    n = len(blocks)
    q = n // 4
    if q < 1:
        raise ValueError("need at least four eligible blocks")
    ranked = sorted(
        blocks,
        key=lambda row: (float(row["i"]), stable_tie_key(tie_seed, str(row["task_id"]))),
    )
    low = list(ranked[:q])
    high = list(ranked[-q:])
    low_ids = {str(row["task_id"]) for row in low}
    high_ids = {str(row["task_id"]) for row in high}
    if low_ids & high_ids:
        raise ValueError("low/high tails overlap")
    return {
        "n_blocks": n,
        "tail_blocks": q,
        "low": low,
        "high": high,
        "low_ids": low_ids,
        "high_ids": high_ids,
        "i_low_min": min(float(row["i"]) for row in low),
        "i_low_max": max(float(row["i"]) for row in low),
        "i_high_min": min(float(row["i"]) for row in high),
        "i_high_max": max(float(row["i"]) for row in high),
        "strict_tail_ordering": max(float(row["i"]) for row in low) < min(float(row["i"]) for row in high),
        "tie_seed": tie_seed,
    }


def arm_mean(blocks: Sequence[dict], arm: str) -> float:
    return mean([float(row[f"v_{arm}"]) for row in blocks])


def estimands(all_blocks: Sequence[dict], low: Sequence[dict], high: Sequence[dict]) -> dict:
    overall = {arm: arm_mean(all_blocks, arm) for arm in ARMS}
    mu_low = {arm: arm_mean(low, arm) for arm in ARMS}
    mu_high = {arm: arm_mean(high, arm) for arm in ARMS}

    tau_u_low = mu_low["EU"] - mu_low["E0"]
    tau_u_high = mu_high["EU"] - mu_high["E0"]
    tau_v_low = mu_low["EV"] - mu_low["E0"]
    tau_v_high = mu_high["EV"] - mu_high["E0"]
    delta_u = tau_u_high - tau_u_low
    delta_v = tau_v_high - tau_v_low
    gamma = delta_v - delta_u

    return {
        "overall_arm_means": overall,
        "average_effect_U": overall["EU"] - overall["E0"],
        "average_effect_V": overall["EV"] - overall["E0"],
        "average_EV_minus_EU": overall["EV"] - overall["EU"],
        "tail_arm_means": {"low": mu_low, "high": mu_high},
        "tau_U_low": tau_u_low,
        "tau_U_high": tau_u_high,
        "tau_V_low": tau_v_low,
        "tau_V_high": tau_v_high,
        "Delta_U": delta_u,
        "Delta_V": delta_v,
        "Gamma_B": gamma,
    }


def bootstrap(
    all_blocks: Sequence[dict],
    low: Sequence[dict],
    high: Sequence[dict],
    *,
    seed: int,
    n_boot: int,
) -> dict[str, dict]:
    rng = random.Random(seed)
    values: dict[str, list[float]] = defaultdict(list)
    n_all = len(all_blocks)
    n_low = len(low)
    n_high = len(high)
    keys = (
        "average_effect_U", "average_effect_V", "average_EV_minus_EU",
        "Delta_U", "Delta_V", "Gamma_B",
    )
    for _ in range(n_boot):
        sampled_all = [rng.choice(all_blocks) for _ in range(n_all)]
        sampled_low = [rng.choice(low) for _ in range(n_low)]
        sampled_high = [rng.choice(high) for _ in range(n_high)]
        est = estimands(sampled_all, sampled_low, sampled_high)
        for key in keys:
            values[key].append(float(est[key]))

    out: dict[str, dict] = {}
    for key, xs in values.items():
        xs.sort()
        out[key] = {
            "low": percentile(xs, 0.025),
            "high": percentile(xs, 0.975),
            "valid_bootstraps": len(xs),
        }
    return out


def permute_block_rows(rows: Sequence[dict], rng: random.Random) -> list[dict]:
    labels = [str(row["arm"]) for row in rows]
    rng.shuffle(labels)
    return [dict(row, arm=label) for row, label in zip(rows, labels)]


def randomization_pvalue(
    grouped: dict[str, list[dict]],
    low_ids: set[str],
    high_ids: set[str],
    observed_gamma: float,
    *,
    seed: int,
    n_perm: int,
) -> dict:
    rng = random.Random(seed)
    extreme = 0
    valid = 0
    for _ in range(n_perm):
        permuted: dict[str, list[dict]] = {}
        for task_id, rows in grouped.items():
            permuted[task_id] = permute_block_rows(rows, rng)
        blocks = collapse_blocks(permuted)
        low = [row for row in blocks if str(row["task_id"]) in low_ids]
        high = [row for row in blocks if str(row["task_id"]) in high_ids]
        gamma = float(estimands(blocks, low, high)["Gamma_B"])
        valid += 1
        if abs(gamma) >= abs(observed_gamma):
            extreme += 1
    return {
        "permutations_requested": n_perm,
        "valid_permutations": valid,
        "two_sided_p_value_for_Gamma_B": (extreme + 1) / (valid + 1),
        "permutation_seed": seed,
        "permutation_rule": "shuffle six observed arm labels only within each block, preserving exact 2/2/2 counts",
    }


def classify(primary_p: float, gamma_ci: dict, config: dict) -> dict:
    alpha = float(config["analysis"]["alpha"])
    eps = float(config["analysis"]["equivalence_margin_for_B_weakening"])
    if primary_p < alpha:
        status = "B_GAINS_SUPPORT"
        reason = "The prespecified two-sided blocked randomization test rejects Gamma_B = 0."
    elif float(gamma_ci["low"]) > -eps and float(gamma_ci["high"]) < eps:
        status = "B_WEAKENS_AT_PRACTICAL_SCALE"
        reason = (
            "The primary test is non-significant and the 95% block-bootstrap interval for Gamma_B "
            f"lies entirely inside the prespecified equivalence region [-{eps}, +{eps}]."
        )
    else:
        status = "B_UNRESOLVED"
        reason = (
            "The primary test does not support differential moderation, but uncertainty is not "
            "narrow enough to satisfy the prespecified equivalence rule."
        )
    return {
        "status": status,
        "reason": reason,
        "alpha": alpha,
        "equivalence_margin": eps,
        "C_authority": (
            "B weakening exposes C but does not confirm C."
            if status == "B_WEAKENS_AT_PRACTICAL_SCALE"
            else "No positive authority for C follows from this gate."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--config", type=Path, default=Path("experiments/PILOT0_B1_CONFIG.json"))
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    config = load_json(args.config)
    if config.get("status") != "frozen before any B1 outcome generation":
        raise ValueError("B1 config is not the frozen pre-data contract")
    rows = read_jsonl(args.input)
    grouped = validate_rows(rows, config)
    blocks = collapse_blocks(grouped)
    tails = exact_tails(blocks, int(config["estimands"]["tail_tie_seed"]))
    observed = estimands(blocks, tails["low"], tails["high"])
    boot = bootstrap(
        blocks,
        tails["low"],
        tails["high"],
        seed=int(config["analysis"]["bootstrap_seed"]),
        n_boot=int(config["analysis"]["bootstrap"]),
    )
    ri = randomization_pvalue(
        grouped,
        tails["low_ids"],
        tails["high_ids"],
        float(observed["Gamma_B"]),
        seed=int(config["analysis"]["permutation_seed"]),
        n_perm=int(config["analysis"]["permutations"]),
    )
    gate = classify(float(ri["two_sided_p_value_for_Gamma_B"]), boot["Gamma_B"], config)

    tail_report = {
        key: value
        for key, value in tails.items()
        if key not in {"low", "high", "low_ids", "high_ids"}
    }
    report = {
        "schema_version": 1,
        "study": config["study"],
        "status": "B1 outcome localization under frozen pre-data contract",
        "input": str(args.input),
        "n_blocks": len(blocks),
        "n_rows": len(rows),
        "assignment_structure": {
            "branches_per_block": int(config["assignment"]["branches_per_block"]),
            "branches_per_arm_per_block": int(config["assignment"]["branches_per_arm_per_block"]),
            "arms": list(ARMS),
            "n_blocks": len(blocks),
        },
        "exact_block_tail_definition": tail_report,
        "estimands": observed,
        "bootstrap_95": boot,
        "primary_randomization_inference": ri,
        "B_gate": gate,
        "interpretation_guardrails": [
            "The only primary hypothesis test is the two-sided blocked randomization test for Gamma_B.",
            "Average EU/EV correction effects are supporting estimands and do not by themselves establish B.",
            "Gamma_B compares differential I1 moderation under EV versus EU; the prior forecast supplies no directional alternative.",
            "A non-significant Gamma_B does not weaken B unless the prespecified equivalence-interval rule is also satisfied.",
            "B weakening exposes C but does not confirm C; B unresolved gives C no additional authority.",
            "B0-v2 manipulation validity is historical prerequisite evidence and is not re-adjudicated using B1 outcomes.",
            "No B1 result changes CARS architecture without a separate earned revision step."
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

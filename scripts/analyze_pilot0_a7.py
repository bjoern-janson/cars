#!/usr/bin/env python3
"""Analyze frozen Pilot 0 A7 encoding x section-scaffold interaction localization.

Primary scientific unit: one initially-wrong frozen prestate block.
Primary interactions use orientation:
  Gamma_FS = (UP - UF) - (LP - LF)

Primary endpoints:
  Gamma_FS_change
  Gamma_FS_instability
  Gamma_FS_verified

Identification is from the fresh randomized factorial. Primary p-values use a
centered whole-block bootstrap for the interaction null Gamma_FS=0, then Holm
adjustment across the three co-primary interactions. A3-A6 style cell-label
permutation is intentionally not used because it would test the stronger sharp
null of no representation effects rather than the interaction null with main
effects allowed.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Sequence

from run_pilot0_local import stable_seed

CELLS = (
    "LF_E0", "LF_EV", "LP_E0", "LP_EV",
    "UF_E0", "UF_EV", "UP_E0", "UP_EV",
)
CELL_FACTORS = {
    "LF_E0": ("LF", "L", "F", "E0"),
    "LF_EV": ("LF", "L", "F", "EV"),
    "LP_E0": ("LP", "L", "P", "E0"),
    "LP_EV": ("LP", "L", "P", "EV"),
    "UF_E0": ("UF", "U", "F", "E0"),
    "UF_EV": ("UF", "U", "F", "EV"),
    "UP_E0": ("UP", "U", "P", "E0"),
    "UP_EV": ("UP", "U", "P", "EV"),
}
REPRESENTATIONS = ("LF", "LP", "UF", "UP")
PRIMARY = ("Gamma_FS_change", "Gamma_FS_instability", "Gamma_FS_verified")


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            row = json.loads(raw)
            unit_id = str(row.get("id", ""))
            if not unit_id:
                raise ValueError(f"{path}:{line_no}: missing id")
            if unit_id in seen:
                raise ValueError(f"{path}:{line_no}: duplicate id {unit_id}")
            seen.add(unit_id)
            rows.append(row)
    if not rows:
        raise ValueError(f"{path}: no rows")
    return rows


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def mean(xs: Sequence[float]) -> float:
    if not xs:
        raise ValueError("mean of empty sequence")
    return sum(xs) / len(xs)


def percentile(values: list[float], q: float) -> float:
    values = sorted(values)
    if not values:
        raise ValueError("percentile of empty sequence")
    if len(values) == 1:
        return float(values[0])
    pos = (len(values) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    if lo == hi:
        return float(values[lo])
    frac = pos - lo
    return float(values[lo] * (1.0 - frac) + values[hi] * frac)


def validate_rows(rows: Sequence[dict], config: dict) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    expected_randomization_seed = int(config["assignment"]["randomization_seed"])
    base_seed = int(config["invariants"]["generation_base_seed"])
    retries = int(config["invariants"]["parse_retries"])
    expected_each = int(config["assignment"]["branches_per_cell_per_block"])
    expected_total = int(config["assignment"]["branches_per_block"])
    signals = config["factors"]["signal"]

    for row in rows:
        task_id = str(row.get("task_id") or row.get("stratum") or "")
        if not task_id or str(row.get("stratum")) != task_id:
            raise ValueError(f"branch {row.get('id')}: invalid task_id/stratum")
        cell = str(row.get("a7_cell") or row.get("arm") or "")
        if cell not in CELLS or str(row.get("arm")) != cell:
            raise ValueError(f"branch {row.get('id')}: invalid/disagreeing A7 cell")
        rep, scaffold, encoding, signal = CELL_FACTORS[cell]
        if str(row.get("representation")) != rep:
            raise ValueError(f"branch {row['id']}: representation disagrees with cell")
        if str(row.get("scaffold")) != scaffold or str(row.get("encoding")) != encoding:
            raise ValueError(f"branch {row['id']}: representation factors disagree")
        if str(row.get("signal")) != signal:
            raise ValueError(f"branch {row['id']}: signal disagrees with cell")
        if str(row.get("signal_text")) != str(signals[signal]):
            raise ValueError(f"branch {row['id']}: signal text differs from frozen contract")
        if row.get("factorial_bridge_verified") is not True:
            raise ValueError(f"branch {row['id']}: factorial bridge provenance missing")
        if int(row.get("randomization_seed", -1)) != expected_randomization_seed:
            raise ValueError(f"branch {row['id']}: wrong randomization seed")
        v = float(row.get("v"))
        if v not in (0.0, 1.0):
            raise ValueError(f"branch {row['id']}: V must be binary")
        expected_base = stable_seed(base_seed, f"a7::{row['id']}")
        if int(row.get("post_base_generation_seed", -1)) != expected_base:
            raise ValueError(f"branch {row['id']}: generation base seed is not branch-id-fixed")
        if row.get("post_seed_rule_arm_independent") is not True:
            raise ValueError(f"branch {row['id']}: arm-independent seed provenance missing")
        used_seed = int(row.get("post_generation_seed", -1))
        if not (expected_base <= used_seed <= expected_base + retries):
            raise ValueError(f"branch {row['id']}: parse-retry seed outside frozen range")
        grouped[task_id].append(row)

    expected_rep_hash_field = {
        "LF": "lf_user_message_sha256",
        "LP": "lp_user_message_sha256",
        "UF": "uf_user_message_sha256",
        "UP": "up_user_message_sha256",
    }

    for task_id, block_rows in grouped.items():
        if len(block_rows) != expected_total:
            raise ValueError(
                f"block {task_id}: expected {expected_total} rows, got {len(block_rows)}"
            )
        counts = Counter(str(row["a7_cell"]) for row in block_rows)
        expected = {cell: expected_each for cell in CELLS}
        if dict(counts) != expected:
            raise ValueError(f"block {task_id}: cell counts {dict(counts)} != {expected}")

        initial = {str(row["initial_answer"]).strip().upper() for row in block_rows}
        benchmark = {str(row["benchmark_answer"]).strip().upper() for row in block_rows}
        prestates = {str(row["pre_state_sha256"]) for row in block_rows}
        if len(initial) != 1 or len(benchmark) != 1 or len(prestates) != 1:
            raise ValueError(f"block {task_id}: frozen prestate fields disagree")
        if next(iter(initial)) == next(iter(benchmark)):
            raise ValueError(f"block {task_id}: A7 contains initially-correct prestate")

        for signal in ("E0", "EV"):
            signal_rows = [row for row in block_rows if str(row["signal"]) == signal]
            semantic_hashes = {str(row.get("semantic_state_sha256", "")) for row in signal_rows}
            semantic_payloads = {str(row.get("semantic_state_json", "")) for row in signal_rows}
            chunk_hashes = {str(row.get("chunk_bodies_sha256", "")) for row in signal_rows}
            chunk_payloads = {str(row.get("chunk_bodies_json", "")) for row in signal_rows}
            if len(semantic_hashes) != 1 or len(semantic_payloads) != 1:
                raise ValueError(
                    f"block {task_id} signal {signal}: representation changed semantic state"
                )
            if len(chunk_hashes) != 1 or len(chunk_payloads) != 1:
                raise ValueError(
                    f"block {task_id} signal {signal}: representation changed frozen chunk bodies"
                )

        for cell in CELLS:
            cell_rows = [row for row in block_rows if str(row["a7_cell"]) == cell]
            message_hashes = {str(row.get("user_message_sha256", "")) for row in cell_rows}
            messages = {str(row.get("user_message", "")) for row in cell_rows}
            if len(message_hashes) != 1 or len(messages) != 1:
                raise ValueError(
                    f"block {task_id} {cell}: rendered message changed across replicates"
                )
            rep = CELL_FACTORS[cell][0]
            expected_field = expected_rep_hash_field[rep]
            if any(
                str(row.get("user_message_sha256", ""))
                != str(row.get(expected_field, ""))
                for row in cell_rows
            ):
                raise ValueError(f"block {task_id} {cell}: rendering provenance mismatch")

    return dict(grouped)


def representation_metrics(
    e0_rows: Sequence[dict],
    ev_rows: Sequence[dict],
    initial: str,
    benchmark: str,
) -> dict:
    if len(e0_rows) != 2 or len(ev_rows) != 2:
        raise ValueError("representation metrics require exactly two E0 and two EV rows")
    neutral_finals = [str(row["final_answer"]).strip().upper() for row in e0_rows]
    revision_count = sum(final != initial for final in neutral_finals)
    neutral_correct_count = sum(final == benchmark for final in neutral_finals)
    if neutral_correct_count > revision_count:
        raise ValueError("neutral correctness exceeds revision count")
    verified_correct_count = sum(
        str(row["final_answer"]).strip().upper() == benchmark for row in ev_rows
    )
    return {
        "revision_count": revision_count,
        "neutral_correct_count": neutral_correct_count,
        "verified_correct_count": verified_correct_count,
        "T_change": revision_count / 2.0,
        "T_instability": 1.0 if neutral_finals[0] != neutral_finals[1] else 0.0,
        "T_verified": verified_correct_count / 2.0,
        "mean_V_E0": mean([float(row["v"]) for row in e0_rows]),
        "mean_V_EV": mean([float(row["v"]) for row in ev_rows]),
    }


def interaction(up: float, uf: float, lp: float, lf: float) -> float:
    return (up - uf) - (lp - lf)


def collapse_block(task_id: str, rows: Sequence[dict]) -> dict:
    initial = str(rows[0]["initial_answer"]).strip().upper()
    benchmark = str(rows[0]["benchmark_answer"]).strip().upper()
    by_cell = {cell: [row for row in rows if str(row["a7_cell"]) == cell] for cell in CELLS}
    reps = {
        rep: representation_metrics(
            by_cell[f"{rep}_E0"], by_cell[f"{rep}_EV"], initial, benchmark
        )
        for rep in REPRESENTATIONS
    }
    return {
        "task_id": task_id,
        **reps,
        "Gamma_FS_change": interaction(
            reps["UP"]["T_change"],
            reps["UF"]["T_change"],
            reps["LP"]["T_change"],
            reps["LF"]["T_change"],
        ),
        "Gamma_FS_instability": interaction(
            reps["UP"]["T_instability"],
            reps["UF"]["T_instability"],
            reps["LP"]["T_instability"],
            reps["LF"]["T_instability"],
        ),
        "Gamma_FS_verified": interaction(
            reps["UP"]["T_verified"],
            reps["UF"]["T_verified"],
            reps["LP"]["T_verified"],
            reps["LF"]["T_verified"],
        ),
    }


def collapse_all(grouped: dict[str, list[dict]]) -> list[dict]:
    return [collapse_block(task_id, rows) for task_id, rows in sorted(grouped.items())]


def primary_estimates(blocks: Sequence[dict]) -> dict:
    return {key: mean([float(block[key]) for block in blocks]) for key in PRIMARY}


def factorial_cell_means(blocks: Sequence[dict]) -> dict:
    out = {}
    for rep in REPRESENTATIONS:
        out[rep] = {
            "T_change": mean([float(block[rep]["T_change"]) for block in blocks]),
            "T_instability": mean(
                [float(block[rep]["T_instability"]) for block in blocks]
            ),
            "T_verified": mean([float(block[rep]["T_verified"]) for block in blocks]),
            "mean_V_E0": mean([float(block[rep]["mean_V_E0"]) for block in blocks]),
            "mean_V_EV": mean([float(block[rep]["mean_V_EV"]) for block in blocks]),
        }
    return out


def qn_summary(blocks: Sequence[dict]) -> dict:
    out = {}
    for rep in REPRESENTATIONS:
        revisions = sum(int(block[rep]["revision_count"]) for block in blocks)
        correct = sum(int(block[rep]["neutral_correct_count"]) for block in blocks)
        out[rep] = {
            "revision_events": revisions,
            "correct_revision_events": correct,
            "Q_N": (correct / revisions) if revisions > 0 else None,
        }

    qs = [out[rep]["Q_N"] for rep in REPRESENTATIONS]
    if any(q is None for q in qs):
        gamma_qn = None
    else:
        gamma_qn = interaction(
            float(out["UP"]["Q_N"]),
            float(out["UF"]["Q_N"]),
            float(out["LP"]["Q_N"]),
            float(out["LF"]["Q_N"]),
        )
    out["Gamma_FS_Q_N"] = gamma_qn
    return out


def bootstrap_intervals(blocks: Sequence[dict], config: dict) -> dict:
    rng = random.Random(int(config["analysis"]["bootstrap_seed"]))
    n_boot = int(config["analysis"]["bootstrap"])
    n = len(blocks)
    primary_values = {key: [] for key in PRIMARY}
    qn_values: list[float] = []
    threshold = int(
        config["analysis"]["Q_N_min_revision_events_per_representation_cell"]
    )
    observed_qn = qn_summary(blocks)
    qn_adjudicable = all(
        int(observed_qn[rep]["revision_events"]) >= threshold for rep in REPRESENTATIONS
    )

    for _ in range(n_boot):
        sample = [rng.choice(blocks) for _ in range(n)]
        estimates = primary_estimates(sample)
        for key in PRIMARY:
            primary_values[key].append(float(estimates[key]))
        if qn_adjudicable:
            gamma_qn = qn_summary(sample)["Gamma_FS_Q_N"]
            if gamma_qn is not None and math.isfinite(float(gamma_qn)):
                qn_values.append(float(gamma_qn))

    def ci(xs: list[float]) -> dict:
        if not xs:
            return {"low": None, "high": None, "valid_bootstraps": 0}
        return {
            "low": percentile(xs, 0.025),
            "high": percentile(xs, 0.975),
            "valid_bootstraps": len(xs),
        }

    return {
        "primary": {key: ci(xs) for key, xs in primary_values.items()},
        "Q_N_interaction": ci(qn_values),
        "Q_N_observed_adjudicable": qn_adjudicable,
    }


def centered_bootstrap_pvalues(
    blocks: Sequence[dict], observed: dict, config: dict
) -> dict:
    rng = random.Random(int(config["analysis"]["bootstrap_test_seed"]))
    n_boot = int(config["analysis"]["bootstrap"])
    n = len(blocks)
    centered = {
        key: [float(block[key]) - float(observed[key]) for block in blocks]
        for key in PRIMARY
    }
    extreme = {key: 0 for key in PRIMARY}

    for _ in range(n_boot):
        idx = [rng.randrange(n) for _ in range(n)]
        for key in PRIMARY:
            null_mean = mean([centered[key][j] for j in idx])
            if abs(null_mean) >= abs(float(observed[key])):
                extreme[key] += 1

    raw = {key: (extreme[key] + 1) / (n_boot + 1) for key in PRIMARY}
    return {
        "raw_two_sided": raw,
        "holm_adjusted": holm_adjust(raw),
        "bootstrap_null_draws": n_boot,
        "bootstrap_test_seed": int(config["analysis"]["bootstrap_test_seed"]),
        "method": (
            "center each block-level interaction contrast by its observed block mean; "
            "resample whole blocks with replacement under the centered null; compare "
            "absolute null mean with absolute observed mean"
        ),
        "why_not_cell_label_permutation": config["analysis"][
            "why_not_cell_label_permutation"
        ],
    }


def holm_adjust(pvalues: dict[str, float]) -> dict[str, float]:
    ordered = sorted(pvalues.items(), key=lambda item: item[1])
    m = len(ordered)
    running = 0.0
    out: dict[str, float] = {}
    for rank, (key, p) in enumerate(ordered):
        running = max(running, min(1.0, (m - rank) * float(p)))
        out[key] = min(1.0, running)
    return out


def classify(observed: dict, boot: dict, inference: dict, config: dict) -> dict:
    alpha = float(config["analysis"]["alpha_familywise"])
    margin = float(config["analysis"]["practical_equivalence_margin"])
    adjusted = inference["holm_adjusted"]
    earned = [key for key in PRIMARY if float(adjusted[key]) < alpha]

    equivalence = {}
    interval_beyond_margin = {}
    for key in PRIMARY:
        ci = boot["primary"][key]
        lo = ci["low"]
        hi = ci["high"]
        equivalence[key] = bool(
            lo is not None
            and hi is not None
            and float(lo) > -margin
            and float(hi) < margin
        )
        interval_beyond_margin[key] = bool(
            lo is not None
            and hi is not None
            and (float(lo) > margin or float(hi) < -margin)
        )

    if earned:
        status = "CAUSAL_ENCODING_SCAFFOLD_INTERACTION_SIGNAL"
        reason = (
            "At least one prespecified encoding x scaffold interaction survives "
            "Holm familywise adjustment."
        )
    elif all(equivalence.values()):
        status = "ENCODING_SCAFFOLD_INTERACTION_WEAKENED_AT_A2_SCALE"
        reason = (
            "No primary interaction survives Holm adjustment and all three 95% "
            "whole-block bootstrap intervals lie inside the frozen +/-0.05 region."
        )
    else:
        status = "A7_UNRESOLVED"
        reason = (
            "No primary interaction survives Holm adjustment, but practical "
            "equivalence is not established for all three dimensions."
        )

    return {
        "status": status,
        "reason": reason,
        "alpha_familywise": alpha,
        "practical_equivalence_margin": margin,
        "dimensions_with_causal_signal": [
            {
                "estimand": key,
                "estimate": float(observed[key]),
                "holm_adjusted_p": float(adjusted[key]),
                "point_estimate_abs_ge_practical_margin": abs(float(observed[key]))
                >= margin,
                "bootstrap_95_entirely_beyond_practical_margin": interval_beyond_margin[
                    key
                ],
            }
            for key in earned
        ],
        "equivalence_by_primary_dimension": equivalence,
        "authority": (
            "A causal signal earns state-encoding x section-scaffold interaction "
            "authority only for the named transition dimensions under the frozen A7 assay."
            if earned
            else "No causal encoding x scaffold interaction is earned by this gate."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument(
        "--config", type=Path, default=Path("experiments/PILOT0_A7_CONFIG.json")
    )
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    config = load_json(args.config)
    if config.get("status") != "frozen before any A7 outcome generation":
        raise ValueError("A7 config is not the frozen pre-outcome contract")

    rows = read_jsonl(args.input)
    grouped = validate_rows(rows, config)
    blocks = collapse_all(grouped)
    observed = primary_estimates(blocks)
    cell_means = factorial_cell_means(blocks)
    boot = bootstrap_intervals(blocks, config)
    inference = centered_bootstrap_pvalues(blocks, observed, config)
    decision = classify(observed, boot, inference, config)

    threshold = int(
        config["analysis"]["Q_N_min_revision_events_per_representation_cell"]
    )
    qn = qn_summary(blocks)
    qn_adjudicable = bool(boot["Q_N_observed_adjudicable"])
    qn_report = {
        **qn,
        "minimum_revision_events_per_representation_cell": threshold,
        "interaction_adjudicable": qn_adjudicable,
        "bootstrap_95_Gamma_FS_Q_N": (
            boot["Q_N_interaction"]
            if qn_adjudicable
            else {"low": None, "high": None, "valid_bootstraps": 0}
        ),
    }

    report = {
        "schema_version": 1,
        "study": config["study"],
        "status": (
            "A7 randomized encoding x section-scaffold interaction localization "
            "under frozen pre-outcome contract"
        ),
        "authority": (
            "causal transition-specific representation-interaction localization; "
            "no global correction construct"
        ),
        "input": str(args.input),
        "n_blocks": len(blocks),
        "n_rows": len(rows),
        "assignment_structure": {
            "branches_per_block": int(config["assignment"]["branches_per_block"]),
            "branches_per_cell_per_block": int(
                config["assignment"]["branches_per_cell_per_block"]
            ),
            "cells": list(CELLS),
            "randomization_seed": int(config["assignment"]["randomization_seed"]),
            "rng_rule": config["assignment"]["rng_rule"],
            "rng_interpretation": config["assignment"]["rng_interpretation"],
        },
        "manipulation_boundary": config["representation_factorial"],
        "factorial_cell_endpoint_means": cell_means,
        "primary_estimands": observed,
        "primary_bootstrap_95": boot["primary"],
        "primary_interaction_inference": inference,
        "secondary": {
            "Q_N": qn_report,
        },
        "A7_gate": decision,
        "interpretation_guardrails": config["interpretation_guardrails"],
    }

    text = json.dumps(report, indent=2) + "\n"
    print(text, end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

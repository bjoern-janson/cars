#!/usr/bin/env python3
"""Analyze frozen Pilot 0 A3 randomized interface-form bundle localization.

Primary scientific unit: one initially-wrong frozen prestate block.
Primary endpoints remain transition-specific:
  Delta_J_change       = T_change(J_R,E0) - T_change(J_L,E0)
  Delta_J_instability  = T_instability(J_R,E0) - T_instability(J_L,E0)
  Delta_J_verified     = T_verified(J_R,EV) - T_verified(J_L,EV)

The only primary p-values are two-sided blocked randomization p-values for those
three effects, Holm-adjusted as one family. Q_N and the J x signal interaction
are secondary and cannot determine the A3 summary gate.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Callable, Sequence

from run_pilot0_local import stable_seed

CELLS = ("JL_E0", "JL_EV", "JR_E0", "JR_EV")
CELL_FACTORS = {
    "JL_E0": ("J_L", "E0"),
    "JL_EV": ("J_L", "EV"),
    "JR_E0": ("J_R", "E0"),
    "JR_EV": ("J_R", "EV"),
}
PRIMARY = ("Delta_J_change", "Delta_J_instability", "Delta_J_verified")


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
        if not task_id:
            raise ValueError(f"branch {row.get('id')}: missing task_id/stratum")
        if str(row.get("stratum")) != task_id:
            raise ValueError(f"branch {row['id']}: stratum != task_id")
        cell = str(row.get("a3_cell") or row.get("arm") or "")
        if cell not in CELLS:
            raise ValueError(f"branch {row['id']}: invalid A3 cell {cell!r}")
        if str(row.get("arm")) != cell:
            raise ValueError(f"branch {row['id']}: arm and a3_cell disagree")
        interface, signal = CELL_FACTORS[cell]
        if str(row.get("interface")) != interface or str(row.get("signal")) != signal:
            raise ValueError(f"branch {row['id']}: cell factor fields disagree")
        if str(row.get("signal_text")) != str(signals[signal]):
            raise ValueError(f"branch {row['id']}: signal text differs from frozen A3 contract")
        if int(row.get("randomization_seed", -1)) != expected_randomization_seed:
            raise ValueError(f"branch {row['id']}: wrong randomization seed")
        v = float(row.get("v"))
        if v not in (0.0, 1.0):
            raise ValueError(f"branch {row['id']}: V must be binary")
        expected_base = stable_seed(base_seed, f"a3::{row['id']}")
        if int(row.get("post_base_generation_seed", -1)) != expected_base:
            raise ValueError(f"branch {row['id']}: generation base seed is not branch-id-fixed")
        if row.get("post_seed_rule_arm_independent") is not True:
            raise ValueError(f"branch {row['id']}: arm-independent seed provenance flag missing")
        used_seed = int(row.get("post_generation_seed", -1))
        if not (expected_base <= used_seed <= expected_base + retries):
            raise ValueError(f"branch {row['id']}: parse-retry generation seed outside frozen range")
        grouped[task_id].append(row)

    for task_id, block_rows in grouped.items():
        if len(block_rows) != expected_total:
            raise ValueError(f"block {task_id}: expected {expected_total} rows, got {len(block_rows)}")
        counts = Counter(str(row["a3_cell"]) for row in block_rows)
        expected = {cell: expected_each for cell in CELLS}
        if dict(counts) != expected:
            raise ValueError(f"block {task_id}: cell counts {dict(counts)} != {expected}")
        initial_answers = {str(row["initial_answer"]).strip().upper() for row in block_rows}
        benchmark_answers = {str(row["benchmark_answer"]).strip().upper() for row in block_rows}
        hashes = {str(row["pre_state_sha256"]) for row in block_rows}
        if len(initial_answers) != 1 or len(benchmark_answers) != 1 or len(hashes) != 1:
            raise ValueError(f"block {task_id}: frozen prestate fields disagree")
        if next(iter(initial_answers)) == next(iter(benchmark_answers)):
            raise ValueError(f"block {task_id}: A3 contains initially-correct prestate")
    return dict(grouped)


def interface_metrics(e0_rows: Sequence[dict], ev_rows: Sequence[dict], initial: str, benchmark: str) -> dict:
    if len(e0_rows) != 2 or len(ev_rows) != 2:
        raise ValueError("interface metrics require exactly two E0 and two EV rows")
    neutral_finals = [str(row["final_answer"]).strip().upper() for row in e0_rows]
    revision_count = sum(final != initial for final in neutral_finals)
    neutral_correct_count = sum(final == benchmark for final in neutral_finals)
    if neutral_correct_count > revision_count:
        raise ValueError("neutral correctness exceeds revision count for initially-wrong prestate")
    verified_correct_count = sum(str(row["final_answer"]).strip().upper() == benchmark for row in ev_rows)
    return {
        "revision_count": revision_count,
        "neutral_correct_count": neutral_correct_count,
        "verified_correct_count": verified_correct_count,
        "T_change": revision_count / 2.0,
        "T_instability": 1.0 if neutral_finals[0] != neutral_finals[1] else 0.0,
        "T_verified": verified_correct_count / 2.0,
        "C2_neutral_self_correction": neutral_correct_count / 2.0,
        "mean_V_E0": mean([float(row["v"]) for row in e0_rows]),
        "mean_V_EV": mean([float(row["v"]) for row in ev_rows]),
    }


def collapse_block(task_id: str, rows: Sequence[dict]) -> dict:
    initial = str(rows[0]["initial_answer"]).strip().upper()
    benchmark = str(rows[0]["benchmark_answer"]).strip().upper()
    by_cell = {cell: [row for row in rows if str(row["a3_cell"]) == cell] for cell in CELLS}
    left = interface_metrics(by_cell["JL_E0"], by_cell["JL_EV"], initial, benchmark)
    right = interface_metrics(by_cell["JR_E0"], by_cell["JR_EV"], initial, benchmark)
    return {
        "task_id": task_id,
        "J_L": left,
        "J_R": right,
        "Delta_J_change": right["T_change"] - left["T_change"],
        "Delta_J_instability": right["T_instability"] - left["T_instability"],
        "Delta_J_verified": right["T_verified"] - left["T_verified"],
        "tau_E_L": left["mean_V_EV"] - left["mean_V_E0"],
        "tau_E_R": right["mean_V_EV"] - right["mean_V_E0"],
        "Gamma_JE": (right["mean_V_EV"] - right["mean_V_E0"]) - (left["mean_V_EV"] - left["mean_V_E0"]),
    }


def collapse_all(grouped: dict[str, list[dict]]) -> list[dict]:
    return [collapse_block(task_id, rows) for task_id, rows in sorted(grouped.items())]


def primary_estimates(blocks: Sequence[dict]) -> dict:
    return {key: mean([float(block[key]) for block in blocks]) for key in PRIMARY}


def qn_summary(blocks: Sequence[dict]) -> dict:
    out = {}
    for interface in ("J_L", "J_R"):
        revisions = sum(int(block[interface]["revision_count"]) for block in blocks)
        correct = sum(int(block[interface]["neutral_correct_count"]) for block in blocks)
        out[interface] = {
            "revision_events": revisions,
            "correct_revision_events": correct,
            "Q_N": (correct / revisions) if revisions > 0 else None,
        }
    ql = out["J_L"]["Q_N"]
    qr = out["J_R"]["Q_N"]
    out["difference_JR_minus_JL"] = None if ql is None or qr is None else float(qr) - float(ql)
    return out


def secondary_estimates(blocks: Sequence[dict]) -> dict:
    tau_l = mean([float(block["tau_E_L"]) for block in blocks])
    tau_r = mean([float(block["tau_E_R"]) for block in blocks])
    return {
        "tau_E_L": tau_l,
        "tau_E_R": tau_r,
        "Gamma_JE": tau_r - tau_l,
        "G_verified_minus_neutral_JL": tau_l,
        "G_verified_minus_neutral_JR": tau_r,
    }


def bootstrap(blocks: Sequence[dict], config: dict) -> dict:
    rng = random.Random(int(config["analysis"]["bootstrap_seed"]))
    n_boot = int(config["analysis"]["bootstrap"])
    n = len(blocks)
    primary_values = {key: [] for key in PRIMARY}
    secondary_values = {"Gamma_JE": [], "Q_N_interface_difference": []}
    qn_threshold = int(config["analysis"]["Q_N_min_revision_events_per_interface"])
    observed_qn = qn_summary(blocks)
    qn_adjudicable = (
        int(observed_qn["J_L"]["revision_events"]) >= qn_threshold
        and int(observed_qn["J_R"]["revision_events"]) >= qn_threshold
    )

    for _ in range(n_boot):
        sample = [rng.choice(blocks) for _ in range(n)]
        for key, value in primary_estimates(sample).items():
            primary_values[key].append(float(value))
        secondary_values["Gamma_JE"].append(float(secondary_estimates(sample)["Gamma_JE"]))
        if qn_adjudicable:
            qn = qn_summary(sample)
            diff = qn["difference_JR_minus_JL"]
            if diff is not None and math.isfinite(float(diff)):
                secondary_values["Q_N_interface_difference"].append(float(diff))

    def ci(xs: list[float]) -> dict:
        xs.sort()
        if not xs:
            return {"low": None, "high": None, "valid_bootstraps": 0}
        return {
            "low": percentile(xs, 0.025),
            "high": percentile(xs, 0.975),
            "valid_bootstraps": len(xs),
        }

    return {
        "primary": {key: ci(xs) for key, xs in primary_values.items()},
        "secondary": {key: ci(xs) for key, xs in secondary_values.items()},
        "Q_N_observed_adjudicable": qn_adjudicable,
    }


def permuted_interface_metrics(rows: Sequence[dict], rng: random.Random, signal: str, initial: str, benchmark: str) -> tuple[dict, dict]:
    signal_rows = [row for row in rows if str(row["signal"]) == signal]
    if len(signal_rows) != 4:
        raise ValueError(f"expected four {signal} rows per block")
    shuffled = list(signal_rows)
    rng.shuffle(shuffled)
    left = shuffled[:2]
    right = shuffled[2:]
    if signal == "E0":
        def neutral_metrics(group: Sequence[dict]) -> dict:
            finals = [str(row["final_answer"]).strip().upper() for row in group]
            return {
                "T_change": sum(final != initial for final in finals) / 2.0,
                "T_instability": 1.0 if finals[0] != finals[1] else 0.0,
            }
        return neutral_metrics(left), neutral_metrics(right)
    if signal == "EV":
        def verified_metrics(group: Sequence[dict]) -> dict:
            return {
                "T_verified": sum(str(row["final_answer"]).strip().upper() == benchmark for row in group) / 2.0
            }
        return verified_metrics(left), verified_metrics(right)
    raise ValueError(f"unsupported signal {signal}")


def randomization_pvalues(grouped: dict[str, list[dict]], observed: dict, config: dict) -> dict:
    rng = random.Random(int(config["analysis"]["permutation_seed"]))
    n_perm = int(config["analysis"]["permutations"])
    extreme = {key: 0 for key in PRIMARY}

    for _ in range(n_perm):
        values = {key: [] for key in PRIMARY}
        for rows in grouped.values():
            initial = str(rows[0]["initial_answer"]).strip().upper()
            benchmark = str(rows[0]["benchmark_answer"]).strip().upper()
            l0, r0 = permuted_interface_metrics(rows, rng, "E0", initial, benchmark)
            lv, rv = permuted_interface_metrics(rows, rng, "EV", initial, benchmark)
            values["Delta_J_change"].append(r0["T_change"] - l0["T_change"])
            values["Delta_J_instability"].append(r0["T_instability"] - l0["T_instability"])
            values["Delta_J_verified"].append(rv["T_verified"] - lv["T_verified"])
        for key in PRIMARY:
            stat = mean(values[key])
            if abs(stat) >= abs(float(observed[key])):
                extreme[key] += 1

    raw = {key: (extreme[key] + 1) / (n_perm + 1) for key in PRIMARY}
    return {
        "raw_two_sided": raw,
        "holm_adjusted": holm_adjust(raw),
        "permutations": n_perm,
        "permutation_seed": int(config["analysis"]["permutation_seed"]),
        "rule": "within each prestate block, condition on signal membership and shuffle J_L/J_R labels preserving exact 2/2 within E0 and exact 2/2 within EV",
    }


def holm_adjust(pvalues: dict[str, float]) -> dict[str, float]:
    ordered = sorted(pvalues.items(), key=lambda item: item[1])
    m = len(ordered)
    adjusted_sorted: list[tuple[str, float]] = []
    running = 0.0
    for rank, (key, p) in enumerate(ordered):
        candidate = min(1.0, (m - rank) * float(p))
        running = max(running, candidate)
        adjusted_sorted.append((key, min(1.0, running)))
    return dict(adjusted_sorted)


def classify(observed: dict, boot: dict, ri: dict, config: dict) -> dict:
    alpha = float(config["analysis"]["alpha_familywise"])
    margin = float(config["analysis"]["practical_equivalence_margin"])
    adjusted = ri["holm_adjusted"]
    earned = [key for key in PRIMARY if float(adjusted[key]) < alpha]
    equivalence = {}
    for key in PRIMARY:
        ci = boot["primary"][key]
        inside = (
            ci["low"] is not None
            and ci["high"] is not None
            and float(ci["low"]) > -margin
            and float(ci["high"]) < margin
        )
        equivalence[key] = bool(inside)

    if earned:
        status = "CAUSAL_INTERFACE_FORM_SIGNAL"
        reason = "At least one prespecified transition-specific interface effect survives Holm familywise adjustment."
    elif all(equivalence.values()):
        status = "INTERFACE_FORM_WEAKENED_AT_A2_SCALE"
        reason = "No primary interface effect is significant and all three 95% block-bootstrap intervals lie inside the frozen +/-0.05 practical region."
    else:
        status = "A3_UNRESOLVED"
        reason = "No primary interface effect survives Holm adjustment, but practical equivalence is not established for all three primary dimensions."

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
            }
            for key in earned
        ],
        "equivalence_by_primary_dimension": equivalence,
        "authority": (
            "A causal signal earns interface presentation form as a causal layer only for the named transition dimensions."
            if status == "CAUSAL_INTERFACE_FORM_SIGNAL"
            else "No causal interface-form layer is earned by this gate."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--config", type=Path, default=Path("experiments/PILOT0_A3_CONFIG.json"))
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    config = load_json(args.config)
    if config.get("status") != "frozen before any A3 outcome generation":
        raise ValueError("A3 config is not the frozen pre-outcome contract")
    rows = read_jsonl(args.input)
    grouped = validate_rows(rows, config)
    blocks = collapse_all(grouped)
    observed = primary_estimates(blocks)
    secondary = secondary_estimates(blocks)
    qn = qn_summary(blocks)
    boot = bootstrap(blocks, config)
    ri = randomization_pvalues(grouped, observed, config)
    decision = classify(observed, boot, ri, config)

    qn_threshold = int(config["analysis"]["Q_N_min_revision_events_per_interface"])
    qn_adjudicable = bool(boot["Q_N_observed_adjudicable"])
    qn_report = {
        **qn,
        "minimum_revision_events_per_interface": qn_threshold,
        "adjudicable": qn_adjudicable,
        "bootstrap_95_difference_JR_minus_JL": (
            boot["secondary"]["Q_N_interface_difference"]
            if qn_adjudicable
            else {"low": None, "high": None, "valid_bootstraps": 0}
        ),
    }

    report = {
        "schema_version": 1,
        "study": config["study"],
        "status": "A3 randomized interface-form bundle localization under frozen pre-outcome contract",
        "authority": "causal transition-specific interface localization; no global correction construct",
        "input": str(args.input),
        "n_blocks": len(blocks),
        "n_rows": len(rows),
        "assignment_structure": {
            "branches_per_block": int(config["assignment"]["branches_per_block"]),
            "branches_per_cell_per_block": int(config["assignment"]["branches_per_cell_per_block"]),
            "cells": list(CELLS),
            "randomization_seed": int(config["assignment"]["randomization_seed"]),
            "rng_rule": config["assignment"]["rng_rule"],
            "rng_interpretation": config["assignment"]["rng_interpretation"],
        },
        "interface_boundary": config["factors"]["interface"]["boundary"],
        "primary_estimands": observed,
        "primary_bootstrap_95": boot["primary"],
        "primary_randomization_inference": ri,
        "secondary": {
            **secondary,
            "Gamma_JE_bootstrap_95": boot["secondary"]["Gamma_JE"],
            "Q_N": qn_report,
        },
        "A3_gate": decision,
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

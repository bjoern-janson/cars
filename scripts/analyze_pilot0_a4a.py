#!/usr/bin/env python3
"""Analyze frozen Pilot 0 A4a conversational-topology localization.

Primary scientific unit: one initially-wrong frozen prestate block.
Primary endpoints:
  Delta_K_change       = T_change(K_history,E0) - T_change(K_inline,E0)
  Delta_K_instability  = T_instability(K_history,E0) - T_instability(K_inline,E0)
  Delta_K_verified     = T_verified(K_history,EV) - T_verified(K_inline,EV)

The only primary p-values are two-sided blocked randomization p-values for those
three effects, Holm-adjusted as one family. Q_N and Gamma_KE are secondary.
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

CELLS = ("KI_E0", "KI_EV", "KH_E0", "KH_EV")
CELL_FACTORS = {
    "KI_E0": ("K_inline", "E0"),
    "KI_EV": ("K_inline", "EV"),
    "KH_E0": ("K_history", "E0"),
    "KH_EV": ("K_history", "EV"),
}
PRIMARY = ("Delta_K_change", "Delta_K_instability", "Delta_K_verified")


def read_jsonl(path: Path) -> list[dict]:
    rows, seen = [], set()
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
    if len(values) == 1:
        return values[0]
    pos = (len(values) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    if lo == hi:
        return values[lo]
    frac = pos - lo
    return values[lo] * (1.0 - frac) + values[hi] * frac


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
        cell = str(row.get("a4a_cell") or row.get("arm") or "")
        if cell not in CELLS or str(row.get("arm")) != cell:
            raise ValueError(f"branch {row.get('id')}: invalid/disagreeing A4a cell")
        topology, signal = CELL_FACTORS[cell]
        if str(row.get("topology")) != topology or str(row.get("signal")) != signal:
            raise ValueError(f"branch {row['id']}: cell factors disagree")
        if str(row.get("signal_text")) != str(signals[signal]):
            raise ValueError(f"branch {row['id']}: signal text differs from frozen contract")
        if row.get("lexical_identity_verified") is not True:
            raise ValueError(f"branch {row['id']}: lexical identity provenance missing")
        if int(row.get("randomization_seed", -1)) != expected_randomization_seed:
            raise ValueError(f"branch {row['id']}: wrong randomization seed")
        v = float(row.get("v"))
        if v not in (0.0, 1.0):
            raise ValueError(f"branch {row['id']}: V must be binary")
        expected_base = stable_seed(base_seed, f"a4a::{row['id']}")
        if int(row.get("post_base_generation_seed", -1)) != expected_base:
            raise ValueError(f"branch {row['id']}: generation base seed is not branch-id-fixed")
        if row.get("post_seed_rule_arm_independent") is not True:
            raise ValueError(f"branch {row['id']}: arm-independent seed provenance missing")
        used_seed = int(row.get("post_generation_seed", -1))
        if not (expected_base <= used_seed <= expected_base + retries):
            raise ValueError(f"branch {row['id']}: parse-retry seed outside frozen range")
        grouped[task_id].append(row)

    for task_id, block_rows in grouped.items():
        if len(block_rows) != expected_total:
            raise ValueError(f"block {task_id}: expected {expected_total} rows, got {len(block_rows)}")
        counts = Counter(str(row["a4a_cell"]) for row in block_rows)
        expected = {cell: expected_each for cell in CELLS}
        if dict(counts) != expected:
            raise ValueError(f"block {task_id}: cell counts {dict(counts)} != {expected}")
        initial = {str(row["initial_answer"]).strip().upper() for row in block_rows}
        benchmark = {str(row["benchmark_answer"]).strip().upper() for row in block_rows}
        hashes = {str(row["pre_state_sha256"]) for row in block_rows}
        if len(initial) != 1 or len(benchmark) != 1 or len(hashes) != 1:
            raise ValueError(f"block {task_id}: frozen prestate fields disagree")
        if next(iter(initial)) == next(iter(benchmark)):
            raise ValueError(f"block {task_id}: A4a contains initially-correct prestate")
        for signal in ("E0", "EV"):
            signal_rows = [row for row in block_rows if str(row["signal"]) == signal]
            canonical_hashes = {str(row.get("canonical_content_sha256", "")) for row in signal_rows}
            canonical_texts = {str(row.get("canonical_text", "")) for row in signal_rows}
            if len(canonical_hashes) != 1 or len(canonical_texts) != 1:
                raise ValueError(f"block {task_id} signal {signal}: topology changed canonical content")
    return dict(grouped)


def topology_metrics(e0_rows: Sequence[dict], ev_rows: Sequence[dict], initial: str, benchmark: str) -> dict:
    if len(e0_rows) != 2 or len(ev_rows) != 2:
        raise ValueError("topology metrics require exactly two E0 and two EV rows")
    neutral_finals = [str(row["final_answer"]).strip().upper() for row in e0_rows]
    revision_count = sum(final != initial for final in neutral_finals)
    neutral_correct_count = sum(final == benchmark for final in neutral_finals)
    if neutral_correct_count > revision_count:
        raise ValueError("neutral correctness exceeds revision count")
    verified_correct_count = sum(str(row["final_answer"]).strip().upper() == benchmark for row in ev_rows)
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


def collapse_block(task_id: str, rows: Sequence[dict]) -> dict:
    initial = str(rows[0]["initial_answer"]).strip().upper()
    benchmark = str(rows[0]["benchmark_answer"]).strip().upper()
    by_cell = {cell: [row for row in rows if str(row["a4a_cell"]) == cell] for cell in CELLS}
    inline = topology_metrics(by_cell["KI_E0"], by_cell["KI_EV"], initial, benchmark)
    history = topology_metrics(by_cell["KH_E0"], by_cell["KH_EV"], initial, benchmark)
    tau_i = inline["mean_V_EV"] - inline["mean_V_E0"]
    tau_h = history["mean_V_EV"] - history["mean_V_E0"]
    return {
        "task_id": task_id,
        "K_inline": inline,
        "K_history": history,
        "Delta_K_change": history["T_change"] - inline["T_change"],
        "Delta_K_instability": history["T_instability"] - inline["T_instability"],
        "Delta_K_verified": history["T_verified"] - inline["T_verified"],
        "tau_E_inline": tau_i,
        "tau_E_history": tau_h,
        "Gamma_KE": tau_h - tau_i,
    }


def collapse_all(grouped: dict[str, list[dict]]) -> list[dict]:
    return [collapse_block(task_id, rows) for task_id, rows in sorted(grouped.items())]


def primary_estimates(blocks: Sequence[dict]) -> dict:
    return {key: mean([float(block[key]) for block in blocks]) for key in PRIMARY}


def qn_summary(blocks: Sequence[dict]) -> dict:
    out = {}
    for topology in ("K_inline", "K_history"):
        revisions = sum(int(block[topology]["revision_count"]) for block in blocks)
        correct = sum(int(block[topology]["neutral_correct_count"]) for block in blocks)
        out[topology] = {
            "revision_events": revisions,
            "correct_revision_events": correct,
            "Q_N": (correct / revisions) if revisions > 0 else None,
        }
    qi = out["K_inline"]["Q_N"]
    qh = out["K_history"]["Q_N"]
    out["difference_history_minus_inline"] = None if qi is None or qh is None else float(qh) - float(qi)
    return out


def secondary_estimates(blocks: Sequence[dict]) -> dict:
    tau_i = mean([float(block["tau_E_inline"]) for block in blocks])
    tau_h = mean([float(block["tau_E_history"]) for block in blocks])
    return {
        "tau_E_inline": tau_i,
        "tau_E_history": tau_h,
        "Gamma_KE": tau_h - tau_i,
        "G_verified_minus_neutral_inline": tau_i,
        "G_verified_minus_neutral_history": tau_h,
    }


def bootstrap(blocks: Sequence[dict], config: dict) -> dict:
    rng = random.Random(int(config["analysis"]["bootstrap_seed"]))
    n_boot = int(config["analysis"]["bootstrap"])
    n = len(blocks)
    primary_values = {key: [] for key in PRIMARY}
    gamma_values, qn_values = [], []
    threshold = int(config["analysis"]["Q_N_min_revision_events_per_topology"])
    observed_qn = qn_summary(blocks)
    qn_adjudicable = (
        int(observed_qn["K_inline"]["revision_events"]) >= threshold
        and int(observed_qn["K_history"]["revision_events"]) >= threshold
    )
    for _ in range(n_boot):
        sample = [rng.choice(blocks) for _ in range(n)]
        estimates = primary_estimates(sample)
        for key in PRIMARY:
            primary_values[key].append(float(estimates[key]))
        gamma_values.append(float(secondary_estimates(sample)["Gamma_KE"]))
        if qn_adjudicable:
            diff = qn_summary(sample)["difference_history_minus_inline"]
            if diff is not None and math.isfinite(float(diff)):
                qn_values.append(float(diff))

    def ci(xs: list[float]) -> dict:
        if not xs:
            return {"low": None, "high": None, "valid_bootstraps": 0}
        return {"low": percentile(xs, 0.025), "high": percentile(xs, 0.975), "valid_bootstraps": len(xs)}

    return {
        "primary": {key: ci(xs) for key, xs in primary_values.items()},
        "Gamma_KE": ci(gamma_values),
        "Q_N_difference": ci(qn_values),
        "Q_N_observed_adjudicable": qn_adjudicable,
    }


def permuted_metrics(rows: Sequence[dict], rng: random.Random, signal: str, initial: str, benchmark: str) -> tuple[dict, dict]:
    signal_rows = [row for row in rows if str(row["signal"]) == signal]
    if len(signal_rows) != 4:
        raise ValueError(f"expected four {signal} rows per block")
    shuffled = list(signal_rows)
    rng.shuffle(shuffled)
    inline, history = shuffled[:2], shuffled[2:]
    if signal == "E0":
        def neutral(group: Sequence[dict]) -> dict:
            finals = [str(row["final_answer"]).strip().upper() for row in group]
            return {
                "T_change": sum(final != initial for final in finals) / 2.0,
                "T_instability": 1.0 if finals[0] != finals[1] else 0.0,
            }
        return neutral(inline), neutral(history)
    def verified(group: Sequence[dict]) -> dict:
        return {"T_verified": sum(str(row["final_answer"]).strip().upper() == benchmark for row in group) / 2.0}
    return verified(inline), verified(history)


def randomization_pvalues(grouped: dict[str, list[dict]], observed: dict, config: dict) -> dict:
    rng = random.Random(int(config["analysis"]["permutation_seed"]))
    n_perm = int(config["analysis"]["permutations"])
    extreme = {key: 0 for key in PRIMARY}
    for _ in range(n_perm):
        values = {key: [] for key in PRIMARY}
        for rows in grouped.values():
            initial = str(rows[0]["initial_answer"]).strip().upper()
            benchmark = str(rows[0]["benchmark_answer"]).strip().upper()
            i0, h0 = permuted_metrics(rows, rng, "E0", initial, benchmark)
            iv, hv = permuted_metrics(rows, rng, "EV", initial, benchmark)
            values["Delta_K_change"].append(h0["T_change"] - i0["T_change"])
            values["Delta_K_instability"].append(h0["T_instability"] - i0["T_instability"])
            values["Delta_K_verified"].append(hv["T_verified"] - iv["T_verified"])
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
        "rule": "within each prestate block, condition on signal and shuffle K_inline/K_history labels preserving exact 2/2 within E0 and exact 2/2 within EV",
    }


def holm_adjust(pvalues: dict[str, float]) -> dict[str, float]:
    ordered = sorted(pvalues.items(), key=lambda item: item[1])
    m, running, out = len(ordered), 0.0, {}
    for rank, (key, p) in enumerate(ordered):
        running = max(running, min(1.0, (m - rank) * float(p)))
        out[key] = min(1.0, running)
    return out


def classify(observed: dict, boot: dict, ri: dict, config: dict) -> dict:
    alpha = float(config["analysis"]["alpha_familywise"])
    margin = float(config["analysis"]["practical_equivalence_margin"])
    adjusted = ri["holm_adjusted"]
    earned = [key for key in PRIMARY if float(adjusted[key]) < alpha]
    equivalence = {}
    for key in PRIMARY:
        ci = boot["primary"][key]
        equivalence[key] = bool(
            ci["low"] is not None and ci["high"] is not None
            and float(ci["low"]) > -margin and float(ci["high"]) < margin
        )
    if earned:
        status = "CAUSAL_CONVERSATIONAL_TOPOLOGY_SIGNAL"
        reason = "At least one prespecified topology effect survives Holm familywise adjustment."
    elif all(equivalence.values()):
        status = "CONVERSATIONAL_TOPOLOGY_WEAKENED_AT_A2_SCALE"
        reason = "No primary topology effect is significant and all three 95% block-bootstrap intervals lie inside the frozen +/-0.05 practical region."
    else:
        status = "A4A_UNRESOLVED"
        reason = "No primary topology effect survives Holm adjustment, but practical equivalence is not established for all three dimensions."
    return {
        "status": status,
        "reason": reason,
        "alpha_familywise": alpha,
        "practical_equivalence_margin": margin,
        "dimensions_with_causal_signal": [
            {"estimand": key, "estimate": float(observed[key]), "holm_adjusted_p": float(adjusted[key])}
            for key in earned
        ],
        "equivalence_by_primary_dimension": equivalence,
        "authority": (
            "A causal signal earns conversational role/turn topology as a causal component only for the named transition dimensions."
            if earned else "No causal conversational-topology component is earned by this gate."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--config", type=Path, default=Path("experiments/PILOT0_A4A_CONFIG.json"))
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    config = load_json(args.config)
    if config.get("status") != "frozen before any A4a outcome generation":
        raise ValueError("A4a config is not the frozen pre-outcome contract")
    rows = read_jsonl(args.input)
    grouped = validate_rows(rows, config)
    blocks = collapse_all(grouped)
    observed = primary_estimates(blocks)
    secondary = secondary_estimates(blocks)
    qn = qn_summary(blocks)
    boot = bootstrap(blocks, config)
    ri = randomization_pvalues(grouped, observed, config)
    decision = classify(observed, boot, ri, config)

    threshold = int(config["analysis"]["Q_N_min_revision_events_per_topology"])
    qn_adjudicable = bool(boot["Q_N_observed_adjudicable"])
    qn_report = {
        **qn,
        "minimum_revision_events_per_topology": threshold,
        "adjudicable": qn_adjudicable,
        "bootstrap_95_difference_history_minus_inline": (
            boot["Q_N_difference"] if qn_adjudicable
            else {"low": None, "high": None, "valid_bootstraps": 0}
        ),
    }

    report = {
        "schema_version": 1,
        "study": config["study"],
        "status": "A4a randomized conversational-topology localization under frozen pre-outcome contract",
        "authority": "causal transition-specific component localization; no global correction construct",
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
        "manipulation_boundary": config["canonical_content"],
        "primary_estimands": observed,
        "primary_bootstrap_95": boot["primary"],
        "primary_randomization_inference": ri,
        "secondary": {
            **secondary,
            "Gamma_KE_bootstrap_95": boot["Gamma_KE"],
            "Q_N": qn_report,
        },
        "A4a_gate": decision,
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

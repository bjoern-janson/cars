#!/usr/bin/env python3
"""Analyze frozen Pilot 0 A5 prior-state field/prose encoding localization.

Primary scientific unit: one initially-wrong frozen prestate block.
Primary endpoints:
  Delta_R_change       = T_change(R_prose,E0) - T_change(R_fields,E0)
  Delta_R_instability  = T_instability(R_prose,E0) - T_instability(R_fields,E0)
  Delta_R_verified     = T_verified(R_prose,EV) - T_verified(R_fields,EV)

The only primary p-values are two-sided blocked randomization p-values for those
three effects, Holm-adjusted as one family. Q_N and Gamma_RE are secondary.
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

CELLS = ("RF_E0", "RF_EV", "RP_E0", "RP_EV")
CELL_FACTORS = {
    "RF_E0": ("R_fields", "E0"),
    "RF_EV": ("R_fields", "EV"),
    "RP_E0": ("R_prose", "E0"),
    "RP_EV": ("R_prose", "EV"),
}
PRIMARY = ("Delta_R_change", "Delta_R_instability", "Delta_R_verified")


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
        cell = str(row.get("a5_cell") or row.get("arm") or "")
        if cell not in CELLS or str(row.get("arm")) != cell:
            raise ValueError(f"branch {row.get('id')}: invalid/disagreeing A5 cell")
        encoding, signal = CELL_FACTORS[cell]
        if str(row.get("encoding")) != encoding or str(row.get("signal")) != signal:
            raise ValueError(f"branch {row['id']}: cell factors disagree")
        if str(row.get("signal_text")) != str(signals[signal]):
            raise ValueError(f"branch {row['id']}: signal text differs from frozen contract")
        if row.get("encoding_bridge_verified") is not True:
            raise ValueError(f"branch {row['id']}: encoding bridge provenance missing")
        if int(row.get("randomization_seed", -1)) != expected_randomization_seed:
            raise ValueError(f"branch {row['id']}: wrong randomization seed")
        v = float(row.get("v"))
        if v not in (0.0, 1.0):
            raise ValueError(f"branch {row['id']}: V must be binary")
        expected_base = stable_seed(base_seed, f"a5::{row['id']}")
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
        counts = Counter(str(row["a5_cell"]) for row in block_rows)
        expected = {cell: expected_each for cell in CELLS}
        if dict(counts) != expected:
            raise ValueError(f"block {task_id}: cell counts {dict(counts)} != {expected}")

        initial = {str(row["initial_answer"]).strip().upper() for row in block_rows}
        benchmark = {str(row["benchmark_answer"]).strip().upper() for row in block_rows}
        prestates = {str(row["pre_state_sha256"]) for row in block_rows}
        if len(initial) != 1 or len(benchmark) != 1 or len(prestates) != 1:
            raise ValueError(f"block {task_id}: frozen prestate fields disagree")
        if next(iter(initial)) == next(iter(benchmark)):
            raise ValueError(f"block {task_id}: A5 contains initially-correct prestate")

        for signal in ("E0", "EV"):
            signal_rows = [row for row in block_rows if str(row["signal"]) == signal]
            semantic_hashes = {str(row.get("semantic_state_sha256", "")) for row in signal_rows}
            semantic_payloads = {str(row.get("semantic_state_json", "")) for row in signal_rows}
            scaffold_hashes = {str(row.get("outer_scaffold_sha256", "")) for row in signal_rows}
            scaffold_payloads = {str(row.get("outer_scaffold_json", "")) for row in signal_rows}
            if len(semantic_hashes) != 1 or len(semantic_payloads) != 1:
                raise ValueError(f"block {task_id} signal {signal}: encoding changed semantic state")
            if len(scaffold_hashes) != 1 or len(scaffold_payloads) != 1:
                raise ValueError(f"block {task_id} signal {signal}: encoding changed outer scaffold")

        for cell in CELLS:
            cell_rows = [row for row in block_rows if str(row["a5_cell"]) == cell]
            message_hashes = {str(row.get("user_message_sha256", "")) for row in cell_rows}
            messages = {str(row.get("user_message", "")) for row in cell_rows}
            if len(message_hashes) != 1 or len(messages) != 1:
                raise ValueError(f"block {task_id} {cell}: rendering changed across replicated branches")

        fields_rows = [row for row in block_rows if str(row["encoding"]) == "R_fields"]
        prose_rows = [row for row in block_rows if str(row["encoding"]) == "R_prose"]
        if any(
            str(row.get("user_message_sha256", "")) != str(row.get("fields_user_message_sha256", ""))
            for row in fields_rows
        ):
            raise ValueError(f"block {task_id}: R_fields provenance mismatch")
        if any(
            str(row.get("user_message_sha256", "")) != str(row.get("prose_user_message_sha256", ""))
            for row in prose_rows
        ):
            raise ValueError(f"block {task_id}: R_prose provenance mismatch")

    return dict(grouped)


def encoding_metrics(e0_rows: Sequence[dict], ev_rows: Sequence[dict], initial: str, benchmark: str) -> dict:
    if len(e0_rows) != 2 or len(ev_rows) != 2:
        raise ValueError("encoding metrics require exactly two E0 and two EV rows")
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


def collapse_block(task_id: str, rows: Sequence[dict]) -> dict:
    initial = str(rows[0]["initial_answer"]).strip().upper()
    benchmark = str(rows[0]["benchmark_answer"]).strip().upper()
    by_cell = {cell: [row for row in rows if str(row["a5_cell"]) == cell] for cell in CELLS}
    fields = encoding_metrics(by_cell["RF_E0"], by_cell["RF_EV"], initial, benchmark)
    prose = encoding_metrics(by_cell["RP_E0"], by_cell["RP_EV"], initial, benchmark)
    tau_f = fields["mean_V_EV"] - fields["mean_V_E0"]
    tau_p = prose["mean_V_EV"] - prose["mean_V_E0"]
    return {
        "task_id": task_id,
        "R_fields": fields,
        "R_prose": prose,
        "Delta_R_change": prose["T_change"] - fields["T_change"],
        "Delta_R_instability": prose["T_instability"] - fields["T_instability"],
        "Delta_R_verified": prose["T_verified"] - fields["T_verified"],
        "tau_E_fields": tau_f,
        "tau_E_prose": tau_p,
        "Gamma_RE": tau_p - tau_f,
    }


def collapse_all(grouped: dict[str, list[dict]]) -> list[dict]:
    return [collapse_block(task_id, rows) for task_id, rows in sorted(grouped.items())]


def primary_estimates(blocks: Sequence[dict]) -> dict:
    return {key: mean([float(block[key]) for block in blocks]) for key in PRIMARY}


def qn_summary(blocks: Sequence[dict]) -> dict:
    out = {}
    for encoding in ("R_fields", "R_prose"):
        revisions = sum(int(block[encoding]["revision_count"]) for block in blocks)
        correct = sum(int(block[encoding]["neutral_correct_count"]) for block in blocks)
        out[encoding] = {
            "revision_events": revisions,
            "correct_revision_events": correct,
            "Q_N": (correct / revisions) if revisions > 0 else None,
        }
    qf = out["R_fields"]["Q_N"]
    qp = out["R_prose"]["Q_N"]
    out["difference_prose_minus_fields"] = None if qf is None or qp is None else float(qp) - float(qf)
    return out


def secondary_estimates(blocks: Sequence[dict]) -> dict:
    tau_f = mean([float(block["tau_E_fields"]) for block in blocks])
    tau_p = mean([float(block["tau_E_prose"]) for block in blocks])
    return {
        "tau_E_fields": tau_f,
        "tau_E_prose": tau_p,
        "Gamma_RE": tau_p - tau_f,
        "G_verified_minus_neutral_fields": tau_f,
        "G_verified_minus_neutral_prose": tau_p,
    }


def bootstrap(blocks: Sequence[dict], config: dict) -> dict:
    rng = random.Random(int(config["analysis"]["bootstrap_seed"]))
    n_boot = int(config["analysis"]["bootstrap"])
    n = len(blocks)
    primary_values = {key: [] for key in PRIMARY}
    gamma_values: list[float] = []
    qn_values: list[float] = []
    threshold = int(config["analysis"]["Q_N_min_revision_events_per_encoding"])
    observed_qn = qn_summary(blocks)
    qn_adjudicable = (
        int(observed_qn["R_fields"]["revision_events"]) >= threshold
        and int(observed_qn["R_prose"]["revision_events"]) >= threshold
    )

    for _ in range(n_boot):
        sample = [rng.choice(blocks) for _ in range(n)]
        estimates = primary_estimates(sample)
        for key in PRIMARY:
            primary_values[key].append(float(estimates[key]))
        gamma_values.append(float(secondary_estimates(sample)["Gamma_RE"]))
        if qn_adjudicable:
            diff = qn_summary(sample)["difference_prose_minus_fields"]
            if diff is not None and math.isfinite(float(diff)):
                qn_values.append(float(diff))

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
        "Gamma_RE": ci(gamma_values),
        "Q_N_difference": ci(qn_values),
        "Q_N_observed_adjudicable": qn_adjudicable,
    }


def permuted_metrics(
    rows: Sequence[dict],
    rng: random.Random,
    signal: str,
    initial: str,
    benchmark: str,
) -> tuple[dict, dict]:
    signal_rows = [row for row in rows if str(row["signal"]) == signal]
    if len(signal_rows) != 4:
        raise ValueError(f"expected four {signal} rows per block")
    shuffled = list(signal_rows)
    rng.shuffle(shuffled)
    fields, prose = shuffled[:2], shuffled[2:]
    if signal == "E0":
        def neutral(group: Sequence[dict]) -> dict:
            finals = [str(row["final_answer"]).strip().upper() for row in group]
            return {
                "T_change": sum(final != initial for final in finals) / 2.0,
                "T_instability": 1.0 if finals[0] != finals[1] else 0.0,
            }
        return neutral(fields), neutral(prose)

    def verified(group: Sequence[dict]) -> dict:
        return {
            "T_verified": sum(
                str(row["final_answer"]).strip().upper() == benchmark for row in group
            ) / 2.0
        }
    return verified(fields), verified(prose)


def randomization_pvalues(grouped: dict[str, list[dict]], observed: dict, config: dict) -> dict:
    rng = random.Random(int(config["analysis"]["permutation_seed"]))
    n_perm = int(config["analysis"]["permutations"])
    extreme = {key: 0 for key in PRIMARY}

    for _ in range(n_perm):
        values = {key: [] for key in PRIMARY}
        for rows in grouped.values():
            initial = str(rows[0]["initial_answer"]).strip().upper()
            benchmark = str(rows[0]["benchmark_answer"]).strip().upper()
            f0, p0 = permuted_metrics(rows, rng, "E0", initial, benchmark)
            fv, pv = permuted_metrics(rows, rng, "EV", initial, benchmark)
            values["Delta_R_change"].append(p0["T_change"] - f0["T_change"])
            values["Delta_R_instability"].append(p0["T_instability"] - f0["T_instability"])
            values["Delta_R_verified"].append(pv["T_verified"] - fv["T_verified"])
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
        "rule": (
            "within each prestate block, condition on signal and shuffle "
            "R_fields/R_prose labels preserving exact 2/2 within E0 and exact 2/2 within EV"
        ),
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
        status = "CAUSAL_PRIOR_STATE_ENCODING_SIGNAL"
        reason = "At least one prespecified prior-state encoding effect survives Holm familywise adjustment."
    elif all(equivalence.values()):
        status = "PRIOR_STATE_ENCODING_WEAKENED_AT_A2_SCALE"
        reason = (
            "No primary encoding effect is significant and all three 95% block-bootstrap "
            "intervals lie inside the frozen +/-0.05 practical region."
        )
    else:
        status = "A5_UNRESOLVED"
        reason = (
            "No primary encoding effect survives Holm adjustment, but practical equivalence "
            "is not established for all three dimensions."
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
                "point_estimate_abs_ge_practical_margin": abs(float(observed[key])) >= margin,
            }
            for key in earned
        ],
        "equivalence_by_primary_dimension": equivalence,
        "authority": (
            "A causal signal earns prior-state field-versus-prose encoding as a causal "
            "component only for the named transition dimensions; causal difference does "
            "not imply practical magnitude >= the frozen margin."
            if earned
            else "No causal prior-state encoding component is earned by this gate."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--config", type=Path, default=Path("experiments/PILOT0_A5_CONFIG.json"))
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    config = load_json(args.config)
    if config.get("status") != "frozen before any A5 outcome generation":
        raise ValueError("A5 config is not the frozen pre-outcome contract")
    rows = read_jsonl(args.input)
    grouped = validate_rows(rows, config)
    blocks = collapse_all(grouped)
    observed = primary_estimates(blocks)
    secondary = secondary_estimates(blocks)
    qn = qn_summary(blocks)
    boot = bootstrap(blocks, config)
    ri = randomization_pvalues(grouped, observed, config)
    decision = classify(observed, boot, ri, config)

    threshold = int(config["analysis"]["Q_N_min_revision_events_per_encoding"])
    qn_adjudicable = bool(boot["Q_N_observed_adjudicable"])
    qn_report = {
        **qn,
        "minimum_revision_events_per_encoding": threshold,
        "adjudicable": qn_adjudicable,
        "bootstrap_95_difference_prose_minus_fields": (
            boot["Q_N_difference"] if qn_adjudicable
            else {"low": None, "high": None, "valid_bootstraps": 0}
        ),
    }

    report = {
        "schema_version": 1,
        "study": config["study"],
        "status": "A5 randomized prior-state field/prose encoding localization under frozen pre-outcome contract",
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
        "manipulation_boundary": {
            "fixed_scaffold": config["fixed_scaffold"],
            "encoding_factor": config["encoding_factor"],
        },
        "primary_estimands": observed,
        "primary_bootstrap_95": boot["primary"],
        "primary_randomization_inference": ri,
        "secondary": {
            **secondary,
            "Gamma_RE_bootstrap_95": boot["Gamma_RE"],
            "Q_N": qn_report,
        },
        "A5_gate": decision,
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

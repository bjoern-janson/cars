#!/usr/bin/env python3
"""Plumbing-only audit for frozen A1-D realized-choice extraction.

This checker reads extraction records only. It does not accept correction outcome
files and does not inspect any association between S/I1 and later behavior.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

import torch

FORBIDDEN_OUTCOME_FIELDS = {
    "final_answer",
    "final_correct",
    "v",
    "revision_rate",
    "self_correct_rate",
    "instability",
    "arm",
    "signal",
    "signal_text",
}


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            row = json.loads(raw)
            task_id = str(row.get("task_id", ""))
            if not task_id:
                raise ValueError(f"{path}:{line_no}: missing task_id")
            if task_id in seen:
                raise ValueError(f"{path}:{line_no}: duplicate task_id {task_id}")
            seen.add(task_id)
            rows.append(row)
    if not rows:
        raise ValueError(f"{path}: no rows")
    return rows


def percentile(sorted_values: list[float], q: float) -> float:
    if len(sorted_values) == 1:
        return sorted_values[0]
    pos = (len(sorted_values) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return sorted_values[lo]
    frac = pos - lo
    return sorted_values[lo] * (1.0 - frac) + sorted_values[hi] * frac


def validate_row(row: dict) -> None:
    required = {
        "task_id",
        "pre_state_sha256",
        "initial_answer",
        "p_correct",
        "i",
        "valid_letters",
        "valid_option_token_ids",
        "valid_option_logits",
        "q_valid_option",
        "q_sum",
        "valid_option_mass_under_unconstrained_vocab",
        "q_realized_answer",
        "q_strongest_alternative",
        "strongest_alternative_letters",
        "s_realized_choice_margin",
        "modal_valid_probability",
        "modal_valid_letters",
        "realized_answer_is_modal",
        "reconstructed_input_tokens",
        "historical_input_tokens",
        "extraction_location",
        "normalization",
        "no_generation",
        "no_correction_outcomes_read",
    }
    missing = required - row.keys()
    if missing:
        raise ValueError(f"task {row.get('task_id')}: missing {sorted(missing)}")
    forbidden_present = FORBIDDEN_OUTCOME_FIELDS & row.keys()
    if forbidden_present:
        raise ValueError(
            f"task {row['task_id']}: extraction record contains forbidden outcome fields {sorted(forbidden_present)}"
        )
    if row["no_generation"] is not True or row["no_correction_outcomes_read"] is not True:
        raise ValueError(f"task {row['task_id']}: extraction provenance flags are not true")
    if int(row["reconstructed_input_tokens"]) != int(row["historical_input_tokens"]):
        raise ValueError(f"task {row['task_id']}: reconstructed/historical input token counts differ")

    letters = [str(x) for x in row["valid_letters"]]
    if len(letters) < 2 or len(set(letters)) != len(letters):
        raise ValueError(f"task {row['task_id']}: invalid valid_letters")
    for mapping_name in ("valid_option_token_ids", "valid_option_logits", "q_valid_option"):
        if set(row[mapping_name]) != set(letters):
            raise ValueError(f"task {row['task_id']}: {mapping_name} keys differ from valid_letters")

    q = {letter: float(row["q_valid_option"][letter]) for letter in letters}
    if any((not math.isfinite(value)) or value < 0.0 or value > 1.0 for value in q.values()):
        raise ValueError(f"task {row['task_id']}: invalid q values")
    q_sum = sum(q.values())
    if not math.isclose(q_sum, 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(f"task {row['task_id']}: q values sum to {q_sum}")
    if not math.isclose(float(row["q_sum"]), q_sum, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(f"task {row['task_id']}: stored q_sum mismatch")

    logits = torch.tensor(
        [float(row["valid_option_logits"][letter]) for letter in letters],
        dtype=torch.float64,
    )
    reconstructed_q = torch.softmax(logits, dim=0).tolist()
    for letter, value in zip(letters, reconstructed_q):
        if not math.isclose(q[letter], float(value), rel_tol=0.0, abs_tol=1e-12):
            raise ValueError(f"task {row['task_id']}: q does not equal softmax(valid logits)")

    selected = str(row["initial_answer"])
    if selected not in q:
        raise ValueError(f"task {row['task_id']}: realized answer outside valid q")
    selected_q = q[selected]
    alt_q = max(value for letter, value in q.items() if letter != selected)
    margin = selected_q - alt_q
    if not math.isclose(float(row["q_realized_answer"]), selected_q, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(f"task {row['task_id']}: realized-answer q mismatch")
    if not math.isclose(float(row["q_strongest_alternative"]), alt_q, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(f"task {row['task_id']}: strongest-alternative q mismatch")
    if not math.isclose(float(row["s_realized_choice_margin"]), margin, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(f"task {row['task_id']}: S margin identity failure")

    expected_alt_letters = sorted(
        letter for letter, value in q.items() if letter != selected and value == alt_q
    )
    if [str(x) for x in row["strongest_alternative_letters"]] != expected_alt_letters:
        raise ValueError(f"task {row['task_id']}: strongest-alternative tie reporting mismatch")
    modal_q = max(q.values())
    expected_modal_letters = sorted(letter for letter, value in q.items() if value == modal_q)
    if [str(x) for x in row["modal_valid_letters"]] != expected_modal_letters:
        raise ValueError(f"task {row['task_id']}: modal tie reporting mismatch")
    if bool(row["realized_answer_is_modal"]) != (selected in expected_modal_letters):
        raise ValueError(f"task {row['task_id']}: modal indicator mismatch")

    valid_mass = float(row["valid_option_mass_under_unconstrained_vocab"])
    if not math.isfinite(valid_mass) or not (0.0 <= valid_mass <= 1.0):
        raise ValueError(f"task {row['task_id']}: invalid unconstrained valid-option mass")
    if not math.isclose(float(row["i"]), 1.0 - float(row["p_correct"]), rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(f"task {row['task_id']}: carried I1 != 1-P(correct)")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    for row in rows:
        validate_row(row)

    margins = sorted(float(row["s_realized_choice_margin"]) for row in rows)
    unique_margins = len(set(margins))
    valid_masses = sorted(
        float(row["valid_option_mass_under_unconstrained_vocab"]) for row in rows
    )
    nonmodal = sum(not bool(row["realized_answer_is_modal"]) for row in rows)
    pass_plumbing = unique_margins > 1

    report = {
        "schema_version": 1,
        "study": "Pilot 0 A1-D0 realized-choice extraction plumbing",
        "status": "PASS" if pass_plumbing else "FAIL",
        "authority": "measurement extraction only; no correction-association or construct-validity authority",
        "input": str(args.input),
        "n_prestates": len(rows),
        "checks": {
            "all_records_outcome_blind": True,
            "all_records_no_generation": True,
            "all_token_locations_reconstructed": True,
            "all_probability_simplex_checks_passed": True,
            "all_margin_identity_checks_passed": True,
            "unique_s_values": unique_margins,
            "s_non_degenerate": unique_margins > 1,
        },
        "s_summary": {
            "min": margins[0],
            "median": percentile(margins, 0.5),
            "max": margins[-1],
            "n_realized_answers_nonmodal": nonmodal,
            "nonmodal_rate": nonmodal / len(rows),
        },
        "unconstrained_valid_option_mass_diagnostic": {
            "min": valid_masses[0],
            "median": percentile(valid_masses, 0.5),
            "max": valid_masses[-1],
            "note": "diagnostic only; invalid-vocabulary mass is excluded from S by frozen definition",
        },
        "gate": {
            "pass_rule": "PASS iff every extraction identity/check succeeds and S is not constant across the plumbing prestates.",
            "correction_associations_examined": False,
            "A1_V_created": False,
        },
        "interpretation_guardrails": [
            "PASS means only that S is reproducibly recoverable from frozen prestates under the frozen extraction definition.",
            "PASS does not mean S predicts revision, self-correction, instability, or verified correction success.",
            "FAIL localizes to extraction/instrumentation and does not update I1, B, C, H1, or CARS.",
            "Do not inspect correction associations until the A1-D characterization contract is frozen."
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

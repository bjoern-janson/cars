#!/usr/bin/env python3
"""Extract frozen A1-D realized-choice margin S from Pilot 0 prestates.

This script performs no generation. For each frozen prestate it reconstructs the
exact pre-answer conversation up to the historical assistant prefill ``ANSWER: ``
and reads the model's raw next-token logits. It then normalizes only across valid
option-letter tokens, matching the distribution induced by the historical
first-token valid-choice constraint.

No correction outcome file is accepted or read.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import torch

from run_pilot0_local import (
    ASSISTANT_PREFILL,
    CHOICE_CONSTRAINT,
    INTERFACE_VERSION,
    letters_for,
    load_model,
    option_letter_token_ids,
)

ANSWER_RE = re.compile(r"ANSWER\s*:\s*([A-J])\b", re.I)


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


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


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def same_float(a: object, b: object) -> bool:
    try:
        return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=1e-12)
    except (TypeError, ValueError):
        return False


def verify_model_manifest(pilot_config: dict, model_dir: Path) -> dict:
    manifest_path = model_dir / "pilot0_model_manifest.json"
    if not manifest_path.exists():
        raise ValueError(f"missing {manifest_path}")
    manifest = load_json(manifest_path)
    if manifest.get("repo_id") != pilot_config["model"]["repo_id"]:
        raise ValueError("cached model repo_id differs from frozen Pilot 0 config")
    if manifest.get("revision") != pilot_config["model"]["revision"]:
        raise ValueError("cached model revision differs from frozen Pilot 0 config")
    return manifest


def validate_frozen_prestate(row: dict, pilot_config: dict, model_dir: Path) -> None:
    required = {
        "id",
        "question",
        "options",
        "initial_answer",
        "p_correct",
        "i",
        "pre_prompt",
        "raw_model_output",
        "input_tokens",
        "pre_state_sha256",
        "pre_state_audit",
        "model_requested",
        "backend",
        "reasoning_effort",
        "temperature",
        "top_p",
        "top_k",
        "interface_version",
        "assistant_prefill",
        "choice_constraint",
    }
    missing = required - row.keys()
    if missing:
        raise ValueError(f"prestate {row.get('id')!r}: missing {sorted(missing)}")

    declared_hash = str(row["pre_state_sha256"])
    computed_hash = canonical_sha256(row["pre_state_audit"])
    if declared_hash != computed_hash:
        raise ValueError(f"prestate {row['id']!r}: frozen-state SHA-256 mismatch")

    generation = pilot_config["generation"]
    interface = pilot_config["interface"]
    checks = {
        "model_requested": row["model_requested"] == str(model_dir),
        "backend": row["backend"] == pilot_config["model"]["backend"],
        "reasoning_effort": row["reasoning_effort"] == "non-thinking",
        "temperature": same_float(row["temperature"], generation["temperature"]),
        "top_p": same_float(row["top_p"], generation["top_p"]),
        "top_k": int(row["top_k"]) == int(generation["top_k"]),
        "interface_version": row["interface_version"] == interface["version"],
        "assistant_prefill": row["assistant_prefill"] == interface["assistant_prefill"],
        "choice_constraint": row["choice_constraint"] == interface["choice_constraint"],
    }
    failed = [name for name, ok in checks.items() if not ok]
    if failed:
        raise ValueError(f"prestate {row['id']!r}: frozen config mismatch: {failed}")

    match = ANSWER_RE.search(str(row["raw_model_output"]))
    if not match:
        raise ValueError(f"prestate {row['id']!r}: cannot parse ANSWER from frozen raw output")
    parsed_answer = match.group(1).upper()
    stored_answer = str(row["initial_answer"]).strip().upper()
    if parsed_answer != stored_answer:
        raise ValueError(
            f"prestate {row['id']!r}: frozen raw ANSWER {parsed_answer} != stored {stored_answer}"
        )

    if not same_float(float(row["i"]), 1.0 - float(row["p_correct"])):
        raise ValueError(f"prestate {row['id']!r}: I1 != 1-P(correct)")


def reconstruct_predecision_inputs(tokenizer, row: dict) -> dict[str, torch.Tensor]:
    messages = [
        {"role": "user", "content": str(row["pre_prompt"])},
        {"role": "assistant", "content": ASSISTANT_PREFILL},
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        continue_final_message=True,
        enable_thinking=False,
    )
    return tokenizer(text, return_tensors="pt")


def extract_one(tokenizer, model, row: dict) -> dict:
    options = [str(x) for x in row["options"]]
    valid_letters = letters_for(options)
    token_ids = option_letter_token_ids(tokenizer, valid_letters)
    initial_answer = str(row["initial_answer"]).strip().upper()
    if initial_answer not in valid_letters:
        raise ValueError(f"{row['id']}: initial answer {initial_answer} outside valid options")

    cpu_inputs = reconstruct_predecision_inputs(tokenizer, row)
    reconstructed_input_tokens = int(cpu_inputs["input_ids"].shape[-1])
    historical_input_tokens = int(row["input_tokens"])
    if reconstructed_input_tokens != historical_input_tokens:
        raise ValueError(
            f"{row['id']}: reconstructed input token count {reconstructed_input_tokens} "
            f"!= historical {historical_input_tokens}"
        )
    inputs = {key: value.to(model.device) for key, value in cpu_inputs.items()}

    with torch.inference_mode():
        outputs = model(**inputs, use_cache=False)
        next_logits = outputs.logits[0, -1, :].detach().to(device="cpu", dtype=torch.float64)

    valid_tensor = torch.tensor(token_ids, dtype=torch.long)
    valid_logits = next_logits[valid_tensor]
    q_tensor = torch.softmax(valid_logits, dim=0)

    if not bool(torch.isfinite(q_tensor).all()):
        raise ValueError(f"{row['id']}: non-finite valid-option probabilities")
    q_sum = float(q_tensor.sum().item())
    if not math.isclose(q_sum, 1.0, rel_tol=0.0, abs_tol=1e-12):
        raise ValueError(f"{row['id']}: valid-option probabilities sum to {q_sum}")

    log_valid_mass = torch.logsumexp(valid_logits, dim=0) - torch.logsumexp(next_logits, dim=0)
    valid_mass_unconstrained = float(torch.exp(log_valid_mass).item())

    q = {letter: float(q_tensor[idx].item()) for idx, letter in enumerate(valid_letters)}
    logits = {letter: float(valid_logits[idx].item()) for idx, letter in enumerate(valid_letters)}
    token_map = {letter: int(token_ids[idx]) for idx, letter in enumerate(valid_letters)}

    selected_q = q[initial_answer]
    alternatives = {letter: prob for letter, prob in q.items() if letter != initial_answer}
    strongest_alt_q = max(alternatives.values())
    strongest_alt_letters = sorted(
        letter for letter, prob in alternatives.items() if prob == strongest_alt_q
    )
    s_margin = selected_q - strongest_alt_q

    modal_q = max(q.values())
    modal_letters = sorted(letter for letter, prob in q.items() if prob == modal_q)

    return {
        "task_id": str(row["id"]),
        "pre_state_sha256": str(row["pre_state_sha256"]),
        "initial_answer": initial_answer,
        "p_correct": float(row["p_correct"]),
        "i": float(row["i"]),
        "valid_letters": valid_letters,
        "valid_option_token_ids": token_map,
        "valid_option_logits": logits,
        "q_valid_option": q,
        "q_sum": q_sum,
        "valid_option_mass_under_unconstrained_vocab": valid_mass_unconstrained,
        "q_realized_answer": selected_q,
        "q_strongest_alternative": strongest_alt_q,
        "strongest_alternative_letters": strongest_alt_letters,
        "s_realized_choice_margin": s_margin,
        "modal_valid_probability": modal_q,
        "modal_valid_letters": modal_letters,
        "realized_answer_is_modal": initial_answer in modal_letters,
        "reconstructed_input_tokens": reconstructed_input_tokens,
        "historical_input_tokens": historical_input_tokens,
        "extraction_location": "raw next-token logits immediately after assistant prefill ANSWER: and before first-token choice constraint",
        "normalization": "softmax over valid option-letter logits only",
        "no_generation": True,
        "no_correction_outcomes_read": True,
        "extracted_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("frozen_prestates", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--extraction-config",
        type=Path,
        default=Path("experiments/PILOT0_A1D_EXTRACTION_CONFIG.json"),
    )
    parser.add_argument(
        "--pilot-config",
        type=Path,
        default=Path("experiments/PILOT0_QWEN3_4B_CONFIG.json"),
    )
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=Path("/kaggle/working/pilot0-qwen3-4b"),
    )
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    extraction_config = load_json(args.extraction_config)
    if extraction_config.get("status") != "frozen before any A1-D correction-association inspection":
        raise ValueError("A1-D extraction contract is not in the expected frozen pre-association state")
    pilot_config = load_json(args.pilot_config)
    verify_model_manifest(pilot_config, args.model_dir)

    if extraction_config["extraction"]["assistant_prefill"] != ASSISTANT_PREFILL:
        raise ValueError("A1-D assistant prefill differs from frozen runner")
    if pilot_config["interface"]["version"] != INTERFACE_VERSION:
        raise ValueError("frozen Pilot 0 interface version differs from local runner")
    if pilot_config["interface"]["choice_constraint"] != CHOICE_CONSTRAINT:
        raise ValueError("frozen Pilot 0 choice constraint differs from local runner")

    rows = read_jsonl(args.frozen_prestates)
    if args.limit is not None:
        if args.limit <= 0:
            raise ValueError("--limit must be positive")
        rows = rows[: args.limit]

    tokenizer, model = load_model(str(args.model_dir))
    output: list[dict] = []
    for index, row in enumerate(rows, 1):
        validate_frozen_prestate(row, pilot_config, args.model_dir)
        extracted = extract_one(tokenizer, model, row)
        output.append(extracted)
        print(
            f"[{index}/{len(rows)}] {row['id']}: a*={extracted['initial_answer']} "
            f"S={extracted['s_realized_choice_margin']:+.6f} "
            f"modal={extracted['realized_answer_is_modal']}",
            file=sys.stderr,
        )

    write_jsonl(args.output, output)
    print(f"wrote {len(output)} A1-D choice-margin records to {args.output}", file=sys.stderr)
    print("no answer generation or correction-outcome access occurred", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

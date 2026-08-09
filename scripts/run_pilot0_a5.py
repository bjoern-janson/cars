#!/usr/bin/env python3
"""Execute frozen Pilot 0 A5 prior-state field/prose encoding branches.

A5 crosses field/value versus prose encoding of the same prior answer and
P_CORRECT inside an otherwise identical canonical inline scaffold. Eight
randomized branches are required per frozen prestate, exactly two per cell.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import sys
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

import torch
from transformers import LogitsProcessorList

from run_pilot0_local import (
    ASSISTANT_PREFILL,
    CHOICE_CONSTRAINT,
    INTERFACE_VERSION,
    FirstTokenChoiceLogitsProcessor,
    letters_for,
    load_model,
    option_letter_token_ids,
    render_question,
    set_seed,
    stable_seed,
    write_jsonl,
)

CELLS = ("RF_E0", "RF_EV", "RP_E0", "RP_EV")
CELL_FACTORS = {
    "RF_E0": ("R_fields", "E0"),
    "RF_EV": ("R_fields", "EV"),
    "RP_E0": ("R_prose", "E0"),
    "RP_EV": ("R_prose", "EV"),
}
SEPARATOR = "\n\n"


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


def same_float(a: object, b: object) -> bool:
    try:
        return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=1e-12)
    except (TypeError, ValueError):
        return False


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def verify_model_manifest(pilot_config: dict, model_dir: Path) -> None:
    manifest_path = model_dir / "pilot0_model_manifest.json"
    if not manifest_path.exists():
        raise ValueError(f"missing {manifest_path}")
    manifest = load_json(manifest_path)
    if manifest.get("repo_id") != pilot_config["model"]["repo_id"]:
        raise ValueError("cached model repo_id differs from frozen Pilot 0 config")
    if manifest.get("revision") != pilot_config["model"]["revision"]:
        raise ValueError("cached model revision differs from frozen Pilot 0 config")


def validate_frozen_prestate(row: dict, pilot_config: dict, model_dir: Path) -> None:
    required = {
        "id", "pre_state_sha256", "question", "options", "benchmark_answer",
        "initial_answer", "p_correct", "i", "initial_correct", "model_requested",
        "backend", "reasoning_effort", "temperature", "top_p", "top_k",
        "interface_version", "assistant_prefill", "choice_constraint",
    }
    missing = required - row.keys()
    if missing:
        raise ValueError(f"prestate {row.get('id')!r}: missing {sorted(missing)}")

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


def validate_design(assignments: list[dict], frozen: dict[str, dict], config: dict) -> None:
    grouped: dict[str, list[dict]] = defaultdict(list)
    expected_seed = int(config["assignment"]["randomization_seed"])
    for branch in assignments:
        unit_id = str(branch["id"])
        task_id = str(branch.get("task_id") or unit_id.split("::", 1)[0])
        cell = str(branch.get("arm", ""))
        if cell not in CELLS:
            raise ValueError(f"branch {unit_id}: invalid A5 cell {cell!r}")
        if task_id not in frozen:
            raise ValueError(f"branch {unit_id}: no frozen prestate for {task_id}")
        if int(branch.get("randomization_seed", -1)) != expected_seed:
            raise ValueError(f"branch {unit_id}: wrong randomization seed")
        source = frozen[task_id]
        if bool(source["initial_correct"]):
            raise ValueError(f"branch {unit_id}: A5 includes initially-correct prestate")
        if branch.get("pre_state_sha256") != source.get("pre_state_sha256"):
            raise ValueError(f"branch {unit_id}: frozen prestate hash mismatch")
        for field in ("question", "options", "benchmark_answer", "initial_answer", "p_correct", "i"):
            if branch.get(field) != source.get(field):
                raise ValueError(f"branch {unit_id}: {field} differs from frozen prestate")
        grouped[task_id].append(branch)

    expected_total = int(config["assignment"]["branches_per_block"])
    expected_each = int(config["assignment"]["branches_per_cell_per_block"])
    for task_id, rows in grouped.items():
        if len(rows) != expected_total:
            raise ValueError(f"block {task_id}: expected {expected_total} branches, got {len(rows)}")
        counts = Counter(str(row["arm"]) for row in rows)
        expected = {cell: expected_each for cell in CELLS}
        if dict(counts) != expected:
            raise ValueError(f"block {task_id}: cell counts {dict(counts)} != {expected}")


def semantic_state(source: dict, signal_text: str, revision_instruction: str) -> dict:
    return {
        "question": str(source["question"]),
        "options": [str(x) for x in source["options"]],
        "initial_answer": str(source["initial_answer"]).strip().upper(),
        "p_correct_6dp": f"{float(source['p_correct']):.6f}",
        "benchmark_answer": str(source["benchmark_answer"]).strip().upper(),
        "signal_text": signal_text,
        "revision_instruction": revision_instruction,
    }


def sections(source: dict, signal_text: str, revision_instruction: str) -> dict[str, str]:
    question_section = "QUESTION:\n" + render_question(
        str(source["question"]), [str(x) for x in source["options"]]
    )
    state_fields = (
        "PREVIOUS STATE:\n"
        f"ANSWER: {str(source['initial_answer']).strip().upper()}\n"
        f"P_CORRECT: {float(source['p_correct']):.6f}"
    )
    state_prose = (
        "PREVIOUS STATE:\n"
        f"Your previous answer was {str(source['initial_answer']).strip().upper()}. "
        f"Before feedback, you assigned probability {float(source['p_correct']):.6f} "
        "that this answer was correct."
    )
    signal_section = "SIGNAL:\n" + signal_text
    revision_section = "REVISION REQUEST:\n" + revision_instruction
    return {
        "question_section": question_section,
        "state_fields_section": state_fields,
        "state_prose_section": state_prose,
        "signal_section": signal_section,
        "revision_section": revision_section,
    }


def outer_scaffold_payload(chunks: dict[str, str]) -> dict[str, str]:
    return {
        "question_section": chunks["question_section"],
        "signal_section": chunks["signal_section"],
        "revision_section": chunks["revision_section"],
        "section_order": "QUESTION|PREVIOUS STATE|SIGNAL|REVISION REQUEST",
        "section_separator": SEPARATOR,
        "state_section_label": "PREVIOUS STATE:",
    }


def render_user_message(chunks: dict[str, str], encoding: str) -> str:
    if encoding == "R_fields":
        state = chunks["state_fields_section"]
    elif encoding == "R_prose":
        state = chunks["state_prose_section"]
    else:
        raise ValueError(f"unsupported encoding {encoding!r}")
    return SEPARATOR.join([
        chunks["question_section"],
        state,
        chunks["signal_section"],
        chunks["revision_section"],
    ])


def build_messages(
    source: dict,
    encoding: str,
    signal_text: str,
    revision_instruction: str,
) -> tuple[list[dict], dict[str, str]]:
    chunks = sections(source, signal_text, revision_instruction)
    fields_message = render_user_message(chunks, "R_fields")
    prose_message = render_user_message(chunks, "R_prose")
    user_message = fields_message if encoding == "R_fields" else prose_message

    state = semantic_state(source, signal_text, revision_instruction)
    scaffold = outer_scaffold_payload(chunks)
    provenance = {
        "user_message": user_message,
        "user_message_sha256": sha256_text(user_message),
        "fields_user_message_sha256": sha256_text(fields_message),
        "prose_user_message_sha256": sha256_text(prose_message),
        "semantic_state_json": canonical_json(state),
        "semantic_state_sha256": sha256_text(canonical_json(state)),
        "outer_scaffold_json": canonical_json(scaffold),
        "outer_scaffold_sha256": sha256_text(canonical_json(scaffold)),
        **chunks,
    }
    messages = [
        {"role": "user", "content": user_message},
        {"role": "assistant", "content": ASSISTANT_PREFILL},
    ]
    return messages, provenance


def verify_encoding_bridge(source: dict, signals: dict, revision_instruction: str) -> None:
    for signal in ("E0", "EV"):
        signal_text = str(signals[signal])
        _, fields = build_messages(source, "R_fields", signal_text, revision_instruction)
        _, prose = build_messages(source, "R_prose", signal_text, revision_instruction)

        if fields["semantic_state_sha256"] != prose["semantic_state_sha256"]:
            raise ValueError(f"{source['id']} {signal}: encoding changed semantic-state signature")
        if fields["semantic_state_json"] != prose["semantic_state_json"]:
            raise ValueError(f"{source['id']} {signal}: encoding changed semantic-state payload")
        if fields["outer_scaffold_sha256"] != prose["outer_scaffold_sha256"]:
            raise ValueError(f"{source['id']} {signal}: encoding changed outer scaffold")
        if fields["outer_scaffold_json"] != prose["outer_scaffold_json"]:
            raise ValueError(f"{source['id']} {signal}: encoding changed outer scaffold payload")
        if fields["user_message_sha256"] != fields["fields_user_message_sha256"]:
            raise ValueError(f"{source['id']} {signal}: R_fields provenance mismatch")
        if prose["user_message_sha256"] != prose["prose_user_message_sha256"]:
            raise ValueError(f"{source['id']} {signal}: R_prose provenance mismatch")

        for key in ("question_section", "signal_section", "revision_section"):
            if fields[key] != prose[key]:
                raise ValueError(f"{source['id']} {signal}: encoding changed {key}")
        if fields["state_fields_section"] != prose["state_fields_section"]:
            raise ValueError(f"{source['id']} {signal}: field-state template mismatch")
        if fields["state_prose_section"] != prose["state_prose_section"]:
            raise ValueError(f"{source['id']} {signal}: prose-state template mismatch")


def generate_answer(
    tokenizer,
    model,
    *,
    messages: list[dict],
    base_seed: int,
    valid_letters: list[str],
    max_new_tokens: int,
    retries: int,
    temperature: float,
    top_p: float,
    top_k: int,
) -> tuple[str, str, int, int, int]:
    last_text = ""
    for attempt in range(retries + 1):
        used_seed = base_seed + attempt
        set_seed(used_seed)
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            continue_final_message=True,
            enable_thinking=False,
        )
        inputs = tokenizer(text, return_tensors="pt").to(model.device)
        input_len = int(inputs["input_ids"].shape[-1])
        allowed = option_letter_token_ids(tokenizer, valid_letters)
        processors = LogitsProcessorList([FirstTokenChoiceLogitsProcessor(input_len, allowed)])
        with torch.inference_mode():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=True,
                temperature=temperature,
                top_p=top_p,
                top_k=top_k,
                pad_token_id=tokenizer.eos_token_id,
                logits_processor=processors,
            )
        output_ids = outputs[0][input_len:]
        continuation = tokenizer.decode(output_ids, skip_special_tokens=True)
        decoded = (ASSISTANT_PREFILL + continuation).strip()
        last_text = decoded
        answer = continuation.strip()[:1].upper()
        if answer in valid_letters:
            return answer, decoded, used_seed, input_len, int(output_ids.shape[-1])
    raise ValueError(f"could not parse final answer after {retries + 1} attempts: {last_text!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("assignments", type=Path)
    parser.add_argument("frozen_prestates", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--a5-config", type=Path, default=Path("experiments/PILOT0_A5_CONFIG.json"))
    parser.add_argument("--pilot-config", type=Path, default=Path("experiments/PILOT0_QWEN3_4B_CONFIG.json"))
    parser.add_argument("--model-dir", type=Path, default=Path("/kaggle/working/pilot0-qwen3-4b"))
    args = parser.parse_args()

    config = load_json(args.a5_config)
    if config.get("status") != "frozen before any A5 outcome generation":
        raise ValueError("A5 contract is not in the expected frozen pre-outcome state")
    pilot_config = load_json(args.pilot_config)
    verify_model_manifest(pilot_config, args.model_dir)

    generation = pilot_config["generation"]
    inv = config["invariants"]
    frozen_values = {
        "generation_base_seed": generation["base_seed"],
        "temperature": generation["temperature"],
        "top_p": generation["top_p"],
        "top_k": generation["top_k"],
        "parse_retries": generation["parse_retries"],
        "post_max_new_tokens": generation["post_max_new_tokens"],
    }
    for field, expected in frozen_values.items():
        if not same_float(inv[field], expected):
            raise ValueError(f"A5 invariant {field} differs from frozen Pilot 0 generation")
    if inv["assistant_prefill"] != ASSISTANT_PREFILL or inv["choice_constraint"] != CHOICE_CONSTRAINT:
        raise ValueError("A5 output interface differs from frozen Pilot 0 answer interface")
    if pilot_config["interface"]["version"] != INTERFACE_VERSION:
        raise ValueError("local interface version differs from frozen Pilot 0 config")

    frozen_rows = read_jsonl(args.frozen_prestates)
    frozen = {str(row["id"]): row for row in frozen_rows}
    if len(frozen) != len(frozen_rows):
        raise ValueError("duplicate frozen prestate ids")
    for row in frozen_rows:
        validate_frozen_prestate(row, pilot_config, args.model_dir)

    assignments = read_jsonl(args.assignments)
    validate_design(assignments, frozen, config)

    signals = config["factors"]["signal"]
    revision_instruction = str(config["factors"]["common_revision_instruction"])

    for source in frozen_rows:
        if bool(source["initial_correct"]):
            continue
        verify_encoding_bridge(source, signals, revision_instruction)

    tokenizer, model = load_model(str(args.model_dir))
    output: list[dict] = []
    started = time.time()

    for index, branch in enumerate(assignments, 1):
        task_id = str(branch["task_id"])
        source = frozen[task_id]
        cell = str(branch["arm"])
        encoding, signal = CELL_FACTORS[cell]
        signal_text = str(signals[signal])
        messages, provenance = build_messages(source, encoding, signal_text, revision_instruction)
        valid_letters = letters_for([str(x) for x in source["options"]])
        base_seed = stable_seed(int(inv["generation_base_seed"]), f"a5::{branch['id']}")
        final_answer, raw_text, used_seed, input_tokens, output_tokens = generate_answer(
            tokenizer,
            model,
            messages=messages,
            base_seed=base_seed,
            valid_letters=valid_letters,
            max_new_tokens=int(inv["post_max_new_tokens"]),
            retries=int(inv["parse_retries"]),
            temperature=float(inv["temperature"]),
            top_p=float(inv["top_p"]),
            top_k=int(inv["top_k"]),
        )
        benchmark = str(source["benchmark_answer"]).strip().upper()
        correct = final_answer == benchmark
        out = dict(branch)
        out.update({
            "a5_cell": cell,
            "encoding": encoding,
            "signal": signal,
            "signal_text": signal_text,
            "encoding_bridge_verified": True,
            **provenance,
            "final_answer": final_answer,
            "v": 1 if correct else 0,
            "final_correct": correct,
            "post_base_generation_seed": base_seed,
            "post_generation_seed": used_seed,
            "post_seed_rule": "stable_seed(generation_base_seed, 'a5::' + branch_id)",
            "post_seed_rule_arm_independent": True,
            "post_temperature": float(inv["temperature"]),
            "post_top_p": float(inv["top_p"]),
            "post_top_k": int(inv["top_k"]),
            "post_reasoning_effort": "non-thinking",
            "post_interface_version": INTERFACE_VERSION,
            "post_assistant_prefill": ASSISTANT_PREFILL,
            "post_choice_constraint": CHOICE_CONSTRAINT,
            "post_raw_model_output": raw_text,
            "post_input_tokens": input_tokens,
            "post_output_tokens": output_tokens,
            "post_total_tokens": input_tokens + output_tokens,
            "post_generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        })
        output.append(out)
        print(
            f"[{index}/{len(assignments)}] {branch['id']} {cell}: "
            f"{source['initial_answer']} -> {final_answer} correct={correct}",
            file=sys.stderr,
        )

    write_jsonl(args.output, output)
    print(f"wrote {len(output)} A5 outcome branches", file=sys.stderr)
    print(f"elapsed_seconds={time.time() - started:.1f}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

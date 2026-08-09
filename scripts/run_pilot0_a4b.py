#!/usr/bin/env python3
"""Execute frozen Pilot 0 A4b historical-prestate rendering branches.

A4b crosses canonicalized versus verbatim historical-prestate rendering while
holding the multi-turn conversational topology and E0/EV signal/revision turn
fixed. Eight randomized branches are required per frozen prestate, exactly two
per factorial cell.
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
    PRE_RE,
    FirstTokenChoiceLogitsProcessor,
    letters_for,
    load_model,
    option_letter_token_ids,
    pre_prompt,
    render_question,
    set_seed,
    stable_seed,
    write_jsonl,
)

CELLS = ("HC_E0", "HC_EV", "HV_E0", "HV_EV")
CELL_FACTORS = {
    "HC_E0": ("H_canonical", "E0"),
    "HC_EV": ("H_canonical", "EV"),
    "HV_E0": ("H_verbatim", "E0"),
    "HV_EV": ("H_verbatim", "EV"),
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
        "id", "pre_prompt", "raw_model_output", "pre_state_sha256", "question",
        "options", "benchmark_answer", "initial_answer", "p_correct", "i",
        "initial_correct", "model_requested", "backend", "reasoning_effort",
        "temperature", "top_p", "top_k", "interface_version",
        "assistant_prefill", "choice_constraint",
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

    expected_prompt = pre_prompt(str(row["question"]), [str(x) for x in row["options"]])
    if str(row["pre_prompt"]) != expected_prompt:
        raise ValueError(f"prestate {row['id']!r}: stored pre_prompt is not the exact frozen historical prompt")

    match = PRE_RE.search(str(row["raw_model_output"]))
    if not match:
        raise ValueError(f"prestate {row['id']!r}: historical raw_model_output does not parse")
    parsed_answer = match.group(1).upper()
    parsed_p = float(match.group(2))
    if parsed_answer != str(row["initial_answer"]).strip().upper():
        raise ValueError(f"prestate {row['id']!r}: historical output answer differs from frozen initial answer")
    if not same_float(parsed_p, row["p_correct"]):
        raise ValueError(f"prestate {row['id']!r}: historical output P_CORRECT differs from frozen value")


def validate_design(assignments: list[dict], frozen: dict[str, dict], config: dict) -> None:
    grouped: dict[str, list[dict]] = defaultdict(list)
    expected_seed = int(config["assignment"]["randomization_seed"])
    for branch in assignments:
        unit_id = str(branch["id"])
        task_id = str(branch.get("task_id") or unit_id.split("::", 1)[0])
        cell = str(branch.get("arm", ""))
        if cell not in CELLS:
            raise ValueError(f"branch {unit_id}: invalid A4b cell {cell!r}")
        if task_id not in frozen:
            raise ValueError(f"branch {unit_id}: no frozen prestate for {task_id}")
        if int(branch.get("randomization_seed", -1)) != expected_seed:
            raise ValueError(f"branch {unit_id}: wrong randomization seed")
        source = frozen[task_id]
        if bool(source["initial_correct"]):
            raise ValueError(f"branch {unit_id}: A4b includes initially-correct prestate")
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


def canonical_prestate_turns(source: dict) -> tuple[str, str]:
    user_turn = "QUESTION:\n" + render_question(
        str(source["question"]), [str(x) for x in source["options"]]
    )
    assistant_turn = (
        "PREVIOUS STATE:\n"
        f"ANSWER: {str(source['initial_answer']).strip().upper()}\n"
        f"P_CORRECT: {float(source['p_correct']):.6f}"
    )
    return user_turn, assistant_turn


def common_signal_revision_turn(signal_text: str, revision_instruction: str) -> str:
    return (
        "SIGNAL:\n" + signal_text
        + SEPARATOR
        + "REVISION REQUEST:\n" + revision_instruction
    )


def build_messages(
    source: dict,
    rendering: str,
    signal_text: str,
    revision_instruction: str,
) -> tuple[list[dict], dict[str, str]]:
    signal_turn = common_signal_revision_turn(signal_text, revision_instruction)
    canonical_user, canonical_assistant = canonical_prestate_turns(source)

    if rendering == "H_canonical":
        user_prestate = canonical_user
        assistant_prestate = canonical_assistant
    elif rendering == "H_verbatim":
        user_prestate = str(source["pre_prompt"])
        assistant_prestate = str(source["raw_model_output"])
    else:
        raise ValueError(f"unsupported rendering {rendering!r}")

    messages = [
        {"role": "user", "content": user_prestate},
        {"role": "assistant", "content": assistant_prestate},
        {"role": "user", "content": signal_turn},
        {"role": "assistant", "content": ASSISTANT_PREFILL},
    ]
    provenance = {
        "user_prestate_turn": user_prestate,
        "assistant_prestate_turn": assistant_prestate,
        "signal_revision_turn": signal_turn,
        "user_prestate_sha256": sha256_text(user_prestate),
        "assistant_prestate_sha256": sha256_text(assistant_prestate),
        "signal_revision_sha256": sha256_text(signal_turn),
        "canonical_user_prestate_sha256": sha256_text(canonical_user),
        "canonical_assistant_prestate_sha256": sha256_text(canonical_assistant),
        "historical_user_prestate_sha256": sha256_text(str(source["pre_prompt"])),
        "historical_assistant_prestate_sha256": sha256_text(str(source["raw_model_output"])),
    }
    return messages, provenance


def verify_rendering_bridge(source: dict, signals: dict, revision_instruction: str) -> None:
    canonical_user, canonical_assistant = canonical_prestate_turns(source)
    if not canonical_user or not canonical_assistant:
        raise ValueError(f"{source['id']}: empty canonical prestate rendering")
    for signal in ("E0", "EV"):
        signal_text = str(signals[signal])
        _, canonical = build_messages(source, "H_canonical", signal_text, revision_instruction)
        _, verbatim = build_messages(source, "H_verbatim", signal_text, revision_instruction)
        if canonical["signal_revision_turn"] != verbatim["signal_revision_turn"]:
            raise ValueError(f"{source['id']} {signal}: rendering changed signal/revision content")
        if canonical["signal_revision_sha256"] != verbatim["signal_revision_sha256"]:
            raise ValueError(f"{source['id']} {signal}: signal/revision hashes differ")
        if canonical["user_prestate_sha256"] != canonical["canonical_user_prestate_sha256"]:
            raise ValueError(f"{source['id']} {signal}: H_canonical user turn provenance mismatch")
        if canonical["assistant_prestate_sha256"] != canonical["canonical_assistant_prestate_sha256"]:
            raise ValueError(f"{source['id']} {signal}: H_canonical assistant turn provenance mismatch")
        if verbatim["user_prestate_sha256"] != verbatim["historical_user_prestate_sha256"]:
            raise ValueError(f"{source['id']} {signal}: H_verbatim user turn provenance mismatch")
        if verbatim["assistant_prestate_sha256"] != verbatim["historical_assistant_prestate_sha256"]:
            raise ValueError(f"{source['id']} {signal}: H_verbatim assistant turn provenance mismatch")


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
    parser.add_argument("--a4b-config", type=Path, default=Path("experiments/PILOT0_A4B_CONFIG.json"))
    parser.add_argument("--pilot-config", type=Path, default=Path("experiments/PILOT0_QWEN3_4B_CONFIG.json"))
    parser.add_argument("--model-dir", type=Path, default=Path("/kaggle/working/pilot0-qwen3-4b"))
    args = parser.parse_args()

    config = load_json(args.a4b_config)
    if config.get("status") != "frozen before any A4b outcome generation":
        raise ValueError("A4b contract is not in the expected frozen pre-outcome state")
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
            raise ValueError(f"A4b invariant {field} differs from frozen Pilot 0 generation")
    if inv["assistant_prefill"] != ASSISTANT_PREFILL or inv["choice_constraint"] != CHOICE_CONSTRAINT:
        raise ValueError("A4b output interface differs from frozen Pilot 0 answer interface")
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
    revision_instruction = (
        "Review your previous answer and revise if necessary.\n"
        "Return exactly one line: ANSWER: <one option letter>"
    )
    expected_common = str(config["factors"]["common_signal_revision_turn"])
    for signal in ("E0", "EV"):
        rendered = common_signal_revision_turn(str(signals[signal]), revision_instruction)
        expected = expected_common.replace("<exact E0 or EV signal text>", str(signals[signal]))
        if rendered != expected:
            raise ValueError(f"A4b common signal/revision template mismatch for {signal}")

    # Fail closed on the rendering bridge before model loading or outcome generation.
    for source in frozen_rows:
        if bool(source["initial_correct"]):
            continue
        verify_rendering_bridge(source, signals, revision_instruction)

    tokenizer, model = load_model(str(args.model_dir))
    output: list[dict] = []
    started = time.time()

    for index, branch in enumerate(assignments, 1):
        task_id = str(branch["task_id"])
        source = frozen[task_id]
        cell = str(branch["arm"])
        rendering, signal = CELL_FACTORS[cell]
        signal_text = str(signals[signal])
        messages, provenance = build_messages(source, rendering, signal_text, revision_instruction)
        valid_letters = letters_for([str(x) for x in source["options"]])
        base_seed = stable_seed(int(inv["generation_base_seed"]), f"a4b::{branch['id']}")
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
            "a4b_cell": cell,
            "rendering": rendering,
            "signal": signal,
            "signal_text": signal_text,
            "rendering_bridge_verified": True,
            **provenance,
            "final_answer": final_answer,
            "v": 1 if correct else 0,
            "final_correct": correct,
            "post_base_generation_seed": base_seed,
            "post_generation_seed": used_seed,
            "post_seed_rule": "stable_seed(generation_base_seed, 'a4b::' + branch_id)",
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
    print(f"wrote {len(output)} A4b outcome branches", file=sys.stderr)
    print(f"elapsed_seconds={time.time() - started:.1f}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

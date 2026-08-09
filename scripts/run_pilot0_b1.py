#!/usr/bin/env python3
"""Execute frozen Pilot 0 Localization B1 outcome branches.

B1 preserves the B0-v2 conversational reconstruction but replaces the P_POST
probe with one revision opportunity and final-answer scoring. Signal wording is
read from the frozen B1 contract. The branch id fixes the stochastic stream;
arm identity changes only the signal text.
"""

from __future__ import annotations

import argparse
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
    read_jsonl,
    set_seed,
    stable_seed,
    write_jsonl,
)

ARMS = ("E0", "EU", "EV")


def same_float(a: object, b: object) -> bool:
    try:
        return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=1e-12)
    except (TypeError, ValueError):
        return False


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def verify_model_manifest(pilot_config: dict, model_dir: Path) -> None:
    manifest_path = model_dir / "pilot0_model_manifest.json"
    if not manifest_path.exists():
        raise ValueError(f"missing {manifest_path}")
    manifest = load_json(manifest_path)
    if manifest.get("repo_id") != pilot_config["model"]["repo_id"]:
        raise ValueError("cached model repo_id differs from frozen Pilot 0 config")
    if manifest.get("revision") != pilot_config["model"]["revision"]:
        raise ValueError("cached model revision differs from frozen Pilot 0 config")


def validate_design(assignments: list[dict], frozen: dict[str, dict], config: dict) -> None:
    by_block: dict[str, list[dict]] = defaultdict(list)
    seen_ids: set[str] = set()
    for row in assignments:
        unit_id = str(row["id"])
        if unit_id in seen_ids:
            raise ValueError(f"duplicate branch id {unit_id}")
        seen_ids.add(unit_id)
        task_id = str(row.get("task_id") or unit_id.split("::", 1)[0])
        if task_id not in frozen:
            raise ValueError(f"branch {unit_id}: no frozen prestate for {task_id}")
        if str(row.get("arm")) not in ARMS:
            raise ValueError(f"branch {unit_id}: invalid arm {row.get('arm')!r}")
        if int(row.get("randomization_seed", -1)) != int(config["assignment"]["randomization_seed"]):
            raise ValueError(f"branch {unit_id}: wrong randomization seed")
        source = frozen[task_id]
        if bool(source["initial_correct"]):
            raise ValueError(f"branch {unit_id}: B1 includes an initially-correct prestate")
        if row.get("pre_state_sha256") != source.get("pre_state_sha256"):
            raise ValueError(f"branch {unit_id}: frozen prestate hash mismatch")
        for field in ("question", "options", "benchmark_answer", "initial_answer", "p_correct", "i"):
            if row.get(field) != source.get(field):
                raise ValueError(f"branch {unit_id}: {field} differs from frozen prestate")
        by_block[task_id].append(row)

    expected_total = int(config["assignment"]["branches_per_block"])
    expected_each = int(config["assignment"]["branches_per_arm_per_block"])
    for task_id, rows in by_block.items():
        if len(rows) != expected_total:
            raise ValueError(f"block {task_id}: expected {expected_total} branches, got {len(rows)}")
        counts = Counter(str(row["arm"]) for row in rows)
        expected = {arm: expected_each for arm in ARMS}
        if dict(counts) != expected:
            raise ValueError(f"block {task_id}: arm counts {dict(counts)} != {expected}")


def validate_frozen_prestate(row: dict, pilot_config: dict, model_dir: Path) -> None:
    required = {
        "id", "pre_prompt", "raw_model_output", "pre_state_sha256",
        "initial_answer", "p_correct", "i", "initial_correct",
        "model_requested", "backend", "reasoning_effort", "temperature",
        "top_p", "top_k", "interface_version", "assistant_prefill",
        "choice_constraint",
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
        raise ValueError(f"prestate {row.get('id')!r}: frozen config mismatch: {failed}")


def revision_message(signal_text: str) -> str:
    return (
        f"{signal_text}\n\n"
        "Review your previous answer and revise if necessary.\n"
        "Return exactly one line: ANSWER: <one option letter>"
    )


def generate_answer(
    tokenizer,
    model,
    *,
    pre_prompt: str,
    prior_response: str,
    new_message: str,
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
        seed = base_seed + attempt
        set_seed(seed)
        messages = [
            {"role": "user", "content": pre_prompt},
            {"role": "assistant", "content": prior_response},
            {"role": "user", "content": new_message},
            {"role": "assistant", "content": ASSISTANT_PREFILL},
        ]
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
            return answer, decoded, seed, input_len, int(output_ids.shape[-1])
    raise ValueError(f"could not parse final answer after {retries + 1} attempts: {last_text!r}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("assignments", type=Path)
    parser.add_argument("frozen_prestates", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--b1-config", type=Path, default=Path("experiments/PILOT0_B1_CONFIG.json"))
    parser.add_argument("--pilot-config", type=Path, default=Path("experiments/PILOT0_QWEN3_4B_CONFIG.json"))
    parser.add_argument("--model-dir", type=Path, default=Path("/kaggle/working/pilot0-qwen3-4b"))
    args = parser.parse_args()

    config = load_json(args.b1_config)
    pilot_config = load_json(args.pilot_config)
    verify_model_manifest(pilot_config, args.model_dir)

    if config.get("status") != "frozen before any B1 outcome generation":
        raise ValueError("B1 contract is not in the expected frozen pre-data state")
    signals = config["signals"]
    if tuple(signals.keys()) != ARMS:
        raise ValueError(f"B1 arms must be exactly {ARMS}")

    generation = pilot_config["generation"]
    inv = config["invariants"]
    for field in ("generation_base_seed", "temperature", "top_p", "top_k", "parse_retries", "post_max_new_tokens"):
        expected = {
            "generation_base_seed": generation["base_seed"],
            "temperature": generation["temperature"],
            "top_p": generation["top_p"],
            "top_k": generation["top_k"],
            "parse_retries": generation["parse_retries"],
            "post_max_new_tokens": generation["post_max_new_tokens"],
        }[field]
        if not same_float(inv[field], expected):
            raise ValueError(f"B1 invariant {field} differs from frozen Pilot 0 generation")
    if inv["assistant_prefill"] != ASSISTANT_PREFILL or inv["choice_constraint"] != CHOICE_CONSTRAINT:
        raise ValueError("B1 output interface differs from frozen Pilot 0 answer interface")

    frozen_rows = read_jsonl(args.frozen_prestates)
    frozen = {str(row["id"]): row for row in frozen_rows}
    if len(frozen) != len(frozen_rows):
        raise ValueError("duplicate frozen prestate ids")
    for row in frozen_rows:
        validate_frozen_prestate(row, pilot_config, args.model_dir)

    assignments = read_jsonl(args.assignments)
    validate_design(assignments, frozen, config)

    tokenizer, model = load_model(str(args.model_dir))
    output: list[dict] = []
    started = time.time()
    total = len(assignments)
    for index, branch in enumerate(assignments, 1):
        task_id = str(branch["task_id"])
        source = frozen[task_id]
        arm = str(branch["arm"])
        options = [str(x) for x in branch["options"]]
        valid_letters = letters_for(options)
        message = revision_message(signals[arm])
        base_seed = stable_seed(int(inv["generation_base_seed"]), f"post::{branch['id']}")
        final_answer, raw_text, used_seed, input_tokens, output_tokens = generate_answer(
            tokenizer,
            model,
            pre_prompt=str(source["pre_prompt"]),
            prior_response=str(source["raw_model_output"]),
            new_message=message,
            base_seed=base_seed,
            valid_letters=valid_letters,
            max_new_tokens=int(inv["post_max_new_tokens"]),
            retries=int(inv["parse_retries"]),
            temperature=float(inv["temperature"]),
            top_p=float(inv["top_p"]),
            top_k=int(inv["top_k"]),
        )
        benchmark = str(branch["benchmark_answer"]).strip().upper()
        correct = final_answer == benchmark
        out = dict(branch)
        out.update({
            "signal_text": signals[arm],
            "final_answer": final_answer,
            "v": 1 if correct else 0,
            "final_correct": correct,
            "post_model_requested": str(args.model_dir),
            "post_response_model": str(args.model_dir),
            "post_response_id": f"local::{branch['id']}::{used_seed}",
            "post_reasoning_effort": "non-thinking",
            "post_backend": pilot_config["model"]["backend"],
            "post_generation_seed": used_seed,
            "post_base_generation_seed": base_seed,
            "post_temperature": float(inv["temperature"]),
            "post_top_p": float(inv["top_p"]),
            "post_top_k": int(inv["top_k"]),
            "post_interface_version": INTERFACE_VERSION,
            "post_assistant_prefill": ASSISTANT_PREFILL,
            "post_choice_constraint": CHOICE_CONSTRAINT,
            "post_conversation_interface": "b0-v2-history-plus-signal-then-revision-v1",
            "post_user_message": message,
            "post_raw_model_output": raw_text,
            "post_input_tokens": input_tokens,
            "post_output_tokens": output_tokens,
            "post_total_tokens": input_tokens + output_tokens,
            "post_generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        })
        output.append(out)
        print(
            f"[{index}/{total}] {branch['id']} {arm}: {branch['initial_answer']} -> {final_answer} correct={correct}",
            file=sys.stderr,
        )

    write_jsonl(args.output, output)
    print(f"wrote {len(output)} B1 outcome branches", file=sys.stderr)
    print(f"elapsed_seconds={time.time() - started:.1f}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Run the candidate Pilot 0 B0-v2 signal probe on frozen prestates.

B0-v2 preserves the exact original pre-treatment conversation:
  user:      frozen pre_prompt
  assistant: frozen raw_model_output (ANSWER + P_CORRECT)
  user:      new signal + P_POST request
  assistant: P_POST: <sampled probability>

The new user message never restates P_PRE. P_PRE is retained externally only for
computing M = P_POST - P_PRE. No answer reconsideration or revision is allowed.

This runner is suitable for plumbing before B0-v2 is frozen for manipulation
validation. It does not score correctness or inspect the desired signal ordering.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

P_POST_RE = re.compile(r"P_POST\s*:\s*(0(?:\.\d+)?|1(?:\.0+)?)\b", re.I)
ASSISTANT_PREFILL = "P_POST: "


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


def stable_seed(base_seed: int, label: str) -> int:
    digest = hashlib.sha256(label.encode("utf-8")).digest()
    offset = int.from_bytes(digest[:8], "big") % 1_000_000_000
    return (base_seed + offset) % 2_147_483_647


def set_seed(seed: int) -> None:
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)


def load_model(model_name: str):
    if not torch.cuda.is_available():
        print("warning: CUDA unavailable; local inference may be very slow", file=sys.stderr)
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        dtype=dtype,
        device_map="auto",
    )
    model.eval()
    return tokenizer, model


def verify_model_manifest(pilot_config: dict, model_dir: Path) -> None:
    manifest_path = model_dir / "pilot0_model_manifest.json"
    if not manifest_path.exists():
        raise ValueError(
            f"missing {manifest_path}; run scripts/cache_pilot0_qwen3_4b.py first"
        )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("repo_id") != pilot_config["model"]["repo_id"]:
        raise ValueError("cached model repo_id differs from frozen Pilot 0 config")
    if manifest.get("revision") != pilot_config["model"]["revision"]:
        raise ValueError("cached model revision differs from frozen Pilot 0 config")


def same_float(a: object, b: object) -> bool:
    try:
        return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=1e-12)
    except (TypeError, ValueError):
        return False


def validate_frozen_prestate(row: dict, pilot_config: dict, model_dir: Path) -> None:
    required = {
        "id",
        "initial_answer",
        "p_correct",
        "i",
        "initial_correct",
        "pre_prompt",
        "raw_model_output",
        "pre_state_sha256",
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
        raise ValueError(
            f"prestate {row.get('id')!r}: differs from frozen Pilot 0 config: {failed}"
        )


def new_user_message(signal_text: str) -> str:
    return (
        f"{signal_text}\n\n"
        "Do not solve the multiple-choice question again and do not revise the previous answer. "
        "Based only on the new signal above, report your current probability that your previous "
        "answer is correct.\n"
        "Return exactly one line: P_POST: <a number from 0 to 1>"
    )


def generate_probability(
    tokenizer,
    model,
    *,
    pre_prompt: str,
    prior_response: str,
    signal_text: str,
    seed: int,
    max_new_tokens: int,
    temperature: float,
    top_p: float,
    top_k: int,
) -> tuple[float, str, int, int, str]:
    set_seed(seed)
    probe_message = new_user_message(signal_text)
    messages = [
        {"role": "user", "content": pre_prompt},
        {"role": "assistant", "content": prior_response},
        {"role": "user", "content": probe_message},
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
    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            pad_token_id=tokenizer.eos_token_id,
        )
    output_ids = outputs[0][input_len:]
    continuation = tokenizer.decode(output_ids, skip_special_tokens=True)
    decoded = (ASSISTANT_PREFILL + continuation).strip()
    match = P_POST_RE.search(decoded)
    if not match:
        raise ValueError(f"could not parse B0-v2 probability output: {decoded!r}")
    p_post = float(match.group(1))
    if not 0.0 <= p_post <= 1.0:
        raise ValueError(f"P_POST outside [0,1]: {p_post}")
    return p_post, decoded, input_len, int(output_ids.shape[-1]), probe_message


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="Frozen pre-treatment JSONL.")
    parser.add_argument("output", type=Path, help="B0-v2 probe JSONL.")
    parser.add_argument(
        "--pilot-config",
        type=Path,
        default=Path("experiments/PILOT0_QWEN3_4B_CONFIG.json"),
    )
    parser.add_argument(
        "--interface-config",
        type=Path,
        default=Path("experiments/PILOT0_B0_V2_INTERFACE_PLUMBING.json"),
    )
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=Path("/kaggle/working/pilot0-qwen3-4b"),
    )
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    pilot_config = json.loads(args.pilot_config.read_text(encoding="utf-8"))
    interface_config = json.loads(args.interface_config.read_text(encoding="utf-8"))
    verify_model_manifest(pilot_config, args.model_dir)

    signals: dict[str, str] = interface_config["signals"]
    if list(signals) != ["E0", "EU", "EV"]:
        raise ValueError("B0-v2 signals must be ordered exactly E0, EU, EV")

    generation = pilot_config["generation"]
    probe_generation = interface_config["generation"]
    for field in ("base_seed", "temperature", "top_p", "top_k"):
        if not same_float(probe_generation[field], generation[field]):
            raise ValueError(f"B0-v2 {field} differs from frozen Pilot 0 generation")
    if int(probe_generation.get("parse_retries", -1)) != 0:
        raise ValueError("candidate B0-v2 interface requires parse_retries=0")
    if probe_generation.get("assistant_prefill") != ASSISTANT_PREFILL:
        raise ValueError("B0-v2 assistant prefill differs from interface contract")

    replicates = int(interface_config["plumbing"]["replicates_per_signal"])
    if replicates != 2:
        raise ValueError("candidate B0-v2 plumbing requires exactly two replicates per signal")

    rows = read_jsonl(args.input)
    eligible = [row for row in rows if not bool(row["initial_correct"])]
    if args.limit is not None:
        if args.limit <= 0:
            raise ValueError("--limit must be positive")
        eligible = eligible[: args.limit]
    if not eligible:
        raise ValueError("no initially-wrong frozen prestates")

    tokenizer, model = load_model(str(args.model_dir))
    output: list[dict] = []
    started = time.time()
    total = len(eligible) * replicates * len(signals)
    index = 0

    for prestate in eligible:
        validate_frozen_prestate(prestate, pilot_config, args.model_dir)
        task_id = str(prestate["id"])
        p_pre = float(prestate["p_correct"])
        if not 0.0 <= p_pre <= 1.0:
            raise ValueError(f"{task_id}: P_PRE outside [0,1]")

        for rep in range(1, replicates + 1):
            matched_seed = stable_seed(
                int(probe_generation["base_seed"]),
                f"b0v2::{task_id}::r{rep}",
            )
            for signal, signal_text in signals.items():
                index += 1
                p_post, raw_text, input_tokens, output_tokens, probe_message = generate_probability(
                    tokenizer,
                    model,
                    pre_prompt=str(prestate["pre_prompt"]),
                    prior_response=str(prestate["raw_model_output"]),
                    signal_text=signal_text,
                    seed=matched_seed,
                    max_new_tokens=int(probe_generation["max_new_tokens"]),
                    temperature=float(probe_generation["temperature"]),
                    top_p=float(probe_generation["top_p"]),
                    top_k=int(probe_generation["top_k"]),
                )
                record = {
                    "id": f"{task_id}::r{rep}::{signal}",
                    "task_id": task_id,
                    "stratum": task_id,
                    "replicate": rep,
                    "signal": signal,
                    "signal_text": signal_text,
                    "pre_state_sha256": prestate["pre_state_sha256"],
                    "p_pre": p_pre,
                    "i": float(prestate["i"]),
                    "p_post": p_post,
                    "m": p_post - p_pre,
                    "matched_generation_seed": matched_seed,
                    "interface_version": "pilot0-b0-v2-conversational-state-candidate",
                    "history_pre_prompt": prestate["pre_prompt"],
                    "history_prior_response": prestate["raw_model_output"],
                    "new_user_message": probe_message,
                    "assistant_prefill": ASSISTANT_PREFILL,
                    "raw_model_output": raw_text,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                }
                output.append(record)
                print(
                    f"[{index}/{total}] {task_id} r{rep} {signal}: "
                    f"P_PRE={p_pre:.3f} P_POST={p_post:.3f} M={p_post - p_pre:+.3f}",
                    file=sys.stderr,
                )

    write_jsonl(args.output, output)
    print(f"eligible frozen prestates: {len(eligible)}", file=sys.stderr)
    print(f"wrote {len(output)} candidate B0-v2 probes", file=sys.stderr)
    print(f"elapsed_seconds={time.time() - started:.1f}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

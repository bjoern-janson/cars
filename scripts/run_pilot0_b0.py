#!/usr/bin/env python3
"""Run Pilot 0 Localization B0 manipulation validation on frozen prestates.

B0 does not allow answer revision and does not score final correctness. It asks
whether three signal conditions produce the intended ordered update in the
reported probability that the already-frozen previous answer is correct.

Each eligible frozen prestate receives every signal with two matched stochastic
replicates. For a given prestate/replicate pair, all signals use the same base
generation seed; signal identity is therefore not confounded with RNG seed.
"""

from __future__ import annotations

import argparse
import hashlib
import json
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


def b0_prompt(initial_answer: str, p_pre: float, signal_text: str) -> str:
    return (
        "Do not solve or reconsider the multiple-choice question, and do not change "
        "the previous answer.\n"
        "Use the frozen pre-treatment probability below as the probability before "
        "receiving the signal.\n\n"
        f"Previous answer: {initial_answer}\n"
        f"P_PRE: {p_pre:.6f}\n\n"
        f"{signal_text}\n\n"
        "Without reconsidering the question, report only your probability now that "
        "the previous answer is correct.\n"
        "Return exactly one line: P_POST: <a number from 0 to 1>"
    )


def generate_probability(
    tokenizer,
    model,
    prompt: str,
    *,
    seed: int,
    max_new_tokens: int,
    temperature: float,
    top_p: float,
    top_k: int,
) -> tuple[float, str, int, int]:
    set_seed(seed)
    messages = [
        {"role": "user", "content": prompt},
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
        raise ValueError(f"could not parse B0 probability output: {decoded!r}")
    p_post = float(match.group(1))
    if not 0.0 <= p_post <= 1.0:
        raise ValueError(f"P_POST outside [0,1]: {p_post}")
    return p_post, decoded, input_len, int(output_ids.shape[-1])


def validate_frozen_prestate(row: dict, pilot_config: dict, model_dir: Path) -> None:
    required = {
        "id",
        "initial_answer",
        "p_correct",
        "i",
        "initial_correct",
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
        "temperature": float(row["temperature"]) == float(generation["temperature"]),
        "top_p": float(row["top_p"]) == float(generation["top_p"]),
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path, help="Frozen pre-treatment JSONL.")
    parser.add_argument("output", type=Path, help="B0 signal-probe JSONL.")
    parser.add_argument(
        "--pilot-config",
        type=Path,
        default=Path("experiments/PILOT0_QWEN3_4B_CONFIG.json"),
    )
    parser.add_argument(
        "--b0-config",
        type=Path,
        default=Path("experiments/PILOT0_B0_CONFIG.json"),
    )
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=Path("/kaggle/working/pilot0-qwen3-4b"),
    )
    args = parser.parse_args()

    pilot_config = json.loads(args.pilot_config.read_text(encoding="utf-8"))
    b0_config = json.loads(args.b0_config.read_text(encoding="utf-8"))
    verify_model_manifest(pilot_config, args.model_dir)

    signals: dict[str, str] = b0_config["signals"]
    expected_signals = ["E0", "EU", "EV"]
    if list(signals) != expected_signals:
        raise ValueError(
            f"B0 signals must be ordered exactly {expected_signals}; got {list(signals)}"
        )
    replicates = int(b0_config["design"]["replicates_per_signal"])
    if replicates != 2:
        raise ValueError("frozen B0 design requires exactly 2 replicates per signal")

    generation = pilot_config["generation"]
    b0_generation = b0_config["generation"]
    if float(b0_generation["temperature"]) != float(generation["temperature"]):
        raise ValueError("B0 temperature differs from frozen Pilot 0 generation")
    if float(b0_generation["top_p"]) != float(generation["top_p"]):
        raise ValueError("B0 top_p differs from frozen Pilot 0 generation")
    if int(b0_generation["top_k"]) != int(generation["top_k"]):
        raise ValueError("B0 top_k differs from frozen Pilot 0 generation")
    if int(b0_generation["base_seed"]) != int(generation["base_seed"]):
        raise ValueError("B0 base_seed differs from frozen Pilot 0 generation")
    if int(b0_generation.get("parse_retries", -1)) != 0:
        raise ValueError("frozen B0 interface requires parse_retries=0")
    if b0_generation.get("assistant_prefill") != ASSISTANT_PREFILL:
        raise ValueError("B0 assistant prefill differs from frozen B0 config")

    rows = read_jsonl(args.input)
    eligible = [row for row in rows if not bool(row["initial_correct"])]
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
        initial_answer = str(prestate["initial_answer"]).strip().upper()
        p_pre = float(prestate["p_correct"])
        if not 0.0 <= p_pre <= 1.0:
            raise ValueError(f"{task_id}: P_PRE outside [0,1]")

        for rep in range(1, replicates + 1):
            matched_seed = stable_seed(
                int(b0_generation["base_seed"]),
                f"b0::{task_id}::r{rep}",
            )
            for signal, signal_text in signals.items():
                index += 1
                prompt = b0_prompt(initial_answer, p_pre, signal_text)
                p_post, raw_text, input_tokens, output_tokens = generate_probability(
                    tokenizer,
                    model,
                    prompt,
                    seed=matched_seed,
                    max_new_tokens=int(b0_generation["max_new_tokens"]),
                    temperature=float(b0_generation["temperature"]),
                    top_p=float(b0_generation["top_p"]),
                    top_k=int(b0_generation["top_k"]),
                )
                record = {
                    "id": f"{task_id}::r{rep}::{signal}",
                    "task_id": task_id,
                    "stratum": task_id,
                    "replicate": rep,
                    "signal": signal,
                    "signal_text": signal_text,
                    "pre_state_sha256": prestate["pre_state_sha256"],
                    "initial_answer": initial_answer,
                    "p_pre": p_pre,
                    "i": float(prestate["i"]),
                    "p_post": p_post,
                    "m": p_post - p_pre,
                    "model_requested": str(args.model_dir),
                    "backend": pilot_config["model"]["backend"],
                    "reasoning_effort": "non-thinking",
                    "temperature": float(b0_generation["temperature"]),
                    "top_p": float(b0_generation["top_p"]),
                    "top_k": int(b0_generation["top_k"]),
                    "matched_generation_seed": matched_seed,
                    "assistant_prefill": ASSISTANT_PREFILL,
                    "prompt": prompt,
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
    print(f"signals: {','.join(signals)}", file=sys.stderr)
    print(f"replicates per signal: {replicates}", file=sys.stderr)
    print(f"wrote {len(output)} B0 signal probes", file=sys.stderr)
    print(f"elapsed_seconds={time.time() - started:.1f}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

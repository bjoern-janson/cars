#!/usr/bin/env python3
"""Run Pilot 0 with a local/open-weight causal language model.

Default target: Qwen/Qwen3-4B on a free GPU notebook such as Kaggle.
This changes only the execution backend. The Pilot 0 measurement, treatment,
randomization, scoring, and analysis remain unchanged.

Requires: torch, transformers>=4.51.0, accelerate
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
from transformers import AutoModelForCausalLM, AutoTokenizer, LogitsProcessor, LogitsProcessorList

LETTERS = "ABCDEFGHIJ"
PRE_RE = re.compile(
    r"ANSWER\s*:\s*([A-J])\b.*?P_CORRECT\s*:\s*(0(?:\.\d+)?|1(?:\.0+)?)",
    re.I | re.S,
)
POST_RE = re.compile(r"ANSWER\s*:\s*([A-J])\b", re.I)
ASSISTANT_PREFILL = "ANSWER: "
INTERFACE_VERSION = "pilot0-local-prefill-constrained-choice-v1"
CHOICE_CONSTRAINT = "first-generated-token-valid-option-letter"


class FirstTokenChoiceLogitsProcessor(LogitsProcessor):
    """Restrict only the first generated token to the declared option letters."""

    def __init__(self, prompt_length: int, allowed_token_ids: list[int]):
        if not allowed_token_ids:
            raise ValueError("allowed_token_ids must not be empty")
        self.prompt_length = int(prompt_length)
        self.allowed_token_ids = sorted(set(int(x) for x in allowed_token_ids))

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        if int(input_ids.shape[-1]) != self.prompt_length:
            return scores
        constrained = torch.full_like(scores, float("-inf"))
        constrained[:, self.allowed_token_ids] = scores[:, self.allowed_token_ids]
        return constrained


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
    return rows


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")


def letters_for(options: list[str]) -> list[str]:
    if not (2 <= len(options) <= len(LETTERS)):
        raise ValueError(f"expected 2-{len(LETTERS)} options, got {len(options)}")
    return list(LETTERS[: len(options)])


def normalize_answer(row: dict) -> str:
    if "answer" in row:
        value = str(row["answer"]).strip().upper()
        if value in LETTERS:
            return value
    if "answer_index" in row:
        idx = int(row["answer_index"])
        if 0 <= idx < len(LETTERS):
            return LETTERS[idx]
    raise ValueError(f"task {row.get('id')!r} requires answer or answer_index")


def render_question(question: str, options: list[str]) -> str:
    letters = letters_for(options)
    rendered = "\n".join(f"{letter}. {option}" for letter, option in zip(letters, options))
    return f"{question.strip()}\n\n{rendered}"


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


def option_letter_token_ids(tokenizer, valid_letters: list[str]) -> list[int]:
    """Return one-token encodings for valid option letters; fail closed otherwise."""
    token_ids: list[int] = []
    for letter in valid_letters:
        encoded = tokenizer.encode(letter, add_special_tokens=False)
        if len(encoded) != 1:
            raise ValueError(
                f"option letter {letter!r} is not a single token under this tokenizer: {encoded}"
            )
        token_id = int(encoded[0])
        decoded = tokenizer.decode([token_id], skip_special_tokens=True).strip().upper()
        if decoded != letter:
            raise ValueError(
                f"tokenizer round-trip mismatch for option letter {letter!r}: "
                f"token_id={token_id} decoded={decoded!r}"
            )
        token_ids.append(token_id)
    return token_ids


def generate(
    tokenizer,
    model,
    prompt: str,
    *,
    seed: int,
    max_new_tokens: int,
    temperature: float,
    top_p: float,
    top_k: int,
    assistant_prefill: str,
    valid_choice_letters: list[str],
) -> tuple[str, int, int]:
    """Generate from a fixed assistant prefill with a constrained first choice token.

    The only token-level constraint is on the first generated token immediately
    after ``ANSWER: ``. It must be one of the task's declared option letters.
    All subsequent generation remains sampled under the frozen temperature,
    top-p, and top-k settings so the model still reports its own P_CORRECT.
    """
    set_seed(seed)
    messages = [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_prefill},
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        continue_final_message=True,
        enable_thinking=False,
    )
    inputs = tokenizer(text, return_tensors="pt").to(model.device)
    input_len = int(inputs["input_ids"].shape[-1])
    allowed_token_ids = option_letter_token_ids(tokenizer, valid_choice_letters)
    logits_processor = LogitsProcessorList(
        [FirstTokenChoiceLogitsProcessor(input_len, allowed_token_ids)]
    )
    with torch.inference_mode():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            pad_token_id=tokenizer.eos_token_id,
            logits_processor=logits_processor,
        )
    output_ids = outputs[0][input_len:]
    continuation = tokenizer.decode(output_ids, skip_special_tokens=True)
    decoded = (assistant_prefill + continuation).strip()
    return decoded, input_len, int(output_ids.shape[-1])


def generate_with_parse(
    tokenizer,
    model,
    prompt: str,
    *,
    base_seed: int,
    parser: re.Pattern[str],
    max_new_tokens: int,
    retries: int,
    temperature: float,
    top_p: float,
    top_k: int,
    assistant_prefill: str,
    valid_choice_letters: list[str],
) -> tuple[re.Match[str], str, int, int, int]:
    last_text = ""
    for attempt in range(retries + 1):
        seed = base_seed + attempt
        text, input_tokens, output_tokens = generate(
            tokenizer,
            model,
            prompt,
            seed=seed,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            assistant_prefill=assistant_prefill,
            valid_choice_letters=valid_choice_letters,
        )
        last_text = text
        match = parser.search(text)
        if match:
            return match, text, seed, input_tokens, output_tokens
    raise ValueError(f"could not parse output after {retries + 1} attempts: {last_text!r}")


def pre_prompt(question: str, options: list[str]) -> str:
    return (
        "Answer the multiple-choice question. Return exactly two lines:\n"
        "ANSWER: <one option letter>\n"
        "P_CORRECT: <a number from 0 to 1>\n"
        "P_CORRECT is your probability, before receiving any feedback, that your answer is correct.\n\n"
        + render_question(question, options)
    )


def post_prompt(row: dict) -> str:
    arm = row["arm"]
    if arm == "E0":
        intervention = "Review your previous answer and revise if necessary."
    elif arm == "E+":
        intervention = (
            "Verified feedback: your previous answer is incorrect.\n"
            "Review your previous answer and revise if necessary."
        )
    else:
        raise ValueError(f"unsupported arm {arm!r}")

    previous = (
        f"Your previous answer was {row['initial_answer']}. "
        f"Before feedback, you assigned probability {float(row['p_correct']):.6f} "
        "that this answer was correct."
    )
    return (
        render_question(str(row["question"]), [str(x) for x in row["options"]])
        + "\n\n"
        + previous
        + "\n\n"
        + intervention
        + "\n\nReturn exactly one line: ANSWER: <one option letter>"
    )


def run_pre(args: argparse.Namespace, tokenizer, model) -> int:
    tasks = read_jsonl(args.input)
    if args.limit is not None:
        tasks = tasks[: args.limit]
    output: list[dict] = []

    for index, task in enumerate(tasks, 1):
        task_id = str(task["id"])
        question = str(task["question"])
        options = [str(x) for x in task["options"]]
        valid_letters = letters_for(options)
        benchmark_answer = normalize_answer(task)
        prompt = pre_prompt(question, options)
        seed = stable_seed(args.seed, f"pre::{task_id}")
        match, raw_text, used_seed, input_tokens, output_tokens = generate_with_parse(
            tokenizer,
            model,
            prompt,
            base_seed=seed,
            parser=PRE_RE,
            max_new_tokens=args.pre_max_new_tokens,
            retries=args.parse_retries,
            temperature=args.temperature,
            top_p=args.top_p,
            top_k=args.top_k,
            assistant_prefill=ASSISTANT_PREFILL,
            valid_choice_letters=valid_letters,
        )
        initial_answer = match.group(1).upper()
        if initial_answer not in valid_letters:
            raise ValueError(f"{task_id}: parsed answer {initial_answer} outside valid options")
        p_correct = float(match.group(2))
        initial_correct = initial_answer == benchmark_answer
        now = datetime.now(timezone.utc).isoformat(timespec="seconds")
        row = {
            "id": task_id,
            "question": question,
            "options": options,
            "benchmark_answer": benchmark_answer,
            "category": task.get("category"),
            "source": task.get("src"),
            "initial_answer": initial_answer,
            "p_correct": p_correct,
            "i": 1.0 - p_correct,
            "initial_correct": initial_correct,
            "model_requested": args.model,
            "response_model": args.model,
            "response_id": f"local::{task_id}::{used_seed}",
            "reasoning_effort": "non-thinking",
            "backend": "transformers-local",
            "generation_seed": used_seed,
            "temperature": args.temperature,
            "top_p": args.top_p,
            "top_k": args.top_k,
            "interface_version": INTERFACE_VERSION,
            "assistant_prefill": ASSISTANT_PREFILL,
            "choice_constraint": CHOICE_CONSTRAINT,
            "pre_prompt": prompt,
            "raw_model_output": raw_text,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": input_tokens + output_tokens,
            "generated_at_utc": now,
        }
        output.append(row)
        print(
            f"[{index}/{len(tasks)}] {task_id}: answer={initial_answer} "
            f"key={benchmark_answer} p={p_correct:.3f} wrong={not initial_correct}",
            file=sys.stderr,
        )

    write_jsonl(args.output, output)
    wrong = sum(not row["initial_correct"] for row in output)
    print(f"wrote {len(output)} pre-treatment rows; {wrong} initially wrong", file=sys.stderr)
    return 0


def run_post(args: argparse.Namespace, tokenizer, model) -> int:
    rows = read_jsonl(args.input)
    if args.limit is not None:
        rows = rows[: args.limit]
    output: list[dict] = []

    for index, row in enumerate(rows, 1):
        options = [str(x) for x in row["options"]]
        valid_letters = letters_for(options)
        seed = stable_seed(args.seed, f"post::{row['id']}::{row['arm']}")
        prompt = post_prompt(row)
        match, raw_text, used_seed, input_tokens, output_tokens = generate_with_parse(
            tokenizer,
            model,
            prompt,
            base_seed=seed,
            parser=POST_RE,
            max_new_tokens=args.post_max_new_tokens,
            retries=args.parse_retries,
            temperature=args.temperature,
            top_p=args.top_p,
            top_k=args.top_k,
            assistant_prefill=ASSISTANT_PREFILL,
            valid_choice_letters=valid_letters,
        )
        final_answer = match.group(1).upper()
        if final_answer not in valid_letters:
            raise ValueError(f"{row['id']}: parsed final answer {final_answer} outside valid options")
        benchmark_answer = str(row["benchmark_answer"]).strip().upper()
        correct = final_answer == benchmark_answer
        out = dict(row)
        out.update(
            {
                "final_answer": final_answer,
                "v": 1 if correct else 0,
                "final_correct": correct,
                "post_model_requested": args.model,
                "post_response_model": args.model,
                "post_response_id": f"local::{row['id']}::{used_seed}",
                "post_reasoning_effort": "non-thinking",
                "post_backend": "transformers-local",
                "post_generation_seed": used_seed,
                "post_interface_version": INTERFACE_VERSION,
                "post_assistant_prefill": ASSISTANT_PREFILL,
                "post_choice_constraint": CHOICE_CONSTRAINT,
                "post_prompt": prompt,
                "post_raw_model_output": raw_text,
                "post_input_tokens": input_tokens,
                "post_output_tokens": output_tokens,
                "post_total_tokens": input_tokens + output_tokens,
                "post_generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            }
        )
        output.append(out)
        print(
            f"[{index}/{len(rows)}] {row['id']} {row['arm']}: "
            f"{row['initial_answer']} -> {final_answer} correct={correct}",
            file=sys.stderr,
        )

    write_jsonl(args.output, output)
    print(f"wrote {len(output)} post-treatment rows", file=sys.stderr)
    return 0


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--model", default="Qwen/Qwen3-4B")
    parser.add_argument("--seed", type=int, default=20260809)
    parser.add_argument("--limit", type=int)
    parser.add_argument("--temperature", type=float, default=0.7)
    parser.add_argument("--top-p", type=float, default=0.8)
    parser.add_argument("--top-k", type=int, default=20)
    parser.add_argument("--parse-retries", type=int, default=2)
    parser.add_argument("--pre-max-new-tokens", type=int, default=48)
    parser.add_argument("--post-max-new-tokens", type=int, default=24)


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="stage", required=True)
    pre = sub.add_parser("pre")
    add_common(pre)
    pre.set_defaults(func=run_pre)
    post = sub.add_parser("post")
    add_common(post)
    post.set_defaults(func=run_post)
    args = parser.parse_args()

    tokenizer, model = load_model(args.model)
    started = time.time()
    result = args.func(args, tokenizer, model)
    print(f"elapsed_seconds={time.time() - started:.1f}", file=sys.stderr)
    return result


if __name__ == "__main__":
    raise SystemExit(main())

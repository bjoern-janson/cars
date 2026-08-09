#!/usr/bin/env python3
"""Run the two-stage Pilot 0 MMLU-Pro assay against the OpenAI Responses API.

This script is experiment plumbing. It does not download MMLU-Pro and it does
not submit batch jobs. Feed it a frozen JSONL task sample, then use the existing
branch-preparation/randomization tools before the post-treatment stage.

Requires OPENAI_API_KEY. Uses Python standard library only.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Iterable

API_URL = "https://api.openai.com/v1/responses"
LETTERS = "ABCDEFGHIJ"


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
            handle.write(json.dumps(row, sort_keys=True) + "\n")


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


def extract_output_text(response: dict) -> str:
    pieces: list[str] = []
    for item in response.get("output", []):
        if item.get("type") != "message":
            continue
        for part in item.get("content", []):
            if part.get("type") == "output_text":
                pieces.append(part.get("text", ""))
    text = "".join(pieces).strip()
    if not text:
        raise ValueError("response contained no output_text")
    return text


def response_call(
    *,
    api_key: str,
    model: str,
    effort: str,
    prompt: str,
    schema_name: str,
    schema: dict,
    timeout: float,
    retries: int,
) -> tuple[dict, dict]:
    payload = {
        "model": model,
        "input": prompt,
        "store": False,
        "reasoning": {"effort": effort},
        "text": {
            "verbosity": "low",
            "format": {
                "type": "json_schema",
                "name": schema_name,
                "strict": True,
                "schema": schema,
            },
        },
    }
    body = json.dumps(payload).encode("utf-8")
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    last_error: Exception | None = None
    for attempt in range(retries + 1):
        request = urllib.request.Request(API_URL, data=body, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=timeout) as response:
                raw = json.loads(response.read().decode("utf-8"))
            parsed = json.loads(extract_output_text(raw))
            return parsed, raw
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, ValueError, json.JSONDecodeError) as exc:
            last_error = exc
            if attempt >= retries:
                break
            time.sleep(2 ** attempt)
    raise RuntimeError(f"OpenAI request failed after {retries + 1} attempts: {last_error}")


def usage_record(response: dict) -> dict:
    usage = response.get("usage") or {}
    return {
        "input_tokens": usage.get("input_tokens"),
        "output_tokens": usage.get("output_tokens"),
        "total_tokens": usage.get("total_tokens"),
        "response_id": response.get("id"),
        "response_model": response.get("model"),
    }


def run_pre(args: argparse.Namespace) -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is not set")

    tasks = read_jsonl(args.input)
    if args.limit is not None:
        tasks = tasks[: args.limit]
    output: list[dict] = []

    for index, task in enumerate(tasks, 1):
        task_id = str(task["id"])
        question = str(task["question"])
        options = [str(x) for x in task["options"]]
        benchmark_answer = normalize_answer(task)
        letters = letters_for(options)
        prompt = (
            "Answer the multiple-choice question. "
            "Return your best answer and your probability from 0 to 1 that this answer is correct. "
            "The probability should reflect your uncertainty before receiving any feedback.\n\n"
            + render_question(question, options)
        )
        schema = {
            "type": "object",
            "properties": {
                "answer": {"type": "string", "enum": letters},
                "p_correct": {"type": "number", "minimum": 0, "maximum": 1},
            },
            "required": ["answer", "p_correct"],
            "additionalProperties": False,
        }
        parsed, raw = response_call(
            api_key=api_key,
            model=args.model,
            effort=args.effort,
            prompt=prompt,
            schema_name="pilot0_pre_answer",
            schema=schema,
            timeout=args.timeout,
            retries=args.retries,
        )
        initial_answer = parsed["answer"].strip().upper()
        p_correct = float(parsed["p_correct"])
        initial_correct = initial_answer == benchmark_answer
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
            "reasoning_effort": args.effort,
            **usage_record(raw),
        }
        output.append(row)
        print(
            f"[{index}/{len(tasks)}] {task_id}: answer={initial_answer} "
            f"key={benchmark_answer} p={p_correct:.3f} wrong={not initial_correct}",
            file=sys.stderr,
        )
        if args.sleep:
            time.sleep(args.sleep)

    write_jsonl(args.output, output)
    wrong = sum(not row["initial_correct"] for row in output)
    print(f"wrote {len(output)} pre-treatment rows; {wrong} initially wrong", file=sys.stderr)
    return 0


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
        + "\n\nReturn your final answer."
    )


def run_post(args: argparse.Namespace) -> int:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("OPENAI_API_KEY is not set")

    rows = read_jsonl(args.input)
    if args.limit is not None:
        rows = rows[: args.limit]
    output: list[dict] = []

    for index, row in enumerate(rows, 1):
        options = [str(x) for x in row["options"]]
        schema = {
            "type": "object",
            "properties": {
                "answer": {"type": "string", "enum": letters_for(options)},
            },
            "required": ["answer"],
            "additionalProperties": False,
        }
        parsed, raw = response_call(
            api_key=api_key,
            model=args.model,
            effort=args.effort,
            prompt=post_prompt(row),
            schema_name="pilot0_post_answer",
            schema=schema,
            timeout=args.timeout,
            retries=args.retries,
        )
        final_answer = parsed["answer"].strip().upper()
        benchmark_answer = str(row["benchmark_answer"]).strip().upper()
        correct = final_answer == benchmark_answer
        out = dict(row)
        out.update(
            {
                "final_answer": final_answer,
                "v": 1 if correct else 0,
                "final_correct": correct,
                "post_model_requested": args.model,
                "post_reasoning_effort": args.effort,
                **{f"post_{k}": v for k, v in usage_record(raw).items()},
            }
        )
        output.append(out)
        print(
            f"[{index}/{len(rows)}] {row['id']} {row['arm']}: "
            f"{row['initial_answer']} -> {final_answer} correct={correct}",
            file=sys.stderr,
        )
        if args.sleep:
            time.sleep(args.sleep)

    write_jsonl(args.output, output)
    print(f"wrote {len(output)} post-treatment rows", file=sys.stderr)
    return 0


def add_common(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--model", default="gpt-5.6-luna")
    parser.add_argument(
        "--effort",
        default="low",
        choices=["none", "low", "medium", "high", "xhigh", "max"],
    )
    parser.add_argument("--limit", type=int)
    parser.add_argument("--timeout", type=float, default=180.0)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--sleep", type=float, default=0.0)


def main() -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="stage", required=True)

    pre = sub.add_parser("pre", help="generate frozen pre-treatment answers/confidence")
    add_common(pre)
    pre.set_defaults(func=run_pre)

    post = sub.add_parser("post", help="run randomized E0/E+ continuation branches")
    add_common(post)
    post.set_defaults(func=run_post)

    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())

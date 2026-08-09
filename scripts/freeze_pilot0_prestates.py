#!/usr/bin/env python3
"""Freeze Pilot 0 pre-treatment rows into auditable, tamper-evident state records.

Run this immediately after the pre-treatment API stage and before branch creation.
The output preserves the exact visible pre-treatment prompt/configuration and adds
canonical SHA-256 fingerprints. It does not alter the scientific measurement.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable

API_URL = "https://api.openai.com/v1/responses"
LETTERS = "ABCDEFGHIJ"
PROMPT_TEMPLATE_VERSION = "pilot0-pre-v1"


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            row = json.loads(raw)
            required = {
                "id",
                "question",
                "options",
                "benchmark_answer",
                "initial_answer",
                "p_correct",
                "i",
                "initial_correct",
                "model_requested",
                "reasoning_effort",
                "response_id",
                "response_model",
            }
            missing = required - row.keys()
            if missing:
                raise ValueError(f"line {line_no}: missing {sorted(missing)}")
            task_id = str(row["id"])
            if task_id in seen:
                raise ValueError(f"line {line_no}: duplicate id {task_id}")
            seen.add(task_id)
            rows.append(row)
    if not rows:
        raise ValueError("input contains no pre-treatment rows")
    return rows


def write_jsonl(path: Path, rows: Iterable[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def render_question(question: str, options: list[str]) -> str:
    if not (2 <= len(options) <= len(LETTERS)):
        raise ValueError(f"expected 2-{len(LETTERS)} options, got {len(options)}")
    letters = LETTERS[: len(options)]
    rendered = "\n".join(f"{letter}. {option}" for letter, option in zip(letters, options))
    return f"{question.strip()}\n\n{rendered}"


def exact_pre_prompt(row: dict) -> str:
    return (
        "Answer the multiple-choice question. "
        "Return your best answer and your probability from 0 to 1 that this answer is correct. "
        "The probability should reflect your uncertainty before receiving any feedback.\n\n"
        + render_question(str(row["question"]), [str(x) for x in row["options"]])
    )


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def freeze_row(row: dict, frozen_at: str) -> dict:
    prompt = exact_pre_prompt(row)
    request_config = {
        "api_url": API_URL,
        "model_requested": row["model_requested"],
        "reasoning_effort": row["reasoning_effort"],
        "store": False,
        "text_verbosity": "low",
        "structured_output_schema": "pilot0_pre_answer",
        "generation_seed": None,
        "prompt_template_version": PROMPT_TEMPLATE_VERSION,
    }
    audit = {
        "task_id": str(row["id"]),
        "question": row["question"],
        "options": row["options"],
        "benchmark_answer": row["benchmark_answer"],
        "initial_answer": row["initial_answer"],
        "p_correct": row["p_correct"],
        "i": row["i"],
        "initial_correct": row["initial_correct"],
        "pre_prompt": prompt,
        "pre_prompt_sha256": canonical_sha256(prompt),
        "request_config": request_config,
        "response_id": row["response_id"],
        "response_model": row["response_model"],
        "input_tokens": row.get("input_tokens"),
        "output_tokens": row.get("output_tokens"),
        "total_tokens": row.get("total_tokens"),
        "frozen_at_utc": frozen_at,
    }
    out = dict(row)
    out["pre_prompt"] = prompt
    out["pre_prompt_sha256"] = audit["pre_prompt_sha256"]
    out["pre_request_config"] = request_config
    out["pre_state_frozen_at_utc"] = frozen_at
    out["pre_state_audit"] = audit
    out["pre_state_sha256"] = canonical_sha256(audit)
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    frozen_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    frozen = [freeze_row(row, frozen_at) for row in rows]
    write_jsonl(args.output, frozen)

    print(f"froze {len(frozen)} pre-treatment states")
    print(f"freeze timestamp: {frozen_at}")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

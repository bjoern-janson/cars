#!/usr/bin/env python3
"""Freeze local/open-weight Pilot 0 prestates into auditable SHA-256 records."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    rows: list[dict] = []
    seen: set[str] = set()
    frozen_at = datetime.now(timezone.utc).isoformat(timespec="seconds")

    with args.input.open(encoding="utf-8") as handle:
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
                "response_model",
                "response_id",
                "backend",
                "generation_seed",
                "pre_prompt",
                "interface_version",
                "assistant_prefill",
                "choice_constraint",
            }
            missing = required - row.keys()
            if missing:
                raise ValueError(f"line {line_no}: missing {sorted(missing)}")
            task_id = str(row["id"])
            if task_id in seen:
                raise ValueError(f"line {line_no}: duplicate id {task_id}")
            seen.add(task_id)

            audit = {
                "task_id": task_id,
                "question": row["question"],
                "options": row["options"],
                "benchmark_answer": row["benchmark_answer"],
                "initial_answer": row["initial_answer"],
                "p_correct": row["p_correct"],
                "i": row["i"],
                "initial_correct": row["initial_correct"],
                "pre_prompt": row["pre_prompt"],
                "pre_prompt_sha256": canonical_sha256(row["pre_prompt"]),
                "interface_version": row["interface_version"],
                "assistant_prefill": row["assistant_prefill"],
                "choice_constraint": row["choice_constraint"],
                "backend": row["backend"],
                "model_requested": row["model_requested"],
                "response_model": row["response_model"],
                "response_id": row["response_id"],
                "reasoning_effort": row.get("reasoning_effort"),
                "generation_seed": row["generation_seed"],
                "temperature": row.get("temperature"),
                "top_p": row.get("top_p"),
                "top_k": row.get("top_k"),
                "raw_model_output": row.get("raw_model_output"),
                "input_tokens": row.get("input_tokens"),
                "output_tokens": row.get("output_tokens"),
                "total_tokens": row.get("total_tokens"),
                "generated_at_utc": row.get("generated_at_utc"),
                "frozen_at_utc": frozen_at,
            }
            out = dict(row)
            out["pre_prompt_sha256"] = audit["pre_prompt_sha256"]
            out["pre_state_frozen_at_utc"] = frozen_at
            out["pre_state_audit"] = audit
            out["pre_state_sha256"] = canonical_sha256(audit)
            rows.append(out)

    if not rows:
        raise ValueError("input contains no pre-treatment rows")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True, ensure_ascii=False) + "\n")

    print(f"froze {len(rows)} local pre-treatment states")
    print(f"freeze timestamp: {frozen_at}")
    print(f"wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

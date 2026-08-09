#!/usr/bin/env python3
"""Create replicated post-treatment branch units from eligible Pilot 0 prestates."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
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
            }
            missing = required - row.keys()
            if missing:
                raise ValueError(f"line {line_no}: missing {sorted(missing)}")
            rows.append(row)
    return rows


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--replicates", type=int, default=4)
    args = parser.parse_args()

    if args.replicates < 2:
        raise ValueError("replicates must be at least 2")

    rows = read_jsonl(args.input)
    branches: list[dict] = []
    eligible = 0
    for row in rows:
        if row["initial_correct"]:
            continue
        eligible += 1
        task_id = str(row["id"])
        for rep in range(args.replicates):
            branch = {
                "id": f"{task_id}::r{rep + 1}",
                "task_id": task_id,
                "stratum": task_id,
                "question": row["question"],
                "options": row["options"],
                "benchmark_answer": row["benchmark_answer"],
                "initial_answer": row["initial_answer"],
                "p_correct": row["p_correct"],
                "i": row["i"],
                "category": row.get("category"),
                "source": row.get("source"),
                "pre_response_id": row.get("response_id"),
                "pre_response_model": row.get("response_model"),
            }
            branches.append(branch)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in branches:
            handle.write(json.dumps(row, sort_keys=True) + "\n")

    print(f"eligible task-prestate blocks: {eligible}")
    print(f"created branches: {len(branches)}")
    print(f"branches per eligible block: {args.replicates}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

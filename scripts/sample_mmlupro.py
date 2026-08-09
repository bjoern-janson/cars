#!/usr/bin/env python3
"""Sample reproducible MMLU-Pro test items through the Hugging Face dataset-viewer API.

Uses Python standard library only. Public datasets normally require no token,
but HF_TOKEN is used if present. Sampling is by dataset row index and can
exclude IDs from earlier plumbing/development samples.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import urllib.parse
import urllib.request
from pathlib import Path

DATASET = "TIGER-Lab/MMLU-Pro"
CONFIG = "default"
SPLIT = "test"
NUM_TEST_ROWS = 12032
ROWS_URL = "https://datasets-server.huggingface.co/rows"
PAGE_SIZE = 100


def read_excluded(paths: list[Path]) -> set[str]:
    excluded: set[str] = set()
    for path in paths:
        with path.open(encoding="utf-8") as handle:
            for raw in handle:
                if not raw.strip():
                    continue
                row = json.loads(raw)
                if "id" in row:
                    excluded.add(str(row["id"]))
                if "question_id" in row:
                    excluded.add(str(row["question_id"]))
    return excluded


def fetch_page(offset: int, token: str | None) -> list[dict]:
    params = urllib.parse.urlencode(
        {
            "dataset": DATASET,
            "config": CONFIG,
            "split": SPLIT,
            "offset": offset,
            "length": PAGE_SIZE,
        }
    )
    request = urllib.request.Request(f"{ROWS_URL}?{params}")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.loads(response.read().decode("utf-8"))
    return payload["rows"]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output", type=Path)
    parser.add_argument("--n", type=int, default=30)
    parser.add_argument("--seed", type=int, default=20260809)
    parser.add_argument("--exclude-jsonl", type=Path, action="append", default=[])
    args = parser.parse_args()

    if not (1 <= args.n <= NUM_TEST_ROWS):
        raise ValueError(f"--n must be between 1 and {NUM_TEST_ROWS}")

    excluded = read_excluded(args.exclude_jsonl)
    rng = random.Random(args.seed)

    candidate_indices = list(range(NUM_TEST_ROWS))
    rng.shuffle(candidate_indices)

    pages: dict[int, list[dict]] = {}
    selected: list[dict] = []
    token = os.environ.get("HF_TOKEN")

    for row_idx in candidate_indices:
        page_offset = (row_idx // PAGE_SIZE) * PAGE_SIZE
        if page_offset not in pages:
            pages[page_offset] = fetch_page(page_offset, token)
        page = pages[page_offset]
        local = row_idx - page_offset
        if local >= len(page):
            continue
        record = page[local]["row"]
        question_id = str(record["question_id"])
        if question_id in excluded:
            continue
        selected.append(
            {
                "id": question_id,
                "question_id": record["question_id"],
                "dataset_row_idx": row_idx,
                "question": record["question"],
                "options": record["options"],
                "answer": record["answer"],
                "answer_index": record["answer_index"],
                "category": record.get("category"),
                "src": record.get("src"),
                "dataset": DATASET,
                "config": CONFIG,
                "split": SPLIT,
                "sample_seed": args.seed,
            }
        )
        if len(selected) == args.n:
            break

    if len(selected) != args.n:
        raise RuntimeError(
            f"could select only {len(selected)} rows after exclusions; requested {args.n}"
        )

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", encoding="utf-8") as handle:
        for row in selected:
            handle.write(json.dumps(row, sort_keys=True) + "\n")

    print(f"sampled {len(selected)} MMLU-Pro test items")
    print(f"seed: {args.seed}")
    print(f"excluded IDs: {len(excluded)}")
    print(f"wrote: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

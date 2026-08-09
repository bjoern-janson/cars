#!/usr/bin/env python3
"""Sample reproducible MMLU-Pro test items from one pinned Parquet snapshot.

The sampler downloads the public test Parquet through the Hugging Face Hub
resolver once, verifies its SHA-256, then samples locally by dataset row index.
This avoids repeated dataset-viewer API calls and keeps the benchmark snapshot
auditable. HF_TOKEN is optional for the public dataset.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
from pathlib import Path

try:
    import pyarrow.parquet as pq
    from huggingface_hub import hf_hub_download
except ImportError as exc:
    raise SystemExit(
        "sample_mmlupro.py requires huggingface_hub and pyarrow; "
        "install them with: pip install huggingface_hub pyarrow"
    ) from exc

DATASET = "TIGER-Lab/MMLU-Pro"
CONFIG = "default"
SPLIT = "test"
NUM_TEST_ROWS = 12032
DATASET_REVISION = "24ac2da5bb7c7b42ea1a984c6b535e35a73d30b3"
DATASET_FILE = "data/test-00000-of-00001.parquet"
DATASET_FILE_SHA256 = "0e24a191921c2f453518a537a8b2117bd137e7714d4ef1565e9ba06c1ecb9ad8"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


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


def load_test_rows(token: str | None) -> tuple[list[dict], Path, str]:
    cached = Path(
        hf_hub_download(
            repo_id=DATASET,
            repo_type="dataset",
            filename=DATASET_FILE,
            revision=DATASET_REVISION,
            token=token,
        )
    )
    actual_sha256 = sha256_file(cached)
    if actual_sha256 != DATASET_FILE_SHA256:
        raise ValueError(
            "MMLU-Pro test snapshot SHA-256 mismatch: "
            f"expected {DATASET_FILE_SHA256}, got {actual_sha256}"
        )

    table = pq.read_table(cached)
    rows = table.to_pylist()
    if len(rows) != NUM_TEST_ROWS:
        raise ValueError(
            f"expected {NUM_TEST_ROWS} MMLU-Pro test rows, got {len(rows)}"
        )
    return rows, cached, actual_sha256


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
    rows, cached_path, dataset_sha256 = load_test_rows(os.environ.get("HF_TOKEN"))

    rng = random.Random(args.seed)
    candidate_indices = list(range(NUM_TEST_ROWS))
    rng.shuffle(candidate_indices)

    selected: list[dict] = []
    for row_idx in candidate_indices:
        record = rows[row_idx]
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
                "dataset_revision": DATASET_REVISION,
                "dataset_file": DATASET_FILE,
                "dataset_file_sha256": dataset_sha256,
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
    print(f"dataset revision: {DATASET_REVISION}")
    print(f"dataset SHA-256: {dataset_sha256}")
    print(f"cached parquet: {cached_path}")
    print(f"seed: {args.seed}")
    print(f"excluded IDs: {len(excluded)}")
    print(f"wrote: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

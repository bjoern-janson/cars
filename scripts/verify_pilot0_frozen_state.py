#!/usr/bin/env python3
"""Verify Pilot 0 branch assignments against frozen pre-treatment state records."""

from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from pathlib import Path


def canonical_sha256(value: object) -> str:
    encoded = json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("frozen_prestates", type=Path)
    parser.add_argument("assignments", type=Path)
    args = parser.parse_args()

    frozen_rows = read_jsonl(args.frozen_prestates)
    assignment_rows = read_jsonl(args.assignments)

    frozen: dict[str, dict] = {}
    for row in frozen_rows:
        task_id = str(row["id"])
        audit = row.get("pre_state_audit")
        declared_hash = row.get("pre_state_sha256")
        if audit is None or declared_hash is None:
            raise ValueError(f"frozen prestate {task_id}: missing audit/hash")
        computed_hash = canonical_sha256(audit)
        if computed_hash != declared_hash:
            raise ValueError(
                f"frozen prestate {task_id}: hash mismatch "
                f"declared={declared_hash} computed={computed_hash}"
            )
        if task_id in frozen:
            raise ValueError(f"duplicate frozen task id {task_id}")
        frozen[task_id] = row

    per_task_hashes: dict[str, set[str]] = defaultdict(set)
    checked = 0
    visible_fields = (
        "question",
        "options",
        "benchmark_answer",
        "initial_answer",
        "p_correct",
        "i",
    )

    for row in assignment_rows:
        task_id = str(row.get("task_id") or str(row["id"]).split("::", 1)[0])
        if task_id not in frozen:
            raise ValueError(f"assignment {row.get('id')}: no frozen prestate for {task_id}")
        source = frozen[task_id]
        branch_hash = row.get("pre_state_sha256")
        if branch_hash != source["pre_state_sha256"]:
            raise ValueError(
                f"assignment {row.get('id')}: prestate hash differs from frozen record"
            )
        for field in visible_fields:
            if row.get(field) != source.get(field):
                raise ValueError(
                    f"assignment {row.get('id')}: field {field!r} differs from frozen prestate"
                )
        per_task_hashes[task_id].add(branch_hash)
        checked += 1

    for task_id, hashes in per_task_hashes.items():
        if len(hashes) != 1:
            raise ValueError(f"task {task_id}: branches reference multiple prestate hashes")

    print(f"verified frozen prestates: {len(frozen)}")
    print(f"verified assignment branches: {checked}")
    print(f"verified assigned task-prestate blocks: {len(per_task_hashes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

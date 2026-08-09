#!/usr/bin/env python3
"""Create balanced, deterministic randomized assignments for an LLM assay.

Input JSONL records require an `id`. Optional `stratum` values keep assignment
balanced within prespecified strata. All other fields are copied unchanged.
"""

from __future__ import annotations

import argparse
import json
import random
from collections import defaultdict
from pathlib import Path


def load_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            row = json.loads(raw)
            if "id" not in row:
                raise ValueError(f"line {line_no}: missing id")
            unit_id = str(row["id"])
            if unit_id in seen:
                raise ValueError(f"line {line_no}: duplicate id {unit_id}")
            if "arm" in row:
                raise ValueError(f"line {line_no}: input already contains arm")
            seen.add(unit_id)
            rows.append(row)
    if not rows:
        raise ValueError("input contains no units")
    return rows


def assign(rows: list[dict], arms: list[str], seed: int) -> list[dict]:
    if len(arms) < 2:
        raise ValueError("at least two arms are required")
    if len(set(arms)) != len(arms):
        raise ValueError("arm names must be unique")

    groups: dict[str, list[int]] = defaultdict(list)
    for idx, row in enumerate(rows):
        groups[str(row.get("stratum", "__all__"))].append(idx)

    assigned = [dict(row) for row in rows]
    rng = random.Random(seed)

    for stratum in sorted(groups):
        indices = groups[stratum][:]
        rng.shuffle(indices)
        arm_cycle = arms[:]
        rng.shuffle(arm_cycle)
        for position, idx in enumerate(indices):
            assigned[idx]["arm"] = arm_cycle[position % len(arm_cycle)]
            assigned[idx]["randomization_seed"] = seed

    return assigned


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, sort_keys=True) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--arms", nargs="+", default=["E0", "E+"])
    parser.add_argument("--seed", type=int, default=20260809)
    args = parser.parse_args()

    rows = load_jsonl(args.input)
    assigned = assign(rows, args.arms, args.seed)
    write_jsonl(args.output, assigned)

    counts: dict[tuple[str, str], int] = defaultdict(int)
    for row in assigned:
        counts[(str(row.get("stratum", "__all__")), row["arm"])] += 1
    for (stratum, arm), count in sorted(counts.items()):
        print(f"{stratum}\t{arm}\t{count}")
    print(f"wrote {len(assigned)} assignments to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

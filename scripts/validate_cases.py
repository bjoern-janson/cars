#!/usr/bin/env python3
"""Validate the internal CARS seed benchmark JSONL structure."""

from __future__ import annotations

import json
from pathlib import Path

REQUIRED = {"id", "category", "prompt", "expected_properties", "failure_traps"}


def main() -> int:
    path = Path(__file__).resolve().parents[1] / "benchmarks" / "seed_cases.jsonl"
    seen: set[str] = set()
    count = 0
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            item = json.loads(raw)
            missing = REQUIRED - item.keys()
            if missing:
                raise ValueError(f"line {line_no}: missing {sorted(missing)}")
            if item["id"] in seen:
                raise ValueError(f"line {line_no}: duplicate id {item['id']}")
            if not isinstance(item["expected_properties"], list) or not item["expected_properties"]:
                raise ValueError(f"line {line_no}: expected_properties must be a non-empty list")
            if not isinstance(item["failure_traps"], list) or not item["failure_traps"]:
                raise ValueError(f"line {line_no}: failure_traps must be a non-empty list")
            seen.add(item["id"])
            count += 1
    print(f"validated {count} CARS seed cases")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

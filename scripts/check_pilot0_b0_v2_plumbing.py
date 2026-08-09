#!/usr/bin/env python3
"""Plumbing-only non-degeneracy check for candidate Pilot 0 B0-v2 interface.

This check asks only whether the repaired interface escapes deterministic
baseline copying and can produce any matched signal-dependent response. It does
NOT inspect the desired E0/EU/EV ordering and has no authority over B, C, H1, or
B1.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import Counter, defaultdict
from pathlib import Path

SIGNALS = ("E0", "EU", "EV")


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            required = {
                "task_id",
                "replicate",
                "signal",
                "p_pre",
                "p_post",
                "m",
                "matched_generation_seed",
                "raw_model_output",
            }
            missing = required - row.keys()
            if missing:
                raise ValueError(f"{path}:{line_no}: missing {sorted(missing)}")
            rows.append(row)
    if not rows:
        raise ValueError(f"{path}: no rows")
    return rows


def same(a: float, b: float) -> bool:
    return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=1e-12)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    by_signal: dict[str, list[dict]] = defaultdict(list)
    matched: dict[tuple[str, int], dict[str, dict]] = defaultdict(dict)

    for row in rows:
        signal = str(row["signal"])
        if signal not in SIGNALS:
            raise ValueError(f"unsupported signal {signal!r}")
        p_pre = float(row["p_pre"])
        p_post = float(row["p_post"])
        expected_m = p_post - p_pre
        if not same(float(row["m"]), expected_m):
            raise ValueError(
                f"{row['task_id']} r{row['replicate']} {signal}: stored M != P_POST-P_PRE"
            )
        by_signal[signal].append(row)
        key = (str(row["task_id"]), int(row["replicate"]))
        if signal in matched[key]:
            raise ValueError(f"duplicate matched row for {key} {signal}")
        matched[key][signal] = row

    for signal in SIGNALS:
        if not by_signal[signal]:
            raise ValueError(f"no rows for signal {signal}")

    replicate_summary: dict[str, dict] = {}
    any_noncopy = False
    for signal in SIGNALS:
        signal_rows = by_signal[signal]
        copy_count = sum(
            same(float(row["p_post"]), float(row["p_pre"])) for row in signal_rows
        )
        noncopy_count = len(signal_rows) - copy_count
        any_noncopy = any_noncopy or noncopy_count > 0
        directions = Counter()
        for row in signal_rows:
            m = float(row["m"])
            if same(m, 0.0):
                directions["copy"] += 1
            elif m > 0:
                directions["up"] += 1
            else:
                directions["down"] += 1
        replicate_summary[signal] = {
            "n_rows": len(signal_rows),
            "copy_count": copy_count,
            "copy_rate": copy_count / len(signal_rows),
            "noncopy_count": noncopy_count,
            "direction_counts": dict(sorted(directions.items())),
        }

    matched_complete = 0
    matched_signal_difference = 0
    same_seed_failures = 0
    examples: list[dict] = []

    for (task_id, replicate), group in sorted(matched.items()):
        if set(group) != set(SIGNALS):
            raise ValueError(
                f"matched group {task_id} r{replicate} has signals {sorted(group)}, expected {list(SIGNALS)}"
            )
        matched_complete += 1
        seeds = {int(group[signal]["matched_generation_seed"]) for signal in SIGNALS}
        if len(seeds) != 1:
            same_seed_failures += 1
        values = {signal: float(group[signal]["p_post"]) for signal in SIGNALS}
        distinct = len({round(value, 12) for value in values.values()}) > 1
        if distinct:
            matched_signal_difference += 1
            if len(examples) < 10:
                examples.append(
                    {
                        "task_id": task_id,
                        "replicate": replicate,
                        "p_pre": float(group["E0"]["p_pre"]),
                        "p_post": values,
                    }
                )

    all_parsed = True  # reaching this point means every row parsed and validated
    pass_plumbing = (
        all_parsed
        and same_seed_failures == 0
        and any_noncopy
        and matched_signal_difference > 0
    )

    report = {
        "schema_version": 1,
        "study": "Pilot 0 B0-v2 candidate interface plumbing",
        "status": "PASS" if pass_plumbing else "FAIL",
        "authority": "instrumentation only; does not test manipulation ordering, B, C, H1, or B1",
        "input": str(args.input),
        "n_rows": len(rows),
        "replicate_level_by_signal": replicate_summary,
        "matched_signal_check": {
            "n_complete_task_replicates": matched_complete,
            "same_seed_failures": same_seed_failures,
            "n_with_nonidentical_p_post_across_signals": matched_signal_difference,
            "rate_with_nonidentical_p_post_across_signals": (
                matched_signal_difference / matched_complete if matched_complete else None
            ),
            "examples": examples,
        },
        "gate": {
            "all_rows_parsed": all_parsed,
            "any_replicate_level_noncopy": any_noncopy,
            "any_matched_signal_dependent_response": matched_signal_difference > 0,
            "pass_rule": (
                "PASS iff all requested probes parse, matched arms preserve one RNG seed, "
                "at least one P_POST differs from stored P_PRE, and at least one matched "
                "task/replicate has non-identical P_POST values across signals."
            ),
            "ordering_examined": false,
        },
        "interpretation_guardrails": [
            "This plumbing gate deliberately ignores whether E0, EU, and EV move in the intended direction.",
            "PASS means only that the repaired interface escaped deterministic baseline copying and is capable of signal-dependent output.",
            "FAIL means continue interface localization; do not strengthen or weaken B or C.",
            "No B1 run is authorized by plumbing PASS alone; B0-v2 must first be frozen and tested on a fresh manipulation cohort."
        ],
    }

    text = json.dumps(report, indent=2) + "\n"
    print(text, end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

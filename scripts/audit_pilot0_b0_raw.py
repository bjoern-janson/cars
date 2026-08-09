#!/usr/bin/env python3
"""Audit replicate-level raw outputs from failed Pilot 0 B0-v1.

This is a diagnostic audit only. It does not alter the B0 gate, reanalyze B1,
or update B/C/H1. Its purpose is to distinguish:

  * literal copying of the frozen P_PRE value;
  * stochastic movements that cancel after replicate averaging;
  * matched-signal insensitivity under the same RNG stream;
  * output-format artifacts in the probability probe.

The input is the already-generated B0 completed JSONL. No model calls occur.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Sequence

SIGNALS = ("E0", "EU", "EV")
FULL_OUTPUT_RE = re.compile(r"^P_POST:\s*(0(?:\.\d+)?|1(?:\.0+)?)\s*$", re.I)


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            row = json.loads(raw)
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
            if str(row["signal"]) not in SIGNALS:
                raise ValueError(f"{path}:{line_no}: unsupported signal {row['signal']!r}")
            expected_m = float(row["p_post"]) - float(row["p_pre"])
            if not math.isclose(float(row["m"]), expected_m, rel_tol=0.0, abs_tol=1e-12):
                raise ValueError(f"{path}:{line_no}: stored m != p_post-p_pre")
            rows.append(row)
    if not rows:
        raise ValueError(f"{path}: no rows")
    return rows


def mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs)


def sd(xs: Sequence[float]) -> float | None:
    if len(xs) < 2:
        return None
    m = mean(xs)
    return math.sqrt(sum((x - m) ** 2 for x in xs) / (len(xs) - 1))


def classify_delta(delta: float, tol: float = 1e-12) -> str:
    if abs(delta) <= tol:
        return "copy"
    return "up" if delta > 0 else "down"


def signal_summary(rows: Sequence[dict], signal: str) -> dict:
    use = [row for row in rows if str(row["signal"]) == signal]
    deltas = [float(row["m"]) for row in use]
    classes = Counter(classify_delta(delta) for delta in deltas)
    prompt_rounded_copy = sum(
        math.isclose(
            float(row["p_post"]),
            round(float(row["p_pre"]), 6),
            rel_tol=0.0,
            abs_tol=5e-7,
        )
        for row in use
    )
    strict_format = sum(bool(FULL_OUTPUT_RE.fullmatch(str(row["raw_model_output"]).strip())) for row in use)
    changed = [
        {
            "task_id": str(row["task_id"]),
            "replicate": int(row["replicate"]),
            "p_pre": float(row["p_pre"]),
            "p_post": float(row["p_post"]),
            "m": float(row["m"]),
            "raw_model_output": str(row["raw_model_output"]),
        }
        for row in use
        if classify_delta(float(row["m"])) != "copy"
    ]
    changed.sort(key=lambda row: abs(float(row["m"])), reverse=True)
    return {
        "n_replicate_rows": len(use),
        "mean_replicate_m": mean(deltas),
        "sd_replicate_m": sd(deltas),
        "copy_exact_count": classes["copy"],
        "copy_exact_rate": classes["copy"] / len(use),
        "copy_prompt_rounded_count": prompt_rounded_copy,
        "copy_prompt_rounded_rate": prompt_rounded_copy / len(use),
        "move_down_count": classes["down"],
        "move_up_count": classes["up"],
        "strict_one_line_output_count": strict_format,
        "strict_one_line_output_rate": strict_format / len(use),
        "largest_changed_examples": changed[:10],
    }


def replicate_averaging_audit(rows: Sequence[dict]) -> dict:
    grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in rows:
        grouped[(str(row["task_id"]), str(row["signal"]))].append(row)

    out: dict[str, dict] = {}
    for signal in SIGNALS:
        patterns = Counter()
        zero_average_nonzero_components = 0
        n_blocks = 0
        for (task_id, sig), block_rows in grouped.items():
            if sig != signal:
                continue
            if len(block_rows) != 2:
                raise ValueError(f"{task_id} {signal}: expected exactly 2 replicates")
            n_blocks += 1
            deltas = [float(row["m"]) for row in sorted(block_rows, key=lambda r: int(r["replicate"]))]
            labels = tuple(classify_delta(delta) for delta in deltas)
            patterns["/".join(labels)] += 1
            avg = mean(deltas)
            if math.isclose(avg, 0.0, rel_tol=0.0, abs_tol=1e-12) and any(
                not math.isclose(delta, 0.0, rel_tol=0.0, abs_tol=1e-12)
                for delta in deltas
            ):
                zero_average_nonzero_components += 1
        out[signal] = {
            "n_blocks": n_blocks,
            "replicate_direction_patterns": dict(sorted(patterns.items())),
            "zero_block_average_but_nonzero_replicates": zero_average_nonzero_components,
        }
    return out


def matched_signal_audit(rows: Sequence[dict]) -> dict:
    grouped: dict[tuple[str, int], dict[str, dict]] = defaultdict(dict)
    for row in rows:
        key = (str(row["task_id"]), int(row["replicate"]))
        signal = str(row["signal"])
        if signal in grouped[key]:
            raise ValueError(f"duplicate matched row for {key} {signal}")
        grouped[key][signal] = row

    pairs = (("E0", "EU"), ("EU", "EV"), ("E0", "EV"))
    counts = {f"{a}_vs_{b}": Counter() for a, b in pairs}
    same_seed_failures = 0
    examples: dict[str, list[dict]] = {f"{a}_vs_{b}": [] for a, b in pairs}

    for key, by_signal in sorted(grouped.items()):
        if set(by_signal) != set(SIGNALS):
            raise ValueError(f"matched unit {key}: missing signal rows")
        seeds = {int(by_signal[s]["matched_generation_seed"]) for s in SIGNALS}
        if len(seeds) != 1:
            same_seed_failures += 1
        for a, b in pairs:
            pa = float(by_signal[a]["p_post"])
            pb = float(by_signal[b]["p_post"])
            name = f"{a}_vs_{b}"
            if math.isclose(pa, pb, rel_tol=0.0, abs_tol=1e-12):
                counts[name]["identical"] += 1
            elif pa > pb:
                counts[name][f"{a}_higher"] += 1
                if len(examples[name]) < 10:
                    examples[name].append(
                        {
                            "task_id": key[0],
                            "replicate": key[1],
                            f"p_post_{a}": pa,
                            f"p_post_{b}": pb,
                        }
                    )
            else:
                counts[name][f"{b}_higher"] += 1
                if len(examples[name]) < 10:
                    examples[name].append(
                        {
                            "task_id": key[0],
                            "replicate": key[1],
                            f"p_post_{a}": pa,
                            f"p_post_{b}": pb,
                        }
                    )

    n = len(grouped)
    return {
        "n_matched_task_replicates": n,
        "same_seed_failures": same_seed_failures,
        "pairwise": {
            name: {
                **dict(counter),
                "identical_rate": counter["identical"] / n,
                "nonidentical_examples": examples[name],
            }
            for name, counter in counts.items()
        },
    }


def raw_output_frequency(rows: Sequence[dict]) -> dict:
    out: dict[str, list[dict]] = {}
    for signal in SIGNALS:
        counter = Counter(
            str(row["raw_model_output"]).strip()
            for row in rows
            if str(row["signal"]) == signal
        )
        out[signal] = [
            {"raw_model_output": text, "count": count}
            for text, count in counter.most_common(15)
        ]
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    rows = read_jsonl(args.input)
    report = {
        "schema_version": 1,
        "study": "Pilot 0 B0-v1 raw-response audit",
        "status": "diagnostic interface audit only; no B1/B/C/H1 update",
        "input": str(args.input),
        "n_rows": len(rows),
        "replicate_level_by_signal": {
            signal: signal_summary(rows, signal) for signal in SIGNALS
        },
        "replicate_averaging_audit": replicate_averaging_audit(rows),
        "matched_signal_same_rng_audit": matched_signal_audit(rows),
        "most_common_raw_outputs": raw_output_frequency(rows),
        "interpretation_guardrails": [
            "This audit inspects already-generated B0-v1 outputs and makes no new model calls.",
            "Replicate-level copying is distinguished from zero block means caused by cancellation.",
            "Matched signal comparisons use task/replicate pairs that shared the same RNG seed in B0-v1.",
            "Identical E0/EU outputs under matched RNG are evidence of probe/signal insensitivity under this interface, not proof that the model cannot represent uncertainty.",
            "A changed EV output does not by itself establish correct signal comprehension or a valid manipulation.",
            "No result from this audit authorizes B1 or promotes C.",
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

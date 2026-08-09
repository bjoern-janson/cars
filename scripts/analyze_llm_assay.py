#!/usr/bin/env python3
"""Analyze a completed randomized LLM assay from JSONL.

Required fields by default:
  id, arm, i, v

Optional:
  baseline, stratum

Primary statistic:
  treatment-effect contrast between exact high-I and low-I block tails.

For Pilot 0, each frozen pre-treatment state is a stratum/block with replicated
post-treatment branches. Exact tails are selected on unique strata, not branch
rows. Ties in I are broken deterministically by an outcome-blind SHA-256 key.
Permutation inference preserves the observed treatment counts within every
stratum, matching blocked randomization such as 2 x E0 / 2 x E+ per prestate.

A linear I x E coefficient is reported only as a secondary representation.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import Counter, defaultdict
from pathlib import Path
from typing import Iterable, Sequence


def mean(xs: Sequence[float]) -> float:
    if not xs:
        raise ValueError("mean of empty sequence")
    return sum(xs) / len(xs)


def solve_linear(a: list[list[float]], b: list[float]) -> list[float]:
    n = len(b)
    aug = [row[:] + [rhs] for row, rhs in zip(a, b)]
    for col in range(n):
        pivot = max(range(col, n), key=lambda r: abs(aug[r][col]))
        if abs(aug[pivot][col]) < 1e-12:
            raise ValueError("singular design matrix")
        aug[col], aug[pivot] = aug[pivot], aug[col]
        p = aug[col][col]
        aug[col] = [x / p for x in aug[col]]
        for r in range(n):
            if r == col:
                continue
            f = aug[r][col]
            if f:
                aug[r] = [x - f * y for x, y in zip(aug[r], aug[col])]
    return [aug[r][-1] for r in range(n)]


def ols(rows: Sequence[Sequence[float]], y: Sequence[float]) -> list[float]:
    p = len(rows[0])
    xtx = [[0.0] * p for _ in range(p)]
    xty = [0.0] * p
    for x, target in zip(rows, y):
        for j in range(p):
            xty[j] += x[j] * target
            for k in range(p):
                xtx[j][k] += x[j] * x[k]
    return solve_linear(xtx, xty)


def load(path: Path, fields: dict[str, str]) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    required = [fields["id"], fields["arm"], fields["i"], fields["v"]]
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            row = json.loads(raw)
            missing = [field for field in required if field not in row]
            if missing:
                raise ValueError(f"line {line_no}: missing {missing}")
            unit_id = str(row[fields["id"]])
            if unit_id in seen:
                raise ValueError(f"line {line_no}: duplicate id {unit_id}")
            seen.add(unit_id)
            row["_id"] = unit_id
            row["_arm"] = str(row[fields["arm"]])
            row["_i"] = float(row[fields["i"]])
            row["_v"] = float(row[fields["v"]])
            if fields["baseline"] in row:
                row["_baseline"] = float(row[fields["baseline"]])
            if fields["stratum"] in row:
                row["_stratum"] = str(row[fields["stratum"]])
            else:
                row["_stratum"] = "__all__"
            rows.append(row)
    if not rows:
        raise ValueError("no rows")
    return rows


def effect(rows: Iterable[dict], treated: str, control: str) -> float:
    t = [r["_v"] for r in rows if r["_arm"] == treated]
    c = [r["_v"] for r in rows if r["_arm"] == control]
    if not t or not c:
        raise ValueError("both treatment and control must be present in each analyzed slice")
    return mean(t) - mean(c)


def stable_tie_key(seed: int, stratum: str) -> str:
    return hashlib.sha256(f"{seed}::{stratum}".encode("utf-8")).hexdigest()


def block_i_values(rows: Sequence[dict]) -> dict[str, float]:
    grouped: dict[str, list[float]] = defaultdict(list)
    for row in rows:
        grouped[row["_stratum"]].append(row["_i"])

    out: dict[str, float] = {}
    for stratum, values in grouped.items():
        first = values[0]
        if any(not math.isclose(value, first, rel_tol=0.0, abs_tol=1e-12) for value in values[1:]):
            raise ValueError(f"stratum {stratum!r} contains multiple I values")
        out[stratum] = first
    return out


def exact_tail_blocks(rows: Sequence[dict], tie_seed: int) -> dict:
    """Choose literal bottom/top quarter of unique blocks.

    Blocks are ordered by I and then by a deterministic SHA-256 tie key derived
    only from the analysis tie seed and stratum identifier. Outcomes and arms do
    not enter tail assignment.
    """
    by_block = block_i_values(rows)
    n_blocks = len(by_block)
    q = n_blocks // 4
    if q < 1:
        raise ValueError("need at least 4 unique strata for exact tail analysis")

    ranked = sorted(
        by_block.items(),
        key=lambda pair: (pair[1], stable_tie_key(tie_seed, pair[0])),
    )
    low = ranked[:q]
    high = ranked[-q:]
    low_blocks = {stratum for stratum, _ in low}
    high_blocks = {stratum for stratum, _ in high}
    if low_blocks & high_blocks:
        raise ValueError("low/high exact tails overlap")

    low_values = [value for _, value in low]
    high_values = [value for _, value in high]
    return {
        "n_blocks": n_blocks,
        "tail_blocks": q,
        "low_blocks": low_blocks,
        "high_blocks": high_blocks,
        "i_low_min": min(low_values),
        "i_low_max": max(low_values),
        "i_high_min": min(high_values),
        "i_high_max": max(high_values),
        "strict_tail_ordering": max(low_values) < min(high_values),
        "tie_seed": tie_seed,
        "tie_breaker": "sha256(f'{tie_seed}::{stratum}')",
    }


def primary_stat(
    rows: Sequence[dict],
    treated: str,
    control: str,
    low_blocks: set[str],
    high_blocks: set[str],
) -> dict:
    low_rows = [r for r in rows if r["_stratum"] in low_blocks]
    high_rows = [r for r in rows if r["_stratum"] in high_blocks]
    tau_low = effect(low_rows, treated, control)
    tau_high = effect(high_rows, treated, control)
    return {
        "n_low_blocks": len(low_blocks),
        "n_high_blocks": len(high_blocks),
        "n_low_rows": len(low_rows),
        "n_high_rows": len(high_rows),
        "tau_low": tau_low,
        "tau_high": tau_high,
        "tau_high_minus_low": tau_high - tau_low,
    }


def interaction_delta(rows: Sequence[dict], treated: str, control: str, adjust_baseline: bool) -> float:
    use = [r for r in rows if r["_arm"] in (treated, control)]
    x: list[list[float]] = []
    y: list[float] = []
    baseline_available = adjust_baseline and all("_baseline" in r for r in use)
    for r in use:
        e = 1.0 if r["_arm"] == treated else 0.0
        row = [1.0, r["_i"], e, r["_i"] * e]
        if baseline_available:
            row.append(r["_baseline"])
        x.append(row)
        y.append(r["_v"])
    coefs = ols(x, y)
    return coefs[3]


def assignment_structure(rows: Sequence[dict], treated: str, control: str) -> dict:
    grouped: dict[str, Counter[str]] = defaultdict(Counter)
    for row in rows:
        if row["_arm"] in (treated, control):
            grouped[row["_stratum"]][row["_arm"]] += 1

    patterns: Counter[str] = Counter()
    missing_both: list[str] = []
    for stratum, counts in grouped.items():
        if counts[treated] == 0 or counts[control] == 0:
            missing_both.append(stratum)
        pattern = f"{control}={counts[control]},{treated}={counts[treated]}"
        patterns[pattern] += 1
    if missing_both:
        raise ValueError(
            "each analyzed stratum must contain treated and control assignments; "
            f"violations: {missing_both[:5]}"
        )
    return {
        "n_strata": len(grouped),
        "assignment_patterns": dict(sorted(patterns.items())),
        "permutation_rule": "shuffle observed arm labels only within each stratum",
    }


def permuted_arms(rows: Sequence[dict], treated: str, control: str, rng: random.Random) -> list[str]:
    arms = [r["_arm"] for r in rows]
    groups: dict[str, list[int]] = defaultdict(list)
    for idx, r in enumerate(rows):
        if r["_arm"] in (treated, control):
            groups[r["_stratum"]].append(idx)
    out = arms[:]
    for indices in groups.values():
        labels = [arms[idx] for idx in indices]
        rng.shuffle(labels)
        for idx, label in zip(indices, labels):
            out[idx] = label
    return out


def permutation_pvalues(
    rows: Sequence[dict],
    treated: str,
    control: str,
    low_blocks: set[str],
    high_blocks: set[str],
    observed: float,
    n_perm: int,
    seed: int,
) -> dict[str, float | int | None]:
    if n_perm <= 0:
        return {
            "valid_permutations": 0,
            "two_sided": None,
            "one_sided_positive": None,
            "one_sided_negative": None,
        }

    rng = random.Random(seed)
    two_sided = 0
    positive = 0
    negative = 0
    valid = 0
    base = [dict(r) for r in rows]

    for _ in range(n_perm):
        labels = permuted_arms(base, treated, control, rng)
        perm = [dict(r, _arm=label) for r, label in zip(base, labels)]
        stat = primary_stat(perm, treated, control, low_blocks, high_blocks)[
            "tau_high_minus_low"
        ]
        valid += 1
        if abs(stat) >= abs(observed):
            two_sided += 1
        if stat >= observed:
            positive += 1
        if stat <= observed:
            negative += 1

    denom = valid + 1
    return {
        "valid_permutations": valid,
        "two_sided": (two_sided + 1) / denom,
        "one_sided_positive": (positive + 1) / denom,
        "one_sided_negative": (negative + 1) / denom,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--treated", default="E+")
    parser.add_argument("--control", default="E0")
    parser.add_argument("--id-field", default="id")
    parser.add_argument("--arm-field", default="arm")
    parser.add_argument("--i-field", default="i")
    parser.add_argument("--v-field", default="v")
    parser.add_argument("--baseline-field", default="baseline")
    parser.add_argument("--stratum-field", default="stratum")
    parser.add_argument("--permutations", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=20260809)
    parser.add_argument(
        "--tail-tie-seed",
        type=int,
        default=20260809,
        help="Outcome-blind deterministic tie-break seed for exact block tails.",
    )
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    fields = {
        "id": args.id_field,
        "arm": args.arm_field,
        "i": args.i_field,
        "v": args.v_field,
        "baseline": args.baseline_field,
        "stratum": args.stratum_field,
    }
    rows = load(args.input, fields)
    use = [r for r in rows if r["_arm"] in (args.treated, args.control)]
    if len(use) < 8:
        raise ValueError("need at least 8 treated/control rows")
    arm_counts = Counter(r["_arm"] for r in use)
    if args.treated not in arm_counts or args.control not in arm_counts:
        raise ValueError("treated/control arms not both present")

    assignment = assignment_structure(use, args.treated, args.control)
    tails = exact_tail_blocks(use, args.tail_tie_seed)
    primary = primary_stat(
        use,
        args.treated,
        args.control,
        tails["low_blocks"],
        tails["high_blocks"],
    )
    delta_raw = interaction_delta(use, args.treated, args.control, adjust_baseline=False)
    baseline_available = all("_baseline" in r for r in use)
    delta_adj = (
        interaction_delta(use, args.treated, args.control, adjust_baseline=True)
        if baseline_available
        else None
    )
    pvals = permutation_pvalues(
        use,
        args.treated,
        args.control,
        tails["low_blocks"],
        tails["high_blocks"],
        primary["tau_high_minus_low"],
        args.permutations,
        args.seed,
    )

    tail_report = {
        key: value
        for key, value in tails.items()
        if key not in {"low_blocks", "high_blocks"}
    }

    report = {
        "schema_version": 2,
        "input": str(args.input),
        "treated": args.treated,
        "control": args.control,
        "n_rows": len(use),
        "arm_counts": dict(arm_counts),
        "assignment_structure": assignment,
        "exact_block_tail_definition": tail_report,
        "primary_ordering_test": primary,
        "secondary_linear_representation": {
            "delta_unadjusted": delta_raw,
            "delta_baseline_adjusted": delta_adj,
        },
        "randomization_inference": {
            "permutations_requested": args.permutations,
            "permutation_seed": args.seed,
            "valid_permutations": pvals["valid_permutations"],
            "one_sided_p_value_for_prespecified_positive_ordering": pvals[
                "one_sided_positive"
            ],
            "two_sided_p_value_for_nonzero_ordering": pvals["two_sided"],
            "one_sided_p_value_for_negative_ordering_diagnostic": pvals[
                "one_sided_negative"
            ],
            "stratum_field": args.stratum_field,
            "permutation_rule": "preserve observed treatment counts within every stratum",
        },
        "interpretation_guardrails": [
            "Primary scientific object is the treatment-effect ordering, not the linear coefficient.",
            "Exact low/high tails are defined on unique pre-treatment strata, not replicated branch rows.",
            "Tail ties are resolved deterministically without using outcomes or treatment assignments.",
            "The prespecified directional alternative is tau_high_minus_low > 0; the two-sided p-value answers a different question.",
            "A result is scoped to the supplied I, E, V, horizon, population, and measurement class.",
            "Permutation inference is valid only to the extent that the declared strata reproduce the actual assignment blocks.",
        ],
    }

    text = json.dumps(report, indent=2, sort_keys=False) + "\n"
    print(text, end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

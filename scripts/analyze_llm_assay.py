#!/usr/bin/env python3
"""Analyze a completed randomized LLM assay from JSONL.

Required fields by default:
  id, arm, i, v

Optional:
  baseline, stratum

The primary statistic is the treatment-effect contrast between high-I and low-I
strata. A linear I×E coefficient is reported as a secondary representation.
Permutation inference preserves treatment counts within declared strata.
"""

from __future__ import annotations

import argparse
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


def quartile_cutoffs(rows: Sequence[dict]) -> tuple[float, float]:
    values = sorted(row["_i"] for row in rows)
    n = len(values)
    if n < 8:
        raise ValueError("need at least 8 units for quartile analysis")
    lo = values[max(0, math.ceil(0.25 * n) - 1)]
    hi = values[max(0, math.ceil(0.75 * n) - 1)]
    return lo, hi


def effect(rows: Iterable[dict], treated: str, control: str) -> float:
    t = [r["_v"] for r in rows if r["_arm"] == treated]
    c = [r["_v"] for r in rows if r["_arm"] == control]
    if not t or not c:
        raise ValueError("both treatment and control must be present in each analyzed slice")
    return mean(t) - mean(c)


def primary_stat(rows: Sequence[dict], treated: str, control: str, lo: float, hi: float) -> dict:
    low_rows = [r for r in rows if r["_i"] <= lo]
    high_rows = [r for r in rows if r["_i"] >= hi]
    tau_low = effect(low_rows, treated, control)
    tau_high = effect(high_rows, treated, control)
    return {
        "i_low_cutoff": lo,
        "i_high_cutoff": hi,
        "n_low": len(low_rows),
        "n_high": len(high_rows),
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


def permutation_pvalue(
    rows: Sequence[dict],
    treated: str,
    control: str,
    lo: float,
    hi: float,
    observed: float,
    n_perm: int,
    seed: int,
) -> float | None:
    if n_perm <= 0:
        return None
    rng = random.Random(seed)
    extreme = 0
    base = [dict(r) for r in rows]
    for _ in range(n_perm):
        labels = permuted_arms(base, treated, control, rng)
        perm = [dict(r, _arm=label) for r, label in zip(base, labels)]
        try:
            stat = primary_stat(perm, treated, control, lo, hi)["tau_high_minus_low"]
        except ValueError:
            continue
        if abs(stat) >= abs(observed):
            extreme += 1
    return (extreme + 1) / (n_perm + 1)


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
        raise ValueError("need at least 8 treated/control units")
    arm_counts = Counter(r["_arm"] for r in use)
    if args.treated not in arm_counts or args.control not in arm_counts:
        raise ValueError("treated/control arms not both present")

    lo, hi = quartile_cutoffs(use)
    primary = primary_stat(use, args.treated, args.control, lo, hi)
    delta_raw = interaction_delta(use, args.treated, args.control, adjust_baseline=False)
    baseline_available = all("_baseline" in r for r in use)
    delta_adj = interaction_delta(use, args.treated, args.control, adjust_baseline=True) if baseline_available else None
    p_perm = permutation_pvalue(
        use,
        args.treated,
        args.control,
        lo,
        hi,
        primary["tau_high_minus_low"],
        args.permutations,
        args.seed,
    )

    report = {
        "schema_version": 1,
        "input": str(args.input),
        "treated": args.treated,
        "control": args.control,
        "n": len(use),
        "arm_counts": dict(arm_counts),
        "primary_ordering_test": primary,
        "secondary_linear_representation": {
            "delta_unadjusted": delta_raw,
            "delta_baseline_adjusted": delta_adj,
        },
        "randomization_inference": {
            "permutations": args.permutations,
            "two_sided_p_value_for_tau_high_minus_low": p_perm,
            "stratum_field": args.stratum_field,
        },
        "interpretation_guardrails": [
            "Primary scientific object is the treatment-effect ordering, not the linear coefficient.",
            "A positive result is scoped to the supplied I, E, V, horizon, population, and measurement class.",
            "Permutation inference is valid only to the extent that the declared assignment mechanism and strata match the experiment.",
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

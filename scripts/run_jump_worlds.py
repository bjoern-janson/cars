#!/usr/bin/env python3
"""Run threshold and rare-jump stress tests for the CARS minimal assay.

These worlds test whether the scientific ordering can survive non-smooth or
mixture-generated response structure without treating a linear interaction
coefficient as the scientific object.

Synthetic development evidence only.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from pathlib import Path
from statistics import mean
from typing import Iterable, Sequence


def linear_fit(xs: Sequence[float], ys: Sequence[float]) -> tuple[float, float]:
    mx = mean(xs)
    my = mean(ys)
    denom = sum((x - mx) ** 2 for x in xs)
    if denom <= 0:
        raise ValueError("zero variance in predictor")
    slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / denom
    intercept = my - slope * mx
    return intercept, slope


def interaction_fit(
    i_vals: Sequence[float],
    e_vals: Sequence[int],
    outcomes: Sequence[float],
) -> tuple[float, float]:
    control = [j for j, e in enumerate(e_vals) if e == 0]
    treated = [j for j, e in enumerate(e_vals) if e == 1]
    c_intercept, c_slope = linear_fit(
        [i_vals[j] for j in control], [outcomes[j] for j in control]
    )
    t_intercept, t_slope = linear_fit(
        [i_vals[j] for j in treated], [outcomes[j] for j in treated]
    )
    gamma = t_intercept - c_intercept
    delta = t_slope - c_slope
    return gamma, delta


def quantile_effects(
    i_vals: Sequence[float],
    e_vals: Sequence[int],
    outcomes: Sequence[float],
    fraction: float = 0.25,
) -> tuple[float, float, float]:
    order = sorted(range(len(i_vals)), key=lambda j: i_vals[j])
    k = max(2, int(len(order) * fraction))
    low = order[:k]
    high = order[-k:]

    def effect(indices: Iterable[int]) -> float:
        treated = [outcomes[j] for j in indices if e_vals[j] == 1]
        control = [outcomes[j] for j in indices if e_vals[j] == 0]
        return mean(treated) - mean(control)

    tau_low = effect(low)
    tau_high = effect(high)
    return tau_low, tau_high, tau_high - tau_low


def threshold_world(rng: random.Random, n: int) -> dict:
    threshold = 0.65
    jump_gain = 8.0
    i_vals = [rng.random() for _ in range(n)]
    e_vals = [rng.randrange(2) for _ in range(n)]
    true_tau = [0.0 if i < threshold else jump_gain for i in i_vals]
    outcomes = [
        20.0 + 2.0 * i + e * tau + rng.gauss(0, 1.5)
        for i, e, tau in zip(i_vals, e_vals, true_tau)
    ]

    gamma, delta = interaction_fit(i_vals, e_vals, outcomes)
    tau_low, tau_high, ordering = quantile_effects(i_vals, e_vals, outcomes)

    grid = [j / 100 for j in range(101)]
    fitted_tau = [gamma + delta * i for i in grid]
    true_grid_tau = [0.0 if i < threshold else jump_gain for i in grid]
    rmse = math.sqrt(
        mean((pred - truth) ** 2 for pred, truth in zip(fitted_tau, true_grid_tau))
    )
    max_abs_error = max(
        abs(pred - truth) for pred, truth in zip(fitted_tau, true_grid_tau)
    )

    ok = (
        ordering > 6.0
        and tau_low < 0.5
        and tau_high > 7.0
        and rmse > 1.5
        and max_abs_error > 3.0
    )

    return {
        "name": "threshold_jump_world",
        "status": "survived" if ok else "failed",
        "truth": {
            "tau_below_threshold": 0.0,
            "tau_at_or_above_threshold": jump_gain,
            "threshold": threshold,
        },
        "metrics": {
            "tau_low": tau_low,
            "tau_high": tau_high,
            "tau_high_minus_low": ordering,
            "linear_gamma": gamma,
            "linear_delta": delta,
            "linear_tau_rmse_against_true_step": rmse,
            "linear_tau_max_abs_error": max_abs_error,
        },
        "expectation": (
            "The order-based assay should detect the high-vs-low response difference, "
            "while the linear interaction smooths a discontinuous treatment-response shape."
        ),
    }


def rare_jump_world(rng: random.Random, n: int) -> dict:
    jump_gain = 30.0
    i_vals = [rng.random() for _ in range(n)]
    e_vals = [rng.randrange(2) for _ in range(n)]
    jump_prob = [0.02 + 0.10 * i for i in i_vals]

    jumped = []
    outcomes = []
    for i, e, p in zip(i_vals, e_vals, jump_prob):
        jump = 1 if (e == 1 and rng.random() < p) else 0
        jumped.append(jump)
        outcomes.append(20.0 + 2.0 * i + jump * jump_gain + rng.gauss(0, 2.0))

    gamma, delta = interaction_fit(i_vals, e_vals, outcomes)
    tau_low, tau_high, ordering = quantile_effects(i_vals, e_vals, outcomes)

    order = sorted(range(n), key=lambda j: i_vals[j])
    k = max(2, n // 4)
    low = order[:k]
    high = order[-k:]

    def treated_jump_rate(indices: Sequence[int]) -> float:
        treated = [j for j in indices if e_vals[j] == 1]
        return sum(jumped[j] for j in treated) / len(treated)

    jump_rate_low = treated_jump_rate(low)
    jump_rate_high = treated_jump_rate(high)

    ok = (
        ordering > 1.5
        and jump_rate_high > jump_rate_low + 0.05
        and jump_rate_high < 0.15
        and jump_rate_low < 0.05
    )

    return {
        "name": "rare_jump_mixture_world",
        "status": "survived" if ok else "failed",
        "truth": {
            "tau_i": "P(jump|i) * gain_if_jump",
            "jump_probability": "0.02 + 0.10*i",
            "gain_if_jump": jump_gain,
        },
        "metrics": {
            "tau_low": tau_low,
            "tau_high": tau_high,
            "tau_high_minus_low": ordering,
            "linear_gamma": gamma,
            "linear_delta": delta,
            "treated_jump_rate_low": jump_rate_low,
            "treated_jump_rate_high": jump_rate_high,
            "gain_if_jump": jump_gain,
        },
        "expectation": (
            "Positive mean moderation can arise because higher I changes the probability "
            "of a rare large jump even when jump magnitude is fixed. Mean CATE therefore "
            "does not identify probability-of-jump and value-of-jump separately."
        ),
    }


def run(seed: int, n: int) -> dict:
    threshold = threshold_world(random.Random(seed), n)
    rare = rare_jump_world(random.Random(seed + 1009), n)
    results = [threshold, rare]
    failures = [item["name"] for item in results if item["status"] == "failed"]
    return {
        "schema_version": 1,
        "seed": seed,
        "n_per_world": n,
        "evidence_status": "synthetic development evidence only",
        "results": results,
        "summary": {
            "total": len(results),
            "failed": len(failures),
            "failed_worlds": failures,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=20260809)
    parser.add_argument("--n", type=int, default=20000)
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    report = run(args.seed, args.n)
    for item in report["results"]:
        print(f"{item['status']:>10}  {item['name']}")
        for key, value in item["metrics"].items():
            if isinstance(value, float):
                print(f"    {key}: {value:.6g}")
            else:
                print(f"    {key}: {value}")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
        print(f"wrote {args.json_out}")
    return 1 if report["summary"]["failed"] else 0


if __name__ == "__main__":
    raise SystemExit(main())

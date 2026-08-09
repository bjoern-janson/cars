#!/usr/bin/env python3
"""Run deterministic synthetic red-team attacks against the CARS minimal assay.

This script is development infrastructure, not empirical evidence about real systems.
It generates known worlds, estimates treatment-effect moderation, and checks whether
the analysis pipeline recovers the expected nulls, sign changes, and invariances.
"""

from __future__ import annotations

import argparse
import json
import math
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Callable, Iterable, Sequence


@dataclass
class Fit:
    intercept: float
    beta_i: float
    beta_e: float
    delta_ie: float
    beta_baseline: float | None = None


@dataclass
class AttackResult:
    name: str
    status: str
    metrics: dict[str, float | int | str | bool]
    expectation: str


def mean(xs: Sequence[float]) -> float:
    return sum(xs) / len(xs)


def solve_linear(a: list[list[float]], b: list[float]) -> list[float]:
    """Solve Ax=b by Gaussian elimination with partial pivoting."""
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


def fit_interaction(
    i_vals: Sequence[float],
    e_vals: Sequence[float],
    outcomes: Sequence[float],
    baseline: Sequence[float] | None = None,
) -> Fit:
    rows: list[list[float]] = []
    for idx, (i, e) in enumerate(zip(i_vals, e_vals)):
        row = [1.0, i, e, i * e]
        if baseline is not None:
            row.append(baseline[idx])
        rows.append(row)
    coefs = ols(rows, outcomes)
    return Fit(
        intercept=coefs[0],
        beta_i=coefs[1],
        beta_e=coefs[2],
        delta_ie=coefs[3],
        beta_baseline=coefs[4] if baseline is not None else None,
    )


def quantile_strata_effect(
    i_vals: Sequence[float],
    e_vals: Sequence[int],
    outcomes: Sequence[float],
    low_fraction: float = 0.25,
) -> tuple[float, float, float]:
    order = sorted(range(len(i_vals)), key=lambda idx: i_vals[idx])
    k = max(2, int(len(order) * low_fraction))
    low = order[:k]
    high = order[-k:]

    def effect(indices: Iterable[int]) -> float:
        treated = [outcomes[j] for j in indices if e_vals[j] == 1]
        control = [outcomes[j] for j in indices if e_vals[j] == 0]
        return mean(treated) - mean(control)

    tau_low = effect(low)
    tau_high = effect(high)
    return tau_low, tau_high, tau_high - tau_low


def corr(xs: Sequence[float], ys: Sequence[float]) -> float:
    mx, my = mean(xs), mean(ys)
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    denx = math.sqrt(sum((x - mx) ** 2 for x in xs))
    deny = math.sqrt(sum((y - my) ** 2 for y in ys))
    return num / (denx * deny)


def attack_constant_effect(rng: random.Random, n: int) -> AttackResult:
    i_vals = [rng.gauss(0, 1) for _ in range(n)]
    e_vals = [rng.randrange(2) for _ in range(n)]
    baseline = [50 + 15 * i + rng.gauss(0, 5) for i in i_vals]
    y = [b + 5 * e + rng.gauss(0, 4) for b, e in zip(baseline, e_vals)]
    fit = fit_interaction(i_vals, e_vals, y, baseline)
    low, high, diff = quantile_strata_effect(i_vals, e_vals, y)
    ok = abs(fit.delta_ie) < 0.18 and abs(diff) < 0.45
    return AttackResult(
        "constant_effect_prognostic_I",
        "survived" if ok else "failed",
        {
            "delta_hat": fit.delta_ie,
            "tau_low": low,
            "tau_high": high,
            "tau_high_minus_low": diff,
            "corr_I_baseline": corr(i_vals, baseline),
        },
        "True treatment effect is constant; moderation should be approximately zero despite strong prognostic I.",
    )


def attack_ceiling(rng: random.Random, n: int) -> AttackResult:
    i_vals = [rng.random() for _ in range(n)]
    e_vals = [rng.randrange(2) for _ in range(n)]
    latent0 = [70 + 30 * i + rng.gauss(0, 4) for i in i_vals]
    latent = [v + 8 * e + rng.gauss(0, 2) for v, e in zip(latent0, e_vals)]
    observed = [min(100.0, max(0.0, v)) for v in latent]
    latent_fit = fit_interaction(i_vals, e_vals, latent)
    observed_fit = fit_interaction(i_vals, e_vals, observed)
    clipped = sum(v >= 100.0 for v in observed) / n
    ok = abs(latent_fit.delta_ie) < 0.45 and observed_fit.delta_ie < -2.0
    return AttackResult(
        "ceiling_measurement",
        "survived" if ok else "failed",
        {
            "latent_delta_hat": latent_fit.delta_ie,
            "observed_delta_hat": observed_fit.delta_ie,
            "upper_clip_fraction": clipped,
        },
        "Latent moderation is zero; bounded measurement should be able to manufacture negative observed moderation.",
    )


def attack_nonlinear_outcome(rng: random.Random, n: int) -> AttackResult:
    i_vals = [rng.random() for _ in range(n)]
    e_vals = [rng.randrange(2) for _ in range(n)]
    base = [20 + 80 * i for i in i_vals]
    latent = [v + 5 * e for v, e in zip(base, e_vals)]
    identity = latent
    logged = [math.log(v) for v in latent]
    squared = [v * v for v in latent]
    d_identity = fit_interaction(i_vals, e_vals, identity).delta_ie
    d_log = fit_interaction(i_vals, e_vals, logged).delta_ie
    d_square = fit_interaction(i_vals, e_vals, squared).delta_ie
    ok = abs(d_identity) < 0.05 and d_log < -0.01 and d_square > 100.0
    return AttackResult(
        "nonlinear_outcome_remeasurement",
        "estimand changed" if ok else "failed",
        {
            "delta_identity": d_identity,
            "delta_log": d_log,
            "delta_square": d_square,
        },
        "Same latent states can yield zero, negative, or positive additive moderation under nonlinear monotone outcome transformations.",
    )


def attack_affine_invariance(rng: random.Random, n: int) -> AttackResult:
    i_vals = [rng.gauss(0, 1) for _ in range(n)]
    e_vals = [rng.randrange(2) for _ in range(n)]
    y_a = [
        20 + 2 * i + 3 * e + 0.6 * i * e + rng.gauss(0, 2)
        for i, e in zip(i_vals, e_vals)
    ]
    a, b = 3.0, 7.0
    y_b = [a * y + b for y in y_a]
    d_a = fit_interaction(i_vals, e_vals, y_a).delta_ie
    d_b = fit_interaction(i_vals, e_vals, y_b).delta_ie
    ratio = d_b / d_a
    ok = abs(ratio - a) < 1e-9 and d_a * d_b > 0
    return AttackResult(
        "positive_affine_outcome",
        "survived" if ok else "failed",
        {"delta_A": d_a, "delta_B": d_b, "delta_ratio": ratio, "expected_ratio": a},
        "Positive affine outcome remeasurement must preserve moderation sign and scale the linear coefficient by a.",
    )


def attack_baseline_randomization(rng: random.Random, n: int) -> AttackResult:
    z = [rng.gauss(0, 1) for _ in range(n)]
    i_vals = [0.85 * zz + rng.gauss(0, 0.35) for zz in z]
    baseline = [40 + 12 * zz + 4 * zz * zz + rng.gauss(0, 4) for zz in z]
    e_vals = [rng.randrange(2) for _ in range(n)]
    y = [b + 5 * e + rng.gauss(0, 4) for b, e in zip(baseline, e_vals)]
    unadj = fit_interaction(i_vals, e_vals, y)
    adj = fit_interaction(i_vals, e_vals, y, baseline)
    ok = abs(unadj.delta_ie) < 0.35 and abs(adj.delta_ie) < 0.22
    return AttackResult(
        "baseline_structure_under_randomization",
        "survived" if ok else "failed",
        {
            "delta_unadjusted": unadj.delta_ie,
            "delta_adjusted": adj.delta_ie,
            "corr_I_baseline": corr(i_vals, baseline),
        },
        "Strong shared baseline structure should not manufacture systematic moderation when treatment is genuinely randomized.",
    )


def fit_arm_slope(
    i_vals: Sequence[float],
    arms: Sequence[str],
    outcomes: Sequence[float],
    target: str,
) -> float:
    keep = [idx for idx, arm in enumerate(arms) if arm in ("E0", target)]
    ii = [i_vals[j] for j in keep]
    ee = [1 if arms[j] == target else 0 for j in keep]
    yy = [outcomes[j] for j in keep]
    return fit_interaction(ii, ee, yy).delta_ie


def attack_generic_plasticity(rng: random.Random, n: int) -> AttackResult:
    i_vals = [rng.gauss(0, 1) for _ in range(n)]
    arms = [("E0", "E+", "E-")[rng.randrange(3)] for _ in range(n)]
    y = []
    for i, arm in zip(i_vals, arms):
        effect = 0.0
        if arm == "E+":
            effect = 3.0 + 0.6 * i
        elif arm == "E-":
            effect = -1.0 + 0.6 * i
        y.append(30 + 2 * i + effect + rng.gauss(0, 2))
    d_plus = fit_arm_slope(i_vals, arms, y, "E+")
    d_minus = fit_arm_slope(i_vals, arms, y, "E-")
    specificity = d_plus - d_minus
    ok = d_plus > 0.35 and d_minus > 0.35 and abs(specificity) < 0.20
    return AttackResult(
        "generic_plasticity",
        "survived" if ok else "failed",
        {
            "delta_plus": d_plus,
            "delta_minus": d_minus,
            "delta_plus_minus_delta_minus": specificity,
        },
        "Primary responsiveness can be positive while discrimination is approximately zero.",
    )


def attack_discriminative_responsiveness(rng: random.Random, n: int) -> AttackResult:
    i_vals = [rng.gauss(0, 1) for _ in range(n)]
    arms = [("E0", "E+", "E-")[rng.randrange(3)] for _ in range(n)]
    y = []
    for i, arm in zip(i_vals, arms):
        effect = 0.0
        if arm == "E+":
            effect = 3.0 + 0.6 * i
        elif arm == "E-":
            effect = -1.0 - 0.6 * i
        y.append(30 + 2 * i + effect + rng.gauss(0, 2))
    d_plus = fit_arm_slope(i_vals, arms, y, "E+")
    d_minus = fit_arm_slope(i_vals, arms, y, "E-")
    specificity = d_plus - d_minus
    ok = d_plus > 0.35 and d_minus < -0.35 and specificity > 0.75
    return AttackResult(
        "discriminative_responsiveness",
        "survived" if ok else "failed",
        {
            "delta_plus": d_plus,
            "delta_minus": d_minus,
            "delta_plus_minus_delta_minus": specificity,
        },
        "A discriminative world should separate warranted from misleading intervention responsiveness.",
    )


def attack_broken_randomization(rng: random.Random, n: int) -> AttackResult:
    z = [rng.gauss(0, 1) for _ in range(n)]
    i_vals = [0.85 * zz + rng.gauss(0, 0.35) for zz in z]
    baseline = [40 + 12 * zz + 8 * zz * zz + rng.gauss(0, 4) for zz in z]
    e_vals = []
    for zz in z:
        propensity = 1.0 / (1.0 + math.exp(-1.5 * zz))
        e_vals.append(1 if rng.random() < propensity else 0)
    y = [b + 5 * e + rng.gauss(0, 4) for b, e in zip(baseline, e_vals)]
    unadj = fit_interaction(i_vals, e_vals, y)
    adj = fit_interaction(i_vals, e_vals, y, baseline)
    ok = abs(unadj.delta_ie) > 5.0 and abs(adj.delta_ie) < 0.25
    return AttackResult(
        "broken_randomization_confounding",
        "survived" if ok else "failed",
        {
            "delta_unadjusted": unadj.delta_ie,
            "delta_baseline_adjusted": adj.delta_ie,
            "treated_fraction": sum(e_vals) / n,
            "corr_I_baseline": corr(i_vals, baseline),
        },
        "When treatment assignment depends on latent baseline structure, a constant true effect can produce very large false moderation.",
    )


def attack_high_correlation_disagreement(rng: random.Random, n: int) -> AttackResult:
    i_vals = [rng.gauss(0, 1) for _ in range(n)]
    e_vals = [rng.randrange(2) for _ in range(n)]
    base = [100 + 15 * i + rng.gauss(0, 2) for i in i_vals]
    v_a = [
        b + 5 * e + 0.6 * i * e + rng.gauss(0, 1)
        for b, e, i in zip(base, e_vals, i_vals)
    ]
    v_b = [
        3 * va + 7 - 2.4 * i * e + rng.gauss(0, 0.5)
        for va, i, e in zip(v_a, i_vals, e_vals)
    ]
    delta_a = fit_interaction(i_vals, e_vals, v_a).delta_ie
    delta_b = fit_interaction(i_vals, e_vals, v_b).delta_ie
    residual = [vb - (3 * va + 7) for va, vb in zip(v_a, v_b)]
    residual_delta = fit_interaction(i_vals, e_vals, residual).delta_ie
    agreement = corr(v_a, v_b)
    ok = agreement > 0.99 and delta_a > 0.3 and delta_b < -0.3 and residual_delta < -1.5
    return AttackResult(
        "high_correlation_causal_disagreement",
        "survived" if ok else "failed",
        {
            "corr_VA_VB": agreement,
            "delta_A": delta_a,
            "delta_B": delta_b,
            "residual_delta_IE": residual_delta,
        },
        "Very high ordinary correlation must not be treated as evidence that two instruments preserve the same heterogeneous causal contrast.",
    )


def attack_nonlinear_i_reparameterization(rng: random.Random, n: int) -> AttackResult:
    i_vals = [rng.random() for _ in range(n)]
    i_prime = [math.exp(4 * i) for i in i_vals]
    e_vals = [rng.randrange(2) for _ in range(n)]
    y = [
        20 + 2 * i + 3 * e + 0.8 * i * e + rng.gauss(0, 1)
        for i, e in zip(i_vals, e_vals)
    ]
    delta_i = fit_interaction(i_vals, e_vals, y).delta_ie
    delta_ip = fit_interaction(i_prime, e_vals, y).delta_ie
    _, _, ordering_i = quantile_strata_effect(i_vals, e_vals, y)
    _, _, ordering_ip = quantile_strata_effect(i_prime, e_vals, y)
    ok = ordering_i > 0.3 and abs(ordering_i - ordering_ip) < 1e-12 and abs(delta_i - delta_ip) > 0.5
    return AttackResult(
        "nonlinear_I_reparameterization",
        "survived" if ok else "failed",
        {
            "tau_high_minus_low_I": ordering_i,
            "tau_high_minus_low_Iprime": ordering_ip,
            "delta_I": delta_i,
            "delta_Iprime": delta_ip,
        },
        "Strictly increasing reparameterization of I preserves the primitive ordering while the numerical linear interaction coefficient can change substantially.",
    )


ATTACKS: list[Callable[[random.Random, int], AttackResult]] = [
    attack_constant_effect,
    attack_ceiling,
    attack_nonlinear_outcome,
    attack_affine_invariance,
    attack_baseline_randomization,
    attack_broken_randomization,
    attack_generic_plasticity,
    attack_discriminative_responsiveness,
    attack_high_correlation_disagreement,
    attack_nonlinear_i_reparameterization,
]


def run(seed: int, n: int) -> dict:
    results = []
    for idx, attack in enumerate(ATTACKS):
        rng = random.Random(seed + 1009 * idx)
        results.append(attack(rng, n))
    failures = [r.name for r in results if r.status == "failed"]
    return {
        "schema_version": 1,
        "seed": seed,
        "n_per_attack": n,
        "evidence_status": "synthetic development evidence only",
        "results": [asdict(r) for r in results],
        "summary": {
            "total": len(results),
            "failed": len(failures),
            "failed_attacks": failures,
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
        print(f"{item['status']:>16}  {item['name']}")
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

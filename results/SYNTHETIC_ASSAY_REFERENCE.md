# Synthetic Assay Reference Run

## Status

This is **synthetic development evidence only**.

It validates that the current executable red-team harness can recover several known nulls, artifacts, and invariances in generated worlds. It is not empirical support for the substantive CARS assay hypothesis in real systems.

Reference command:

```text
python scripts/run_assay_red_team.py \
  --seed 20260809 \
  --n 20000 \
  --json-out results/synthetic_assay_reference.json
```

Machine-readable output:

[`synthetic_assay_reference.json`](synthetic_assay_reference.json)

## Reference results

```text
SURVIVED
constant_effect_prognostic_I

δ_hat ≈ -0.0217
τ_high - τ_low ≈ +0.117
corr(I, baseline) ≈ 0.949
```

Interpretation: strong prognostic association did not manufacture meaningful treatment-effect moderation in the constant-effect randomized world.

```text
SURVIVED
ceiling_measurement

latent δ_hat   ≈ +0.163
observed δ_hat ≈ -5.141
upper clipping ≈ 17.0%
```

Interpretation: a bounded observed scale manufactured strong negative moderation while the latent treatment effect remained constant.

```text
ESTIMAND CHANGED
nonlinear_outcome_remeasurement

identity δ_hat ≈ 0
log δ_hat      ≈ -0.146
square δ_hat   ≈ +841.98
```

Interpretation: nonlinear monotone outcome transformations can change additive causal-effect shape and sign. This is an estimand change, not a licensed-invariance failure.

```text
SURVIVED
positive_affine_outcome

δ_A ≈ 0.57085
δ_B ≈ 1.71255
δ_B / δ_A = 3.0
```

The simulated transformation was:

```text
V_B = 3V_A + 7
```

The expected coefficient scaling was recovered to floating-point precision.

```text
SURVIVED
baseline_structure_under_randomization

unadjusted δ_hat ≈ -0.256
adjusted δ_hat   ≈ -0.0215
corr(I, baseline) ≈ 0.804
```

Interpretation: strong shared baseline structure can perturb a finite-sample unadjusted interaction, while prespecified baseline adjustment recovers the constant-effect null in this generated design.

```text
SURVIVED
generic_plasticity

δ+ ≈ +0.616
δ- ≈ +0.614
δ+ - δ- ≈ +0.0026
```

Interpretation: the primary responsiveness condition can pass while discriminative specificity is essentially absent.

```text
SURVIVED
discriminative_responsiveness

δ+ ≈ +0.640
δ- ≈ -0.519
δ+ - δ- ≈ +1.160
```

Interpretation: the specificity statistic separates the discriminative synthetic world from generic plasticity.

## What this run establishes

Within these generated worlds, the implementation currently distinguishes:

```text
prognostic association
≠
treatment-effect moderation
```

```text
latent constant effect
≠
bounded observed-scale effect
```

```text
licensed affine remeasurement
≠
nonlinear estimand change
```

```text
responsiveness
≠
discriminative responsiveness
```

## What it does not establish

This run does not establish:

- that any real system satisfies `τ(i₁) > τ(i₀)` for `i₁ > i₀`;
- that a proposed `M_I` measures intelligence;
- that a proposed `M_V` is construct-valid;
- that the current thresholds are a statistical power analysis;
- that these generated worlds cover all relevant assay failures;
- that a positive real result would transport across models, tasks, interventions, horizons, or outcome measurements.

The appropriate next use of this harness is adversarial extension: add new generated worlds when a plausible false-positive mechanism is discovered.

# Synthetic Assay Reference Run

## Status

This is **synthetic development evidence only**.

It validates that the current executable red-team harness can recover known nulls, artifacts, invariances, identification failures, and representation/estimator separations in generated worlds. It is not empirical support for the substantive CARS assay hypothesis in real systems.

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

### Constant effect with strongly prognostic I

```text
SURVIVED

δ_hat ≈ -0.0217
τ_high - τ_low ≈ +0.117
corr(I, baseline) ≈ 0.949
```

Strong prognostic association did not manufacture meaningful treatment-effect moderation in the randomized constant-effect world.

### Ceiling measurement

```text
SURVIVED

latent δ_hat   ≈ +0.163
observed δ_hat ≈ -5.141
upper clipping ≈ 17.0%
```

A bounded observed scale manufactured strong negative moderation while the latent treatment effect remained constant.

### Nonlinear outcome remeasurement

```text
ESTIMAND CHANGED

identity δ_hat ≈ 0
log δ_hat      ≈ -0.146
square δ_hat   ≈ +841.98
```

Nonlinear monotone outcome transformations can change additive causal-effect shape and sign. This is an estimand change, not a licensed-invariance failure.

### Positive affine outcome control

```text
SURVIVED

δ_A ≈ 0.57085
δ_B ≈ 1.71255
δ_B / δ_A = 3.0
```

For:

```text
V_B = 3V_A + 7
```

the expected coefficient scaling was recovered to floating-point precision.

### Baseline structure under randomization

```text
SURVIVED

unadjusted δ_hat ≈ -0.256
adjusted δ_hat   ≈ -0.0215
corr(I, baseline) ≈ 0.804
```

Strong shared baseline structure perturbed the finite-sample unadjusted interaction, while prespecified baseline adjustment recovered the constant-effect null in this generated design.

### Broken randomization / confounding

```text
SURVIVED AS AN ATTACK

unadjusted δ_hat ≈ +17.512
baseline-adjusted δ_hat ≈ +0.0226
corr(I, baseline) ≈ 0.657
```

Treatment assignment depended on latent baseline structure while the true treatment effect remained constant. The resulting false moderation was enormous. This attack demonstrates why genuine randomization is not optional.

### Generic plasticity

```text
SURVIVED

δ+ ≈ +0.640
δ- ≈ +0.681
δ+ - δ- ≈ -0.040
```

The primary responsiveness condition passed while discriminative specificity was approximately absent.

### Discriminative responsiveness

```text
SURVIVED

δ+ ≈ +0.592
δ- ≈ -0.581
δ+ - δ- ≈ +1.172
```

The specificity statistic separated the discriminative synthetic world from generic plasticity.

### High-correlation causal disagreement

```text
SURVIVED

corr(V_A, V_B) ≈ 0.999596
δ_A ≈ +0.610
δ_B ≈ -0.563
residual I×E coefficient ≈ -2.392
```

Two outcome instruments can agree almost perfectly in ordinary correlation while disagreeing in sign exactly where the heterogeneous causal claim lives. Convergent correlation is not causal-estimand equivalence.

### Nonlinear I reparameterization

```text
SURVIVED

τ_high - τ_low on I       ≈ +0.576773
τ_high - τ_low on f(I)    ≈ +0.576773
linear δ on I             ≈ +0.768812
linear δ on f(I)          ≈ +0.014004
```

The transform was strictly increasing. The primitive ordering survived exactly because the ordered units were unchanged, while the numerical linear interaction coefficient changed radically.

This directly demonstrates:

```text
hypothesis invariance
≠
estimator invariance
```

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
randomized treatment
≠
confounded treatment assignment
```

```text
high measurement correlation
≠
causal-estimand equivalence
```

```text
scientific ordering
≠
linear coefficient representation
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
- that the current thresholds constitute a statistical power analysis;
- that these generated worlds cover all relevant assay failures;
- that baseline adjustment repairs arbitrary confounding in observational data;
- that a positive real result would transport across models, tasks, interventions, horizons, or outcome measurements.

The appropriate next use of this harness is adversarial extension: add a generated world whenever a new plausible false-positive mechanism is discovered.

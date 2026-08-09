# CARS Ablation Plan

Ablations identify which assumptions, measurements, or protocol components matter **after an effect or failure is observed**.

Keep experimental surfaces distinct:

```text
CARS prompt ablation
≠
assay ablation
≠
measurement ablation
≠
historical catalyst/architecture ablation
```

## 1. CARS prompt-level ablations

Use these only for the control-protocol experiment.

### P0 — generic careful reasoning

Remove CARS-specific concepts while keeping a generic instruction to reason carefully, consider alternatives, check assumptions, and revise when warranted.

**Purpose:** control for generic deliberation and prompt attention.

### P1 — no representation-escalation gate

Remove the rule that representation/interface change requires evidence of representation insufficiency.

**Risk:** over-escalation after ordinary errors.

### P2 — no departure/adoption separation

Remove:

```text
A_leave ↛ A_adopt
```

**Risk:** incumbent rejection becomes successor validation.

### P3 — no unresolved-state permission

**Risk:** forced narrative completion.

### P4 — no independence emphasis

**Risk:** common-mode evidence receives excessive authority.

### P5 — no behavioral retest

**Risk:** retrospective explanation without future correction.

### P6 — no belief/decision separation

**Risk:** false certainty or decision paralysis.

### P7 — invariants only

Provide only compact CARS invariants.

**Question:** are the operating rules necessary beyond the principles?

## 2. Assay scientific-object ablations

These tests probe whether a reported result depends on stronger assumptions than the primitive proposition requires.

### A0 — ordered-strata test

Test only:

```text
i₁ > i₀
?
τ(i₁) > τ(i₀)
```

**Purpose:** closest representation of the scientific object.

### A1 — smooth derivative representation

Use:

```text
∂τ(i)/∂i > 0
```

**Question:** does smoothness add useful information or exclude valid monotone structure?

### A2 — linear moderation

Use:

```text
τ(i) = τ₀ + δi
```

**Question:** is linearity an adequate approximation?

A linear-model failure should not be promoted into a monotonicity failure without checking A0/A1.

## 3. Moderator measurement ablations

### I0 — affine reparameterization

```text
I' = aI+b
a>0
```

Expected: ordering and linear shape preserved up to coefficient rescaling.

### I1 — nonlinear monotone reparameterization

```text
I' = f(I)
f strictly increasing
```

Expected: primitive ordering preserved; linearity may not be.

**Purpose:** verify that the benchmark distinguishes scientific-proposition invariance from parametric invariance.

### I2 — degraded moderator reliability

Inject measurement noise or use a lower-reliability instrument.

**Question:** how quickly does attenuation or misclassification destroy detectable heterogeneity?

## 4. Outcome measurement ablations

### V0 — positive affine transform

```text
V' = aV+b
a>0
```

Expected:

```text
τ'(i)=aτ(i)
```

and identical treatment-effect ordering.

**Purpose:** positive control for licensed measurement invariance.

### V1 — nonlinear monotone transform

Examples:

```text
log(V+c)
```

or a convex monotone transform.

**Expected:** additive CATE may change; classify as a changed estimand unless independent measurement theory licenses equivalence.

### V2 — clipping / saturation

```text
V_obs = clip(V_latent, lower, upper)
```

**Question:** can bounded measurement manufacture moderation from constant latent treatment effect?

### V3 — independent interval instrument

Use a separately constructed `M_V^B` and independently calibrated affine link to `M_V^A`.

**Question:** does the treatment-effect ordering survive genuine interval-equivalent measurement?

## 5. Causal-identification ablations

### C0 — randomized assignment

Reference causal design.

### C1 — intentionally confounded assignment

Let treatment depend on baseline/latent structure.

**Purpose:** confirm that naive analysis can manufacture false HTE and that the evaluation protocol catches the identification failure.

### C2 — restricted positivity

Reduce treatment overlap in parts of the `I` support.

**Question:** does the estimator overstate certainty or extrapolate unsupported treatment effects?

### C3 — differential attrition

Make follow-up observation depend on treatment and/or `I`.

**Question:** does the assay detect loss of identification?

## 6. Headroom ablations

### H0 — matched baseline/headroom

Construct groups with similar current outcome opportunity but different `I`.

**Purpose:** reduce trivial response-range explanations.

### H1 — deliberately mismatched headroom

High and low `I` groups have different proximity to bounds.

**Purpose:** test artifact susceptibility.

### H2 — difficulty-adaptive outcome measurement

Use an instrument designed to maintain dynamic range across the `I` support.

**Question:** does moderation survive reduced ceiling/floor pressure?

## 7. Specificity ablations

### S0 — warranted intervention only

Tests primary responsiveness.

### S1 — add neutral intervention

Tests whether higher `I` responds indiscriminately to extra input.

### S2 — add misleading intervention

Tests discriminative responsiveness.

### S3 — intervention labels chosen by tested system

**Purpose:** negative control for circular authority assignment.

Expected: downgrade specificity evidence because intervention status is not independent.

## 8. Horizon ablations

Test:

```text
h₁, h₂, h₃
```

separately.

Possible patterns:

- transient effect;
- persistent effect;
- decay;
- reversal;
- overshoot.

Do not treat horizon dependence as a failure unless the claim was explicitly horizon-invariant.

## 9. Estimator ablations

Compare where justified:

- ordered-strata differences;
- flexible/nonparametric CATE estimation;
- preregistered linear interaction;
- alternative robust estimators.

The goal is not estimator shopping. Freeze the primary estimator before confirmatory testing and use alternatives diagnostically.

## 10. Historical catalyst and recursive-architecture ablations

The earlier catalyst and recursive-architecture ablations remain recoverable from Git history and the August 8 research notes.

If those surfaces are reactivated, preserve their original experimental identity rather than silently merging them into the current assay.

## Interpretation rule

For every ablation, state what level it targets:

```text
scientific object?
shape?
measurement?
causal identification?
estimator?
prompt mechanism?
```

A useful ablation localizes dependence. It should not be used to make a lower-level implementation artifact look like a high-level scientific result.

# Experiment Matrix

The current notebook separates:

```text
CARS prompt intervention
≠
minimal causal-responsiveness assay
≠
measurement invariance tests
≠
optional longitudinal / historical experiments
```

A result on one surface does not automatically establish another.

## 1. Primary assay

Define:

```text
τ(i)
=
E[V(e₁) - V(e₀) | I=i]
```

Primary proposition:

```text
i₁ > i₀
⇒
τ(i₁) > τ(i₀)
```

### Core conditions

| Condition | Assignment | Purpose |
|---|---|---|
| A0 | `E=e₀` | control potential-outcome arm |
| A1 | `E=e₁` | intervention potential-outcome arm |

Measure `I` before randomization and `V` after the prespecified horizon.

### Primary analyses

| Analysis | Object | Question |
|---|---|---|
| P1 | stratum/ordered CATE | is `τ(i₁) > τ(i₀)` for prespecified `i₁>i₀`? |
| P2 | monotonic shape | is `τ(i)` increasing over the relevant support? |
| P3 | smooth representation | is `∂τ(i)/∂i > 0` where differentiability is justified? |
| P4 | linear representation | if preregistered, is `δ>0` in `τ(i)=τ₀+δi`? |

P4 is not a substitute for P1/P2 unless linearity is adequately supported.

## 2. Constant-effect adversarial world

Construct:

```text
τ(i) = constant
```

while allowing strong association between `I` and baseline outcome.

Expected:

```text
no treatment-effect ordering by I
```

A positive moderation result is a benchmark failure requiring localization.

## 3. Ceiling / floor world

Keep the latent treatment effect constant and observe through:

```text
V_obs = clip(V_latent, lower, upper)
```

Vary the proportion of observations near the boundaries.

Questions:

- how much saturation is needed to manufacture apparent moderation?
- can headroom controls detect the artifact?
- does the sign reverse under realistic bounded measurement?

## 4. Nonlinear outcome-measurement world

Keep the underlying experimental states fixed while changing the measured outcome:

| Condition | Measurement | Expected status |
|---|---|---|
| M0 | `V` | reference estimand |
| M1 | `aV+b`, `a>0` | licensed affine-equivalent positive control |
| M2 | `log(V+c)` | generally different additive estimand |
| M3 | convex monotone transform | generally different additive estimand |

The benchmark should preserve the distinction:

```text
licensed invariance failure
≠
estimand-changing transformation
```

## 5. Baseline-structure / identification worlds

### R0 — randomized, prognostic moderator

```text
Z → I
Z → V_t
E randomized
τ(i) constant
```

Expected: no manufactured treatment-effect ordering.

### R1 — deliberately confounded treatment

Let treatment assignment depend on `Z` or baseline state.

Expected: naive analysis may manufacture heterogeneity; the benchmark should identify the causal-identification failure rather than promote the result.

## 6. Generic-plasticity / specificity worlds

Use intervention status established independently of the tested system:

```text
E⁺ = warranted correction
E⁰ = neutral / irrelevant
E⁻ = misleading
```

### S0 — generic plasticity

Higher `I` amplifies response to all intervention types.

Expected:

```text
primary responsiveness may pass
specificity should fail
```

### S1 — discriminative responsiveness

Higher `I` amplifies beneficial response to `E⁺` while leaving `E⁰` weak and avoiding beneficial response to `E⁻`.

Test separately:

```text
H_primary:
τ⁺ increases with I
```

and:

```text
H_specificity:
[τ⁺(i₁)-τ⁻(i₁)]
>
[τ⁺(i₀)-τ⁻(i₀)]
```

## 7. I-side reparameterization

Use strictly increasing transforms:

```text
I' = f(I)
```

including nonlinear `f`.

Expected:

```text
ordering hypothesis preserved
linear coefficient need not be preserved
```

This attack verifies that the benchmark distinguishes the scientific proposition from its parametric representation.

## 8. V-side affine invariance positive control

Use:

```text
V^B = aV^A + b
a > 0
```

Expected:

```text
τ_B(i) = aτ_A(i)
```

and:

```text
sign[τ_B(i₁)-τ_B(i₀)]
=
sign[τ_A(i₁)-τ_A(i₀)]
```

Under a linear model:

```text
δ_B = aδ_A
```

Failure is an implementation, estimation, or protocol problem.

## 9. Independent interval-instrument test

Construct two outcome instruments independently:

```text
M_V^A ← target
M_V^B ← target
```

### Gate A — calibration

Using independent calibration data, test whether:

```text
V^B ≈ aV^A + b
```

within a prespecified tolerance.

Freeze `a,b` before outcome analysis.

### Gate B — causal ordering

Test whether:

```text
sign[τ_B(i₁)-τ_B(i₀)]
=
sign[τ_A(i₁)-τ_A(i₀)]
```

If Gate A was genuinely passed and Gate B reverses with adequate precision, a real discrepancy exists.

## 10. High-correlation causal disagreement

After freezing the affine link:

```text
r = V^B - (aV^A+b)
```

fit/test:

```text
r ~ I + E + I×E
```

Key failure pattern:

```text
high corr(V^A,V^B)
+
nonzero residual I×E
```

This shows construct-level agreement without causal-estimand equivalence.

## 11. Sensitivity matrix

Vary:

- sample size;
- treatment allocation;
- variance of `I`;
- measurement reliability;
- treatment-effect magnitude;
- moderator-effect magnitude;
- ceiling/floor exposure;
- attrition;
- outcome noise.

Determine the range in which the assay can distinguish:

```text
flat
vs
small positive
vs
negative
vs
non-monotonic
```

before treating null results as substantive.

## 12. Horizon matrix

For a positive within-horizon result, test prespecified horizons separately:

```text
h₁, h₂, h₃, ...
```

Do not assume:

```text
τ_{h₁}(i) = τ_{h₂}(i)
```

Possible patterns include transient gain, persistence, decay, reversal, or overshoot.

## 13. Transport matrix

Only after within-design validation, vary one boundary at a time where feasible:

| Axis | Examples |
|---|---|
| intervention | correction type / intensity |
| domain | task family |
| population | model family / subject population |
| moderator measure | `M_I^A`, `M_I^B` |
| outcome measure | interval-equivalent `M_V^A`, `M_V^B` |
| generator | independently authored benchmark family |

Each boundary is a new empirical claim.

## 14. CARS prompt experiment

Keep the control-protocol experiment separate:

| Condition | Intervention | Purpose |
|---|---|---|
| C0 | none | native reasoning |
| C1 | generic careful-reasoning control | deliberation control |
| C2 | `CARS-CONTROL-PROTOCOL.md` | structured epistemic-control intervention |

Use `eval/SCORING.md`.

Prompt efficacy does not establish the causal-responsiveness hypothesis.

## 15. Historical prompt/catalyst/architecture experiments

Historical v0.1/v0.2 prompt comparisons and August 8 catalyst/recursive-architecture experiments remain reproducible from their files.

Use their dedicated scoring surfaces if reactivated.

They are not the current empirical frontier and should not be silently merged into assay evidence.

## Falsification ladder

```text
Does primary ordering hold?
        │
   ┌────┴────┐
   │         │
  NO        YES
   │         │
localize   attack measurement
and report      │
            ┌───┴───────────┐
            │               │
       dependency on    survives licensed
       measurement      transformations
            │               │
           STOP        test specificity
                            │
                       test h
                            │
                       test transport
                            │
                       test independent
                       measurement
```

The ladder is cumulative. Do not skip directly from one positive interaction coefficient to a general construct claim.

## Interpretation rule

A positive result should be scoped to the exact scientific object, measurement structure, intervention assignment, horizon, population, estimator, and benchmark generator actually tested.

A disagreement is informative only after determining whether the compared representations were licensed to preserve the same object.

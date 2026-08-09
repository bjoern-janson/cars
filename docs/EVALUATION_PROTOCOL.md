# CARS Evaluation Protocol

## Goal

Evaluate the scientific object actually under test, then localize failures before revising higher-level claims.

The current repository separates four evaluation surfaces:

```text
1. CARS prompt/control-protocol evaluation
2. minimal causal-responsiveness assay
3. measurement / invariance validation
4. optional historical catalyst or recursive-architecture evaluation
```

Evidence at one surface does not automatically validate another.

## A. Minimal assay

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

Use a randomized intervention whenever feasible.

### Required ordering

```text
measure I_t
→ randomize E_t
→ measure V_{t+h}
→ estimate τ_{t,h}(i)
→ test ordering
```

`I_t` is a pre-treatment moderator. Do not describe the result as a causal effect of `I` unless `I` is itself experimentally manipulated in a separate design.

## B. Scientific object before estimator

Evaluate at the most primitive level the data support.

Preferred hierarchy:

```text
LEVEL 1 — scientific proposition
τ(i₁) > τ(i₀) for i₁ > i₀

LEVEL 2 — shape representation
∂τ(i)/∂i > 0
or monotonicity over support

LEVEL 3 — parametric representation
τ(i) = τ₀ + δi

LEVEL 4 — estimator
regression / learner / nonparametric estimator
```

A failed lower-level representation does not automatically falsify a higher-level object.

## C. Measurement requirements

Measurement partly constitutes the identity of `τ`.

Before testing invariance, specify the admissible transformation class.

### Moderator `I`

The primary proposition uses order.

Strictly increasing reparameterizations preserve the substantive ordering.

A nonlinear monotone reparameterization may destroy linearity without changing the ordering hypothesis.

### Outcome `V`

The additive CATE uses differences.

Positive affine transformations preserve the additive-treatment-effect ordering:

```text
V' = aV + b
a > 0

τ'(i) = aτ(i)
```

General monotone nonlinear transforms are treated as potentially different causal estimands unless a separate measurement theory licenses equivalence.

See `MEASUREMENT_BOUNDARY.md`.

## D. Primary analysis

Where possible, report the conditional treatment-effect curve or prespecified stratum contrasts directly.

For ordered moderator values or strata:

```text
Δτ_10
=
τ(i₁) - τ(i₀)
```

with `i₁ > i₀`.

Primary question:

```text
Δτ_10 > 0 ?
```

If the linear model is preregistered and adequate:

```text
V_{t+h}
=
α + βI_t + γE_t + δ(I_t×E_t) + λV_t + ε
```

report `β`, `γ`, and `δ` separately.

Do not use `δ` as a substitute for checking the shape of `τ(i)` when nonlinear heterogeneity is plausible.

## E. Sensitivity and power

Before interpreting a null result, predeclare or estimate the smallest treatment-effect ordering difference the design is intended to resolve.

A null result with wide uncertainty is not the same as precise evidence for flat `τ(i)`.

Report:

- support/range of `I`;
- treatment counts across relevant `I` strata;
- uncertainty on `τ(i)` or contrasts;
- attrition and missingness;
- ceiling/floor exposure;
- outcome reliability;
- effective sample size under the estimator.

## F. Red-team phase

A positive result should not be promoted before the assay is attacked.

Use `RED_TEAM_PROTOCOL.md`.

At minimum include:

1. constant treatment effect + prognostic `I`;
2. ceiling/floor world;
3. nonlinear outcome remeasurement;
4. randomized baseline-structure control;
5. broken-randomization negative control;
6. generic-plasticity world;
7. positive affine measurement control;
8. independent interval-instrument test;
9. high-correlation residual `I×E` disagreement test;
10. nonlinear `I` reparameterization;
11. sensitivity / low-power attacks.

Classify each attack as:

```text
survived
failed
estimand changed
inconclusive
```

## G. Measurement-equivalence testing

For independently constructed outcome instruments `A` and `B`, first use independent calibration data to test whether they are legitimately interval-equivalent within declared tolerance:

```text
V^B ≈ aV^A + b
a > 0
```

Freeze `a,b` before the treatment-effect analysis.

Then test the primary ordering on both instruments.

A useful residual diagnostic is:

```text
r = V^B - (aV^A + b)

r ~ I + E + I×E
```

A systematic `I×E` residual indicates disagreement exactly where the scientific claim lives.

High ordinary correlation between instruments is not sufficient evidence of causal-estimand equivalence.

## H. Specificity phase

Only after the primary responsiveness result survives measurement attacks should the benchmark test discriminative responsiveness.

Use independently established intervention status:

```text
E⁺ = warranted correction
E⁰ = neutral / irrelevant
E⁻ = misleading
```

Estimate separate conditional treatment-effect functions:

```text
τ⁺(i)
τ⁰(i)
τ⁻(i)
```

Keep primary and specificity hypotheses distinct.

A stronger specificity contrast is:

```text
[τ⁺(i₁)-τ⁻(i₁)]
>
[τ⁺(i₀)-τ⁻(i₀)]
```

for `i₁ > i₀`.

## I. Horizon and transport

Treat each horizon `h` as part of the estimand.

```text
τ_{t,h₁}(i)
≠
τ_{t,h₂}(i)
```

in general.

Do not silently pool horizons.

After within-design validation, test transport across:

- intervention family;
- task/domain;
- population/model family;
- moderator instrument;
- outcome instrument;
- benchmark generator.

Transport is a new empirical claim at each boundary.

## J. CARS prompt evaluation

The CARS control protocol can separately be evaluated as a reasoning intervention.

Use identical tasks under:

```text
B0 — no CARS-specific intervention
B1 — generic careful-reasoning control
C0 — CARS control protocol
```

Score behavior, not vocabulary recognition.

Useful dimensions remain:

- failure localization;
- scope control;
- possibility/authority separation;
- independence sensitivity;
- revision proportionality;
- representation-escalation control;
- departure/adoption separation;
- unresolved-state calibration;
- behavioral transfer;
- belief/decision separation;
- task outcome;
- cost.

Use `eval/SCORING.md`.

A positive prompt result does not establish the heterogeneous-responsiveness assay.

## K. Historical catalyst / architecture evaluation

The August 8 catalyst and recursive-architecture documents are retained for lineage and optional separate testing.

If those experiments are run, continue to use their dedicated scoring surfaces:

- `eval/CATALYST_SCORING.md`;
- `eval/ARCHITECTURE_SCORING.md`.

Do not treat their results as evidence for the current assay unless the relevant causal and measurement objects are explicitly instantiated.

## L. Failure localization protocol

When an apparent contradiction appears, inspect the shallowest plausible locus first:

```text
1. intervention assignment / causal identification
2. measurement equivalence / saturation / error
3. scientific-object identity
4. shape representation
5. estimator / statistical specification
6. implementation
7. substantive proposition
```

This ordering is diagnostic, not ontological.

Stop escalation once independent evidence identifies the failure.

## M. Genuine contradiction criterion

A strong measurement-form contradiction requires:

```text
licensed transformation
+
reliable measurement
+
identified causal contrast
+
adequate estimator
+
opposite ordering
```

If those conditions hold, the discrepancy cannot be dismissed as harmless reparameterization.

## N. Cost accounting

Record where feasible:

- tokens / compute;
- latency;
- external tool calls;
- number of observations or interventions requested;
- abstention rate;
- measurement burden;
- benchmark construction cost.

A stronger result that depends on uncontrolled cost expansion should be reported as such.

## O. Result classes

Classify each result as:

- **positive within scope**;
- **negative/null**;
- **mixed tradeoff**;
- **estimand changed**;
- **invalid/inconclusive**.

Do not force every run into positive/negative if the scientific object was not preserved or identification failed.

## P. Reporting principle

A positive result should state exactly what gained authority and under which measurement, intervention, horizon, population, and estimator conditions.

A failed invariance test should state whether the tested transformation was licensed to preserve the same object.

The evaluation protocol is successful when it makes the location of failure explicit rather than merely labeling a run as robust or non-robust.

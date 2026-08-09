# Claims and Non-Claims

## Current repository-level claim

CARS is a living research notebook containing:

```text
1. an epistemic control protocol;
2. a minimal heterogeneous causal-response assay;
3. a measurement-boundary specification;
4. an adversarial falsification program;
5. historical prompt, catalyst, and recursive-architecture lineage.
```

None of these artifacts acquire empirical authority merely because they are mutually coherent.

## Role separation

Keep the following distinction explicit:

```text
CARS control protocol
≠
empirical assay
```

CARS governs how evidence is handled, failures are localized, authority is assigned, and revisions are made.

The assay tests a specific proposition and produces evidence for CARS to process.

Neither validates the other.

## Motivating conjecture

The broader research trajectory uses:

```text
I ∝ C_improve
```

as a motivating conjecture / design objective.

This is not an established definition of intelligence, a causal law, or the frozen assay hypothesis.

## Current scientific object

The assay defines:

```text
τ(i)
=
E[V(e₁) - V(e₀) | I=i]
```

and tests the primitive ordering proposition:

```text
i₁ > i₀
⇒
τ(i₁) > τ(i₀)
```

Where smoothness is justified, this can be represented as:

```text
∂τ(i)/∂i > 0
```

Under an explicitly justified linear specification:

```text
τ(i) = τ₀ + δi
δ > 0
```

The ordering proposition is the scientific object. The derivative and `δ` are representations of it.

## What a positive primary result would authorize

A valid positive result can support a scoped claim such as:

> Within intervention `E`, outcome measurement `M_V`, moderator measurement `M_I`, horizon `h`, population `P`, and the stated causal-identification and estimation protocol, higher pre-intervention `I` is associated with larger causal treatment effects on `V`.

It does not automatically establish:

- a causal effect of `I`;
- that `I` is intelligence;
- that `V` is viability, value, welfare, or utility;
- that `I ∝ τ`;
- linearity;
- a mechanism of responsiveness;
- discriminative correction capacity;
- transport to another intervention, domain, horizon, population, or measurement system.

## Measurement claim boundary

Measurement partly constitutes the identity of the scientific object.

For `I`, the primitive hypothesis is ordering-based. Strictly increasing reparameterizations preserve that order.

For `V`, the causal estimand is difference-based. For the current additive CATE, positive affine transformations preserve the treatment-effect ordering:

```text
V' = aV + b
a > 0

τ'(i) = aτ(i)
```

Therefore:

```text
sign[τ'(i₁)-τ'(i₀)]
=
sign[τ(i₁)-τ(i₀)]
```

General monotone nonlinear transformations of `V` are not assumed to preserve the same additive causal estimand.

See `MEASUREMENT_BOUNDARY.md`.

## Shape / estimator claim boundary

Keep explicit:

```text
scientific object
>
shape representation
>
estimator
```

Accordingly:

```text
estimator failure
↛
shape failure
```

and:

```text
linear δ failure
↛
monotonicity failure
```

unless the corresponding estimator and linear shape assumptions have independently been established as adequate.

## Responsiveness / specificity boundary

A positive result under a warranted intervention does not automatically establish discriminative responsiveness.

A system can satisfy:

```text
τ⁺ increasing with I
```

while also responding strongly to neutral or misleading interventions.

Specificity therefore requires separate conditions such as:

```text
E⁺
E⁰
E⁻
```

with intervention status established independently of the tested system.

## Dynamics / equilibrium boundary

Keep distinct:

```text
causal heterogeneity
≠
longitudinal dynamics
≠
equilibrium
≠
stationary stochastic distribution
```

A positive responsiveness result does not establish a longitudinal transition law for `I`.

If later work defines:

```text
T_h^(e)(i)
=
E[I_{t+h} | do(E_t=e), I_t=i]
```

then a fixed-point claim:

```text
i* = T_h^(e)(i*)
```

is a separate empirical statement requiring additional conditions.

## CARS prompt claim

`prompts/CARS-CONTROL-PROTOCOL.md` is a candidate epistemic control intervention.

A prompt-level experiment may test whether CARS improves reasoning relative to baseline or generic careful-reasoning controls.

That experiment is independent of the responsiveness assay. CARS prompt efficacy does not establish the assay hypothesis, and assay success does not establish CARS prompt efficacy.

Historical prompt snapshots remain in `prompts/CARS-v0.1.md` and `prompts/CARS-v0.2-CANDIDATE.md`.

## Historical catalyst / recursive-architecture claim

The August 8 catalyst and recursive-architecture artifacts remain part of the research lineage.

They are now treated primarily as:

- historical candidate interventions;
- mechanism hypotheses;
- diagnostic scaffolding;
- sources of adversarial benchmark dimensions.

They are not required by the current headline assay.

A catalyst-decoding result or recursive-architecture result should still be interpreted only within its own protocol if those historical surfaces are tested.

## Claims requiring evidence

Evidence may eventually support scoped statements such as:

- higher pre-intervention `I` orders larger causal response under a specified randomized intervention;
- the ordering survives licensed positive-affine outcome remeasurement;
- the result survives independently constructed interval-equivalent outcome instruments;
- the result persists across prespecified horizons;
- the result transfers across domains or populations;
- `I` predicts responsiveness beyond ordinary prognostic capability;
- higher `I` predicts greater discrimination between warranted and misleading intervention;
- CARS prompt use improves specified reasoning outcomes relative to matched controls;
- a longitudinal `I` transition map possesses a stable fixed point under a specified intervention regime.

Each statement requires its own measurement, protocol, and scope.

## Current non-claims

This repository does not currently establish that:

- CARS improves reasoning, safety, or real-world decisions;
- `I` is intelligence;
- `I ∝ C_improve` is a validated law or definition;
- `I ∝ τ`;
- higher `I` predicts larger causal responsiveness in real systems;
- the moderation relation is linear;
- arbitrary monotone outcome transformations preserve the result;
- generic intervention responsiveness is correction capacity;
- the assay identifies the mechanism of response;
- a stable mean equilibrium exists;
- a stationary stochastic distribution exists;
- the historical catalyst is effective;
- the historical recursive architecture is validated;
- the framework solves alignment or autonomous representation invention.

## Authority separation

Observed task success, treatment-effect heterogeneity, or measurement agreement does not automatically establish:

- mechanism;
- causal attribution to `I`;
- future reliability;
- provenance quality;
- transport;
- robustness;
- safety;
- measurement equivalence;
- construct identity.

Likewise:

```text
A_leave ↛ A_adopt
```

Evidence sufficient to withdraw authority from an incumbent claim does not automatically grant authority to a proposed replacement.

## Genuine contradiction rule

Before testing invariance, specify the transformation class licensed to preserve the object.

A strong contradiction to a claimed measurement-form invariance requires:

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

If that occurs, localize the failure before revising the substantive proposition.

The protocol is not designed to make claims unfalsifiable. It is designed to make the location of falsification explicit.

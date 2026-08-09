# CARS Research Contract

## Status

This is the current repository-level research contract.

It separates:

```text
CARS control protocol
≠
heterogeneous causal-response assay
≠
optional longitudinal / equilibrium extensions
```

Historical prompt, catalyst, and recursive-architecture artifacts remain available for lineage and separate experiments.

## Primary empirical question

For a pre-intervention measured quantity `I`, intervention `E ∈ {e₀,e₁}`, and prespecified outcome `V`, define:

```text
τ(i)
=
E[V(e₁) - V(e₀) | I=i]
```

The primary scientific proposition is:

```text
i₁ > i₀
⇒
τ(i₁) > τ(i₀)
```

The experiment asks whether higher pre-intervention `I` orders larger causal treatment effects on later `V`.

## What the primary question does not assume

It does not assume that:

- `I` is intelligence;
- `I` causes `τ`;
- `V` is value, viability, utility, welfare, or performance by definition;
- the relation is linear;
- `I ∝ τ`;
- `I ∝ C_improve` is an empirical law;
- generic intervention responsiveness is discriminative correction capacity.

## Minimal design

```text
measure I_t
→ randomize E_t
→ measure V_{t+h}
→ estimate τ_{t,h}(i)
→ test ordering
```

The temporal ordering is not a causal arrow from `I` to `τ`.

## Measurement contract

Measurement partly constitutes the identity of the scientific object.

The admissible transformation classes must be specified before invariance claims are tested.

### I side

The primitive proposition uses order.

Strictly increasing transformations of `I` preserve the substantive ordering.

### V side

The additive CATE uses differences.

Positive affine transformations:

```text
V' = aV + b
a > 0
```

preserve:

```text
τ'(i) = aτ(i)
```

and therefore preserve the ordering of treatment-effect heterogeneity.

General monotone nonlinear transformations are not assumed to preserve the same additive causal estimand.

## Shape contract

The scientific proposition is not identical to a parametric model.

Where justified:

```text
∂τ(i)/∂i > 0
```

is a smooth representation.

A preregistered linear approximation may use:

```text
τ(i) = τ₀ + δi
δ > 0
```

but:

```text
δ failure
↛
monotonicity failure
```

unless linearity is itself established as adequate.

## Identification contract

Prefer randomized intervention assignment.

Randomization is used to identify the causal contrast of `E` on `V` within the experimental design.

Randomization does not make `I` causal. `I` remains a pre-treatment moderator.

Record treatment assignment, exclusions, attrition, protocol deviations, and any design restriction that could compromise positivity or identification.

## Primary outcome

The primary outcome is the ordering of estimated conditional treatment effects over prespecified ordered `I` values, strata, or a monotonicity functional.

A linear `I×E` coefficient is a secondary representation when the linear model is justified.

## Primary negative outcomes

Scientifically meaningful negative or mixed outcomes include:

- flat `τ(i)` within adequate precision;
- decreasing `τ(i)`;
- non-monotonic `τ(i)` that violates the global ordering claim;
- apparent moderation explained by ceiling/floor geometry;
- sign dependence on an outcome transformation not licensed to preserve the same estimand;
- disagreement between instruments that fail interval-equivalence calibration;
- positive response under warranted intervention accompanied by equally strong response to misleading intervention;
- results that disappear under independent measurement or held-out domains;
- insufficient sensitivity to distinguish zero from the preregistered smallest effect of interest.

## Red-team requirement

Before strong positive interpretation, the assay should be challenged with adversarial worlds or controls designed to manufacture false moderation.

Minimum attacks are described in `RED_TEAM_PROTOCOL.md`.

Important families include:

- constant effect + prognostic `I`;
- ceiling/floor saturation;
- nonlinear outcome measurement;
- baseline structure and broken-randomization controls;
- generic plasticity;
- affine measurement positive controls;
- independently constructed interval-equivalent instruments;
- high-correlation causal disagreement;
- nonlinear `I` reparameterization;
- sensitivity limits.

## Specificity extension

A positive primary result licenses a stronger follow-up, not an automatic stronger interpretation.

Use independently established intervention status:

```text
E⁺
E⁰
E⁻
```

to test whether higher `I` predicts discrimination between warranted and misleading interventions rather than generic susceptibility.

## Transport contract

A result is scoped to the tested:

```text
intervention
outcome measurement
moderator measurement
horizon
domain
population
estimator
causal-identification design
```

Transport across any of these is a separate empirical claim.

## CARS prompt experiment

The CARS control protocol can separately be tested as a reasoning intervention against baseline and generic careful-reasoning controls.

Prompt efficacy does not establish the heterogeneous-responsiveness hypothesis.

Assay success does not establish prompt efficacy.

## Historical research surfaces

The August 8 catalyst and recursive-architecture artifacts remain historical research surfaces.

They may be tested separately, but their results should not be silently promoted into the current assay claim.

## Optional longitudinal extension

Only if data warrant it, define:

```text
T_h^(e)(i)
=
E[I_{t+h} | do(E_t=e), I_t=i]
```

A fixed point or contraction result is a separate claim about longitudinal dynamics.

Do not treat it as implied by the primary responsiveness assay.

## Claim rule

A positive result authorizes only the tested scientific object under the measurement, identification, estimation, and scope conditions actually used.

A negative result should be localized before revision.

A genuine contradiction at the scientific-proposition level requires that lower-level explanations—measurement identity, causal identification, shape representation, estimator adequacy, and implementation—have been sufficiently ruled out.

## Version discipline

Record the exact prompt, assay specification, measurement instruments, intervention protocol, code, estimator, and repository commit used for any result whose evidential status matters.

A changed object should receive a new version or explicit comparison condition rather than being silently treated as the same experiment.

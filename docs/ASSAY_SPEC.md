# CARS Minimal Assay Specification

## Status

> **Historical Pilot-0 assay specification.** This document is preserved as the frozen specification for the Pilot-0 causal-response program. It is **not** the repository's current top-level scientific object or active benchmark.

Current repository-level state:

- [`INTELLIGENCE_THEORY.md`](INTELLIGENCE_THEORY.md)
- [`CURRENT_RESEARCH_STATE.md`](CURRENT_RESEARCH_STATE.md)
- [`RESEARCH_CONTRACT.md`](RESEARCH_CONTRACT.md)

CARS governs how evidence is processed. This historical assay tested one scientific proposition.

## Scientific object

For a pre-intervention measured quantity `I`, define the conditional causal response:

```text
τ(i)
=
E[V(e₁) - V(e₀) | I=i]
```

where:

- `I` is measured before intervention;
- `E ∈ {e₀,e₁}` is experimentally assigned;
- `V` is a prespecified outcome measured after the intervention;
- `τ(i)` is the conditional average treatment effect on the chosen outcome scale.

The primitive Pilot-0 proposition was an ordering claim:

```text
i₁ > i₀
⇒
τ(i₁) > τ(i₀)
```

This proposition is historical and was not supported by the Pilot-0 implementation using `I₁ = 1 - P(correct)`. See [`../results/PILOT0_TERMINAL_RECORD.md`](../results/PILOT0_TERMINAL_RECORD.md).

## Representations of the proposition

The ordering claim is more primitive than any particular smooth or parametric representation.

Where differentiability is justified:

```text
∂τ(i)/∂i > 0
```

Under an explicitly preregistered linear moderation model:

```text
τ(i) = τ₀ + δi
δ > 0
```

These are stronger representations of the ordering proposition, not replacements for it.

Therefore:

```text
δ failure
↛
monotonicity failure
```

unless the linear specification has itself been established as adequate.

## Minimal experimental design

```text
measure I_t
    ↓
randomize E_t
    ↓
measure V_{t+h}
    ↓
estimate τ_{t,h}(i)
    ↓
test whether τ increases with i
```

The temporal ordering does not assert that `I` causally determines `τ`. `I` is a pre-treatment moderator.

Randomization identifies the causal contrast of `E` on `V` under the design assumptions. It does not make `I` a randomized cause.

## Linear implementation

A simple preregistered implementation is:

```text
V_{t+h}
=
α + βI_t + γE_t + δ(I_t×E_t) + λV_t + ε
```

Interpretation:

```text
β
→ association with ordinary outcome level / capability

γ
→ average causal effect of E

δ
→ effect modification by pre-treatment I
```

The especially discriminating pattern is:

```text
β ≈ 0
δ > 0
```

because it separates responsiveness from ordinary prognostic performance.

Do not call `δ` the causal effect of `I`.

## Scientific separation

Keep the following distinct:

```text
measurement
≠
causal effect
≠
hypothesis
```

and:

```text
causal heterogeneity
≠
longitudinal dynamics
≠
equilibrium
≠
stationary stochastic distribution
```

The minimal assay does not require a dynamical equilibrium claim.

## Measurement role

Measurement partly constitutes the identity of the scientific object.

`τ(i)` is not fully specified independently of the measurement structure used for `I` and `V`.

Pilot-0 measurement requirements:

```text
I
→ order structure
→ the proposition is invariant to strictly increasing reparameterizations

V
→ additive difference structure
→ additive CATE is invariant to positive affine transformations
```

See `MEASUREMENT_BOUNDARY.md`.

## Primary test

Prefer a direct monotonicity test at the level of the scientific proposition.

For prespecified ordered values or strata:

```text
i₁ > i₀
?
τ(i₁) > τ(i₀)
```

A derivative or linear coefficient can be used when the corresponding shape assumptions are justified.

## Null and falsifying outcomes

Scientifically meaningful outcomes include:

```text
τ increasing with I
→ support within scope

τ flat within adequate precision
→ no support / direct hit on the proposed ordering

τ decreasing with I
→ opposite-direction evidence

τ non-monotonic
→ failure of the global monotonicity claim, even if local positive regions exist
```

A null result is informative only when the design has adequate sensitivity over the relevant `I` range and outcome scale.

## Specificity extension

The minimal assay tests responsiveness, not discriminative responsiveness.

After a positive primary result, intervention quality can be varied:

```text
E⁺ = independently warranted corrective intervention
E⁰ = irrelevant / neutral intervention
E⁻ = misleading intervention
```

Estimate:

```text
τ⁺(i)
τ⁰(i)
τ⁻(i)
```

A stronger specificity test is:

```text
[τ⁺(i₁) - τ⁻(i₁)]
>
[τ⁺(i₀) - τ⁻(i₀)]
```

for `i₁ > i₀`.

Do not retroactively replace the historical Level-0 hypothesis with this stronger test.

## Optional longitudinal extension

Only if data warrant a dynamical question, remeasure `I` after intervention:

```text
T_h^(e)(i)
=
E[I_{t+h} | do(E_t=e), I_t=i]
```

This maps the `I` measurement space back into itself and can support a well-typed fixed-point question:

```text
i* = T_h^(e)(i*)
```

A contraction claim requires additional conditions such as:

```text
T_h^(e)([a,b]) ⊆ [a,b]
sup_i |T_h^(e)'(i)| < 1
```

These are optional historical extensions. They are not part of the active future-plasticity benchmark.

## Claim discipline

The assay does not establish that:

- `I` is intelligence;
- `I` causally produces responsiveness;
- `V` is viability, value, welfare, or utility;
- `I ∝ τ`;
- the top-level intelligence conjecture is true;
- a positive response identifies the mechanism of correction;
- one intervention, horizon, population, or outcome scale transports automatically to another.

This document remains part of Pilot-0 provenance and should not be used as the current repository research contract.

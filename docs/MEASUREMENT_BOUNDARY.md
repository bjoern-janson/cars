# Measurement Boundary for the CARS Assay

## Status

> **Historical Pilot-0 measurement specification.** This document specifies the transformation classes under which the Pilot-0 causal-response assay retained the same scientific identity. It is not the active repository-level empirical contract.

Current repository-level state:

- [`INTELLIGENCE_THEORY.md`](INTELLIGENCE_THEORY.md)
- [`CURRENT_RESEARCH_STATE.md`](CURRENT_RESEARCH_STATE.md)
- [`RESEARCH_CONTRACT.md`](RESEARCH_CONTRACT.md)

Protocol rule:

```text
Before testing invariance,
specify the admissible transformation class.
```

A disagreement under an inadmissible transformation can simply mean that the estimand changed. A disagreement under a licensed transformation is a genuine discrepancy that must be localized.

## Scientific proposition

The primitive Pilot-0 assay claim was:

```text
i₁ > i₀
⇒
τ(i₁) > τ(i₀)
```

with:

```text
τ(i)
=
E[V(e₁) - V(e₀) | I=i]
```

The proposition is ordering-based on the `I` side and difference-based on the `V` side.

## I-side measurement structure

The substantive hypothesis uses only the order of `I`.

For any strictly increasing transformation:

```text
i' = f(i)
```

we have:

```text
i₁ > i₀
⇔
i₁' > i₀'
```

Therefore the primitive ordering proposition is invariant to strictly increasing reparameterizations of `I`.

Where differentiability is justified and `f'(i) > 0`:

```text
∂τ'(i')/∂i'
=
[∂τ(i)/∂i] / f'(i)
```

so the derivative sign is preserved.

However, a linear specification need not remain linear after a nonlinear monotone transformation of `I`.

If:

```text
τ(i) = τ₀ + δi
```

and:

```text
i' = f(i)
```

then generally:

```text
τ'(i')
=
τ₀ + δ f^(-1)(i')
```

which need not be linear.

Therefore:

```text
hypothesis invariance
≠
estimator / linear-form invariance
```

## V-side measurement structure

The causal object uses subtraction:

```text
V(e₁) - V(e₀)
```

so its identity depends on a measurement scale on which additive differences are meaningful.

### Measurement Boundary Theorem

If two outcome representations are related by a positive affine transformation:

```text
V^(2) = aV^(1) + b
a > 0
```

then:

```text
τ^(2)(i) = a τ^(1)(i)
```

and for every `i₁ > i₀`:

```text
τ^(2)(i₁) - τ^(2)(i₀)
=
a[τ^(1)(i₁) - τ^(1)(i₀)]
```

Therefore:

```text
sign[τ^(2)(i₁) - τ^(2)(i₀)]
=
sign[τ^(1)(i₁) - τ^(1)(i₀)]
```

The zero/nonzero status and ordering of additive treatment-effect heterogeneity are preserved.

Under a linear moderation model:

```text
τ(i) = τ₀ + δi
```

this yields the corollary:

```text
δ^(2) = aδ^(1)
```

so the coefficient magnitude rescales while its sign is preserved.

## Nonlinear transformations

For a general strictly increasing nonlinear transformation:

```text
V' = g(V)
```

the additive causal contrast becomes:

```text
E[g(V(e₁)) - g(V(e₀)) | I=i]
```

which is generally a different causal estimand.

A constant treatment effect on one scale can become positive, negative, or non-monotonic heterogeneity on another monotone nonlinear scale.

Therefore:

```text
ordinal equivalence of V
is not sufficient
for additive-CATE invariance
```

## Asymmetry

Freeze the following distinction:

```text
I
→ ordering
→ strictly increasing transformations admissible

V
→ subtraction / additive difference
→ positive affine transformations admissible
```

Compactly:

```text
I requires order structure.
V requires difference structure.
```

This asymmetry is a property of the estimand, not a defect in the assay.

## Independent-instrument test

The strongest measurement test uses independently constructed outcome instruments rather than mathematical copies.

Suppose:

```text
M_V^A ← target
M_V^B ← target
```

with separate construction and calibration.

First establish on independent calibration data that the instruments are legitimately interval-equivalent within declared tolerance:

```text
V^B ≈ aV^A + b
a > 0
```

Freeze `a,b` before the treatment-effect analysis.

Then test whether the treatment-effect ordering is preserved.

Under a justified linear model, a secondary prediction is:

```text
δ_B ≈ aδ_A
```

The primary test remains at the scientific-proposition level:

```text
sign[τ_B(i₁)-τ_B(i₀)]
?
=
sign[τ_A(i₁)-τ_A(i₀)]
```

## Residual disagreement diagnostic

After freezing the affine link:

```text
r = V^B - (aV^A + b)
```

fit or test whether residual disagreement contains systematic moderator/treatment structure:

```text
r
~
I + E + I×E
```

A nonzero `I×E` term means the instruments disagree specifically about the heterogeneous treatment contrast, even if their overall correlation is high.

Thus:

```text
construct agreement
≠
measurement equivalence
≠
causal-estimand equivalence
```

## Falsification rule

A genuine measurement-form contradiction requires:

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

If those conditions hold, localize the failure across:

```text
measurement equivalence?
measurement error / saturation?
causal identification?
shape representation?
estimator?
implementation?
```

Only after localization should the substantive proposition be revised.

The protocol does not protect the historical hypothesis from contradiction. It specifies what would count as one.

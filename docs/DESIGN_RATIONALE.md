# Design Rationale

CARS is designed around a tension: systems must remain correctable without becoming rigid, novelty-seeking, or self-authorizing.

The repository now separates two roles that earlier work partially mixed:

```text
CARS
→ epistemic control protocol

ASSAY
→ minimal empirical test of heterogeneous causal responsiveness
```

The control protocol governs how evidence is handled. The assay produces evidence about a specific scientific proposition. Neither validates the other.

## 1. The empirical core should be smaller than the mechanism story

The motivating conjecture:

```text
I ∝ C_improve
```

was useful because it pointed toward correction capacity rather than current capability.

But it also carried semantic commitments about `I`, improvement, viability, and proportionality.

The current assay removes those commitments and asks only:

```text
τ(i)
=
E[V(e₁) - V(e₀) | I=i]
```

and:

```text
i₁ > i₀
⇒
τ(i₁) > τ(i₀)
```

The benchmark supplies the operational referents. Interpretation comes after evidence.

## 2. Scientific object, representation, and estimator are different layers

Freeze:

```text
SCIENTIFIC PROPOSITION
τ(i₁) > τ(i₀) for i₁ > i₀

        ↓ represented by

SHAPE
∂τ(i)/∂i > 0
or
τ(i) = τ₀ + δi

        ↓ instantiated on

MEASUREMENT STRUCTURE
I: order-preserving
V: difference-preserving

        ↓ recovered by

ESTIMATOR
```

A failed linear interaction can reflect a bad linear representation without falsifying monotonicity.

An invalid measurement structure is different: because `τ` is defined using measured differences in `V`, changing the measurement structure can change the identity of the causal object itself.

## 3. Measurement partly constitutes the scientific object

The current assay is asymmetric.

`I` enters through ordering:

```text
i₁ > i₀
```

so strictly increasing transformations preserve the substantive ordering.

`V` enters through subtraction:

```text
V(e₁) - V(e₀)
```

so additive treatment-effect invariance requires a transformation class that preserves meaningful differences.

For the current assay:

```text
V' = aV + b
a > 0
```

preserves:

```text
τ'(i) = aτ(i)
```

General nonlinear monotone transformations can redefine the additive CATE.

This yields the protocol rule:

> **Before testing invariance, specify the admissible transformation class.**

See `MEASUREMENT_BOUNDARY.md`.

## 4. Localize before revising

A contradiction does not identify its cause.

When assay results disagree, inspect the shallowest plausible failure locus first:

```text
measurement / saturation?
causal identification?
scientific-object identity?
shape representation?
estimator?
implementation?
substantive proposition?
```

Do not revise the highest-level claim because a lower-level representation failed.

## 5. Possibility is cheap; authority is expensive

A candidate explanation for a failed assay is not evidence that the explanation is correct.

Likewise:

```text
possible transformation
≠
admissible transformation
```

and:

```text
candidate replacement
≠
authorized replacement
```

The protocol should keep multiple explanations available until discriminating evidence identifies one.

## 6. Scope leakage is a common failure

A positive treatment-effect ordering under one:

```text
E, h, domain, population, M_I, M_V
```

does not establish the same ordering elsewhere.

Transport is an empirical extension, not a default entitlement.

## 7. Repeated evidence can share one failure mode

Many agreeing instruments or models can share the same measurement artifact, benchmark geometry, judge bias, or intervention confound.

High correlation between two outcome instruments does not establish that they preserve the same causal contrast.

This motivates independent-instrument tests and residual `I×E` diagnostics.

## 8. Minimal revision is an empirical discipline

The nonlinear-measurement red-team result is the canonical example.

The stronger claim:

```text
arbitrary monotone outcome transformations preserve moderation sign
```

failed.

The minimal revision was not to abandon the substantive proposition. It was to restrict the measurement invariance claim to the class that mathematically preserves additive differences:

```text
positive affine transformations
```

That is the intended CARS correction pattern:

```text
claim
→ counterexample
→ failure localization
→ minimal sufficient revision
```

## 9. Responsiveness is not discriminative responsiveness

The minimal assay can detect generic susceptibility to intervention.

A stronger correction-capacity interpretation requires separate intervention-status conditions such as:

```text
E⁺ = warranted correction
E⁰ = neutral / irrelevant
E⁻ = misleading
```

A system that responds strongly to all three is different from one whose response tracks the independently warranted status of the intervention.

Therefore:

```text
responsiveness
≠
discriminative responsiveness
```

The specificity test is a later empirical layer, not part of the minimal headline claim.

## 10. Current capability is not causal responsiveness

A pre-treatment variable can be strongly prognostic of ordinary outcome level while having no treatment-modifying value.

Under a linear implementation:

```text
V_{t+h}
=
α + βI_t + γE_t + δ(I_t×E_t) + λV_t + ε
```

keep distinct:

```text
β
→ ordinary prognostic association

δ
→ treatment-effect modification
```

The especially informative case is:

```text
β ≈ 0
δ > 0
```

because it separates responsiveness from ordinary capability.

## 11. Headroom is an assay threat, not a semantic issue

A bounded outcome can manufacture apparent treatment-effect heterogeneity even when the latent treatment effect is constant.

Therefore the benchmark must explicitly attack:

- ceiling/floor effects;
- recoverable-headroom differences;
- nonlinear response scales;
- task difficulty mismatches.

The aim is to make false positive moderation easy to generate during development so the assay learns to reject it.

## 12. Randomization protects the treatment contrast, not the meaning of I

Randomizing `E` identifies the causal effect of the intervention under the design assumptions.

It does not establish:

```text
I → τ
```

as a causal relation.

`I` is a pre-treatment moderator whose value may predict heterogeneity for reasons not yet mechanistically identified.

Effect modification by `I` is therefore not the same as a causal effect of `I`.

## 13. Departure from adoption remains central

The old authority firewall remains fully active:

```text
A_leave ↛ A_adopt
```

A failed representation, measurement claim, or estimator does not authorize the first replacement that happens to be available.

The scientifically valid state can be:

```text
incumbent claim insufficient
+
replacement not yet earned
=
remain unresolved
```

## 14. Mechanism machinery is downstream of the assay

Earlier concepts such as residual mapping, candidate generation, validation independence, adoption, transfer, and inheritance remain useful.

Their role has changed.

```text
old role:
parts of a candidate master architecture

current role:
diagnostic mechanism hypotheses and benchmark dimensions
```

Reopen them when an empirical result requires explanation or a stronger layer is being tested.

Do not put them back into the headline assay merely because they are conceptually available.

## 15. Dynamics and equilibrium are separate scientific questions

The responsiveness assay asks whether `I` orders heterogeneous causal response.

A longitudinal transition question requires a separate observable:

```text
T_h^(e)(i)
=
E[I_{t+h} | do(E_t=e), I_t=i]
```

A fixed point:

```text
i* = T_h^(e)(i*)
```

and a contraction condition are stronger claims about a different object.

Keep:

```text
causal heterogeneity
≠
longitudinal dynamics
≠
equilibrium
≠
stationary stochastic distribution
```

## 16. CARS itself remains testable

CARS is the control protocol around the assay, but it can also be studied as a reasoning intervention:

```text
reasoning without CARS
vs
reasoning with CARS
```

on failure localization, calibration, transfer, regression, decision quality, and cost.

That is a separate experiment from the heterogeneous-responsiveness assay.

## 17. Historical catalyst and recursive architecture remain lineage

The August 8 catalyst and recursive-correction documents are retained for provenance and optional future testing.

They are not the current empirical frontier.

Their concepts remain useful when they help construct discriminating attacks or explain observed response geometry.

## 18. Stopping is part of the method

The current scientific proposition is testable enough to attack.

Therefore the next high-information move is not more notation.

```text
simple experiment first
→ complex explanation only if earned
```

The governing research posture is:

> Build an assay that tries hard to make the target ordering appear when the true answer is zero. If it survives, the positive result becomes more interesting.

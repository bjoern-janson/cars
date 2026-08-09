# CARS Assay Red-Team Protocol

## Objective

Stop trying to prove the assay and try to break it.

Construct worlds in which the primitive hypothesis is false or unsupported, while the benchmark is tempted to report:

```text
i₁ > i₀
⇒
τ(i₁) > τ(i₀)
```

The red-team target is not the CARS control protocol. It is the empirical assay and the measurement/estimation chain that instantiates it.

## Core principle

```text
stronger claim
→ counterexample
→ failure localization
→ minimal sufficient revision
```

A benchmark should be rewarded for rejecting manufactured positive results.

## Attack 1 — constant-effect world

Construct:

```text
τ(i) = constant
```

while allowing `I` to correlate strongly with baseline outcome or capability.

Expected result:

```text
no systematic treatment-effect ordering by I
```

Under a correctly specified linear randomized analysis:

```text
δ ≈ 0
```

If the benchmark reports positive moderation, investigate model misspecification, leakage, treatment imbalance, measurement geometry, or estimator failure.

## Attack 2 — ceiling / floor world

Keep the latent treatment effect constant while observing a bounded outcome:

```text
V_obs = clip(V_latent, lower, upper)
```

This can create apparent treatment-effect heterogeneity because units have unequal observable headroom.

Required controls include at least one of:

- adequate dynamic range;
- explicit modeling of the bounded scale;
- a preregistered outcome transformation whose causal estimand is justified;
- matching/stratification on recoverable headroom where appropriate;
- reporting both latent/simulation truth and observed-scale estimands in synthetic validation.

Do not treat headroom as a cosmetic regression covariate. It can change the sign of the observed moderation.

## Attack 3 — nonlinear outcome remeasurement

Start with a latent outcome `V*` and constant causal effect, then measure:

```text
V = g(V*)
```

for monotone nonlinear `g`, such as log-like or convex transforms.

Expected result:

```text
additive CATE may change shape or sign
```

This is not automatically a benchmark failure because nonlinear monotone transformations generally redefine the additive causal estimand.

Use this attack to verify that the implementation distinguishes:

```text
inadmissible / estimand-changing transformation
≠
genuine failure of licensed invariance
```

## Attack 4 — baseline structure / confounding

Generate a latent variable that strongly drives both `I` and baseline outcome:

```text
Z → I
Z → V_t
```

while keeping the true randomized treatment effect constant.

Under genuine randomization, the assay should not manufacture treatment-effect heterogeneity merely because `I` is prognostic.

Then deliberately break randomization or treatment assignment to verify that confounding can create false heterogeneity and that the benchmark detects the identification failure.

Keep explicit:

```text
prognostic I
≠
predictive I
```

and:

```text
E randomized
↛
I randomized
```

## Attack 5 — generic plasticity

Use at least three intervention statuses established independently of the tested system:

```text
E⁺ = warranted correction
E⁰ = irrelevant / neutral input
E⁻ = misleading input
```

Construct a system for which higher `I` amplifies response to all three.

The minimal assay may pass under `E⁺`:

```text
τ⁺(i₁) > τ⁺(i₀)
```

while specificity fails.

Therefore keep separate:

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

Do not promote generic intervention susceptibility into discriminative correction capacity.

## Attack 6 — affine positive control

Take the same observed outcome and construct:

```text
V^B = aV^A + b
a > 0
```

The scientific ordering must be preserved exactly up to sampling/estimation uncertainty.

Under a linear moderation model:

```text
δ_B = aδ_A
```

Failure here is an implementation, estimation, or protocol error.

## Attack 7 — independent interval instruments

Construct two outcome measurements independently:

```text
M_V^A ← target
M_V^B ← target
```

Do not define one as a mathematical transform of the other.

On independent calibration data, establish whether they are legitimately interval-equivalent:

```text
V^B ≈ aV^A + b
```

Freeze the calibration before the randomized treatment analysis.

Then compare the scientific ordering:

```text
sign[τ_B(i₁)-τ_B(i₀)]
?
=
sign[τ_A(i₁)-τ_A(i₀)]
```

If the licensed equivalence holds but the causal ordering reverses with adequate precision, a genuine discrepancy exists and must be localized.

## Attack 8 — high-correlation causal disagreement

Create or identify instruments with high ordinary agreement but treatment/moderator-specific disagreement.

After freezing:

```text
V^B = aV^A + b + r
```

test:

```text
r
~
I + E + I×E
```

The key attack is:

```text
corr(V^A,V^B) high
+
I×E residual structure nonzero
```

This demonstrates why convergent correlation alone is not evidence of causal-estimand equivalence.

## Attack 9 — nonlinear I reparameterization

Replace:

```text
I' = f(I)
```

for strictly increasing nonlinear `f`.

The primitive ordering hypothesis must retain the same truth value.

However a linear interaction coefficient need not be stable because linearity is parameterization-dependent.

This attack verifies that the benchmark does not confuse:

```text
scientific proposition
≠
shape representation
≠
parametric estimator
```

## Attack 10 — sensitivity / null-result attack

Generate small positive effects near the assay's resolution limit.

Determine whether the design can distinguish:

```text
true zero
```

from:

```text
small positive effect
```

before interpreting a null result as a substantive failure.

Predeclare the smallest effect or ordering difference the experiment is intended to resolve.

## Falsification ladder

```text
Does the primary ordering hold?
        │
   ┌────┴────┐
   │         │
  NO        YES
   │         │
localize   attack measurement
and report      │
            ┌───┴───────────┐
            │               │
      measurement-      survives licensed
      dependent         transformations
            │               │
           STOP        test E specificity
                            │
                       test horizon
                            │
                       test transport
                            │
                       test independent
                       measurement
```

`STOP` means do not promote the stronger claim. It does not mean hide or discard the result.

## Failure localization order

When a red-team contradiction appears, check the shallowest plausible locus first:

```text
1. intervention assignment / causal identification
2. measurement equivalence / saturation / error
3. scientific-object identity
4. shape representation
5. estimator / statistical specification
6. implementation
7. substantive proposition
```

The ordering is diagnostic, not metaphysical. Stop escalation once independent evidence identifies the failure.

## Required result classes

Report each attack as:

- **survived** — expected invariant or null behavior recovered;
- **failed** — benchmark produced an unauthorized conclusion;
- **estimand changed** — transformation was not licensed to preserve the same scientific object;
- **inconclusive** — insufficient power, calibration, or identification.

A red-team protocol succeeds by discovering boundaries, not by maximizing the number of green checks.

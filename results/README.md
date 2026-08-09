# Results

## Pilot 0 terminal status

Pilot 0 is now **closed** under an epistemic stopping rule. The repository contains scoped positive causal results about representation-dependent transition behavior, but these do **not** establish a global correction construct, psychological mechanism, transport invariance, or general intelligence claim.

Terminal record:

- [`PILOT0_TERMINAL_RECORD.md`](PILOT0_TERMINAL_RECORD.md)

The original moderation hypothesis was **not supported**. The later representation-localization program earned endpoint-specific causal authority, and the R1 replication/transport branch established a small replicated positive prior-state-encoding effect on `T_instability` whose common 95% interval lies entirely inside the inherited `±0.05` practical region.

Keep the stopping rule explicit:

```text
STOP
≠ truth
≠ completeness
≠ certainty

STOP
= no presently justified escalation
```

No A8, R2, or further `T_instability` decomposition is currently earned. A future experiment requires a genuinely new scientific question and a new pre-outcome contract.

Future result packages should record enough information to reconstruct:

```text
what scientific object was tested
what measurement structure instantiated it
how treatment was assigned
what estimator represented it
what transformations were licensed
what claim the result actually supports
```

## Result surfaces

Keep distinct:

```text
prompt result
≠
causal-responsiveness result
≠
measurement-invariance result
≠
specificity result
≠
longitudinal/equilibrium result
≠
historical catalyst/architecture result
```

A positive result on one surface does not automatically promote claims on another.

## Primary assay result package

For:

```text
τ(i)
=
E[V(e₁)-V(e₀) | I=i]
```

record:

- exact operational definition of `I` / `M_I`;
- exact intervention levels `e₀,e₁`;
- randomization/assignment procedure;
- exact operational definition of `V` / `M_V`;
- horizon `h`;
- population/model family;
- treatment counts across relevant `I` support;
- baseline outcome or headroom variables where used;
- attrition/missingness;
- estimator and version/code;
- whether the primary test was ordered strata, monotonicity, derivative, or linear interaction;
- uncertainty intervals;
- smallest effect/order difference the design was intended to resolve;
- ceiling/floor exposure;
- protocol deviations;
- raw or auditable outputs where licensing/privacy permits.

Report the scientific proposition before the parametric representation.

For example:

```text
τ(i₁) - τ(i₀)
```

before or alongside:

```text
δ
```

when a linear model is used.

## Measurement / invariance result package

Before reporting an invariance result, record the transformation class that was licensed to preserve the object.

### I-side

For a strictly increasing reparameterization:

```text
I' = f(I)
```

record whether the primitive ordering of `τ` across `I` was preserved.

Do not require a linear coefficient to remain numerically invariant under nonlinear `f`.

### V-side

For a positive affine transformation:

```text
V' = aV + b
a > 0
```

record whether:

```text
τ'(i) = aτ(i)
```

within estimation uncertainty and whether treatment-effect ordering is preserved.

For nonlinear monotone outcome transforms, label the run as a changed/additional estimand unless a separate measurement model licenses equivalence.

## Independent-instrument result package

For independently constructed `M_V^A` and `M_V^B`, report:

- instrument construction process;
- calibration data source;
- evidence that calibration data were independent of the treatment-effect analysis;
- fitted/frozen affine link `V^B ≈ aV^A+b`;
- prespecified tolerance for interval equivalence;
- calibration uncertainty;
- treatment-effect ordering under both instruments;
- residual diagnostic:

```text
r = V^B - (aV^A+b)
r ~ I + E + I×E
```

- ordinary correlation only as secondary information.

Do not describe high correlation alone as measurement equivalence.

## Red-team result package

For every adversarial attack in `docs/RED_TEAM_PROTOCOL.md`, report one of:

```text
survived
failed
estimand changed
inconclusive
```

Record the synthetic/known truth where applicable.

A useful red-team report should make false positives visible rather than optimize for a green dashboard.

## Specificity result package

For:

```text
E⁺
E⁰
E⁻
```

record how intervention status was established independently of the tested system.

Report separately:

```text
τ⁺(i)
τ⁰(i)
τ⁻(i)
```

and the specificity contrast if used.

Do not promote responsiveness under `E⁺` into discriminative correction capacity without these comparisons.

## Horizon / transport result package

Treat each horizon as a separate estimand unless pooling is preregistered and justified.

Record each boundary crossed:

- intervention;
- domain;
- population/model family;
- moderator instrument;
- outcome instrument;
- benchmark generator.

A result that survives one boundary gains only the corresponding scoped transport authority.

## Prompt-level result package

For CARS prompt/control-protocol evaluation, record:

- exact CARS prompt file/hash;
- generic control prompt/hash;
- baseline condition;
- model/version/date;
- task source/authorship;
- per-dimension scores from `eval/SCORING.md`;
- substantive task outcome;
- cost metrics;
- exclusions/protocol deviations.

Prompt efficacy remains independent of the causal-responsiveness assay.

## Optional longitudinal / equilibrium result package

If later work estimates:

```text
T_h^(e)(i)
=
E[I_{t+h} | do(E_t=e), I_t=i]
```

record:

- exact repeated `I` measurement procedure;
- intervention regime `e`;
- horizon;
- evidence for time-homogeneous/iterable dynamics if repeated-map claims are made;
- fixed-point estimate and uncertainty;
- self-map/domain conditions;
- contraction/stability diagnostics if claimed.

Do not infer equilibrium from a positive responsiveness assay.

## Historical catalyst / architecture result package

If the August 8 catalyst or recursive architecture is tested, retain the historical reporting requirements and dedicated scoring surfaces.

Do not silently merge those results with the current assay evidence.

## Result classification

Classify each result as one of:

- **positive within scope**;
- **negative/null**;
- **mixed tradeoff**;
- **estimand changed**;
- **invalid/inconclusive**.

Invalid or changed-estimand runs are not automatically evidence for or against the primitive proposition.

## Genuine contradiction reporting

For a claimed measurement-form contradiction, state whether all of the following were satisfied:

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

If yes, document the localization sequence and explain why lower-level failure loci were ruled out.

## Claim discipline

A positive result should state exactly what gained authority and within what scope.

Do not promote:

```text
positive interaction
→ I is intelligence
→ mechanism understood
→ discriminative correction capacity
→ cross-domain transport
→ equilibrium
→ theory validated
```

without separate evidence for each transition.

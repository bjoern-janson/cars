# Evaluation Threat Model

CARS can appear successful for reasons unrelated to the scientific object under test. This document covers the current causal-responsiveness assay, measurement/invariance testing, CARS prompt evaluation, and historical research surfaces.

## Core threat: scientific object drift

The same notation can hide a different empirical object if the measurement structure changes.

For the current assay:

```text
τ(i)
=
E[V(e₁)-V(e₀) | I=i]
```

measurement partly constitutes the identity of `τ`.

**Control:** specify the admissible transformation class before testing invariance. Treat non-licensed transformations as potentially different estimands rather than automatic robustness failures.

## Ceiling / floor artifacts

Bounded outcome scales can create apparent treatment-effect heterogeneity when units differ in available observable headroom.

A constant latent treatment effect can become strongly positive or negative on a clipped observed scale.

**Control:** dynamic-range analysis, headroom diagnostics, bounded-scale modeling, prespecified measurement choice, and synthetic worlds with known constant latent effects.

## Nonlinear outcome remeasurement

A strictly increasing nonlinear transformation can change the sign or shape of additive treatment-effect heterogeneity.

**Control:** preserve the measurement boundary:

```text
V' = aV+b, a>0
→ licensed affine-equivalent transformation

general nonlinear monotone g(V)
→ generally a different additive estimand
```

Do not claim ordinal invariance for an additive CATE.

## Moderator reparameterization / linear-model confusion

A strictly increasing nonlinear transformation of `I` preserves the primitive ordering hypothesis but may destroy a linear `τ(i)=τ₀+δi` representation.

**Control:** test monotonicity or ordered CATE contrasts directly. Treat `δ` as a representation, not the scientific object.

## Prognostic/predictive conflation

`I` may strongly predict baseline or future outcome level without modifying the causal treatment effect.

**Control:** randomized treatment assignment, constant-effect adversarial worlds, explicit separation of ordinary prognostic association from `I×E` moderation.

Keep:

```text
β ≠ 0
↛
δ ≠ 0
```

## Treatment confounding

If treatment is not genuinely randomized or otherwise identified, baseline structure can manufacture apparent heterogeneous causal response.

**Control:** randomization where feasible, assignment audits, positivity checks, attrition analysis, and deliberately confounded negative-control worlds.

## Headroom mistaken for responsiveness

Higher or lower `I` groups can differ in recoverable deficit, task difficulty, saturation, or baseline state.

**Control:** measure baseline outcome or an appropriate analogue, inspect response range, use matched/headroom-aware designs where scientifically justified, and avoid interpreting raw treatment-effect differences as intrinsic responsiveness without these checks.

## Generic plasticity mistaken for discriminative correction

A system may respond more strongly to any intervention as `I` rises.

**Control:** independently establish intervention status and compare:

```text
E⁺ warranted
E⁰ neutral
E⁻ misleading
```

Keep responsiveness and specificity as separate hypotheses.

## Intervention-status circularity

If the tested system itself determines which intervention counts as warranted, the specificity test can self-validate.

**Control:** establish `E⁺/E⁰/E⁻` using criteria independent of the tested system and independent of the response used to score it.

## Measurement correlation mistaken for equivalence

Two instruments can correlate highly while disagreeing on the exact treatment/moderator contrast.

**Control:** independent interval-equivalence calibration and residual diagnostics:

```text
r = V^B - (aV^A+b)
r ~ I + E + I×E
```

A nonzero residual `I×E` term is a direct warning that the instruments disagree where the assay lives.

## Calibration leakage

If the affine link between instruments is tuned using the same treatment-effect data later used to test invariance, measurement equivalence can be manufactured post hoc.

**Control:** estimate and freeze calibration on independent data before treatment-effect analysis.

## Shape-model misspecification

A nonlinear monotonic `τ(i)` can be misrepresented by a linear interaction coefficient.

**Control:** inspect nonparametric or flexible CATE shape, preregister the shape test, and do not interpret `δ≈0` as monotonicity failure when the linear representation is inadequate.

## Insufficient power / restricted moderator range

A true positive ordering can be hidden by weak treatment contrast, measurement noise, narrow `I` support, or small sample size.

**Control:** sensitivity analysis, prespecified smallest effect of interest, uncertainty intervals, and explicit support reporting.

## Multiple-horizon fishing

Testing many horizons and reporting only the positive one can manufacture a persistence narrative.

**Control:** preregister horizons or multiplicity handling. Treat each `h` as part of the estimand.

## Transport overreach

A result under one intervention, population, domain, or measurement system may not hold elsewhere.

**Control:** transport one boundary at a time where feasible and report exact scope.

## Semantic overinterpretation of I/E/V

Models and researchers may infer familiar meanings from notation—`I=information/intelligence`, `V=value`, `E=environment/evidence`—that are not licensed by the assay definition.

**Control:** define operational referents in the benchmark and keep semantic interpretation downstream of evidence.

## Hypothesis/theorem collapse

A model can recognize the CATE structure and then incorrectly infer that:

```text
∂τ(i)/∂i > 0
```

follows from the definition.

**Control:** include zero-prior-context reasoning checks where the only correct answer is that monotonicity is an empirical/model-specific question.

## Prompt-level threats

### Prompt-length advantage

A longer CARS intervention may simply induce more deliberation.

**Control:** generic careful-reasoning baselines and cost accounting.

### Vocabulary leakage

Tasks using CARS terminology may reward protocol recognition rather than better reasoning.

**Control:** held-out language and behavior-based scoring.

### Judge preference

Structured caution can be preferred stylistically without substantive improvement.

**Control:** blinded/outcome-based scoring, transfer probes, penalties for unnecessary intervention.

### Excessive conservatism

CARS may reduce false updates by failing to update when evidence is sufficient.

**Control:** matched true/false contradiction cases and missed-correction metrics.

### Unresolved-state abuse

Permission to remain unresolved can become an escape hatch.

**Control:** cases where evidence clearly licenses a determinate answer.

### False representation escalation

Difficult cases may be mislabeled as representation failures.

**Control:** matched shallow-repair worlds and explicit over-escalation scoring.

## Historical catalyst threats

Historical catalyst tests remain vulnerable to:

- semantic collision;
- syntactic recovery mistaken for semantic recovery;
- legend/rubric leakage;
- equation/prose confounding;
- decoding/execution conflation.

Use `eval/CATALYST_SCORING.md` if those experiments are reactivated.

These are no longer the current empirical frontier.

## Historical recursive-architecture threats

Historical recursive-architecture tests remain vulnerable to:

- residual-mapping error;
- candidate-generation blind spots;
- validator tuning after selection;
- adaptive holdout reuse;
- recursive lineage overfitting;
- metric gaming;
- global-average dilution;
- arbitrary regression tolerances;
- invalid self-certification.

Use `eval/ARCHITECTURE_SCORING.md` if those experiments are reactivated.

## Falsification target

The current adversarial objective is:

> **Construct conditions under which the assay reports that higher `I` orders larger causal responsiveness even though the true target effect is flat, opposite, or undefined under the claimed measurement equivalence.**

The assay should fail closed: when measurement identity, causal identification, or estimator adequacy is unresolved, report the run as changed-estimand or inconclusive rather than promoting a positive causal claim.

## Localization rule

When a contradiction appears, inspect:

```text
1. intervention assignment / causal identification
2. measurement equivalence / saturation / error
3. scientific-object identity
4. shape representation
5. estimator / statistical specification
6. implementation
7. substantive proposition
```

Do not let the diagnostic ladder become a shield. If a licensed transformation, reliable measurement, identified causal contrast, adequate estimator, and opposite ordering all survive scrutiny, the contradiction reaches the scientific proposition.

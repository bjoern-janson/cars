# CARS Failure Model

This document defines diagnostic failure classes used by the CARS control protocol and by empirical benchmarks. The assay-specific examples below are retained from the historical Pilot-0 causal-response program; they are not the repository's current top-level scientific object. These categories are not an ontology of all reasoning or measurement errors.

Current repository-level state:

- [`INTELLIGENCE_THEORY.md`](INTELLIGENCE_THEORY.md)
- [`CURRENT_RESEARCH_STATE.md`](CURRENT_RESEARCH_STATE.md)
- [`RESEARCH_CONTRACT.md`](RESEARCH_CONTRACT.md)

The governing rule is:

```text
failure does not identify its cause
```

When a contradiction appears, localize the shallowest sufficient failure before revising higher-level structure.

# Assay / benchmark failure layers

## 1. Causal-identification failure

The intervention contrast does not identify the intended causal effect because treatment assignment, positivity, attrition, interference, missingness, or other design assumptions fail.

**Corrective pressure:** repair the intervention design or downgrade the causal claim before interpreting heterogeneity.

## 2. Measurement failure

The measured variables are noisy, saturated, unreliable, or generated through an invalid measurement procedure.

Historical Pilot-0 examples include `I` and `V` measurement. General examples include:

- ceiling/floor compression;
- differential measurement error;
- treatment-dependent measurement distortion;
- insufficient reliability;
- incompatible outcome instruments.

**Corrective pressure:** improve or revalidate the measurement procedure; do not immediately revise the substantive hypothesis.

## 3. Measurement-identity failure

A transformation or alternate instrument changes the scientific object rather than merely reexpressing it.

For the historical Pilot-0 additive CATE:

```text
V' = aV+b, a>0
```

is licensed to preserve additive-effect ordering, while a general nonlinear monotone `g(V)` is not.

**Corrective pressure:** determine whether the compared measurements belong to the same admissible transformation class before calling the disagreement a contradiction.

## 4. Shape-representation failure

The scientific proposition may be correct while the chosen representation is wrong.

Historical Pilot-0 example:

```text
τ(i)
```

is monotone increasing but nonlinear, while the analysis assumes:

```text
τ(i) = τ₀ + δi.
```

A near-zero linear `δ` can therefore be a bad shape representation rather than a failed monotonicity claim.

**Corrective pressure:** test the ordering or shape more directly.

## 5. Estimator / predictor failure

The chosen estimator or predictor is biased, unstable, misspecified, underpowered, poorly regularized, or unable to recover the intended object under known-truth controls.

**Corrective pressure:** strengthen or validate the estimator before revising the scientific proposition.

Pilot 1 / ID1 demonstrated this distinction directly: an apparent A/N structural gap under weaker predictors largely disappeared under a stronger generic identifier and failed directional replication.

## 6. Implementation failure

The code, data pipeline, randomization, scoring, calibration, concealment ordering, or analysis differs from the declared protocol.

**Corrective pressure:** repair the implementation without changing the scientific contract and rerun.

## 7. Scientific-proposition failure

After shallower explanations—measurement identity, causal identification where relevant, shape representation, estimator adequacy, implementation, and finite-sample variation—have survived scrutiny, the data contradict the frozen scientific proposition.

Historical Pilot-0 example:

```text
i₁ > i₀
```

does not imply:

```text
τ(i₁) > τ(i₀).
```

For the active future-plasticity benchmark, failure is gate-local rather than theory-global. Example:

```text
G0 fails
→ no forecastability claim at this measurement/sample resolution
↛ intelligence theory falsified
```

# CARS reasoning failure classes

## Observation / measurement failure

Available evidence is noisy, corrupted, incomplete, mismeasured, or produced by an unreliable observation process.

**Corrective pressure:** improve measurement, inspect source quality, seek independent observations.

## Inference failure

The evidence is adequate but the conclusion does not follow, or relevant alternatives were ignored.

**Corrective pressure:** revise inference while preserving unaffected observation/model structure.

## Model failure

The current explanatory or predictive model is wrong or incomplete even though the task-relevant distinction is available.

**Corrective pressure:** revise within the current representational vocabulary before escalating.

## Representation / interface failure

The current interface or vocabulary collapses a task-relevant distinction, making the needed correction unavailable inside the current representation.

**Corrective pressure:** investigate representation adequacy only after plausible within-representation explanations have been discriminated.

A representation can be highly detailed while remaining non-identifying.

## Mechanism uncertainty

A result is observed, but the causal or generative mechanism is not identified.

**Corrective pressure:** do not convert result validity into causal or mechanistic authority.

## Missing-information state

Available evidence is insufficient to choose among plausible explanations.

**Corrective pressure:** remain unresolved or seek a discriminating observation/intervention.

## Decision failure

Beliefs may be adequately calibrated while action selection ignores consequences, reversibility, downside, opportunity cost, or information value.

**Corrective pressure:** separate epistemic confidence from decision policy.

# Historical recursive-architecture diagnostics

Earlier CARS work introduced additional diagnostic loci:

- residual-mapping failure;
- candidate-generation failure;
- validation-procedure failure;
- correction-procedure failure.

These remain useful mechanism hypotheses and historical architecture categories. They are not required by the current repository-level theory or active future-plasticity benchmark.

If reactivated, preserve the old discipline:

```text
ρ_t = Φ_t(E_t)
```

is a provisional residual representation, not hidden truth.

Likewise:

```text
A_leave ↛ A_adopt
```

applies to proposed replacements at every layer.

# Cross-cutting pathologies

## Prognostic/predictive collapse

A variable that predicts baseline outcome is treated as though it necessarily predicts treatment-effect heterogeneity or future adaptation.

## Headroom artifact

Differential observable range is interpreted as intrinsic differential responsiveness.

## Estimand drift

A changed measurement, transformation, benchmark, or task family is described as the same scientific object without justification.

## Parametric capture

A convenient coefficient or latent score becomes the scientific object even though the proposition is more general.

## Authority laundering

Evidence for one property is silently reused as evidence for another.

Examples:

```text
high correlation
↛ measurement equivalence
```

```text
positive δ
↛ I is intelligence
```

```text
forecastability
↛ causal mechanism
```

```text
future trainability difference
↛ viability gain
```

```text
viability gain
↛ evidence-mediated intelligence
```

## Premature retention

The system preserves an incumbent despite sufficient contrary evidence.

## Premature replacement

The system treats failure of an incumbent as validation of a successor.

## Over-escalation

A lower-level measurement, estimator, inference, implementation, or finite-sample error triggers unnecessary theory/representation revision.

## Under-escalation

Repeated failures are patched at a shallow layer despite evidence that the scientific object or representation itself is inadequate.

## Common-mode validation

Repeated confirmation is treated as independent despite shared measurement channels, assumptions, benchmark generators, task families, or selection information.

## Narrative-only correction

The explanation changes while future reasoning, action, or measured behavior does not.

## Benchmark lineage overfitting

Repeated revisions adapt to previously exposed evaluation cases, which are then incorrectly described as fresh holdout evidence.

## Intellectual escalation after closure

A closed discrepancy is used to justify a longer horizon, richer grammar, more complex mechanism, additional replication, or new construct whose primary purpose is to recover the vanished effect.

**Corrective pressure:** require an independently motivated scientific question and fresh pre-outcome contract.

# Evaluation principle

Failure localization is itself testable.

The benchmark should not reward the model merely for naming a category. The relevant question is whether localization changes what is measured, tested, revised, or left unresolved in a way that survives independent follow-up.

A useful red-team architecture does not protect a scientific proposition from contradiction. It specifies what lower-level failures must be ruled out before a contradiction reaches it.

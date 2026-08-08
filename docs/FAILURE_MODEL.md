# CARS Failure Model

This document defines failure classes used for evaluation design. They are diagnostic categories, not an ontology of all reasoning errors.

The current architecture treats even the diagnostic representation as corrigible. A residual representation

```text
ρ_t = Φ_t(E_t)
```

is therefore a hypothesis about the encountered limitation, not the limitation itself.

## Observation / measurement failure

The available evidence is noisy, corrupted, incomplete, mismeasured, or generated through an unreliable observation process.

**Corrective pressure:** improve measurement, inspect source quality, seek independent observations.

## Inference failure

The evidence is adequate but the conclusion does not follow, or relevant alternatives were ignored.

**Corrective pressure:** revise inference while preserving the observation layer.

## Model failure

The current explanatory or predictive model is wrong or incomplete even though the relevant distinction is available to the system.

**Corrective pressure:** revise model structure or parameters within the current representational vocabulary.

## Representation / interface failure

The current interface or vocabulary collapses a task-relevant distinction, making the needed correction unavailable within the existing representation.

**Corrective pressure:** investigate representation adequacy; only then generate or select candidate distinctions.

A representation can be detailed yet non-identifying. More resolution is not automatically the corrective move; a different partition may be required.

## Residual-mapping failure

The procedure that maps evidence into the current residual representation is itself inadequate:

```text
Φ_t(E_t) = ρ_t,
ρ_t ≠ ρ*
```

This can cause the system to correct the wrong object, merge distinct failure classes, or split one mechanism into misleading categories.

**Corrective pressure:** challenge the residual mapping using alternate partitions, discriminating interventions, or withheld ground truth. Do not treat the current diagnostic partition as self-validating.

## Candidate-generation failure

The limitation is adequately represented, but the candidate generator fails to propose a viable discriminating revision or proposes only variants that share the same blind spot.

**Corrective pressure:** revise candidate generation or expand the candidate space without granting generated alternatives automatic authority.

## Validation-procedure failure

The validation procedure is incapable of discriminating viable from non-viable successors, or is contaminated by information that influenced candidate generation or selection.

**Corrective pressure:** revise validation design and revalidate using evidence insulated from the selection-information boundary.

## Mechanism uncertainty

The result is observed, but the causal or generative mechanism is not identified.

**Corrective pressure:** do not convert result validity into causal authority.

## Missing-information state

Available evidence is insufficient to choose among plausible explanations.

**Corrective pressure:** remain unresolved or seek discriminating evidence.

## Decision failure

Beliefs may be adequate, but action selection ignores consequences, downside, reversibility, or information value.

**Corrective pressure:** separate epistemic confidence from decision policy.

## Correction-procedure failure

The current process for detecting, localizing, generating, testing, or retaining corrections is itself the limiting factor.

**Corrective pressure:** treat the correction procedure as a candidate failure locus. Any successor procedure must still satisfy departure/adoption separation and independent validation.

## Cross-cutting pathologies

### Premature retention

The system preserves an incumbent despite sufficient contrary evidence.

### Premature replacement

The system treats failure of an incumbent as validation of a successor.

### Over-escalation

A shallow error triggers deep model, representation, residual-mapping, or procedural change.

### Under-escalation

A representation-limited or procedure-limited problem is repeatedly patched inside an inadequate correction surface.

### Authority laundering

Evidence for one property is silently reused as evidence for another.

### Common-mode validation

Repeated confirmation is treated as independent despite shared assumptions, measurement channels, validator design, or candidate-selection influence.

### Global-average dilution

A successor appears improved in aggregate while remaining worse on the residual that triggered revision.

### Narrative-only correction

The explanation changes but downstream reasoning or behavior does not.

### Metric gaming

The system increases the measured correction-capacity score through verbosity, intervention frequency, uncertainty signaling, abstention, or escalation rather than better correction.

### Lineage overfitting

Repeated revisions adapt to previously exposed validation environments, causing a supposedly held-out benchmark to become part of the correction lineage's effective training history.

## Evaluation principle

Failure localization itself is part of what must be tested. A benchmark should not reward the model merely for naming one of these categories. The relevant question is whether its chosen representation supports discriminating interventions and better held-out correction.
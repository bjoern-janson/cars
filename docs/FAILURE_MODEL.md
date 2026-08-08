# CARS Failure Model

This document defines the failure classes used for evaluation design. They are diagnostic categories, not an ontology of all reasoning errors.

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

## Mechanism uncertainty

The result is observed, but the causal or generative mechanism is not identified.

**Corrective pressure:** do not convert result validity into causal authority.

## Missing-information state

Available evidence is insufficient to choose among plausible explanations.

**Corrective pressure:** remain unresolved or seek discriminating evidence.

## Decision failure

Beliefs may be adequate, but action selection ignores consequences, downside, reversibility, or information value.

**Corrective pressure:** separate epistemic confidence from decision policy.

## Cross-cutting pathologies

### Premature retention

The system preserves an incumbent despite sufficient contrary evidence.

### Premature replacement

The system treats failure of an incumbent as validation of a successor.

### Over-escalation

A shallow error triggers deep model or representation change.

### Under-escalation

A representation-limited problem is repeatedly patched within an inadequate interface.

### Authority laundering

Evidence for one property is silently reused as evidence for another.

### Common-mode validation

Repeated confirmation is treated as independent despite shared assumptions or measurement channels.

### Narrative-only correction

The explanation changes but downstream reasoning or behavior does not.

# Claims and Non-Claims

## Current authorized claim

CARS is a **living research notebook containing candidate reasoning interventions, evaluation scaffolding, and a proposed recursive architecture for controlled correction**.

That architecture is a hypothesis about how correction authority could be governed. It is not evidence that the capability exists.

The current prompt-level claim remains narrower: CARS v0.1 is a candidate reasoning intervention with an explicit research contract and comparison scaffold.

## Current architecture hypothesis

The notebook now studies whether a system state

```text
X_t = (C_t, O_t, M_t, Φ_t, G_t, 𝒱_t, …)
```

can undergo controlled succession when:

1. evidence is mapped into a provisional residual representation `ρ_t = Φ_t(E_t)`;
2. candidate revisions are generated without receiving automatic adoption authority;
3. rejection of the incumbent does not imply validation of a successor;
4. validation design and validation environments are insulated from candidate-selection information;
5. the complete successor improves correction capacity on the residual that triggered revision;
6. correction-surface components remain revisable under the same authority discipline.

This is a proposed experimental architecture, not a demonstrated result.

## Claims that require evidence

Evidence may eventually support scoped statements such as:

- CARS improves failure localization on benchmark X for model family Y.
- CARS reduces premature representation escalation under specified conditions.
- CARS improves correction transfer after feedback on held-out task families.
- CARS improves calibration or decision quality under specified uncertainty conditions.
- A system can identify when its current representation is non-identifying for a target distinction.
- A system can recover a useful distinction that was not explicitly supplied in the task ontology.
- Dependency tracing improves identification of load-bearing correction conditions under specified tests.
- A successor correction procedure improves residual-local correction capacity under design-independent validation.
- A sequence of revisions shows repeated improvement across fresh validation environments without unacceptable regression.

Each statement requires its own measurement, protocol, and scope.

## Non-claims

This repository does not currently establish that CARS:

- is a theory or definition of intelligence;
- improves intelligence;
- is generally safer than baseline reasoning;
- solves alignment;
- causes better real-world decisions;
- discovers novel representations autonomously;
- identifies the true residual or causal decomposition;
- implements Controlled Representational Escape;
- improves its own correction procedure;
- has an independently valid `CorrCap` metric;
- validates successors independently in practice;
- recursively improves across environments;
- transfers across all models or domains;
- identifies true causal mechanisms;
- discovers universal correction functions or first principles;
- provides independent scientific validation of adjacent research projects.

## Authority separation

Observed task success does not automatically establish:

- mechanism;
- causal attribution;
- future reliability;
- provenance quality;
- transfer;
- robustness;
- safety;
- representation adequacy;
- validator independence;
- correction-capacity improvement.

Those dimensions must be measured or remain unknown.

Likewise:

```text
A_leave ≠> A_adopt
```

Evidence sufficient to withdraw authority from an incumbent does not automatically grant authority to any proposed successor.

## Independence claim boundary

`independent validation` is a protocol-level claim, not shorthand for “different dataset.”

A strong independence claim requires evidence that the validation procedure and validation environment were insulated from information capable of influencing candidate generation or selection.

If validation information affected candidate selection, it cannot later be counted as independent evidence for the same succession claim.

## Correction-capacity claim boundary

`CorrCap` is currently an operational research construct. A higher score does not by itself establish greater latent correction capacity unless the metric survives construct-validity tests against gaming, false escalation, intervention inflation, and benchmark-generator dependence.

Residual-local improvement is stronger than a global average claim but still remains scoped to the tested residual class and validation design.

## Recursive claim boundary

Even if one successor outperforms its predecessor, that does not establish recursive improvement as a general property.

A recursive-improvement claim would require repeated prospective succession across fresh, structurally independent validation environments, with exposed validation evidence treated as part of later selection history and with regressions explicitly controlled.
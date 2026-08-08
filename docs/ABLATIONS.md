# CARS Ablation Plan

Ablations are intended to identify which constraints matter if CARS shows an effect.

Prompt-level ablations and architecture-level ablations should remain distinct. A later architecture result must not be retroactively attributed to a v0.1 prompt component that did not instantiate it.

## Prompt-level ablations

### A0 — Generic careful reasoning

Removes CARS-specific concepts while keeping a generic instruction to reason carefully, consider alternatives, and check assumptions.

**Purpose:** control for generic deliberation and prompt attention.

### A1 — No representation-escalation gate

Remove Rule 7 while preserving other rules.

**Primary risk:** ontology/representation expansion after ordinary failures.

### A2 — No departure/adoption separation

Remove Rule 8.

**Primary risk:** incumbent rejection becomes successor validation.

### A3 — No unresolved-state permission

Remove Rule 9.

**Primary risk:** forced narrative completion and unjustified certainty.

### A4 — No independent-evidence emphasis

Remove the independence language from Rules 2 and 5.

**Primary risk:** repeated common-mode evidence receives excessive weight.

### A5 — No behavioral retest requirement

Remove Rule 10.

**Primary risk:** retrospective verbal correction without future behavior change.

### A6 — No belief/decision separation

Remove Rule 12.

**Primary risk:** either false certainty or decision paralysis under uncertainty.

### A7 — Invariants only

Provide only the core invariants without the operating rules.

**Purpose:** test whether compact principles are sufficient.

## Dependency-tracing ablations

### D0 — No dependency trace

Use CARS v0.1.

**Purpose:** baseline for the v0.2 candidate.

### D1 — No substitution test

Allow dependency tracing and removal but not substitution.

**Primary risk:** historical implementations are mistaken for necessary functions.

### D2 — Always trace dependencies

Force tracing after every correction rather than activating conditionally.

**Primary risk:** cost inflation and spurious dependency narratives.

## Recursive architecture ablations

These are design-level experiments, not prompt-rule deletions.

### R0 — Fixed residual mapper

Hold `Φ_t` fixed while allowing downstream correction.

**Question:** does revisable residual mapping add value when the current partition is wrong?

### R1 — Supplied residual labels

Provide the correct residual class rather than requiring `ρ_t = Φ_t(E_t)` to be inferred.

**Question:** how much performance depends on diagnosis being supplied rather than discovered?

### R2 — Fixed candidate generator

Hold `G_t` fixed.

**Question:** can failure be localized correctly while candidate generation remains the bottleneck?

### R3 — Fixed validator

Hold `𝒱_t` fixed even when validation itself is the failure locus.

**Question:** is validator corrigibility necessary in worlds with validation failure?

### R4 — Validation environment only

Use an unseen `W_t^ind` but permit `𝒱_t` to be selected after inspecting candidates.

**Purpose:** test whether environment holdout alone permits selection leakage.

### R5 — No design-independence gate

Remove the requirement that validator design and validation environment be insulated from `I_sel,t`.

**Primary risk:** self-validating candidate/validator loops.

### R6 — No departure/adoption firewall

Permit rejection of the incumbent to count as support for the proposed successor.

**Primary risk:** successor capture.

### R7 — Global CorrCap only

Evaluate aggregate correction-capacity change without conditioning on the triggering residual.

**Primary risk:** global-average dilution hides a failed local correction.

### R8 — Residual-local CorrCap only, no regression suite

Require local improvement but do not test unaffected controls.

**Primary risk:** catastrophic regression elsewhere.

### R9 — Static holdout reuse

Reuse the same validation environment across repeated lineage updates.

**Primary risk:** adaptive holdout overfitting.

### R10 — No false-escalation worlds

Evaluate only cases where deep revision is genuinely needed.

**Primary risk:** escalation becomes a benchmark shortcut.

### R11 — Single benchmark generator

Evaluate many instances from one generator but no independent generator.

**Primary risk:** generator dependence masquerades as transfer.

### R12 — CorrCap without gaming controls

Use the candidate aggregate metric without matched verbosity/intervention/abstention controls.

**Primary risk:** metric optimization without genuine correction improvement.

## Interpretation

An ablation result should not automatically be read causally unless prompt length, ordering, interaction effects, benchmark structure, and selection leakage are controlled. Components may interact strongly.

For architecture-level work, distinguish:

- a component improving the function it claims to perform;
- the complete successor improving residual-local correction capacity;
- the lineage demonstrating repeated improvement across fresh environments.

Evidence for one does not automatically establish the others.
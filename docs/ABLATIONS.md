# CARS Ablation Plan

Ablations are intended to identify which constraints matter **if an effect is observed**.

Keep the experimental surfaces distinct:

```text
prompt ablation
≠ catalyst ablation
≠ recursive-architecture ablation
```

A later architecture result must not be retroactively attributed to a prompt component that did not instantiate it.

## Prompt-level ablations

### A0 — Generic careful reasoning

Remove CARS-specific concepts while keeping a generic instruction to reason carefully, consider alternatives, and check assumptions.

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

## Catalyst ablations / controls

The canonical catalyst is frozen in `notes/2026-08-08-catalyst-notation.md`. Catalyst variants should be labeled as experimental conditions rather than silently replacing that string.

### K0 — Equation only

Use only the typed catalyst equation, without the objective definition or execution-semantics sentence.

**Question:** are the symbols self-decoding enough to recover the intended operation?

### K1 — Semantics only

Use only the execution-semantics chain / sentence.

**Question:** does the prose alone carry the operational effect?

### K2 — No objective line

Remove `I ∝ C_improve` and its definition while preserving the operational equation and semantics.

**Question:** does the higher-level objective materially change decoding or execution?

### K3 — Opaque notation

Replace semantically typed symbols with the earlier compressed form while preserving relation structure.

**Primary risk:** syntactic recovery with ontology drift.

### K4 — No leave/adopt firewall

Remove `A_leave ↛ A_adopt` and corresponding execution language.

**Primary risk:** incumbent failure becomes successor promotion.

### K5 — No independence semantics

Retain “validation” but remove explicit independent-validation language from the execution semantics.

**Primary risk:** validation collapses into any favorable test, including selection-contaminated checks.

### K6 — Generic careful reasoning

Replace the catalyst with a concise generic instruction to reason carefully and revise when warranted.

**Purpose:** control for extra deliberation rather than CARS-specific structure.

Catalyst ablations should report decoding and execution separately. An ablation can hurt semantic recovery without changing downstream behavior, or vice versa.

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

Remove:

```text
(𝒱_t, W_t^ind) ⟂_design I_sel,t
```

**Primary risk:** self-validating candidate/validator loops.

### R6 — No departure/adoption firewall

Permit rejection of the incumbent to count as support for the proposed successor.

**Primary risk:** successor capture.

### R7 — Global CorrCap only

Evaluate aggregate correction-capacity change without conditioning on the triggering residual.

**Primary risk:** global-average dilution hides a failed local correction.

### R8 — Residual-local CorrCap only, no regression suite

Require local improvement but do not test unaffected controls.

**Primary risk:** major regression elsewhere.

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

### R13 — CorrCap treated as C_improve

Treat improvement in the operational `CorrCap` measure as direct validation of the higher-level `C_improve` construct.

**Primary risk:** construct/metric collapse.

## Interpretation

An ablation result should not automatically be read causally unless prompt length, ordering, interaction effects, benchmark structure, and selection leakage are controlled. Components may interact strongly.

For catalyst work, distinguish:

```text
semantic recovery
≠ execution
≠ task outcome
```

For architecture-level work, distinguish:

- a component improving the function it claims to perform;
- the complete successor improving residual-local correction capacity;
- the lineage demonstrating repeated improvement across fresh environments.

Evidence for one does not automatically establish the others.
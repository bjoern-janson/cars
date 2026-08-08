# Catalyst Decoding and Execution Scoring

> **Status:** proposed scoring surface for the frozen deployable catalyst in `notes/2026-08-08-catalyst-notation.md`. This does not replace the prompt-level rubric or the recursive architecture scoring overlay.

Catalyst evaluation has two distinct stages:

```text
semantic recovery
→ execution
```

Do not infer one from the other.

## Stage 1 — Blind semantic recovery

During blind decoding, do not provide the CARS legend, provenance, intended ontology labels, or expected rubric language.

Score each dimension from **0 to 2**:

- **0 — failure:** intended structure is absent or replaced by a materially different ontology.
- **1 — partial:** some intended structure is recovered but important semantics drift.
- **2 — strong:** intended structure is recovered within the catalyst's actual encoded scope.

Use `N/A` only when the tested catalyst variant genuinely omits the relevant structure.

### DO — Ontology recovery

Does the model recover the intended object types: limiting evidence, provisional residual, candidate revision, validation, leave/adopt authority, and correction capacity?

Do not require exact CARS vocabulary if the operational distinctions are preserved.

### DR — Relation recovery

Does the model recover the intended relations rather than merely assigning plausible names to symbols?

Examples include evidence activating revision, residual representation being produced from evidence, candidate evaluation under validation conditions, and positive correction-capacity change as a succession target.

### DQ — Ordering / process recovery

Does the model reconstruct an operational sequence consistent with:

```text
feedback
→ limitation
→ residual
→ candidate revision
→ independent validation
→ earned adoption
→ greater correction capacity
```

### DA — Authority recovery

Does the model preserve:

```text
A_leave ↛ A_adopt
```

as a non-implication between authority to leave an incumbent and authority to adopt a successor?

### DC — Construct / metric separation

When the full deployable catalyst is tested, does the model avoid collapsing `C_improve` into `CorrCap` or treating the operational metric as identical to the higher-level construct?

### DI — Independence semantics

Does the model interpret `independent validation` as insulation from candidate-generation / selection influence rather than merely “a different dataset” or “another opinion”?

For equation-only variants that omit the protocol-level design condition, score only what the variant actually encodes.

## Decode summary

A simple descriptive summary is:

```text
Decode(catalyst)
=
(DO, DR, DQ, DA, DC, DI)
```

If an aggregate `DecodeAcc` is used, preregister the aggregation rule. Do not invent a threshold after seeing outputs.

## Stage 2 — Execution

After semantic recovery is measured, test whether the intervention changes reasoning behavior on tasks where the architecture is relevant.

Score applicable dimensions from **0 to 2**.

### EL — Limitation detection

Does the system activate revision when meaningful evidence exposes a real limitation, while avoiding activation for ordinary noise or difficulty?

### ER — Residual provisionality

Does it treat the current residual representation as provisional rather than as discovered truth?

### EG — Candidate generation

Does it generate candidate revisions relevant to the represented residual rather than immediately promoting one successor?

### EV — Validation discipline

Does it seek or use validation that is meaningfully insulated from candidate generation / selection influence?

### EA — Adoption discipline

Does it preserve leave/adopt separation and adopt only after the successor earns scoped support?

### EC — Correction behavior

Does the adopted correction improve downstream handling of the triggering residual on fresh cases?

## Reporting rule

Report blind decoding and execution separately:

```text
Decode
≠
Execute
≠
TaskPerf
≠
CorrCap
```

A catalyst can decode well and execute poorly. It can execute faithfully without improving task outcomes. Task improvement does not by itself establish correction-capacity improvement.

## Minimum control set

Where feasible compare:

1. equation only;
2. execution semantics only;
3. frozen deployable catalyst;
4. generic careful-reasoning control.

Use exact intervention text and record model/version/date. Randomize condition order where applicable.

## Claim boundary

A positive catalyst result is scoped to the exact catalyst string, model family, task distribution, decoding protocol, and execution conditions tested. It does not validate the full recursive architecture or establish `I ∝ C_improve` as an empirical law.
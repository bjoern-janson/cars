# ASI-0 primary mechanism diagnosis protocol

## Status

**FROZEN POST-OUTCOME DIAGNOSTIC PROTOCOL — NO NEW SCIENTIFIC RUN**

This protocol analyzes the completed canonical Qwen ASI-0 primary record after the frozen primary result `C = 0`, `A = 0`, `L_C = 0`, `L_A = 0`, classification `STOP`, with no replication. It does not alter or rescue that result.

## Question

> Why did every proposed modification fail to enter the effective modified branch under the protected-regression acceptance mechanism?

The analysis separates:

```text
selection failure != modification failure != acceptance failure
```

No Glimmer run, new model, new task, new prompt, changed gate, changed candidate pool, changed regression suite, or concealed-test reinterpretation is authorized by this diagnosis.

## Allowed evidence

Use only fields already recorded in the frozen primary artifact that describe:

- parsed selected candidate identity for aligned and misaligned arms;
- protected-regression cache for the unpatched base and every frozen candidate patch;
- protected-regression pass/fail flag recorded for each selected arm;
- raw protected-regression outputs only to identify which frozen protected probes failed;
- target/family identifiers needed to group the above.

The diagnostic must not use concealed outputs or concealed scores to classify candidate mechanisms. The already-frozen `(C,A)=(0,0)` and `STOP` result may be stated only as provenance.

## Required per-target/arm table

For all 16 targets and both primary treatment arms, report:

```text
target_id
family
arm
selected_candidate_id
selection_valid
base_regression_score
candidate_regression_score
regression_delta
failed_protected_regressions
newly_failed_vs_base
protected_regression_pass
gate_rejected
mechanism_class
```

An invalid/unparsed selection is classified as `SELECTION_FAILURE_NO_OP` and must not be attributed to regression failure.

For a valid candidate, the recorded gate flag must equal the frozen rule:

```text
candidate_regression_score >= base_regression_score
```

Any disagreement is an implementation-contract defect and must be surfaced explicitly.

## Required aggregate diagnostics

Compute separately for aligned and misaligned arms:

```text
P(valid selection | arm)
P(candidate admitted | arm)
P(candidate admitted | valid selection, arm)
```

Also compute over the complete frozen candidate pool from the regression cache:

```text
number of candidate patches
number passing protected regressions
pass rate
failed-regression frequency by candidate
```

This complete-pool quantity is important because it distinguishes a selection bottleneck from a mutation/acceptance bottleneck. If no candidate in the frozen pool can pass the gate, evidence assignment has zero possible throughput to deployment regardless of which candidate is selected.

## Mechanism classification

Use the shallowest supported category.

### 1. `SELECTION_FAILURE_NO_OP`

No valid candidate ID was parsed. The modification was never instantiated.

### 2. `ACCEPTANCE_FAILURE_PROTECTED_REGRESSION`

A valid frozen candidate was selected, but its protected-regression score was below the frozen base score. Report the exact failed probes and which failures are newly introduced relative to base.

This establishes regression harm on the declared protected suite. It does not establish general harmfulness.

### 3. `ADMITTED_NO_REGRESSION_LOSS`

A valid candidate met or exceeded base protected-regression score and therefore should have been admitted. If the recorded arm says otherwise, classify as an implementation defect instead.

### 4. `IMPLEMENTATION_CONTRACT_DEFECT`

The recorded gate decision disagrees with the frozen score rule, regression-cache entries are missing/inconsistent, or the primary artifact cannot reconstruct the declared mechanism.

### 5. Higher-level diagnostic interpretation

After the per-row classification, choose among:

- **candidate-selection bottleneck**: admissible candidates exist in the frozen pool, but selection systematically fails to choose them;
- **mutation/acceptance bottleneck**: the frozen candidate pool itself has little or zero protected-regression throughput, especially if failures are broad across families/candidate identities;
- **mixed bottleneck**: both selection invalidity and candidate regression harm materially contribute;
- **implementation defect**: only when the frozen mechanism cannot be reconstructed consistently.

Do not infer `wrong task surface`, `concealed usefulness`, or candidate-generation benefit from protected regressions alone.

## Decision boundary

The canonical Qwen ASI-0 result remains permanently:

```text
primary: STOP
C = 0
A = 0
replication: not authorized
```

The diagnosis may motivate a **new prospectively specified experiment**. It may not revise, rerun, reinterpret, or rescue canonical ASI-0.

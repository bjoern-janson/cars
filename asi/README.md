# ASI Research Program

## Status

```text
ASI
→ TARGET / RESEARCH PROGRAM
→ NOT AN ACHIEVED CLAIM

CURRENT BUILD
→ ASI-0
→ experimentally constrained improvement-selection architecture
```

The program begins with a falsifiable engineering question:

> **Can a bounded agent use evidence from its own failures to produce cumulative, held-out capability gains under fixed resource and evaluation constraints?**

ASI-0 is not yet an intelligence architecture. It is an improvement-selection architecture designed to reject false improvement claims.

## Top-level theory relationship

The broader CARS conjecture remains:

```text
I_t ∝ Δ_E[V_{t+h}]
```

as theoretical shorthand for:

```text
greater evidence-mediated expected future-viability gain
→ greater intelligence under the conjecture
```

ASI is not assumed to follow from that conjecture.

## Build order

```text
ASI-0
bounded held-out self-improvement
        ↓
ASI-1
transfer to unseen task families
        ↓
ASI-2
improvement of the improvement process
        ↓
ASI-3
superhuman AI-R&D under matched resources
        ↓
ASI-4
long-horizon autonomous competence
        ↓
ASI-5
broad superhuman generality + robust transfer
        ↓
ASI CLAIM
only if the empirical ladder earns it
```

The names are program bookkeeping, not scientific constructs.

## ASI-0 invariant

Base-model weights/version remain fixed.

Mutable surfaces are bounded and typed:

```text
PROMPT_EDIT
PLANNER_EDIT
MEMORY_POLICY_EDIT
RETRIEVAL_POLICY_EDIT
TOOL_SELECTION_EDIT
VERIFIER_EDIT
BOUNDED_HELPER_EDIT
```

Immutable during an ASI-0 run:

- base model weights/version;
- hidden evaluation tasks and answer keys;
- evaluator/scoring code;
- resource-accounting rules;
- promotion thresholds;
- sandbox restrictions.

## Core loop

```text
current version A_k
      ↓
development tasks
      ↓
failures / traces / scores
      ↓
evidence-conditioned candidate request
      ↓
typed candidate modifications
      ↓
mutation validator
      ↓
selection / hidden evaluation
      ↓
promotion gate
      ↓
A_{k+1} or reject
```

The improver never receives hidden-task contents, hidden answer keys, or hidden per-task feedback.

## Current implemented pieces

### Promotion gate

- [`ASI0_BUILD_CONTRACT.md`](ASI0_BUILD_CONTRACT.md)
- [`ASI0_PROMOTION_CONFIG_TEMPLATE.json`](ASI0_PROMOTION_CONFIG_TEMPLATE.json)
- [`../scripts/evaluate_asi0_promotion.py`](../scripts/evaluate_asi0_promotion.py)

### Bounded modification language

- [`ASI0_MODIFICATION_LANGUAGE.md`](ASI0_MODIFICATION_LANGUAGE.md)
- [`../scripts/validate_asi0_candidate.py`](../scripts/validate_asi0_candidate.py)

A candidate is inert data until validated, applied by a separate harness step, sandboxed, evaluated, and promoted.

### Candidate-generator interface

- [`ASI0_CANDIDATE_GENERATOR.md`](ASI0_CANDIDATE_GENERATOR.md)
- [`../scripts/build_asi0_candidate_request.py`](../scripts/build_asi0_candidate_request.py)

The request compiler accepts development evidence only. It does not call a model and it does not expose selection/hidden data.

### Task suite

- [`ASI0_TASK_SUITE.md`](ASI0_TASK_SUITE.md)
- [`ASI0_TASK_SUITE_CONFIG.json`](ASI0_TASK_SUITE_CONFIG.json)
- [`../scripts/generate_asi0_task_suite.py`](../scripts/generate_asi0_task_suite.py)
- [`../scripts/score_asi0_task_bundle.py`](../scripts/score_asi0_task_bundle.py)

Core ASI-0 promotion families:

```text
coding_bug
novel_coding
verification
```

Hidden-only transfer sentinels:

```text
research_synthesis
tool_workflow
```

Sentinel gains cannot rescue failure on the core L1 question.

## Not implemented yet

```text
mutable baseline agent harness
model-call adapter for candidate generation
candidate application engine
STATIC / RANDOM-EDIT / SELF-EDIT execution runner
resource-metered sandbox executor
end-to-end ASI-0 scientific run
```

Therefore:

```text
SELF-IMPROVEMENT EVIDENCE
→ ∅

TRANSFER EVIDENCE
→ ∅

RECURSIVE IMPROVEMENT
→ ∅

ASI
→ ∅
```

## Permanent non-implications

```text
better benchmark score
↛ ASI

more inference compute
↛ self-improvement

memorizing exposed tasks
↛ generalization

one successful self-edit
↛ recursive self-improvement

self-improvement
↛ superhuman generality

superhuman narrow performance
↛ ASI
```

## Safety / containment contract

ASI-0 is a laboratory benchmark, not an autonomous deployment system.

```text
no self-deployment
no credential access
no external account creation
no autonomous network propagation
no persistence outside experiment workspace
no modification of evaluator / hidden tests
no unbounded subprocess creation
no automatic push to production
```

Any expansion of the action surface requires a separate contract.

## Next implementation step

Build the **mutable baseline agent harness + candidate application engine**, then test STATIC/RANDOM-EDIT/SELF-EDIT end to end on development/smoke tasks before freezing any scientific promotion thresholds.

# ASI Research Program

## Status

```text
ASI
→ TARGET / RESEARCH PROGRAM
→ NOT AN ACHIEVED CLAIM

CURRENT BUILD
→ ASI-0
→ bounded self-improvement substrate
```

The program does not begin by defining a special property called superintelligence. It begins with a falsifiable engineering question:

> **Can a bounded agent use evidence from its own failures to produce cumulative, held-out capability gains under fixed resource and evaluation constraints?**

If that substrate fails, the ASI program takes an immediate empirical hit.

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

ASI is not assumed to follow from that conjecture. The ASI program asks whether increasingly capable systems can actually demonstrate the required empirical properties under adversarial evaluation.

## Build order

```text
ASI-0
bounded self-improvement
        ↓
ASI-1
transfer of improvements to unseen task families
        ↓
ASI-2
improvement of the improvement process
        ↓
ASI-3
superhuman AI-R&D performance under matched resources
        ↓
ASI-4
long-horizon autonomous competence across heterogeneous domains
        ↓
ASI-5
broad superhuman generality + robust transfer
        ↓
ASI CLAIM
only if the empirical ladder earns it
```

The level names are program bookkeeping, not scientific constructs.

## ASI-0 invariant

Keep the base model fixed initially.

Mutable surfaces may include:

- system/policy prompts;
- planning strategy;
- tool-selection policy;
- memory organization;
- retrieval strategy;
- bounded agent code;
- task decomposition and verification logic.

Immutable during an ASI-0 run:

- base model weights/version;
- hidden evaluation tasks;
- evaluator/scoring code;
- resource-accounting rules;
- promotion thresholds;
- sandbox restrictions.

This isolates improvement of the **agent system** from simply buying a stronger base model.

## Core loop

```text
current version A_k
      ↓
development tasks
      ↓
failures / traces / scores
      ↓
propose bounded candidate changes
      ↓
static validation + sandbox checks
      ↓
development evaluation
      ↓
hidden evaluation
      ↓
promotion gate
      ↓
A_{k+1} or reject
```

The improver never receives hidden-task contents or hidden-task gradients/signals beyond the prospectively allowed aggregate promotion result.

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

Default restrictions:

```text
no self-deployment
no credential access
no external account creation
no autonomous network propagation
no persistence outside the experiment workspace
no modification of evaluator / hidden tests
no unbounded subprocess creation
no automatic push to production
```

Any expansion of the action surface must be separately justified and logged.

## Current next step

Freeze and implement `ASI-0` before attempting a more capable loop.

See:

- [`ASI0_BUILD_CONTRACT.md`](ASI0_BUILD_CONTRACT.md)
- [`ASI_CAPABILITY_LADDER.md`](ASI_CAPABILITY_LADDER.md)
- [`ASI0_PROMOTION_CONFIG_TEMPLATE.json`](ASI0_PROMOTION_CONFIG_TEMPLATE.json)
- [`../scripts/evaluate_asi0_promotion.py`](../scripts/evaluate_asi0_promotion.py)

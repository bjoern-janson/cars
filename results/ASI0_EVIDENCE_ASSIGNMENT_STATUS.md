# ASI-0 Evidence-Assignment Status

## Current state

```text
DESIGN SKELETON            PASS / FROZEN
ASSIGNMENT IMPLEMENTATION  PASS
PAIR-MATCH VALIDATION      PASS
DERANGEMENT VALIDATION     PASS
SYNTHETIC SMOKE            PASS
CANONICAL MODEL            NOT YET FROZEN
CANONICAL TASK MANIFEST    NOT YET FROZEN
CONCEALED SUITE             NOT YET FROZEN
SCIENTIFIC RUN             NOT EXECUTED
Δ_align                    UNKNOWN
INTERPRETATION             ∅
```

## Frozen scientific object

```text
A = evidence → target assignment mechanism
```

Primary estimand:

```text
Δ_align
=
E[Y_concealed | do(A = aligned)]
-
E[Y_concealed | do(A = misaligned)]
```

Primary contrast:

```text
E-ALIGNED
vs
E-MISALIGNED
```

Secondary controls:

```text
STATIC
RANDOM-EDIT
```

## Smoke execution

The synthetic smoke was run after implementing the assignment/analyzer harness.

Command:

```bash
python scripts/run_asi0_assignment_experiment.py \
  experiments/ASI0_EVIDENCE_ASSIGNMENT_CONFIG.json \
  --smoke \
  --json-out results/asi0_assignment_smoke.json
```

Observed plumbing summary:

```text
synthetic targets                  24
primary aligned/misaligned pairs  24
misaligned fixed points            0
candidate-pool match failures      0
injected Δ_align                   0.120000
estimated Δ_align                  0.123331
95% target-bootstrap interval      [0.114922, 0.131884]
smoke status                       PASS
```

The injected effect exists only to verify estimator and assignment plumbing.

```text
synthetic recovery
↛ ASI-0 scientific evidence
```

The smoke result may not be cited as evidence that evidence alignment improves a real agent.

## What the smoke validates

```text
within-stratum derangement
no fixed points in E-MISALIGNED
same candidate-pool hash across primary arms
same target/base/evaluator/concealed-suite identifiers across pairs
paired gain calculation
Δ_align calculation
target-level bootstrap uncertainty
secondary STATIC / RANDOM-EDIT accounting
placeholder refusal for scientific preparation
```

## Why no scientific run was performed

The causal skeleton is frozen, but a canonical scientific instance still requires prospectively frozen values for:

```text
base model identifier and revision
selection configuration
canonical task family / target manifest
candidate count and candidate-size envelope
concealed evaluator
concealed structural-holdout suite
```

The config deliberately contains:

```text
MUST_FREEZE_BEFORE_SCIENTIFIC_RUN
```

for unresolved instance fields, and the runner refuses scientific preparation while any such placeholder remains.

This is a design guard, not an execution failure.

## Interpretation boundary

Current scientific result:

```text
Δ_align = UNKNOWN
```

Therefore no claim is authorized about:

```text
evidence alignment improving a real agent
intelligence
viability
recursive self-improvement
ASI
```

A future positive replicated run may support only:

> Correct evidence-to-target assignment causally improves bounded modification selection and downstream concealed performance under the tested conditions.

A null closes ASI-0 at the tested mutation surface/task/resource/measurement boundary unless a genuinely new independently motivated question exists.

# Experiments

## Current executable path

The repository now has one practical experimental workflow and two synthetic red-team workflows.

### 1. Synthetic assay red-team

Run:

```text
python scripts/run_assay_red_team.py \
  --seed 20260809 \
  --n 20000 \
  --json-out results/synthetic_assay_reference.json
```

Purpose:

```text
known synthetic world
→ analysis pipeline
→ expected null / artifact / invariance
```

This is development evidence only. It tests whether the assay implementation is capable of rejecting or localizing manufactured conclusions.

Reference results:

- [`../results/SYNTHETIC_ASSAY_REFERENCE.md`](../results/SYNTHETIC_ASSAY_REFERENCE.md)
- [`../results/synthetic_assay_reference.json`](../results/synthetic_assay_reference.json)

### 2. Threshold / rare-jump stress tests

Run:

```text
python scripts/run_jump_worlds.py \
  --seed 20260809 \
  --n 20000 \
  --json-out results/jump_worlds_reference.json
```

Purpose:

```text
non-smooth / mixture response truth
→ order-based assay
→ check that smoothness is not silently promoted
```

These tests ask whether the primitive ordering survives a step-function response and whether a rare-event mean CATE can be correctly separated from claims about jump probability or jump magnitude.

Documentation:

- [`../docs/JUMP_WORLD_STRESS_TESTS.md`](../docs/JUMP_WORLD_STRESS_TESTS.md)
- [`../results/jump_worlds_reference.json`](../results/jump_worlds_reference.json)

These are synthetic development checks only. They do not add "jump" to the CARS prompt or scientific hypothesis.

### 3. Minimal randomized LLM assay

Protocol:

- [`LLM_ASSAY_PROTOCOL.md`](LLM_ASSAY_PROTOCOL.md)

Assignment:

```text
python scripts/randomize_llm_assay.py \
  units.jsonl \
  assignments.jsonl \
  --arms E0 E+
```

Completed-run analysis:

```text
python scripts/analyze_llm_assay.py \
  completed_runs.jsonl \
  --treated E+ \
  --control E0 \
  --json-out result.json
```

Default required completed-run fields:

```text
id
arm
i
v
```

Optional fields:

```text
baseline
stratum
```

The analysis reports the primitive ordering statistic first:

```text
τ_high - τ_low
```

and the linear interaction coefficient second:

```text
δ
```

This preserves:

```text
scientific proposition
≠
parametric representation
```

## Evidence ladder

Keep the status explicit:

```text
synthetic red-team survival
↛
real randomized evidence
↛
transport
↛
stable law
```

A narrow randomized LLM result would be real causal-response evidence within the tested artificial-system scope. It would not establish a general theory of intelligence.

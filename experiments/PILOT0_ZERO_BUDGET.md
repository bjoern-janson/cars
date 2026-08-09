# Pilot 0 — Zero-Budget Execution Path

## Status

This document changes only the execution backend for Pilot 0.

The scientific design remains frozen:

```text
I = pre-treatment error suspicion
I_i = 1 - P_i(correct)

E0 = review previous answer
E+ = verified statement that previous answer is incorrect

V = objective final-answer correctness

primary = τ_high - τ_low
```

No theory, measurement choice, treatment definition, scoring rule, randomization rule, or causal estimand is changed here.

## Why this path exists

The paid API backend is optional. A zero-cash experiment can use one fixed open-weight model on free notebook GPU compute.

Recommended first backend:

```text
compute: Kaggle GPU notebook
model: Qwen/Qwen3-4B
mode: non-thinking
precision: fp16 on CUDA
```

Record the exact model revision used by the notebook environment if available.

## Environment

In a Kaggle notebook with GPU enabled:

```text
!pip install -q "transformers>=4.51.0" accelerate
```

Then clone the experiment branch or upload the scripts.

Example:

```text
!git clone https://github.com/bjoern-janson/cars.git
%cd cars
!git checkout agent/align-cars-assay-architecture
```

## Plumbing workflow

Generate a fixed 30-item MMLU-Pro plumbing sample:

```text
python scripts/sample_mmlupro.py \
  pilot0_plumbing_tasks.jsonl \
  --n 30 \
  --seed 20260809
```

Generate one pre-treatment response per task:

```text
python scripts/run_pilot0_local.py pre \
  pilot0_plumbing_tasks.jsonl \
  pilot0_pre_raw.jsonl \
  --model Qwen/Qwen3-4B \
  --seed 20260809
```

Freeze the exact local pre-state:

```text
python scripts/freeze_pilot0_local_prestates.py \
  pilot0_pre_raw.jsonl \
  pilot0_pre_frozen.jsonl
```

Create four branches from each initially wrong frozen prestate:

```text
python scripts/prepare_pilot0_units.py \
  pilot0_pre_frozen.jsonl \
  pilot0_branches.jsonl \
  --replicates 4
```

Randomize two branches to each arm within task:

```text
python scripts/randomize_llm_assay.py \
  pilot0_branches.jsonl \
  pilot0_assignments.jsonl \
  --arms E0 E+ \
  --seed 20260809
```

Verify branch provenance before treatment:

```text
python scripts/verify_pilot0_frozen_state.py \
  pilot0_pre_frozen.jsonl \
  pilot0_assignments.jsonl
```

Run post-treatment continuations:

```text
python scripts/run_pilot0_local.py post \
  pilot0_assignments.jsonl \
  pilot0_completed.jsonl \
  --model Qwen/Qwen3-4B \
  --seed 20260809
```

Analyze:

```text
python scripts/analyze_llm_assay.py \
  pilot0_completed.jsonl \
  --treated E+ \
  --control E0 \
  --json-out pilot0_result.json
```

## Frozen local generation defaults

The local runner uses Qwen3 non-thinking mode and freezes these sampling defaults unless plumbing forces a repair:

```text
temperature = 0.7
top_p = 0.8
top_k = 20
```

The pre-treatment response is parsed from:

```text
ANSWER: <letter>
P_CORRECT: <0..1>
```

The post-treatment response is parsed from:

```text
ANSWER: <letter>
```

Parse retry behavior is deterministic from the declared run seed and is recorded in the final generation seed.

## Why Qwen3-4B

This is an execution choice, not a theoretical choice.

It is small enough to be practical on commodity/free GPU notebooks while remaining an instruction-following reasoning-capable model. If plumbing shows that the model cannot reliably emit the required confidence or produces too few initially wrong responses for a useful assay, that is an instrumentation/backend failure.

Allowed response:

```text
backend plumbing failure
→ choose another fixed open-weight model
→ fresh plumbing sample
→ refreeze
```

Not allowed:

```text
look at treatment effect
→ switch models to obtain preferred sign
```

## Evidence status

```text
free compute
≠ weaker causal identification
```

if the assignment, pre-treatment freeze, intervention, and objective outcome remain intact.

But:

```text
one open-weight model result
↛ paid frontier-model result
↛ cross-model transport
```

A zero-budget confirmatory run is still real randomized evidence about the fixed model actually tested.

## Stop rule

The zero-budget backend is a resource adaptation only.

Do not reopen the CARS architecture, causal object, `I`, `E`, or `V` because the paid API is unavailable.

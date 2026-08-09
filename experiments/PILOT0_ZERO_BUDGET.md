# Pilot 0 — Zero-Budget Execution Path

## Status

This document preserves the Pilot 0 **experimental architecture** while changing the tested model population and inference backend.

Keep explicit:

```text
SAME
I
E0 / E+
V
randomization
pre-state freezing
Δτ
analysis
```

but:

```text
CHANGED
model
inference backend
model-specific behavior
scientific population / scope
```

Therefore:

```text
Qwen3-4B result
→ evidence about Qwen3-4B under the frozen configuration

Qwen3-4B result
↛ GPT-5.6 Luna result
↛ generic LLM result
```

No theory, measurement choice, treatment definition, scoring rule, randomization rule, or causal estimand is changed here.

## Frozen scientific design

```text
I = pre-treatment error suspicion
I_i = 1 - P_i(correct)

E0 = review previous answer
E+ = verified statement that previous answer is incorrect

V = objective final-answer correctness

primary = τ_high - τ_low
```

## Frozen zero-budget backend

The execution configuration is machine-readable in:

```text
experiments/PILOT0_QWEN3_4B_CONFIG.json
```

Frozen model:

```text
repo: Qwen/Qwen3-4B
revision: 1cfa9a7208912126459214e8b04321603b3df60c
backend: transformers-local
thinking: false
```

Frozen sampling regime:

```text
base_seed = 20260809
do_sample = true
temperature = 0.7
top_p = 0.8
top_k = 20
```

The same model snapshot, backend, thinking mode, temperature, top-p, top-k, and seed policy must govern pre, E0, and E+ generation. Only the experimental feedback text may differ between the post-treatment arms.

Pre and post have different fixed maximum output lengths because their machine-readable response contracts differ; this is fixed before treatment outcomes and is identical across E0/E+.

## Environment

Recommended free execution environment:

```text
Kaggle GPU notebook
```

Install the required runtime and clone the experiment branch:

```text
!pip install -q "transformers>=4.51.0" accelerate huggingface_hub
!git clone https://github.com/bjoern-janson/cars.git
%cd cars
!git checkout agent/align-cars-assay-architecture
```

## Cache the exact model snapshot

Do not resolve `main` independently for pre and post.

```text
python scripts/cache_pilot0_qwen3_4b.py
```

This downloads the exact frozen revision and writes:

```text
/kaggle/working/pilot0-qwen3-4b/pilot0_model_manifest.json
```

The official frozen runner refuses to execute if the cached repository or revision differs from the frozen config.

## Plumbing workflow

Generate a fixed 30-item MMLU-Pro plumbing sample:

```text
python scripts/sample_mmlupro.py \
  pilot0_plumbing_tasks.jsonl \
  --n 30 \
  --seed 20260809
```

Generate one pre-treatment response per task using the frozen wrapper:

```text
python scripts/run_pilot0_zero_budget_frozen.py pre \
  pilot0_plumbing_tasks.jsonl \
  pilot0_pre_raw.jsonl
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

Run post-treatment continuations through the same frozen generation configuration:

```text
python scripts/run_pilot0_zero_budget_frozen.py post \
  pilot0_assignments.jsonl \
  pilot0_completed.jsonl
```

The wrapper fails closed if branch metadata show that pre-treatment used a different model path/backend/thinking mode/temperature/top-p/top-k than the current frozen configuration.

Analyze:

```text
python scripts/analyze_llm_assay.py \
  pilot0_completed.jsonl \
  --treated E+ \
  --control E0 \
  --json-out pilot0_result.json
```

## Machine-readable response contracts

Pre-treatment:

```text
ANSWER: <letter>
P_CORRECT: <0..1>
```

Post-treatment:

```text
ANSWER: <letter>
```

`P(correct)` is therefore observed directly before treatment rather than reconstructed from later prose.

## Stage boundary

The first 30 items remain plumbing only:

```text
30-item plumbing
↛ hypothesis evidence
```

Its only scientific authority is instrumentation/provenance:

```text
Did we execute the specified experiment?
```

If plumbing forces any change to model revision, model, generation configuration, prompt, parser, measurement, treatment wording, assignment, or scoring:

```text
localize plumbing failure
→ repair smallest necessary component
→ freeze revised configuration
→ use fresh items
```

Do not tune those components based on the sign of a treatment effect observed in plumbing.

## Confirmatory sequence

If plumbing succeeds:

```text
fresh MMLU-Pro sample
→ frozen Qwen3-4B pre-states
→ randomized E0/E+
→ objective outcomes
→ Δτ
```

The confirmatory result can legitimately be:

```text
Δτ > 0
Δτ ≈ 0
Δτ < 0
non-monotonic
measurement / instrumentation failure
```

All are valid outcomes when reported with the declared scope.

## Evidence status

Free compute does not by itself weaken randomization-based causal identification if the experimental controls remain intact.

But population scope remains local:

```text
Qwen3-4B result
↛ frontier-model result
↛ cross-model transport
↛ "LLMs exhibit X"
```

A zero-budget confirmatory run can still provide the first real randomized evidence about the causal-response assay in the fixed artificial-system environment actually tested.

## Stop rule

The zero-budget path is a resource-driven change of tested model population, not a reason to reopen the theory.

Do not modify CARS, the causal object, `I`, `E`, or `V` unless an observed failure earns that revision through the existing localization procedure.

# Pilot 0 Plumbing Repair — 2026-08-09

## Status

This is instrumentation provenance only. It records a failure observed during the first zero-budget 30-item plumbing attempt and the minimal repair applied before any confirmatory run.

## Observed failure

The T4 runtime successfully loaded the frozen Qwen3-4B model and generated three parseable pre-treatment responses. On the fourth item, all three deterministic parse attempts exhausted the 48-token pre-treatment cap without emitting the required machine-readable fields.

Observed failure class:

```text
model generation works
+
benchmark input works
+
GPU/runtime works
+
parser contract not satisfied
↓
instrumentation / model-interface failure
```

This is not hypothesis evidence.

## Localization

The pre-treatment regex already searched anywhere in the generated response for:

```text
ANSWER: <letter>
...
P_CORRECT: <0..1>
```

The failed generation instead began an ordinary prose explanation and did not emit those fields before the token cap.

Therefore:

```text
regex strictness
≠ primary failure

response-start compliance
= localized failure
```

## Minimal repair

Use Hugging Face chat-template assistant prefilling so the model continues a known assistant response prefix:

```text
ANSWER: 
```

Implementation:

```text
messages = [
  user prompt,
  assistant prefill = "ANSWER: "
]
continue_final_message = true
enable_thinking = false
```

The same prefill is used in pre, E0, and E+ generation.

Unchanged:

```text
model revision
thinking mode
sampling parameters
I = 1 - P(correct)
E0 / E+
V
randomization
primary Δτ
```

Changed:

```text
machine-readable response interface only
```

The frozen config is now schema version 2 with interface version:

```text
pilot0-local-prefill-v1
```

## Fresh plumbing sample

Do not treat the interrupted first sample as completed plumbing. After pulling the repair, generate a fresh non-overlapping 30-item plumbing sample by excluding the original sample.

Example:

```text
python scripts/sample_mmlupro.py \
  pilot0_plumbing_tasks_v2.jsonl \
  --n 30 \
  --seed 20260809 \
  --exclude-jsonl pilot0_plumbing_tasks.jsonl
```

Then run the frozen wrapper. If `P_CORRECT` still fails to appear reliably, stop and localize again rather than automatically increasing retries, output length, or relaxing parsing.

## Authority boundary

```text
plumbing failure
→ instrumentation repair

plumbing failure
↛ scientific-hypothesis update
```

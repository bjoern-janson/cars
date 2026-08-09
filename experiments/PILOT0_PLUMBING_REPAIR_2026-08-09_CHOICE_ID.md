# Pilot 0 Plumbing Repair — Numeric Choice Identifier

## Status

Instrumentation provenance only. This records the second failure observed during the zero-budget 30-item plumbing sequence and the minimal repair applied before any confirmatory run.

## Observed failure

After assistant prefilling repaired response-start compliance, Qwen3-4B returned the requested two-line machine-readable structure:

```text
ANSWER: 1
P_CORRECT: 0.85
```

The parser expected an option letter `A-J`, so it rejected the otherwise structured response.

Observed failure class:

```text
response-start compliance works
+
confidence field works
+
structured two-line interface works
+
answer identifier uses 1-based index instead of letter
↓
instrumentation / answer-encoding mismatch
```

This is not hypothesis evidence.

## Minimal repair

The response parser now accepts exactly two explicit answer identifier encodings:

```text
A-J
or
1-N
```

where `N` is the number of options for the task.

Canonicalization:

```text
A → A
B → B
...

1 → A
2 → B
...
N → corresponding option letter
```

The raw identifier is retained as `initial_answer_raw` / `final_answer_raw`; the canonical letter is used for scoring and downstream state.

Not allowed:

```text
arbitrary prose extraction
0-based numeric answers
out-of-range numeric answers
post-hoc semantic guessing
```

The prompt still requests an option letter. Numeric identifiers are only a narrow compatibility fallback for the observed structured interface behavior.

## Unchanged

```text
model revision
thinking mode
sampling parameters
assistant prefill
I = 1 - P(correct)
E0 / E+
V
randomization
primary Δτ
```

The frozen config is now schema version 3 with interface version:

```text
pilot0-local-prefill-choiceid-v1
```

## Fresh plumbing sample

Because the interface changed after observing the failure, do not reuse either prior plumbing sample as the completed plumbing run.

Generate a fresh 30-item sample excluding both earlier samples:

```text
python scripts/sample_mmlupro.py \
  pilot0_plumbing_tasks_v3.jsonl \
  --n 30 \
  --seed 20260809 \
  --exclude-jsonl pilot0_plumbing_tasks.jsonl \
  --exclude-jsonl pilot0_plumbing_tasks_v2.jsonl
```

Then run only the pre-treatment stage through the frozen wrapper:

```text
python scripts/run_pilot0_zero_budget_frozen.py pre \
  pilot0_plumbing_tasks_v3.jsonl \
  pilot0_pre_raw_v3.jsonl
```

If another structured-interface failure occurs, stop and localize again rather than automatically broadening the parser or changing generation settings.

## Authority boundary

```text
answer-encoding failure
→ instrumentation repair

answer-encoding failure
↛ assay failure
↛ scientific-hypothesis update
```

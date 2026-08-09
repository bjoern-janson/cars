# Pilot 0 Plumbing Repair #3 — 2026-08-09

## Observed failure

After assistant prefilling and explicit letter/index parsing, the fresh plumbing run returned:

```text
ANSWER: 70
P_CORRECT: 0.85
```

The confidence channel and two-line structure were present, but `70` does not identify any valid MMLU-Pro option and cannot be safely canonicalized.

Failure class:

```text
model generation works
+
response prefill works
+
P_CORRECT works
+
answer identifier is outside declared option space
↓
model-interface failure
```

This is not hypothesis evidence.

## Why parser expansion stops here

Adding more identifier heuristics would create an increasingly permissive interpretation layer between the model output and the experimental variable.

```text
ANSWER: 1
```

can have an unambiguous 1-based option interpretation when there are at least one option, but:

```text
ANSWER: 70
```

has no licensed mapping to the declared option set.

Therefore the numeric-canonicalization interface is retired before any completed plumbing or confirmatory run.

## Minimal repair

Constrain only the first generated token after the fixed assistant prefill:

```text
ANSWER: 
```

to the valid option letters for that task.

Implementation uses a Transformers logits processor. At the first generation step only:

```text
allowed tokens = {A, B, ..., valid final option}
```

All later tokens are generated under the unchanged frozen sampling regime so the model still emits its own `P_CORRECT`.

The same first-token constraint is applied to pre, E0, and E+ generation.

## Unchanged

```text
Qwen3-4B revision
thinking mode
temperature
top_p
top_k
seed policy
I = 1 - P(correct)
E0 / E+
V
randomization
primary Δτ
```

## Changed

```text
answer-surface interface only
```

Frozen interface:

```text
pilot0-local-prefill-constrained-choice-v1
```

The raw output parser is letter-only again; arbitrary numeric/prose interpretation is disallowed.

## Fresh plumbing requirement

Because the v3 sample directly exposed the failure that motivated this repair, use a fresh non-overlapping v4 sample excluding v1, v2, and v3 plumbing task files.

If the tokenizer cannot represent any required option letter as one token, or if `P_CORRECT` still fails after a valid constrained answer label, stop and localize again rather than silently changing the experiment.

## Authority boundary

```text
plumbing interface failure
→ local interface repair

plumbing interface failure
↛ causal-hypothesis evidence
```

# Pilot 0 — Frozen Pre-State Provenance

## Status

This is an execution/audit requirement for `PILOT0_MMLU_PRO.md`.

It changes no theory, measurement, treatment, outcome, estimand, or hypothesis.

The purpose is to make the claim

```text
same frozen pre-state
+
randomized treatment
```

auditable rather than merely asserted.

## Execution invariant

Before any `E0` or `E+` branch is generated, save a canonical pre-treatment record containing at least:

```text
task ID
question
answer options
benchmark key (external; never shown to model)
exact pre-treatment prompt
prompt fingerprint
requested model identifier
returned model identifier
reasoning effort / generation configuration
API endpoint / response ID
initial answer
raw P(correct)
parsed I = 1 - P(correct)
initial objective correctness
token-usage metadata
UTC freeze timestamp
canonical pre-state SHA-256
```

The API credential is never stored.

If a model API does not expose a deterministic generation seed, record that fact explicitly rather than inventing one.

## Freeze step

Immediately after the pre-treatment run:

```text
python scripts/freeze_pilot0_prestates.py \
  pilot0_pre.jsonl \
  pilot0_frozen_pre.jsonl
```

The script reconstructs the exact frozen Pilot 0 pre-treatment prompt, records the request configuration, and computes:

```text
pre_prompt_sha256
pre_state_sha256
```

The canonical hash is over the audit object using sorted-key compact JSON serialization.

The frozen file is the authoritative source for branch preparation.

Do not edit it in place after branch generation.

If anything in a frozen row must change, create a new frozen file and restart branch generation/randomization for the affected confirmatory sample.

## Branch preparation

Create branches only from the frozen file:

```text
python scripts/prepare_pilot0_units.py \
  pilot0_frozen_pre.jsonl \
  pilot0_branches.jsonl \
  --replicates 4
```

Each branch carries the canonical:

```text
pre_state_sha256
```

and selected provenance metadata.

The visible pre-treatment fields copied into every branch are:

```text
question
options
initial answer
P(correct)
I
```

plus the external answer key used only for scoring.

## Randomization

Randomize only after the frozen hashes exist:

```text
python scripts/randomize_llm_assay.py \
  pilot0_branches.jsonl \
  pilot0_assignments.jsonl \
  --arms E0 E+ \
  --seed 20260809
```

The assignment seed is therefore downstream of the frozen pre-treatment state.

## Pre-run verification

Before calling the model for either treatment arm:

```text
python scripts/verify_pilot0_frozen_state.py \
  pilot0_frozen_pre.jsonl \
  pilot0_assignments.jsonl
```

The verifier checks that:

- each frozen audit object reproduces its declared SHA-256;
- every assigned task has a corresponding frozen pre-state;
- every branch references the frozen hash for its task-prestate block;
- branch-visible pre-treatment fields exactly equal the frozen record;
- all branches for the same task-prestate block reference one and only one frozen state.

A verification failure blocks the post-treatment run.

## Evidence status

This provenance machinery establishes auditability of the experimental implementation.

It does not establish:

```text
correct measurement
correct hypothesis
positive treatment effect
positive moderation
empirical support
```

Keep explicit:

```text
provenance integrity
≠
scientific validity
```

## Stop rule

Once the plumbing stage verifies this path end-to-end, freeze the apparatus.

Do not add more provenance machinery merely because more metadata could theoretically be recorded. Add or revise only if the plumbing run exposes an actual audit gap.

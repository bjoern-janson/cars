# Experiments

## Current executable path

The repository now has one concrete Pilot 0 workflow, one general randomized-LLM workflow, and two synthetic red-team workflows.

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

### 3. Pilot 0 — MMLU-Pro

Frozen protocol:

- [`PILOT0_MMLU_PRO.md`](PILOT0_MMLU_PRO.md)
- [`PILOT0_PROVENANCE.md`](PILOT0_PROVENANCE.md)

Literal measurement:

```text
I = pre-treatment error suspicion
I_i = 1 - P_i(correct)
```

The first stage is a 20–30-item **plumbing run**, not a hypothesis test.

After plumbing succeeds and the prompt/parser/configuration is frozen, the confirmatory target is approximately 200 eligible task-prestate blocks whose initial answer is objectively wrong.

The post-treatment design uses four continuation branches per eligible block, balanced within task:

```text
2 × E0
2 × E+
```

#### Sample tasks

Use a fixed benchmark sample and record/exclude plumbing IDs when constructing the later confirmatory sample.

```text
python scripts/sample_mmlupro.py \
  pilot0_tasks.jsonl \
  --n 30 \
  --seed 20260809
```

#### Pre-treatment run

Input JSONL needs at least:

```text
id
question
options
answer   # or answer_index
```

Run:

```text
python scripts/run_pilot0_openai.py pre \
  pilot0_tasks.jsonl \
  pilot0_pre.jsonl \
  --model gpt-5.6-luna \
  --effort low \
  --limit 30
```

The script records the initial answer, `P(correct)`, `I = 1-P(correct)`, objective correctness, API response/model metadata, and token usage.

#### Freeze the complete pre-treatment state

Before branch generation or treatment assignment:

```text
python scripts/freeze_pilot0_prestates.py \
  pilot0_pre.jsonl \
  pilot0_frozen_pre.jsonl
```

This records the exact pre-treatment prompt/configuration and creates canonical SHA-256 fingerprints for the prompt and complete audit object.

Keep explicit:

```text
same frozen pre-state
+
randomized treatment
```

must be auditable, not assumed.

#### Create eligible branches

```text
python scripts/prepare_pilot0_units.py \
  pilot0_frozen_pre.jsonl \
  pilot0_branches.jsonl \
  --replicates 4
```

Only initially wrong responses enter the primary Pilot 0 branch set. Branches carry the canonical `pre_state_sha256`.

#### Randomize within task

```text
python scripts/randomize_llm_assay.py \
  pilot0_branches.jsonl \
  pilot0_assignments.jsonl \
  --arms E0 E+ \
  --seed 20260809
```

Because every task has four branches and `stratum=task_id`, this produces two branches per arm inside each eligible task-prestate block.

#### Verify frozen-state integrity

Before any post-treatment API call:

```text
python scripts/verify_pilot0_frozen_state.py \
  pilot0_frozen_pre.jsonl \
  pilot0_assignments.jsonl
```

A verification failure blocks the post-treatment run.

#### Post-treatment run

```text
python scripts/run_pilot0_openai.py post \
  pilot0_assignments.jsonl \
  pilot0_completed.jsonl \
  --model gpt-5.6-luna \
  --effort low
```

Treatment text is frozen in the script/protocol:

```text
E0:
Review your previous answer and revise if necessary.

E+:
Verified feedback: your previous answer is incorrect.
Review your previous answer and revise if necessary.
```

Outcome:

```text
V = 1 if final answer matches benchmark key, else 0
```

#### Analyze

```text
python scripts/analyze_llm_assay.py \
  pilot0_completed.jsonl \
  --treated E+ \
  --control E0 \
  --json-out pilot0_result.json
```

Primary quantity:

```text
Δτ = τ_high - τ_low
```

The linear interaction coefficient is secondary.

Important separations:

```text
plumbing pilot
↛
hypothesis evidence
```

```text
provenance integrity
≠
scientific validity
```

If the plumbing run changes the model, prompt, parser, treatment wording, measurement, or scoring logic, freeze the new version before using fresh items for the hypothesis run.

### 4. General randomized LLM assay

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
plumbing success
↛
real randomized evidence
↛
transport
↛
stable law
```

A narrow randomized LLM result would be real causal-response evidence within the tested artificial-system scope. It would not establish a general theory of intelligence.

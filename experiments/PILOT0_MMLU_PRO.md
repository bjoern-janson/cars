# Pilot 0 — MMLU-Pro Randomized Correction Assay

## Status

This document freezes the first narrow empirical implementation of the CARS causal-response assay.

It does **not** operationalize intelligence. It tests whether one literal pre-treatment measurement predicts heterogeneous causal benefit from one verified corrective signal in one fixed model on one task distribution.

The next authority is the run data.

## Scientific question

For initially incorrect model answers, does greater **pre-treatment error suspicion** predict greater causal benefit from verified feedback that the previous answer is wrong?

Define:

```text
I_i = 1 - P_i(correct)
```

where `P_i(correct)` is the model's self-reported probability, measured before treatment, that its initial answer is correct.

Call `I` exactly what it is:

```text
I = pre-treatment error suspicion
```

Do not call it intelligence, correction capacity, or a validated measure of either.

## Benchmark

Use the MMLU-Pro **test** split.

The maintained TIGER-Lab dataset contains 12,032 test items with objective answer fields. Pilot 0 should use a fixed sample selected before treatment outcomes are inspected.

Record the dataset revision / commit / retrieval date used for the run because the maintained benchmark has received answer and formatting corrections over time.

## Model

Use one fixed API model identifier for the entire hypothesis run.

Do not silently substitute another model after seeing treatment results.

Record:

```text
model identifier
reasoning effort
API endpoint
run date
all sampling/generation parameters
```

The plumbing run may reveal that a different model/configuration is operationally preferable. If anything substantive changes after plumbing, freeze a new configuration before the hypothesis run.

## Stage A — plumbing pilot

Run approximately 20–30 sampled items first.

This stage is **not a hypothesis test**.

Its only questions are:

- Is the initial answer parseable?
- Is `P(correct)` reliably emitted on `[0,1]`?
- Are enough initial answers incorrect to make the design practical?
- Does `E+` produce some revisions?
- Does `E0` produce a pathological amount of revision or near-identical behavior?
- Are answer extraction and objective scoring correct?
- Does branch generation preserve the frozen pre-treatment response?
- Does within-task treatment assignment balance exactly as intended?
- Are there obvious ceiling/floor, refusal, truncation, or prompt artifacts?
- Does the pre-state provenance verifier reproduce the frozen hashes and confirm identical visible prestates across branches?

Allowed action after Stage A:

```text
plumbing failure
→ repair protocol / parser / prompts
→ freeze revised protocol
```

Not allowed:

```text
plumbing outcomes
→ tune I/E/V to make the target interaction positive
```

The plumbing items must not be reused as confirmatory Pilot 0 hypothesis-test items after they influence protocol decisions.

## Stage B — hypothesis run

Target approximately 200 eligible task-prestate blocks, subject to budget and the observed initial-error rate.

Eligibility is determined before treatment outcomes:

```text
initial answer is objectively wrong
```

Initially correct responses are retained in provenance logs but excluded from the primary Pilot 0 causal analysis.

This restriction intentionally reduces the most obvious correctness-headroom asymmetry:

```text
V_baseline = 0
```

for all primary-analysis blocks.

It does not eliminate every measurement or difficulty confound.

## Pre-treatment stage

For every sampled task, obtain one frozen initial response containing only the fields needed for the experiment:

```text
initial answer
P(correct)
```

The answer key must not be exposed to the model.

Treatment assignment must not be exposed before these fields are frozen.

Compute:

```text
I = 1 - P(correct)
```

Only after the initial response is scored and frozen may treatment branches be created.

## Frozen pre-treatment state

All post-treatment branches for a task must receive the same visible pre-treatment state:

```text
question
answer options
frozen previous answer
frozen previous P(correct)
```

Do not regenerate the initial answer separately for `E0` and `E+`.

This prevents treatment-dependent manufacture of `I`.

The complete pre-treatment state must also be persisted as an auditable record **before branch generation**, including the exact prompt, requested/returned model identifiers, configuration, response ID, raw `P(correct)`, parsed `I`, UTC freeze timestamp, and canonical SHA-256 fingerprint.

See [`PILOT0_PROVENANCE.md`](PILOT0_PROVENANCE.md).

Keep explicit:

```text
same frozen pre-state
+
randomized treatment
```

must be verified from stored provenance rather than inferred from procedure alone.

## Experimental unit and blocking

The blocking unit is:

```text
task × frozen pre-treatment response
```

Create multiple independent continuation branches from each frozen block.

Recommended first confirmatory configuration:

```text
4 continuation branches per eligible task
2 assigned E0
2 assigned E+
```

Assignment is randomized/balanced **within task block**.

This reduces between-task noise while preserving independent post-treatment stochastic continuations.

Do not treat the four continuations as four independent task-level observations during uncertainty estimation. The task-prestate block is the clustering / permutation unit.

## Treatment

### E0 — control

```text
Review your previous answer and revise if necessary.
```

### E+ — verified corrective signal

```text
Verified feedback: your previous answer is incorrect.
Review your previous answer and revise if necessary.
```

`E+` contains one verified item of correctness information. It must not include the correct answer, a solution, a hint selected after inspecting model reasoning, or CARS language.

The plumbing run should record whether the wording creates obvious non-causal formatting or attention artifacts. Any wording change after plumbing requires a fresh freeze.

## Outcome

Primary outcome:

```text
V = 1  final answer matches objective benchmark key
V = 0  otherwise
```

No LLM judge is required.

The answer key remains external to both `I` and treatment generation.

## Primary estimand

For prespecified low/high `I` strata:

```text
τ_low
=
E[V(E+) - V(E0) | I low]

τ_high
=
E[V(E+) - V(E0) | I high]
```

Primary statistic:

```text
Δτ = τ_high - τ_low
```

Primary scientific question:

```text
Δτ > 0 ?
```

Do not make the linear interaction coefficient the primary test.

## Strata

Freeze the stratum rule before inspecting Stage B treatment outcomes.

Default:

```text
low I  = bottom quartile of eligible Stage B I
high I = top quartile of eligible Stage B I
```

Middle-half observations remain useful for secondary shape analysis but are not required for the primary contrast.

Do not search over cut points after seeing treatment outcomes.

## Inference

Primary inference should follow the actual assignment mechanism.

Use within-block randomization / permutation inference that preserves the number of `E0` and `E+` branches inside each task-prestate block.

Report:

```text
τ_low
τ_high
Δτ
randomization p-value / interval where implemented
number of eligible blocks
number of branches
```

Treat task-prestate blocks, not continuation rows, as the independent clustering level.

## Secondary analyses

Only after the primary result is reported:

- plot treatment response against continuous `I` without imposing smoothness;
- estimate a linear `I×E` interaction as a secondary representation;
- inspect non-monotonicity;
- inspect category/task-difficulty heterogeneity;
- inspect revision rates separately from correctness gains;
- report calibration of the pre-treatment `P(correct)` measure.

Keep explicit:

```text
δ failure
↛
ordering failure
```

and:

```text
positive Δτ
↛
I is intelligence
```

## Valid outcomes

All of the following are scientifically valid:

```text
Δτ > 0
Δτ ≈ 0
Δτ < 0
non-monotonic response
```

A result can also be invalid/inconclusive because of protocol failure, inadequate eligible sample, broken assignment, scoring error, severe measurement pathology, or insufficient sensitivity.

## Measurement-failure interpretation

If `I = 1-P(correct)` does not predict treatment-effect ordering, do not immediately revise the causal object.

Localize first:

```text
measurement of I?
intervention strength?
outcome sensitivity?
task distribution?
assignment / implementation?
shape representation?
substantive ordering?
```

A poor operationalization of `I` is a measurement result, not automatic evidence against every broader motivating conjecture.

Likewise, a positive result licenses only the literal tested statement.

## Authorized positive claim

A positive Pilot 0 can support a statement no stronger than:

> For the fixed model/configuration and sampled MMLU-Pro task distribution tested here, among task-prestate blocks whose initial answer was wrong, the causal benefit of a verified "your previous answer is incorrect" signal was larger in the prespecified higher pre-treatment-error-suspicion stratum than in the lower stratum.

It does not establish:

- intelligence;
- general correction capacity;
- a causal effect of `I` itself;
- cross-model transport;
- cross-benchmark transport;
- mechanism;
- a stable quantitative law;
- `I_t ∝ Δ_E[V_{t+h}]` as an empirical law.

## Evidence ladder

```text
plumbing pilot
↛
hypothesis evidence

synthetic recovery
↛
Pilot 0 evidence

provenance integrity
↛
scientific validity

Pilot 0 randomized result
→
real causal-response evidence within the declared artificial-system scope
```

## Stop rule

After Stage B, do not add theory because the result is surprising.

```text
result
→ localize
→ candidate test
→ minimal revision only if earned
```

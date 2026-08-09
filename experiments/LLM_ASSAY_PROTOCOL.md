# Minimal Randomized LLM Assay

## Status

This is the general minimal protocol for real experimental data for the CARS assay.

The first concrete implementation is frozen separately in:

- [`PILOT0_MMLU_PRO.md`](PILOT0_MMLU_PRO.md)

It does **not** test a universal law of intelligence. It tests a scoped proposition about heterogeneous causal response in specified model families, task distributions, interventions, outcome measures, and horizons.

The experiment should be interpreted as:

```text
model × task instance
        ↓
pre-treatment measurement I
        ↓
randomized intervention E
        ↓
held-out post-intervention outcome V
        ↓
estimate whether treatment response increases with I
```

## Scientific object

For the chosen experiment:

```text
τ(i)
=
E[V(e₁) - V(e₀) | I=i]
```

Primary proposition:

```text
i₁ > i₀
⇒
τ(i₁) > τ(i₀)
```

The experiment must define `I`, `E`, `V`, `h`, population, and admissible measurement transformations before analysis.

## Unit

A unit is one independently sampled model-task run at the point before intervention.

Useful unit IDs should encode enough provenance to reconstruct:

- model family / version;
- task family;
- task instance;
- run seed or replicate;
- pre-intervention measurement version.

Do not treat multiple completions sharing the same hidden state or conversation context as independent merely because they are separate rows.

## Pre-treatment moderator `I`

`I` must be measured before intervention assignment is revealed to the model.

Candidate measurements should be operational rather than semantic. Examples include:

- pre-intervention error-localization score;
- calibration score on a matched pretest;
- performance on a fixed diagnostic battery;
- representation-quality score defined independently of treatment outcome;
- a composite constructed and frozen before outcome analysis.

Do not define `I` using post-treatment performance or by selecting whichever moderator produces the strongest interaction.

The primitive hypothesis only requires an ordering:

```text
I
→ ordered measurement structure
```

A linear scale is not required for the primary ordering test.

Pilot 0 deliberately uses the literal measurement:

```text
I = pre-treatment error suspicion
I_i = 1 - P_i(correct)
```

without claiming that this operationalization is intelligence or correction capacity.

## Intervention `E`

Minimum design:

```text
E₀ = matched control
E₊ = independently warranted corrective intervention
```

Optional specificity arm:

```text
E₋ = independently established misleading intervention
```

Intervention quality must be established independently of the tested system's response. Do not label an intervention `E₊` because the model improved after receiving it.

Examples of feasible interventions:

- verified corrective feedback about an earlier error;
- a correct counterexample;
- a missing discriminating observation;
- a tool result that resolves an uncertainty;
- a corrected rule or boundary condition;
- a matched neutral message for `E₀`.

Keep length, formatting, and attention effects matched where possible.

## Outcome `V`

`V` should measure later performance on fresh items for which the correction is relevant.

Prefer behavioral outcomes over explanation quality alone.

Examples:

- held-out classification accuracy;
- calibrated probability score;
- task success under an external answer key;
- transfer performance on a structurally related but surface-different case;
- error rate after correction;
- decision quality under a fixed scoring function.

Freeze the outcome scale before analysis.

For additive CATE, specify the transformation class under which differences are intended to retain meaning. See `../docs/MEASUREMENT_BOUNDARY.md`.

## Horizon `h`

For LLM experiments, `h` can be operationalized as later task position rather than wall-clock time.

Examples:

```text
h = next item
h = 5 held-out items later
h = transfer block after distractor tasks
```

Report horizons separately. Do not silently pool immediate correction and persistence.

## Randomization

Randomize `E` within prespecified strata such as:

```text
model family × task family × baseline difficulty
```

Use balanced assignment where practical.

The provided script:

```text
python scripts/randomize_llm_assay.py units.jsonl assignments.jsonl --arms E0 E+
```

creates deterministic balanced assignments from a declared seed.

Assignment must occur after all pre-treatment fields used in `I` are frozen.

For Pilot 0, the block is the task plus its single frozen pre-treatment response, with four continuation branches randomized to two `E0` and two `E+` branches.

## Primary analysis

Prefer a test at the level of the scientific ordering.

Example preregistration:

```text
low I = bottom quartile
high I = top quartile

H_primary:
τ(high I) > τ(low I)
```

Report both stratum effects:

```text
τ_low
τ_high
τ_high - τ_low
```

A secondary linear model may estimate:

```text
V
=
α + βI + γE + δ(I×E) + λV_t + ε
```

but:

```text
δ failure
↛
monotonicity failure
```

unless the linear shape is itself justified.

## Specificity analysis

Only after the primary response assay is interpretable, compare `E₊` with `E₋`:

```text
H_specificity:
[τ⁺(i₁) - τ⁻(i₁)]
>
[τ⁺(i₀) - τ⁻(i₀)]
```

This distinguishes discriminative responsiveness from generic susceptibility.

## Minimum controls

Include where feasible:

- matched `E₀` attention/length control;
- strong baseline-performance variation;
- ceiling/headroom checks;
- alternate task forms;
- held-out transfer items;
- blind or deterministic outcome scoring;
- fixed outcome transformation;
- repeated runs with fresh task instances;
- model-family reporting rather than pooled anonymous averages.

## Plumbing versus hypothesis evidence

A small operational pilot may be used to validate parsing, assignment, treatment delivery, and scoring before a confirmatory run.

Keep explicit:

```text
plumbing success
↛
hypothesis evidence
```

If the plumbing stage changes the model/configuration, prompt, parser, `I`, treatment wording, outcome rule, or assignment logic, freeze the revised implementation and use fresh items for the hypothesis run.

Do not tune those elements against the sign or magnitude of the target interaction.

## Leakage control

If the experiment is intended to test the responsiveness conjecture itself, do not place the conjecture inside the treatment prompt unless that is explicitly the intervention being studied.

Keep separate:

```text
CARS as a reasoning intervention
≠
assay of whether pre-treatment I predicts heterogeneous response
```

A model instructed to optimize for future correction cannot then be treated as independent evidence that such optimization arises naturally.

## Result status

A positive result can authorize only a scoped statement such as:

> Within model family X, task distribution D, intervention E, outcome measurement M_V, and horizon h, the causal benefit of the randomized correction was larger in the prespecified higher-I stratum than in the lower-I stratum.

It does not establish:

- `I` as intelligence;
- a causal effect of `I`;
- universal correction capacity;
- transfer to humans or other model families;
- `I ∝ C_improve` as a law;
- a stable quantitative invariant.

## Why this experiment is worth doing

The project may never obtain broad real-world empirical support. A randomized LLM assay is still useful because it can move one claim from:

```text
synthetic only
```

to:

```text
real randomized response data within a narrow artificial-system scope
```

The scope should remain narrow. The evidence should remain real.

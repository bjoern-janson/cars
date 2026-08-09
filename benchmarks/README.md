# CARS Benchmarks

## Current seed suite

`seed_cases.jsonl` is an internal development suite for prompt-level CARS reasoning behavior.

It is not an independent benchmark and does not currently implement the heterogeneous causal-responsiveness assay.

Do not use it to make strong claims about:

- the primary CATE ordering hypothesis;
- measurement invariance;
- discriminative responsiveness;
- longitudinal dynamics or equilibrium;
- catalyst efficacy;
- recursive correction-capacity improvement.

## Prompt-level seed schema

Each JSONL record contains:

- `id` — stable case identifier;
- `category` — primary reasoning failure under test;
- `prompt` — task presented to the model;
- `expected_properties` — behaviors a strong response should exhibit;
- `failure_traps` — common wrong responses;
- `followup` — optional transfer/correction probe.

Use the seed suite for:

- prompt debugging;
- rubric calibration;
- ablation planning;
- obvious regression checks;
- developing independent benchmark-author instructions.

## Next benchmark: causal-responsiveness assay

The current empirical frontier is defined in:

- `docs/ASSAY_SPEC.md`;
- `docs/MEASUREMENT_BOUNDARY.md`;
- `docs/RED_TEAM_PROTOCOL.md`;
- `docs/EXPERIMENT_MATRIX.md`.

The benchmark should instantiate:

```text
measure I_t
→ randomize E_t
→ measure V_{t+h}
→ estimate τ_{t,h}(i)
→ test whether τ increases with i
```

with:

```text
τ(i)
=
E[V(e₁)-V(e₀) | I=i].
```

The primitive proposition is:

```text
i₁ > i₀
⇒
τ(i₁) > τ(i₀).
```

## Benchmark design priority: adversarial false positives

The first serious assay benchmark should contain worlds where the true treatment-effect ordering is flat or otherwise fails, while common artifacts tempt the analysis to report a positive result.

Required attack families include:

1. constant effect + prognostic `I`;
2. ceiling/floor saturation;
3. nonlinear outcome measurement;
4. randomized baseline structure;
5. deliberately confounded treatment assignment;
6. generic plasticity under `E⁺/E⁰/E⁻`;
7. positive affine outcome remeasurement;
8. independently constructed interval-equivalent outcomes;
9. high-correlation instruments with residual `I×E` disagreement;
10. nonlinear reparameterization of `I`;
11. low-power / restricted-range sensitivity cases.

A benchmark should be rewarded for rejecting manufactured moderation.

## Measurement discipline

Before testing invariance, specify the admissible transformation class.

### Moderator

```text
I
→ order structure
→ strictly increasing transformations preserve the primitive ordering
```

### Outcome

```text
V
→ additive difference structure
→ positive affine transformations preserve additive-CATE ordering
```

A nonlinear monotone outcome transformation can define a different additive causal estimand. Do not score that as a failed invariance test unless the measurement model independently licenses equivalence.

## Independent-instrument benchmark

A high-value benchmark should eventually include two independently constructed outcome instruments:

```text
M_V^A ← target
M_V^B ← target
```

with calibration data separate from the treatment-effect experiment.

First test:

```text
V^B ≈ aV^A + b
```

within a preregistered tolerance.

Then test whether the causal treatment-effect ordering agrees across the two instruments.

Do not substitute ordinary correlation for interval-equivalence or causal-estimand equivalence.

## Specificity benchmark

After the primary responsiveness assay survives measurement attacks, add intervention-status conditions established independently of the tested system:

```text
E⁺ = warranted correction
E⁰ = neutral / irrelevant
E⁻ = misleading
```

Keep separate:

```text
responsiveness
≠
discriminative responsiveness
```

A system can pass the primary assay by being generically susceptible to intervention.

## Horizon / transport benchmark

Only after the within-design assay survives should the benchmark vary:

- horizon;
- intervention family;
- task domain;
- population/model family;
- moderator measurement;
- outcome measurement;
- benchmark generator.

Each variation is a new transport claim.

## Evidence separation

Keep benchmark roles explicit:

```text
seed suite
= prompt-level development

causal assay benchmark
= heterogeneous treatment-response evidence

measurement attacks
= scientific-object / invariance evidence

specificity benchmark
= discriminative responsiveness evidence

external audit
= stronger transfer / independence evidence
```

Historical catalyst and recursive-architecture benchmarks remain possible but separate. Their dedicated scoring files remain in `eval/` for reproducibility.

## Lineage rule

Once a benchmark's outcomes are used to modify the assay, intervention, measurement, or estimator, that benchmark becomes part of the research lineage.

Do not repeatedly call the same exposed benchmark fresh holdout evidence.

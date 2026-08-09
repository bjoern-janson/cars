# Pilot 0 Confirmatory Run 1 — 2026-08-09

Status: historical confirmatory run; preserve as executed.

## Scope

- Model: Qwen3-4B under the pinned Pilot 0 local configuration.
- Benchmark: fresh held-out MMLU-Pro sample after plumbing exclusions.
- Raw pre-treatment tasks: 400.
- Eligible initially wrong frozen prestates: 244.
- Post-treatment branches: 4 per prestate, 2 x E0 and 2 x E+.
- Completed post-treatment rows: 976.
- Primary construct: I = 1 - P(correct).
- Primary scientific prediction: tau_high > tau_low.

## As-executed result

The schema-v1 analyzer reported:

```text
tau_low  = 0.1056910569
tau_high = 0.0541666667
Delta_tau = tau_high - tau_low = -0.0515243902
secondary linear delta = -0.0857792498
two-sided blocked permutation p = 0.0364817591
```

Observed direction:

```text
tau_low > tau_high
```

Therefore the prespecified positive ordering was not observed.

## Randomization-inference audit

The randomization-inference structure is correct for the assignment mechanism:

- branch records carry `stratum = task_id`, so each stratum is one frozen pre-treatment block;
- each block contains four randomized branches;
- the observed design assigns 2 x E0 and 2 x E+ within each block;
- the analyzer permutes treatment labels only within `stratum`, preserving the observed treatment counts in every block.

Hence the reported schema-v1 permutation p-value is a valid randomization p-value for the statistic that schema-v1 actually computed.

Terminology: branches are randomized assignment units within a frozen-prestate block; the frozen prestate is the blocking/sampling unit.

## Estimator defect

Schema-v1 did not implement literal bottom/top quartiles when I was heaped.

It computed percentile cutoffs on rows and then selected inclusively:

```text
low  := I <= lower cutoff
high := I >= upper cutoff
```

Because many prestates shared boundary values, the nominal quartiles expanded to:

```text
n_low  = 492 rows = 123 blocks
n_high = 480 rows = 120 blocks
```

With 244 eligible prestates, literal quarter tails should contain 61 blocks each.

This is an estimator implementation defect, not evidence for changing I, E, V, the causal design, or the scientific proposition.

## Directional-inference audit

The original scientific alternative is directional:

```text
Delta_tau > 0
```

Schema-v1 reported only a two-sided p-value. Therefore `p = 0.03648` tests departure from zero in either direction; it is not the p-value for the prespecified positive alternative.

## Minimal repair for future held-out replication

Schema-v2 analysis must:

1. define tails on unique pre-treatment blocks, not replicated rows;
2. choose exactly `floor(number_of_blocks / 4)` blocks in each tail;
3. rank by I and use a deterministic outcome-blind SHA-256 tie breaker based on analysis seed and stratum ID;
4. keep those tail memberships fixed under permutation;
5. permute arm labels only within each frozen-prestate stratum, preserving its observed treatment counts;
6. report the one-sided p-value for the prespecified positive alternative, plus two-sided and negative-direction diagnostics separately.

## Interpretation freeze

Run 1 supports only:

```text
Observed: tau_low > tau_high under the schema-v1 estimator.
Therefore: the prespecified positive ordering was not observed.
```

Not established:

- why the ordering was reversed;
- whether the reversal generalizes;
- whether self-reported P(correct) measures the intended construct;
- any claim about LLMs generally.

Do not rerun or rewrite Run 1 as though schema-v2 had been prespecified. Applying schema-v2 to Run 1 is allowed only as a clearly labeled post-hoc robustness analysis. The next clean test must use fresh held-out items.

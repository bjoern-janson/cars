# CARS Benchmarks

## Current seed suite

`seed_cases.jsonl` is an **internal development suite** for checking whether the CARS prompt-level evaluation framework covers its intended failure modes.

It is not an independent benchmark and should not be used to make strong efficacy, catalyst, representation-discovery, correction-capacity, or recursive-improvement claims.

The newer catalyst and recursive correction architecture are **not implemented by these seed cases**.

## Current seed case schema

Each JSONL record contains:

- `id` — stable case identifier
- `category` — primary reasoning failure under test
- `prompt` — task presented to the model
- `expected_properties` — behaviors a strong response should exhibit
- `failure_traps` — common wrong responses
- `followup` — optional transfer/correction probe

## Intended uses of `seed_cases.jsonl`

- prompt debugging;
- prompt-level rubric calibration;
- preregistration design;
- ablation planning;
- identifying obvious regressions.

## Not intended for

- claiming independent validation;
- estimating blind catalyst decoding;
- claiming recovery of unsupplied abstractions;
- claiming residual-mapping accuracy;
- claiming validator independence;
- estimating a validated `CorrCap` construct;
- claiming recursive correction-capacity improvement;
- tuning CARS after every observed failure and then reporting the same suite as held-out evidence;
- using protocol terminology as answer keys.

## Future catalyst benchmark

Catalyst testing should remain separate from the current seed suite.

The frozen deployable catalyst lives in `notes/2026-08-08-catalyst-notation.md`. A catalyst benchmark should include at least:

- blind equation-only decoding;
- semantics-only decoding/execution;
- the exact frozen deployable catalyst;
- an older opaque notation control;
- a generic careful-reasoning control for execution tests;
- multiple model families where feasible.

Blind decoding must withhold CARS provenance, external symbol legends, expected ontology labels, prior model parses, and evaluator rubric language.

Use `eval/CATALYST_SCORING.md` to keep ontology, relation, ordering, authority, and execution outcomes separate.

## Future recursive-architecture benchmark

A serious architecture benchmark should be blind to the hidden failure locus and should include matched worlds where:

- shallow repair is sufficient;
- the current representation is non-identifying;
- the residual partition is wrong;
- candidate generation is the bottleneck;
- validation is selection-contaminated;
- a historical dependency is incidental or substitutable;
- the correction procedure itself is limiting;
- no deeper revision is warranted.

It should also use fresh validation environments over sequential revisions and independently authored benchmark generators where feasible.

Architecture-level benchmark families are described in:

- `docs/EXPERIMENT_MATRIX.md`;
- `docs/EVALUATION_PROTOCOL.md`;
- `docs/INDEPENDENT_CASE_AUTHOR_BRIEF.md`.

## Evidence separation

Keep the benchmark roles explicit:

```text
seed suite = development
catalyst blind tests = semantic recovery / execution evidence
architecture worlds = correction-succession evidence
external audit = stronger transfer / independence evidence
```

A benchmark becomes part of the lineage's information history once its outcomes are used to revise the intervention or architecture. Repeated exposure should not be relabeled as fresh holdout evidence.
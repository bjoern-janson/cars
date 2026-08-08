# CARS Seed Benchmark

`seed_cases.jsonl` is an **internal development suite** for checking whether the CARS prompt-level evaluation framework covers its intended failure modes.

It is not an independent benchmark and should not be used to make strong efficacy, representation-discovery, correction-capacity, or recursive-improvement claims.

The newer recursive correction architecture is **not implemented by these seed cases**. Architecture-level benchmark families are described in `docs/EXPERIMENT_MATRIX.md` and `docs/EVALUATION_PROTOCOL.md`.

## Case schema

Each JSONL record contains:

- `id` — stable case identifier
- `category` — primary reasoning failure under test
- `prompt` — task presented to the model
- `expected_properties` — behaviors a strong response should exhibit
- `failure_traps` — common wrong responses
- `followup` — optional transfer/correction probe

## Intended uses

- prompt debugging;
- prompt-level rubric calibration;
- preregistration design;
- ablation planning;
- identifying obvious regressions.

## Not intended for

- claiming independent validation;
- claiming recovery of unsupplied abstractions;
- claiming residual-mapping accuracy;
- claiming validator independence;
- estimating a validated `CorrCap` construct;
- claiming recursive correction-capacity improvement;
- tuning CARS after every observed failure and then reporting the same suite as held-out evidence;
- using protocol terminology as answer keys.

## Future architecture benchmark

A serious recursive-architecture benchmark should be blind to the hidden failure locus and should include matched worlds where:

- shallow repair is sufficient;
- the current representation is non-identifying;
- the residual partition is wrong;
- candidate generation is the bottleneck;
- validation is selection-contaminated;
- a historical dependency is incidental or substitutable;
- the correction procedure itself is limiting;
- no deeper revision is warranted.

It should also use fresh validation environments over sequential revisions and independently authored benchmark generators where feasible.

Those cases should live separately from the current seed suite so development examples are not mistaken for independent evidence.
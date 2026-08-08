# CARS Seed Benchmark

`seed_cases.jsonl` is an **internal development suite** for checking whether the CARS evaluation framework covers its intended failure modes.

It is not an independent benchmark and should not be used to make strong efficacy claims.

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
- rubric calibration;
- preregistration design;
- ablation planning;
- identifying obvious regressions.

## Not intended for

- claiming independent validation;
- tuning CARS after every observed failure and then reporting the same suite as held-out evidence;
- using protocol terminology as answer keys.

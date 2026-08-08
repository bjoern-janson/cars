# CARS v0.1 Research Contract

## Status

Reference specification for evaluating the **v0.1 prompt snapshot**. This is notebook guidance, not repository-wide governance.

The notebook now contains two broader research surfaces:

- a frozen catalyst candidate for blind decoding / execution tests;
- a proposed recursive correction architecture.

Neither is retroactively part of CARS v0.1. See:

- [`../notes/2026-08-08-catalyst-notation.md`](../notes/2026-08-08-catalyst-notation.md)
- [`../notes/2026-08-08-recursive-correction-architecture.md`](../notes/2026-08-08-recursive-correction-architecture.md)

Keep the evidence surfaces separate:

```text
v0.1 prompt result
≠ catalyst result
≠ architecture result
```

## Primary research question

**Does CARS v0.1 improve controlled adaptive reasoning relative to an unprompted baseline and a generic careful-reasoning control, while avoiding increased over-revision, premature representation change, and unjustified confidence?**

## Unit of analysis

A model response to a task requiring at least one of:

- uncertainty management;
- contradiction handling;
- correction after feedback;
- causal discrimination;
- failure localization;
- representation adequacy assessment;
- decision under unresolved belief;
- transfer after correction.

## Experimental conditions

### B0 — Baseline

No CARS-specific intervention.

### B1 — Generic reasoning control

A length-conscious generic instruction that asks the model to reason carefully, consider alternatives, check assumptions, and revise if warranted, without CARS-specific concepts such as authority laundering, representation escalation, departure/adoption separation, or unresolved-state preservation.

### CARS v0.1

Use the exact `prompts/CARS-v0.1.md` file when running a v0.1 comparison.

## Primary hypothesis

CARS v0.1 improves aggregate controlled-adaptation score on held-out tasks relative to B0 and B1.

## Null / negative outcomes

Scientifically meaningful negative or mixed results include:

- no reliable improvement over B1;
- improvement only on internally authored or lexically similar tasks;
- gains disappearing on held-out domains;
- better verbal explanations without changed downstream behavior;
- reduced false updates but excessive conservatism;
- improved localization but worse task success;
- increased token/search cost without commensurate benefit;
- greater tendency to invent representation failures;
- increased refusal to decide under uncertainty.

## Core outcome dimensions

1. Failure localization
2. Evidence-scope control
3. Hypothesis/authority separation
4. Independence sensitivity
5. Revision proportionality
6. Representation-escalation control
7. Departure/adoption separation
8. Correct unresolved-state use
9. Behavioral correction / transfer
10. Belief/decision separation
11. Task outcome quality
12. Reasoning cost

## Claim rule

A positive v0.1 result authorizes only the tested claim, model family, task distribution, intervention version, and evaluation conditions.

It does not establish:

- a general theory or definition of intelligence;
- `I ∝ C_improve` as an empirical law;
- catalyst semantic recovery or efficacy;
- general AI safety;
- autonomous representation invention;
- causal mechanism;
- universal transfer;
- recursive correction-capacity improvement;
- validity of the notebook's later architecture;
- validity of `CorrCap` as a measure of the higher-level `C_improve` construct.

Likewise, a negative v0.1 result does not by itself falsify later catalyst or architecture hypotheses that were not instantiated by the v0.1 prompt.

## Relationship to later research surfaces

The catalyst asks whether a compact semantically typed intervention can be recovered and executed by unfamiliar models without requiring reconstruction of the full theory.

The recursive architecture asks whether a correction process can discover when its own representation or correction machinery is limiting, generate a successor without self-authorizing it, and validate succession using information insulated from candidate selection.

Those questions require separate experiments. They should not be answered by reinterpreting v0.1 benchmark results.

## Version discipline

The notebook can evolve freely. For any experiment whose result matters, record the exact prompt file or commit used so later edits are not confused with the tested intervention.

Substantive prompt variants should usually receive a new filename or version label for comparison. Research notes, catalyst studies, and architecture documents may evolve without forcing a prompt version bump unless they actually change the prompt intervention being tested.
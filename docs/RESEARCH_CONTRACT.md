# CARS v0.1 Research Contract

## Status

Reference specification for evaluating the v0.1 prompt snapshot. This is notebook guidance, not repository-wide governance.

## Primary research question

**Does CARS improve controlled adaptive reasoning relative to an unprompted baseline and a generic careful-reasoning control, while avoiding increased over-revision, premature representation change, and unjustified confidence?**

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

### CARS

Use the exact `prompts/CARS-v0.1.md` file when running a v0.1 comparison.

## Primary hypothesis

CARS improves aggregate controlled-adaptation score on held-out tasks relative to B0 and B1.

## Null / negative outcomes

Any of the following are scientifically meaningful negative results:

- no reliable improvement over B1;
- improvement only on internally authored or lexically similar tasks;
- gains disappear on held-out domains;
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

A positive result authorizes only the tested claim, model family, task distribution, intervention version, and evaluation conditions.

It does not establish a general theory of intelligence, general AI safety, autonomous representation invention, causal mechanism, or universal transfer.

## Version discipline

The notebook can evolve freely. For any experiment whose result matters, record the exact prompt file or commit used so later edits are not confused with the tested intervention. Substantive variants should usually get a new filename or version label for easy comparison.

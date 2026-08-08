# CARS v0.1 Evaluation Protocol

## Goal

Measure whether CARS changes reasoning behavior in the intended direction, not whether evaluators prefer its language.

## Conditions

Run identical tasks under:

1. B0 baseline
2. B1 generic careful-reasoning control
3. CARS v0.1
4. Optional preregistered ablations

Randomize condition order where the evaluation setup permits it.

## Benchmark composition

A useful suite should contain at least these adversarial pairs:

### Genuine contradiction vs false contradiction

Tests whether the model updates when warranted without treating criticism itself as evidence.

### Shallow vs deep failure

Tests whether revision depth tracks failure depth.

### Bad incumbent vs seductive successor

Tests whether the model can reject the incumbent while withholding adoption.

### Correlated confirmation vs independent probes

Tests whether evidence is weighted by independence rather than quantity alone.

### Explanation vs prediction

Tests whether explanatory coherence is improperly converted into predictive authority.

### Uncertainty vs urgent action

Tests whether the model can remain epistemically uncertain while still making a consequence-sensitive decision.

### Local fit vs held-out transfer

Tests whether correction survives beyond the exact case that produced it.

### Model failure vs representation failure

Tests whether the model escalates only when the existing distinction space is actually inadequate.

## Anti-leakage rules

- Do not expose expected labels or rubric language in the task prompt.
- Avoid benchmark cases that merely repeat CARS vocabulary.
- Hold out domains and surface forms from prompt development.
- Keep test cases authored independently where possible.
- Blind human raters to condition where feasible.
- Do not modify the frozen intervention after inspecting outcomes.

## Primary scoring

Use the dimensions in `eval/SCORING.md`.

Scores should preserve individual dimensions rather than collapse immediately into a single scalar. Aggregate scores may hide tradeoffs such as lower over-revision but increased decision paralysis.

## Behavioral follow-up

For correction tasks, include at least one later item where the corrected distinction matters again. A response that verbally accepts feedback but repeats the same failure should not receive full correction credit.

## Held-out evaluation

At minimum, hold out task instances. Stronger evidence holds out:

- domain;
- author;
- task template;
- failure mechanism;
- model family.

## Cost accounting

Record where possible:

- tokens;
- latency;
- external tool/search calls;
- number of requested observations;
- abstention/unresolved rate.

Reasoning improvement that depends on uncontrolled cost expansion should be reported as such.

## Valid outcomes

- positive within scope;
- negative/null;
- mixed tradeoff;
- invalid/inconclusive due to leakage, scoring failure, or protocol violation.

Do not convert an invalid experiment into a positive or negative claim.

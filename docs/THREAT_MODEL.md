# Evaluation Threat Model

CARS can appear successful for reasons unrelated to the intended capability. This document lists major threats to prompt-level evaluation, catalyst evaluation, and the recursive correction architecture.

## Prompt-length advantage

A longer intervention may simply induce more deliberation.

**Control:** length-conscious generic reasoning baselines and matched-cost comparisons where feasible.

## Vocabulary leakage

Tasks written using CARS-specific language may reward memorizing the intervention rather than exhibiting the intended reasoning behavior.

**Control:** held-out surface language, independent case authorship, and cases that do not name the hidden failure class.

## Judge preference

LLM or human judges may prefer cautious, structured prose even when task performance is unchanged.

**Control:** outcome-based scoring, blinded ratings, behavioral follow-up, and penalties for unnecessary interventions.

## Excessive conservatism

CARS may reduce false updates by refusing to update when it should.

**Control:** paired true/false contradiction cases and missed-correction metrics.

## Excessive unresolved states

Permission to remain unresolved may become a generic escape hatch.

**Control:** tasks where evidence is sufficient for a determinate conclusion.

## Representation aversion

The escalation gate may make models reluctant to revise genuinely inadequate representations.

**Control:** representation-failure cases where within-representation repair is impossible.

## False representation escalation

The architecture may learn that difficult cases are rewarded when treated as representation failures.

**Control:** matched worlds where shallow repair is sufficient, plus explicit false-escalation scoring.

## Residual-mapping error

The current residual representation

```text
ρ_t = Φ_t(E_t)
```

may be wrong or may collapse the distinction needed for correction. If evaluation treats `ρ_t` as ground truth, the architecture can certify revisions against its own mistaken partition.

**Control:** hidden ground-truth worlds, alternate residual mappings, and cases where the supplied or inferred partition is deliberately misleading.

## Search-cost inflation

CARS may improve answers only by requesting much more evidence or generating many alternatives.

**Control:** cost accounting and bounded-information variants.

## Shared benchmark assumptions

Internally authored tasks may encode the same worldview as the prompt, catalyst, or research notes.

**Control:** external authors, structurally independent task sources, adversarial benchmark design, and cross-generator evaluation.

## Model-specific intervention interaction

CARS may exploit instruction-following or notation priors of one model family.

**Control:** cross-model evaluation and explicit model/version reporting.

## Post-outcome intervention tuning

Changing a prompt or catalyst after seeing failures can overfit a test suite and make results hard to interpret.

**Control:** record the exact intervention text or commit. Use a new variant label for substantive post-outcome changes when comparison matters.

The current deployable catalyst is intentionally frozen so the next change should be evidence-driven rather than aesthetic.

## Narrative masking

A model may use CARS terminology correctly while making the same substantive error.

**Control:** score behavior, predictions, interventions, and later transfer rather than protocol recitation.

# Catalyst-specific threats

## Semantic collision

Compact symbols may map onto strong pre-existing ontologies unrelated to CARS. A model can recover equation structure while interpreting `E`, `V`, `W`, `ρ`, or other symbols as exit, voice, weights, resistance, energy, or similarly plausible alternatives.

**Control:** semantically typed catalyst symbols, blind ontology-recovery scoring, and comparison against earlier opaque notation.

## Syntactic recovery mistaken for semantic recovery

A model may correctly identify arrows, functions, and non-implications while assigning the wrong object types.

**Control:** score ontology and relation recovery separately. A structurally coherent parse with the wrong ontology is not full decoding success.

## Legend leakage

Providing a symbol legend, CARS provenance, expected ontology labels, or prior interpretations turns a blind-decoding test into a guided explanation test.

**Control:** keep blind conditions free of external legend/provenance and record exactly what context the model received.

## Rubric leakage through the question

A decoding prompt can accidentally name the distinctions it is supposed to test, such as “residual,” “candidate revision,” or “authority.”

**Control:** use neutral decoding instructions and keep expected categories evaluator-side.

## Scoring unencoded structure

Evaluators may penalize a catalyst for failing to recover distinctions the tested variant never encoded.

**Control:** score only the semantic content actually present in the intervention condition.

## Equation/prose confounding

If the frozen catalyst beats controls, the gain may come from the prose semantics rather than the equation, or from the equation's semantic typing rather than the prose.

**Control:** equation-only, semantics-only, full-catalyst, and generic-careful-reasoning conditions.

## Decode/execute conflation

A model may explain the catalyst correctly but fail to use it on tasks.

**Control:** score blind decoding and execution in separate stages.

## Execution/efficacy conflation

A model may follow the catalyst faithfully without improving substantive outcomes.

**Control:** report execution fidelity separately from task performance and correction-capacity measures.

# Architecture-specific threats

## Validation-environment leakage

A supposedly held-out validation world may contain information already available during candidate generation or selection.

**Control:** define the selection-information boundary explicitly and exclude information capable of changing candidate generation or selection from later independent-validation claims.

## Validator tuning after selection

Even when the validation environment is unseen, the validation procedure `𝒱_t` may be chosen or tuned after inspecting candidate revisions.

This creates a self-validating loop:

```text
candidate selection
→ validator tuning
→ favorable validation outcome
```

**Control:** require design-level insulation of both the validation procedure and validation environment from `I_sel,t`, or explicitly downgrade the evidence status.

## Statistical independence confused with design independence

A validation sample can be statistically unrelated yet still be selected or evaluated using knowledge of the candidate.

**Control:** document methodological/design insulation:

```text
(𝒱_t, W_t^ind) ⟂_design I_sel,t
```

rather than asserting unsupported probabilistic independence.

## Adaptive holdout reuse

A validation benchmark may be independent for one transition but become selection information for later transitions once its results are observed.

**Control:** treat exposed validation evidence as part of later selection history. Use renewable validation environments and a separate audit layer for lineage-level claims.

## Recursive lineage overfitting

Repeated successor selection can gradually optimize the lineage to a finite family of validation environments even when each local step appears clean.

**Control:** fresh validation environments, cross-generator transfer, and final audit cases unavailable to the lineage.

## CorrCap gaming

A correction-capacity metric may reward proxies such as verbosity, intervention count, uncertainty declarations, representation changes, or abstention.

**Control:** negative-control worlds, restraint scoring, matched-cost conditions, and construct-validity tests for the metric itself.

## Construct/metric collapse

The theory may implicitly treat `CorrCap` as identical to the higher-level `C_improve` construct it is intended to operationalize.

**Control:** preserve:

```text
C_improve ≠ CorrCap
```

and test whether CorrCap tracks independent indicators of future correctability rather than only theory-selected proxies.

## Global-average dilution

A successor may improve average performance while remaining worse on the residual that triggered revision.

**Control:** require residual-local reporting rather than relying only on aggregate performance.

## Arbitrary regression tolerance

A successor may be declared acceptable because the tolerated regression threshold was chosen after outcomes were seen.

**Control:** predeclare non-inferiority or material-regression margins before validation.

## Successor regression

A revision can repair the triggering residual while damaging previously reliable correction behavior.

**Control:** regression suites over unaffected cases and explicit tradeoff reporting. Local improvement is not sufficient for unrestricted adoption.

## False dependency discovery

Conditions present during successful correction may be mistaken for necessary dependencies.

**Control:** removal, perturbation, substitution, and transfer tests; include incidental and redundant conditions.

## Spurious functional equivalence

Two implementations may appear substitutable in a narrow test while differing on hidden or later-relevant functions.

**Control:** validate substitution over the declared function and transfer scope; do not promote local substitutability into universal equivalence.

## Benchmark-generator dependence

Success across many instances from one generator may reflect adaptation to the generator rather than general correction capacity.

**Control:** independently authored generators, structurally different task families, and external or natural failure cases where feasible.

## Invalid self-certification

Because `Φ_t`, `G_t`, and `𝒱_t` may themselves be revised, the architecture can accidentally let a revised evaluator certify its own validity.

**Control:** the object being revised must not supply the sole authority for its successor. Apply the same leave/adopt separation and design-independent validation requirement to correction-surface revisions.

## Falsification target

The strongest adversarial objective is:

> **Construct conditions under which CARS appears to earn correction authority without actually increasing independently validated correction capacity.**

If such conditions reliably manufacture positive results, the authority architecture has failed even if ordinary task performance looks impressive.
# Evaluation Threat Model

CARS can appear successful for reasons unrelated to the intended capability. This document lists major threats to both prompt-level evaluation and the newer recursive correction architecture.

## Prompt-length advantage

A longer prompt may simply induce more deliberation.

**Control:** length-conscious generic reasoning baseline.

## Vocabulary leakage

Tasks written using terms such as "authority laundering," "departure vs adoption," or the notebook's own architecture vocabulary may reward memorizing the intervention.

**Control:** held-out surface language, independent case authorship, and cases that do not name the hidden failure class.

## Judge preference

LLM or human judges may prefer cautious, structured prose even when task performance is unchanged.

**Control:** outcome-based scoring, blinded ratings, behavioral follow-up, and explicit penalties for unnecessary interventions.

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

**Control:** matched worlds in which shallow repair is sufficient, plus explicit false-escalation scoring.

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

Internally authored tasks may encode the same worldview as the prompt or research notes.

**Control:** external authors, structurally independent task sources, adversarial benchmark design, and cross-generator evaluation.

## Model-specific prompt interaction

CARS may exploit instruction-following tendencies of one model family.

**Control:** cross-model evaluation.

## Post-outcome prompt tuning

Changing the intervention after seeing failures can overfit a test suite and make results hard to interpret.

**Control:** when reporting an experiment, record the exact prompt version or commit that produced the result. Use a new version label for substantive post-outcome changes when comparison matters.

## Narrative masking

A model may use CARS terminology correctly while making the same substantive error.

**Control:** score behavior, predictions, interventions, and later transfer rather than protocol recitation.

## Validation-environment leakage

A supposedly held-out validation world may contain information already available during candidate generation or selection.

**Control:** define the selection-information boundary explicitly and exclude any information capable of changing candidate generation or selection from later independent-validation claims.

## Validator tuning after selection

Even when the validation environment is unseen, the validation procedure `𝒱_t` may be chosen or tuned after inspecting candidate revisions.

This creates a self-validating loop:

```text
candidate selection
→ validator tuning
→ favorable validation outcome
```

**Control:** specify or generate the validation procedure independently of candidate-selection information, or explicitly downgrade the evidence status.

## Statistical independence confused with design independence

The architecture's independence claim is methodological. A validation sample can be statistically unrelated yet still be selected using knowledge of the candidate.

**Control:** document procedural/design insulation rather than asserting unsupported probabilistic independence.

## Adaptive holdout reuse

A validation benchmark may be independent for one transition but become training information for later transitions once its results are observed.

**Control:** treat exposed validation evidence as part of later selection history. Use renewable held-out environments and a separate audit layer for lineage-level claims.

## Recursive lineage overfitting

Repeated successor selection can gradually optimize the entire lineage to a finite family of validation environments even when each local step looks clean.

**Control:** fresh validation environments over time, cross-generator transfer, and final audit cases unavailable to the lineage.

## CorrCap gaming

A correction-capacity metric may reward proxies such as verbosity, intervention count, uncertainty declarations, representation changes, or abstention.

**Control:** negative-control worlds, explicit restraint scoring, matched-cost conditions, and construct-validity tests for the metric itself.

## Global-average dilution

A successor may improve average performance while remaining worse on the residual that triggered revision.

**Control:** require residual-local reporting and succession evidence rather than relying only on aggregate performance.

## Arbitrary regression tolerance

A successor may be declared acceptable because the tolerated regression threshold was chosen after outcomes were seen.

**Control:** predeclare non-inferiority margins or other material-harm tolerances before validation.

## Successor regression

A revision can repair the triggering residual while destroying previously reliable correction behavior.

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

**Control:** the object being revised must not supply the sole authority for its successor. Apply the same departure/adoption separation and independent-validation requirement to correction-surface revisions.

## Falsification target

The strongest adversarial objective is:

> **Construct conditions under which CARS appears to earn correction authority without actually increasing independently validated correction capacity.**

If such conditions reliably manufacture positive results, the authority architecture has failed even if ordinary task performance looks impressive.
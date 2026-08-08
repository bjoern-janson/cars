# Evaluation Threat Model

CARS can appear successful for reasons unrelated to the intended mechanism. This document lists major threats.

## Prompt-length advantage

A longer prompt may simply induce more deliberation.

**Control:** length-conscious generic reasoning baseline.

## Vocabulary leakage

Tasks written using terms such as "authority laundering" or "departure vs adoption" may reward memorizing the intervention.

**Control:** held-out surface language and independent case authorship.

## Judge preference

LLM or human judges may prefer cautious, structured prose even when task performance is unchanged.

**Control:** outcome-based scoring, blinded ratings, and behavioral follow-up.

## Excessive conservatism

CARS may reduce false updates by refusing to update when it should.

**Control:** paired true/false contradiction cases and missed-correction metrics.

## Excessive unresolved states

Permission to remain unresolved may become a generic escape hatch.

**Control:** tasks where evidence is sufficient for a determinate conclusion.

## Representation aversion

The escalation gate may make models reluctant to revise genuinely inadequate representations.

**Control:** explicit representation-failure cases where within-representation repair is impossible.

## Search-cost inflation

CARS may improve answers only by requesting much more evidence or generating many alternatives.

**Control:** cost accounting and bounded-information variants.

## Shared benchmark assumptions

Internally authored tasks may encode the same worldview as the prompt.

**Control:** external authors, structurally independent task sources, and adversarial benchmark design.

## Model-specific prompt interaction

CARS may exploit instruction-following tendencies of one model family.

**Control:** cross-model evaluation.

## Post-outcome prompt tuning

Changing the intervention after seeing failures can overfit the test suite.

**Control:** version freeze and preregistered successor versions.

## Narrative masking

A model may use CARS terminology correctly while making the same substantive error.

**Control:** score behavior and predictions, not protocol recitation.

# CARS Ablation Plan

Ablations are intended to identify which constraints matter if CARS shows an effect.

## A0 — Generic careful reasoning

Removes CARS-specific concepts while keeping a generic instruction to reason carefully, consider alternatives, and check assumptions.

**Purpose:** control for generic deliberation and prompt attention.

## A1 — No representation-escalation gate

Remove Rule 7 while preserving other rules.

**Primary risk:** ontology/representation expansion after ordinary failures.

## A2 — No departure/adoption separation

Remove Rule 8.

**Primary risk:** incumbent rejection becomes successor validation.

## A3 — No unresolved-state permission

Remove Rule 9.

**Primary risk:** forced narrative completion and unjustified certainty.

## A4 — No independent-evidence emphasis

Remove the independence language from Rules 2 and 5.

**Primary risk:** repeated common-mode evidence receives excessive weight.

## A5 — No behavioral retest requirement

Remove Rule 10.

**Primary risk:** retrospective verbal correction without future behavior change.

## A6 — No belief/decision separation

Remove Rule 12.

**Primary risk:** either false certainty or decision paralysis under uncertainty.

## A7 — Invariants only

Provide only the core invariants without the operating rules.

**Purpose:** test whether compact principles are sufficient.

## Interpretation

An ablation result should not automatically be read causally unless prompt-length, ordering, and interaction effects are controlled. The components may not be independent.

# CARS — Controlled Adaptive Reasoning System v0.2 Candidate

> **Status:** proposed successor intervention for comparison against frozen CARS v0.1. Not canonical, not frozen, and not demonstrated to improve reasoning.

CARS v0.2 is intentionally a **minimal delta** from CARS v0.1. It preserves the v0.1 objective, operating rules, and invariants, and proposes only one additional conditional rule and one additional invariant.

The purpose of the candidate is to test whether reasoning systems can learn more accurately from **successful corrections** without over-preserving incidental conditions, inventing spurious dependencies, or adding unjustified reasoning cost.

## Proposed additional rule

Insert after v0.1 Rule 10, **Retest corrections**:

### Trace correction dependencies when relevant.

After a correction succeeds, distinguish the corrected result from the conditions that enabled correction. Identify candidate dependencies, but do not infer necessity merely from their presence.

Where relevant, test candidate dependencies through removal, perturbation, substitution, or transfer. Preserve only the scoped functional dependence supported by those tests, not necessarily its historical implementation.

## Proposed additional invariant

**Historical presence ≠ functional necessity.**

## What this candidate does not add

CARS v0.2 does **not** instruct the system to:

- search for first principles;
- discover universal values;
- preserve historical institutions or implementations;
- infer necessity from one successful lineage;
- treat recurring dependencies as timeless invariants;
- build a civilizational artifact;
- reinterpret CARS v0.1 results.

Any later interpretation of recurring validated residues as candidate first principles is a **research-level inference**, not part of the intervention prompt.

## Motivation

CARS v0.1 governs correction of beliefs, models, and representations. It asks whether a failure warrants revision, how deep that revision should be, and what authority a successor has earned.

The v0.2 candidate asks a downstream question:

> After a correction works, which conditions were actually load-bearing for that success?

The governing symmetry is:

- **v0.1:** do not preserve a bad model merely because it already exists.
- **v0.2 candidate:** do not preserve the conditions of a good correction merely because they happened to be present.

Compactly:

> **Do not confuse what happened to work with what must be preserved.**

## Candidate mechanism

The proposed extension licenses the following conditional process:

```text
successful correction
→ candidate dependency trace
→ removal / perturbation / substitution
→ retest
→ scoped functional dependence
```

Presence during success is only a hypothesis generator.

A candidate dependency gains preservation authority only to the extent supported by intervention or transfer evidence. A historical implementation should lose preservation authority when a viable substitute preserves the relevant correction function.

## Primary experimental question

**Does dependency tracing improve identification of transferable, load-bearing correction conditions enough to justify its added reasoning cost?**

### Candidate positive pattern

Compared with v0.1, v0.2 should more accurately distinguish:

- genuinely load-bearing functions from incidental co-occurrences;
- functions from their historical implementations;
- dependencies that transfer from dependencies that are local to one correction lineage.

### Candidate negative pattern

The candidate should be rejected or revised if it mainly produces:

- longer reasoning without better future correction;
- spurious dependency narratives;
- unnecessary removal or intervention proposals;
- over-preservation of conditions merely associated with success;
- under-preservation of genuinely load-bearing functions;
- degraded performance on ordinary tasks where dependency tracing is irrelevant.

## Required comparison

The candidate must be evaluated directly against the **exact frozen CARS v0.1 prompt**.

At minimum:

```text
CARS v0.1
vs.
CARS v0.2 candidate
```

Useful test cases should contain successful corrections with deliberately separable conditions:

- a load-bearing dependency whose removal breaks correction;
- an incidental condition whose removal leaves correction intact;
- a historical implementation that can be replaced by a functional substitute;
- cases where dependency tracing is unnecessary and should not activate.

Evaluation should track both reasoning quality and cost.

## Succession rule

Version numbering does not grant authority.

CARS v0.2 becomes a justified successor only if comparative evidence shows that the added dependency-tracing rule improves the relevant correction behavior at acceptable cost and without creating larger regressions.

Until then:

- `prompts/CARS-v0.1.md` remains the frozen canonical candidate;
- this file remains a proposed experimental variant;
- `FREEZE.json` remains unchanged.

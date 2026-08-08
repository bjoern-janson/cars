# CARS — Controlled Adaptive Reasoning System

> **Status:** candidate reasoning intervention, not an established theory or demonstrated performance improvement.

CARS is a compact reasoning protocol for situations where uncertainty, contradiction, causal ambiguity, representation failure, hidden dependency, or failed transfer materially affects the problem.

Its core objective is simple:

```text
feedback → localized correction → better adaptation → greater correction capacity
```

CARS treats **correction quality** as a research target. It does not assume that correction means changing the representation. Representation change is an escalation path that must itself be justified.

## Central research question

**Does a structured reasoning protocol improve controlled adaptation relative to baseline and generic careful-reasoning controls, without increasing over-revision, premature representation change, or unjustified confidence?**

## What CARS is trying to prevent

CARS is designed around recurring reasoning failures:

- updating at the wrong depth;
- treating a possibility as evidence for itself;
- overgeneralizing beyond the scope of evidence;
- laundering validity into causal, mechanistic, provenance, or predictive authority;
- counting correlated confirmation as independent validation;
- replacing an incumbent merely because it was challenged;
- forcing a determinate answer when unresolved is warranted;
- producing a better retrospective explanation without changing future behavior.

## The frozen candidate prompt

The canonical v0.1 candidate is in [`prompts/CARS-v0.1.md`](prompts/CARS-v0.1.md).

Do not silently modify that file during an evaluation. New variants should receive a new version.

## Repository map

```text
prompts/
  CARS-v0.1.md              Frozen candidate intervention

docs/
  RESEARCH_CONTRACT.md      Primary question, hypotheses, outcomes, claim boundary
  DESIGN_RATIONALE.md       Why each constraint exists
  CLAIMS_AND_NONCLAIMS.md   What evidence may and may not establish
  FAILURE_MODEL.md          Failure classes CARS is intended to handle
  EVALUATION_PROTOCOL.md    Comparison design and anti-leakage rules
  ABLATIONS.md              Component-removal tests
  THREAT_MODEL.md           Ways a CARS evaluation can fool itself
  PROVENANCE.md             Research and AI-assisted workflow disclosure
benchmarks/
  seed_cases.jsonl          Internal seed cases, not yet independent evidence
  README.md                 Case schema and benchmark status

eval/
  SCORING.md                Human-readable scoring rubric
  rubric.json               Machine-readable rubric dimensions
scripts/
  validate_cases.py         Schema and integrity checker
examples/
  evaluation_record.json    Example result record
```

## Research ladder

CARS should be evaluated in layers rather than treated as successful because it sounds coherent.

1. **Instruction adherence** — does the model actually follow the protocol?
2. **Reasoning quality** — does it improve localization, scope control, discrimination, and calibration?
3. **Correction behavior** — does a correction change later reasoning or action where relevant?
4. **Transfer** — do gains survive held-out domains and structurally different tasks?
5. **Cost** — what latency, token, search, or decision penalties does CARS impose?
6. **Failure analysis** — where does CARS make reasoning worse?

A valid negative result is a valid result.

## Primary comparison

A serious test should compare at least:

- **B0 — Baseline:** model without CARS.
- **B1 — Generic careful-reasoning control:** a length-matched instruction to reason carefully, consider alternatives, and check work without CARS-specific machinery.
- **CARS — Frozen candidate:** exact prompt in `prompts/CARS-v0.1.md`.

Optional ablations test whether any observed benefit depends on specific CARS components rather than prompt length or generic deliberation.

## Core invariants

> **Possibility space ≠ epistemic authority space.**

> **Search allocates attention; evidence allocates authority.**

> **Evidence can authorize departure without authorizing destination.**

> **Never make the current interface final; never make its successor self-authorizing.**

## Evidence status

This repository currently provides a **candidate intervention and internal evaluation scaffold**.

It does **not** establish that CARS:

- improves reasoning;
- improves safety;
- improves calibration;
- increases intelligence;
- causes better adaptation;
- generalizes across models or domains;
- solves representation invention or Controlled Representational Escape.

The seed benchmark is internally authored and therefore suitable for development, debugging, and preregistration design—not independent validation.

## Relationship to adjacent work

CARS is separate from, but informed by, a broader research trajectory around correction, representation adequacy, and adaptive evaluation.

- **The Correctable Lineage:** governance of scope, provenance, authority, and reopening.
- **Negative-Space Search:** when representation search should expand.
- **MAGIKARP:** whether prospective failure-depth diagnosis predicts held-out recovery under supplied correction mechanisms.
- **CARS:** a candidate reasoning intervention intended to improve controlled adaptation.

Success or failure of CARS does not retroactively validate or invalidate those other artifacts.

## Authorship and workflow

Research direction, conceptual architecture, claims, and evaluation priorities are directed by **Björn Janson**. AI systems are used as research collaborators and implementation tools for drafting, critique, repository construction, comparison, and code assistance. See [`docs/PROVENANCE.md`](docs/PROVENANCE.md).

## License

MIT. See [`LICENSE`](LICENSE).

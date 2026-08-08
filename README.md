# CARS — Controlled Adaptive Reasoning System

> **Status:** living research notebook and candidate reasoning intervention. Nothing here should be treated as an established theory or demonstrated performance improvement.

CARS is an evolving reasoning protocol for situations where uncertainty, contradiction, causal ambiguity, representation failure, hidden dependency, or failed transfer materially affects the problem.

Its core objective is simple:

```text
feedback → localized correction → better adaptation → greater correction capacity
```

CARS treats **correction quality** as a research target. It does not assume that correction means changing the representation. Representation change is an escalation path that must itself be justified.

## Central research question

**Does a structured reasoning protocol improve controlled adaptation relative to baseline and generic careful-reasoning controls, without increasing over-revision, premature representation change, or unjustified confidence?**

## Notebook philosophy

This repository is meant to preserve the thread of the research while allowing it to change.

- Prompt versions are reference snapshots, not sacred artifacts.
- Git history provides provenance for changes.
- New ideas can live beside older versions before they are tested.
- Experiments should record the exact prompt/version used when outcomes matter.
- Stronger release or preregistration discipline can be added later when a specific experiment requires it.

The goal is to keep the research **reopenable without making iteration expensive**.

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

## Prompt versions

[`prompts/CARS-v0.1.md`](prompts/CARS-v0.1.md) is the first reference snapshot.

[`prompts/CARS-v0.2-CANDIDATE.md`](prompts/CARS-v0.2-CANDIDATE.md) explores one narrow extension: tracing dependencies of successful corrections. It adds the invariant:

> **Historical presence ≠ functional necessity.**

Version numbers organize the notebook; they do not imply that a later version is better. When comparing versions experimentally, record the exact files used.

## Repository map

```text
prompts/
  CARS-v0.1.md              First reference prompt snapshot
  CARS-v0.2-CANDIDATE.md    Dependency-tracing experimental variant
  GENERIC-CONTROL-v0.1.md   Generic careful-reasoning comparison control

docs/
  RESEARCH_CONTRACT.md      Primary question, hypotheses, outcomes, claim boundary
  DESIGN_RATIONALE.md       Why each constraint exists
  CLAIMS_AND_NONCLAIMS.md   What evidence may and may not establish
  FAILURE_MODEL.md          Failure classes CARS is intended to handle
  EVALUATION_PROTOCOL.md    Suggested comparison design and anti-leakage rules
  EXPERIMENT_MATRIX.md      Suggested experiment families
  ABLATIONS.md              Component-removal ideas
  THREAT_MODEL.md           Ways a CARS evaluation can fool itself
  INDEPENDENT_CASE_AUTHOR_BRIEF.md
                            Brief for independently authored cases
  PROVENANCE.md             Research and AI-assisted workflow disclosure
benchmarks/
  seed_cases.jsonl          Internal seed cases, not independent evidence
  README.md                 Case schema and benchmark status

eval/
  SCORING.md                Human-readable scoring rubric
  rubric.json               Machine-readable rubric dimensions
scripts/
  validate_cases.py         Seed-case schema and integrity checker
examples/
  evaluation_record.json    Example result record
results/
  README.md                 Place for future results
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

## Useful comparisons

A serious v0.1 test could compare:

- **B0 — Baseline:** model without CARS.
- **B1 — Generic careful-reasoning control:** a length-conscious instruction to reason carefully, consider alternatives, and check work without CARS-specific machinery.
- **CARS v0.1:** exact prompt in `prompts/CARS-v0.1.md`.

A v0.2 experiment can compare v0.1 directly with the dependency-tracing variant. Its narrower question is:

> **Does dependency tracing improve identification of transferable, load-bearing correction conditions enough to justify its added reasoning cost?**

These are experiment ideas, not repository governance requirements.

## Core invariants

> **Possibility space ≠ epistemic authority space.**

> **Search allocates attention; evidence allocates authority.**

> **Evidence can authorize departure without authorizing destination.**

> **Never make the current interface final; never make its successor self-authorizing.**

The v0.2 candidate adds:

> **Historical presence ≠ functional necessity.**

## Evidence status

This repository currently provides **candidate interventions, notes, and an internal evaluation scaffold**.

It does **not** establish that CARS:

- improves reasoning;
- improves safety;
- improves calibration;
- increases intelligence;
- causes better adaptation;
- generalizes across models or domains;
- solves representation invention or Controlled Representational Escape;
- discovers transferable correction dependencies;
- identifies first principles.

The seed benchmark is internally authored and therefore useful for development and debugging, not independent validation.

## Relationship to adjacent work

CARS is separate from, but informed by, a broader research trajectory around correction, representation adequacy, and adaptive evaluation.

- **The Correctable Lineage:** governance of scope, provenance, authority, and reopening.
- **Negative-Space Search:** when representation search should expand.
- **MAGIKARP:** whether prospective failure-depth diagnosis predicts held-out recovery under supplied correction mechanisms.
- **CARS:** candidate reasoning interventions for controlled adaptation.

Success or failure of CARS does not retroactively validate or invalidate those other artifacts.

## Authorship and workflow

Research direction, conceptual architecture, claims, and evaluation priorities are directed by **Björn Janson**. AI systems are used as research collaborators and implementation tools for drafting, critique, repository construction, comparison, and code assistance. See [`docs/PROVENANCE.md`](docs/PROVENANCE.md).

## License

MIT. See [`LICENSE`](LICENSE).

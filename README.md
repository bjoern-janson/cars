# CARS — Controlled Adaptive Reasoning System

> **Status:** living research notebook containing candidate reasoning interventions, a frozen catalyst candidate for testing, and a proposed recursive correction architecture. Nothing here should be treated as an established theory, demonstrated performance improvement, validated intelligence definition, or validated self-improving system.

CARS studies a simple question with increasingly demanding forms:

```text
Can feedback produce a correction that improves future correction?
```

The current research frontier is:

> **Can a reasoning system discover when its own representation or correction process is the limiting factor, propose a successor without self-authorizing it, and earn adoption through evidence insulated from the process that selected that successor?**

## Current research posture

The notebook is now intentionally in a **test-before-refine** state.

```text
freeze
→ blind test
→ measure decoding
→ measure correction
→ revise only if evidence warrants
```

Prompt snapshots remain unchanged. The current catalyst is frozen as an exact intervention for the next decoding/execution tests. The formal architecture remains a hypothesis to be attacked, not a theory to be protected.

A valid negative result is a valid result.

## Three research surfaces

CARS now keeps three experimental surfaces distinct:

```text
prompt intervention
≠ catalyst intervention
≠ recursive architecture
```

### Prompt intervention

Tests whether explicit CARS reasoning instructions improve controlled adaptation relative to baselines.

### Catalyst intervention

Tests whether a compact semantically typed intervention can be recovered and executed without requiring the model to reconstruct the entire theory.

### Recursive architecture

Tests whether correction-surface revisions can earn succession authority through design-independent validation, residual-local correction gain, and regression control.

Evidence at one level does not automatically validate the others.

## Canonical representation stack

```text
Catalyst activates
→ Formalism constrains
→ Semantics executes
```

The layers optimize different things:

```text
formal notation = representation
catalyst notation = intervention
execution semantics = operational instruction
```

See [`notes/2026-08-08-catalyst-notation.md`](notes/2026-08-08-catalyst-notation.md).

## Frozen deployable catalyst

The current exact catalyst candidate is:

```text
I ∝ C_improve
I = intelligence; C_improve = capacity to convert feedback into increased future viability.
E_evidence,lim → C_revision; ρ_res = Φ_res(E); V_val^ind = 𝒱(R_candidate; W_val^ind); A_leave ↛ A_adopt; ΔCorrCap_ρres > 0.
Feedback reveals a limitation → represent the residual provisionally → generate candidate revisions → independently validate them → do not infer successor authority from authority to leave the incumbent → adopt only when the successor demonstrates greater correction capacity on the residual that triggered revision.
```

This is a **candidate catalyst**, not an empirical law.

In particular:

```text
I ∝ C_improve
```

is a research objective / framing, not an established definition of intelligence.

The construct and operational measure remain distinct:

```text
C_improve ≠ CorrCap
```

`C_improve` is the higher-level capacity to convert feedback into increased future correctability / viability. `CorrCap` is an operational measurement target whose construct validity must be tested.

## Formal recursive architecture

The full architecture is documented in [`notes/2026-08-08-recursive-correction-architecture.md`](notes/2026-08-08-recursive-correction-architecture.md).

Let:

```text
X_t = (C_t, O_t, M_t, Φ_t, G_t, 𝒱_t, …)
```

where the correction procedure, observation/interface, model, residual mapper, candidate generator, and validation procedure are all potentially revisable.

The current residual representation is:

```text
ρ_t = Φ_t(E_t)
```

Crucially:

```text
ρ_t ≠ ρ*
```

is permitted. The residual representation is provisional; it is not assumed to be the true hidden failure class.

The compact succession architecture is:

```text
X_t
  --(E_t, Φ_t)--> ρ_t
  --G_t--> R_cand,t
  --(𝒱_t, W_t^ind)--> V_t^ind
  --[A_leave ↛ A_adopt; Ind_t = 1]--> X_{t+1}
```

subject to residual-local improvement:

```text
ΔCorrCap_{ρ_t} > 0
```

and, where unrestricted succession is claimed, regression control on unaffected behavior.

## Independent validation

The validation procedure and validation outcome are different objects:

```text
𝒱_t := validation procedure
V_t^ind := 𝒱_t(R_cand,t ; W_t^ind)
```

An unseen validation environment is not enough if the validation procedure itself was tuned after candidate selection.

Let:

```text
I_sel,t := all information capable of influencing candidate generation or selection
```

The strong independence condition is design-level:

```text
(𝒱_t, W_t^ind) ⟂_design I_sel,t
```

Practical rule:

> **If information could have changed which revision was generated or selected, it cannot later be counted as independent validation evidence for that revision.**

## Authority firewall

A central invariant is:

```text
A_leave ↛ A_adopt
```

Evidence sufficient to withdraw authority from an incumbent does not automatically grant authority to a successor.

This applies not only to models, but to representations, residual mappings, candidate generators, validators, and correction procedures themselves.

## Prompt track

[`prompts/CARS-v0.1.md`](prompts/CARS-v0.1.md) is the first reference prompt snapshot.

[`prompts/CARS-v0.2-CANDIDATE.md`](prompts/CARS-v0.2-CANDIDATE.md) is a narrow experimental variant that asks whether successful corrections should trigger dependency tracing. It adds one candidate invariant:

> **Historical presence ≠ functional necessity.**

It does **not** instruct the model to search for first principles, universal functions, or recursive self-modification.

Version numbers organize experimental variants; they do not imply epistemic superiority.

## Core research invariants

> **Possibility space ≠ epistemic authority space.**

> **Search allocates attention; evidence allocates authority.**

> **Evidence can authorize departure without authorizing destination.**

> **Historical presence ≠ functional necessity.** *(v0.2 candidate)*

> **Resolution is not explanatory authority.** *(research note; not a prompt rule)*

No correction-surface component receives epistemic immunity merely because it is part of the current architecture.

## What CARS is trying to prevent

Recurring failure modes include:

- updating at the wrong depth;
- treating possibility as evidence for itself;
- overgeneralizing beyond evidence-supported scope;
- laundering validity into causal, mechanistic, provenance, predictive, or future-reliability authority;
- counting common-mode confirmation as independent validation;
- treating incumbent failure as successor validation;
- forcing determinate conclusions when unresolved is warranted;
- producing retrospective explanation without changed future behavior;
- confusing historical participation with functional necessity;
- granting explanatory authority to representations that collapse the required distinction;
- treating the current residual partition as truth;
- tuning validation after candidate selection and then calling it independent;
- hiding failure on the triggering residual behind global average improvement;
- optimizing the correction metric rather than correction capacity itself.

See [`docs/FAILURE_MODEL.md`](docs/FAILURE_MODEL.md) and [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md).

## Evaluation stack

The evaluation protocol is in [`docs/EVALUATION_PROTOCOL.md`](docs/EVALUATION_PROTOCOL.md).

Use distinct scoring surfaces:

- [`eval/SCORING.md`](eval/SCORING.md) and [`eval/rubric.json`](eval/rubric.json) — prompt-level reasoning;
- [`eval/CATALYST_SCORING.md`](eval/CATALYST_SCORING.md) — catalyst decoding and execution;
- [`eval/ARCHITECTURE_SCORING.md`](eval/ARCHITECTURE_SCORING.md) — recursive architecture behavior.

Keep the evidence ladder explicit:

```text
semantic recovery
↛ faithful execution
↛ task improvement
↛ CorrCap improvement
↛ recursive improvement
```

A single aggregate should not erase these distinctions.

## Current empirical sequence

The next high-information work is empirical rather than conceptual.

### 1. Blind catalyst decoding

Test whether unfamiliar models recover the intended operational ontology without receiving the CARS legend, repository provenance, expected labels, or prior parses.

Useful comparison conditions include:

- typed equation only;
- execution semantics only;
- frozen deployable catalyst;
- older opaque notation;
- generic reasoning control for execution tests.

### 2. Catalyst execution

Test whether semantic recovery translates into the intended correction behavior on fresh tasks.

### 3. Recursive architecture stress test

Construct worlds where the architecture can appear to earn succession authority without genuinely improving independently validated correction capacity.

Strong benchmark families should include:

- shallow repair sufficient;
- representation non-identifiability;
- wrong residual partition;
- candidate-generation failure;
- validator contamination;
- incidental dependency;
- substitutable implementation;
- correction-procedure failure;
- no-escalation negative controls;
- successor regression;
- adaptive holdout contamination;
- cross-generator transfer.

See [`docs/EXPERIMENT_MATRIX.md`](docs/EXPERIMENT_MATRIX.md).

## Evidence status

This repository currently provides **candidate interventions, formal hypotheses, internally generated notes, and evaluation scaffolding**.

It does **not** establish that CARS:

- improves reasoning or safety;
- increases intelligence;
- validates `I ∝ C_improve` as a law or definition;
- validates `CorrCap` as a measure of the full `C_improve` construct;
- discovers novel representations autonomously;
- identifies the true residual or causal decomposition;
- improves its own correction procedure;
- validates successors independently in practice;
- improves correction capacity;
- recursively improves across environments;
- discovers universal correction functions or first principles;
- solves Controlled Representational Escape or alignment.

The current seed suite is internally authored and is development evidence only.

See [`docs/CLAIMS_AND_NONCLAIMS.md`](docs/CLAIMS_AND_NONCLAIMS.md) and [`docs/PROVENANCE.md`](docs/PROVENANCE.md).

## Notebook philosophy

This repository preserves a research lineage while keeping revision cheap enough to remain corrigible.

- Prompt versions are reference snapshots, not sacred artifacts.
- Notes may advance without changing prompts.
- Git history provides default provenance.
- Exact intervention text and evaluation context should be recorded when results matter.
- Stronger preregistration/release discipline should be added when the evidential claim warrants it.
- Internally coherent artifacts are not independent evidence for one another.
- Further refinement should be driven by observed failure once the current object is testable.

The goal is to remain **reopenable, testable, and corrigible without confusing notebook evolution with empirical progress**.

## Repository map

```text
prompts/
  CARS-v0.1.md
  CARS-v0.2-CANDIDATE.md
  GENERIC-CONTROL-v0.1.md

notes/
  2026-08-08-one-layer-enough.md
  2026-08-08-typed-attribution.md
  2026-08-08-representation-authority.md
  2026-08-08-recursive-correction-architecture.md
  2026-08-08-catalyst-notation.md

docs/
  RESEARCH_CONTRACT.md
  DESIGN_RATIONALE.md
  CLAIMS_AND_NONCLAIMS.md
  FAILURE_MODEL.md
  EVALUATION_PROTOCOL.md
  EXPERIMENT_MATRIX.md
  ABLATIONS.md
  THREAT_MODEL.md
  INDEPENDENT_CASE_AUTHOR_BRIEF.md
  PROVENANCE.md

benchmarks/
  seed_cases.jsonl
  README.md

eval/
  SCORING.md
  CATALYST_SCORING.md
  ARCHITECTURE_SCORING.md
  rubric.json

scripts/
  validate_cases.py

examples/
  evaluation_record.json

results/
  README.md
```

## Relationship to adjacent work

CARS is separate from, but informed by, a broader research trajectory around correction, representation adequacy, and adaptive evaluation.

- **The Correctable Lineage:** governance of scope, provenance, authority, and reopening.
- **Negative-Space Search:** when representation search should expand.
- **MAGIKARP:** whether prospective failure-depth diagnosis predicts held-out recovery under supplied correction mechanisms.
- **CARS:** candidate reasoning interventions and a notebook architecture for studying controlled correction.

Success or failure of CARS does not retroactively validate or invalidate those other artifacts.

## Authorship and workflow

Research direction, conceptual architecture, claims, and evaluation priorities are directed by **Björn Janson**. AI systems are used as research collaborators and implementation tools for drafting, critique, repository construction, comparison, code assistance, formalization, and adversarial development.

AI-assisted agreement is not independent scientific validation. See [`docs/PROVENANCE.md`](docs/PROVENANCE.md).

## License

MIT. See [`LICENSE`](LICENSE).
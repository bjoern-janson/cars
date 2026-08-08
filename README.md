# CARS — Controlled Adaptive Reasoning System

> **Status:** living research notebook and candidate reasoning intervention. Nothing here should be treated as an established theory, demonstrated performance improvement, or validated self-improving architecture.

CARS studies a simple question with increasingly demanding forms:

```text
Can feedback produce a correction that improves future correction?
```

The original prompt work focuses on controlled reasoning under uncertainty, contradiction, representation failure, hidden dependency, and failed transfer. The current notebook frontier asks a harder question:

> **Can a system discover when its own representation or correction machinery is the limiting factor, propose a successor without self-authorizing it, and earn adoption through independent validation?**

The repository deliberately separates **prompt interventions** from **research architecture**. New conceptual work does not automatically become a new CARS prompt.

## Notebook philosophy

This repository preserves a research lineage while keeping iteration cheap.

- Prompt versions are reference snapshots, not sacred artifacts.
- Notes may advance the research without changing the intervention.
- Git history provides provenance.
- Experiments should record the exact prompt, code, cases, and evaluation procedure used when results matter.
- Stronger preregistration or release discipline should be added when the evidential claim warrants it.
- A valid negative result is a valid result.

The goal is to remain **reopenable, testable, and corrigible without confusing notebook evolution with empirical progress**.

## Prompt track

[`prompts/CARS-v0.1.md`](prompts/CARS-v0.1.md) is the first reference prompt snapshot.

[`prompts/CARS-v0.2-CANDIDATE.md`](prompts/CARS-v0.2-CANDIDATE.md) is a narrow experimental variant that asks whether successful corrections should trigger dependency tracing. It adds one candidate invariant:

> **Historical presence ≠ functional necessity.**

It does **not** instruct the model to search for first principles, universal functions, or recursive self-modification.

Version numbers organize experimental variants; they do not imply epistemic superiority.

## Current research architecture

The latest notebook synthesis is recorded in [`notes/2026-08-08-recursive-correction-architecture.md`](notes/2026-08-08-recursive-correction-architecture.md).

Let

```text
X_t = (C_t, O_t, M_t, Φ_t, G_t, 𝒱_t, …)
```

where the correction procedure, observation/interface, model, residual mapper, candidate generator, and validation procedure are all potentially revisable.

The residual encountered at time `t` is represented as:

```text
ρ_t = Φ_t(E_t)
```

Crucially, `ρ_t` is the **current representation of the residual**, not the discovered truth. `ρ_t ≠ ρ*` is an admissible possibility.

The compact succession architecture is:

```text
X_t
  --(E_t, Φ_t)--> ρ_t
  --G_t--> R_cand,t
  --(𝒱_t, W_t^ind)--> V_t^ind
  --[Ind_t = 1; A_leave ≠> A_adopt]--> X_{t+1}
```

subject to:

```text
ΔCorrCap_{ρ_t} > 0
```

The intended meaning is:

1. represent the newly observed residual;
2. generate candidate revisions;
3. do not treat evidence against the incumbent as evidence for a successor;
4. validate using a protocol insulated from candidate-selection information;
5. adopt only when the complete successor improves correction capacity on the residual that triggered revision.

This architecture is a research hypothesis, not a demonstrated property of CARS.

## Validator vs validation evidence

The notebook distinguishes the validation procedure from its outcome:

```text
𝒱_t := validation procedure
V_t^ind := 𝒱_t(R_cand,t ; W_t^ind)
```

An unseen validation environment is not enough if `𝒱_t` itself was tuned after candidate selection.

Let `I_sel,t` denote all information capable of influencing candidate generation or selection. Protocol-level independence is therefore a design claim:

```text
Ind_t := Ind(𝒱_t, W_t^ind ; I_sel,t) = 1
```

Practical rule:

> **If information could have changed which revision was generated or selected, it cannot later be counted as independent validation evidence for that revision.**

## What CARS is trying to prevent

Across the prompt and research architecture, recurring failure modes include:

- updating at the wrong depth;
- treating a possibility as evidence for itself;
- overgeneralizing beyond evidence-supported scope;
- laundering validity into causal, mechanistic, provenance, or predictive authority;
- counting correlated confirmation as independent validation;
- replacing an incumbent merely because it was challenged;
- forcing a determinate answer when unresolved is warranted;
- producing retrospective explanation without changed future behavior;
- confusing historical participation with functional necessity;
- granting explanatory authority to a representation that collapses the distinction the target claim requires;
- validating a successor with information that influenced its construction;
- hiding failure on the triggering residual behind global average improvement.

## Core invariants

> **Possibility space ≠ epistemic authority space.**

> **Search allocates attention; evidence allocates authority.**

> **Evidence can authorize departure without authorizing destination.**

> **Historical presence ≠ functional necessity.** *(v0.2 candidate)*

> **Resolution is not explanatory authority.** *(research note; not a prompt rule)*

The current architecture adds no new privileged ontology. Even the residual mapper and validation procedure remain revisable research objects.

## Current empirical frontier

The most informative next benchmark is not another prompt extension. It is an adversarial test of whether the authority machinery can be fooled.

Target capabilities include:

- detecting a real correction limit without over-escalating;
- recovering a missing distinction not explicitly supplied by the task ontology;
- discovering when the current representation is non-identifying;
- distinguishing incidental conditions from load-bearing dependencies;
- finding substitutes for historical implementations;
- detecting when the correction procedure itself is the limiting factor;
- validating successors on information unavailable to candidate selection;
- improving correction capacity on the triggering residual without unacceptable regression elsewhere.

The strongest test cases should include worlds where **no deeper revision is required**, so escalation itself cannot become a shortcut.

## Evaluation principles

CARS should be evaluated in layers rather than treated as successful because it sounds coherent.

1. **Instruction adherence** — does the system follow the intervention?
2. **Reasoning quality** — does localization, scope control, discrimination, and calibration improve?
3. **Correction behavior** — does feedback change later reasoning or action where relevant?
4. **Representation adequacy** — can the system notice when its current partition cannot identify the required distinction?
5. **Authority validity** — does adoption depend on evidence insulated from candidate-selection information?
6. **Transfer** — do gains survive held-out domains, mechanisms, authors, and generators?
7. **Regression** — does the successor preserve unaffected correction ability within a predeclared tolerance?
8. **Cost** — what token, latency, search, intervention, or abstention cost is added?
9. **Failure analysis** — where does CARS make reasoning worse or merely game the metric?

`CorrCap` is itself an operational construct that requires validation. More interventions, more uncertainty, more verbosity, or more representation changes must not automatically score as higher correction capacity.

## Adversarial threats

The current architecture should be attacked for:

- validation leakage;
- validator tuning after candidate selection;
- adaptive holdout reuse;
- arbitrary regression tolerance selection;
- CorrCap gaming;
- false representation escalation;
- false dependency discovery;
- spurious functional equivalence;
- benchmark-generator dependence;
- successor regressions;
- recursive lineage overfitting;
- incorrect residual mapping.

See [`docs/THREAT_MODEL.md`](docs/THREAT_MODEL.md).

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
  rubric.json

scripts/
  validate_cases.py

examples/
  evaluation_record.json

results/
  README.md
```

The seed cases are internally authored and are useful for development and debugging, not independent validation.

## Evidence status

This repository currently provides **candidate interventions, research notes, and evaluation scaffolding**.

It does **not** establish that CARS:

- improves reasoning or safety;
- increases intelligence;
- discovers novel representations autonomously;
- identifies the true residual or causal decomposition;
- improves its own correction procedure;
- validates successors independently in practice;
- improves correction capacity;
- recursively improves across environments;
- discovers universal correction functions or first principles;
- solves Controlled Representational Escape or alignment.

Any stronger statement requires evidence matched to its scope.

## Relationship to adjacent work

CARS is separate from, but informed by, a broader research trajectory around correction, representation adequacy, and adaptive evaluation.

- **The Correctable Lineage:** governance of scope, provenance, authority, and reopening.
- **Negative-Space Search:** when representation search should expand.
- **MAGIKARP:** whether prospective failure-depth diagnosis predicts held-out recovery under supplied correction mechanisms.
- **CARS:** candidate reasoning interventions and a notebook architecture for studying controlled correction.

Success or failure of CARS does not retroactively validate or invalidate those other artifacts.

## Authorship and workflow

Research direction, conceptual architecture, claims, and evaluation priorities are directed by **Björn Janson**. AI systems are used as research collaborators and implementation tools for drafting, critique, repository construction, comparison, and code assistance. See [`docs/PROVENANCE.md`](docs/PROVENANCE.md).

## License

MIT. See [`LICENSE`](LICENSE).

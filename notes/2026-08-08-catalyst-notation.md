# Note — Catalyst notation as intervention

> **Status:** current deployable catalyst candidate, frozen for blind decoding and execution tests. This is a research-note freeze point, not repository governance, not a prompt revision, and not a change to the formal recursive architecture.

## Canonical representation stack

```text
Catalyst activates
→ Formalism constrains
→ Semantics executes
```

The three layers optimize different things and should not be collapsed into one representation.

- **Formal architecture:** maximum precision, recursion, auditability, and explicit claim constraints.
- **Catalyst:** minimum compression consistent with blind semantic recovery.
- **Execution semantics:** minimum prose needed to tell a reasoning system what the catalyst operationally requires.

Compactly:

```text
formal notation = representation
catalyst notation = intervention
execution semantics = operational instruction
```

## Frozen deployable catalyst

Use this exact text for the next blind-decoding and execution tests unless the experiment explicitly studies a variant:

```text
I ∝ C_improve
I = intelligence; C_improve = capacity to convert feedback into increased future viability.
E_evidence,lim → C_revision; ρ_res = Φ_res(E); V_val^ind = 𝒱(R_candidate; W_val^ind); A_leave ↛ A_adopt; ΔCorrCap_ρres > 0.
Feedback reveals a limitation → represent the residual provisionally → generate candidate revisions → independently validate them → do not infer successor authority from authority to leave the incumbent → adopt only when the successor demonstrates greater correction capacity on the residual that triggered revision.
```

The first line states the research objective. The second line fixes the two highest-level symbols. The third line is the typed catalyst equation. The fourth line supplies execution semantics without reconstructing the full formal architecture.

`I ∝ C_improve` is a **research objective / candidate framing**, not an established empirical definition of intelligence.

`C_improve` and `CorrCap` must remain distinct:

```text
C_improve
= higher-level capacity to convert feedback into increased future correctability / viability

CorrCap
= operational measurement target used to test correction-capacity claims
```

A metric is not identical to the construct it is intended to measure.

## Formal architecture relation

The catalyst is not the complete formalism. The formal recursive architecture remains in [`2026-08-08-recursive-correction-architecture.md`](2026-08-08-recursive-correction-architecture.md).

In particular, the pocket catalyst abbreviates the stronger protocol-level independence requirement:

```text
(𝒱, W_val^ind) ⟂_design I_sel
```

where `I_sel` contains all information capable of influencing candidate generation or selection.

Practical rule:

> **If information could have changed which revision was generated or selected, it cannot later be counted as independent validation evidence for that revision.**

`⊥_design` denotes methodological/design insulation, not probabilistic independence.

## Design principle

> **Formal notation documents the architecture; catalyst notation activates the architecture.**

The relevant question is not merely whether a reader can understand the notation after receiving a legend. It is whether an unfamiliar reasoner can recover the intended operation before seeing explanatory context.

A catalyst may therefore be slightly less elegant than research notation and still be better at its intended job.

## Blind-decoding criterion

Primary construct-validity target:

```text
DecodeAcc(catalyst)
:= Pr(intended operational structure recovered without legend or CARS provenance)
```

A useful decomposition is:

```text
Decode(catalyst)
=
(D_ontology,
 D_relations,
 D_ordering,
 D_authority)
```

Score at least:

1. **Ontology recovery** — does the reasoner recover limiting evidence, provisional residual, candidate revision, validation, authority separation, and correction capacity rather than importing an unrelated ontology?
2. **Relation recovery** — does it preserve what the relations are doing rather than merely matching symbol shapes?
3. **Ordering recovery** — does it reconstruct the intended process rather than treating the notation as an unordered set of variables?
4. **Authority recovery** — does it preserve `A_leave ↛ A_adopt` rather than converting incumbent failure into successor justification?

Do not score the catalyst against distinctions it does not actually encode.

## First blind-decoding diagnostic

An informal blind parse of an earlier, less semantically typed version recovered much of the relation structure but mapped the ontology into an institutional / exit–voice framework. Symbols such as `E`, `V`, `W`, and `ρ` received plausible but unintended meanings.

The useful diagnostic was:

```text
syntactic / relational recovery
≫
semantic / ontological recovery
```

That is a notation-level failure signal, not evidence against the underlying architecture. It motivated semantic typing of collision-heavy symbols and the current deployable form.

The diagnostic is development evidence only. A single model parse is not a validated estimate of `DecodeAcc`.

## Evaluation sequence

The next information-bearing sequence is:

```text
freeze exact catalyst
→ blind decoding test
→ measure semantic recovery
→ execution test
→ measure downstream correction behavior
→ correction-capacity test
→ revise only if evidence warrants
```

Keep these outcomes separate:

```text
semantic recovery
≠ faithful execution
≠ task improvement
≠ CorrCap improvement
≠ recursive improvement
```

A notation can decode correctly and still fail to improve reasoning. A procedure can execute faithfully and still fail the system-level succession criterion.

## Suggested catalyst controls

A minimal experiment should distinguish at least:

- **equation only** — tests whether typed notation is self-decoding;
- **execution semantics only** — tests whether the prose alone carries the effect;
- **frozen deployable catalyst** — objective definition + typed equation + execution semantics;
- **generic careful-reasoning control** — controls for extra deliberation without CARS-specific structure.

Do not expose the CARS legend, notebook provenance, intended ontology labels, or expected decoding rubric to the model during a blind-decoding condition.

## Stopping rule

```text
freeze
→ blind test
→ measure decoding
→ measure correction
→ revise only if evidence warrants
```

The catalyst itself remains corrigible:

```text
catalyst
→ interpretation
→ observed decoding or execution failure
→ notation revision
→ blind retest
```

But revisions should now be triggered by measured failures rather than aesthetic preference.

## Claim boundary

Successful blind decoding would establish only that the catalyst reliably communicates or activates the intended operational structure under the tested models and conditions.

It would not by itself establish that:

- CARS improves reasoning;
- the activated architecture improves correction capacity;
- semantic recovery implies faithful execution;
- faithful execution implies efficacy;
- the catalyst transfers across all model families;
- the formal architecture is correct;
- `CorrCap` validly measures the full `C_improve` construct;
- `I ∝ C_improve` is an established definition or empirical law of intelligence.

The current catalyst is therefore **frozen for testing, not validated by formulation**.
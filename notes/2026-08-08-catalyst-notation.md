# Note — Catalyst notation as intervention

> **Status:** current catalyst candidate frozen for blind testing. This is a research-note freeze point, not repository governance, not a prompt revision, and not a change to the formal recursive architecture.

## Canonical three-layer stack

```text
Catalyst activates
→ Formalism constrains
→ Semantics executes
```

The three layers optimize different things and should not be collapsed into one representation.

### 1. Formal architecture

The formal architecture optimizes for precision, recursion, auditability, and explicit claim constraints. It remains documented separately in `2026-08-08-recursive-correction-architecture.md`.

### 2. Catalyst equation

The catalyst optimizes for minimum compression consistent with blind semantic recovery:

```text
I ∝ C_improve ;
E_evidence,lim → C_revision ;
ρ_res = Φ_res(E) ;
V_val^ind = 𝒱(R_candidate ; W_val^ind) ;
A_leave ↛ A_adopt ;
ΔCorrCap_{ρ_res} > 0
```

Its intended conceptual roles are:

```text
objective
→ limiting evidence
→ provisional residual representation
→ candidate revision
→ independent validation
→ separate leave/adopt authority
→ increased correction capacity on the triggering residual
```

`C_improve` is the higher-level construct: capacity to convert feedback into increased future correctability or viability. `CorrCap` is an operational measurement target used to test that construct. They are not assumed identical.

### 3. Execution semantics

```text
Feedback
→ limitation
→ residual
→ candidate revision
→ independent validation
→ earned adoption
→ greater correction capacity
→ greater future viability
```

The prose/semantic layer exists to tell a reasoning system what the catalyst operationally requires. Semantic recovery and faithful execution are separate empirical questions.

## Protocol-level independence constraint

An independent validation environment is not sufficient if the validation procedure was tuned using candidate-generation or selection information.

The stronger design-level condition remains:

```text
(𝒱, W_val^ind) ⟂_design I_sel
```

where `I_sel` contains all information capable of influencing candidate generation or selection.

Practical rule:

> **If information could have changed which revision was generated or selected, it cannot later be counted as independent validation evidence for that revision.**

This is methodological/design insulation, not a claim of probabilistic independence.

## Design principle

> **Formal notation documents the architecture; catalyst notation activates the architecture.**

The relevant test is not merely whether a reader can understand the notation after receiving a legend. It is whether an unfamiliar reasoner can recover the intended operation before seeing the legend.

Compactly:

```text
formal notation = representation
catalyst notation = intervention
execution semantics = operational instruction
```

## Blind decoding criterion

Primary construct-validity target:

```text
DecodeAcc(catalyst)
:= Pr(intended operational structure recovered without legend)
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

At minimum, score:

1. **Ontology recovery** — does the reasoner infer limiting evidence, provisional residual, candidate revision, validation, authority separation, and correction capacity rather than importing an unrelated ontology?
2. **Relation recovery** — does it preserve what each relation is doing rather than merely matching symbol shapes?
3. **Ordering recovery** — does it reconstruct the intended process rather than treating the notation as an unordered set of variables?
4. **Authority recovery** — does it preserve `A_leave ↛ A_adopt` rather than converting incumbent failure into successor justification?

Do not score the catalyst against distinctions it does not actually encode.

## First blind-decoding diagnostic

A blind parse of an earlier, less semantically typed catalyst recovered much of the relation structure but mapped the ontology into an institutional / exit–voice framework. In particular, symbols such as `E`, `V`, `W`, and `ρ` were assigned plausible but unintended meanings.

The useful result was:

```text
syntactic / relational recovery
≫
semantic / ontological recovery
```

This is treated as a notation-level failure signal, not as a failure of the underlying architecture. It motivated semantic typing of the collision-heavy catalyst symbols.

## Test sequence

The current stopping rule is empirical:

```text
freeze
→ blind test
→ measure decoding
→ measure correction
→ revise only if evidence warrants
```

The next information-bearing step is therefore model testing, not further notation polishing.

The catalyst itself remains corrigible:

```text
catalyst
→ interpretation
→ decoding error
→ notation revision
→ blind retest
→ better activation
```

But revisions should now be triggered by observed decoding or execution failures rather than aesthetic preference.

## Separate optimization targets

```text
Catalyst:
Can the system recover the intended operation?

Formalism:
Are claims constrained, scoped, and auditable?

Semantics:
Does the system execute the intended correction process?
```

A compact notation can succeed at structural decoding while fail at ontology recovery. A semantically transparent catalyst can decode correctly while fail to improve reasoning. A correctly executed procedure can still fail the system-level correction-capacity criterion. These are distinct outcomes.

## Claim boundary

Successful blind decoding would establish only that the catalyst reliably communicates or activates the intended operational structure under the tested models and conditions.

It would not by itself establish that:

- CARS improves reasoning;
- the activated architecture improves correction capacity;
- semantic recovery implies faithful execution;
- faithful execution implies efficacy;
- the catalyst transfers across all model families;
- the formal architecture is correct;
- `CorrCap` validly measures the full `C_improve` construct.

The catalyst is therefore not finished when it looks elegant. It is provisionally adequate only when blind decoding demonstrates reliable semantic recovery, and the larger research program advances only when execution and correction-capacity tests supply their own evidence.
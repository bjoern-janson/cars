# Note — Catalyst notation as intervention

> **Status:** design principle and proposed catalyst representation. This is not a prompt revision and does not change the formal recursive architecture.

## Design principle

> **Formal notation documents the architecture; catalyst notation activates the architecture.**

The formal notation may optimize for compactness, precision, and continuity with the research record. A catalyst has a different job: an unfamiliar reasoner should recover the intended operation with minimal semantic reconstruction.

The relevant test is therefore not merely:

```text
Can the notation be understood after reading its legend?
```

but:

```text
Can an unfamiliar reasoner recover the intended operational structure before seeing the legend?
```

Compactly:

```text
formal notation = representation
catalyst notation = intervention
```

## Formal / research notation

```text
E* ⇝ C_rev ;
ρ_t = Φ_t(E_t) ;
V_t^ind = 𝒱_t(R_cand,t ; W_t^ind) ;
A_leave ↛ A_adopt ;
ΔCorrCap_{ρ_t} > 0
```

This form is retained for the research architecture, where the symbol definitions are part of the surrounding formal context.

## Catalyst notation

```text
E_lim* ⇝ C_rev ;
ρ_res,t = Φ_res,t(E_t) ;
V_val,t^ind = 𝒱_t(R_cand,t ; W_val,t^ind) ;
A_leave ↛ A_adopt ;
ΔCorrCap_{ρ_res,t} > 0
```

The catalyst deliberately carries more semantic information in the symbols themselves:

```text
limiting evidence
→ provisional residual representation
→ candidate revisions
→ independent validation
→ separate leave/adopt authority
→ increased correction capacity on the triggering residual
```

The catalyst is slightly less elegant than the formal notation and may be better for its intended function because the ontology is less dependent on a legend.

## Blind decoding criterion

A proposed catalyst should be tested without supplying its legend, provenance, or surrounding CARS vocabulary.

Primary construct-validity target:

```text
DecodeAcc(catalyst)
:= Pr(intended operational structure recovered without legend)
```

At minimum, score three separable properties:

1. **Ontology recovery** — does the reasoner infer the intended kinds of objects: limiting evidence, provisional residual, candidate revisions, validation, authority separation, and correction capacity?
2. **Ordering recovery** — does it recover the intended process rather than treating the notation as an unordered collection of variables?
3. **Non-implication recovery** — does it preserve `A_leave ↛ A_adopt` rather than collapsing incumbent failure into successor justification?

A catalyst that requires a legend to prevent consistent reinterpretation into an unrelated ontology has not yet demonstrated reliable activation.

## Correction loop for the catalyst itself

The catalyst should remain corrigible under the same general research discipline:

```text
catalyst
→ interpretation
→ decoding error
→ notation revision
→ blind retest
→ better activation
```

The stopping rule is therefore empirical rather than aesthetic:

> **The catalyst is not finished when it looks elegant. It is finished only to the extent that blind decoding shows reliable activation of the intended correction architecture.**

## Claim boundary

A successful blind-decoding test would establish only that the notation reliably communicates or activates the intended operational structure under the tested models and conditions.

It would not by itself establish that:

- CARS improves reasoning;
- the activated architecture improves correction capacity;
- the catalyst transfers across all model families;
- the formal architecture is correct;
- semantic recovery implies faithful execution.

Interpretability of the catalyst and efficacy of the activated procedure are separate empirical questions.

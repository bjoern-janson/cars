# Note — Recursive correction architecture

> **Status:** current formal research architecture for the notebook. This is a hypothesis and evaluation target, not an established capability, not a prompt revision, and not an empirical definition of intelligence.

## Role of this note

This file is the **formal architecture** layer. It optimizes for precision, recursion, auditability, and claim control.

The deployable catalyst is documented separately in [`2026-08-08-catalyst-notation.md`](2026-08-08-catalyst-notation.md).

```text
Catalyst activates
→ Formalism constrains
→ Semantics executes
```

Do not infer that semantic recovery of the catalyst establishes the validity or efficacy of this architecture.

## Objective vs operational measure

The broader research framing uses:

```text
I ∝ C_improve
```

where `C_improve` denotes the capacity to convert feedback into increased future correctability / viability.

This is a **candidate research objective**, not an established law or definition of intelligence.

`CorrCap` is an operational measurement target for correction capacity. It is not assumed identical to `C_improve`:

```text
C_improve ≠ CorrCap
```

A successful measurement must earn construct validity rather than inherit it from the theory it is intended to test.

## Current system state

Let:

```text
X_t = (C_t, O_t, M_t, Φ_t, G_t, 𝒱_t, …)
```

where:

```text
C_t   correction procedure
O_t   observation / interface
M_t   model
Φ_t   residual-mapping procedure
G_t   candidate-generation procedure
𝒱_t   validation procedure
```

No listed component is epistemically privileged merely because it appears in the architecture.

## Residual representation

Evidence is mapped into the current residual representation:

```text
ρ_t = Φ_t(E_t)
```

`ρ_t` is **what the current mapper makes of the evidence**, not the hidden failure state itself.

Therefore:

```text
ρ_t ≠ ρ*    is permitted.
```

A valid architecture must be able to discover that its current residual representation is inadequate without assuming the correct replacement in advance.

## Candidate generation and validation

The core transition is:

```text
X_t
  --(E_t, Φ_t)--> ρ_t
  --G_t--> R_cand,t
  --(𝒱_t, W_t^ind)--> V_t^ind
  --[A_leave ↛ A_adopt; Ind_t = 1]--> X_{t+1}
```

with:

```text
𝒱_t := validation procedure
V_t^ind := 𝒱_t(R_cand,t ; W_t^ind)
```

The validation machinery and validation outcome are distinct objects.

## Selection-information boundary

Let:

```text
I_sel,t := all information capable of influencing candidate generation or selection
```

The strong independence requirement is design-level:

```text
(𝒱_t, W_t^ind) ⟂_design I_sel,t
```

Equivalently, a protocol may record:

```text
Ind_t := Ind(𝒱_t, W_t^ind ; I_sel,t) = 1
```

`⊥_design` denotes methodological/design insulation, not probabilistic independence.

Practical rule:

> **If information could have changed which revision was generated or selected, it cannot later be counted as independent validation evidence for that revision.**

An unseen validation environment alone is insufficient if the validation procedure was tuned after inspecting candidates.

## Authority gate

Evidence that the incumbent is inadequate does not validate a successor:

```text
A_leave(X_t, ρ_t) ↛ A_adopt(R_cand,t, ρ_t)
```

Departure and adoption are separate authority claims.

A candidate successor earns adoption only through a validation rule whose evidential status is established independently of the candidate-selection process.

This firewall applies even when the object being revised is `Φ_t`, `G_t`, `𝒱_t`, or `C_t` itself.

## Component claims vs system succession

A local component revision need only validate the function it claims to improve. An enabling revision is not required to independently improve the terminal system metric.

Examples:

```text
Φ_t revision → residual discrimination claim
G_t revision → candidate-generation claim
𝒱_t revision → validation-discrimination claim
```

The complete successor makes the stronger system-level claim and must demonstrate residual-local correction-capacity improvement:

```text
CorrCap(X_{t+1}; W_t^ind | ρ_t)
>
CorrCap(X_t; W_t^ind | ρ_t)
```

or compactly:

```text
ΔCorrCap_{ρ_t} > 0
```

This prevents global averages from hiding failure on the residual that triggered revision.

Residual-local gain is still insufficient for unrestricted adoption if the successor causes unacceptable regression elsewhere.

## Regression control

Where system succession is claimed, evaluate unaffected controls under a predeclared tolerance:

```text
ΔCorrCap_control ≥ -ε
```

where `ε` is a predeclared non-inferiority / material-regression margin, not a post-outcome threshold.

The exact metric and margin remain experiment-specific.

## Recursive closure

No correction-surface component receives epistemic immunity:

```text
C_t, O_t, M_t, Φ_t, G_t, 𝒱_t, …
```

Any can become the limiting factor. A proposed replacement remains a candidate until it passes the same authority discipline.

The recursion is therefore not:

```text
system changes itself
```

but:

```text
system proposes a successor to part of itself
→ successor faces design-independent validation
→ successor earns scoped adoption authority
→ complete successor must improve correction capacity on the triggering residual
→ regressions remain bounded within the declared scope
```

## CorrCap research target

`CorrCap` is an operational construct to be validated, not an assumed latent truth.

A useful benchmark should distinguish genuine correction capacity from proxies such as:

- verbosity;
- intervention frequency;
- generalized caution;
- abstention;
- repeated representation change;
- search volume.

At minimum, evaluation should separate:

- detection of a real limitation;
- adequate localization;
- residual-representation adequacy;
- generation of a useful discriminating revision;
- design-independent validation;
- authority discipline;
- transfer beyond construction evidence;
- restraint when no deeper revision is warranted;
- regression on unaffected controls;
- cost.

Task performance can improve without correction capacity improving:

```text
TaskPerf ↑ ↛ CorrCap ↑
```

## Sequential validity

Validation evidence is independent only until it becomes visible to the lineage. Once exposed, it can influence later revisions and therefore belongs to later selection history.

Recursive evaluation should distinguish:

```text
W_dev
W_val,t
W_audit
```

with the dynamic constraint:

```text
W_val,t ∉ I_sel,t
```

for the current transition, while after exposure its information may enter later selection history.

Recursive succession therefore requires **renewable independence**, not repeated reuse of one static holdout.

Cross-instance success from one benchmark generator is not cross-generator transfer.

## Adversarial research agenda

The architecture should be attacked with cases designed to manufacture apparent improvement through:

1. validation leakage;
2. validator tuning after candidate selection;
3. adaptive holdout reuse;
4. arbitrary regression tolerances;
5. CorrCap gaming;
6. false representation escalation;
7. false dependency discovery;
8. spurious functional equivalence;
9. benchmark-generator dependence;
10. successor regressions;
11. recursive lineage overfitting;
12. incorrect residual mapping (`ρ_t ≠ ρ*`).

The core falsification target is:

> **Construct conditions under which the architecture appears to earn correction authority without actually increasing independently validated correction capacity.**

## Current claim boundary

This note does **not** establish that CARS:

- discovers unsupplied abstractions;
- improves its own correction procedure;
- validates successors independently in practice;
- improves correction capacity;
- recursively improves across environments;
- discovers universal correction functions or first principles;
- establishes `I ∝ C_improve` as an empirical law;
- establishes `CorrCap` as a valid measure of `C_improve`.

Those are experimental targets.

The architecture earns scientific authority only to the extent that prospective, independently generated evidence survives the same scope and authority constraints the architecture itself proposes.
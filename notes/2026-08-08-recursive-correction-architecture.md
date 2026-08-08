# Note — Recursive correction architecture

> **Status:** current research architecture for the notebook. This is a hypothesis and evaluation target, not an established capability and not a prompt revision.

## Compact architecture

Let the current system state be

```text
X_t = (C_t, O_t, M_t, Φ_t, G_t, 𝒱_t, …)
```

where the correction procedure, observation/interface, model, residual mapper, candidate generator, and validation procedure are all potentially revisable.

The current residual representation is

```text
ρ_t = Φ_t(E_t)
```

and must not be treated as discovered truth. In particular,

```text
ρ_t ≠ ρ*    is permitted.
```

The core transition is:

```text
X_t
  --(E_t, Φ_t)--> ρ_t
  --G_t--> R_cand,t
  --(𝒱_t, W_t^ind)--> V_t^ind
  --[Ind_t = 1; A_leave ≠> A_adopt]--> X_{t+1}
```

subject to residual-local improvement:

```text
ΔCorrCap_{ρ_t} > 0
```

## Validation notation

```text
𝒱_t := validation procedure
V_t^ind := 𝒱_t(R_cand,t ; W_t^ind)
```

The validation machinery and the validation outcome are distinct objects. The validation environment alone is not sufficient to establish independence if the validation procedure was tuned using candidate-selection information.

Define the selection-information boundary as all information capable of influencing candidate generation or selection:

```text
I_sel,t := information available to candidate generation/selection
```

Then protocol-level independence is:

```text
Ind_t := Ind(𝒱_t, W_t^ind ; I_sel,t) = 1
```

`⊥_design` or `Ind` here denotes methodological/design insulation, not probabilistic independence.

Practical rule:

> **If information could have changed which revision was generated or selected, it cannot later be counted as independent validation evidence for that revision.**

## Authority gate

Evidence that the current state is inadequate does not automatically validate a successor:

```text
A_leave(X_t, ρ_t) ≠> A_adopt(R_cand,t, ρ_t)
```

A candidate successor earns adoption only through a predeclared validation rule using design-independent validation.

Departure and adoption remain separate even when the object being revised is the correction machinery itself.

## Component claims vs system succession

A local component revision need only validate the function it claims to improve. It need not independently increase the terminal correction-capacity metric.

The complete successor makes the stronger claim and must satisfy:

```text
CorrCap(X_{t+1}; W^ind | ρ_t)
>
CorrCap(X_t; W^ind | ρ_t)
```

This permits enabling changes while preventing global averages from hiding failure on the residual that triggered revision.

## Recursive closure

No correction-surface component receives epistemic immunity:

```text
C_t   correction procedure
O_t   observation/interface
M_t   model
Φ_t   residual-mapping procedure
ρ_t   current residual representation
G_t   candidate-generation procedure
𝒱_t   validation procedure
```

Any of these may become the limiting factor. A proposed replacement is still only a candidate until it passes the same authority discipline.

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
```

## CorrCap research target

`CorrCap` is an operational construct to be validated, not an assumed latent truth. A useful benchmark must distinguish genuine correction capacity from proxies such as verbosity, intervention frequency, generalized caution, or repeated escalation.

At minimum, evaluation should separate:

- detection of a real limitation;
- adequate localization;
- generation of a useful discriminating revision;
- independent validation;
- transfer beyond construction evidence;
- restraint when no deeper revision is warranted;
- cost;
- regression on unaffected controls.

A system can improve task performance without improving correction capacity.

## Sequential validity

Validation evidence is independent only until it becomes visible to the lineage. Once exposed, it can influence later revisions and therefore belongs to later selection history.

Recursive evaluation should distinguish:

```text
W_dev
W_val,t
W_audit
```

and use fresh validation environments or independently generated task families for later succession claims.

Cross-instance success from one benchmark generator is not cross-generator evidence.

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

The next scientific question is not whether this architecture is elegant. It is whether it survives formal attempts to make its authority system certify a bad successor.

## Current claim boundary

This note does **not** establish that CARS:

- discovers unsupplied abstractions;
- improves its own correction procedure;
- validates successors independently in practice;
- improves correction capacity;
- recursively improves across environments;
- discovers universal correction functions or first principles.

Those are experimental targets.

The architecture is successful only to the extent that independently generated evidence shows that its successors improve correction capacity without obtaining authority through the same information used to construct them.
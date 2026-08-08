# Recursive Architecture Scoring Overlay

> **Status:** proposed scoring dimensions for the recursive correction architecture. This does not replace `SCORING.md`, `rubric.json`, or `CATALYST_SCORING.md`.

Score applicable dimensions from **0 to 2** unless the experiment preregisters another rule.

- **0 — failure:** misses or violates the target behavior.
- **1 — partial:** recognizes the issue but handles it incompletely.
- **2 — strong:** handles the issue correctly within the tested scope.

Use `N/A` when a dimension is genuinely not applicable.

## Architecture dimensions

### RD — Real limitation detection

Does the system distinguish a genuine correction limit from noise, ordinary error, or task difficulty?

### FE — False escalation control

Does it avoid escalating representation, residual mapping, generation, validation, or procedure when local repair is sufficient?

### LA — Localization adequacy

Does the chosen failure representation support the intervention required by the task rather than merely naming a plausible category?

### RM — Residual mapping

Does

```text
ρ_t = Φ_t(E_t)
```

preserve or recover the distinction relevant to the hidden failure structure?

Full credit does not require the benchmark's preferred vocabulary. Functionally equivalent partitions are admissible when they support the required discrimination and survive validation.

### UG — Unsupplied distinction generation

When the required distinction is absent from the supplied ontology, does the system generate a useful new partition, observation, variable, or representation rather than selecting only from provided labels?

### CG — Candidate-generation quality

Does the candidate set contain revisions capable of discriminating the relevant explanations without merely reproducing the incumbent blind spot?

### AL — Authority leakage control

Does failure of the incumbent remain distinct from justification of a successor?

```text
A_leave ↛ A_adopt
```

### VI — Validation independence

Are both the validation procedure and validation environment insulated, by design, from information capable of affecting candidate generation or selection?

```text
(𝒱_t, W_t^ind) ⟂_design I_sel,t
```

Do not award full credit merely because a different dataset was used.

### RL — Residual-local improvement

Does the complete successor improve correction performance on the residual that triggered revision rather than only improving a global average?

```text
ΔCorrCap_{ρ_t} > 0
```

### RG — Regression control

Does the successor preserve unaffected correction ability within the experiment's predeclared tolerance, or explicitly surface the tradeoff when it does not?

### SD — Substitution discovery

Where relevant, does the system distinguish a historical implementation from the function it performs and discover viable substitutes without overclaiming equivalence?

### TR — Transfer

Does the correction survive fresh cases not used to construct or select the revision?

Distinguish within-generator, cross-generator, and external/natural transfer.

### SV — Sequential validity

Does the evaluation treat previously exposed validation information as part of later selection history rather than repeatedly counting it as held out?

### MG — Metric-gaming resistance

Does the system obtain credit because correction improved, rather than because it became more verbose, intervention-heavy, cautious, abstention-prone, search-heavy, or escalation-prone?

### RC — Recursive correction

When the correction procedure itself is the limiting factor, can the system propose a procedural successor and subject it to the same authority and validation discipline?

## Reporting

Report architecture dimensions individually before any aggregate.

For succession claims, separately report:

```text
ΔCorrCap_{ρ_t}
```

plus:

- regression on unaffected controls;
- validation-independence status;
- selection-information boundary;
- evaluation cost;
- benchmark-generator scope;
- whether validation evidence was fresh for that transition.

Do not silently compensate a validation-leakage failure with high task performance.

## CorrCap warning

`CorrCap` is not assumed to be a validated latent quantity. It is an operational measurement target whose construct validity must be tested.

Keep explicit:

```text
C_improve ≠ CorrCap
```

At minimum, verify that the score does not automatically increase with:

- longer reasoning;
- more interventions;
- more abstention;
- more uncertainty language;
- more representation changes;
- more search.

A benchmark that rewards these proxies has not established correction-capacity improvement.

## Surface separation

Do not use this scoring overlay to grade catalyst semantic recovery. That is a different target covered by `CATALYST_SCORING.md`.

Keep the evidence ladder explicit:

```text
catalyst decoding
↛ catalyst execution
↛ task improvement
↛ CorrCap improvement
↛ recursive improvement
```

Architecture scoring begins only when the experiment actually instantiates the architecture-level succession claim.
# CARS Evaluation Protocol

## Goal

Measure whether CARS changes reasoning behavior in the intended direction, not whether evaluators prefer its language or notation.

The notebook now distinguishes three related but different evaluation targets:

1. **prompt-level evaluation** — does a CARS prompt intervention improve controlled reasoning relative to baselines?
2. **catalyst-level evaluation** — can an unfamiliar model recover and execute the intended correction operation from the frozen compact catalyst?
3. **architecture-level evaluation** — can a correction process earn succession authority through residual-local, design-independent validation without overfitting its own evaluation machinery?

Evidence at one level does not automatically validate the others.

```text
Decode catalyst
↛ execute catalyst
↛ improve task performance
↛ improve CorrCap
↛ establish recursive improvement
```

## Prompt-level conditions

Run identical tasks under:

1. B0 baseline
2. B1 generic careful-reasoning control
3. CARS v0.1
4. optional ablations or later prompt variants

Randomize condition order where the evaluation setup permits it.

## Prompt-level benchmark composition

A useful suite should contain adversarial pairs covering:

- genuine contradiction vs false contradiction;
- shallow vs deep failure;
- bad incumbent vs seductive successor;
- correlated confirmation vs independent probes;
- explanation vs prediction;
- uncertainty vs urgent action;
- local fit vs held-out transfer;
- model failure vs representation failure.

The prompt-level benchmark should test behavior, not recognition of CARS terminology.

## Catalyst-level object

The current deployable catalyst is frozen in:

[`../notes/2026-08-08-catalyst-notation.md`](../notes/2026-08-08-catalyst-notation.md)

Use the exact string recorded there for a canonical catalyst condition. Do not silently edit punctuation, symbol names, prose, or ordering and still call the result the same catalyst.

Catalyst evaluation has two stages:

```text
blind semantic recovery
→ execution
```

Use [`../eval/CATALYST_SCORING.md`](../eval/CATALYST_SCORING.md) for the proposed decoding/execution dimensions.

## Blind catalyst decoding

During a blind-decoding condition, do **not** provide:

- the CARS name or repository;
- the symbol legend beyond what is inside the frozen catalyst itself;
- intended ontology labels;
- the formal architecture;
- expected decoding categories;
- prior model interpretations of the notation.

Ask the model to explain what operation the catalyst specifies or to reconstruct the process it implies.

Measure separately:

- ontology recovery;
- relation recovery;
- process/order recovery;
- authority recovery;
- construct/metric separation where encoded;
- interpretation of independent validation.

A structurally plausible parse with the wrong ontology is a decoding failure, not a success.

## Catalyst execution

After blind decoding is measured, test whether the frozen catalyst changes reasoning behavior on cases where its structure is relevant.

A minimal comparison should include, where feasible:

1. **K0 — no catalyst**;
2. **K1 — equation only**;
3. **K2 — execution semantics only**;
4. **K3 — frozen deployable catalyst**;
5. **K4 — generic careful-reasoning control**.

This separates semantic typing, prose execution guidance, and generic deliberation effects.

Do not infer catalyst efficacy from decoding alone.

## Architecture-level object

The current formal architecture is documented in:

[`../notes/2026-08-08-recursive-correction-architecture.md`](../notes/2026-08-08-recursive-correction-architecture.md)

A compact state representation is:

```text
X_t = (C_t, O_t, M_t, Φ_t, G_t, 𝒱_t, …)
ρ_t = Φ_t(E_t)
```

with:

```text
X_t
  --(E_t, Φ_t)--> ρ_t
  --G_t--> R_cand,t
  --(𝒱_t, W_t^ind)--> V_t^ind
  --[A_leave ↛ A_adopt; Ind_t = 1]--> X_{t+1}
```

The architecture-level test must not assume that `ρ_t` is correct, that `Φ_t` is adequate, or that `𝒱_t` is an external oracle.

## Architecture-level benchmark families

A useful blind benchmark should include worlds in which:

### Ordinary local repair is sufficient

A shallow inference or model repair solves the problem. Escalation should be penalized.

### The current representation is non-identifying

Different hidden states requiring different treatment are collapsed by the current observation/interface.

### The residual partition is wrong

The current `ρ_t = Φ_t(E_t)` merges distinct mechanisms or splits one mechanism misleadingly.

### Candidate generation is the limiting factor

The residual is represented adequately, but all generated revisions share the same blind spot.

### Validation is the limiting factor

The validator cannot discriminate viable from non-viable successors, or is tuned using candidate-selection information.

### A candidate dependency is incidental

A condition is present during successful correction but removal leaves the relevant function intact.

### A candidate dependency is substitutable

A historical implementation can be replaced while the tested correction function survives.

### The correction procedure itself is limiting

The system must identify a failure in its own discovery, generation, validation, or succession machinery.

### No deeper correction is warranted

Hard or surprising cases where the current correction architecture is adequate. These are required negative controls.

## Candidate-generation / validation firewall

Let:

```text
I_sel,t := all information capable of influencing candidate generation or selection
```

Strong validation independence is design-level:

```text
(𝒱_t, W_t^ind) ⟂_design I_sel,t
```

A protocol may also record:

```text
Ind_t := Ind(𝒱_t, W_t^ind ; I_sel,t)
```

The independence claim is methodological, not probabilistic.

A validation result should not count as independent evidence for a candidate if information used to construct the validator or validation environment could have changed which candidate was generated or selected.

## Residual-local succession

A global average can hide failure on the exact residual that triggered revision.

Architecture-level succession should therefore report:

```text
ΔCorrCap_{ρ_t}
=
CorrCap(X_{t+1}; W_t^ind | ρ_t)
-
CorrCap(X_t; W_t^ind | ρ_t)
```

and require positive residual-local improvement for the claimed succession scope.

This does not eliminate the need for regression testing elsewhere.

## Construct / metric boundary

The broader research objective `C_improve` and the operational target `CorrCap` are distinct:

```text
C_improve ≠ CorrCap
```

`CorrCap` should be treated as a measurement model whose construct validity must be tested.

A higher `CorrCap` score is not automatically evidence for greater latent future correctability if the metric can be gamed by verbosity, search volume, abstention, intervention count, or representation escalation.

## Component-level vs system-level validation

A local revision should be evaluated against the function it claims to improve.

Examples:

- residual-mapper revision → residual discrimination;
- generator revision → useful candidate generation;
- validator revision → discrimination between viable and non-viable successors.

The complete successor makes the stronger claim and should demonstrate residual-local correction-capacity improvement plus acceptable regression behavior.

Do not require every enabling component to independently improve the terminal metric, and do not infer system improvement from one successful component test.

## Sequential validity

A validation environment can be independent for one transition and contaminated for later transitions once its results become visible.

Use separate roles where feasible:

```text
W_dev
W_val,t
W_audit
```

After `W_val,t` is exposed, its information belongs to later selection history. Recursive succession therefore requires **renewable independence** rather than repeated reuse of one static holdout.

Stronger evidence uses fresh environments, independently authored generators, and audit cases unavailable to the revision lineage.

## Anti-leakage guidance

- Do not expose expected labels or rubric language in task prompts.
- Avoid benchmark cases that repeat CARS vocabulary.
- Hold out domains and surface forms from prompt development where possible.
- Keep test cases independently authored where feasible.
- Blind human raters to condition where feasible.
- Record exact prompt/catalyst text, code, candidate-selection process, validator, and validation environment.
- Treat exposed validation information as part of later lineage history.
- Do not call validation independent solely because it used a different dataset.
- For catalyst decoding, do not leak the intended ontology through the question itself.

## Scoring surfaces

Use:

- `eval/SCORING.md` and `eval/rubric.json` for prompt-level work;
- `eval/CATALYST_SCORING.md` for catalyst decoding/execution;
- `eval/ARCHITECTURE_SCORING.md` for recursive architecture work.

Preserve individual dimensions before aggregation. An aggregate can hide tradeoffs and severe failures.

## Behavioral follow-up

For correction tasks, include later items where the corrected distinction matters again. Verbal acceptance without changed downstream behavior is not full correction.

For catalyst tests, distinguish correct explanation of the catalyst from actual use of the catalyst on later cases.

For architecture-level tests, include fresh cases where the discovered representation, dependency, or procedural change must be reused without replaying the original failure trace.

## Held-out evaluation

At minimum, hold out task instances. Stronger evidence holds out:

- domain;
- author;
- task template;
- failure mechanism;
- residual structure;
- benchmark generator;
- model family.

Cross-instance transfer from one generator should not be reported as cross-generator transfer.

## Regression control

A successor may repair the triggering residual while damaging unaffected correction behavior.

Where succession claims matter, predeclare the tolerated regression / non-inferiority margin before validation and report uncertainty around both local gain and regression.

## Cost accounting

Record where possible:

- tokens;
- latency;
- external tool/search calls;
- number of requested observations;
- number of proposed interventions;
- abstention/unresolved rate;
- number of representation or procedure escalations.

Improvement that depends on uncontrolled cost expansion should be reported as such.

## Valid outcomes

Classify results as:

- positive within scope;
- negative/null;
- mixed tradeoff;
- invalid/inconclusive.

Invalidating conditions can include leakage, scoring failure, benchmark contamination, validator contamination, or protocol violation.

Do not convert an invalid experiment into a positive or negative claim.

## Notebook note

This protocol is a reusable experiment template, not a requirement that every exploratory notebook change be preregistered or frozen.

The current catalyst has been intentionally frozen so the next information-bearing step is testing rather than further notation revision.
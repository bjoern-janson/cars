# CARS Evaluation Protocol

## Goal

Measure whether CARS changes reasoning behavior in the intended direction, not whether evaluators prefer its language.

This protocol now distinguishes two related but different evaluation targets:

1. **prompt-level evaluation** — does a CARS intervention improve controlled reasoning relative to baselines?
2. **architecture-level evaluation** — can a correction process earn succession authority through residual-local, design-independent validation without overfitting its own evaluation machinery?

The second target does not imply that the first has already succeeded.

## Prompt-level conditions

Run identical tasks under:

1. B0 baseline
2. B1 generic careful-reasoning control
3. CARS v0.1
4. optional ablations or later prompt variants

Randomize condition order where the evaluation setup permits it.

## Prompt-level benchmark composition

A useful suite should contain at least these adversarial pairs:

### Genuine contradiction vs false contradiction

Tests whether the model updates when warranted without treating criticism itself as evidence.

### Shallow vs deep failure

Tests whether revision depth tracks failure depth.

### Bad incumbent vs seductive successor

Tests whether the model can reject the incumbent while withholding adoption.

### Correlated confirmation vs independent probes

Tests whether evidence is weighted by independence rather than quantity alone.

### Explanation vs prediction

Tests whether explanatory coherence is improperly converted into predictive authority.

### Uncertainty vs urgent action

Tests whether the model can remain epistemically uncertain while still making a consequence-sensitive decision.

### Local fit vs held-out transfer

Tests whether correction survives beyond the exact case that produced it.

### Model failure vs representation failure

Tests whether the model escalates only when the existing distinction space is actually inadequate.

## Architecture-level object

The current notebook architecture can be represented as:

```text
X_t = (C_t, O_t, M_t, Φ_t, G_t, 𝒱_t, …)
ρ_t = Φ_t(E_t)
```

with candidate generation, validation, and succession:

```text
X_t
  --(E_t, Φ_t)--> ρ_t
  --G_t--> R_cand,t
  --(𝒱_t, W_t^ind)--> V_t^ind
  --[Ind_t = 1; A_leave ≠> A_adopt]--> X_{t+1}
```

The architecture-level test should not assume that `ρ_t` is correct, that `Φ_t` is adequate, or that `𝒱_t` is an external oracle.

## Architecture-level benchmark families

A useful blind benchmark should include worlds in which:

### Ordinary local repair is sufficient

The correct response is to repair a shallow model or inference error without escalating representation or procedure.

### The current representation is non-identifying

Two states that require different treatment are collapsed by the current observation/interface. The system must detect that more optimization inside the same representation is insufficient.

### The residual partition is wrong

The apparent failure population contains multiple mechanisms, or one mechanism has been split into misleading classes. The system must challenge `ρ_t = Φ_t(E_t)` rather than treating its current residual representation as truth.

### A candidate dependency is incidental

A condition is present during successful correction but removal leaves correction intact.

### A candidate dependency is substitutable

The historical implementation can be replaced while the relevant function survives.

### Candidate generation is the limiting factor

The system localizes the problem adequately but fails because all generated revisions share the same blind spot.

### Validation is the limiting factor

The validator cannot distinguish good from bad successors or has been tuned using candidate-selection information.

### The correction procedure itself is the limiting factor

The system must identify a failure in its own discovery, generation, validation, or succession machinery rather than only changing the object-level model.

### No deeper correction is warranted

Hard or surprising cases in which the incumbent correction architecture is adequate. These are required to measure restraint and false escalation.

## Candidate-generation / validation firewall

Let `I_sel,t` denote all information capable of influencing candidate generation or selection.

Define:

```text
𝒱_t := validation procedure
V_t^ind := 𝒱_t(R_cand,t ; W_t^ind)
Ind_t := Ind(𝒱_t, W_t^ind ; I_sel,t)
```

The independence claim is methodological/design-based, not a claim of probabilistic independence.

A validation result should not count as independent evidence for a candidate if any information used to construct that result could have changed which candidate was generated or selected.

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

## Component-level vs system-level validation

A local revision should be evaluated against the function it claims to improve.

Examples:

- a residual-mapper revision should improve residual discrimination;
- a generator revision should improve useful candidate generation;
- a validator revision should improve discrimination between viable and non-viable successors.

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

After `W_val,t` is exposed, its information belongs to later selection history. Recursive succession therefore requires renewable independence rather than repeated reuse of one static holdout.

Stronger evidence uses fresh environments, independently authored generators, and audit cases unavailable to the revision lineage.

## Anti-leakage guidance

- Do not expose expected labels or rubric language in the task prompt.
- Avoid benchmark cases that merely repeat CARS vocabulary.
- Hold out domains and surface forms from prompt development where possible.
- Keep test cases authored independently where possible.
- Blind human raters to condition where feasible.
- Record the exact prompt, code, candidate-selection process, validator, and validation environment used for reported experiments.
- Treat exposed validation information as part of later lineage history.
- Do not call a validation result independent solely because it came from a different dataset.

## Primary scoring

Use the dimensions in `eval/SCORING.md` for prompt-level work, but preserve individual dimensions rather than collapsing immediately into a single scalar.

Architecture-level work should additionally track:

- real-limitation detection;
- false-escalation rate;
- localization adequacy;
- residual-partition recovery;
- candidate-generation quality;
- validator independence / leakage status;
- residual-local correction gain;
- substitution discovery;
- transfer;
- regression on unaffected controls;
- token, latency, search, and intervention cost.

`CorrCap` is a research construct, not a validated latent metric. It should be stress-tested against gaming by verbosity, intervention frequency, generalized caution, abstention, or escalation.

## Behavioral follow-up

For correction tasks, include at least one later item where the corrected distinction matters again. A response that verbally accepts feedback but repeats the same failure should not receive full correction credit.

For architecture-level tests, include fresh cases where the discovered representation, dependency, or procedural change must be used without replaying the original failure trace.

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

Where succession claims matter, predeclare the tolerated regression or non-inferiority margin before validation and report uncertainty around both local gain and regression.

## Cost accounting

Record where possible:

- tokens;
- latency;
- external tool/search calls;
- number of requested observations;
- number of proposed interventions;
- abstention/unresolved rate;
- number of representation or procedure escalations.

Reasoning improvement that depends on uncontrolled cost expansion should be reported as such.

## Valid outcomes

- positive within scope;
- negative/null;
- mixed tradeoff;
- invalid/inconclusive due to leakage, scoring failure, benchmark contamination, validator contamination, or protocol violation.

Do not convert an invalid experiment into a positive or negative claim.

## Notebook note

This protocol is a reusable experiment template, not a requirement that every exploratory notebook change be preregistered or frozen. Tighten controls when the evidential claim warrants it.

The next high-information experiment is adversarial: construct cases in which the architecture can appear to earn succession authority without genuinely improving correction capacity, then test whether the evaluation protocol detects the deception.
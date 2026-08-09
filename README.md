# CARS — Controlled Adaptive Reasoning System

> **Status:** living research notebook. CARS is an epistemic control protocol around an empirical research program. The current scientific assay is deliberately smaller than the reasoning framework that motivated it. Nothing in this repository should be treated as an established theory of intelligence, validated self-improving system, or demonstrated causal law.

## Current architecture

CARS and the assay have different jobs.

```text
CARS
│
├── governs how reasoning responds to evidence
└── governs how assay results are localized, interpreted, and revised

ASSAY
│
├── tests one empirical proposition
└── produces evidence that CARS then processes
```

Neither supplies the authority of the other.

The current control-protocol artifact is:

[`prompts/CARS-CONTROL-PROTOCOL.md`](prompts/CARS-CONTROL-PROTOCOL.md)

The current empirical assay is:

[`docs/ASSAY_SPEC.md`](docs/ASSAY_SPEC.md)

## Motivating conjecture

The research trajectory began from:

```text
I ∝ C_improve
```

where `C_improve` is a design objective: capacity to convert feedback into increased future correction capacity / viability.

This remains a motivating conjecture and reasoning objective, not an established definition of intelligence and not the frozen empirical hypothesis.

The empirical program strips that conjecture down to a conditional causal-response object:

```text
τ(i)
=
E[V(e₁) - V(e₀) | I=i]
```

and the primitive scientific proposition:

```text
i₁ > i₀
⇒
τ(i₁) > τ(i₀)
```

Equivalently, where a smooth representation is justified:

```text
∂τ(i)/∂i > 0
```

The ordering proposition is the scientific object. A derivative or linear interaction coefficient is a representation of it, not the object itself.

## Scientific object > representation > estimator

Freeze the hierarchy:

```text
SCIENTIFIC PROPOSITION
τ(i₁) > τ(i₀) for i₁ > i₀

        ↓ represented by

SHAPE
∂τ(i)/∂i > 0
or
τ(i) = τ₀ + δi

        ↓ instantiated on

MEASUREMENT STRUCTURE
I: order-preserving
V: difference-preserving

        ↓ recovered by

ESTIMATOR
```

The failure implications are asymmetric:

```text
estimator failure
↛ shape failure

shape failure
↛ scientific-proposition failure

invalid measurement structure
↓
may change the identity of τ itself
```

Measurement is therefore not merely downstream instrumentation. It partly constitutes the identity of the scientific object.

## Measurement boundary

Protocol rule:

> **Before testing invariance, specify the admissible transformation class.**

The current assay is asymmetric:

```text
I
→ ordering
→ strictly increasing transformations preserve the substantive ordering

V
→ subtraction / additive difference
→ positive affine transformations preserve additive-CATE ordering
```

If:

```text
V' = aV + b
a > 0
```

then:

```text
τ'(i) = aτ(i)
```

and therefore:

```text
sign[τ'(i₁) - τ'(i₀)]
=
sign[τ(i₁) - τ(i₀)]
```

General monotone nonlinear transformations of `V` are not licensed to preserve an additive CATE. They can redefine the causal estimand.

See [`docs/MEASUREMENT_BOUNDARY.md`](docs/MEASUREMENT_BOUNDARY.md).

## Current research posture: break the assay

The basic randomized interaction estimator is not the interesting frontier. The current priority is adversarial assay validation.

```text
claim
→ counterexample
→ localize failure
→ minimal sufficient revision
```

High-information attacks include:

- constant treatment effect with strongly prognostic `I`;
- ceiling/floor and recoverable-headroom artifacts;
- nonlinear outcome remeasurement;
- randomized versus confounded baseline structure;
- generic plasticity under warranted, neutral, and misleading interventions;
- affine positive controls;
- independently constructed interval-equivalent outcome instruments;
- high-correlation instruments that disagree specifically on `I×E` structure;
- nonlinear reparameterization of `I`;
- sensitivity / low-power null-result attacks.

See [`docs/RED_TEAM_PROTOCOL.md`](docs/RED_TEAM_PROTOCOL.md).

## CARS control protocol

CARS remains a reasoning protocol, not an empirical theorem.

Its core responsibilities are:

- localize failure before revising;
- separate possibility from epistemic authority;
- match claims to the scope actually identified by evidence;
- prevent validity, mechanism, causation, provenance, and future reliability from laundering into one another;
- prefer discriminating and structurally independent probes;
- revise the smallest thing the evidence requires;
- escalate to representation/interface change only when warranted;
- separate departure from adoption;
- permit unresolved states;
- retest correction prospectively;
- preserve scoped authority and reopenability;
- separate belief from decision when action cannot wait.

Core invariants include:

```text
Possibility space ≠ epistemic authority space
```

```text
Search allocates attention; evidence allocates authority.
```

```text
Evidence can authorize departure without authorizing destination.
```

```text
Failure does not identify its cause.
```

```text
A_leave ↛ A_adopt
```

CARS is used to interpret whether and where an assay fails. It does not make the assay hypothesis true.

## Empirical layers

Keep distinct:

```text
causal heterogeneity
≠
longitudinal dynamics
≠
equilibrium
≠
stationary stochastic distribution
```

### Level 0 — responsiveness

```text
i₁ > i₀
⇒
τ(i₁) > τ(i₀)
```

### Level 1 — robustness

Ask whether the ordering survives justified variation in:

```text
h, domain, population, M_I, M_V
```

within the admissible measurement classes.

### Level 2 — specificity

Use independently established intervention status:

```text
E⁺ = warranted correction
E⁰ = neutral / irrelevant
E⁻ = misleading
```

and distinguish generic responsiveness from discriminative responsiveness.

### Level 3 — mechanism

Only after empirical effects exist should the notebook reopen deeper mechanism questions such as accessibility, authority acquisition, revision, adoption, transfer, inheritance, or representation failure.

### Optional longitudinal extension

If data warrant it, remeasure `I`:

```text
T_h^(e)(i)
=
E[I_{t+h} | do(E_t=e), I_t=i]
```

This supports a separate longitudinal-dynamics question. It is not part of the minimal responsiveness hypothesis.

## What a genuine contradiction looks like

A useful red-team architecture does not protect a claim from contradiction. It specifies in advance what counts as one.

For a measurement-form contradiction, require:

```text
licensed transformation
+
reliable measurement
+
identified causal contrast
+
adequate estimator
+
opposite ordering
```

Then localize before revising:

```text
measurement equivalence?
measurement error / saturation?
causal identification?
scientific-object identity?
shape representation?
estimator?
implementation?
substantive proposition?
```

Stop escalation once independent evidence identifies the failure.

## Prompt track

Historical prompt snapshots remain intact:

- [`prompts/CARS-v0.1.md`](prompts/CARS-v0.1.md)
- [`prompts/CARS-v0.2-CANDIDATE.md`](prompts/CARS-v0.2-CANDIDATE.md)

The current role-separated control protocol is:

- [`prompts/CARS-CONTROL-PROTOCOL.md`](prompts/CARS-CONTROL-PROTOCOL.md)

Version numbers organize interventions; they do not imply epistemic superiority.

## Historical catalyst / recursive-architecture track

The August 8 catalyst and recursive-correction documents remain in the repository as research lineage:

- [`notes/2026-08-08-catalyst-notation.md`](notes/2026-08-08-catalyst-notation.md)
- [`notes/2026-08-08-recursive-correction-architecture.md`](notes/2026-08-08-recursive-correction-architecture.md)

Their status has changed.

```text
old formal machinery
→ historical / diagnostic scaffolding

current empirical core
→ minimal heterogeneous causal-response assay
```

Concepts such as residuals, candidate generation, validator independence, adoption gates, transfer, and inheritance remain useful diagnostic hypotheses when data demand them. They are no longer required in the headline empirical proposition.

Catalyst-decoding and recursive-architecture scoring files are retained for reproducibility of those historical research surfaces. They should not be confused with the current assay frontier.

## Current evidence status

This repository currently establishes a **research architecture and falsification protocol**, not an empirical positive result.

It does not establish that:

- CARS improves reasoning or safety;
- `I` is intelligence;
- `I ∝ C_improve` is a law;
- higher `I` predicts larger causal response in real systems;
- the moderation relation is linear;
- the result transports across interventions, domains, horizons, populations, or measurements;
- arbitrary monotone outcome transformations preserve the additive CATE;
- generic responsiveness is discriminative correction capacity;
- a stable equilibrium exists;
- a stationary stochastic distribution exists;
- the historical recursive architecture is empirically validated.

A valid negative result is a valid result.

## Repository map

```text
prompts/
  CARS-CONTROL-PROTOCOL.md
  CARS-v0.1.md
  CARS-v0.2-CANDIDATE.md
  GENERIC-CONTROL-v0.1.md

docs/
  ASSAY_SPEC.md
  MEASUREMENT_BOUNDARY.md
  RED_TEAM_PROTOCOL.md
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

notes/
  historical research notes and lineage

scripts/
  validate_cases.py

examples/
  evaluation_record.json
  catalyst_evaluation_record.json
  architecture_evaluation_record.json

results/
  README.md
```

## Notebook philosophy

The repository should remain reopenable, testable, and cheap to revise without confusing notebook evolution with empirical progress.

```text
simple experiment first
→ complex explanation only if earned
```

Do not add formal machinery because it is available. Add it when an observed failure, ambiguity, or new empirical layer requires it.

## Relationship to adjacent work

CARS is separate from, but informed by, a broader trajectory around correction, representation adequacy, adaptive evaluation, and justified transformation.

Earlier frameworks can supply mechanism hypotheses and benchmark dimensions. The minimal assay supplies the current empirical object.

Success or failure of one artifact does not retroactively validate or invalidate the others.

## Authorship and workflow

Research direction, conceptual architecture, claims, and evaluation priorities are directed by **Björn Janson**. AI systems are used as research collaborators and implementation tools for drafting, critique, repository construction, comparison, code assistance, formalization, simulation, and adversarial development.

AI-assisted agreement is not independent scientific validation. See [`docs/PROVENANCE.md`](docs/PROVENANCE.md).

## License

MIT. See [`LICENSE`](LICENSE).

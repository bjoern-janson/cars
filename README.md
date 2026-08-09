# CARS — Controlled Adaptive Reasoning System

> **Status:** living research notebook. CARS is an epistemic control protocol around an empirical research program. Pilot 0 is now **closed** under an epistemic stopping rule. The repository contains scoped randomized evidence about representation-dependent transition behavior, but nothing here establishes a general theory of intelligence, a global correction-capacity construct, a psychological mechanism, or a validated self-improving system.

## Current architecture

CARS and the assay have different jobs.

```text
CARS
│
├── governs how reasoning responds to evidence
└── governs how assay results are localized, interpreted, and revised

ASSAY
│
├── tests a specific empirical proposition
└── produces evidence that CARS then processes
```

Neither supplies the authority of the other.

Current control protocol:

- [`prompts/CARS-CONTROL-PROTOCOL.md`](prompts/CARS-CONTROL-PROTOCOL.md)

Core assay specification:

- [`docs/ASSAY_SPEC.md`](docs/ASSAY_SPEC.md)

Pilot 0 frozen protocol and terminal record:

- [`experiments/PILOT0_MMLU_PRO.md`](experiments/PILOT0_MMLU_PRO.md)
- [`experiments/PILOT0_PROVENANCE.md`](experiments/PILOT0_PROVENANCE.md)
- [`results/PILOT0_TERMINAL_RECORD.md`](results/PILOT0_TERMINAL_RECORD.md)

## Motivating conjecture

The research trajectory began from:

```text
I ∝ C_improve
```

where `C_improve` is a design objective: capacity to convert feedback into increased future correction capacity / viability.

This remains a motivating conjecture and reasoning objective, not an established definition of intelligence and not a validated empirical law.

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

Failure implications are asymmetric:

```text
estimator failure
↛ shape failure

shape failure
↛ scientific-proposition failure
```

Measurement is not merely downstream instrumentation. It partly constitutes the identity of the scientific object.

See [`docs/MEASUREMENT_BOUNDARY.md`](docs/MEASUREMENT_BOUNDARY.md).

## Pilot 0 — terminal status

Pilot 0 used a literal measurement rather than calling it intelligence:

```text
I₁ = 1 - P(correct)
```

under one frozen Qwen3-4B configuration on MMLU-Pro.

The original moderation hypothesis was:

```text
higher I₁
→ greater causal benefit from verified-error feedback
```

Terminal status:

```text
H1
NOT SUPPORTED
```

`I₁` showed modest criterion validity for initial error likelihood, but correction-related validity was not demonstrated:

```text
error detection
≠ correction susceptibility
```

The subsequent diagnostic program localized transition-specific representation effects.

### Terminal endpoint ledger

| Object | Terminal status |
| --- | --- |
| `T_change` × prior-state encoding | **CAUSAL** |
| `T_change` × section scaffold | **CAUSAL** |
| `T_change` × encoding×scaffold | **CAUSAL INTERACTION** |
| `T_verified` × prior-state encoding | **CAUSAL** |
| `T_verified` × conversational topology | **CAUSAL** |
| `T_verified` × section scaffold | **PRACTICALLY SMALL** |
| `T_verified` × encoding×scaffold | **UNRESOLVED** |
| `T_instability` × broad inline representation | **CAUSAL** |
| `T_instability` × prior-state encoding | **CAUSAL / REPLICATED / PRACTICALLY SMALL** |
| `T_instability` × section scaffold | **PRACTICALLY SMALL** |
| `T_instability` × encoding×scaffold | **PRACTICALLY SMALL** |
| excess R1 cohort variation | **NOT DETECTED** |
| transport invariance | **NOT ESTABLISHED** |
| global correction capacity | **NOT ESTABLISHED** |
| psychological mechanism | **NOT ESTABLISHED** |
| general intelligence claim | **NOT ESTABLISHED** |

The unresolved `T_verified` interaction is endpoint-local:

```text
unresolved T_verified interaction
↛ reopen T_instability
```

### R1 replication / transport

R1 directly tested the A5↔A7 replication discrepancy for the labeled-scaffold, E0-only prior-state prose-versus-fields effect on `T_instability` across four fresh disjoint prestate cohorts.

```text
C1  +0.030043
C2  +0.045267
C3  +0.025974
C4  +0.034615

Δ_common = +0.033975
95% CI   = [+0.021316,+0.047791]
p        = 0.00019996
```

The effect is nonzero/reproduced while the entire common-effect interval lies inside the inherited `±0.05` practical region.

Transport diagnostic:

```text
Q = 1.120334
df = 3
p = 0.772168
I² = 0
tau²_DL = 0
```

Authorized:

```text
observed cohort effects
→ compatible with a common-effect model
```

Not authorized:

```text
compatible with common effect
→ proven transport invariance
```

See [`results/PILOT0_TERMINAL_RECORD.md`](results/PILOT0_TERMINAL_RECORD.md) for the complete terminal lineage and authority boundary.

## Pilot 0 stopping rule

Pilot 0 is not closed because nothing else could theoretically be tested.

It is closed because nothing else is presently justified to test.

```text
sufficiently contracted live hypothesis space
+
alternatives discriminated
+
surviving effects replicated / bounded
+
remaining uncertainty locally contained
+
no sufficiently discriminating next experiment
────────────────────────────────────────────
                        ↓
                      STOP
```

Keep explicit:

```text
STOP
≠ truth
≠ completeness
≠ certainty

STOP
= no presently justified escalation
```

Therefore:

```text
A-series representation localization
→ sufficiently resolved

R1 replication/transport
→ closed

A8
→ NOT EARNED

R2
→ NOT EARNED

additional T_instability decomposition
→ NOT EARNED
```

Any future empirical branch requires a genuinely new scientific question and a fresh pre-outcome contract.

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

## Evidence and authority boundaries

Keep distinct:

```text
causal heterogeneity
≠ longitudinal dynamics
≠ equilibrium
≠ stationary stochastic distribution
```

A scoped randomized result does not automatically establish:

- a causal effect of the moderator itself;
- construct identity;
- mechanism;
- discriminative correction capacity;
- cross-model or cross-domain transport;
- transport invariance;
- safety;
- equilibrium;
- theory validation.

See [`docs/CLAIMS_AND_NONCLAIMS.md`](docs/CLAIMS_AND_NONCLAIMS.md).

## Synthetic red-team track

The repository retains synthetic and adversarial checks for assay failure modes:

- [`docs/RED_TEAM_PROTOCOL.md`](docs/RED_TEAM_PROTOCOL.md)
- [`docs/JUMP_WORLD_STRESS_TESTS.md`](docs/JUMP_WORLD_STRESS_TESTS.md)
- [`results/SYNTHETIC_ASSAY_REFERENCE.md`](results/SYNTHETIC_ASSAY_REFERENCE.md)

Synthetic survival is development evidence only:

```text
synthetic red-team survival
↛ plumbing success
↛ real randomized evidence
↛ replication
↛ transport invariance
↛ stable law
```

## Prompt and historical tracks

Historical prompt snapshots remain intact:

- [`prompts/CARS-v0.1.md`](prompts/CARS-v0.1.md)
- [`prompts/CARS-v0.2-CANDIDATE.md`](prompts/CARS-v0.2-CANDIDATE.md)

The current role-separated control protocol is:

- [`prompts/CARS-CONTROL-PROTOCOL.md`](prompts/CARS-CONTROL-PROTOCOL.md)

Historical catalyst and recursive-correction artifacts remain research lineage, not validated current theory.

## Repository map

```text
prompts/
  CARS-CONTROL-PROTOCOL.md

docs/
  ASSAY_SPEC.md
  MEASUREMENT_BOUNDARY.md
  RED_TEAM_PROTOCOL.md
  CLAIMS_AND_NONCLAIMS.md
  FAILURE_MODEL.md
  RESEARCH_CONTRACT.md

experiments/
  README.md
  PILOT0_MMLU_PRO.md
  PILOT0_PROVENANCE.md
  PILOT0_*_CONFIG.json
  LLM_ASSAY_PROTOCOL.md

results/
  README.md
  PILOT0_TERMINAL_RECORD.md
  SYNTHETIC_ASSAY_REFERENCE.md

scripts/
  frozen Pilot 0 runners / analyzers
  randomized-assay utilities
  synthetic red-team utilities
```

## Notebook philosophy

The repository should remain reopenable, testable, and cheap to revise without confusing notebook evolution with empirical progress.

```text
simple experiment first
→ complex explanation only if earned
```

Pilot 0 adds the complementary terminal discipline:

```text
CORRECTION
→ contraction of the live hypothesis space
→ not perpetual hypothesis generation
```

Successful correction can terminate when no remaining uncertainty supports a sufficiently discriminating next experiment.

## Authorship and workflow

Research direction, conceptual architecture, claims, and evaluation priorities are directed by **Björn Janson**. AI systems are used as research collaborators and implementation tools for drafting, critique, repository construction, comparison, code assistance, formalization, simulation, and adversarial development.

AI-assisted agreement is not independent scientific validation. See [`docs/PROVENANCE.md`](docs/PROVENANCE.md).

## License

MIT. See [`LICENSE`](LICENSE).

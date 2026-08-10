# CARS — Controlled Adaptive Reasoning System

> **Status:** living research notebook. The project now separates a broad functional intelligence conjecture from a subtractive empirical program. Pilot 0 is closed, the Pilot-1/ID1 synthetic predictive-resource lineage is closed at its tested questions, and an independent future-plasticity forecast benchmark is frozen but has **no scientific result yet** because canonical MNIST was unavailable in the active execution environment.

## Top-level theory

Canonical statement:

> **Intelligence is the capacity of a system to convert appropriately informative new evidence into increased expected future viability.**

Compact shorthand:

```text
I_t ∝ Δ_E[V_{t+h}]
```

The proportionality symbol is shorthand, **not** a claimed linear law. The scientifically meaningful commitment is:

```text
greater evidence-mediated expected future-viability gain
→ greater intelligence under the conjecture
```

The theory is currently a **conjecture**. Its mechanism is unspecified and current empirical support is not established.

See:

- [`docs/INTELLIGENCE_THEORY.md`](docs/INTELLIGENCE_THEORY.md)
- [`docs/CURRENT_RESEARCH_STATE.md`](docs/CURRENT_RESEARCH_STATE.md)

## Theory ≠ mechanism

The theory is functional rather than architectural.

```text
informative evidence
        ↓
system-mediated update
        ↓
changed state / policy / representation / memory
        ↓
changed future trajectory
        ↓
changed expected viability
```

Nothing in the current evidence establishes a special intelligence mechanism, correction controller, correction-specific state, adaptive-complexity variable, or novel predictive-state ontology.

Keep frozen:

```text
current performance
≠ intelligence

learning speed
≠ intelligence

behavioral change
≠ intelligence

prediction
≠ intelligence

evidence response
≠ viability gain

viability gain without evidence mediation
≠ evidence-conversion intelligence
```

## Current empirical hierarchy

```text
THEORY
Intelligence concerns evidence → future viability
        │
        ▼
FORECASTABILITY
Can present state predict future response to unseen tasks/evidence?
        │
        ▼
PREDICTIVE STRUCTURE
What ordinary state variables explain that response?
        │
        ▼
RESOURCE QUESTION
How much representation / computation / data is required?
        │
        ▼
ADAPTATION
Is the response actually evidence-mediated change?
        │
        ▼
VIABILITY
Does that change improve future outcomes?
        │
        ▼
CAUSAL MEDIATION
Did the system's use of evidence cause the gain?
        │
        ▼
CONSTRUCT VALIDITY
Does this relation earn the name intelligence?
```

Each arrow is a separate empirical burden. A benchmark is not allowed to inherit the conclusion it is meant to earn.

## CARS control protocol

CARS is the epistemic-control layer around the research process. It governs how evidence is localized, interpreted, revised, and bounded.

```text
feedback
→ localize
→ discriminate
→ revise minimally
→ retest
→ stop when no discriminating residual remains
```

Core rules include:

```text
possibility ≠ authority
failure ≠ cause
A_leave ↛ A_adopt
validated consequence grants local authority only
```

Current protocol:

- [`prompts/CARS-CONTROL-PROTOCOL.md`](prompts/CARS-CONTROL-PROTOCOL.md)

CARS does not make any assay hypothesis true. Empirical results do not validate CARS merely because CARS helped interpret them.

## Pilot 0 — closed

Pilot 0 used Qwen3-4B on MMLU-Pro and tested the literal moderator:

```text
I₁ = 1 - P(correct)
```

The original hypothesis was:

```text
higher I₁
→ greater causal benefit from verified-error feedback
```

Terminal result:

```text
H1
→ NOT SUPPORTED
```

`I₁` retained modest criterion validity for initial error likelihood, but correction-related validity was not established:

```text
error detection
≠ correction susceptibility
```

The diagnostic program nevertheless localized representation-dependent transition effects.

### Pilot 0 terminal endpoint ledger

| Object | Status |
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

Authoritative records:

- [`experiments/PILOT0_MMLU_PRO.md`](experiments/PILOT0_MMLU_PRO.md)
- [`experiments/PILOT0_PROVENANCE.md`](experiments/PILOT0_PROVENANCE.md)
- [`results/PILOT0_TERMINAL_RECORD.md`](results/PILOT0_TERMINAL_RECORD.md)

Pilot 0 remains read-only. No A8, R2, or further `T_instability` decomposition is earned by that lineage.

## Post-Pilot-0 subtraction

The project repeatedly attempted to isolate a correction-specific scientific object. Candidate controller, transition, lineage, sufficiency, discovery, compression, and challengeability formulations were progressively absorbed by ordinary state, dynamics, information, policy/search, update, controlled observation, predictive-state, and decision-theoretic machinery.

Current scoped conclusion:

> **Within the audited Pilot-0 phenomenon space, no empirically independent correction-specific primitive is presently required.**

Keep explicit:

```text
no residual found
≠ no residual exists

generic representability
≠ complete mechanistic explanation

negative differentiation
≠ philosophical reduction
```

The detailed historical subtraction branches remain provenance. The canonical current summary is in [`docs/CURRENT_RESEARCH_STATE.md`](docs/CURRENT_RESEARCH_STATE.md).

## Pilot 1 — predictive-resource subtraction toy

Pilot 1 asked a genuinely new synthetic question using:

```text
F — frozen dynamics
N — exogenously changing dynamics
A — intervention-coupled changing dynamics
```

A restricted predictor showed a small A>N distortion on structurally held-out order reversals. But with full state and known equations, an exact simulator predicted both N and A with zero distortion.

Therefore:

```text
estimator-level structural-generalization difference
→ YES

intrinsic adaptive predictive-resource burden
→ NOT DEMONSTRATED
```

Record:

- [`results/PILOT1_PREDICTIVE_RESOURCE_TOY_MATCH1.md`](results/PILOT1_PREDICTIVE_RESOURCE_TOY_MATCH1.md)

## ID1 — finite-data system identification, closed

ID1 hid the transition/update equations and required finite-data identification.

A weak P2 identifier showed a visible A/N gap. A stronger generic P3 identifier removed approximately **99.46%** of the high-resource gap.

At the frozen high-resource P3 cell:

```text
ID1
A - N = +4.70792e-7 structural NMSE
```

A fresh-seed replication produced:

```text
ID1-R1
A - N = -3.90770244e-6
```

The sign reversed, sample-threshold crossings remained identical, and no distinct sample-scaling regime was established.

Therefore:

```text
finite-data adaptive identification burden
→ NOT DEMONSTRATED

distinct sample-complexity regime
→ NOT DEMONSTRATED

ID1 discrepancy
→ CLOSED
```

Records:

- [`results/PILOT1_ID1_SYSTEM_IDENTIFICATION.md`](results/PILOT1_ID1_SYSTEM_IDENTIFICATION.md)
- [`results/PILOT1_ID1_P3_REPLICATION.md`](results/PILOT1_ID1_P3_REPLICATION.md)

Do not run another replication merely to recover the original sign.

## Independent future-plasticity forecast benchmark — frozen

The next authorized benchmark does **not** descend from the failed ID1 toy. It uses an independently established continual-learning phenomenon: plasticity variation under Online Permuted MNIST.

Neutral object:

```text
Γ_t(E*)
=
future learning trajectory from checkpoint S_t
on concealed future task transformation E*
```

Each checkpoint is compared to a matched fresh network on the exact same future task, data order, initialization family, optimizer, and training budget.

The first pass tests only:

```text
G0 — forecastability
G1 — current capability beyond age
G2 — established plasticity variables beyond capability
G3 — broader checkpoint-state sketch beyond plasticity variables
```

Frozen artifacts:

- [`experiments/FUTURE_PLASTICITY_FORECAST.md`](experiments/FUTURE_PLASTICITY_FORECAST.md)
- [`experiments/FUTURE_PLASTICITY_FORECAST_CONFIG.json`](experiments/FUTURE_PLASTICITY_FORECAST_CONFIG.json)
- [`scripts/run_future_plasticity_forecast.py`](scripts/run_future_plasticity_forecast.py)
- [`results/FUTURE_PLASTICITY_FORECAST_STATUS.md`](results/FUTURE_PLASTICITY_FORECAST_STATUS.md)

Current state:

```text
DESIGN          PASS
IMPLEMENTATION  PASS
SMOKE           PASS
CANONICAL DATA  unavailable in active execution environment
SCIENTIFIC RUN  NOT EXECUTED
RESULT          ∅
INTERPRETATION  ∅
```

No surrogate dataset, G4–G6 escalation, new `Z`, new construct, or theory interpretation is authorized before the canonical run.

## Current research contract

Repository-level authority and escalation rules:

- [`docs/RESEARCH_CONTRACT.md`](docs/RESEARCH_CONTRACT.md)
- [`docs/CLAIMS_AND_NONCLAIMS.md`](docs/CLAIMS_AND_NONCLAIMS.md)
- [`docs/CURRENT_RESEARCH_STATE.md`](docs/CURRENT_RESEARCH_STATE.md)

The governing rule is:

> **The theory specifies what may matter. The empirical program gives ordinary machinery every opportunity to explain it away. Only what survives that subtraction earns additional scientific structure.**

## Repository map

```text
prompts/
  CARS-CONTROL-PROTOCOL.md

docs/
  INTELLIGENCE_THEORY.md
  CURRENT_RESEARCH_STATE.md
  CLAIMS_AND_NONCLAIMS.md
  RESEARCH_CONTRACT.md
  ASSAY_SPEC.md
  MEASUREMENT_BOUNDARY.md
  FAILURE_MODEL.md
  RED_TEAM_PROTOCOL.md

experiments/
  README.md
  PILOT0_*                         historical frozen Pilot 0
  PILOT1_PREDICTIVE_RESOURCE_*    closed synthetic predictive-resource toy
  PILOT1_ID1_*                    closed finite-data identification toy
  FUTURE_PLASTICITY_FORECAST.*    current frozen independent benchmark

results/
  README.md
  PILOT0_TERMINAL_RECORD.md
  PILOT1_PREDICTIVE_RESOURCE_TOY_MATCH1.md
  PILOT1_ID1_SYSTEM_IDENTIFICATION.md
  PILOT1_ID1_P3_REPLICATION.md
  FUTURE_PLASTICITY_FORECAST_STATUS.md

scripts/
  frozen Pilot 0 runners/analyzers
  Pilot 1 / ID1 synthetic runners
  future-plasticity forecast runner
```

## Evidence discipline

```text
smoke
↛ scientific result

predictive gain
↛ causal mechanism

viability gain
↛ evidence mediation

measurable evidence-mediated viability gain
↛ automatically intelligence

successful subtraction
↛ universal completeness
```

The project is allowed to terminate branches with the empty set.

## Authorship and workflow

Research direction, conceptual architecture, claims, and evaluation priorities are directed by **Björn Janson**. AI systems are used as research collaborators and implementation tools for drafting, critique, repository construction, comparison, code assistance, formalization, simulation, and adversarial development.

AI-assisted agreement is not independent scientific validation. See [`docs/PROVENANCE.md`](docs/PROVENANCE.md).

## License

MIT. See [`LICENSE`](LICENSE).

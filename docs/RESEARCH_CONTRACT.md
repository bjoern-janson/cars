# CARS Research Contract

## Status

This is the current repository-level research contract.

It separates:

```text
INTELLIGENCE THEORY
≠
CARS CONTROL PROTOCOL
≠
EMPIRICAL BENCHMARKS
≠
HISTORICAL PILOT-0 ASSAY
```

The theory can remain ambitious only if experiments remain scoped and independently falsifiable.

## Top-level theory

Canonical theory:

- [`INTELLIGENCE_THEORY.md`](INTELLIGENCE_THEORY.md)

Conjecture:

> **Intelligence is the capacity of a system to convert appropriately informative new evidence into increased expected future viability.**

Shorthand:

```text
I_t ∝ Δ_E[V_{t+h}]
```

The proportionality symbol is shorthand, not a linear-law commitment.

The scientifically meaningful ordering claim is:

```text
greater evidence-mediated expected future-viability gain
→ greater intelligence under the conjecture
```

Current status:

```text
THEORY
→ CONJECTURE

MECHANISM
→ UNSPECIFIED

EMPIRICAL SUPPORT
→ NOT ESTABLISHED
```

## Theory-to-evidence burden

The empirical program must not smuggle the theory into lower-level benchmarks.

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
Is the response actually evidence-mediated system change?
        │
        ▼
VIABILITY
Does the change improve future outcomes under a prospectively defined V?
        │
        ▼
CAUSAL MEDIATION
Is the gain attributable to the system's use of evidence?
        │
        ▼
CONSTRUCT VALIDITY
Does the relation explain intelligence better than alternatives?
```

Each arrow is a separate empirical burden.

## Current empirical question

The active frozen benchmark is **not** a direct intelligence test.

It asks:

> **Can prospectively measured checkpoint state forecast how much a continually trained neural network's future trainability will differ from a matched fresh network on the same concealed future task transformation?**

Neutral object:

```text
Γ_t(E*)
=
future learning trajectory produced from checkpoint S_t on E*
```

The frozen benchmark tests only G0–G3:

```text
G0 forecastability
G1 current capability beyond age
G2 selected plasticity measurements beyond capability
G3 broad checkpoint-state sketch beyond selected plasticity measurements
```

Contract:

- [`../experiments/FUTURE_PLASTICITY_FORECAST.md`](../experiments/FUTURE_PLASTICITY_FORECAST.md)
- [`../experiments/FUTURE_PLASTICITY_FORECAST_CONFIG.json`](../experiments/FUTURE_PLASTICITY_FORECAST_CONFIG.json)

Current status:

```text
DESIGN          PASS
IMPLEMENTATION  PASS
SMOKE           PASS
CANONICAL DATA  unavailable in active execution environment
SCIENTIFIC RUN  NOT EXECUTED
RESULT          ∅
INTERPRETATION  ∅
```

No surrogate dataset is authorized merely to obtain a number.

## Future-task concealment contract

The future task identity must not enter checkpoint measurement construction.

Operational ordering:

```text
train continual history
→ reach checkpoint
→ measure checkpoint state
→ freeze measurements
→ only then consume future-task RNG
→ evaluate future learning
```

This prevents future-task identity from leaking into the checkpoint predictors by construction.

## Matched fresh-network control

For every checkpoint/future-task pair, the future learning trajectory is compared against a fresh network trained on the identical future task under matched training conditions.

The benchmark therefore targets:

```text
history-dependent future trainability
```

rather than raw future-task difficulty.

Primary summaries:

```text
ΔAUC
=
AUC(checkpoint future curve)
-
AUC(fresh future curve)

T90_gap
=
T90(checkpoint)
-
T90(fresh)
```

The full learning curve `Γ` remains the scientific object; scalar summaries are reporting projections.

## Forecast hierarchy contract

The first pass compares increasingly rich ordinary predictors:

```text
NULL
→ outer-training mean

AGE
→ task age

CAPABILITY
→ age + current task accuracy/loss

PLASTICITY
→ capability + prospectively frozen trainability/network-state measures

RICH
→ plasticity + fixed 32-D projection of full parameter displacement
```

Evaluation uses grouped out-of-fold prediction by continual-history run, with nested regularization selection and group-bootstrap comparison.

No predictor receives future-task identity as a checkpoint feature.

## Escalation rule

This pass terminates at G0–G3.

```text
G4/G5 cross-family transport
→ NOT AUTHORIZED

G6 compression search
→ NOT AUTHORIZED

new Z
→ NOT AUTHORIZED

new construct
→ NOT AUTHORIZED

new theory
→ NOT AUTHORIZED
```

A failed gate terminates the corresponding escalation.

Examples:

```text
G0 fails
→ no forecastability claim at this measurement/sample resolution

AGE explains most prediction
→ simple temporal trajectory is sufficient at this resolution

PLASTICITY absorbs capability-relative signal
→ ordinary plasticity variables explain the tested increment

RICH ≈ PLASTICITY
→ broad parameter sketch adds little incremental information
```

No negative result is generalized beyond its measurement and benchmark scope.

## Historical Pilot 0 contract

Pilot 0 used a different scientific object and remains closed.

It tested the pre-intervention moderator:

```text
I₁ = 1 - P(correct)
```

against causal response to verified-error feedback.

The original moderation hypothesis was not supported. Subsequent diagnostics localized representation-dependent transition effects.

Authoritative terminal record:

- [`../results/PILOT0_TERMINAL_RECORD.md`](../results/PILOT0_TERMINAL_RECORD.md)

Do not reinterpret the active future-plasticity benchmark as a continuation or retrofit of Pilot 0.

## Pilot 1 / ID1 contract boundary

The synthetic predictive-resource and finite-data system-identification lineages are closed at their tested questions.

They established no intrinsic adaptive-specific predictive-resource or sample-complexity burden.

Records:

- [`../results/PILOT1_PREDICTIVE_RESOURCE_TOY_MATCH1.md`](../results/PILOT1_PREDICTIVE_RESOURCE_TOY_MATCH1.md)
- [`../results/PILOT1_ID1_SYSTEM_IDENTIFICATION.md`](../results/PILOT1_ID1_SYSTEM_IDENTIFICATION.md)
- [`../results/PILOT1_ID1_P3_REPLICATION.md`](../results/PILOT1_ID1_P3_REPLICATION.md)

Do not increase horizon, intervention complexity, adaptive mechanism complexity, or replication count merely to recover a vanished discrepancy.

## Measurement contract

Measurement partly constitutes the identity of the scientific object.

For every result whose evidential status matters, record:

```text
scientific object
measurement variables
pre-outcome contract
future-data concealment rule where applicable
data-generation / assignment process
predictor / estimator family
resource budget
held-out structure
uncertainty
protocol deviations
claim actually earned
```

A changed object receives a new contract or explicit comparison condition rather than being silently treated as the same experiment.

## Identification and causal contract

Predictive forecastability is not causal evidence.

```text
prediction
↛ causal mechanism
```

The top-level theory eventually requires evidence-mediated viability gain, which is a stronger causal object than future trainability forecasting.

Do not infer:

```text
future trainability difference
→ viability gain

viability gain
→ evidence mediation

evidence mediation
→ construct validity as intelligence
```

Each transition requires a separate identification strategy and prospective measurement definition.

## Construct-validity contract

Even if an evidence-mediated future-viability quantity becomes measurable and causal, it is not automatically intelligence.

Construct validity requires comparison against alternative intelligence accounts and independent outcomes that an intelligence measure is expected to explain.

The repository currently makes no construct-validity claim.

## CARS prompt experiment

The CARS control protocol can separately be tested as a reasoning intervention against baseline and generic careful-reasoning controls.

Prompt efficacy does not establish the intelligence conjecture, Pilot-0 assay, predictive-resource results, or future-plasticity forecastability.

## Subtraction rule

When an apparent special effect appears:

```text
apparent discrepancy
→ strongest ordinary comparator
→ shallowest failure localization
→ minimal repair / stronger estimator
→ held-out retest
→ independent replication if warranted
→ transport only if earned
→ new construct only if residual survives
```

The repository is allowed to end with:

```text
residual = ∅
```

## Claim rule

A positive result authorizes only the tested object under the measurement, identification, estimator, and scope conditions actually used.

A negative result is localized before revision.

A strong contradiction at the scientific-proposition level requires that shallower explanations—measurement, identification, representation, estimator adequacy, implementation, and finite-sample variation—have been sufficiently ruled out.

## Version discipline

Record the exact protocol, configuration, code, dataset identity, estimator, seed streams, and repository commit for any result whose authority matters.

Smoke/development streams remain separate from scientific outcome streams.

## Governing sentence

> **The theory specifies what may matter. The empirical program gives ordinary machinery every opportunity to explain it away. Only what survives that subtraction earns additional scientific structure.**

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

ASI-0 does not jump this hierarchy. It tests only a lower mechanistic fragment:

```text
development evidence
→ modification selection
→ bounded agent modification
→ concealed future capability
```

## Current live causal question — ASI-0

ASI-0 is **not** a direct intelligence, viability, recursive-self-improvement, or ASI test.

It asks:

> **Can a fixed-base-model agent use development evidence to select bounded modifications that produce greater concealed future capability than evidence-misaligned selection under matched resources?**

Treatment object:

```text
A = evidence → target assignment mechanism
```

Primary estimand:

```text
Δ_align
=
E[Y_concealed | do(A = aligned)]
-
E[Y_concealed | do(A = misaligned)]
```

This is an interventional contrast. The randomized/permuted assignment mechanism is what licenses the causal reading.

Frozen contract:

- [`../experiments/ASI0_EVIDENCE_ASSIGNMENT.md`](../experiments/ASI0_EVIDENCE_ASSIGNMENT.md)
- [`../experiments/ASI0_EVIDENCE_ASSIGNMENT_CONFIG.json`](../experiments/ASI0_EVIDENCE_ASSIGNMENT_CONFIG.json)
- [`../scripts/run_asi0_assignment_experiment.py`](../scripts/run_asi0_assignment_experiment.py)
- [`../results/ASI0_EVIDENCE_ASSIGNMENT_STATUS.md`](../results/ASI0_EVIDENCE_ASSIGNMENT_STATUS.md)

Current status:

```text
CAUSAL DESIGN SKELETON   FROZEN
IMPLEMENTATION            PASS
SYNTHETIC SMOKE           PASS
CANONICAL MODEL           NOT YET FROZEN
CANONICAL TARGET MANIFEST NOT YET FROZEN
CONCEALED SUITE           NOT YET FROZEN
SCIENTIFIC RUN            NOT EXECUTED
Δ_align                   UNKNOWN
INTERPRETATION            ∅
```

## ASI-0 assignment contract

For each target `i` with development evidence `E_i`:

```text
ALIGNED
E_i → target i

MISALIGNED
E_{π(i)} → target i
π(i) ≠ i
```

The misaligned arm is a prospectively seeded within-stratum derangement. It is not a nonsense-evidence control.

The design preserves generic information structure while breaking relevance.

Where feasible, matching strata preserve:

```text
task family
evidence type
trace-length bucket
difficulty bucket
candidate count
resource budget
```

A stratum unable to support a derangement is ineligible for the primary contrast.

## ASI-0 matched candidate-pool contract

The candidate pool is frozen before assignment and reused exactly across the primary aligned/misaligned pair.

```text
same target
same candidate IDs
same candidate texts
same candidate count
same candidate-generation machinery
same candidate-generation evidence access

ONLY CHANGE
assigned evidence used for candidate selection
```

Candidate generation is not the treatment. Correct evidence assignment is the treatment.

This is intentionally a hard null: generic candidate diversity and generic information richness are available to both primary arms.

## ASI-0 fixed-base and mutation contract

Every branch resets from the identical frozen base-agent snapshot.

Frozen first-pass mutation surface:

```text
one bounded textual policy patch
one mutable policy slot
frozen weights
frozen tool permissions
no cross-branch carryover
no architecture expansion
no recursive self-modification
```

Therefore:

```text
ASI-0
↛ recursive self-improvement
```

Changing the mutation surface after seeing `Δ_align` creates a new experiment rather than rescuing ASI-0.

## ASI-0 secondary controls

Secondary controls:

```text
STATIC
RANDOM-EDIT
```

They help bound repeated execution and arbitrary mutation, but:

```text
SELF vs RANDOM
→ useful control
→ insufficient attribution test
```

The primary attribution test remains:

```text
E-ALIGNED
vs
E-MISALIGNED
```

## ASI-0 gates

The frozen gate order is:

```text
resource matched
        ↓
protected regressions
        ↓
concealed confirmation
        ↓
structural holdout
        ↓
replication if positive
```

Every primary arm uses the same protected-regression gate. A rejected patch becomes an explicit no-op rather than receiving a hand-selected replacement.

The concealed evaluator must be blind to arm and must not feed concealed outcomes back into candidate generation or selection.

The task family must define structural holdout prospectively; surface novelty alone is insufficient.

## ASI-0 scientific-instance gate

The current config intentionally contains:

```text
MUST_FREEZE_BEFORE_SCIENTIFIC_RUN
```

for unresolved canonical instance fields such as the base model/revision, selection configuration, candidate count, evaluator, and concealed suite.

The runner refuses scientific manifest preparation while any such placeholder remains.

```text
smoke success
↛ preregistration complete
↛ scientific result
```

## ASI-0 result contract

For each arm:

```text
G_arm
=
Y_concealed(modified-or-gated agent)
-
Y_concealed(frozen base agent)
```

Primary report:

```text
mean G_aligned
mean G_misaligned
Δ_align
target-cluster bootstrap interval
number of targets / replicate pairs
protected-regression pass rate by arm
```

Targets, not branch rows, are the primary clustering unit.

### Maximum positive interpretation

A positive replicated result authorizes, at most:

> **Correct evidence-to-target assignment causally improves bounded modification selection and downstream concealed performance under the tested conditions.**

Do not infer:

```text
future capability gain
→ viability gain

viability gain
→ intelligence

evidence-aligned modification
→ recursive self-improvement

ASI-0
→ ASI
```

### Null interpretation

If:

```text
E-aligned ≈ E-misaligned
```

then the authorized interpretation is:

> **Correct semantic assignment of development evidence adds no detectable value under the tested mutation surface, task family, resource envelope, and measurement resolution.**

Do not rescue a null by:

```text
inventing a new Z
expanding the mutation surface post hoc
increasing autonomy post hoc
claiming the effect must emerge at scale
```

If the effect disappears, ASI-0 closes at that boundary unless a genuinely new independently motivated question is introduced.

## Independent future-plasticity contract

The future-plasticity benchmark remains independently frozen and pending canonical MNIST. ASI-0 neither supersedes its scientific object nor inherits authority from it.

Neutral object:

```text
Γ_t(E*)
=
future learning trajectory produced from checkpoint S_t on E*
```

Frozen G0–G3 questions:

```text
G0 forecastability
G1 current capability beyond age
G2 selected plasticity measurements beyond capability
G3 broad checkpoint-state sketch beyond selected plasticity measurements
```

Artifacts:

- [`../experiments/FUTURE_PLASTICITY_FORECAST.md`](../experiments/FUTURE_PLASTICITY_FORECAST.md)
- [`../experiments/FUTURE_PLASTICITY_FORECAST_CONFIG.json`](../experiments/FUTURE_PLASTICITY_FORECAST_CONFIG.json)
- [`../results/FUTURE_PLASTICITY_FORECAST_STATUS.md`](../results/FUTURE_PLASTICITY_FORECAST_STATUS.md)

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

No surrogate dataset, G4–G6 escalation, new `Z`, new construct, or theory interpretation is authorized merely to obtain a result.

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

Do not reinterpret ASI-0 or future plasticity as a retrofit of Pilot 0.

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

ASI-0 uses randomized/permuted assignment to identify a narrower causal object, but even a positive assignment effect is not a viability result.

Keep explicit:

```text
correct evidence assignment
→ bounded concealed capability gain
↛ viability gain
↛ intelligence
↛ ASI
```

The top-level theory eventually requires evidence-mediated viability gain, which is a stronger object than either future-trainability forecasting or ASI-0 capability attribution.

Each transition requires a separate identification strategy and prospective measurement definition.

## Construct-validity contract

Even if an evidence-mediated future-viability quantity becomes measurable and causal, it is not automatically intelligence.

Construct validity requires comparison against alternative intelligence accounts and independent outcomes that an intelligence measure is expected to explain.

The repository currently makes no construct-validity claim.

## CARS prompt experiment

The CARS control protocol can separately be tested as a reasoning intervention against baseline and generic careful-reasoning controls.

Prompt efficacy does not establish the intelligence conjecture, Pilot-0 assay, predictive-resource results, future-plasticity forecastability, or ASI-0 evidence-assignment leverage.

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

ASI-0 adds the specific subtraction:

```text
SELF improves
→ subtract search / mutation / compute / evaluator feedback

E-aligned improves
→ match information quantity / candidate diversity

E-aligned > E-misaligned
→ correct evidence-target relation has incremental leverage
→ STOP
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

Record the exact protocol, configuration, code, dataset identity, estimator, seed streams, assignment mechanism, and repository commit for any result whose authority matters.

Smoke/development streams remain separate from scientific outcome streams.

## Governing sentence

> **The theory specifies what may matter. The empirical program gives ordinary machinery every opportunity to explain it away. Only what survives that subtraction earns additional scientific structure.**

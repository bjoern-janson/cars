# Experiments

## Current status

```text
Pilot 0
→ CLOSED / READ-ONLY

Pilot 1 predictive-resource toy
→ CLOSED AT TESTED QUESTION

ID1 finite-data identification
→ CLOSED

Future plasticity forecast benchmark
→ FROZEN G0–G3 CONTRACT
→ scientific result pending canonical MNIST data
```

The current repository-level theory and authority state are documented in:

- [`../docs/INTELLIGENCE_THEORY.md`](../docs/INTELLIGENCE_THEORY.md)
- [`../docs/CURRENT_RESEARCH_STATE.md`](../docs/CURRENT_RESEARCH_STATE.md)

## Pilot 0 — closed

Pilot 0 tested whether the literal moderator:

```text
I₁ = 1 - P(correct)
```

predicted larger causal benefit from verified-error feedback under one frozen Qwen3-4B / MMLU-Pro configuration.

The original moderation hypothesis was **not supported**. The subsequent diagnostic program localized representation-dependent transition effects and closed after R1 replication/transport.

Authoritative terminal record:

- [`../results/PILOT0_TERMINAL_RECORD.md`](../results/PILOT0_TERMINAL_RECORD.md)

Frozen protocol/provenance:

- [`PILOT0_MMLU_PRO.md`](PILOT0_MMLU_PRO.md)
- [`PILOT0_PROVENANCE.md`](PILOT0_PROVENANCE.md)

Keep explicit:

```text
Pilot 0 CLOSED
≠ theory established
≠ certainty
≠ zero uncertainty

CLOSED
= no presently justified escalation from that lineage
```

No A8, R2, or additional `T_instability` decomposition is earned.

## Pilot 1 — predictive-resource subtraction toy

Pilot 1 introduced a new synthetic question independent of Pilot 0.

System ladder:

```text
F — frozen dynamics
N — exogenously changing dynamics
A — intervention-coupled changing dynamics
```

The first restricted predictor showed a small structural-generalization A>N gap on unseen order reversals. After pairing the realized initial states across F/N/A, that descriptive pattern persisted under the restricted estimator.

However, the exact known-dynamics simulator predicted N and A with:

```text
D = 0
```

from the same full-state dimensionality and essentially the same per-step computational class.

Therefore:

```text
estimator-level structural-generalization difference
→ YES

intrinsic adaptive predictive-resource burden
→ NOT DEMONSTRATED
```

Artifacts:

- [`PILOT1_PREDICTIVE_RESOURCE_TOY.md`](PILOT1_PREDICTIVE_RESOURCE_TOY.md)
- [`PILOT1_PREDICTIVE_RESOURCE_TOY_CONFIG.json`](PILOT1_PREDICTIVE_RESOURCE_TOY_CONFIG.json)
- [`PILOT1_PREDICTIVE_RESOURCE_TOY_MATCH1_CONFIG.json`](PILOT1_PREDICTIVE_RESOURCE_TOY_MATCH1_CONFIG.json)
- [`../results/PILOT1_PREDICTIVE_RESOURCE_TOY_MATCH1.md`](../results/PILOT1_PREDICTIVE_RESOURCE_TOY_MATCH1.md)

The unpaired Run 1 remains quarantined as a design-repair record:

- [`../results/PILOT1_PREDICTIVE_RESOURCE_TOY_RUN1.md`](../results/PILOT1_PREDICTIVE_RESOURCE_TOY_RUN1.md)

Do not tune this toy to enlarge the A/N difference.

## ID1 — finite-data system identification, closed

ID1 changed exactly one scientific dimension:

```text
known transition/update equations
→ hidden from learner
```

The learner had to identify local dynamics from finite trajectories and recursively predict structurally held-out order reversals.

Frozen contract:

- [`PILOT1_ID1_SYSTEM_IDENTIFICATION.md`](PILOT1_ID1_SYSTEM_IDENTIFICATION.md)
- [`PILOT1_ID1_SYSTEM_IDENTIFICATION_CONFIG.json`](PILOT1_ID1_SYSTEM_IDENTIFICATION_CONFIG.json)

A weak P2 identifier showed a visible A/N gap. The stronger generic P3 identifier removed approximately 99.46% of the high-resource gap.

The remaining tiny positive P3 discrepancy was then replicated on a fresh seed under an unchanged generator/grammar/estimator/endpoint and reversed sign.

Replication contract:

- [`PILOT1_ID1_P3_REPLICATION_CONFIG.json`](PILOT1_ID1_P3_REPLICATION_CONFIG.json)

Terminal interpretation:

```text
finite-data adaptive identification burden
→ NOT DEMONSTRATED

distinct sample-complexity regime
→ NOT DEMONSTRATED

ID1 discrepancy
→ CLOSED
```

Records:

- [`../results/PILOT1_ID1_SYSTEM_IDENTIFICATION.md`](../results/PILOT1_ID1_SYSTEM_IDENTIFICATION.md)
- [`../results/PILOT1_ID1_P3_REPLICATION.md`](../results/PILOT1_ID1_P3_REPLICATION.md)

Do not run another replication merely to recover the original sign. Longer horizons, richer intervention algebra, and a more complicated adaptive mechanism are not earned by ID1.

## Future plasticity forecast benchmark — current frozen experiment

This benchmark is independently motivated by established continual-learning plasticity variation. It does not descend from ID1 and does not use the A/N framing.

Neutral object:

```text
Γ_t(E*)
=
future learning trajectory from checkpoint S_t
on a concealed future task transformation E*
```

Each checkpoint is paired with a fresh network trained on the exact same future Permuted-MNIST task and example order.

Frozen G0–G3 contract:

- [`FUTURE_PLASTICITY_FORECAST.md`](FUTURE_PLASTICITY_FORECAST.md)
- [`FUTURE_PLASTICITY_FORECAST_CONFIG.json`](FUTURE_PLASTICITY_FORECAST_CONFIG.json)

Runner:

- [`../scripts/run_future_plasticity_forecast.py`](../scripts/run_future_plasticity_forecast.py)

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

Status:

- [`../results/FUTURE_PLASTICITY_FORECAST_STATUS.md`](../results/FUTURE_PLASTICITY_FORECAST_STATUS.md)

Frozen full-run command once canonical MNIST is provisioned:

```bash
python scripts/run_future_plasticity_forecast.py \
  experiments/FUTURE_PLASTICITY_FORECAST_CONFIG.json \
  --json-out results/future_plasticity_forecast_result.json
```

No substitute dataset, G4–G6 escalation, new `Z`, new construct, or theory claim is authorized before the canonical G0–G3 outcome.

## General assay and synthetic red-team utilities

The repository retains the Pilot-0 assay/red-team tooling for provenance and reusable methodological checks.

Synthetic assay red-team:

```bash
python scripts/run_assay_red_team.py \
  --seed 20260809 \
  --n 20000 \
  --json-out results/synthetic_assay_reference.json
```

Threshold / rare-jump stress tests:

```bash
python scripts/run_jump_worlds.py \
  --seed 20260809 \
  --n 20000 \
  --json-out results/jump_worlds_reference.json
```

General randomized LLM assay:

- [`LLM_ASSAY_PROTOCOL.md`](LLM_ASSAY_PROTOCOL.md)

These are not the active future-plasticity benchmark and do not inherit its authority.

## Evidence ladder

```text
smoke / synthetic plumbing
↛ scientific result

restricted estimator difference
↛ intrinsic complexity

predictive forecastability
↛ causal mechanism

future learning difference
↛ viability gain

viability gain
↛ evidence-mediated intelligence
```

A new experiment requires a genuinely discriminating question and a fresh pre-outcome contract.
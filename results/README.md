# Results

## Canonical authority state

```text
Pilot 0                     CLOSED
Pilot 1 predictive toy      CLOSED
ID1                         CLOSED
Future plasticity forecast  UNOBSERVED / FROZEN
ASI-0                       CLOSED NEGATIVE PRIMARY
```

Canonical repository state:

- [`../docs/CURRENT_RESEARCH_STATE.md`](../docs/CURRENT_RESEARCH_STATE.md)

## ASI-0

Terminal record:

- [`ASI0_TERMINAL_RECORD.md`](ASI0_TERMINAL_RECORD.md)

Mechanism diagnosis:

- [`ASI0_PRIMARY_MECHANISM_FAILURE_REPORT.md`](ASI0_PRIMARY_MECHANISM_FAILURE_REPORT.md)

Status ledger:

- [`ASI0_EVIDENCE_ASSIGNMENT_STATUS.md`](ASI0_EVIDENCE_ASSIGNMENT_STATUS.md)

Frozen primary:

```text
C      0
A      0
L_C    0
L_A    0
PRIMARY STOP
REPLICATION NOT AUTHORIZED
ASI-0 GREEN FALSE
```

Mean concealed scores:

```text
base         0.20833333333333331
aligned      0.20833333333333331
misaligned   0.20833333333333331
random-edit  0.20833333333333331
```

Selection / acceptance:

```text
aligned valid selection      14/16
misaligned valid selection   14/16
aligned admission             0/16
misaligned admission          0/16
```

Post-outcome diagnosis:

```text
pool property:
15/16 frozen candidate patches failed baseline protected-behavior preservation

realized-arm property:
28/28 valid selected patches were rejected

all valid selected patches newly failed exact_PINE
```

Earned interpretation:

> Under the frozen proposal + protected-acceptance policy, correctly assigned development evidence produced no concealed capability gain and no incremental outcome leverage relative to misaligned assignment.

ASI-0 is immutable. It is not to be rerun as a rescue, and replication was not authorized.

## Pilot 0

- [`PILOT0_TERMINAL_RECORD.md`](PILOT0_TERMINAL_RECORD.md)

The original moderation hypothesis was not supported. Later diagnostic work established scoped representation-dependent transition effects, including a replicated but practically small prior-state-encoding effect on `T_instability`.

No A8, R2, or further localization is authorized from that lineage.

## Pilot 1 predictive-resource toy

- [`PILOT1_PREDICTIVE_RESOURCE_TOY_MATCH1.md`](PILOT1_PREDICTIVE_RESOURCE_TOY_MATCH1.md)
- [`PILOT1_PREDICTIVE_RESOURCE_TOY_RUN1.md`](PILOT1_PREDICTIVE_RESOURCE_TOY_RUN1.md) — quarantined initial run

The restricted predictor showed a structural-generalization difference, but exact known-dynamics prediction removed the apparent intrinsic adaptive burden.

## ID1 finite-data identification

- [`PILOT1_ID1_SYSTEM_IDENTIFICATION.md`](PILOT1_ID1_SYSTEM_IDENTIFICATION.md)
- [`PILOT1_ID1_P3_REPLICATION.md`](PILOT1_ID1_P3_REPLICATION.md)

A stronger generic identifier removed approximately 99.46% of the earlier high-resource gap. The remaining tiny discrepancy reversed sign under fresh-seed replication. No adaptive-specific sample-complexity regime was established.

## Future plasticity forecast

- [`FUTURE_PLASTICITY_FORECAST_STATUS.md`](FUTURE_PLASTICITY_FORECAST_STATUS.md)

```text
DESIGN          PASS
IMPLEMENTATION  PASS
SMOKE           PASS
SCIENTIFIC RUN  NOT EXECUTED
RESULT          UNOBSERVED
```

No surrogate result has scientific authority.

## Reporting rule

Every result package should preserve:

```text
scientific object
measurement structure
pre-outcome contract
assignment / data-generation process
estimator
resource budget
held-out structure
uncertainty
protocol deviations
claim actually earned
stopping / replication authorization
```

Keep result surfaces separate. A positive or negative result on one surface does not automatically acquire authority on another.

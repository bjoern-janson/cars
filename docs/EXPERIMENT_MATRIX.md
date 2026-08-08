# Experiment Matrix

## Minimum experiment

| Condition | Intervention | Purpose |
|---|---|---|
| B0 | none | native model behavior |
| B1 | Generic Careful-Reasoning Control v0.1 | generic deliberation/control condition |
| C0 | CARS v0.1 | candidate structured intervention |

## Recommended extensions

| Condition | Change | Main question |
|---|---|---|
| A1 | remove representation-escalation gate | does the gate reduce over-escalation? |
| A2 | remove departure/adoption separation | does it reduce successor capture? |
| A3 | remove unresolved-state permission | does it prevent forced conclusions? |
| A4 | remove independence emphasis | does it improve common-mode evidence handling? |
| A5 | remove retest requirement | does it improve behavioral transfer? |
| A6 | remove belief/decision separation | does it help decisions under uncertainty? |
| A7 | invariants only | are compact principles sufficient? |

## Primary analysis

Do not report only one aggregate score. At minimum compare:

- substantive task success;
- over-update rate;
- missed-update rate;
- premature representation-escalation rate;
- premature successor-adoption rate;
- unjustified unresolved rate;
- common-mode evidence errors;
- correction transfer;
- token/latency/search cost.

## Important comparison

If CARS beats B0 but not B1, the evidence supports a generic-deliberation explanation more strongly than a CARS-specific mechanism.

If CARS beats B1 only on internally authored tasks, external transfer remains unresolved.

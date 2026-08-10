# Pilot 0 — Abstraction Gate

## Status

```text
PILOT 0
→ READ-ONLY EMPIRICAL RECORD

PILOT0_DECISION_TRACE.md
→ PROVENANCE PASS

PILOT0_HUMAN_JUDGMENT_AUDIT.md
→ SCHEMA / FIDELITY PASS

THIS DOCUMENT
→ ABSTRACTION REJECTION GATE
→ NOT PRIMITIVE EXTRACTION
→ NOT A CONTROLLER SPECIFICATION
→ NOT A NEW PILOT
```

This artifact asks one narrow question:

> **Which, if any, observed decision structures survive abstraction beyond Pilot 0 without importing an unrecorded rule?**

It is a rejection mechanism, not a theory-building document.

## Authority boundary

```text
observed historical component
↛ controller primitive
```

A candidate abstraction survives only if every gate below is `YES`.

```text
ANY NO
→ NOT EARNED

UNKNOWN
→ NO
```

No `PROBABLY`, `PENDING`, or partial-pass state is allowed.

A surviving abstraction is only a **candidate abstraction**. Survival here does not authorize controller specification, Pilot 1, or a new experiment.

---

# Binary abstraction gate

| Gate | Question |
| --- | --- |
| `G1` | Is the component actually evidenced in the repaired trace / passing audit? |
| `G2` | Does it represent a functionally distinct operation rather than merely a descriptive feature of this case? |
| `G3` | Is the distinction recurrent across multiple audited decision components, or independently motivated without relying on the desired controller architecture? |
| `G4` | Can its authority consequence be stated without hindsight? |
| `G5` | Can its input boundary be specified from the audited record without inventing missing variables or comparison rules? |
| `G6` | Can its output / action boundary be specified from the audited record? |
| `G7` | Can the proposed abstraction generate independently falsifiable behavior outside the source decision in which it was observed? |
| `G8` | Can it be abstracted without adding a rule that the historical record does not contain? |

Evaluation stops at the first `NO`.

## Adversarial anti-retrofit question

For every candidate:

> **Would this abstraction still be justified if Pilot 0 were the only empirical correction case available?**

A useful name for a historical event is not sufficient. The candidate needs either recurrence in the audited process or independent structural justification that does not come from the desired future controller.

---

# Candidate set

The candidate set is induced only from the passing human-judgment audit. It intentionally separates rule-bound support operations from consequential action-selection operations.

```text
C1  prespecified inferential classification
C2  explicit authority-guardrail application
C3  structural next-object selection
C4  replication / transport reframing
C5  scope-local continue / stop control
C6  terminal STOP selection
C7  cost / resource weighting
```

This list is not claimed to be a complete ontology of correction. It is only the smallest set needed to test the strongest recurring-looking structures exposed by the audit.

---

# C1 — Prespecified inferential classification

## Observed audit components

Examples include:

```text
D1.1  classify A5 endpoint effects
D2.1  classify A6 endpoint effects
D3.1  classify A7 instability interaction
D4.1  classify replicated common encoding effect
D4.2  interpret transport diagnostic under frozen authority ceiling
```

## Gate

| Gate | Result | Basis |
| --- | --- | --- |
| G1 | YES | Multiple passing audit components explicitly contain the operation. |
| G2 | YES | The function is distinct: map prespecified estimates / intervals / tests to frozen inferential statuses. |
| G3 | YES | It recurs across multiple independent decision nodes and endpoints. |
| G4 | YES | Outputs such as `CAUSAL`, `PRACTICALLY SMALL`, `NOT DETECTED`, and `NOT ESTABLISHED` have explicit authority consequences. |
| G5 | YES | Inputs are the prespecified estimands, intervals/tests, and frozen decision rules. |
| G6 | YES | Output is a bounded inferential status, not arbitrary next-action selection. |
| G7 | YES | On held-out result vectors governed by the same prespecified rule family, the classification is mechanically testable and can be wrong relative to its contract. |
| G8 | YES | No missing historical comparative action rule is required to abstract this operation. |

## Result

```text
C1
→ SURVIVES ABSTRACTION GATE
→ CANDIDATE ABSTRACTION ONLY
```

Scope ceiling:

```text
prespecified inferential classification
≠ structural action selection
≠ controller
```

---

# C2 — Explicit authority-guardrail application

## Observed audit components

Examples include:

```text
D1.2  do not promote A5 into mechanism / global capacity
D3.2  differing point estimates ↛ heterogeneity
D4.3  unresolved T_verified interaction ↛ reopen T_instability
D4.2  common-effect compatibility ≠ transport invariance
```

## Gate

| Gate | Result | Basis |
| --- | --- | --- |
| G1 | YES | Explicit non-implications and authority ceilings recur in the trace/audit. |
| G2 | YES | The operation is distinct from estimating an effect: it constrains what may be inferred or reopened from that effect. |
| G3 | YES | It recurs across multiple nodes and different inferential objects. |
| G4 | YES | Its authority role is the object itself: prohibit an identified inference or scope expansion. |
| G5 | YES | Input boundary can be limited to an evidence/status object plus an explicitly recorded authority constraint. |
| G6 | YES | Output boundary is `claim/action licensed` versus `specified claim/action not licensed` under that guardrail. |
| G7 | YES | On new cases with explicit guardrails, behavior is falsifiable: granting the prohibited inference is a failure. |
| G8 | YES | The abstraction does not require inferring a new general causal rule; it only abstracts application of explicitly supplied authority constraints. |

## Result

```text
C2
→ SURVIVES ABSTRACTION GATE
→ CANDIDATE ABSTRACTION ONLY
```

Scope ceiling:

```text
apply explicit authority constraint
≠ discover the correct authority constraint
≠ choose the next experiment
```

---

# C3 — Structural next-object selection

## Observed audit components

Examples include:

```text
D1.3 / D1.5  A6 outer-scaffold selection
D2.5         interaction selected over finer rendering
D3.3 / D3.5  replication/transport object selected
```

## Gate

| Gate | Result | Basis |
| --- | --- | --- |
| G1 | YES | Structural next-object choices are historically observable. |
| G2 | YES | Selecting what scientific object to test next is functionally distinct from statistical classification. |
| G3 | YES | The function recurs across D1–D3. |
| G4 | YES | Each observed selection changes which object is authorized for direct testing. |
| G5 | **NO** | The audit repeatedly finds incomplete historical candidate-action sets and missing comparative selection rules. A general input state cannot be specified without adding unrecorded choice structure. |

## Result

```text
C3
→ NOT EARNED
```

Failure locus:

```text
input / comparison boundary not recoverable
```

No later gates are evaluated.

---

# C4 — Replication / transport reframing

## Observed audit component

```text
D3.3
A5 ↔ A7 discrepancy
→ replication / transport question
```

## Gate

| Gate | Result | Basis |
| --- | --- | --- |
| G1 | YES | The R1 scientific-object transition is explicitly recorded. |
| G2 | YES | Reframing a discrepancy as a replication/transport question is distinguishable from computing the discrepancy itself. |
| G3 | **NO** | The audit contains one such transition. No second independent audited instance establishes recurrence, and no independent general rule for when discrepancy warrants replication is present. |

## Result

```text
C4
→ NOT EARNED
```

Additional pressure, not needed for the rejection:

```text
D3.3 also reports:
when does a discrepancy warrant replication/transport?
→ NO FORMAL THRESHOLD RECOVERED
```

Thus `REPLICATE` is not promoted merely because R1 existed.

---

# C5 — Scope-local continue / stop control

## Observed audit components

```text
D1.6  continue with A6
D2.6  continue with A7
D3.4  A-series STOP / no A8
D3.7  A-series STOP while R1 CONTINUE
```

## Gate

| Gate | Result | Basis |
| --- | --- | --- |
| G1 | YES | Scope statuses are historically observable. |
| G2 | YES | Branch-local continuation / closure is distinguishable from endpoint inference. |
| G3 | YES | Continue/stop status recurs across multiple audited transitions. |
| G4 | YES | The status changes whether work in a named branch remains authorized. |
| G5 | **NO** | The audit explicitly reports that continuation thresholds and a branch-local stopping criterion are not recovered. The state variables sufficient to generate the status are therefore underspecified. |

## Result

```text
C5
→ NOT EARNED
```

Observed scope control remains historical evidence; it does not yet become a scope-control primitive.

---

# C6 — Terminal STOP selection

## Observed audit component

```text
D4.5
remaining uncertainty exists
+
no unresolved question supports a sufficiently discriminating next experiment
→ STOP
```

## Gate

| Gate | Result | Basis |
| --- | --- | --- |
| G1 | YES | Terminal STOP and its rationale are explicit in the frozen terminal record and passing audit. |
| G2 | YES | Terminal closure is functionally distinguishable from local inferential classification. |
| G3 | **NO** | There is only one terminal Pilot 0 STOP case in the audited source lineage. The desired future controller cannot count as independent motivation for the primitive. |

## Result

```text
C6
→ NOT EARNED
```

Even if `G3` were provisionally ignored, later gates would still face known defects:

```text
"sufficiently discriminating"
→ not operationally defined

candidate-experiment admissibility threshold
→ not recovered

next-experiment value function
→ absent
```

Therefore:

```text
STOP
→ historically justified outcome
→ not yet transferable primitive
```

---

# C7 — Cost / resource weighting

## Observed audit component

```text
D4.6
whether / how cost or operational constraints entered D1–D4
→ historically UNKNOWN
```

## Gate

| Gate | Result | Basis |
| --- | --- | --- |
| G1 | **NO** | The audit evidences the absence of recoverable cost weighting, not a cost-weighting operation that was historically used. |

## Result

```text
C7
→ NOT EARNED
```

No cost/value primitive may be inferred from operational plausibility alone.

---

# Gate summary

| Candidate | First failing gate | Result |
| --- | --- | --- |
| C1 prespecified inferential classification | — | **SURVIVES** |
| C2 explicit authority-guardrail application | — | **SURVIVES** |
| C3 structural next-object selection | G5 | **NOT EARNED** |
| C4 replication / transport reframing | G3 | **NOT EARNED** |
| C5 scope-local continue / stop control | G5 | **NOT EARNED** |
| C6 terminal STOP selection | G3 | **NOT EARNED** |
| C7 cost / resource weighting | G1 | **NOT EARNED** |

The strongest result is negative for consequential action selection:

```text
rule-bound inference / explicit guardrails
→ survive this abstraction gate

structural action selection / replication choice / stopping
→ do not survive
```

This is not evidence that the rejected abstractions are false or impossible to formalize.

It means only:

```text
Pilot 0 trace + passing audit
↛ sufficient authority to promote them now
```

---

# Anti-retrofit result

The abstraction gate rejects several concepts that are attractive in a prospective controller vocabulary:

```text
REPLICATE
STOP
scope-local control
next-object selection
cost/value ranking
```

Their attractiveness does not substitute for recurrence, input/output specification, or a recoverable generating rule.

Conversely, the two survivors are deliberately narrow:

```text
C1
apply prespecified inferential classification

C2
apply an explicit authority guardrail
```

Neither survivor can choose what experiment to run next.

This is an important ceiling:

```text
surviving abstraction
↛ action-selection controller
```

---

# Terminal authority state

```text
ABSTRACTION GATE
→ completed as a draft artifact

C1 / C2
→ candidate abstractions only

C3–C7
→ NOT EARNED

CONTROLLER PRIMITIVE PROMOTION
→ NOT PERFORMED HERE

CONTROLLER SPECIFICATION
→ NOT AUTHORIZED BY THIS ARTIFACT ALONE

PILOT 1
→ NOT AUTHORIZED

NEW EXPERIMENT
→ NOT EARNED
```

The next question, if this gate itself survives review, is narrower than controller design:

> **Do the surviving C1/C2 abstractions deserve promotion into candidate controller primitives, or are they merely reusable support operations already supplied by ordinary inferential machinery and explicit policy constraints?**

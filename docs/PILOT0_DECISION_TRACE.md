# Pilot 0 — Decision Trace Reconstruction

## Status

```text
PILOT 0
→ READ-ONLY EMPIRICAL RECORD

THIS DOCUMENT
→ HISTORICAL DECISION-TRACE RECONSTRUCTION
→ NOT A CONTROLLER SPECIFICATION
→ NOT A NEW PILOT
```

This document reconstructs consequential Pilot 0 decision transitions from provenance-bearing records.

Foundational anti-hindsight rule:

> **The controller must be reconstructible from information available at the time of each decision; later outcomes may evaluate a decision, but may not retroactively supply its rationale.**

Accordingly:

```text
later interpretation
↛ earlier decision-state reconstruction
```

If the historical record does not establish a field, this trace records:

```text
UNKNOWN
```

rather than filling the gap with a plausible retrospective explanation.

## Purpose

Pilot 0 is no longer the object to extend. It is the provenance-bearing case from which a later correction controller may be reconstructed.

The intended artifact sequence is:

```text
Pilot 0 frozen evidence
→ decision trace reconstruction        ← THIS DOCUMENT
→ human-judgment audit
→ candidate controller primitives
→ controller specification
→ independent falsification criteria
```

No Pilot 1 is authorized by this document.

## Reconstruction rules

This artifact is deliberately narrower than a controller analysis.

1. A candidate action is called **historically recoverable** only when a contemporaneous or terminal source records that action, alternative, or explicit non-authorization.
2. An analytically possible action that is not recorded as historically considered is marked `UNKNOWN`; it is not inserted into the historical candidate set.
3. A hypothesis is called **historically recoverable** only when a source records the hypothesis, fork, or scientific question. Later plausible explanations are not backfilled.
4. Historical rationale is quoted or paraphrased only from provenance-bearing sources. Later labels such as “earned complexity escalation” are not used as contemporaneous rationale.
5. Judgment-type classification is deferred to the later human-judgment audit. This trace records evidence, authority statements, actions, and recoverable rationale only.
6. Endpoint-specific claims remain endpoint-specific unless a source explicitly links them.
7. A nonzero effect and a practically meaningful effect remain separate claims when the source makes that distinction.
8. Cross-cohort or cross-experiment point-estimate differences do not establish heterogeneity when the source explicitly prohibits that inference.
9. Later outcomes appear only under **LATER OUTCOME — QUARANTINED**.
10. This trace performs no cross-node controller abstraction.

## Provenance hierarchy

For each node, reconstruction prefers:

```text
1. frozen pre-outcome contracts
2. committed result artifacts
3. contemporaneous experiment lineage recorded in the next frozen contract
4. committed terminal decision record for the terminal STOP node
5. later summary only as quarantined outcome annotation
```

Primary source artifacts used here:

| Artifact | Role in reconstruction | Content identity |
| --- | --- | --- |
| `experiments/PILOT0_A5_CONFIG.json` | pre-A5 contract and conditional next-step guardrail | blob `531a25cef00e8c34446768d80b000b89dba8dfdc` |
| `experiments/PILOT0_A6_CONFIG.json` | contemporaneous record of A5 result and A6 authorization | blob `44b911f1b56db5ee8adea89c6174b0f5e1c580b6` |
| `experiments/PILOT0_A7_CONFIG.json` | contemporaneous record of A6 result and A7 authorization | blob `3192e7e2d1d0cf26532aaa07ebacf450586564a9` |
| `experiments/PILOT0_R1_CONFIG.json` | contemporaneous record of A7 result and R1 authorization | blob `8a9ea36518e141028173a450f59d8ef61a7cd455` |
| `results/pilot0_r1_result.json` | R1 result used at terminal decision | blob `6a14f89cbd6a0976ff9241eb926d6f9f504a3c50` |
| `results/PILOT0_TERMINAL_RECORD.md` | committed terminal STOP decision and authority ledger | blob `b9aee59363daf3e4994b9c42ce800d1dbb91a334` |

The terminal record is **not** used to backfill the rationale for A5→A6, A6→A7, or A7→R1.

---

# Decision node D1 — A5 → A6

## STATE BEFORE

### Live empirical lineage available at the decision

From the frozen A6 contract:

```text
A4c
legacy-versus-canonical inline rendering
→ causal on T_change
→ causal on T_instability
→ causal on T_verified

A5
prior-state fields versus prose
→ causal on T_change
→ causal on T_verified
→ T_instability practically small at ±0.05
```

The A5 contract had isolated the prior-state body at the state-encoding boundary while holding the surrounding canonical inline scaffold fixed.

### Authorized claims

```text
prior-state encoding → T_change      CAUSAL
prior-state encoding → T_verified    CAUSAL
prior-state encoding → T_instability PRACTICALLY SMALL at ±0.05
```

Not authorized by the A5 contract:

```text
A5 explains A4c completely
A5 identifies a psychological mechanism
A5 establishes global correction capacity
```

### Unresolved uncertainty

The broad A4c `T_instability` effect remained unlocalized after the A5 encoding contrast was practically small for that endpoint.

The A5 pre-outcome contract had stated this conditional next-step guardrail:

```text
if A5 is practically small across the A4c endpoints,
next localization should target remaining outer-section framing
rather than immediately invoking interaction
```

The realized A5 result was mixed across endpoints rather than practically small across all three. The frozen A6 contract nevertheless records A6's object as the remaining outer-scaffold component after A5 isolated prior-state encoding.

### Historical action record

Historically evidenced:

```text
SELECTED:
run A6 section-scaffold localization

NAMED IN PRIOR CONDITIONAL GUARDRAIL:
remaining outer-section framing
immediate interaction as the alternative not to invoke first under that condition
```

Historical consideration of other analytically possible actions, including finer encoding decomposition or stopping the localization branch:

```text
UNKNOWN
```

## EVIDENCE AVAILABLE THEN

The A6 frozen lineage records:

```text
A5:
prior-state field-versus-prose encoding
→ causal T_change
→ causal T_verified
→ T_instability practically small at ±0.05
```

No later A6/A7/R1 evidence is admitted into this section.

## HISTORICAL HYPOTHESIS / QUESTION RECORD

The A6 contract establishes the selected scientific object:

```text
isolate explicit section-label scaffold versus unlabeled scaffold
while holding the prose state body and semantic chunks fixed
```

The A5 guardrail also names immediate interaction as a possible later escalation under its stated condition.

A complete contemporaneous competing-hypothesis set:

```text
UNKNOWN
```

## SELECTED ACTION

```text
run A6 randomized section-scaffold localization
```

A6 isolated:

```text
explicit section labels
vs
same semantic chunks without section labels
```

while holding prose state body, semantic chunk contents, order, separators, topology, signal, revision opportunity, model, generation, and scoring fixed.

## WHY THIS ACTION?

Recoverable from the frozen A6 contract:

```text
A6 localizes the remaining outer-scaffold component
of the broad A4c inline-rendering effect
after A5 isolated prior-state encoding
```

No stronger comparative rule selecting A6 over every analytically possible alternative is recovered from the historical record.

## ALTERNATIVES / REJECTION BASIS

| Alternative | Historical status | Recoverable basis |
| --- | --- | --- |
| immediate interaction escalation | named in A5 conditional guardrail; not selected for D1 | A5 guardrail says remaining outer framing should precede immediate interaction under its stated practically-small condition; exact realized comparison after the mixed A5 result is `UNKNOWN` |
| finer encoding decomposition | historical consideration `UNKNOWN` | `UNKNOWN` |
| stop / preserve unresolved | historical consideration `UNKNOWN` | `UNKNOWN` |

## AUTHORITY CHANGE

Supported by the A5 result and A6 lineage:

```text
encoding component
→ causal for T_change and T_verified
→ practically small for T_instability

A6 outer-scaffold object
→ authorized for direct testing
```

A formal rule mapping this state to A6:

```text
NOT RECOVERED
```

## JUDGMENT CLASSIFICATION

```text
DEFERRED TO HUMAN-JUDGMENT AUDIT
```

This trace does not classify the decision as formal, statistical, structural, or value/cost based.

## STOP / CONTINUE STATUS

Observed historical action:

```text
CONTINUE WITH A6
```

Whether A6 had demonstrably superior value to every other possible action:

```text
UNKNOWN
```

## LATER OUTCOME — QUARANTINED

Not available to D1 at action selection.

Later A6 outcome:

```text
section scaffold → T_change causal
section scaffold → T_instability practically small
section scaffold → T_verified practically small
```

This later outcome may evaluate D1; it may not supply D1's original rationale.

---

# Decision node D2 — A6 → A7

## STATE BEFORE

### Evidence available

The frozen A7 contract records the A6 outcome:

```text
A5
encoding
→ T_change causal
→ T_verified causal
→ T_instability practically small

A6
section scaffold
→ T_change causal
→ T_instability practically small
→ T_verified practically small
```

The A6 pre-outcome guardrail had stated:

```text
if A6 is practically small for T_instability,
the next step should discriminate remaining finer rendering differences
versus interaction;
neither is automatically established
```

### Authorized claims

```text
encoding → T_change      CAUSAL
encoding → T_verified    CAUSAL
encoding → T_instability PRACTICALLY SMALL

scaffold → T_change      CAUSAL
scaffold → T_instability PRACTICALLY SMALL
scaffold → T_verified    PRACTICALLY SMALL
```

### Unresolved uncertainty

For the A4c-motivated instability branch:

```text
A4c broad effect remains
but neither tested A5 nor A6 main-effect component
established a practically meaningful T_instability main effect
```

The A6 historical guardrail explicitly leaves two classes for the next discrimination:

```text
remaining finer rendering differences
versus
interaction
```

### Historical action record

Historically recoverable:

```text
NAMED FOR NEXT DISCRIMINATION BY A6:
1. remaining finer rendering differences
2. interaction

SELECTED IN A7:
encoding × scaffold interaction factorial
```

Historical consideration of stopping or other actions:

```text
UNKNOWN
```

## HISTORICAL HYPOTHESIS / QUESTION RECORD

The A6 guardrail records the two-way discrimination:

```text
remaining finer rendering differences
versus
interaction
```

The A7 contract then defines the interaction object as:

```text
whether the effect of prose versus fields
differs between unlabeled and labeled scaffolds
```

The frozen record does not establish a complete mutually exclusive hypothesis set beyond that documented fork.

## SELECTED ACTION

```text
run A7 encoding × scaffold factorial
```

A7 prospectively closed the missing `UF` cell and tested:

```text
Gamma_FS = (UP - UF) - (LP - LF)
```

in one fresh randomized cohort.

## WHY THIS ACTION?

Recoverable from the A7 frozen contract:

```text
A7 estimates whether the joint representation configuration
produces transition effects beyond the two component main-effect edges
localized by A5 and A6
```

For `T_instability`, the contract explicitly names `Gamma_FS_instability` as the highest-information residual target motivating A7.

The historical record does **not** additionally state a general rule of “earned complexity escalation.” That label is not used as D2's contemporaneous rationale.

## ALTERNATIVES / REJECTION BASIS

| Alternative | Historical status | Recoverable basis |
| --- | --- | --- |
| finer rendering localization | explicitly named by A6 as the other side of the next discrimination; not selected | why interaction was preferred over a specific finer-rendering candidate is `UNKNOWN` |
| stop / preserve unresolved | historical consideration `UNKNOWN` | `UNKNOWN` |

## AUTHORITY CHANGE

At selection time, the A7 contract establishes:

```text
encoding × scaffold interaction
→ defined as the next causal object to test

interaction
↛ established explanation before A7 outcome
```

## JUDGMENT CLASSIFICATION

```text
DEFERRED TO HUMAN-JUDGMENT AUDIT
```

A formal selection rule choosing interaction over a particular finer-rendering experiment:

```text
NOT RECOVERED
```

## STOP / CONTINUE STATUS

Observed historical action:

```text
CONTINUE WITH A7
```

Recoverable reason:

```text
A7 contract identifies the missing factorial cell
and defines a direct encoding × scaffold interaction test
```

Comparative rule showing that this action was superior to every alternative:

```text
UNKNOWN
```

## LATER OUTCOME — QUARANTINED

Not available to D2 at action selection.

Later A7 outcome:

```text
Gamma_FS_change       causal +0.06349
Gamma_FS_instability  practically small at ±0.05
Gamma_FS_verified     unresolved
```

The later classification of what this implies for subsequent decisions belongs to D3, where A7 results were historically available.

---

# Decision node D3 — A7 → R1

## STATE BEFORE

### Evidence available

The frozen R1 contract records:

```text
A5 labeled encoding → T_instability
Delta ≈ +0.0207
95% interval inside ±0.05

A6 scaffold → T_instability
practically small

A7 encoding × scaffold → T_instability
practically small

A7 within-study encoding contrasts:
labeled   ≈ +0.0556
unlabeled ≈ +0.0476
```

The same A7 cohort therefore showed similar prose-minus-fields instability contrasts under both scaffolds while the interaction contrast itself was practically small.

### Authorized claims

```text
encoding × scaffold interaction
→ practically small for T_instability

section scaffold
→ practically small for T_instability
```

The frozen R1 contract explicitly prohibits this inference:

```text
different cohort point estimates
→ heterogeneity
```

### Unresolved uncertainty

The R1 contract defines the new scientific object as:

```text
replicate/transport the labeled-scaffold E0-only
encoding-to-instability contrast
across independently sampled prestates
```

The historical discrepancy recorded in the R1 lineage was:

```text
A5       ≈ +0.0207
A7-L     ≈ +0.0556
A7-U     ≈ +0.0476
```

### Historical action record

Historically evidenced:

```text
SELECTED:
R1 replication/transport test

EXPLICITLY NOT AUTHORIZED:
A8 finer-formatting ablation
heterogeneity merely from differing cohort point estimates
```

Historical consideration of continuing interaction decomposition, stopping before R1, or other actions:

```text
UNKNOWN
```

## HISTORICAL HYPOTHESIS / QUESTION RECORD

The contemporaneous R1 record establishes:

```text
QUESTION:
does the inherited encoding → T_instability contrast
replicate / transport across fresh independently sampled prestates?

GUARDRAIL:
differing cohort point estimates do not by themselves establish heterogeneity
```

A contemporaneous four-item competing explanation set such as sampling variation, prestate composition, context dependence, or transport-limited effect is **not recorded** in the frozen R1 contract.

Historical competing-hypothesis set beyond the recorded replication/transport question and heterogeneity guardrail:

```text
UNKNOWN
```

## SELECTED ACTION

```text
R1 replication / transport branch
```

R1 narrowed the design to:

```text
fixed labeled scaffold
E0 only
fields vs prose
T_instability only
four fresh disjoint prestate cohorts
```

The R1 lineage explicitly states:

```text
A-series
→ localization branch stopped
→ no A8 finer-formatting ablation
```

## WHY THIS ACTION?

Recoverable from the R1 frozen contract:

```text
replicate/transport the labeled-scaffold E0-only
encoding-to-instability contrast
across independently sampled prestates
```

The contract explicitly reframes R1 as a replication/transport branch rather than continuation of the A-series localization ladder.

A formal comparative rule selecting R1 over every other possible action:

```text
NOT RECOVERED
```

## ALTERNATIVES / REJECTION BASIS

| Alternative | Historical status | Recoverable basis |
| --- | --- | --- |
| A8 finer-formatting ablation | explicitly not authorized | R1 lineage states the A-series localization branch stopped and no A8 finer-formatting ablation was authorized |
| infer heterogeneity directly | explicitly prohibited as an inference | R1 guardrail: different cohort point estimates do not by themselves establish heterogeneity |
| continue interaction decomposition | historical consideration `UNKNOWN` | `UNKNOWN` |
| stop before replication | historical consideration `UNKNOWN` | `UNKNOWN` |

## AUTHORITY CHANGE

Supported by the R1 lineage:

```text
A7 encoding × scaffold interaction for T_instability
→ practically small

A5 ↔ A7 encoding contrast discrepancy
→ becomes the object of a replication/transport test
↛ becomes a heterogeneity claim

A-series localization
→ stopped
```

## JUDGMENT CLASSIFICATION

```text
DEFERRED TO HUMAN-JUDGMENT AUDIT
```

No formal threshold for when a replication discrepancy warrants R1 is recovered from the frozen contract.

## STOP / CONTINUE STATUS

Historically recorded scope transition:

```text
A-SERIES: STOP
R1 REPLICATION/TRANSPORT BRANCH: CONTINUE
```

No broader controller interpretation is assigned here.

## LATER OUTCOME — QUARANTINED

Not available to D3 at action selection.

R1 later produced four positive cohort estimates and an equal-cohort common effect:

```text
Delta_common = +0.033975
95% CI       = [+0.021316,+0.047791]
blocked-randomization p = 0.00019996
```

The whole common-effect interval lay inside `[-0.05,+0.05]`.

Transport diagnostic:

```text
Q = 1.120334
df = 3
p = 0.772168
I² = 0
tau²_DL = 0
```

---

# Decision node D4 — R1 → STOP

## STATE BEFORE

### Evidence available

R1 result:

```text
C1  +0.030043
C2  +0.045267
C3  +0.025974
C4  +0.034615

Delta_common = +0.033975
95% CI       = [+0.021316,+0.047791]
p            = 0.00019996
```

Thus, as recorded in the terminal artifact:

```text
encoding → T_instability
→ nonzero / replicated

encoding → T_instability
→ practically small at the inherited ±0.05 scale
```

Transport diagnostic:

```text
Q = 1.120334
p = 0.772168
I² = 0
tau²_DL = 0
```

Authorized transport interpretation:

```text
observed cohort effects
→ compatible with a common-effect model

↛ proven transport invariance
```

### Authorized claims

```text
prior-state encoding → T_instability
CAUSAL / REPLICATED / PRACTICALLY SMALL

excess cohort variation
NOT DETECTED

transport invariance
NOT ESTABLISHED
```

### Remaining unresolved uncertainty

The terminal record retains at least one endpoint-local unresolved question:

```text
T_verified encoding × scaffold interaction
→ UNRESOLVED
```

and explicitly states:

```text
unresolved T_verified interaction
↛ reopen T_instability
```

## Historical action / alternative record

Historically evidenced by the terminal record:

```text
SELECTED:
STOP Pilot 0

EXPLICITLY NOT EARNED:
R2
A8
additional T_instability decomposition

EXPLICIT AUTHORITY BOUNDARY:
unresolved T_verified interaction
↛ reopen T_instability

EXPLICIT NON-CLAIM:
transport invariance not established
```

Whether additional candidate actions were considered but not recorded:

```text
UNKNOWN
```

## SELECTED ACTION

```text
STOP
```

Terminal scope:

```text
PILOT 0
STATUS: CLOSED

A-series
→ sufficiently resolved

R1
→ replication/transport question closed

A8
→ NOT EARNED

R2
→ NOT EARNED

additional T_instability decomposition
→ NOT EARNED
```

## WHY THIS ACTION?

The committed terminal record states:

> Pilot 0 is closed because the evidence has reduced the live explanatory space to a point where no further experiment is presently justified by a sufficiently discriminating unresolved question.

The stopping rule is explicitly epistemic rather than logistical:

```text
STOP
≠ truth
≠ completeness
≠ certainty

STOP
= no presently justified escalation
```

The terminal correction cycle records:

```text
failure detected
→ hypothesis localized
→ alternatives discriminated
→ surviving effects replicated
→ effect sizes bounded
→ endpoint-specific uncertainty preserved
→ further complexity fails to earn authorization
→ STOP
```

## ALTERNATIVES / REJECTION BASIS

| Alternative / claim | Historical status | Recoverable basis from terminal record |
| --- | --- | --- |
| R2 | explicitly not earned | R1 replication/transport question was closed; no sufficiently discriminating unresolved question authorized R2 |
| A8 | explicitly not earned | representation localization was sufficiently resolved; further complexity lacked authorization |
| additional T_instability decomposition | explicitly not earned | terminal record closes the T_instability localization branch after replication/bounding and prior component tests |
| reopen T_instability because `T_verified` interaction is unresolved | explicitly disallowed by authority boundary | endpoint-local uncertainty does not authorize reopening T_instability |
| claim transport invariance | explicitly not established | compatibility with a common-effect model does not establish invariance |

## AUTHORITY CHANGE

Terminal record:

```text
A5 ↔ A7 replication discrepancy
→ addressed by R1 replication/transport branch

encoding → T_instability
→ CAUSAL / REPLICATED / PRACTICALLY SMALL

excess cohort variation
→ NOT DETECTED

transport invariance
→ NOT ESTABLISHED

T_instability localization branch
→ CLOSED

Pilot 0
→ CLOSED
```

## JUDGMENT CLASSIFICATION

```text
DEFERRED TO HUMAN-JUDGMENT AUDIT
```

The historical record does contain the statistical results, endpoint-local authority boundary, and explicit stopping rationale. It does **not** contain a formal next-experiment value function or admissibility threshold.

## STOP / CONTINUE STATUS

```text
STOP
```

Historically recoverable stopping condition:

```text
remaining uncertainty exists
+
no unresolved question supports a sufficiently discriminating next experiment
→ STOP
```

This is recorded here as historical stopping rationale, not as a universal controller primitive.

## LATER OUTCOME — QUARANTINED

There is no later Pilot 0 experimental outcome. Pilot 0 was frozen as read-only after this decision.

Future research may evaluate whether this STOP decision was well calibrated, but such evaluation cannot retroactively alter the rationale recorded here.

---

# No cross-node abstraction in this artifact

The previous draft included cross-node conceptual compression about belief, authority, control, controller failure classes, nested stopping, and candidate controller invariants. Those observations are not part of the historical decision reconstruction and are intentionally removed from the trace surface.

This document records chronology, contemporaneous evidence, historically recoverable action/question structure, authority statements, and quarantined later outcomes only.

Any cross-node decomposition belongs, if authorized after provenance review, in a separate human-judgment audit.

---

# Open reconstruction gaps

The following historical gaps remain intentionally unresolved:

1. **A5→A6:** the record establishes A6's selected outer-scaffold object and a prior conditional outer-framing-versus-immediate-interaction guardrail, but it does not recover a complete realized candidate-action set or a rule showing A6 was preferable to every alternative.
2. **A6→A7:** the record establishes the finer-rendering-versus-interaction fork and A7's selected interaction test, but the comparative rule selecting interaction is not recovered.
3. **A7→R1:** the record establishes the replication/transport question, the no-A8 lineage decision, and the prohibition on inferring heterogeneity from point estimates; it does not recover a broader competing-explanation set or a formal threshold for selecting replication.
4. **R1→STOP:** the stopping rationale and explicitly unearned branches are recorded, but no formal next-experiment value function or admissibility threshold is present.
5. **Candidate-action completeness:** for D1–D4, unrecorded analytically possible actions cannot be treated as historically considered.
6. **Cost/constraint weighting:** whether and how cost or operational constraints entered these four historical choices is not established by this trace and remains `UNKNOWN` unless separate contemporaneous evidence is found.

These gaps are not repaired by inference.

---

# Terminal boundary of this artifact

This trace authorizes no new experiment and no controller abstraction.

```text
Decision Trace
= historical reconstruction only

Human-Judgment Audit
= downstream only after provenance PASS

Controller Primitives
= not authorized by this artifact

Controller Specification
= not authorized by this artifact

Independent Falsification
= not authorized by this artifact
```

No controller equation, scalar value-of-information function, Pilot 1, or autonomous-scientist claim is frozen here.

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

## Controller-relevant distinctions observed in the trace

The trace preserves three distinct layers without yet formalizing them into a controller:

```text
BELIEF
What does the evidence support as potentially true?

AUTHORITY
What claims, scopes, and actions does the evidence license?

CONTROL
Given that authority state, what should happen next?
```

Candidate transition structure:

```text
evidence
→ belief update
→ authority update
→ admissible-action update
→ action selection
```

This reconstruction does **not** assume that the eventual controller must use exactly this representation.

## Trace invariants

The following constraints are preserved because they were repeatedly operative in Pilot 0 and are directly relevant to later controller extraction:

```text
UNRESOLVED
↛ ACTION REQUIRED

ACTIONABLE
↛ EXPERIMENT REQUIRED

EXPERIMENT POSSIBLE
↛ EXPERIMENT AUTHORIZED
```

Additional reconstruction rules:

1. Endpoint-specific uncertainty remains endpoint-local unless the historical record explicitly links it elsewhere.
2. A nonzero effect and a practically meaningful effect are separate authority claims.
3. Cross-cohort or cross-experiment point-estimate differences do not by themselves establish heterogeneity.
4. `PRESERVE_UNRESOLVED` and `STOP` are not treated as equivalent operations.
5. The trace records **why the selected action was supported** separately from **why alternatives were rejected**.
6. Rejected-action rationales are `UNKNOWN` unless the historical record actually contains them.
7. Later outcomes appear only under **LATER OUTCOME — QUARANTINED**.

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

The A5 contract had isolated the prior-state body at the shallowest state-encoding boundary while holding the surrounding canonical inline scaffold fixed.

### Authorized claims

```text
prior-state encoding → T_change      CAUSAL
prior-state encoding → T_verified    CAUSAL
prior-state encoding → T_instability PRACTICALLY SMALL at ±0.05
```

Not authorized:

```text
A5 explains A4c completely
A5 identifies a psychological mechanism
A5 establishes global correction capacity
```

### Unresolved uncertainty

The broad A4c `T_instability` effect remained unlocalized after the A5 encoding contrast was practically small for that endpoint.

The A5 pre-outcome contract had already stated a conditional escalation rule:

```text
if A5 is practically small across the A4c endpoints,
next localization should target remaining outer-section framing
rather than immediately invoking interaction
```

The realized A5 result was mixed across endpoints rather than practically small across all three; the frozen A6 contract nevertheless records the next object as the remaining outer-scaffold component specifically after A5 isolated prior-state encoding.

### Candidate actions recoverable from record

```text
1. test remaining outer section/scaffold framing
2. invoke an interaction model immediately
3. refine the prior-state encoding contrast further
4. preserve unresolved / stop this localization branch
```

Whether this list was exhaustive at the time:

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

## LIVE HYPOTHESES

Recoverable hypotheses:

```text
H_outer:
remaining outer section/scaffold framing contributes to the residual A4c transition effects

H_interaction:
encoding may matter differently under another scaffold configuration
```

Additional hypotheses considered contemporaneously:

```text
UNKNOWN
```

## SELECTED ACTION

```text
DISCRIMINATE
→ run A6 randomized section-scaffold localization
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

This is a structural localization rationale: move to the next experimentally isolatable representation boundary rather than changing mechanism level.

## REJECTED ACTIONS / REJECTION BASIS

| Alternative | Status | Rejection basis recoverable from historical record |
| --- | --- | --- |
| immediate interaction escalation | not selected | A5 contract explicitly preferred remaining outer framing before immediate interaction under its practically-small condition; exact realized-decision comparison is otherwise `UNKNOWN` |
| finer encoding decomposition | not selected | `UNKNOWN` |
| stop / preserve unresolved | not selected | `UNKNOWN` |

## AUTHORITY CHANGE

```text
encoding component
→ localized for T_change and T_verified
→ bounded as practically small for T_instability

residual A4c T_instability uncertainty
→ remains live
→ does not yet authorize interaction as established
```

## JUDGMENT TYPE

```text
STRUCTURAL
+
STATISTICAL input from A5 practical-equivalence result
```

Formal rule sufficient to reproduce the action:

```text
NOT ESTABLISHED
```

## STOP / CONTINUE STATUS

```text
CONTINUE LOCALIZATION
```

Reason recoverable from record:

```text
an experimentally isolatable outer-scaffold boundary remained live
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

The historical record explicitly leaves two broad classes live:

```text
finer rendering difference
OR
encoding × scaffold interaction
```

### Candidate actions recoverable from record

```text
1. test encoding × scaffold interaction
2. test a finer rendering difference
3. preserve unresolved / stop
```

Other contemporaneous alternatives:

```text
UNKNOWN
```

## LIVE HYPOTHESES

```text
H_interaction:
the effect of prose versus fields differs by labeled versus unlabeled scaffold

H_finer:
another operational rendering difference contributes to the A4c instability contrast
```

The frozen record does not establish a complete mutually exclusive hypothesis set.

## SELECTED ACTION

```text
DISCRIMINATE / ESCALATE REPRESENTATION COMPLEXITY
→ run A7 encoding × scaffold factorial
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

This is the clearest historical example in the trace of **earned complexity escalation**: the interaction was not introduced before the two component main-effect boundaries had been directly tested.

## REJECTED ACTIONS / REJECTION BASIS

| Alternative | Status | Rejection basis recoverable from historical record |
| --- | --- | --- |
| finer rendering localization | not selected | A6 record kept it live; why interaction was preferred over a specific finer rendering candidate is `UNKNOWN` |
| stop / preserve unresolved | not selected | A7 contract treats the missing factorial cell as an available discriminating test; comparative stopping rationale otherwise `UNKNOWN` |

## AUTHORITY CHANGE

At selection time:

```text
interaction
→ promoted from live hypothesis to testable causal object

interaction
↛ established explanation
```

No A7 result is admitted before execution.

## JUDGMENT TYPE

```text
STRUCTURAL
+
STATISTICAL input from A5/A6 practical-equivalence decisions
```

The choice between interaction and a particular finer-rendering experiment remained partly human-judged:

```text
FORMAL SELECTION RULE
→ NOT RECOVERED
```

## STOP / CONTINUE STATUS

```text
CONTINUE
```

Reason recoverable from record:

```text
a previously missing factorial cell enabled a direct test
of the live interaction explanation
```

## LATER OUTCOME — QUARANTINED

Not available to D2 at action selection.

Later A7 outcome:

```text
Gamma_FS_change       causal +0.06349
Gamma_FS_instability  practically small at ±0.05
Gamma_FS_verified     unresolved
```

For the motivating instability endpoint, the interaction explanation was weakened at the inherited practical scale.

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

Not authorized:

```text
A5/A7 point-estimate discrepancy
→ cohort heterogeneity

A7 interaction result
→ no encoding effect
```

### Unresolved uncertainty

The live question shifted from:

```text
Does scaffold moderate encoding for T_instability?
```

to:

```text
Does the encoding → T_instability contrast itself
reproduce / transport across independently sampled prestates?
```

The discrepancy was historical:

```text
A5       ≈ +0.0207
A7-L     ≈ +0.0556
A7-U     ≈ +0.0476
```

but the frozen R1 contract explicitly prohibited calling this heterogeneity merely from differing point estimates.

### Candidate actions recoverable from record

```text
1. replicate / test transport of encoding → T_instability
2. run A8 finer-formatting localization
3. infer cohort heterogeneity from A5/A7 differences
4. continue interaction decomposition
5. preserve unresolved / stop
```

Whether other actions were considered:

```text
UNKNOWN
```

## LIVE HYPOTHESES

Recoverable competing explanations for the discrepancy:

```text
sampling variation
population / prestate composition difference
context dependence
transport-limited encoding effect
```

The frozen R1 contract does not treat any one of these as established before R1.

## SELECTED ACTION

```text
REPLICATE / TEST_TRANSPORT
→ R1
```

R1 narrowed the design to:

```text
fixed labeled scaffold
E0 only
fields vs prose
T_instability only
four fresh disjoint prestate cohorts
```

The A-series was explicitly stopped:

```text
no A8 finer-formatting ablation
```

## WHY THIS ACTION?

Recoverable from the R1 frozen contract:

```text
replicate/transport the labeled-scaffold E0-only
encoding-to-instability contrast
across independently sampled prestates
```

The contract explicitly reframed R1 as a different scientific purpose from A-series localization.

The discriminating target was no longer a representation component. It was whether the suspected encoding contrast was stable enough to transport across fresh samples from the same prestate-sampling distribution.

## REJECTED ACTIONS / REJECTION BASIS

| Alternative | Status | Rejection basis recoverable from historical record |
| --- | --- | --- |
| A8 finer-formatting ablation | explicitly rejected | R1 lineage states the A-series localization branch stopped and no A8 finer-formatting ablation was authorized |
| infer heterogeneity directly | explicitly rejected | R1 guardrail: different cohort point estimates do not by themselves establish heterogeneity |
| preserve interaction explanation | rejected for T_instability | A7 interaction was practically small for the motivating endpoint |
| stop before replication | not selected | exact comparative rationale is `UNKNOWN`; R1 contract treats the replication discrepancy as a live directly testable uncertainty |

## AUTHORITY CHANGE

```text
encoding × scaffold explanation for T_instability
→ weakened at ±0.05

A5 ↔ A7 difference
→ promoted to replication/transport question
↛ promoted to heterogeneity claim

A-series localization
→ stopped
```

## JUDGMENT TYPE

```text
STATISTICAL
+
STRUCTURAL
```

Statistical component:

```text
interaction practical-equivalence result
+
discrepant encoding point estimates
```

Structural component:

```text
change scientific object from localization
to replication/transport
```

Formal rule sufficient to choose R1 over STOP:

```text
NOT RECOVERED
```

## STOP / CONTINUE STATUS

```text
A-SERIES: STOP
R1 REPLICATION/TRANSPORT BRANCH: CONTINUE
```

This is an important scoped-control distinction. Stopping one branch did not imply stopping the entire empirical program.

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

Thus:

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

At least one unrelated endpoint-local question remained:

```text
T_verified encoding × scaffold interaction
→ UNRESOLVED
```

But the committed terminal record explicitly preserves:

```text
unresolved T_verified interaction
↛ reopen T_instability
```

Residual uncertainty therefore existed without automatically becoming action-forcing.

### Candidate actions recoverable from record

```text
1. STOP Pilot 0
2. R2 replication / transport escalation
3. reopen T_instability localization
4. A8 finer-formatting localization
5. use unresolved T_verified interaction to continue the representation branch
6. preserve endpoint-local unresolved questions without further experiment
```

Whether this list was exhaustive:

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
→ replication/transport question resolved enough to close

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

## REJECTED ACTIONS / REJECTION BASIS

| Alternative | Status | Rejection basis recoverable from terminal record |
| --- | --- | --- |
| R2 | explicitly not earned | R1 resolved the replication/transport question enough to close; no new sufficiently discriminating unresolved question recorded |
| A8 | explicitly not earned | representation localization already sufficiently resolved; further complexity lacked authorization |
| further T_instability decomposition | explicitly not earned | encoding effect replicated and bounded; scaffold and interaction already practically small; no new discriminating target recorded |
| reopen T_instability because `T_verified` interaction is unresolved | explicitly rejected | endpoint-local uncertainty does not authorize reopening a resolved branch |
| claim transport invariance | explicitly rejected as authority claim | compatibility with common effect does not establish invariance |

## AUTHORITY CHANGE

```text
A5 ↔ A7 replication discrepancy
→ resolved as a fresh replication/transport question

encoding → T_instability
→ CAUSAL / REPLICATED / PRACTICALLY SMALL

heterogeneity branch
→ NOT EARNED

T_instability localization branch
→ CLOSED

Pilot 0
→ CLOSED
```

## JUDGMENT TYPE

Recoverable components:

```text
STATISTICAL
→ replicated nonzero effect
→ practical-equivalence decision
→ transport diagnostic

STRUCTURAL
→ endpoint-local authority preservation
→ no branch leakage
→ no new discriminating target identified
```

Value/cost rule used to compare possible future experiments:

```text
NOT FORMALIZED IN HISTORICAL RECORD
```

This is a major target for the later human-judgment audit.

## STOP / CONTINUE STATUS

```text
STOP
```

This node demonstrates the distinction:

```text
there is still uncertainty
+
another experiment is possible
+
no next experiment is sufficiently justified
=
STOP
```

The trace does **not** treat STOP as evidence that the theory is true, complete, or certain.

## LATER OUTCOME — QUARANTINED

There is no later Pilot 0 experimental outcome. Pilot 0 was frozen as read-only after this decision.

Future research may evaluate whether this STOP decision was well calibrated, but such evaluation cannot retroactively alter the rationale recorded here.

---

# Cross-node observations — descriptive only

These are observations about the reconstructed trace, not yet controller primitives.

## 1. Belief, authority, and control can fail separately

The trace motivates distinguishing:

```text
BELIEF ERROR
wrong substantive interpretation

AUTHORITY ERROR
claim scope or strength exceeds what evidence licenses

CONTROL ERROR
evidence and authority may be interpreted acceptably,
but the next action is poorly selected
```

This document does not yet define formal tests for these failure classes.

## 2. Complexity escalation was not monotonic

Observed sequence:

```text
A5 component
→ A6 component
→ A7 interaction
→ R1 replication/transport
→ STOP
```

The sequence did not continue to finer representation components after the interaction target weakened.

## 3. Scope-local stopping occurred before global stopping

At D3:

```text
A-series → STOP
R1       → CONTINUE
```

At D4:

```text
R1       → STOP
Pilot 0  → STOP
```

This suggests that a future controller may need nested action scopes rather than a single global continue/stop bit.

## 4. `PRESERVE_UNRESOLVED` and `STOP` are observably distinct

At terminal state:

```text
T_verified interaction
→ remains UNRESOLVED
→ preserved locally

T_instability branch
→ STOP

Pilot 0
→ STOP
```

Thus:

```text
UNRESOLVED ≠ ACTION REQUIRED
```

and:

```text
PRESERVE_UNRESOLVED ≠ STOP
```

## 5. A future controller cannot be validated by reproducing this trace alone

```text
reproduce Pilot 0 decisions
≠ general correction controller
```

Pilot 0 is a development / reconstruction case. Any later controller claim requires independent falsification on problems not used to induce its primitives or rules.

---

# Open reconstruction gaps

The following gaps are intentionally left unresolved for the next human-judgment audit:

1. **A5→A6:** why A6 was preferable to every concrete alternative is not fully recoverable from the frozen record.
2. **A6→A7:** the record establishes that finer rendering and interaction were both live; the comparative rule selecting interaction is not formalized.
3. **A7→R1:** the record establishes why heterogeneity could not yet be claimed and why R1 was a direct test, but no formal threshold for “replication discrepancy worth testing” is recorded.
4. **R1→STOP:** the epistemic stopping rationale is explicit, but no formal next-experiment value function or admissibility threshold existed.
5. **Candidate-action completeness:** historical candidate-action sets cannot be proven exhaustive from the committed records.
6. **Cost/constraint weighting:** computational cost influenced the broader program operationally, but the decision trace does not establish a formal cost-weighting rule for these four transitions.

These gaps are not defects to repair retrospectively. They are empirical targets for:

```text
docs/PILOT0_HUMAN_JUDGMENT_AUDIT.md
```

---

# Terminal boundary of this artifact

This trace authorizes no new experiment.

```text
Decision Trace
= historical observation

Human-Judgment Audit
= next decomposition

Controller Primitives
= later abstraction

Controller Specification
= later formalization

Independent Falsification
= later test design
```

No controller equation, scalar value-of-information function, Pilot 1, or autonomous-scientist claim is frozen here.

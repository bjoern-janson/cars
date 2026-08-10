# Pilot 0 — Human-Judgment Audit

## Status

```text
PILOT 0
→ READ-ONLY EMPIRICAL RECORD

PILOT0_DECISION_TRACE.md
→ PROVENANCE PASS

THIS DOCUMENT
→ COMPONENT-LEVEL HUMAN-JUDGMENT AUDIT
→ NOT PRIMITIVE EXTRACTION
→ NOT A CONTROLLER SPECIFICATION
→ NOT A NEW PILOT
```

This audit takes the repaired, provenance-valid `docs/PILOT0_DECISION_TRACE.md` as evidence and decomposes its consequential decisions into the smallest identifiable decision components supported by that trace.

It does **not** improve the historical decisions, infer missing rationales, manufacture comparative rules, or promote recurring-looking components into controller primitives.

Foundational boundary:

```text
we can describe what happened
≠
we know the rule that generated it
```

Where the trace does not establish a rationale, rule, or historical alternative set, this audit preserves that absence.

## Audit ontology

Each decision component is classified independently on multiple axes.

### FUNCTION

```text
FORMAL
STATISTICAL
STRUCTURAL
VALUE/COST
OTHER
UNKNOWN
```

`OTHER` is used only when the component's function is identifiable but does not fit the other classes. A subtype is stated explicitly, for example `OTHER — authority-boundary application`.

### SPECIFICATION

```text
EXPLICIT
IMPLICIT-RECOVERABLE
NOT-RECOVERABLE
```

This asks how explicitly the historical process governed the component, not whether the component was sensible.

### MECHANICAL REPRODUCIBILITY

```text
YES
PARTIAL
NO
UNKNOWN
```

This asks whether the available historical rule and inputs are sufficient to reproduce the component mechanically.

### RATIONALE STATUS

```text
RECOVERABLE
UNKNOWN-RATIONALE
```

### RULE STATUS

```text
RECOVERABLE
UNKNOWN-RULE
```

A known rationale with no recoverable generating rule is recorded as:

```text
RATIONALE: RECOVERABLE
RULE: UNKNOWN-RULE
```

That distinction is central to the audit.

## Source boundary

Primary audit evidence:

- `docs/PILOT0_DECISION_TRACE.md` at the provenance-passing repair commit `1c8ad566aad9a65031128e91fb4a0298def84cd4`.

The trace itself derives from the frozen A5/A6/A7/R1 contracts, R1 result artifact, and terminal Pilot 0 record. This audit does not reopen those sources to expand the historical candidate sets beyond what the trace already admitted.

Later controller concepts are not used as classification evidence.

---

# D1 audit — A5 → A6

## D1.1 — Characterize the A5 endpoint results

**Observed component**

```text
A5 prior-state encoding
→ T_change causal
→ T_verified causal
→ T_instability practically small at ±0.05
```

**Inputs used**

A5 result as recorded in the frozen A6 lineage and inherited practical-equivalence rule.

**Classification**

```text
FUNCTION: STATISTICAL
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES
RATIONALE: RECOVERABLE
RULE: RECOVERABLE
```

**Why**

The causal and practical-scale classifications were governed by frozen inferential rules. The trace does not require discretionary reconstruction to recover these endpoint statuses.

**Authority consequence**

```text
encoding → T_change      CAUSAL
encoding → T_verified    CAUSAL
encoding → T_instability PRACTICALLY SMALL
```

**Automation gap exposed**

```text
NONE IDENTIFIED AT THIS COMPONENT
```

This does not imply that later action selection is mechanical.

---

## D1.2 — Preserve A5 authority ceilings

**Observed component**

Do not promote the A5 result into complete explanation, psychological mechanism, or global correction capacity.

**Classification**

```text
FUNCTION: OTHER — authority-boundary application
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES
RATIONALE: RECOVERABLE
RULE: RECOVERABLE
```

**Why**

The A5 contract explicitly names these non-authorized interpretations.

**Authority consequence**

The causal endpoint effects remain local to the tested encoding contrast.

**Automation gap exposed**

No historical gap is required to apply these named prohibitions. Whether a general authority-boundary system can reproduce analogous limits elsewhere is outside this audit.

---

## D1.3 — Identify outer scaffold as the selected next scientific object

**Observed component**

```text
A6
→ explicit section labels vs unlabeled scaffold
```

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: PARTIAL
RATIONALE: RECOVERABLE
RULE: UNKNOWN-RULE
```

**Why**

The A6 contract explicitly states that it localizes the remaining outer-scaffold component after A5 isolated prior-state encoding. That explains what A6 was intended to do.

However, the record does not contain a complete rule mapping the realized mixed A5 endpoint state to A6 rather than every other possible action.

**Authority consequence**

```text
A6 outer-scaffold contrast
→ authorized for direct testing
```

**Automation gap exposed**

```text
state → next structural boundary selection rule
NOT RECOVERED
```

---

## D1.4 — Defer immediate interaction under the A5 conditional guardrail

**Observed component**

The A5 contract names remaining outer framing before immediate interaction under its stated practically-small condition.

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: EXPLICIT AS A CONDITIONAL GUARDRAIL
MECHANICAL REPRODUCIBILITY: PARTIAL
RATIONALE: RECOVERABLE
RULE: RECOVERABLE FOR THE STATED CONDITION,
      NOT SUFFICIENT FOR THE REALIZED MIXED ENDPOINT STATE
```

**Why**

The historical guardrail exists, but its antecedent was phrased as A5 being practically small across the A4c endpoints. The realized A5 result was mixed. The exact realized-decision comparison is therefore not mechanically supplied by that guardrail alone.

**Automation gap exposed**

```text
how conditional guardrails compose
when realized evidence only partially matches the antecedent
→ NOT SPECIFIED
```

---

## D1.5 — Choose A6 over unrecorded alternatives

**Observed component**

A6 was selected. The trace does not establish historical consideration of finer encoding decomposition or stopping.

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: NOT-RECOVERABLE
MECHANICAL REPRODUCIBILITY: NO
RATIONALE: RECOVERABLE FOR A6'S PURPOSE
RULE: UNKNOWN-RULE FOR COMPARATIVE SELECTION
```

**Why**

The purpose of A6 is documented. A rule establishing that A6 was preferable to all available alternatives is not.

**Authority consequence**

Only the selected A6 object becomes historically evidenced as the next test. Unrecorded alternatives do not acquire historical status through this audit.

**Automation gap exposed**

```text
candidate-action generation
+
comparative action ranking
→ NOT RECOVERED
```

---

## D1.6 — Continue rather than stop

**Observed component**

```text
CONTINUE WITH A6
```

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: IMPLICIT-RECOVERABLE
MECHANICAL REPRODUCIBILITY: NO
RATIONALE: PARTIALLY RECOVERABLE
RULE: UNKNOWN-RULE
```

**Why**

The selected next object and its purpose are recorded, so continuation is observable and its local purpose is recoverable. The record does not establish a general continuation threshold or show that A6 dominated every alternative.

**Automation gap exposed**

```text
continuation authorization threshold
→ NOT RECOVERED
```

---

# D2 audit — A6 → A7

## D2.1 — Characterize A6 results under the frozen endpoint rules

**Observed component**

```text
section scaffold
→ T_change causal
→ T_instability practically small
→ T_verified practically small
```

**Classification**

```text
FUNCTION: STATISTICAL
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES
RATIONALE: RECOVERABLE
RULE: RECOVERABLE
```

**Authority consequence**

The scaffold result is separated by endpoint; null significance alone is not used where practical-equivalence classification is required.

**Automation gap exposed**

None identified at the inferential-classification component.

---

## D2.2 — Preserve the documented finer-rendering-versus-interaction fork

**Observed component**

The A6 guardrail states that if A6 is practically small for `T_instability`, the next discrimination should be:

```text
remaining finer rendering differences
versus
interaction
```

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES FOR RECOVERING THE FORK
RATIONALE: RECOVERABLE
RULE: RECOVERABLE FOR GENERATING THE TWO-WAY FORK
```

**Authority consequence**

Neither side of the fork is established merely by being named.

**Automation gap exposed**

This component recovers the candidate classes, not the rule choosing between them.

---

## D2.3 — Define the A7 interaction object and estimand

**Observed component**

```text
Gamma_FS = (UP - UF) - (LP - LF)
```

with the missing `UF` cell closed prospectively.

**Classification**

```text
FUNCTION: FORMAL
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES
RATIONALE: RECOVERABLE
RULE: RECOVERABLE
```

**Authority consequence**

```text
interaction
→ defined as testable causal object
↛ established explanation
```

**Automation gap exposed**

None at the level of executing the already selected estimand definition.

---

## D2.4 — Treat `Gamma_FS_instability` as the highest-information residual target

**Observed component**

The A7 contract explicitly names the instability interaction as the highest-information residual target motivating A7 while retaining all three endpoints as co-primary.

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: PARTIAL
RATIONALE: RECOVERABLE
RULE: UNKNOWN-RULE
```

**Why**

The target ranking is documented. The historical record does not provide a general computation that would reproduce the phrase `highest-information` from arbitrary candidate targets.

**Automation gap exposed**

```text
information-ranking criterion
→ NOT FORMALIZED
```

---

## D2.5 — Select interaction rather than finer rendering

**Observed component**

```text
SELECTED: A7 interaction factorial
NOT SELECTED: finer rendering branch
```

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: NOT-RECOVERABLE
MECHANICAL REPRODUCIBILITY: NO
RATIONALE: RECOVERABLE FOR WHAT A7 TESTS
RULE: UNKNOWN-RULE FOR WHY A7 DOMINATED THE OTHER DOCUMENTED FORK
```

**Authority consequence**

Only the interaction is promoted from live fork member to the next tested causal object.

**Automation gap exposed**

```text
comparative structural-selection rule
→ NOT RECOVERED
```

This is not repaired by labeling the move `earned complexity escalation`; that label was correctly removed from the historical trace.

---

## D2.6 — Continue with A7

**Observed component**

```text
CONTINUE WITH A7
```

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: IMPLICIT-RECOVERABLE
MECHANICAL REPRODUCIBILITY: PARTIAL
RATIONALE: RECOVERABLE
RULE: UNKNOWN-RULE FOR CONTINUE VS STOP
```

**Why**

The missing factorial cell and direct interaction test are explicit. A comparative stopping rule is not.

**Automation gap exposed**

```text
continue-vs-stop rule at D2
→ NOT RECOVERED
```

---

# D3 audit — A7 → R1

## D3.1 — Characterize the A7 instability interaction as practically small

**Observed component**

```text
Gamma_FS_instability
→ practically small at ±0.05
```

**Classification**

```text
FUNCTION: STATISTICAL
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES
RATIONALE: RECOVERABLE
RULE: RECOVERABLE
```

**Authority consequence**

The interaction explanation is not supported as a practically meaningful instability interaction under the inherited margin.

**Automation gap exposed**

None at the classification step.

---

## D3.2 — Refuse to infer heterogeneity from differing point estimates

**Observed component**

```text
different cohort / experiment point estimates
↛ heterogeneity
```

**Classification**

```text
FUNCTION: OTHER — authority-boundary application
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES
RATIONALE: RECOVERABLE
RULE: RECOVERABLE
```

**Why**

The R1 contract explicitly prohibits the inference.

**Authority consequence**

```text
A5 vs A7 difference
↛ heterogeneity claim
```

**Automation gap exposed**

No gap in applying this explicit prohibition. The generality of such a rule outside this case is not adjudicated here.

---

## D3.3 — Reframe the unresolved object as replication / transport

**Observed component**

```text
Does the inherited labeled-scaffold E0-only
encoding → T_instability contrast
replicate / transport across fresh prestates?
```

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: PARTIAL
RATIONALE: RECOVERABLE
RULE: UNKNOWN-RULE
```

**Why**

The R1 scientific object is explicit. The historical record does not provide a general rule that maps an arbitrary cross-experiment discrepancy into a replication/transport question.

**Authority consequence**

The discrepancy becomes a testable replication/transport question without becoming a heterogeneity claim.

**Automation gap exposed**

```text
when does a discrepancy warrant replication/transport?
→ NO FORMAL THRESHOLD RECOVERED
```

---

## D3.4 — Stop the A-series and explicitly decline A8

**Observed component**

```text
A-series localization branch
→ STOP
A8
→ NOT AUTHORIZED
```

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: EXPLICIT AS HISTORICAL STATUS
MECHANICAL REPRODUCIBILITY: PARTIAL
RATIONALE: PARTIALLY RECOVERABLE
RULE: UNKNOWN-RULE
```

**Why**

The R1 lineage explicitly records that the A-series stopped and no A8 finer-formatting ablation was authorized. It does not provide a general rule sufficient to reproduce this scope closure from arbitrary evidence states.

**Automation gap exposed**

```text
branch-local stopping criterion
→ NOT FORMALIZED
```

---

## D3.5 — Select R1 over stopping the empirical program or another action

**Observed component**

```text
R1 selected
```

Historical consideration of stopping before R1 or continuing other decomposition is `UNKNOWN` in the trace.

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: NOT-RECOVERABLE FOR COMPARATIVE SELECTION
MECHANICAL REPRODUCIBILITY: NO
RATIONALE: RECOVERABLE FOR R1'S PURPOSE
RULE: UNKNOWN-RULE
```

**Authority consequence**

R1 becomes authorized; unrecorded alternatives remain historically unknown rather than retroactively rejected.

**Automation gap exposed**

```text
candidate-action comparison at the localization→replication boundary
→ NOT RECOVERED
```

---

## D3.6 — Narrow R1 to one endpoint, one signal condition, one inherited encoding contrast, four fresh cohorts

**Observed component**

```text
fixed labeled scaffold
E0 only
fields vs prose
T_instability only
four fresh disjoint prestate cohorts
```

**Classification**

```text
FUNCTION: FORMAL
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES
RATIONALE: RECOVERABLE
RULE: RECOVERABLE AS THE FROZEN R1 CONTRACT
```

**Authority consequence**

R1 cannot silently expand into new representation discovery or a global correction construct.

**Automation gap exposed**

None for executing the frozen design once selected. Selection of that design remains covered by D3.3/D3.5.

---

## D3.7 — Continue R1 while the A-series remains stopped

**Observed component**

```text
A-SERIES: STOP
R1: CONTINUE
```

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: EXPLICIT AS HISTORICAL SCOPE STATUS
MECHANICAL REPRODUCIBILITY: PARTIAL
RATIONALE: RECOVERABLE
RULE: UNKNOWN-RULE
```

**Why**

The scope transition is explicit. A general nested-scope control rule is not present in the historical record.

**Automation gap exposed**

```text
scope-specific continuation / stopping rule
→ NOT RECOVERED
```

No controller architecture is inferred from this observation.

---

# D4 audit — R1 → STOP

## D4.1 — Estimate and classify the replicated common encoding effect

**Observed component**

```text
Delta_common = +0.033975
95% CI       = [+0.021316,+0.047791]
p            = 0.00019996
```

with the resulting historical classification:

```text
encoding → T_instability
CAUSAL / REPLICATED / PRACTICALLY SMALL
```

**Classification**

```text
FUNCTION: STATISTICAL
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES
RATIONALE: RECOVERABLE
RULE: RECOVERABLE
```

**Authority consequence**

The inherited encoding contrast gains replicated/nonzero authority while remaining bounded inside the inherited practical margin.

**Automation gap exposed**

None at this inferential classification step.

---

## D4.2 — Interpret the transport diagnostic without upgrading it to invariance

**Observed component**

```text
Q = 1.120334
p = 0.772168
I² = 0
tau²_DL = 0
```

Authorized interpretation:

```text
compatible with a common-effect model
≠ transport invariance established
```

**Classification**

```text
FUNCTION: STATISTICAL
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES
RATIONALE: RECOVERABLE
RULE: RECOVERABLE
```

**Authority consequence**

```text
excess cohort variation → NOT DETECTED
transport invariance    → NOT ESTABLISHED
```

**Automation gap exposed**

None for this prespecified interpretation boundary.

---

## D4.3 — Preserve endpoint locality

**Observed component**

```text
T_verified encoding × scaffold interaction
→ UNRESOLVED

unresolved T_verified interaction
↛ reopen T_instability
```

**Classification**

```text
FUNCTION: OTHER — authority-boundary application
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES FOR THIS NAMED BOUNDARY
RATIONALE: RECOVERABLE
RULE: RECOVERABLE FOR THIS CASE
```

**Authority consequence**

Residual uncertainty remains local and does not automatically reopen a separately resolved endpoint branch.

**Automation gap exposed**

The historical rule is case-specific. This audit does not infer a general endpoint-locality primitive.

---

## D4.4 — Mark A8, R2, and additional `T_instability` decomposition as not earned

**Observed component**

```text
A8                               NOT EARNED
R2                               NOT EARNED
additional T_instability work    NOT EARNED
```

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: EXPLICIT AS TERMINAL STATUS
MECHANICAL REPRODUCIBILITY: PARTIAL
RATIONALE: RECOVERABLE
RULE: UNKNOWN-RULE
```

**Why**

The terminal record states why the branches are not earned in this case: localization is sufficiently resolved, the replication/transport question is closed, and no sufficiently discriminating unresolved question authorizes escalation.

But it does not contain a formal scoring rule that would reproduce the same `NOT EARNED` classifications on arbitrary candidate experiments.

**Automation gap exposed**

```text
candidate-experiment admissibility rule
→ NOT FORMALIZED
```

---

## D4.5 — Select STOP while uncertainty remains

**Observed component**

```text
remaining uncertainty exists
+
no unresolved question supports a sufficiently discriminating next experiment
→ STOP
```

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: EXPLICIT AS RATIONALE
MECHANICAL REPRODUCIBILITY: NO
RATIONALE: RECOVERABLE
RULE: UNKNOWN-RULE
```

**Why**

The terminal stopping rationale is explicit and therefore historically real. However, the historical record contains no formal definition of:

```text
sufficiently discriminating
```

and no formal admissibility threshold or next-experiment value function.

Therefore the STOP decision can be described and its rationale recovered, but cannot be mechanically regenerated from the historical record alone.

**Authority consequence**

```text
Pilot 0 → CLOSED
```

without implying truth, completeness, or certainty.

**Automation gap exposed**

```text
stopping criterion operationalization
→ NOT RECOVERED
```

This is a boundary finding, not authorization to invent a stopping primitive.

---

## D4.6 — Cost / constraint weighting in the STOP decision

**Observed component**

The trace states that whether and how cost or operational constraints entered D1–D4 is not established.

**Classification**

```text
FUNCTION: VALUE/COST
SPECIFICATION: NOT-RECOVERABLE
MECHANICAL REPRODUCIBILITY: UNKNOWN
RATIONALE: UNKNOWN-RATIONALE
RULE: UNKNOWN-RULE
```

**Authority consequence**

No claim that Pilot 0 stopped because of a formal cost-benefit calculation is authorized.

**Automation gap exposed**

```text
cost / resource weighting
→ HISTORICALLY UNKNOWN
```

---

# Audit summary — descriptive, not abstractive

This section summarizes what the component audit found. It does **not** promote any component into a candidate controller primitive.

## Components with explicit, mechanically reproducible historical rules

The audit finds strong recoverability for several components that were already frozen as inferential or formal operations, including:

```text
endpoint causal / practical-equivalence classification
formal estimand definition
blocked replication/common-effect analysis
transport compatibility interpretation
named authority prohibitions
```

These are historical facts about how portions of Pilot 0 were governed. They are not evidence that a general controller architecture has been identified.

## Components with recoverable rationale but missing generating rule

The audit repeatedly finds this pattern:

```text
action observed
+
local purpose recoverable
+
comparative rule absent
```

It occurs in consequential places including:

```text
A5 → A6 structural selection
A6 → A7 interaction selection
A7 → R1 replication/transport selection
R1 → STOP
```

This is an audit result, not a primitive claim.

## Components whose historical status remains unknown

The repaired trace and this audit do not establish complete candidate-action sets for D1–D4.

In particular, unrecorded analytically possible actions remain:

```text
UNKNOWN AS HISTORICAL CONSIDERATIONS
```

The audit therefore cannot reconstruct full comparative choice sets retrospectively.

## Components not mechanically reproducible from the historical record

The clearest gaps are:

```text
comparative structural-action ranking
replication-discrepancy threshold
candidate-experiment admissibility threshold
continue-vs-stop threshold
cost / constraint weighting
formal meaning of “sufficiently discriminating”
```

These are exposed automation boundaries. They are **not** automatically controller requirements or candidate primitives.

## Negative audit result is valid

The audit explicitly permits:

```text
component observed
→ function identifiable
→ rationale partly or fully recoverable
→ rule not recoverable
→ mechanical reproduction unavailable
→ NO ABSTRACTION AUTHORIZED FROM THIS FACT ALONE
```

That outcome occurs multiple times in Pilot 0.

---

# Abstraction gate remains closed

This audit does not ask whether the observed components should become controller primitives.

The next authority question, if this audit itself survives review, would be whether any audited component satisfies a separate abstraction gate involving provenance, functional distinctness, stable/recurrent structure, a specifiable boundary, and independent falsifiability.

That gate has **not** been run here.

```text
Human-Judgment Audit
→ component decomposition only

Human-Judgment Audit
↛ candidate primitives
↛ controller architecture
↛ controller specification
↛ Pilot 1
↛ new experiment
```

## Terminal status of this artifact

```text
TRACE
→ provenance-valid input

AUDIT
→ completed as a draft artifact

PRIMITIVE EXTRACTION
→ NOT AUTHORIZED BY THIS DOCUMENT ALONE

CONTROLLER SPECIFICATION
→ NOT AUTHORIZED

CONTROLLER EXPERIMENT
→ NOT EARNED
```

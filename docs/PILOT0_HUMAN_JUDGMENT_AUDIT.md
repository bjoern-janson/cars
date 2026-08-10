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

`OTHER` is used only when the component's function is identifiable but does not fit the other classes. Any subtype is stated outside the classification value.

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

### Ontology discipline

Classification fields use only the exact frozen values above. Qualifiers such as `FOR THIS CASE`, `AS HISTORICAL STATUS`, or `PARTIALLY RECOVERABLE` are not additional ontology states.

When one row contains two epistemically different questions:

```text
split the component
→ do not enrich the category
```

Nuance belongs in the explanatory text, not in the classification token.

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
FUNCTION: OTHER
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES
RATIONALE: RECOVERABLE
RULE: RECOVERABLE
```

Function subtype: `authority-boundary application`.

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

## D1.4a — Recover the A5 conditional guardrail as written

**Observed component**

The A5 contract names remaining outer framing before immediate interaction under its stated practically-small condition.

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES
RATIONALE: RECOVERABLE
RULE: RECOVERABLE
```

**Why**

The guardrail and its antecedent are written explicitly in the historical contract. This component asks only whether that conditional rule can be recovered as written.

**Authority consequence**

The historical record contains an explicit conditional preference for outer framing before immediate interaction under the stated antecedent.

---

## D1.4b — Determine whether the guardrail mechanically decides the realized mixed-A5 state

**Observed component**

The realized A5 result was mixed across endpoints rather than practically small across all A4c endpoints.

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: NOT-RECOVERABLE
MECHANICAL REPRODUCIBILITY: NO
RATIONALE: UNKNOWN-RATIONALE
RULE: UNKNOWN-RULE
```

**Why**

The recorded conditional antecedent does not match the realized state exactly. The historical record does not supply an additional rule explaining how that guardrail should compose with the mixed outcome.

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
RATIONALE: RECOVERABLE
RULE: UNKNOWN-RULE
```

**Why**

The purpose of A6 is documented. A rule establishing that A6 was preferable to all available alternatives is not. `RATIONALE: RECOVERABLE` refers only to the documented purpose of A6; it does not imply recovery of the comparative selection rule.

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

## D1.6a — Recover the local purpose of continuing with A6

**Observed component**

```text
CONTINUE WITH A6
```

with A6's outer-scaffold purpose documented in the frozen contract.

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: IMPLICIT-RECOVERABLE
MECHANICAL REPRODUCIBILITY: PARTIAL
RATIONALE: RECOVERABLE
RULE: UNKNOWN-RULE
```

**Why**

The continuation action is observed and the selected experiment's local purpose is recoverable. The historical record does not encode a general continuation rule.

---

## D1.6b — Recover the comparative continue-vs-stop rationale

**Observed component**

The program continued with A6 rather than stopping at D1.

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: NOT-RECOVERABLE
MECHANICAL REPRODUCIBILITY: NO
RATIONALE: UNKNOWN-RATIONALE
RULE: UNKNOWN-RULE
```

**Why**

The record does not establish a comparative rationale showing why continuation was preferable to stopping or every other analytically possible action.

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
MECHANICAL REPRODUCIBILITY: YES
RATIONALE: RECOVERABLE
RULE: RECOVERABLE
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
RATIONALE: RECOVERABLE
RULE: UNKNOWN-RULE
```

**Why**

The purpose and object of A7 are recoverable. The comparative rule explaining why A7 dominated the other documented fork member is not.

**Authority consequence**

Only the interaction is promoted from live fork member to the next tested causal object.

**Automation gap exposed**

```text
comparative structural-selection rule
→ NOT RECOVERED
```

This is not repaired by labeling the move `earned complexity escalation`; that label was correctly removed from the historical trace.

---

## D2.6a — Recover the local purpose of continuing with A7

**Observed component**

```text
CONTINUE WITH A7
```

with a missing factorial cell and direct interaction test explicitly documented.

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: IMPLICIT-RECOVERABLE
MECHANICAL REPRODUCIBILITY: PARTIAL
RATIONALE: RECOVERABLE
RULE: UNKNOWN-RULE
```

**Why**

The selected experiment's local purpose is explicit even though no general continue rule is encoded.

---

## D2.6b — Recover the comparative continue-vs-stop rationale

**Observed component**

The program continued with A7 rather than stopping at D2.

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: NOT-RECOVERABLE
MECHANICAL REPRODUCIBILITY: NO
RATIONALE: UNKNOWN-RATIONALE
RULE: UNKNOWN-RULE
```

**Why**

The historical record does not provide a comparative rule or rationale establishing that continuation dominated stopping.

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
FUNCTION: OTHER
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES
RATIONALE: RECOVERABLE
RULE: RECOVERABLE
```

Function subtype: `authority-boundary application`.

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

## D3.4a — Recover the historical A-series STOP / no-A8 status

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
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES
RATIONALE: RECOVERABLE
RULE: UNKNOWN-RULE
```

**Why**

The historical scope outcome is explicit in the R1 lineage. The record supports recovery of the status and its local context, but not a general rule that would generate the same closure from arbitrary evidence states.

---

## D3.4b — Recover the generating rule for A-series closure

**Observed component**

The A-series was closed and A8 was not authorized before R1.

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: NOT-RECOVERABLE
MECHANICAL REPRODUCIBILITY: NO
RATIONALE: UNKNOWN-RATIONALE
RULE: UNKNOWN-RULE
```

**Why**

No formal or general branch-local stopping criterion is recorded at this decision point.

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
SPECIFICATION: NOT-RECOVERABLE
MECHANICAL REPRODUCIBILITY: NO
RATIONALE: RECOVERABLE
RULE: UNKNOWN-RULE
```

**Why**

R1's purpose is recoverable. A comparative action-selection rationale and generating rule are not. Unrecorded alternatives remain historically unknown rather than retroactively rejected.

**Authority consequence**

R1 becomes authorized; unrecorded alternatives do not gain historical status.

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
RULE: RECOVERABLE
```

**Authority consequence**

R1 cannot silently expand into new representation discovery or a global correction construct.

**Automation gap exposed**

None for executing the frozen design once selected. Selection of that design remains covered by D3.3/D3.5.

---

## D3.7a — Recover the historical scope transition

**Observed component**

```text
A-SERIES: STOP
R1: CONTINUE
```

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES
RATIONALE: RECOVERABLE
RULE: UNKNOWN-RULE
```

**Why**

The scope transition itself is explicit in the historical record.

---

## D3.7b — Recover a general rule for scope-specific continuation / stopping

**Observed component**

One branch stopped while a different replication/transport branch continued.

**Classification**

```text
FUNCTION: STRUCTURAL
SPECIFICATION: NOT-RECOVERABLE
MECHANICAL REPRODUCIBILITY: NO
RATIONALE: UNKNOWN-RATIONALE
RULE: UNKNOWN-RULE
```

**Why**

A general nested-scope control rule is not present in the historical record.

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
FUNCTION: OTHER
SPECIFICATION: EXPLICIT
MECHANICAL REPRODUCIBILITY: YES
RATIONALE: RECOVERABLE
RULE: RECOVERABLE
```

Function subtype: `authority-boundary application`.

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
SPECIFICATION: EXPLICIT
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
SPECIFICATION: EXPLICIT
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

The audit explicitly permits component-level outcomes such as:

```text
component observed
→ function identifiable
→ RATIONALE = RECOVERABLE or UNKNOWN-RATIONALE
→ RULE = UNKNOWN-RULE
→ mechanical reproduction unavailable
→ NO ABSTRACTION AUTHORIZED FROM THIS FACT ALONE
```

No intermediate rationale or rule category is introduced to make an awkward component fit.

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

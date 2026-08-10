# Correction Transition Invariants

## Status

```text
PILOT 0
→ READ-ONLY EMPIRICAL RECORD

DECISION TRACE
→ PROVENANCE PASS

HUMAN-JUDGMENT AUDIT
→ PASS

ABSTRACTION GATE
→ PASS
→ NO CONSEQUENTIAL ACTION-SELECTION ABSTRACTION EARNED

THIS DOCUMENT
→ NEW HYPOTHESIS SPACE
→ CANDIDATE TRANSITION INVARIANTS
→ NOT A CONTROLLER SPECIFICATION
→ NOT PRIMITIVE EXTRACTION
→ NOT PILOT 1
→ NOT A NEW EXPERIMENT
```

The failed C2 primitive-promotion branch is intentionally not inherited. No controller primitive is assumed here.

This artifact asks one question:

> **Can correction quality be evaluated from properties of epistemic-state transitions, independently of reproducing the historical human decision sequence?**

The candidate object is not `STOP`, `REPLICATE`, or `CHOOSE_NEXT_TEST`.

It is:

```text
AUTHORIZED TRANSFORMATION
```

meaning, provisionally:

```text
an epistemic-state change whose authority,
scope, and structural consequences are licensed
by the evidence available at that transition
```

This is a hypothesis, not an established principle.

---

# Anti-retrofit rule

```text
Pilot 0 observation
→ candidate invariant

candidate invariant
↛ established principle
↛ controller primitive
↛ controller architecture
```

Likewise:

```text
primitive-extraction failure
↛ transition-invariant success
```

Every candidate below requires independent falsification outside the Pilot-0 decision sequence.

---

# Provenance classes

```text
P0-EMPIRICAL
    Frozen Pilot-0 experimental result.

P0-DECISION
    Frozen contract, provenance-valid trace,
    or terminal decision record.

POST-P0-METHOD
    Behavior observed in the later provenance,
    audit, and abstraction process.

CONCEPTUAL
    Proposed analytical possibility only.
```

Critical boundary:

```text
POST-P0-METHOD ≠ P0-EMPIRICAL
```

---

# Minimal transition object

For this artifact only:

```text
S_t = explicit epistemic state
E_t = new evidence / validated consequence

T_t : (S_t, E_t) → S_{t+1}
```

`S_t` may contain, where represented:

```text
claims / statuses
authority and scope
live alternatives
provenance
open / closed questions
admissible consequences
```

The candidate invariants evaluate `T_t`.

They do not choose `S_{t+1}`.

```text
transition audit      ≠ transition generation
transition legitimacy ≠ action optimality
valid transition      ↛ unique next action
```

A system may choose a different experiment from the historical researcher and still make a justified transition.

A system may imitate the historical sequence while making an unjustified transition.

---

# Candidate invariants

```text
I1  EVIDENCE-BOUNDED AUTHORITY
I2  SCOPE LOCALITY
I3  REVISION CONSERVATION
I4  ALTERNATIVE PRESERVATION
I5  ESCALATION JUSTIFICATION
I6  TERMINATION LEGITIMACY
I7  REPLICATION DISCIPLINE
```

All seven have status:

```text
CANDIDATE HYPOTHESIS
NOT ESTABLISHED
```

---

## I1 — Evidence-Bounded Authority

**Observed basis**

```text
SOURCE: P0-DECISION + POST-P0-METHOD
```

Examples include:

```text
different point estimates ↛ heterogeneity
common-effect compatibility ≠ invariance
localized causal result ↛ global mechanism
```

**Candidate invariant**

```text
authority may increase only along dimensions
identified by the available evidence
```

**Would forbid**

```text
local evidence → unsupported global authority
failure → unsupported causal diagnosis
compatibility → stronger unearned claim
```

**Known gap**

No domain-general representation of authority dimensions has been established.

**Independent falsification requirement**

Use held-out cases with explicit evidence-to-authority relations and compare transitions that remain within versus exceed those relations.

```text
STATUS: NOT ESTABLISHED
```

---

## I2 — Scope Locality

**Observed basis**

```text
SOURCE: P0-DECISION
```

Pilot 0 explicitly preserved:

```text
unresolved T_verified interaction
↛ reopen T_instability
```

**Candidate invariant**

```text
evidence concerning X
must not silently revise Y
without a licensed X→Y link
```

**Would forbid**

```text
uncertainty in A → automatic reopening of B
local failure → global reset
```

**Known gap**

A general representation of scope linkage is not yet available.

**Independent falsification requirement**

Use predeclared X/Y scopes with known link-present versus link-absent cases and test whether unrelated Y-state is preserved.

```text
STATUS: NOT ESTABLISHED
```

---

## I3 — Revision Conservation

**Observed basis**

```text
SOURCE: P0-DECISION + POST-P0-METHOD
```

Examples:

```text
representation boundary localized before deeper escalation
provenance defect → repair trace only
schema defect → split component, not enlarge ontology
```

**Candidate invariant**

```text
revise the smallest evidence-identified failure locus
while preserving unaffected validated structure
```

**Would forbid**

```text
local contradiction → gratuitous global rewrite
estimator failure → automatic proposition rejection
```

**Known gap**

`smallest`, `unaffected`, and `sufficient revision` are not generally operationalized.

**Independent falsification requirement**

Use modular tasks with a known localized failure and independently validated unaffected modules; compare local versus broad revisions prospectively.

```text
STATUS: NOT ESTABLISHED
```

---

## I4 — Alternative Preservation

**Observed basis**

```text
SOURCE: POST-P0-METHOD
```

Examples:

```text
unknown historical rationale → UNKNOWN-RATIONALE
missing generating rule → UNKNOWN-RULE
unsupported candidate set → not reconstructed by plausibility
```

**Candidate invariant**

```text
when evidence does not discriminate live alternatives,
a justified transition preserves their distinguishability
```

**Would forbid**

```text
insufficient evidence → forced single explanation
one observed action → inferred universal rule
```

**Known gap**

Pilot 0 did not directly test whether alternative preservation improves later correction.

**Independent falsification requirement**

Use tasks where hypotheses are initially observationally equivalent and become distinguishable later; compare early-preservation versus early-collapse trajectories.

```text
STATUS: NOT ESTABLISHED
```

---

## I5 — Escalation Justification

**Observed basis**

```text
SOURCE: P0-DECISION
```

Pilot-0 contracts repeatedly constrained automatic complexity escalation.

**Candidate invariant**

```text
moving to a more complex intervention or representation
requires incremental discriminating justification
not already supplied by a shallower alternative
```

**Would forbid**

```text
remaining uncertainty → experiment required
possible interaction → interaction study automatically
point-estimate discrepancy → heterogeneity program
```

**Known gap**

`incremental discriminating justification` is not operationally defined.

That same gap blocked structural action-selection primitives earlier.

**Independent falsification requirement**

A future task must predefine candidate actions, relative complexity, live hypotheses, and what evidence each action could discriminate before outcomes are observed.

```text
STATUS: NOT ESTABLISHED
FALSIFICATION READY: NO
```

---

## I6 — Termination Legitimacy

**Observed basis**

```text
SOURCE: P0-DECISION
```

Pilot 0 stopped with residual uncertainty:

```text
remaining uncertainty
+
no sufficiently discriminating unresolved question
→ STOP
```

while preserving:

```text
STOP ≠ truth ≠ completeness ≠ certainty
```

**Candidate invariant**

```text
residual uncertainty does not itself authorize continuation
```

and, more strongly:

```text
stopping may be legitimate when no currently available
transition has sufficient prospective justification
```

**Would forbid**

```text
uncertainty remains → action required
experiment possible → experiment authorized
```

**Known gap**

`sufficiently discriminating` and `sufficient justification` remain undefined. Pilot 0 contains only one terminal case.

**Independent falsification requirement**

A future task must prospectively define residual uncertainties, candidate actions, and criteria for authority-changing discrimination before STOP can be tested independently.

```text
STATUS: NOT ESTABLISHED
FALSIFICATION READY: NO
```

---

## I7 — Replication Discipline

**Observed basis**

```text
SOURCE: P0-DECISION + P0-EMPIRICAL
```

R1 explicitly enforced:

```text
different point estimates ↛ heterogeneity
```

and prospectively separated common-effect compatibility from invariance.

**Candidate invariant**

```text
discrepancy may motivate discrimination,
but does not acquire heterogeneity / transport-failure authority
without an appropriate direct test
```

**Would forbid**

```text
different estimates → heterogeneity claim
common-effect compatibility → invariance claim
```

**Known gap**

The appropriate discrimination machinery is domain-dependent.

**Independent falsification requirement**

Use held-out repeated-estimate problems with known common-effect, heterogeneous-effect, and transport-failure regimes; measure both false heterogeneity authority and failure to detect real heterogeneity.

```text
STATUS: NOT ESTABLISHED
```

---

# Readiness map

This is not a validation ranking.

It asks only whether an independent test object appears specifiable without first solving the missing action-selection controller.

| Candidate | Source basis | Independent test object currently specifiable? | Established? |
| --- | --- | --- | --- |
| I1 Evidence-bounded authority | P0-decision / post-P0 | **YES**, if authority dimensions are explicit | **NO** |
| I2 Scope locality | P0-decision | **YES**, if scope linkage is explicit | **NO** |
| I3 Revision conservation | process-heavy | **PARTIAL** | **NO** |
| I4 Alternative preservation | post-P0 method | **YES** | **NO** |
| I5 Escalation justification | P0-decision | **NO** — justification criterion missing | **NO** |
| I6 Termination legitimacy | one terminal case | **NO** — stopping criterion missing | **NO** |
| I7 Replication discipline | P0-decision / empirical | **YES**, domain-specific | **NO** |

The `YES` rows are not promoted. They only survive the cheaper question:

```text
can an independent falsification object be specified?
```

---

# Candidate transition-audit target

If any invariant later survives independent testing, the smallest automation object would be:

```text
current epistemic state
+
new evidence
+
proposed transition
        ↓
transition audit
        ↓
AUTHORIZED ALONG TESTED DIMENSION
or
VIOLATION ALONG TESTED DIMENSION
```

Important:

```text
AUTHORIZED ALONG TESTED DIMENSION
↛ globally justified transition
```

No transition generator is proposed.

No next-action selector is proposed.

No scalar transition-quality score is proposed.

No conjunction of I1–I7 is assumed sufficient.

---

# Independent-falsification gate

A candidate invariant becomes a genuine empirical object only if a test can specify, without using Pilot 0 as the answer key:

```text
1. epistemic state
2. new evidence
3. proposed transition
4. invariant-specific expected relation
5. violation criterion
6. held-out cases
7. result capable of falsifying or revising the invariant
```

Invalid test:

```text
"did the system choose what the Pilot-0 researcher chose?"
```

Relevant test:

```text
"did the proposed transition respect the independently
specified constraint on justified epistemic change?"
```

---

# Terminal boundary

```text
CORRECTION TRANSITION INVARIANTS
→ 7 candidate hypotheses
→ 0 established invariants
→ 0 controller primitives
→ 0 controller specification
```

Current authority state:

```text
Pilot-0 primitive extraction
→ TERMINATED WITH ∅

transition-quality framing
→ NEW HYPOTHESIS SPACE

I1–I7
→ CANDIDATES ONLY

controller specification
→ NOT AUTHORIZED

Pilot 1
→ NOT EARNED
```

The next question is only:

> **Does any candidate invariant survive an independent test in which transition quality can be scored without reproducing the Pilot-0 human decision sequence?**

If that cannot be made operational without importing the missing controller, this line stops.
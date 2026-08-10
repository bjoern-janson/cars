# Correction Transition Invariants

## Status

```text
PILOT 0
→ READ-ONLY EMPIRICAL RECORD

PILOT0_DECISION_TRACE.md
→ PROVENANCE PASS

PILOT0_HUMAN_JUDGMENT_AUDIT.md
→ SCHEMA / FIDELITY PASS

PILOT0_ABSTRACTION_GATE.md
→ PASS
→ NO CONSEQUENTIAL ACTION-SELECTION ABSTRACTION EARNED

THIS DOCUMENT
→ NEW SCIENTIFIC OBJECT
→ CANDIDATE TRANSITION INVARIANTS
→ NOT A CONTROLLER SPECIFICATION
→ NOT PRIMITIVE EXTRACTION
→ NOT PILOT 1
→ NOT A NEW EXPERIMENT
```

The failed C2 primitive-promotion branch is intentionally **not** inherited into this branch. No controller primitive is assumed here.

This artifact asks a different question from the Pilot-0 extraction lineage:

> **Can correction quality be characterized by properties of epistemic-state transitions, independently of whether a system reproduces the historical human action sequence?**

The object under consideration is not a command such as `STOP`, `REPLICATE`, or `CHOOSE_NEXT_TEST`.

The candidate object is:

```text
AUTHORIZED TRANSFORMATION
```

or, more cautiously:

```text
transition whose change in epistemic state
is licensed by the evidence and preserves
specified authority / scope / structure constraints
```

Nothing in this document establishes that such an object is fundamental, sufficient, or complete.

---

# Anti-retrofit rule

The transition framing does not get authority merely because controller-primitive extraction returned zero survivors.

```text
primitive-extraction dead end
↛ transition invariants are true
```

Likewise:

```text
Pilot 0 observation
→ candidate invariant

candidate invariant
↛ established principle
↛ controller primitive
↛ controller architecture
```

Every candidate invariant below must eventually face an independent falsification requirement outside the historical decision sequence from which it was noticed.

If no candidate can be made independently testable without importing new unearned rules, this line of inquiry stops.

---

# Source-provenance classes

Candidate invariants can be motivated by different kinds of evidence. Those sources are not interchangeable.

```text
P0-EMPIRICAL
    Directly supported by frozen Pilot-0 experimental results.

P0-DECISION
    Directly supported by frozen pre-outcome contracts,
    the provenance-valid decision trace, or terminal record.

POST-P0-METHOD
    Observed in the later provenance / audit / abstraction process.
    This is methodological behavior, not a Pilot-0 empirical result.

CONCEPTUAL
    Proposed as an analytical possibility only.
```

Important boundary:

```text
POST-P0-METHOD
≠
P0-EMPIRICAL
```

A transition property can be scientifically interesting even when Pilot 0 did not empirically establish it, but its provenance must remain explicit.

---

# Minimal transition object

For this artifact only, let:

```text
S_t
= an explicit epistemic state at time t
```

which may include, where represented:

```text
claims / statuses
claimed authority and scope
live alternatives
provenance
open / closed local questions
admissible actions or consequences
```

Let:

```text
E_t
= new evidence or a new validated consequence available at t
```

and let a realized or proposed transition be:

```text
T_t = (S_t, E_t) → S_{t+1}
```

The candidate invariants are predicates on the legitimacy of `T_t`.

They are **not** policies that choose `S_{t+1}`.

Thus:

```text
transition audit
≠ transition generation

transition legitimacy
≠ action optimality

valid transition
↛ unique next transition
```

A system could choose a different experiment from the historical researcher and still satisfy the same transition constraints.

Conversely, a system could imitate the historical sequence while violating the constraints.

---

# Decision imitation versus transition legitimacy

The distinction motivating this artifact is:

```text
SYSTEM A
→ chooses a different next experiment
→ preserves authority ceilings
→ preserves unrelated scope
→ keeps unresolved alternatives explicit
→ makes only evidence-supported revisions

SYSTEM B
→ reproduces the historical next experiment
→ silently upgrades authority
→ collapses unresolved alternatives
→ revises unrelated structure
```

A sequence-imitation benchmark may prefer `B`.

A transition-quality framework may prefer `A`.

This artifact does not yet claim that the latter judgment is correct. It isolates it as a falsifiable research direction.

---

# Candidate invariants

The following seven candidates are hypotheses only.

```text
I1  EVIDENCE-BOUNDED AUTHORITY
I2  SCOPE LOCALITY
I3  REVISION CONSERVATION
I4  ALTERNATIVE PRESERVATION
I5  ESCALATION JUSTIFICATION
I6  TERMINATION LEGITIMACY
I7  REPLICATION DISCIPLINE
```

For each candidate the document records:

```text
OBSERVED BASIS
CANDIDATE GENERALIZATION
WHAT IT WOULD FORBID
KNOWN LIMIT
INDEPENDENT FALSIFICATION REQUIREMENT
STATUS
```

No candidate receives established-principle status here.

---

# I1 — Evidence-Bounded Authority

## Observed basis

Source classes:

```text
P0-DECISION
POST-P0-METHOD
```

Pilot-0 contracts and terminal interpretation repeatedly preserve explicit non-implications, including examples such as:

```text
different point estimates
↛ heterogeneity

common-effect compatibility
≠ transport invariance

localized causal result
↛ psychological mechanism
↛ global correction capacity
```

The post-Pilot-0 abstraction lineage also rejected promotion when evidence did not distinguish controller-specific necessity from generic policy enforcement.

## Candidate generalization

```text
A transition may increase authority
only along dimensions identified by
available evidence / validated consequence.
```

In transition form:

```text
ΔAuthority(T_t)
⊆
Authority dimensions licensed by E_t
```

This notation is descriptive, not a frozen mathematical model.

## What it would forbid

```text
local effect
→ global mechanism claim

compatibility
→ invariance claim

discrepancy
→ heterogeneity authority

failure signal
→ unsupported causal diagnosis
```

## Known limit

The historical record contains multiple examples of authority ceilings but does not establish a domain-general representation of authority dimensions.

Therefore:

```text
observed non-implications
↛ complete authority algebra
```

## Independent falsification requirement

Construct independent cases with:

```text
explicit evidence E
explicitly defined claim dimensions
known evidence-to-authority relation
candidate transitions that vary only in authority expansion
```

The invariant predicts rejection of transitions that add authority outside the evidence-identified dimensions while allowing evidence-supported authority changes.

It would be falsified, or require revision, if independently valid correction consistently requires authority expansion not identifiable from the available evidence representation.

## Status

```text
OBSERVED PATTERN: YES
POSSIBLE GENERALIZATION: YES
INDEPENDENTLY ESTABLISHED: NO
```

---

# I2 — Scope Locality

## Observed basis

Source class:

```text
P0-DECISION
```

The terminal Pilot-0 record explicitly preserves endpoint locality:

```text
unresolved T_verified interaction
↛ reopen T_instability
```

More generally, the A-series and R1 were treated as distinct scopes even when one branch remained unresolved.

## Candidate generalization

```text
Evidence concerning object / scope X
must not silently revise or reopen Y
without an identified link that licenses the cross-scope change.
```

Transition form:

```text
E_t targets X
+
no licensed X→Y link
→
ΔY = 0
```

Again, this is a candidate constraint, not an established law.

## What it would forbid

```text
uncertainty in endpoint A
→ automatic reopening of endpoint B

failure in one representation layer
→ global theory reset

new evidence about one claim
→ silent changes to unrelated claims
```

## Known limit

A general rule for deciding when two scopes are sufficiently linked is not supplied by Pilot 0.

Thus:

```text
scope locality
requires a representation of scope linkage
that is not yet generalized
```

## Independent falsification requirement

Use independent tasks with predeclared partitions:

```text
scope X
scope Y
known link present / absent
```

Supply evidence local to `X` and compare candidate transitions that either preserve or modify `Y`.

The invariant predicts:

```text
no licensed link
→ Y preserved

licensed link
→ Y may change within the link's authority
```

A consistent need for justified cross-scope revision without representable linkage would challenge the invariant or the state representation.

## Status

```text
OBSERVED PATTERN: YES
POSSIBLE GENERALIZATION: YES
INDEPENDENTLY ESTABLISHED: NO
```

---

# I3 — Revision Conservation

## Observed basis

Source classes:

```text
P0-DECISION
POST-P0-METHOD
```

The Pilot-0 A-series repeatedly isolated shallower representation boundaries before adding further complexity.

The post-Pilot-0 lineage also repaired failures at the narrowest identified layer:

```text
provenance failure
→ repair trace
↛ redesign controller theory

schema contradiction
→ split overloaded audit component
↛ enlarge ontology
```

These are methodological observations, not direct evidence that a general correction system must behave this way.

## Candidate generalization

```text
A justified correction should change the
smallest structure whose failure is identified
while preserving unaffected structure.
```

Equivalent candidate transition property:

```text
identified failure locus L
→ revision concentrated on L
→ unrelated validated structure preserved
```

## What it would forbid

```text
local contradiction
→ global rewrite without evidence

schema defect
→ conceptual redesign

failed estimator
→ automatic rejection of scientific proposition
```

## Known limit

The terms:

```text
smallest
unaffected
sufficient revision
```

are not yet operationally defined across arbitrary epistemic representations.

This candidate therefore carries a substantial representation problem.

## Independent falsification requirement

Create tasks with a known modular state structure in which a contradiction identifies one module and held-out evidence validates the others.

Compare transitions that:

```text
A: repair the identified module only
B: also alter independently validated modules
```

A test must determine whether `B` ever yields systematically better future validity for reasons not captured by the known failure locus.

If broad revision is repeatedly required despite a correctly identified local failure, the candidate would need revision.

## Status

```text
OBSERVED PATTERN: YES, PRIMARILY PROCESS-LEVEL
POSSIBLE GENERALIZATION: YES
INDEPENDENTLY ESTABLISHED: NO
```

---

# I4 — Alternative Preservation

## Observed basis

Source class:

```text
POST-P0-METHOD
```

The strongest evidence for this candidate comes from the reconstruction/audit process rather than Pilot-0 experimental outcomes.

Examples:

```text
unsupported historical candidate set
→ UNKNOWN
↛ reconstructed by plausibility

recoverable rationale
+
missing generating rule
→ UNKNOWN-RULE
↛ inferred rule
```

The post-Pilot-0 process preserved distinctions between unresolved alternatives instead of collapsing them into a cleaner narrative.

## Candidate generalization

```text
When available evidence does not discriminate
between live alternatives, a justified transition
must preserve their distinguishability.
```

This does not require equal probability or equal plausibility.

It requires only that unresolved alternatives are not silently converted into resolved ones.

## What it would forbid

```text
insufficient evidence
→ forced single explanation

unknown rationale
→ plausible reconstructed rationale

one observed action
→ inferred universal generating rule
```

## Known limit

Pilot 0 did not directly test whether alternative preservation improves downstream correction quality.

Thus this candidate currently rests heavily on methodological discipline rather than empirical outcome evidence.

## Independent falsification requirement

Use tasks with two or more explicitly distinguishable hypotheses that are observationally equivalent under current evidence but become distinguishable after later evidence.

Compare systems that:

```text
A: preserve the unresolved alternatives
B: collapse early to one alternative
```

Measure later correction cost, error, recoverability, and authority leakage after discriminating evidence arrives.

A consistent advantage for early collapse without compensating authority error would challenge the candidate.

## Status

```text
OBSERVED PATTERN: POST-P0 METHOD ONLY
POSSIBLE GENERALIZATION: YES
INDEPENDENTLY ESTABLISHED: NO
```

---

# I5 — Escalation Justification

## Observed basis

Source class:

```text
P0-DECISION
```

Pilot-0 pre-outcome contracts repeatedly constrained escalation:

```text
A5
→ isolate prior-state encoding before outer scaffold / interaction escalation

A6
→ if practically small for instability,
   discriminate finer rendering versus interaction;
   neither automatic

A7
→ practically small interaction
   does not automatically authorize further complexity

R1
→ no A8
→ no heterogeneity inference from point-estimate discrepancy alone
```

## Candidate generalization

```text
A transition to a more complex intervention,
representation, or experimental branch requires
incremental discriminating justification not already
available from a shallower alternative.
```

## What it would forbid

```text
remaining uncertainty
→ automatic experiment

possible interaction
→ interaction study without prior discrimination

discrepant estimates
→ heterogeneity program without direct evidence

available finer model
→ automatic adoption
```

## Known limit

The historical record does **not** provide a general operational definition of:

```text
incremental discriminating justification
```

nor a scalar or threshold for comparing candidate experiments.

This is exactly one of the gaps that prevented structural action-selection primitives from surviving the abstraction gate.

## Independent falsification requirement

Before testing this candidate, an independent task must define:

```text
candidate actions
relative complexity
which hypotheses each action discriminates
what evidence could change authority
```

Then compare transitions that escalate versus remain at a shallower discriminating action.

A valid falsification design must not define “justified” retrospectively from which experiment happens to succeed.

## Status

```text
OBSERVED PATTERN: YES
POSSIBLE GENERALIZATION: YES
INDEPENDENTLY ESTABLISHED: NO
FALSIFICATION READY: NOT YET
```

The missing operational criterion is part of the scientific problem.

---

# I6 — Termination Legitimacy

## Observed basis

Source class:

```text
P0-DECISION
```

Pilot 0 terminated with residual uncertainty still present.

The terminal record states, in case-specific form:

```text
remaining uncertainty
+
no sufficiently discriminating unresolved question
→ STOP
```

and explicitly separates:

```text
STOP
≠ truth
≠ completeness
≠ certainty
```

## Candidate generalization

```text
Residual uncertainty does not itself authorize continuation.

Stopping can be legitimate when no currently
available transition is sufficiently justified
by the unresolved state.
```

This is a property of a trajectory boundary, not a `STOP()` command.

## What it would forbid

```text
uncertainty remains
→ experiment required

experiment possible
→ experiment authorized

open question
→ perpetual escalation
```

## Known limit

Pilot 0 contains one terminal case and no general operational threshold for:

```text
sufficiently justified
sufficiently discriminating
```

The prior abstraction gate therefore correctly rejected `STOP` as a transferable primitive.

This invariant does not reverse that result.

## Independent falsification requirement

A future test would need a task with:

```text
explicit residual uncertainties
explicit candidate actions
pre-outcome criteria for authority-changing discrimination
known costs / opportunity constraints only if those are part of the hypothesis
```

The test would compare trajectories that continue versus stop when candidate actions fail the prespecified justification criteria.

The invariant would be challenged if continued action systematically yields justified authority gains in states classified prospectively as having no sufficiently justified next transition.

## Status

```text
OBSERVED PATTERN: ONE TERMINAL CASE
POSSIBLE GENERALIZATION: YES
INDEPENDENTLY ESTABLISHED: NO
FALSIFICATION READY: NOT YET
```

---

# I7 — Replication Discipline

## Observed basis

Source classes:

```text
P0-DECISION
P0-EMPIRICAL
```

The R1 contract explicitly states:

```text
different cohort point estimates
↛ heterogeneity
```

and prospectively distinguishes:

```text
Q p >= .05
→ compatible with common effect
↛ invariance

Q p < .05
→ would earn transport / heterogeneity follow-up
```

The realized R1 result found no excess cohort variation and therefore did not earn R2.

## Candidate generalization

```text
A discrepancy may motivate replication or discrimination,
but must not acquire heterogeneity / transport-failure authority
without an appropriate direct test.
```

This is not the primitive `REPLICATE`.

It constrains what authority a discrepancy may acquire.

## What it would forbid

```text
different estimates
→ heterogeneity claim

one replication failure
→ mechanism-change claim

compatible common-effect diagnostic
→ invariance claim
```

## Known limit

The appropriate discrimination procedure is domain-dependent. R1 supplies one statistical instantiation, not a universal transport test.

## Independent falsification requirement

Use independent repeated-estimate tasks with known data-generating regimes:

```text
common effect + sampling variation
true heterogeneous effects
transport failure with identifiable moderator
```

Compare transition rules that infer heterogeneity directly from discrepancy versus rules requiring prespecified discrimination.

A useful test must measure both false heterogeneity authority and failure to detect real heterogeneity.

## Status

```text
OBSERVED PATTERN: YES
POSSIBLE GENERALIZATION: YES
INDEPENDENTLY ESTABLISHED: NO
```

---

# Cross-invariant non-implications

Even if one or more candidates survive independent tests:

```text
invariant compliance
↛ correct world model

invariant compliance
↛ optimal experiment

invariant compliance
↛ unique next action

invariant compliance
↛ controller exists

transition audit
↛ transition generator
```

The candidate invariants are primarily **negative constraints** on epistemic transformation.

They may be necessary, unnecessary, redundant, incomplete, or representation-dependent.

Those possibilities remain open.

---

# Candidate transition-audit object

If any invariant later survives independent falsification, the smallest automation target would not initially be an autonomous scientist.

It would be a transition auditor:

```text
current epistemic state
        +
new evidence
        +
proposed transition
        ↓
check candidate invariant(s)
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

A transition may satisfy one invariant and violate another.

No scalar transition-quality score is proposed here.

No conjunction of the seven candidates is assumed sufficient.

---

# What would count as a real new empirical object?

A transition invariant becomes a genuine empirical object only if all of the following can be supplied without using Pilot 0 as the answer key:

```text
1. state representation
2. evidence representation
3. candidate transition
4. invariant-specific expected relation
5. violation criterion
6. held-out cases where historical Pilot-0 actions are irrelevant
7. outcomes capable of falsifying or revising the invariant
```

This is the anti-imitation requirement.

A test fails as independent falsification if success is defined as:

```text
"choose what the Pilot-0 researcher chose"
```

The relevant question is instead:

```text
"did the transition respect the independently specified
constraint on justified epistemic change?"
```

---

# Current readiness map

This is not a validation ranking. It records only whether an independent falsification object appears specifiable without first solving the missing controller problem.

| Candidate | Historical / process observation | Independent test object currently specifiable? | Established? |
| --- | --- | --- | --- |
| I1 Evidence-bounded authority | Yes | Yes, with explicit authority dimensions | **NO** |
| I2 Scope locality | Yes | Yes, with explicit scope linkage | **NO** |
| I3 Revision conservation | Yes, process-heavy | Partial; failure-locus representation required | **NO** |
| I4 Alternative preservation | Post-P0 method | Yes, with delayed discriminating evidence | **NO** |
| I5 Escalation justification | Yes | No; discriminating-justification criterion missing | **NO** |
| I6 Termination legitimacy | One terminal case | No; stopping threshold missing | **NO** |
| I7 Replication discipline | Yes | Yes, domain-specific discrimination required | **NO** |

This table does not promote the `Yes` rows. It identifies where the next scientific work could, in principle, become independent of Pilot 0.

---

# Terminal boundary of this artifact

```text
CORRECTION TRANSITION INVARIANTS
→ seven candidate hypotheses
→ zero established principles
→ zero controller primitives
→ zero controller specification
```

The immediate authority state is:

```text
Pilot-0 primitive extraction
→ TERMINATED WITH ∅

transition-quality framing
→ NEW HYPOTHESIS SPACE

I1–I7
→ CANDIDATE INVARIANTS ONLY

independent falsification
→ required before promotion

controller specification
→ NOT AUTHORIZED

Pilot 1
→ NOT EARNED
```

The next question is not:

> Which invariant should become the controller?

It is:

> **Does any candidate invariant survive an independent test in which transition quality can be scored without reproducing the Pilot-0 human decision sequence?**

If the answer cannot be made operational without importing the missing controller, this line stops.
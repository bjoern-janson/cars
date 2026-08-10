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
→ ADVERSARIAL CONCEPTUAL REVIEW COMPLETE
→ CURRENT UNIFIED INVARIANT FRAMING: NOT ESTABLISHED
→ NOT A CONTROLLER SPECIFICATION
→ NOT PRIMITIVE EXTRACTION
→ NOT PILOT 1
→ NOT A NEW EXPERIMENT
```

The failed C2 primitive-promotion branch is intentionally not inherited. No controller primitive is assumed here.

This artifact now asks a stricter question than the first draft:

> **Is there a non-redundant, falsifiable notion of correction-transition quality that cannot be reduced to ordinary belief-revision postulates, domain-specific inference rules, or generic constraint shielding?**

The candidate object remains provisional:

```text
AUTHORIZED TRANSFORMATION
```

meaning only:

```text
an epistemic-state change whose authority,
scope, and structural consequences are licensed
by the evidence available at that transition
```

The review below shows that this description is **not yet sufficient** to define a new scientific object.

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

and:

```text
cleanly auditable transition
↛ novel transition theory
```

No candidate proceeds to experiment merely because it can be written as a predicate on a state transition.

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

The proposed audit evaluates `T_t`; it does not choose `S_{t+1}`.

```text
transition audit      ≠ transition generation
transition legitimacy ≠ action optimality
valid transition      ↛ unique next action
```

That separation is useful, but the literature review below shows that **the separation itself is not novel**.

---

# External conceptual adversaries

The purpose of this section is not literature coverage. It identifies the strongest existing concepts that could make the proposed object redundant.

## A1 — AGM and iterated belief revision

Alchourrón, Gärdenfors, and Makinson formalized rational constraints on belief contraction and revision; Darwiche and Pearl later imposed additional constraints on **iterated epistemic-state revision** and preservation across sequences of observations.

Relevant primary works:

```text
Alchourrón, Gärdenfors & Makinson (1985)
On the Logic of Theory Change
DOI: 10.2307/2274239

Darwiche & Pearl (1997)
On the Logic of Iterated Belief Revision
DOI: 10.1016/S0004-3702(96)00038-0
```

Pressure:

```text
"evaluate rational properties of epistemic-state change"
→ already established research territory
```

Therefore the proposed novelty cannot be merely:

```text
correction quality = postulates on transitions
```

## A2 — Relevance-sensitive / preservation-oriented belief change

Belief-revision work also contains explicit attempts to preserve relevance, conditional structure, and unaffected information under revision.

Relevant primary examples include Parikh-style language splitting / relevance-sensitive revision and later conditional-preservation work.

Pressure:

```text
I2 scope locality
I3 revision conservation
I4 alternative / information preservation
```

cannot be treated as novel merely because they are expressed in Pilot-0 vocabulary.

## A3 — Causal transportability

Pearl and Bareinboim formalize when causal conclusions are licensed to transfer across domains and when stronger transport claims are not identified.

Relevant primary work:

```text
Pearl & Bareinboim (2011)
Transportability of Causal and Statistical Relations: A Formal Approach
DOI: 10.1609/aaai.v25i1.7861
```

Pressure:

```text
I7 replication / transport discipline
```

may be a domain-specific instance of established causal-identification / transportability machinery rather than a general correction invariant.

## A4 — Safety shielding / constrained action filtering

Alshiekh et al. separate an action-generating learner from a synthesized shield that checks or modifies proposed actions to preserve an externally supplied temporal-logic safety specification.

Relevant primary work:

```text
Alshiekh et al. (2018)
Safe Reinforcement Learning via Shielding
DOI: 10.1609/aaai.v32i1.11797
```

Pressure:

```text
policy
→ proposed transition/action
→ external constraint audit
→ allow / block
```

is already an established architectural pattern.

Therefore:

```text
transition audit ≠ transition generation
```

is an important separation, but not by itself a new scientific object.

---

# Residual novelty candidate — not established

After the adversarial comparison, the remaining possible distinction is narrower:

```text
not merely belief revision
not merely causal transportability
not merely policy shielding

but:

evidence
→ changes in epistemic authority / scope / provenance / admissibility
→ evaluated for both local legitimacy and future corrigibility
```

Possible residual object:

> **An evidence-responsive transition relation over structured epistemic states that tracks what claims and actions are licensed, what remains reopenable, and whether current changes preserve future capacity for justified correction.**

This is only a conceptual remainder after subtraction of adjacent fields.

```text
residual distinction
↛ novelty established
↛ formal object established
```

---

# Candidate set from the first draft

The first draft proposed:

```text
I1  EVIDENCE-BOUNDED AUTHORITY
I2  SCOPE LOCALITY
I3  REVISION CONSERVATION
I4  ALTERNATIVE PRESERVATION
I5  ESCALATION JUSTIFICATION
I6  TERMINATION LEGITIMACY
I7  REPLICATION DISCIPLINE
```

All remain:

```text
NOT ESTABLISHED
```

The adversarial review additionally rejects the assumption that all seven belong to one mathematical family.

---

# Taxonomy pressure

The current candidates fracture into at least three functional classes.

## T1 — Transition-integrity constraints

```text
I1 Evidence-bounded authority
I2 Scope locality
I3 Revision conservation
I4 Alternative preservation
```

These are plausibly predicates on a realized epistemic-state transition.

## T2 — Selection / occurrence conditions

```text
I5 Escalation justification
I6 Termination legitimacy
```

These concern whether a transition or action should occur at all. They require candidate-action comparison or a stopping/continuation criterion and therefore cannot currently be treated as ordinary transition invariants.

## T3 — Domain-specific procedural discipline

```text
I7 Replication discipline
```

This currently depends on statistical / causal machinery specific to discrepancy, heterogeneity, and transport questions.

Thus:

```text
I1–I7
↛ one established invariant family
```

The taxonomy is allowed to fracture rather than being forced into a controller-shaped ontology.

---

# Counterexample construction

The object is now pressure-tested with four adversarial constructions. These are conceptual tests, not empirical results.

## Type A — Policy disagreement with equal local validity

Construct an epistemic state with two unresolved hypotheses and evidence that does not discriminate between them.

Two systems choose different policies:

```text
SYSTEM A
→ schedule an independent replication

SYSTEM B
→ preserve unresolved status
→ defer action pending a different measurement opportunity
```

Suppose both transitions:

```text
preserve the same authority ceiling
preserve unrelated scope
keep both hypotheses distinguishable
make no heterogeneity / transport claim
```

Then:

```text
A ≠ B
A locally valid
B locally valid
```

### Result

```text
POLICY DISAGREEMENT TEST
→ PASSES THE INTENDED SEPARATION
```

A transition-quality framework need not identify a unique historical action.

This is evidence that transition auditing **can be conceptually separated from policy imitation**.

It is not evidence that the proposed invariants are sufficient.

---

## Type B — Every local transition valid, lineage globally bad

Construct a finite research budget and a sequence of locally permissible transitions.

At each step the system:

```text
preserves authority ceilings
preserves scope
keeps alternatives explicit
avoids unsupported heterogeneity claims
```

but repeatedly spends its finite experimental budget on redundant, low-information actions.

After enough steps:

```text
all local transitions passed
+
remaining budget exhausted
+
future discriminating experiment no longer possible
```

The trajectory has damaged future correction capacity without necessarily violating I1/I2/I4/I7 at any single step.

An equivalent construction can discard provenance or challenge-channel resolution incrementally while preserving current belief labels.

### Result

```text
single-transition validity
≠ lineage-level correction quality
```

This is a direct insufficiency result for any purely local transition account of correction quality.

A valid future object may therefore need to represent **option value, provenance, reopenability, or future correction capacity** at trajectory scale.

No new invariant is added here.

---

## Type C — Invalid transition with correct outcome

Suppose evidence does not discriminate `H1` from `H2`, but a system collapses to `H1` anyway:

```text
E
↛ authority to prefer H1

system transition:
{H1, H2 live}
→ H1 accepted, H2 discarded
```

Assume `H1` later happens to be objectively true.

Then:

```text
outcome correctness = GOOD
transition justification = BAD
```

### Result

```text
transition quality
≠ outcome correctness
```

This separation survives the counterexample and remains scientifically useful.

---

## Type D — Identity transition under new evidence

Consider:

```text
S_t → S_t
```

with no epistemic-state change.

### D1 — weak / non-discriminating evidence

If `E_t` does not alter the authority of any represented claim, preserving the state may be legitimate.

```text
identity transition
≠ automatic failure to correct
```

### D2 — decisive disconfirming evidence

Now let `E_t` directly defeat a currently authorized claim.

The current I1 formulation says only:

```text
authority may increase only along dimensions
identified by available evidence
```

It does **not** require authority to decrease when evidence defeats an existing claim.

Therefore an unchanged state can satisfy the one-sided safety reading of I1 while refusing to respond to decisive contradiction.

### Result

```text
constraint preservation alone
≠ evidence responsiveness
```

and:

```text
safety-only transition invariants
can permit epistemic inertia
```

This is the strongest defect exposed by the counterexample review.

The current candidate set contains restrictions on unauthorized change but does not yet provide a general criterion requiring **earned change when evidence demands it**.

No additional invariant is introduced here; the defect remains open.

---

# Counterexample summary

| Test | Result | Consequence |
| --- | --- | --- |
| Type A: different policies, both locally valid | **SURVIVES** | Transition audit can be policy-independent. |
| Type B: locally valid, globally bad lineage | **FAILS SUFFICIENCY** | Local validity is not lineage quality. |
| Type C: invalid transition, correct outcome | **SURVIVES** | Transition quality is distinct from outcome correctness. |
| Type D: identity under decisive contradiction | **FAILS RESPONSIVENESS** | Current constraints permit epistemic inertia. |

The mixed result matters:

```text
transition-quality framing
→ not collapsed into policy imitation
→ not collapsed into outcome correctness

but

current local invariant set
→ insufficient for correction quality
```

---

# Readiness map after conceptual pressure test

The earlier question—"can an isolated test object be written?"—was too weak to authorize experimentation on the broader correction-quality claim.

| Candidate | Existing-field pressure | Current class | Independent local test conceivable? | Tests correction quality as claimed? |
| --- | --- | --- | --- | --- |
| I1 Evidence-bounded authority | justification / belief-change overlap | transition integrity | YES | **NO — one-sided responsiveness defect** |
| I2 Scope locality | relevance-sensitive belief revision overlap | transition integrity | YES | **NO — novelty not isolated** |
| I3 Revision conservation | AGM/minimal-change overlap | transition integrity | PARTIAL | **NO** |
| I4 Alternative preservation | iterated/preservation overlap | transition integrity | YES | **NO — lineage benefit unestablished** |
| I5 Escalation justification | action-selection object | selection condition | NO | **NO** |
| I6 Termination legitimacy | stopping/action-selection object | selection condition | NO | **NO** |
| I7 Replication discipline | transportability/statistical overlap | domain-specific | YES | **NO — specialized instance** |

Therefore:

```text
INDEPENDENT INVARIANT EXPERIMENT
→ NOT YET AUTHORIZED
```

Not because every candidate is false, but because no current candidate test cleanly discriminates the proposed **correction-quality object** from established neighboring objects while also surviving the responsiveness / lineage counterexamples.

---

# What remains scientifically live

The review leaves three separable questions.

```text
Q1 POLICY INDEPENDENCE
Can multiple different policies produce transitions
that are equally legitimate under independently specified constraints?

STATUS: conceptually coherent
```

```text
Q2 EVIDENCE RESPONSIVENESS
Can transition quality require both:
(a) blocking unauthorized change, and
(b) requiring authority reduction / revision when evidence defeats it?

STATUS: missing formal object
```

```text
Q3 LINEAGE CORRIGIBILITY
Can a sequence of individually legitimate transitions
still reduce future capacity for justified correction?

STATUS: counterexample says YES in principle;
measurement object missing
```

The scientifically interesting remainder may therefore lie at the intersection:

```text
local epistemic legitimacy
+
evidence responsiveness
+
future corrigibility / reopenability
```

rather than in a generic transition invariant alone.

---

# No automation target yet

The first draft proposed:

```text
state + evidence + proposed transition
→ transition audit
→ authorized / violation
```

The shielding comparison shows that this architecture alone is generic.

The Type B and Type D counterexamples additionally show that a local allow/block audit can miss:

```text
future correction-capacity loss
epistemic inertia under decisive evidence
```

Therefore:

```text
TRANSITION AUDITOR
→ NOT YET AN EARNED AUTOMATION OBJECT
```

No transition generator is proposed.
No next-action selector is proposed.
No scalar transition-quality score is proposed.
No controller specification is authorized.

---

# Revised falsification gate

A future candidate object becomes experimentally eligible only if a test can specify, without using Pilot 0 as the answer key:

```text
1. epistemic state
2. new evidence
3. one or more proposed transitions
4. invariant / relation under test
5. both prohibited and required epistemic changes, where applicable
6. lineage-relevant state if future corrigibility is claimed
7. violation criterion
8. held-out cases
9. strongest neighboring theory that predicts the same result
10. a discriminating outcome that could show the new object adds nothing
```

The final two requirements are new consequences of the conceptual-adversary review.

Invalid novelty test:

```text
"can we audit a transition?"
```

because belief revision and shielding already support closely related structures.

Potentially discriminating test:

```text
"does an authority/responsiveness/lineage constraint
predict correction-quality distinctions that are not already
captured by ordinary belief revision, domain-specific causal
identification, or externally supplied safety shielding?"
```

---

# Terminal boundary

```text
CORRECTION TRANSITION INVARIANTS
→ 7 inherited candidate hypotheses
→ taxonomy fractured
→ 0 established invariants
→ 0 experiments authorized
→ 0 controller primitives
→ 0 controller specification
```

Current authority state:

```text
Pilot-0 primitive extraction
→ TERMINATED WITH ∅

broad transition-audit framing
→ NOT NOVEL BY ITSELF

policy-independence distinction
→ SURVIVES CONCEPTUALLY

outcome-independence distinction
→ SURVIVES CONCEPTUALLY

single-transition sufficiency
→ FAILS COUNTEREXAMPLE

evidence responsiveness
→ MISSING FROM CURRENT SAFETY-ONLY FORMULATION

lineage-level corrigibility
→ LIVE QUESTION, NOT FORMALIZED

controller specification
→ NOT AUTHORIZED

Pilot 1
→ NOT EARNED
```

The next question is no longer "which invariant should we test first?"

It is:

> **Can we define a correction-quality relation that is simultaneously evidence-responsive, lineage-aware, and empirically distinguishable from existing belief-revision and constraint-shielding machinery?**

If not, the transition-quality line should stop rather than accumulate more named invariants.
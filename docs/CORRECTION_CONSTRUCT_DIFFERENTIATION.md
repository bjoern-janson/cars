# Correction Construct Differentiation

## Status

```text
PILOT 0
→ CLOSED / READ-ONLY

PILOT-0 primitive extraction
→ COMPLETE
→ ZERO TRANSFERABLE CONTROLLER PRIMITIVES EARNED

PR #6 transition-quality pressure test
→ broad transition-audit framing not novel by itself
→ current local invariant set insufficient

THIS DOCUMENT
→ CONSTRUCT NULL-SPACE AUDIT
→ ADVERSARIAL ELIMINATION ONLY
→ NOT A NEW THEORY
→ NOT AN EXPERIMENT
→ NOT A CONTROLLER SPECIFICATION
→ NOT PILOT 1
```

This artifact asks one question:

> **After subtracting the strongest existing constructs, is there any observable correction-quality remainder that is nontrivial, nonredundant, and independently measurable?**

The default answer is `NO` until a discriminating pair is constructed.

---

# Killer differentiation test

For candidate construct `C` and strongest existing comparator `M`, distinctness requires a pair of systems or trajectories `A, B` such that:

```text
M(A) = M(B)

but

C(A) ≠ C(B)
```

and the difference must be measurable without using Pilot 0 as the answer key.

A valid pair must also avoid trivial representational leakage:

```text
"A has extra metadata that B lacks"
↛ new construct
```

unless that metadata supports an independently measurable difference in future correction behavior after relevant existing measures are matched.

If no such pair can be specified:

```text
C
→ NOT DISTINCTLY ESTABLISHED
```

If a pair can be written only by redefining the existing state representation so that the comparator is artificially blind:

```text
C
→ NOT DISTINCTLY ESTABLISHED
```

---

# Strongest conceptual adversaries

The null-space audit uses established neighboring objects as elimination targets.

## A1 — Iterated belief revision

Darwiche & Pearl (1997) explicitly study repeated epistemic-state revision and preservation constraints across sequences of observations.

Pressure:

```text
evidence responsiveness
state revision
conditional-belief preservation
iterated correction
```

cannot by themselves establish a new construct.

## A2 — Relevance-sensitive belief change

Relevance-sensitive belief-revision work formalizes preservation of belief compartments not implicated by new information.

Pressure:

```text
scope locality
minimal unrelated change
relevance preservation
```

cannot be claimed as a new correction object merely by changing vocabulary.

## A3 — Online learning / calibration / adaptivity

Online-learning frameworks already measure sequential response to new data through regret, calibration, and stronger forms of adaptation to changing environments.

Pressure:

```text
responds to evidence over time
adapts after error
maintains predictive quality under change
```

are insufficient novelty claims.

## A4 — Safety shielding / constrained filtering

Shielding separates an action-generating policy from an external mechanism that blocks actions violating an explicit specification.

Pressure:

```text
proposed transition
→ constraint audit
→ allow / block
```

is generic policy infrastructure unless a specifically epistemic distinction is independently demonstrated.

## A5 — Safe reachability / recoverability

Safe-exploration work explicitly reasons about safely reachable regions and avoiding states from which no safe way out remains.

Pressure:

```text
preserve future options
avoid dead ends
remain recoverable
```

cannot establish a new construct without an epistemically specific residual.

## A6 — Corrigibility / interruptibility / human control

AI-safety work formalizes properties such as accepting shutdown, avoiding incentives to resist intervention, and remaining responsive to authorized human control.

Pressure:

```text
can still be corrected later
accepts external correction
preserves intervention channel
```

cannot be treated as unoccupied conceptual territory.

## A7 — Causal identification / transportability

Causal transportability formalizes when evidence licenses conclusions across populations or settings and when stronger claims are not identified.

Pressure:

```text
authority across scope
transport claims
replication / heterogeneity discipline
```

may be domain-specific identification machinery rather than a general correction-quality construct.

---

# Ingredient-by-ingredient elimination

## C1 — Evidence responsiveness

Candidate intuition:

```text
when new evidence changes the warranted authority of a claim,
the epistemic state should change accordingly
```

Strongest existing captures:

```text
iterated belief revision
Bayesian / ranking-style updating
online adaptation
calibration / regret-based response
```

What may remain:

```text
not merely changing belief,
but changing represented claim/action authority
while retaining provenance and reopenability
```

### Pair test

Attempt:

```text
A and B
→ same initial beliefs
→ receive same defeating evidence
→ end with same posterior belief set

A
→ records reduced authority and preserved provenance

B
→ reaches same posterior beliefs
→ erases provenance / marks result as globally authoritative
```

Problem:

A sufficiently rich epistemic-state revision framework can represent provenance or meta-beliefs. Merely placing extra fields in `S_t` does not prove a distinct construct.

```text
PAIR STATUS: NOT YET DISCRIMINATING
C1 STATUS: NOT DISTINCTLY ESTABLISHED
```

Necessary future distinction:

```text
matched ordinary revision quality
+
matched predictive / calibration behavior
+
measurably different future correction behavior
```

---

## C2 — Future corrigibility / justified transformability

Candidate intuition:

```text
a trajectory preserves the future ability
to reach evidence-warranted epistemic states
```

Strongest existing captures:

```text
safe reachability / recoverability
corrigibility / interruptibility
online adaptivity
resource-aware sequential decision making
```

Potential residual:

```text
future reachability of WARRANTED epistemic states
conditional on later evidence,
including preservation of provenance,
challenge channels, and discriminating access
```

### Pair test

Desired construction:

```text
A and B matched on:
current task capability
current predictive accuracy
belief-revision quality
calibration
online adaptation / regret
resource use
constraint compliance
ordinary safe recoverability

but later:
new discriminating evidence arrives

A → can reach the warranted revised epistemic state
B → cannot, because prior trajectory destroyed
     an epistemically necessary correction channel
```

Candidate destruction mechanisms:

```text
loss of provenance needed to reinterpret evidence
collapse of distinguishable hypotheses
loss of measurement / challenge access
irreversible authority commitment
resource consumption that removes the only discriminating test
```

Critical problem:

If these variables are simply incorporated into a sufficiently rich reachability or resource state, the distinction may collapse back into ordinary state-space reachability.

Therefore the burden is stronger:

> Show that an epistemically structured reachability quantity predicts future warranted correction beyond ordinary capability, resources, adaptivity, and recoverability metrics.

```text
PAIR STATUS: CONCEIVABLE BUT NOT YET CLEAN
C2 STATUS: LIVE RESIDUAL / NOT ESTABLISHED
```

This is currently the strongest surviving null-space candidate.

---

## C3 — Local legitimacy

Candidate intuition:

```text
a local epistemic change must be licensed by current evidence
```

Strongest existing captures:

```text
belief-revision rationality postulates
Bayesian / ranking update rules
authority constraints supplied by causal identification
formal shielding when constraints are explicit
```

No independent residual is presently identified.

```text
PAIR STATUS: NO CLEAN PAIR
C3 STATUS: ELIMINATED AS DISTINCT CONSTRUCT FOR NOW
```

---

## C4 — Scope preservation

Candidate intuition:

```text
evidence about X should not silently alter unrelated Y
```

Strongest existing capture:

```text
relevance-sensitive belief revision
language splitting / relevance postulates
modular causal-identification scope constraints
```

No pair is currently available that matches relevance-sensitive revision while differing only on the proposed correction construct.

```text
PAIR STATUS: NO CLEAN PAIR
C4 STATUS: ELIMINATED AS DISTINCT CONSTRUCT FOR NOW
```

---

## C5 — Alternative preservation / reopenability

Candidate intuition:

```text
undiscriminated alternatives remain representationally recoverable
```

Strongest existing captures:

```text
iterated epistemic-state revision
partial / ranked belief representations
belief-base approaches preserving explicit distinctions
```

Possible residual:

```text
future ability to recover an alternative
when later evidence makes it warranted
```

But that is already part of the C2 future-corrigibility question rather than a clearly independent construct.

```text
PAIR STATUS: COLLAPSES INTO C2 OR EXISTING BELIEF-STATE RICHNESS
C5 STATUS: NOT INDEPENDENTLY EARNED
```

---

## C6 — Termination legitimacy

Candidate intuition:

```text
residual uncertainty does not itself authorize continuation
```

This concerns action occurrence / stopping rather than the quality of an already realized epistemic transition.

It remains entangled with:

```text
sequential decision theory
value of information
resource constraints
optimal stopping
candidate-action comparison
```

Pilot 0 did not supply an operational stopping threshold, and the transition-quality work did not repair that gap.

```text
PAIR STATUS: NOT AVAILABLE
C6 STATUS: OUTSIDE CURRENT CONSTRUCT / NOT EARNED
```

---

# Null-space result

| Ingredient | Strongest existing capture | Clean matched pair available? | Current status |
| --- | --- | --- | --- |
| Evidence responsiveness | iterated revision / online adaptation | **NO** | NOT DISTINCT |
| Future corrigibility / justified transformability | reachability + corrigibility + adaptivity | **NOT YET** | LIVE RESIDUAL |
| Local legitimacy | revision postulates / identification / shielding | **NO** | ELIMINATED FOR NOW |
| Scope preservation | relevance-sensitive revision | **NO** | ELIMINATED FOR NOW |
| Alternative preservation | rich epistemic-state revision | **NO** | COLLAPSES INTO C2 / EXISTING STATE |
| Termination | sequential selection / stopping | **NO** | OUTSIDE CURRENT OBJECT |

Current contraction:

```text
six proposed ingredients
→ five fail to establish independent construct status
→ one residual remains live

LIVE RESIDUAL:
future justified epistemic transformability
```

This is not a promotion.

```text
live residual
↛ construct established
↛ novelty established
↛ operationalization earned
```

---

# The representation-expansion trap

A particularly important failure mode is:

```text
existing framework uses state X
our framework uses state (X, provenance, authority, reopenability)
therefore ours is new
```

That inference is invalid.

A richer state representation is scientifically useful only if the added structure supports an observable distinction not already recoverable by extending the existing framework in the ordinary way.

Thus:

```text
new state variable
≠ new construct
```

and:

```text
new vocabulary
≠ incremental predictive content
```

---

# Candidate existence test — not yet executable

If a measurable quantity `JT` (justified transformability) is eventually proposed, its existence test should ask whether it adds information about later correction after existing explanations are controlled.

Conceptually:

```text
F = future warranted-correction performance
M = existing measures
    (capability, revision quality, calibration,
     online adaptivity/regret, resources,
     constraint compliance, recoverability)

Distinct construct requires something like:

I(JT ; F | M) > 0
```

or an equivalent held-out incremental-prediction criterion.

This is not a frozen estimator, threshold, or experiment.

Critical null:

```text
I(JT ; F | M) = 0
→ candidate construct adds no detectable information
  beyond existing machinery
```

The construct should be abandoned or reduced if that null cannot be challenged by a prospective design.

---

# What would count as a successful pair?

A successful differentiation pair must satisfy all of:

```text
1. same current task capability
2. same current evidence / starting epistemic state
3. same ordinary belief-revision quality
4. same calibration / predictive quality
5. same ordinary adaptivity measure
6. same resource budget at the comparison point
7. same explicit constraint compliance
8. same ordinary safe/recoverable-state status
9. different future response to a later authority-changing correction
10. difference traceable to a prospectively specified epistemic-path property
```

Then:

```text
A reaches warranted state after future correction
B cannot
```

without scoring either system by resemblance to Pilot 0.

No such clean pair is established in this document.

---

# Terminal authority state

```text
CONTROLLER PRIMITIVES
→ 0

GENERIC TRANSITION-INVARIANT NOVELTY
→ NOT ESTABLISHED

CORRECTION-QUALITY INGREDIENTS EXAMINED
→ 6

DISTINCT INGREDIENTS ESTABLISHED
→ 0

LIVE NULL-SPACE RESIDUALS
→ 1
→ future justified epistemic transformability

OPERATIONALIZATION
→ NOT AUTHORIZED

INDEPENDENT FALSIFICATION
→ NOT AUTHORIZED

EMPIRICAL STUDY
→ NOT EARNED

PILOT 1
→ NOT EARNED
```

The next legitimate question is singular:

> **Can we construct a clean matched pair that is equivalent under the strongest existing measures but differs prospectively in future warranted-correction reachability?**

If not:

```text
CORRECTION-QUALITY CONSTRUCT
→ REDUNDANT / NOT ESTABLISHED
→ STOP THIS LINE
```

If yes, only then is formalization of the residual construct earned.

---

# Primary literature adversaries

```text
Darwiche & Pearl (1997)
On the Logic of Iterated Belief Revision
Artificial Intelligence 89(1–2):1–29
DOI: 10.1016/S0004-3702(96)00038-0

Peppas, Williams, Chopra & Foo (2015)
Relevance in Belief Revision
Artificial Intelligence 229:126–138
DOI: 10.1016/j.artint.2015.08.007

Pearl & Bareinboim (2011)
Transportability of Causal and Statistical Relations: A Formal Approach
AAAI 25(1):247–254
DOI: 10.1609/aaai.v25i1.7861

Alshiekh et al. (2018)
Safe Reinforcement Learning via Shielding
AAAI 32(1)
DOI: 10.1609/aaai.v32i1.11797

Turchetta, Berkenkamp & Krause (2016)
Safe Exploration in Finite Markov Decision Processes with Gaussian Processes
NeurIPS 29

Rakhlin, Sridharan & Tewari (2011)
Online Learning: Beyond Regret
COLT / PMLR 19:559–594

Orseau & Armstrong (2016)
Safely Interruptible Agents
UAI 2016:557–566

Hadfield-Menell, Dragan, Abbeel & Russell (2017)
The Off-Switch Game
IJCAI 2017:220–227
DOI: 10.24963/ijcai.2017/32

Carey & Everitt (2023)
Human Control: Definitions and Algorithms
UAI / PMLR 216:271–281
```

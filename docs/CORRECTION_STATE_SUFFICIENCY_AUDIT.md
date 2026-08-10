# Correction-State Sufficiency Audit

## Status

```text
PILOT 0
→ CLOSED / READ-ONLY

PILOT-0 controller / primitive extraction
→ COMPLETE
→ ZERO TRANSFERABLE CONTROLLER PRIMITIVES EARNED

transition-quality framing
→ PRESSURE-TESTED
→ NOT NOVEL BY ITSELF

correction-quality construct differentiation
→ FAILED TO ESTABLISH DISTINCT CONSTRUCT

history-only residual
→ KILLED BY CURRENT-STATE / INTERFACE SUFFICIENCY ADVERSARY

THIS DOCUMENT
→ ADVERSARIAL STATE-SUFFICIENCY SUBTRACTION AUDIT
→ NOT A NEW THEORY
→ NOT A FORMALIZATION
→ NOT AN EXPERIMENT
→ NOT PILOT 1
```

This artifact asks one question only:

> **Does “correction-relevant state/interface sufficiency” identify a scientific object not already captured by established notions of statistical, predictive, control, or state-representation sufficiency?**

Default answer:

```text
NO
```

until a matched counterexample survives the strongest existing machinery.

---

# Pass / stop rule

For a proposed correction-specific sufficiency property `C` and an established sufficiency concept `M`:

```text
M(R1) = M(R2)

but

C(R1) ≠ C(R2)
```

must be constructible without:

```text
changing the downstream task family after the fact
hiding a correction-relevant variable from M
using Pilot 0 as the answer key
adding semantics that are not independently measurable
```

Then:

```text
clean matched counterexample
→ correction-specific gap remains live
```

Otherwise:

```text
existing concept already explains the distinction
→ adopt existing terminology
→ do not create a new sufficiency construct
```

---

# Candidate object under attack

The live question inherited from the residual casebook is:

```text
history h
→ representation R(h)
→ future evidence E+
→ future warranted-correction outcome F
```

A representation is informally “correction-relevant sufficient” if histories mapped to the same represented state do not differ in future warranted-correction behavior under the same future conditions:

```text
R(h_a) = R(h_b)
→
P(F | h_a, E+) = P(F | h_b, E+)
```

Equivalently, a violation is:

```text
R(h_a) = R(h_b)

but

P(F | h_a, E+) ≠ P(F | h_b, E+)
```

The audit asks whether this is anything more than ordinary task-relative state sufficiency applied to a future-correction target.

---

# Strongest existing adversaries

## A1 — Statistical sufficiency / comparison of experiments

Blackwell's comparison-of-experiments program treats one information structure as at least as informative as another when it can do at least as well across the relevant decision problems.

Primary reference:

```text
David Blackwell (1953)
Equivalent Comparisons of Experiments
Annals of Mathematical Statistics 24(2):265–272
DOI: 10.1214/aoms/1177729032
```

Pressure:

```text
representation sufficient for ordinary decisions
but insufficient for correction decisions
```

may simply mean:

```text
the original decision-problem family was too narrow
```

If correction is added to the relevant decision family, the information structures need no new sufficiency concept to become distinguishable.

---

## A2 — Belief state / information state in partially observed control

Partially observed stochastic control already compresses observation history into a state sufficient for downstream control.

Primary reference:

```text
Richard D. Smallwood & Edward J. Sondik (1973)
The Optimal Control of Partially Observable Markov Processes over a Finite Horizon
Operations Research 21(5):1071–1088
DOI: 10.1287/opre.21.5.1071
```

Related information-state work explicitly treats a sufficient statistic as the recursively propagated state on which optimal control can be based.

Pressure:

```text
history matters for future correction
```

is not enough.

The relevant question is whether the chosen information state is sufficient for the enlarged control / prediction problem in which warranted correction is part of the downstream objective or observable target.

---

## A3 — Predictive State Representations

Predictive State Representations represent state using predictions of future action-conditional observable tests.

Primary reference:

```text
Michael L. Littman, Richard S. Sutton & Satinder Singh (2001)
Predictive Representations of State
Advances in Neural Information Processing Systems 14
```

Pressure:

```text
state = information needed to predict relevant future tests
```

already directly attacks the proposed correction-state idea.

If future correction behavior can be expressed as a family of observable tests, then a representation that fails to predict those tests is simply not sufficient for that predictive target family.

---

## A4 — Causal states / minimal predictive representations

Computational mechanics groups histories by equality of their conditional distributions over futures and constructs a minimal predictive representation.

Primary reference:

```text
Cosma R. Shalizi & James P. Crutchfield (2001)
Computational Mechanics: Pattern and Prediction, Structure and Simplicity
Journal of Statistical Physics 104:817–879
```

Pressure:

```text
R(h_a) = R(h_b)
while
P(Future | h_a) ≠ P(Future | h_b)
```

is already the signature of a representation that merges predictively nonequivalent histories.

A correction-specific target must therefore explain why ordinary predictive equivalence over an appropriately specified future is insufficient.

---

## A5 — Observability

Classical control theory asks whether internal state distinctions can be recovered from available input/output behavior.

Primary reference:

```text
R. E. Kalman (1960)
Contributions to the Theory of Optimal Control
Boletín de la Sociedad Matemática Mexicana 5:102–119
```

Pressure:

```text
correction-relevant latent distinction exists
but interface cannot recover it
```

may be an observability / state-reconstruction problem rather than a new sufficiency concept.

Observability is not identical to predictive sufficiency, but it occupies the same negative space when the claimed novelty is that the interface hides a causally relevant state distinction.

---

## A6 — Bisimulation / state abstraction for control

State-abstraction theory asks when distinct concrete states may be merged without changing downstream control-relevant behavior.

Primary reference:

```text
Robert Givan, Thomas Dean & Matthew Greig (2003)
Equivalence Notions and Model Minimization in Markov Decision Processes
Artificial Intelligence 147(1–2):163–223
DOI: 10.1016/S0004-3702(02)00376-4
```

Pressure:

```text
R1 and R2 have equal ordinary control performance
but differ on future correction
```

may mean only that the abstraction preserved the originally specified reward / transition equivalence but not the enlarged correction-relevant task family.

That is task-relative abstraction insufficiency, not automatically a new construct.

---

## A7 — Action-sufficient state representation

Modern representation-learning work explicitly targets minimal state variables sufficient for downstream decision making under partial observability.

Primary reference:

```text
Biwei Huang et al. (2022)
Action-Sufficient State Representation Learning for Control with Structural Constraints
Proceedings of ICML 2022, PMLR 162:9260–9279
```

Pressure:

```text
which variables must the representation retain
for the downstream decision problem?
```

is already an explicit representation-learning question.

The correction program therefore needs more than a correction-specific list of variables; it needs a distinction not reducible to changing the downstream sufficiency target.

---

## A8 — Approximate information states

Approximate information-state work asks whether a compressed history representation approximately preserves the quantities needed for planning / control and provides performance-loss guarantees.

Primary reference:

```text
Jayakumar Subramanian, Amit Sinha, Raihan Seraj & Aditya Mahajan (2020)
Approximate Information State for Approximate Planning and Reinforcement Learning in Partially Observed Systems
arXiv:2010.08843
```

Pressure:

A correction-relevant interface need not be exactly sufficient to fit existing machinery; approximation error can itself be treated as task-relative information-state error.

Therefore:

```text
correction prediction degrades under compression
```

is not by itself a distinct construct either.

---

# Killer matched-counterexample attempt

## Desired pair

Try to construct two representations:

```text
R1
R2
```

such that they are matched on:

```text
ordinary future prediction
ordinary control value
ordinary adaptability
ordinary calibration
resource visibility
current task performance
```

but differ on:

```text
future evidence-warranted correction
```

Desired conclusion:

```text
existing state sufficiency says R1 = R2

but

correction-state sufficiency says R1 ≠ R2
```

## Adversarial response

The phrase “ordinary” is doing all the work.

Suppose the original downstream target family is:

```text
Q_ordinary
```

and the future correction target is:

```text
Q_corr
```

If:

```text
R1 and R2 are equally sufficient for Q_ordinary
```

but:

```text
R1 predicts / supports Q_corr
R2 does not
```

then existing theory can simply evaluate sufficiency for:

```text
Q* = Q_ordinary ∪ Q_corr
```

Under `Q*`:

```text
R1 and R2 are no longer equally sufficient
```

No new sufficiency relation is required.

## Decision

```text
MATCHED COUNTEREXAMPLE
→ FAILS AS DISTINCT-CONSTRUCT EVIDENCE

FAILURE LOCUS
→ TASK / TARGET FAMILY INCOMPLETENESS
```

This is the central negative result of the audit.

---

# Authority / provenance rescue attempt

A possible rescue is:

```text
ordinary predictive state
≠ epistemic authority state
```

because correction may depend on:

```text
provenance
defeasibility
claim scope
reopenability
challenge-channel access
measurement provenance
```

But there are only two possibilities.

## Case 1 — these variables have observable downstream consequences

Then include them in the state / target / loss / constraint family.

Existing information-state, predictive-state, abstraction, or decision-theoretic machinery can in principle distinguish representations that preserve versus erase them.

```text
important variable
≠ new notion of sufficiency
```

## Case 2 — they have no independently measurable downstream consequence

Then they do not yet define an empirical sufficiency target.

```text
semantic label without observable consequence
↛ empirical construct
```

## Decision

```text
AUTHORITY / PROVENANCE RESCUE
→ DOES NOT YET ESTABLISH NEW SUFFICIENCY CONCEPT
```

---

# Prediction versus control rescue attempt

Another possible rescue is:

```text
prediction sufficiency
≠ correction-control sufficiency
```

This distinction is real but already familiar.

A representation can be sufficient for one task family and insufficient for another.

The relevant existing response is to specify the downstream task / control family for which sufficiency is required.

Therefore:

```text
prediction-sufficient but correction-insufficient
```

establishes:

```text
task-relative insufficiency
```

not automatically:

```text
new sufficiency ontology
```

---

# Observability versus sufficiency

Observability asks whether relevant hidden state can be recovered from available observations.

Sufficiency asks whether the representation retains enough information for the specified downstream prediction / decision problem.

These are not identical.

But the proposed correction-specific problem currently decomposes naturally into existing questions:

```text
1. Is a correction-relevant latent distinction observable / inferable?

2. Does the chosen representation preserve the information
   needed for correction-relevant future prediction or control?

3. Can that representation be recursively updated / learned?

4. What loss follows from approximate compression?
```

No additional correction-specific sufficiency principle has yet been isolated.

---

# Current subtraction table

| Proposed idea | Strongest existing capture | Residual gap established? |
| --- | --- | --- |
| History compression sufficient for future correction | information state / PSR / causal state | **NO** |
| Hidden correction-relevant distinction | observability / state estimation | **NO** |
| Merge states without changing correction behavior | bisimulation / task-relative abstraction | **NO** |
| Minimal representation for correction decisions | action-sufficient representation | **NO** |
| Approximate correction-state representation | approximate information state | **NO** |
| More informative representation for correction decisions | Blackwell comparison / decision sufficiency | **NO** |
| Provenance / authority variables | richer state / target representation if measurable | **NO NEW SUFFICIENCY CONCEPT** |

Result:

```text
CORRECTION-STATE SUFFICIENCY
AS A DISTINCT SUFFICIENCY CONSTRUCT
→ NOT EARNED
```

---

# What remains live

The audit does **not** show that correction-relevant representation is unimportant.

It relocates the open problem.

The unresolved question is no longer:

```text
what is a new kind of sufficiency?
```

It is:

```text
which future variables / decisions / interventions
must be included in the target family
for correction to be identifiable and controllable?
```

That is closer to:

```text
TARGET / INTERFACE DISCOVERY
```

than to a new state-sufficiency theory.

The difficult step is identifying the missing correction-relevant distinctions before the failure has already revealed them.

This is exactly where ordinary sufficiency machinery becomes conditional on a specification that the system may not yet possess.

Important boundary:

```text
existing sufficiency machinery
can test whether R is sufficient for a specified target family

but

that does not automatically tell us
which target variables / distinctions should have been specified
```

This is a live research problem.

It is not yet a new formal construct.

---

# New matched-counterexample requirement

A future attempt to establish a genuinely correction-specific residual must survive a stronger test than the original R1/R2 pair.

It must construct two representations such that:

```text
1. the relevant future target / decision family is fixed prospectively
2. both representations satisfy the strongest existing
   statistical / predictive / control sufficiency criteria
   for that same fixed family
3. ordinary observability / information-state augmentation
   cannot distinguish them
4. yet future evidence-warranted correction differs
5. the difference is independently measurable
6. the difference cannot be removed by adding an omitted
   task variable, state variable, loss, constraint, or future test
```

If no such pair exists:

```text
NO DISTINCT CORRECTION-SUFFICIENCY CONSTRUCT
```

---

# Terminology decision

Until such a pair exists, use existing terminology where applicable:

```text
information state
predictive state
sufficient statistic
state abstraction / bisimulation
observability
approximate information state
```

`correction-relevant state` may remain a descriptive project phrase for:

```text
state variables retained because the downstream task family
includes future evidence-warranted correction
```

but:

```text
correction-relevant state
↛ new state-sufficiency theory
```

---

# Terminal authority state

```text
Pilot-0 controller primitives
→ 0

transition-quality construct
→ NOT ESTABLISHED

correction-quality construct
→ NOT ESTABLISHED

lineage-only residual
→ NOT EARNED

correction-state sufficiency
AS A DISTINCT SUFFICIENCY CONCEPT
→ NOT EARNED

existing state / information sufficiency machinery
→ STRONG CURRENT EXPLANATION

surviving open problem
→ correction-relevant target / interface discovery
→ NOT YET FORMALIZED
```

Therefore:

```text
new sufficiency formalization
→ NOT AUTHORIZED

correction-state experiment
→ NOT AUTHORIZED

controller specification
→ NOT AUTHORIZED

Pilot 1
→ NOT EARNED
```

Reopen only if a prospective matched counterexample survives established task-relative statistical, predictive, observability, information-state, and control-abstraction sufficiency machinery without relying on an omitted correction target.
# Correction Target Discovery — Differentiation Audit

## Status

```text
PILOT 0
→ CLOSED / READ-ONLY

controller / primitive extraction
→ COMPLETE
→ ZERO TRANSFERABLE CONTROLLER PRIMITIVES EARNED

transition-quality construct
→ NOT ESTABLISHED

correction-quality construct
→ NOT ESTABLISHED

lineage-only residual
→ NOT EARNED

correction-state sufficiency
→ REDUCED TO EXISTING TASK-RELATIVE SUFFICIENCY

THIS DOCUMENT
→ ADVERSARIAL TARGET-DISCOVERY SUBTRACTION AUDIT
→ NOT A NEW THEORY
→ NOT A FORMALIZATION
→ NOT AN EXPERIMENT
→ NOT A CONTROLLER SPECIFICATION
→ NOT PILOT 1
```

This artifact asks one question only:

> **Does discovering correction-relevant targets or distinctions before failure reveals them constitute a scientifically distinct problem, rather than an instance of existing feature discovery, causal discovery, active learning, experimental design, goal generation, or open-ended task discovery?**

Default answer:

```text
NO
```

until a matched construction forces otherwise.

---

# Hard elimination rule

A proposed correction-specific discovery operation is eliminated if its apparent advantage can be explained by any of the following:

```text
1. ordinary feature / causal-feature discovery
2. ordinary state / representation discovery
3. expanded downstream target or task family
4. ordinary active learning / experimental design
5. active causal discovery / intervention selection
6. ordinary task selection / curriculum learning
7. self-generated goal / open-ended challenge discovery
8. hypothesis generation under an existing evaluation criterion
9. a different utility, reward, constraint, or loss
10. a richer goal / hypothesis representation
```

Only a residual requiring a genuinely different, independently measurable operation remains live.

```text
existing machinery already captures it
→ ELIMINATE

expanded target / objective captures it
→ ELIMINATE

richer representation captures it
→ ELIMINATE

algorithm A merely performs worse than algorithm B
→ ALGORITHM COMPARISON, NOT NEW CONSTRUCT
```

---

# Existing machinery used as adversaries

## A1 — Feature selection and causal feature selection

Feature-selection methods identify variables relevant to an already specified prediction or decision target.

Local causal / Markov-blanket methods explicitly recover variables causally or predictively relevant to a target variable of interest.

Primary reference:

```text
Aliferis et al. (2010)
Local Causal and Markov Blanket Induction for Causal Discovery
and Feature Selection for Classification, Part I
JMLR 11:171–234
```

Pressure:

```text
target Y fixed
→ discover variables relevant to Y
```

is occupied territory.

This does not solve target formation itself, but it removes any novelty claim based only on discovering omitted variables once the downstream target is known.

---

## A2 — Active learning and experimental design

Sequential design methods choose measurements or interventions to reduce uncertainty about a specified quantity of interest or improve a specified objective.

Primary reference:

```text
Mutny, Janik & Krause (2023)
Active Exploration via Experiment Design in Markov Chains
AISTATS / PMLR 206
```

Pressure:

```text
target / quantity of interest fixed
→ choose informative experiment
```

is occupied territory.

Likewise, active causal-discovery methods select interventions to identify a causal graph or orient unresolved causal structure.

```text
Hauser & Bühlmann (2012)
Two Optimal Strategies for Active Learning of Causal Models
from Interventional Data
```

```text
Scherrer et al. (2021)
Learning Neural Causal Models with Active Interventions
```

Therefore:

```text
choose observations that reveal a missing distinction
↛ new correction-specific problem
```

when the distinction or learning objective is already specified.

---

## A3 — Active task selection / curriculum selection

Meta-learning already contains active selection of informative tasks from candidate task families.

Primary reference:

```text
Chen, Zhang & Low (2022)
Near-Optimal Task Selection for Meta-Learning with Mutual Information
AISTATS / PMLR 151
```

Pressure:

```text
candidate tasks exist
→ choose which task to learn next
```

is not a correction-specific operation.

---

## A4 — Self-generated goals and autotelic learning

The stronger adversary is that some systems do not require a single externally fixed target at all.

Intrinsically motivated goal-exploration processes can self-generate, self-select, self-order, and self-experiment on learning goals.

Primary reference:

```text
Forestier et al. (2022)
Intrinsically Motivated Goal Exploration Processes
with Automatic Curriculum Learning
JMLR 23(152)
```

Other examples:

```text
Florensa et al. (2018)
Automatic Goal Generation for Reinforcement Learning Agents
ICML / PMLR 80

Colas et al. (2019)
CURIOUS: Intrinsically Motivated Modular Multi-Goal RL
ICML / PMLR 97
```

Thus:

```text
no externally fixed target
→ generate and prioritize goals
```

is already an established research pattern.

---

## A5 — Goal-space / representation reshaping

A possible rescue is:

```text
existing methods select within a fixed goal language;
correction requires inventing a new distinction / goal representation
```

But open-ended/autotelic work also pressures this claim.

Primary example:

```text
Colas et al. (2023)
Augmenting Autotelic Agents with Large Language Models
CoLLAs / PMLR 232
```

This work explicitly motivates agents that can reshape goal representations, form abstractions, and generate new high-level goals rather than relying only on a fixed hand-coded goal list.

Open-ended systems also generate their own evolving learning challenges:

```text
Wang et al. (2020)
Enhanced POET: Open-ended Reinforcement Learning through
Unbounded Invention of Learning Challenges and their Solutions
ICML / PMLR 119
```

Therefore:

```text
invent / reshape goals or challenges
↛ correction-specific novelty by itself
```

---

## A6 — “Active target discovery” terminology warning

A 2025 NeurIPS paper is titled:

```text
Active Target Discovery under Uninformative Priors:
The Power of Permanent and Transient Memory
```

Its “target discovery” problem is strategic sampling to locate target instances / promising regions under a discovery objective.

It does **not** by itself establish that the system discovers which scientific quantity or epistemic distinction deserves to become the objective.

Therefore this title must not be used as evidence that target-*specification* discovery is already solved.

```text
same phrase
≠ same object
```

---

# Candidate correction-specific residual under attack

The remaining intuition is:

```text
before failure reveals the omission,
discover distinctions that should become targets
because preserving / testing them matters for future warranted correction
```

Call this only the **candidate residual**. No new construct name is introduced.

The burden is to show that “correction relevance” changes the discovery problem itself rather than merely supplying another utility or task definition.

---

# Killer A/B construction

Construct two research systems:

```text
A = strongest existing open-ended discovery machinery
B = proposed correction-specific discovery machinery
```

Match them on:

```text
observations
prior information
hypothesis / feature / goal language
ability to generate candidate goals
ability to reshape representation, where allowed
computational budget
experimental budget
future environment
candidate intervention access
existing downstream task family
prospectively specified utilities / constraints / losses
```

Require:

```text
B discovers distinction X
A systematically does not
```

and all of the following:

```text
1. X materially changes future evidence-warranted correction
2. X is independently measurable before the terminal outcome
3. X cannot be represented as another feature / state variable
4. X cannot be represented as another goal / task
5. X cannot be represented as another constraint / loss / utility
6. X cannot be recovered by enlarging A's target family
7. X cannot be recovered by ordinary representation / goal-space expansion
8. B's advantage is not merely a better search heuristic
```

Only then:

```text
CORRECTION-SPECIFIC DISCOVERY RESIDUAL
→ REMAINS LIVE
```

---

# Adversarial cases

## Case 1 — B discovers provenance

```text
B discovers:
"preserve source provenance"
```

Attack:

If provenance has a measurable effect on future correction, it can be represented as:

```text
feature
state variable
constraint
task-relevant future test
```

and can enter an existing target / utility family.

```text
CASE 1
→ ELIMINATED AS DISTINCT DISCOVERY OBJECT
```

---

## Case 2 — B discovers challengeability

```text
B discovers:
"preserve an independent challenge channel"
```

Attack:

If channel availability matters prospectively, it is a state/access variable or downstream constraint.

If its value is unknown, an open-ended discovery method can in principle evaluate candidate goals under a utility that rewards future information or recoverability.

```text
CASE 2
→ NO CORRECTION-SPECIFIC OPERATION ISOLATED
```

---

## Case 3 — B preserves alternative hypotheses

Attack:

```text
retain H1/H2 distinguishability
```

can be represented as a richer hypothesis/state representation or as a preservation objective.

The previous lineage and sufficiency audits already showed that representational richness does not itself create a new scientific construct.

```text
CASE 3
→ ELIMINATED
```

---

## Case 4 — B chooses discriminating experiments

Attack:

Once the unresolved quantity or hypothesis family is specified:

```text
choose experiment maximizing discrimination / information
```

is ordinary active learning / experimental design.

```text
CASE 4
→ ELIMINATED
```

---

## Case 5 — B invents a new target not in A's goal language

This is the strongest apparent rescue.

But if B can expand its goal / hypothesis representation while A cannot, the pair is not matched on discovery capacity.

Compare B instead with open-ended / autotelic systems capable of generating or reshaping goal representations.

Then ask what specifically correction-related operation remains.

```text
CASE 5
→ REPRESENTATION / GOAL-SPACE DIFFERENCE
→ NOT YET CORRECTION-SPECIFIC
```

---

## Case 6 — “correction relevance” supplies the missing selection criterion

Suppose B ranks generated targets by:

```text
expected value for future warranted correction
```

There are two possibilities.

### 6A — criterion prospectively measurable

Then it is an outer-level utility / reward / acquisition criterion.

Existing open-ended goal generation or task-selection machinery can in principle optimize that criterion.

```text
new utility
≠ new discovery ontology
```

### 6B — criterion not prospectively measurable

Then the target cannot yet be independently scored as “correction relevant.”

```text
unmeasurable correction relevance
↛ empirical discovery construct
```

Decision:

```text
CASE 6
→ NO DISTINCT OPERATION ESTABLISHED
```

---

# The central fork

The live intuition now encounters a hard dichotomy:

```text
CORRECTION RELEVANCE IS SPECIFIED / MEASURABLE
        ↓
can enter ordinary utility / task / constraint machinery
        ↓
no new discovery construct earned
```

or:

```text
CORRECTION RELEVANCE IS NOT SPECIFIED / MEASURABLE
        ↓
no independent criterion for successful discovery
        ↓
no empirical construct earned
```

This is the central negative result of the audit.

---

# Current subtraction table

| Proposed operation | Strongest existing capture | Correction-specific residual? |
| --- | --- | --- |
| find relevant variables for known target | feature / causal feature selection | **NO** |
| choose informative observation / experiment | active learning / experimental design | **NO** |
| choose informative intervention for causal structure | active causal discovery | **NO** |
| choose among candidate tasks | active task selection / curriculum | **NO** |
| self-generate goals | autotelic goal exploration | **NO** |
| reshape / generate goal representations | open-ended / LLM-augmented autotelic learning | **NO DISTINCT RESIDUAL YET** |
| generate scientific hypotheses / challenges | hypothesis generation / open-ended discovery | **NO DISTINCT RESIDUAL YET** |
| rank targets by correction value | ordinary outer-level utility if measurable | **NO** |
| discover an unmeasurable correction target | no prospective empirical criterion | **NO** |

Result:

```text
CORRECTION-SPECIFIC TARGET DISCOVERY
AS A DISTINCT SCIENTIFIC PROBLEM
→ NOT EARNED
```

---

# What remains live

The audit does not show that discovering missing distinctions is solved.

It shows that the **correction-specific qualifier has not earned independence**.

The remaining difficult problem is more general:

```text
how can a system generate / expand useful target,
feature, hypothesis, or representation spaces
when the important distinctions are not already encoded?
```

That problem is already shared with:

```text
open-ended learning
autotelic goal generation
representation discovery
causal discovery
scientific hypothesis generation
```

The project currently has no evidence that future correction requires a distinct discovery ontology beyond those families.

Important boundary:

```text
unsolved general problem
≠ correction-specific new construct
```

---

# Reopening condition

Reopen only if a prospective matched case satisfies all of the following:

```text
1. A and B receive the same data / priors / budgets
2. A and B have equally expressive feature / goal / hypothesis languages
3. A and B share the same prospectively measurable objective family
4. A uses the strongest relevant existing discovery machinery
5. B performs an additional identifiable operation
6. that operation discovers X before failure
7. X changes future warranted-correction behavior
8. X cannot be encoded as another ordinary feature, target,
   representation variable, constraint, utility, or experiment objective
9. the effect is independently measurable
10. the distinction survives comparison with open-ended goal /
    representation generation, not merely fixed-target methods
```

If no such construction exists:

```text
NO DISTINCT CORRECTION-TARGET-DISCOVERY OBJECT
```

---

# Terminal authority state

```text
controller primitives
→ 0

transition-quality construct
→ NOT ESTABLISHED

correction-quality construct
→ NOT ESTABLISHED

lineage-only construct
→ NOT EARNED

correction-specific sufficiency
→ NOT EARNED

correction-specific target discovery
→ NOT EARNED

existing discovery / open-ended machinery
→ STRONG CURRENT EXPLANATION

remaining general problem
→ target / hypothesis / representation invention
→ NOT CORRECTION-SPECIFICALLY DIFFERENTIATED
```

Therefore:

```text
new target-discovery formalization
→ NOT AUTHORIZED

new correction-discovery metric
→ NOT AUTHORIZED

experiment
→ NOT AUTHORIZED

controller specification
→ NOT AUTHORIZED

Pilot 1
→ NOT EARNED
```

The current endpoint is not a new object. It is a subtraction result:

> **The project has not established that discovering correction-relevant distinctions is scientifically different from existing open-ended target, feature, hypothesis, representation, and experiment discovery once the same prospective objective family is supplied.**

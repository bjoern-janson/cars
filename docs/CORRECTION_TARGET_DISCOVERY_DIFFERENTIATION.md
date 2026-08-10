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
→ NOT A THEORY
→ NOT A FORMALIZATION
→ NOT AN EXPERIMENT
→ NOT PILOT 1
```

Question:

> **Does discovering correction-relevant distinctions before failure reveals them constitute a scientifically distinct problem, rather than an instance of existing feature, target, goal, hypothesis, representation, or experiment discovery?**

Default:

```text
NO
```

until a matched construction forces otherwise.

---

# Hard elimination rule

Eliminate the correction-specific claim if the apparent advantage reduces to:

```text
known-target feature / causal-feature selection
active learning / experimental design
active causal intervention selection
active task / curriculum selection
self-generated goals
open-ended challenge generation
goal / hypothesis representation expansion
expanded downstream task family
new utility / reward / constraint / loss
better search heuristic
```

Only a genuinely different, independently measurable operation may survive.

```text
existing machinery captures it
→ ELIMINATE

expanded target / objective captures it
→ ELIMINATE

richer representation captures it
→ ELIMINATE

B merely searches better than A
→ ALGORITHM COMPARISON, NOT NEW CONSTRUCT
```

---

# Strongest existing adversaries

## A1 — Feature and causal-feature discovery

Local causal / Markov-blanket methods recover variables relevant to a specified target.

```text
Aliferis et al. (2010)
Local Causal and Markov Blanket Induction ... Part I
JMLR 11:171–234
```

Therefore:

```text
target fixed
→ discover relevant variables
```

is occupied territory.

---

## A2 — Active learning / experimental design

Sequential design chooses measurements or interventions for a specified quantity of interest or learning objective.

```text
Mutny, Janik & Krause (2023)
Active Exploration via Experiment Design in Markov Chains
AISTATS / PMLR 206
```

Active causal discovery likewise chooses interventions to resolve causal structure.

```text
Hauser & Bühlmann (2012)
Two Optimal Strategies for Active Learning of Causal Models

Scherrer et al. (2021)
Learning Neural Causal Models with Active Interventions
```

Thus:

```text
specified unresolved quantity
→ choose discriminating experiment
```

is not correction-specific.

---

## A3 — Active task selection

Meta-learning already contains active selection of informative tasks from candidate task families.

```text
Chen, Zhang & Low (2022)
Near-Optimal Task Selection for Meta-Learning with Mutual Information
AISTATS / PMLR 151
```

So:

```text
candidate tasks exist
→ choose next task
```

is occupied.

---

## A4 — Self-generated goals

Autotelic learning is a stronger adversary because the target need not be externally fixed.

```text
Forestier et al. (2022)
Intrinsically Motivated Goal Exploration Processes
with Automatic Curriculum Learning
JMLR 23(152)
```

Such systems self-generate, self-select, self-order, and self-experiment on goals.

Therefore:

```text
no fixed target
→ generate / prioritize goals
```

is already an established problem form.

---

## A5 — Goal-space / challenge invention

Open-ended work also pressures the rescue:

```text
"the needed distinction was outside the fixed goal language"
```

Examples include:

```text
Colas et al. (2023)
Augmenting Autotelic Agents with Large Language Models
→ generate high-level goals / abstractions

Wang et al. (2020)
Enhanced POET
→ generate evolving learning challenges
```

Thus:

```text
invent / reshape goals or challenges
↛ correction-specific novelty by itself
```

---

## A6 — Terminology warning: “active target discovery”

```text
Sarkar, Ji & Vorobeychik (2025)
Active Target Discovery under Uninformative Priors
```

uses “target discovery” for strategic sampling to locate target instances / regions under an existing discovery objective.

It does **not** by itself solve:

```text
which epistemic quantity or distinction
should become the objective?
```

Therefore:

```text
same phrase
≠ same object
```

---

# Candidate residual under attack

Remaining intuition:

```text
before failure reveals the omission,
discover distinctions that should become targets
because they matter for future warranted correction
```

The burden is to show that **correction relevance changes the discovery operation**, rather than merely supplying another target or utility.

---

# Killer A/B construction

Compare:

```text
A = strongest existing open-ended discovery system
B = proposed correction-specific discovery system
```

Match:

```text
observations
priors
feature / hypothesis / goal expressivity
candidate-generation capacity
representation-expansion capacity
compute budget
experimental budget
intervention access
future environment
prospectively specified objective / constraint / loss family
```

Require:

```text
B discovers X
A systematically does not
```

while:

```text
1. X changes future evidence-warranted correction
2. X is prospectively and independently measurable
3. X is not merely another feature / state variable
4. X is not merely another task / goal / hypothesis
5. X is not merely another constraint / utility / loss
6. X is not recovered by enlarging the target family
7. X is not recovered by ordinary goal / representation expansion
8. B's advantage is not merely a superior search heuristic
```

Only then:

```text
CORRECTION-SPECIFIC DISCOVERY RESIDUAL
→ REMAINS LIVE
```

---

# Adversarial examples

| Proposed discovery | Shallowest existing explanation | Decision |
| --- | --- | --- |
| preserve provenance | state / feature / future-test variable | **ELIMINATE** |
| preserve challenge channel | access variable / constraint / information utility | **ELIMINATE** |
| retain alternatives | richer hypothesis representation / preservation objective | **ELIMINATE** |
| choose discriminating experiment | active learning / experimental design | **ELIMINATE** |
| invent target outside fixed goal language | open-ended goal / representation generation | **NOT CORRECTION-SPECIFIC** |
| rank targets by future correction value | outer-level utility if measurable | **ELIMINATE** |

---

# Central fork

The residual hits a hard dichotomy.

```text
CORRECTION RELEVANCE IS PROSPECTIVELY MEASURABLE
        ↓
can be supplied as utility / task / constraint / acquisition criterion
        ↓
existing open-ended discovery machinery can optimize it in principle
        ↓
NO NEW DISCOVERY CONSTRUCT EARNED
```

or:

```text
CORRECTION RELEVANCE IS NOT PROSPECTIVELY MEASURABLE
        ↓
no independent success criterion for discovery
        ↓
NO EMPIRICAL CONSTRUCT EARNED
```

This is the central negative result.

---

# Decision

```text
CORRECTION-SPECIFIC TARGET DISCOVERY
AS A DISTINCT SCIENTIFIC PROBLEM
→ NOT EARNED
```

This does **not** imply that discovering missing distinctions is solved.

It implies only:

```text
unsolved general discovery problem
≠ correction-specific new construct
```

The remaining general problem is:

```text
how can a system generate / expand useful target,
feature, hypothesis, or representation spaces
when important distinctions are not already encoded?
```

That problem is shared with:

```text
open-ended learning
autotelic goal generation
representation discovery
causal discovery
scientific hypothesis generation
```

The current evidence does not isolate a correction-specific discovery ontology beyond them.

---

# Reopening condition

Reopen only if a prospective matched case shows:

```text
same data / priors / budgets
same expressive goal / feature / hypothesis language
same representation-expansion capacity
same measurable objective family
strong existing open-ended discovery machinery in A

but

B performs an additional identifiable operation
→ discovers X before failure
→ X changes future warranted correction
→ X cannot be encoded as feature, target, representation,
   constraint, utility, loss, or experiment objective
→ effect independently measurable
```

If not:

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

Terminal sentence:

> **The project has not established that discovering correction-relevant distinctions is scientifically different from existing open-ended target, feature, hypothesis, representation, and experiment discovery once the same prospective objective family is supplied.**

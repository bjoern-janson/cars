# ASI-0 Task Suite — Boring First Pass

## Scientific role

The suite exists to test one narrow proposition:

> **Can evidence-conditioned harness edits improve performance on tasks not used to generate those edits?**

It is not an ASI benchmark and is not intended to measure broad intelligence.

## Split architecture

```text
DEVELOPMENT
→ visible tasks + traces
→ candidate generation

SELECTION
→ concealed from generator
→ optional local candidate ranking

HIDDEN CONFIRMATION
→ concealed from generator and candidate ranking
→ promotion evidence
```

Hidden task contents and hidden generation seeds must not be committed to the repository used by the candidate generator.

## Core L1 families

ASI-0 promotion uses three deliberately boring families that appear in development and hidden confirmation through different generated instances and template variants.

### A — `coding_bug`

Small Python repair judgments.

A task supplies:

```text
specification
buggy function
four candidate local repairs
```

The agent returns the correct repair id.

Purpose:

```text
local code reasoning
verification discipline
resistance to plausible distractor patches
```

### B — `novel_coding`

Small unfamiliar implementation judgments.

A task supplies a generated functional specification and four candidate implementations. The agent selects the implementation satisfying the complete specification.

Purpose:

```text
specification tracking
edge-case reasoning
planning before commitment
```

### C — `verification`

Constraint-audit tasks.

A task supplies a requirement set and a candidate artifact with exactly one planted violation. The agent returns the violated requirement id.

Purpose:

```text
explicit verification
constraint retention
error localization
```

These families are intentionally objective and cheaply scored. Their simplicity is a feature: ASI-0 should first demonstrate that the improvement-selection machinery works at all.

## Transfer sentinels

Two additional families are hidden-only in the first pass:

```text
research_synthesis
tool_workflow
```

They are **diagnostic sentinels**, not ASI-0 promotion requirements.

### `research_synthesis`

The task provides synthetic evidence cards with controlled support/conflict structure and asks for the best-supported conclusion.

### `tool_workflow`

The task provides a small symbolic tool environment with preconditions/effects and asks for a valid minimal workflow.

Why hidden-only:

```text
core-family hidden gain
→ L1 held-out self-improvement question

sentinel-family gain
→ preliminary transfer diagnostic only
```

Do not promote L2 transfer claims from ASI-0 sentinel performance.

## Structural holdout

Hidden confirmation must differ from development in more than random numeric values.

The task generator therefore supports template variants. Development uses a frozen public subset of variants; selection/hidden use disjoint variant ids generated from external secret seeds.

Required separation:

```text
instance holdout
+
template-variant holdout
```

The first pass does not require entirely unseen core families for promotion.

## Task interface

Each evaluator record contains:

```json
{
  "id": "...",
  "split": "development",
  "family": "coding_bug",
  "variant": "...",
  "prompt": "...",
  "answer": "B",
  "scoring": {"type": "exact_choice"}
}
```

The **agent-facing bundle omits `answer`**. The evaluator bundle retains it.

## Scoring

Primary task metric:

```text
accuracy ∈ {0,1}
```

Family capability is mean accuracy. Overall capability is the prospectively weighted mean of the core L1 families.

Transfer sentinels are reported separately.

Do not compensate for a core-family regression with sentinel gains unless a later contract explicitly changes the scientific object.

## Task counts

Initial default:

```text
DEVELOPMENT
core families:       24 each
transfer sentinels:   0

SELECTION
core families:       12 each
transfer sentinels:   0

HIDDEN CONFIRMATION
core families:       24 each
transfer sentinels:  12 each
```

The counts are benchmark engineering choices, not claims of statistical adequacy. Before a scientific ASI-0 run, the detectable-effect target and required sample size must be frozen.

## Secret-seed rule

Development generation may use a committed public seed.

Selection and hidden generation require an external secret seed file supplied at execution time. The scientific repository must contain the generator and split specification, but not the secret seed or generated hidden answer bundle.

```text
reproducible generator
+
secret evaluation seed
→ concealed generated tasks
```

The secret seed may be disclosed after the corresponding run is terminal if doing so cannot contaminate a planned fresh evaluation.

## Random-edit control compatibility

STATIC, RANDOM-EDIT, and SELF-EDIT are evaluated on the exact same generated task bundle and resource accounting.

```text
same task ids
same order
same base model
same inference envelope
```

The only intended difference is the harness version.

## First-pass stopping rule

If evidence-conditioned SELF-EDIT does not produce a repeatable hidden core-family gain beyond STATIC and size-matched RANDOM-EDIT, stop ASI-0 at this mutation language/task resolution.

Do not add harder tasks merely because the simple suite failed to show improvement.

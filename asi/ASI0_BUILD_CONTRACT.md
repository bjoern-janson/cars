# ASI-0 — Bounded Self-Improvement Contract

## Scientific question

> **Can a bounded agent use evidence from its own development failures to modify its agent-level machinery and thereby improve held-out capability under fixed base-model and resource constraints?**

ASI-0 tests a substrate for self-improvement. It does not test or establish ASI.

## System versions

Let:

```text
A_k = complete agent system at iteration k
```

with the base model held fixed.

A version may contain:

```text
base model reference       IMMUTABLE
system/policy prompt       MUTABLE
planner                    MUTABLE
memory/retrieval policy    MUTABLE
tool policy                MUTABLE
verification logic         MUTABLE
bounded helper code        MUTABLE
```

The mutable surface must be allowlisted before a run.

## Evidence and update

For iteration `k`:

```text
D_k
= development-task trajectories,
  failures,
  scores,
  resource use,
  verifier output
```

The improvement procedure proposes candidates:

```text
C_k = U(A_k, D_k)
```

Candidate generation may use the same base model, but receives no hidden-evaluation content.

## Primary outcome

Let `C_holdout(A)` be prospectively defined held-out capability under a fixed task distribution and fixed resource budget.

Primary gain:

```text
G_k
= C_holdout(A_{k+1}) - C_holdout(A_k)
```

A promoted update must demonstrate a positive held-out gain exceeding the task-specific frozen promotion threshold while satisfying all resource and regression constraints.

Do not infer self-improvement from development-set gains alone.

## Resource normalization

Record at minimum:

```text
input tokens
output tokens
model calls
wall time
CPU/GPU time where relevant
tool calls
external API cost if any
```

A candidate that improves only by exceeding the allowed inference/resource envelope fails ASI-0 promotion.

The benchmark must distinguish:

```text
capability gain
≠ extra inference budget
≠ extra training data
≠ stronger base model
```

## Control conditions

At minimum retain:

### STATIC

```text
A_k → A_k
```

No candidate modification. Measures ordinary run-to-run variance and any task-distribution drift.

### RANDOM-EDIT

Apply size-matched admissible changes independent of development evidence where a meaningful random-edit control can be constructed.

Purpose:

```text
evidence-conditioned candidate generation
vs
mere parameter/configuration perturbation
```

### SELF-EDIT

Candidate modifications are proposed from the allowed evidence `D_k`.

A later human/expert-edit comparator may be added only under a separate contract.

## Hidden evaluation

Partition task information into:

```text
DEVELOPMENT
visible to improver

SELECTION
used for local candidate ranking where allowed

HIDDEN CONFIRMATION
not visible to improver
```

Hidden tasks must differ from development tasks in more than random seeds whenever the benchmark supports structural holdout.

Examples:

- unseen repositories;
- unseen task generators;
- unseen compositions;
- unseen problem families;
- unseen tool configurations.

The exact holdout structure must be frozen before candidate outcomes are inspected.

## Promotion gate

A candidate can replace `A_k` only if all prospectively frozen conditions pass:

```text
1. held-out capability gain >= minimum gain
2. required task-family coverage passes
3. no protected regression exceeds tolerance
4. resource multiplier <= allowed maximum
5. containment / policy checks pass
6. evaluator integrity checks pass
```

Rejected candidates do not become ancestors of later versions unless the contract explicitly permits their development traces to remain visible.

## Cumulative improvement

ASI-0 is not satisfied by one lucky edit.

The first meaningful positive pattern is:

```text
A_0 → A_1 → A_2 → ... → A_m
```

with repeated held-out promotion under fixed rules.

Report:

```text
G_0, G_1, ...
number of proposed candidates
number promoted
resource cost per promoted gain
regressions
family-specific gains
```

A plateau or reversal is an admissible result.

## What ASI-0 does NOT test

```text
recursive self-improvement
→ NOT YET

model-weight self-modification
→ NOT YET

cross-domain superhumanity
→ NOT YET

open-world autonomy
→ NOT YET

self-deployment
→ PROHIBITED

ASI
→ NOT AN ASI-0 CLAIM
```

## Recursive-improvement gate

Do not use the phrase `recursive self-improvement` merely because the agent performs multiple self-edits.

A later experiment must test whether the **improvement process itself** improves, for example through a prospectively defined decrease in resource cost to achieve a fixed held-out capability gain or an increase in the probability that proposed modifications survive independent confirmation.

Formally, a later candidate target might examine whether:

```text
ImprovementEfficiency_{k+1}
>
ImprovementEfficiency_k
```

across independent task families.

ASI-0 does not establish this.

## Containment

The default execution environment is sandboxed.

Prohibited surfaces:

```text
production deployment
credential stores
external account creation
unbounded network access
self-replication
background persistence outside run artifacts
modification of evaluator or hidden data
modification of promotion thresholds after outcome exposure
```

## Stop rules

ASI-0 stops rather than escalates if:

```text
held-out gains disappear under stronger evaluation
random-edit performs comparably
resource matching removes the gain
hidden structural holdout removes the gain
promotion is driven by evaluator leakage
repeated cycles plateau within frozen sensitivity
```

Failure does not authorize a more complicated self-modification surface.

## Authority ladder

```text
development improvement
→ candidate only

held-out improvement
→ local self-improvement evidence

repeated held-out improvement
→ cumulative self-improvement evidence

cross-family transfer
→ separate authority

improvement-process acceleration
→ separate authority

superhuman breadth
→ separate authority

ASI
→ not earned by ASI-0
```

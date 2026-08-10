# ASI-0 — Evidence-to-Target Assignment Causal Attribution

## Status

```text
ASI
→ ∅

recursive self-improvement
→ ∅

intelligence
→ ∅

self-improvement
→ prior art

evidence-conditioned bounded modification
→ testable

causal evidence-assignment effect
→ UNKNOWN

Δ_align
→ only live ASI-0 scientific number
```

This is a **pre-outcome causal contract** for a narrow attribution experiment. It is not an ASI benchmark, intelligence test, recursive-self-improvement demonstration, or viability assay.

The contract freezes the causal seam before a canonical model/task instance is provisioned.

## Scientific question

> **Can a fixed-base-model agent use development evidence to select bounded modifications that produce greater concealed future capability than evidence-misaligned selection under matched resources?**

The treatment object is the evidence-to-target assignment mechanism:

```text
A = evidence → target assignment mechanism
```

The primary estimand is interventional:

```text
Δ_align
=
E[Y_concealed | do(A = aligned)]
-
E[Y_concealed | do(A = misaligned)]
```

Do not reinterpret this as a conditional association.

## Causal chain under test

ASI-0 tests only:

```text
development evidence
        ↓
relevance-preserving assignment
        ↓
modification selection
        ↓
bounded agent modification
        ↓
concealed future capability
```

It does not directly test:

```text
I_t ∝ Δ_E[V_{t+h}]
```

and it does not establish any higher-level construct.

## Primary intervention

For target `i` with development evidence `E_i`:

```text
ALIGNED
E_i → target i
```

The matched control uses a prospectively seeded within-stratum derangement `π`:

```text
MISALIGNED
E_{π(i)} → target i
π(i) ≠ i
```

The manipulation is **not** evidence versus no evidence. It is whether the same class of evidence is correctly assigned to the modification decision it is informative about.

## Why misalignment must be hard

The misaligned arm must preserve generic information quality while destroying target relevance.

Bad control:

```text
aligned evidence
vs
nonsense / empty / obviously irrelevant text
```

Frozen control principle:

```text
preserve evidence quantity and structure
break evidence-target relevance
```

Where feasible, misalignment strata should match:

```text
task family
evidence type
trace-length bucket
failure/difficulty bucket
candidate count
resource budget
```

A stratum with fewer than two eligible targets cannot support a derangement and is not eligible for the primary contrast.

## Fixed base agent

Every experimental branch starts from the identical frozen base-agent snapshot.

```text
branch start
→ same base model/revision
→ same immutable weights
→ same tool permissions
→ same base policy scaffold
```

No selected modification carries into another target or arm.

Therefore:

```text
ASI-0
↛ recursive self-improvement
```

The candidate-selection agent may choose a modification for its own future policy surface, but the experiment resets to base for every branch.

## Frozen mutation surface

The first implementation uses one bounded textual policy-patch slot.

```text
candidate pool
→ choose exactly one patch
→ apply to one mutable policy slot
→ protected-regression gate
→ concealed evaluation
```

Frozen exclusions:

```text
no weight updates
no architecture change
no tool-permission expansion
no recursive carryover
no new memory subsystem
no autonomy expansion
```

The patch byte/token envelope must be frozen before the scientific run.

Changing the mutation surface after seeing `Δ_align` creates a new experiment.

## Candidate-pool matching

The strongest feasible design freezes each target-specific candidate pool **before assignment** and reuses the exact same pool in the aligned and misaligned arms.

```text
same target
same candidate IDs
same candidate texts
same candidate count
same candidate-generation machinery
same candidate-generation evidence access

ONLY CHANGE
assigned evidence used for candidate selection
```

Candidate generation is therefore not the treatment.

It may use development evidence provided that the resulting pool is frozen once and supplied identically to both primary arms.

This deliberately gives the misaligned arm access to the same candidate diversity. The primary question is whether correct evidence assignment adds incremental leverage over that shared pool.

## Candidate selection

For aligned and misaligned branches, the same frozen base model and selection configuration receive:

```text
target context
+
assigned development evidence
+
identical target-specific candidate pool
```

and must return exactly one candidate ID.

The selection prompt, model identifier, revision, generation parameters, parser, retry rule, and resource budget must be identical across primary arms.

## Secondary controls

Secondary controls remain useful but are not substitutes for the primary attribution test.

### STATIC

```text
same frozen base agent
no applied patch
same evaluation accounting
```

This helps bound improvement attributable merely to repeated execution/evaluation.

### RANDOM-EDIT

```text
same frozen candidate pool
one candidate sampled uniformly
selection independent of evidence
```

This helps bound arbitrary mutation.

Keep explicit:

```text
SELF vs RANDOM
→ useful control
→ insufficient attribution test
```

The primary scientific contrast remains:

```text
E-ALIGNED
vs
E-MISALIGNED
```

## Protected-regression gate

Every selected patch passes through the same frozen protected-regression gate before concealed confirmation.

```text
selected patch
        ↓
protected regressions
        │
   pass ├→ apply patch
        │
   fail └→ explicit no-op / base agent
        ↓
concealed confirmation
```

The regression suite must not contain concealed confirmation items or provide feedback from those items.

Gate pass/fail is a downstream mediator of the assignment intervention and must be reported by arm.

Do not silently replace failed patches with hand-selected alternatives.

## Concealed confirmation

The concealed evaluator must be blind to:

```text
arm label
assigned evidence identity
development trace content
candidate-selection rationale
```

The candidate generator and selector must not receive concealed test content or outcome feedback.

Where possible, use deterministic or objective scoring.

## Structural holdout

Concealed tests must be structurally held out from development evidence under a rule frozen before the scientific run.

The holdout should preserve enough relation to make the development evidence potentially useful while preventing direct answer or surface-template transfer.

Keep explicit:

```text
surface novelty
≠ structural holdout
```

The canonical task family must define its holdout rule prospectively.

## Resource matching

For the primary aligned/misaligned pair, match or record:

```text
base model and revision
selection configuration
number of evidence traces
trace type / matched length stratum
candidate pool
candidate count
candidate-generation cost already sunk equally
selection opportunities
modification count
application slot
protected-regression suite
evaluator
concealed suite
resource budget
```

The only intended intervention is:

```text
evidence → candidate-selection mapping
```

## Experimental unit

Primary unit:

```text
target × replicate branch pair
```

Each pair contains both aligned and misaligned branches constructed from the same frozen target/candidate/base/evaluator state.

Targets, not branch rows, are the primary clustering unit for uncertainty.

## Primary outcome

For each arm, define:

```text
G_arm
=
Y_concealed(modified-or-gated agent)
-
Y_concealed(frozen base agent)
```

Then:

```text
Δ_align
=
E[G_aligned - G_misaligned]
```

Because the base agent, target, candidate pool, evaluator, concealed suite, and budget are paired, this is also the paired concealed-score difference when the base score is identical.

Retain the raw base and post-modification scores rather than storing only the difference.

## Randomization / permutation

Misaligned evidence is generated by a prospectively seeded derangement within matched strata.

The runner must reject:

```text
π(i) = i
```

for every misaligned branch.

The permutation must be generated before concealed outcomes are observed.

Do not hand-select especially irrelevant failures for the control.

## Inference

Primary report:

```text
mean G_aligned
mean G_misaligned
Δ_align
95% target-cluster bootstrap interval
target count
replicate count
protected-regression pass rate by arm
```

The paired target-level difference is primary.

Secondary STATIC and RANDOM-EDIT summaries may be reported but do not replace `Δ_align`.

Do not select an alternative endpoint because `Δ_align` is small or negative.

## Replication

A positive first run earns an independent replication of the **same causal question**, not a larger claim.

Replication requires:

```text
fresh target/evidence manifest
fresh concealed holdout
fresh assignment seed
same mutation surface
same estimator
same claim boundary
```

Changing the mutation surface, autonomy, candidate generator, or target family to rescue the sign is not replication.

## Maximum positive interpretation

A positive replicated result authorizes, at most:

> **Correct evidence-to-target assignment causally improves bounded modification selection and downstream concealed performance under the tested conditions.**

It does not establish:

```text
intelligence
viability
recursive self-improvement
ASI
new ontology
new intelligence variable
architecture-level superiority
```

## Null interpretation

If:

```text
E-aligned ≈ E-misaligned
```

then the authorized interpretation is local:

> **Correct semantic assignment of development evidence adds no detectable value under the tested mutation surface, task family, resource envelope, and measurement resolution.**

A null does not authorize:

```text
new Z
larger mutation surface as rescue
more autonomy as rescue
"the effect must emerge at scale"
```

If the effect disappears, ASI-0 closes at exactly that boundary unless a genuinely new independently motivated question is introduced.

## Subtraction discipline

```text
SELF improves
        ↓
could be search / mutation / compute / evaluator feedback
        ↓
subtract those

E-aligned improves
        ↓
could be information quantity / candidate diversity
        ↓
match those

E-aligned > E-misaligned
        ↓
correct evidence-target relation has incremental leverage
        ↓
STOP
```

## Scientific-instance gate

The repository config intentionally contains placeholders for fields that have not yet been scientifically frozen, including the canonical base model, revision, candidate count, evaluator, and concealed suite.

The runner **refuses scientific preparation while any `MUST_FREEZE_BEFORE_SCIENTIFIC_RUN` placeholder remains**.

This prevents the synthetic smoke or generic harness from being mistaken for a completed preregistration.

## Runner

```bash
# plumbing only
python scripts/run_asi0_assignment_experiment.py \
  experiments/ASI0_EVIDENCE_ASSIGNMENT_CONFIG.json \
  --smoke \
  --json-out results/asi0_assignment_smoke.json
```

Once a canonical instance config and target manifest are frozen:

```bash
python scripts/run_asi0_assignment_experiment.py \
  experiments/ASI0_EVIDENCE_ASSIGNMENT_CONFIG.json \
  --prepare-manifest data/asi0_targets.jsonl \
  --assignments-out results/asi0_assignments.jsonl
```

After the external fixed-base-model executor and concealed evaluator populate result rows:

```bash
python scripts/run_asi0_assignment_experiment.py \
  experiments/ASI0_EVIDENCE_ASSIGNMENT_CONFIG.json \
  --analyze-results results/asi0_executed_results.jsonl \
  --json-out results/asi0_analysis.json
```

The harness intentionally does not call a model API. Model execution and concealed evaluation remain explicit external provenance steps.

## Current authority

```text
CAUSAL DESIGN SKELETON
→ FROZEN

IMPLEMENTATION
→ PRESENT

SYNTHETIC SMOKE
→ PASS

CANONICAL MODEL/TASK INSTANCE
→ NOT YET FROZEN

SCIENTIFIC RUN
→ NOT EXECUTED

Δ_align
→ UNKNOWN

SCIENTIFIC INTERPRETATION
→ ∅
```

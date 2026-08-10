# ASI-0 Boolean input-domain repair

## Status

**FROZEN PRE-OUTCOME BOOLEAN REPAIR**

This document reopens exactly one layer of the canonical ASI-0 instance: the finite Boolean input domain. No scientific outcome has been observed. Canonical execution attempt 1 remains `Y = ∅` because the original `boolean_pair` generator could not realize the frozen requirement of 3 distinct development inputs plus 3 disjoint concealed inputs.

The repair was prospectively specified, validated independently, cross-checked against the implementation, and only then frozen. Validation record:

- `results/ASI0_BOOLEAN_TRIPLE_REPAIR_VALIDATION.json`
- GitHub Actions run `31393480741`
- validated implementation commit `583f28f0f262c25c1f9441696f8cd1b864c2dc32`

## Failure localized

Original Boolean domain:

```text
boolean_pair: (p,q) ∈ {false,true}²
|D| = 4
```

Frozen per-target sampling requirement:

```text
n_dev = 3
n_concealed = 3
all six prompts distinct
```

Therefore:

```text
|D_boolean_pair| = 4 < 6 = n_dev + n_concealed
```

The original canonical Boolean instance is constructively impossible. This is not a stochastic failure and does not provide evidence about C or A.

## Minimal frozen repair

Replace only:

```text
boolean_pair → boolean_triple
```

New domain:

```text
boolean_triple: (p,q,r) ∈ {false,true}³
|D| = 8
```

This restores room for 3 diagnostic development inputs and 3 disjoint concealed inputs while leaving 2 domain points unused.

No nuisance tag or ignored identifier is introduced.

## Frozen candidate ontology

Retain the four original Boolean operation names and extend them to three inputs by their standard n-ary/parity semantics:

1. `and`
   - output `true` iff `p`, `q`, and `r` are all true.
2. `or`
   - output `true` iff at least one of `p`, `q`, or `r` is true.
3. `xor`
   - output `true` iff an odd number of `p`, `q`, and `r` are true.
4. `xnor`
   - output `true` iff an even number of `p`, `q`, and `r` are true.

Thus `xor`/`xnor` preserve the parity interpretation of the original pair rules rather than introducing a new Boolean construct.

Candidate textual policies are frozen as:

```text
boolean_triple:and
For TASK inputs with booleans p, q, and r, return true iff p AND q AND r are all true. Return only true or false.

boolean_triple:or
For TASK inputs with booleans p, q, and r, return true iff at least one of p, q, or r is true. Return only true or false.

boolean_triple:xor
For TASK inputs with booleans p, q, and r, return true iff an odd number of p, q, and r are true. Return only true or false.

boolean_triple:xnor
For TASK inputs with booleans p, q, and r, return true iff an even number of p, q, and r are true. Return only true or false.
```

## Acceptance tests — PASSED

### A. Cardinality

```text
|D_boolean_triple| = 8 >= 6
```

For every Boolean target in both primary and replication frozen-seed realizations:

```text
len(dev) = 3
len(concealed) = 3
|dev ∪ concealed| = 6
|dev ∩ concealed| = 0
```

**PASS.**

### B. Development diagnosticity

For each generated 3-input development set, the four candidate operations induce four distinct output signatures.

**PASS for all 8 frozen-seed Boolean targets.**

### C. Exhaustive existence check

Across the complete 8-point Boolean-triple domain:

```text
C(8,3) = 56 possible three-input development subsets
36 / 56 uniquely identify all four candidate rules
```

**PASS.**

### D. Frozen-seed realization

Using the already frozen primary and replication task seeds and unchanged per-family/per-rule seed derivation, all eight Boolean targets terminate and satisfy cardinality + diagnosticity.

**PASS.**

### E. Non-change assertions

Validation cross-checked that the following remain unchanged:

```text
Qwen/Qwen2.5-0.5B-Instruct @ 7ae5576
3 development examples per target
3 concealed examples per target
4 targets per family
16 targets per phase
primary and replication seeds
evidence-assignment mechanism
protected regressions
C and A estimands
one-sided target-cluster bootstrap parameters
L_C > 0 AND L_A > 0 green rule
conditional replication rule
```

**PASS.**

## Frozen implementation

Canonical Boolean repair wrapper:

```text
scripts/run_asi0_canonical_qwen_boolean_triple.py
```

The original runner and hardened entry wrapper are retained for provenance. The repair wrapper mutates only the Boolean family/input-domain implementation before delegating to the unchanged canonical pipeline.

## Authority boundary

This validation authorizes only:

```text
boolean_pair → boolean_triple
```

It does not authorize changing model, example counts, estimands, inferential thresholds, mutation surface, candidate-generation mechanism, assignment, or replication rule.

Canonical execution attempt 1 remains:

```text
Y = ∅
```

No canonical attempt #2 has been launched by this repair/freeze process.

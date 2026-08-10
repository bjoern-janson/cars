# ASI-0 Boolean input-domain repair

## Status

**PROSPECTIVE SCIENTIFIC REPAIR — NOT YET FROZEN**

This document reopens exactly one layer of the canonical ASI-0 instance: the finite Boolean input domain. No scientific outcome has been observed. Canonical execution attempt 1 remains `Y = ∅` because the original `boolean_pair` generator could not realize the frozen requirement of 3 distinct development inputs plus 3 disjoint concealed inputs.

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

## Minimal repair

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

## Frozen candidate ontology proposed

Retain the four original Boolean operation names and extend them to three inputs by their standard n-ary semantics:

1. `and`
   - output `true` iff `p`, `q`, and `r` are all true.
2. `or`
   - output `true` iff at least one of `p`, `q`, or `r` is true.
3. `xor`
   - output `true` iff an odd number of `p`, `q`, and `r` are true.
4. `xnor`
   - output `true` iff an even number of `p`, `q`, and `r` are true.

Thus `xor`/`xnor` preserve the parity interpretation of the original pair rules rather than introducing a new Boolean construct.

Candidate textual policies:

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

## Prospective acceptance tests

The repair may be frozen only if all tests pass before any canonical model outcome is generated.

### A. Cardinality

```text
|D_boolean_triple| = 8 >= 6
```

For every Boolean target in both primary and replication manifests:

```text
len(dev) = 3
len(concealed) = 3
|dev ∪ concealed| = 6
|dev ∩ concealed| = 0
```

### B. Development diagnosticity

For each generated 3-input development set, the four candidate operations must induce four distinct output signatures:

```text
signature(and) != signature(or)
signature(and) != signature(xor)
...
all 4 signatures unique
```

The deterministic generator may prospectively resample development inputs until this condition holds, exactly as in the pre-existing diagnosticity rule.

### C. Exhaustive existence check

Across the complete 8-point Boolean-triple domain, enumerate all `C(8,3)=56` three-input development subsets. At least one must uniquely identify all four candidates. The validation record should report the exact number of identifying subsets.

### D. Frozen-seed realization

Using the already frozen primary and replication task seeds and the unchanged per-family/per-rule seed derivation, all eight Boolean targets (4 primary + 4 replication) must terminate and satisfy A and B.

### E. Non-change assertions

The validation must verify that the following remain unchanged:

```text
Qwen/Qwen2.5-0.5B-Instruct @ 7ae5576
3 development examples per target
3 concealed examples per target
4 targets per family
16 targets per phase
same evidence-assignment mechanism
same protected regressions
same C and A estimands
same one-sided bootstrap gate
same replication rule
```

## Authority boundary

Passing these tests authorizes only this repair:

```text
boolean_pair → boolean_triple
```

It does not authorize changing model, example counts, estimands, inferential thresholds, mutation surface, candidate-generation mechanism, or replication rule.

After validation passes, this document and the canonical config/runner implementation may be marked **FROZEN PRE-OUTCOME BOOLEAN REPAIR**. Canonical attempt #2 remains blocked until that freeze is complete.

# Note — Representation authority and required distinctions

## Core claim

> **Do not grant explanatory authority to a representation before testing whether it preserves the distinction required by the target question.**

Mnemonic:

> **Resolution is not explanatory authority.**

The relevant question is not whether a representation is finer, richer, more mechanistic, or more abstract. It is whether it separates the alternatives that the claim requires.

## Minimal test

For target claim `L` and representation `O`, ask whether states that matter to the claim are collapsed:

```text
O(sa) = O(sb)
while
L(sa) ≠ L(sb)
```

If so, the current representation cannot by itself support the requested attribution.

The corrective move is not automatically “add more detail.” It may require a different partition:

```text
Ot
→ detect collapsed distinction
→ Ot+1
→ retest attribution
```

`Ot+1` may be finer, coarser, or differently organized.

## Convergence cases

```text
Layer study:      update decomposition ≠ necessity decomposition
Core dumps:       similar symptom class ≠ shared mechanism
LessWrong:        measurable variable ≠ discriminating variable
Wiener:           automatable formulation ≠ appropriate system objective
Interpretability: available decomposition ≠ correct explanatory decomposition
```

Shared failure mode:

```text
available representation
→ assumed authority over target claim
```

Shared corrective operation:

> **Test whether the representation separates the counterfactuals the claim requires.**

## Core-dump lesson

The useful change was not simply more resolution. Detailed individual crash analysis already existed.

The key move was a better partition of the observations:

```text
one apparent crash population
→ hardware-induced corruption + unwinding-induced corruption
```

That changed the causal search space and made later microscopic analysis informative.

So:

```text
information quantity ≠ distinction quality
```

More detail can preserve the wrong partition. Less detail can sometimes expose the structure needed to find the mechanism.

## Minimal experiment sketch

Construct tasks where the same underlying phenomenon is exposed through multiple representations:

1. detailed but causally collapsed;
2. coarse but correctly partitioned;
3. detailed and correctly partitioned;
4. partitioned around a correlated but non-causal feature.

Measure whether a system:

- notices when the current representation cannot support the requested attribution;
- asks for or constructs a representation that restores the missing distinction;
- avoids equating additional detail with explanatory progress;
- returns to finer-grained analysis once the relevant classes are separated.

The key comparison is:

```text
detail-seeking
vs.
distinction-seeking
```

A strong result would be recognizing:

> **More resolution is not useful here; the partition has to change.**

## Scope

This is a methodological hypothesis, not a new CARS rule and not evidence that one representation level is generally superior.

The next useful step is empirical: test whether systems can identify representation insufficiency and choose a discriminating re-partition rather than merely requesting more detail.

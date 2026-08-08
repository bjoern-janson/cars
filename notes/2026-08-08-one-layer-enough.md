# Case note — “Is One Layer Enough?”

Paper: **Is One Layer Enough?**  
Reference: https://arxiv.org/pdf/2607.01232

## Why this matters for CARS v0.2

The paper provides a concrete example of the distinction behind dependency tracing:

> A system can change in many places during successful learning without all of those changes being functionally necessary for the correction.

The useful decomposition is:

```text
participation
≠ carrier capacity
≠ sufficiency
≠ necessity
≠ substitutability
```

The paper measures **carrier capacity / isolated sufficiency** well: some individual Transformer layers can recover most or all of the gain from full-parameter RL when trained alone.

That does not establish that those layers are necessary to full-system adaptation.

A layer could satisfy:

```text
high isolated contribution + low necessity
```

and therefore be an excellent carrier or substitute rather than a fundamental dependency.

## Missing complementary intervention

For a layer `k`, distinguish at least:

- **Participation:** how much `k` changes during full RL.
- **Carrier capacity:** how much useful adaptation `k` can carry when trained alone.
- **Necessity:** how much adaptation degrades when `k` is unavailable while the rest of the system can still adapt.
- **Substitutability:** whether another layer or mechanism can preserve the same correction function.

A natural complementary test is:

```text
freeze layer k
train everything else
retest
```

This separates “can carry the correction” from “the correction depends on it.”

## Dependency-elimination interpretation

The relevant loop is:

```text
successful correction
→ candidate dependency
→ removal / restriction
→ substitution
→ retest
→ scoped functional residue
```

If several different layers can independently preserve the same behavioral correction, the important object may not be the historical layer at all. It may be the shared **function** implemented by multiple viable pathways.

```text
historical component
→ substitution class
→ functional residue
```

This is the concrete warning for CARS v0.2:

> **What changed ≠ what can carry change ≠ what change requires.**

Related existing invariant:

> **Historical presence ≠ functional necessity.**

And an experimentally useful reminder already implicit in CARS v0.1:

> **Repeated sufficiency ≠ necessity.**

## Scope

This paper is a motivating case, not evidence that CARS v0.2 works, and not evidence that middle layers are universal dependencies of RL adaptation.

The next useful evidence would come from complementary necessity and substitution interventions, not from adding more conceptual machinery.

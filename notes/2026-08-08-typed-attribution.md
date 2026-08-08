# Note — Typed attribution and discriminating tests

## Minimal catalyst

> **Do not promote an observed relation into a stronger functional attribution without a discriminating test.**

The core research loop is:

```text
attribution
→ claim type
→ discriminating intervention
→ retest
→ scoped authority
```

The point is not to rank every claim on one ladder. Different attribution types answer different questions and require different tests.

## Typed claims

For candidate component or condition `x` and function/outcome `F`:

```text
P(x)        x was present
A(x,F)      x is associated with F
S(x,F)      x can produce or preserve F
N(x,F)      F fails when x is unavailable
R(x,x',F)   x' can replace x while preserving F
T(f)        function f recurs across independent tested systems
```

None of these should be promoted automatically into another.

In particular:

```text
presence ≠ association
association ≠ sufficiency
sufficiency ≠ necessity
repeated sufficiency ≠ necessity
recurrence ≠ universality
```

## Substitution changes the preservation target

If several implementations independently preserve the same function:

```text
x1, x2, x3 → F
```

then successful substitution is evidence against preserving one historical implementation as uniquely necessary.

The preservation target may migrate:

```text
implementation
→ substitution class
→ candidate shared function
```

But the function remains scoped to the tested transfer space:

```text
T(f) ≠ universality(f)
```

## Reusable intervention question

When something appears important, ask:

> **What exactly are we claiming about it, and what intervention could distinguish that claim?**

Useful interventions include removal, perturbation, substitution, alternative measurement mappings, held-out transfer, and independent replication.

## Three independent convergence cases

These are not the same claim, but they expose the same attribution problem:

```text
Layer paper:       participation ≠ necessity
LessWrong debate:  measurement ≠ discrimination
Wiener:            automation ≠ appropriateness
```

Shared methodological warning:

> **Do not infer system-level function from local association.**

More operationally:

> **Identify the claimed functional relation, then choose an intervention that could make the stronger attribution fail.**

## Three entry points

The same procedure can be used:

```text
Before action:   What must remain intact for regulation to work?
After success:   What did success actually depend on?
After failure:   What dependency was absent, invalid, or misidentified?
```

The method may legitimately end with:

> **We do not yet know what this depends on.**

## No axiomatic exemption

The procedure itself receives the same treatment.

Do not assume its current operations are necessary for correction. If a cheaper or more reliable procedure produces better discrimination, substitute it and retest.

This note is a methodological hypothesis, not evidence that the catalyst works. The next useful addition should come from an experiment or an independently encountered lineage that survives the same analysis.

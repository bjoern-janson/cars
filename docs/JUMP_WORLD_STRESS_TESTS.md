# Jump-World Stress Tests

## Status

This is a narrow red-team supplement to `RED_TEAM_PROTOCOL.md`.

It does **not** add a new CARS rule, a new scientific hypothesis, or a claim that LLMs actually exhibit conceptual jumps.

Its purpose is only to test whether the current assay accidentally assumes smooth treatment-response structure.

## Why this test exists

The primitive scientific proposition is order-based:

```text
i₁ > i₀
⇒
τ(i₁) > τ(i₀)
```

A derivative or linear interaction coefficient is a stronger representation:

```text
∂τ(i)/∂i > 0
```

```text
τ(i) = τ₀ + δi
```

The assay should therefore be able to detect ordered causal responsiveness even when the true response surface contains thresholds, discontinuities, or rare-event mixtures.

Keep explicit:

```text
scientific ordering
≠
smoothness
≠
linearity
```

## Stress test 1 — threshold / jump world

Generate:

```text
τ(i) = 0    if i < i*
       Δ    if i ≥ i*
```

The reference implementation uses:

```text
i* = 0.65
Δ = 8
```

Primary question:

```text
Does the order-based assay detect that high-I units have a larger causal response?
```

Secondary question:

```text
Does a linear I×E coefficient conceal the actual discontinuous shape?
```

A positive linear coefficient is not itself a failure. The failure would be to interpret that coefficient as evidence that the underlying response law is linear or smooth.

The reference run reports both:

```text
τ_high - τ_low
```

and the error of the fitted linear treatment-response curve relative to the known step function.

## Stress test 2 — rare-jump mixture world

Generate a response whose mean effect is:

```text
τ(i)
=
P(jump | i) × gain_if_jump
```

The reference implementation holds jump value fixed:

```text
gain_if_jump = 30
```

while allowing jump probability to increase with `i`:

```text
P(jump | i) = 0.02 + 0.10i
```

The order-based assay should detect larger mean treatment response at higher `i`.

But the interpretation must remain limited:

```text
higher mean τ(i)
↛
larger jump magnitude
```

because the same mean CATE can arise through different mixtures of:

```text
jump probability
×
jump value
```

This is a mechanism-identification warning, not a reason to replace the current causal object.

## Reference command

```text
python scripts/run_jump_worlds.py \
  --seed 20260809 \
  --n 20000 \
  --json-out results/jump_worlds_reference.json
```

## Fixed-seed reference

At seed `20260809`, `n=20000`:

### Threshold world

```text
τ_low              ≈ 0.028
τ_high             ≈ 8.030
τ_high - τ_low     ≈ 8.002
linear δ           ≈ 10.898
linear-shape RMSE  ≈ 2.140
max shape error    ≈ 4.351
```

Interpretation:

```text
primary ordering detected
+
linear representation materially smooths the true step
```

### Rare-jump world

```text
τ_low                  ≈ 1.355
τ_high                 ≈ 3.319
τ_high - τ_low         ≈ 1.963
linear δ               ≈ 2.715
jump rate, low I       ≈ 0.0417
jump rate, high I      ≈ 0.1109
gain if jump           = 30
```

Interpretation:

```text
positive mean moderation
+
fixed jump value
+
higher jump probability
```

The mean CATE alone does not identify which component changed.

## Evidence status

These are synthetic development checks only.

They establish that the assay implementation can represent two non-smooth / mixture-generated worlds without promoting smoothness or mechanism claims.

They do not establish that:

- real LLMs jump;
- `I` predicts jump probability;
- conceptual jumps explain any observed treatment effect;
- a threshold response law exists in real systems;
- the substantive CARS responsiveness hypothesis is true.

## Stop rule

No new formal layer follows from these tests.

If future empirical data exhibit threshold, mixture, or discontinuous response structure, reopen the relevant shape/mechanism question then.

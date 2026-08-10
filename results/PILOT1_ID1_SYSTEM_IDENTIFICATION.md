# Pilot 1 ID1 — Finite-Data System Identification Result

## Status

```text
Pilot 1 Match1
→ exact-model oracle: D = 0 for N and A
→ intrinsic predictive-resource excess NOT demonstrated

ID1
→ transition/update equations hidden from learner
→ finite interaction data
→ local dynamics identified and recursively composed
→ structurally held-out order reversals tested
```

Confirmatory seed:

```text
20260830
```

A pre-contract exploratory stream was quarantined. A separate development seed was used for smoke testing. The first confirmatory execution attempt produced no outcome because row-wise evaluation exceeded the local execution budget; the runner was then repaired by vectorizing the mathematically identical rollout evaluation without changing any scientific setting.

---

## Primary result

Frozen primary cell:

```text
identifier       P3 — degree-3 polynomial ridge local dynamics
train trajectories 6000
train transitions  12000
structural holdout BA / CA / CB
endpoint           structural NMSE
```

Observed:

```text
N  0.000234729771
A  0.000235200562

A - N
= +0.000000470792
```

Literal frozen decision label:

```text
DESCRIPTIVE_HIGH_RESOURCE_A_EXCESS
```

Relative to N's structural NMSE:

```text
+0.2006%
```

The sign is positive, but the magnitude is extremely small.

Keep separate:

```text
positive sign
≠ established sample-complexity difference
≠ intrinsic predictive-resource excess
```

---

## The sample-efficiency question

Prespecified P3 tolerance crossings were identical for N and A:

| structural NMSE tolerance | N | A |
| --- | ---: | ---: |
| `0.01` | 48 | 48 |
| `0.005` | 48 | 48 |
| `0.001` | 96 | 96 |

Therefore:

```text
coarse empirical sample-threshold difference
→ NOT DETECTED
```

This is the most direct ID1 result for the finite-data identification question.

It does not prove equal minimax sample complexity.

---

## P3 structural learning curve

```text
N_train      N NMSE          A NMSE          A-N
48           0.0024136954    0.0034263331    +0.0010126377
96           0.0007628708    0.0006796515    -0.0000832193
192          0.0004369237    0.0004299764    -0.0000069473
384          0.0002773853    0.0002772308    -0.0000001545
768          0.0002526875    0.0002524564    -0.0000002312
1536         0.0002411123    0.0002446029    +0.0000034906
3072         0.0002538212    0.0002581747    +0.0000043535
6000         0.0002347298    0.0002352006    +0.0000004708
```

The only large relative P3 A/N difference occurs at the smallest sample budget. From `N=96` onward the curves are extremely close and repeatedly cross.

Thus there is no evidence here for a stable multiplicative A penalty across the sample grid.

---

## Predictor-strength subtraction

The lower-capacity P2 identifier produced a positive A-N structural contrast at every sample count, including:

```text
P2 / N=6000
A - N
= +0.0000877193
```

The stronger P3 identifier reduces that high-resource difference to:

```text
+0.0000004708
```

or about:

```text
0.54% of the P2 absolute A-N difference
```

This is strong evidence that most of the apparent A/N gap under the lower-order identifier is a **model-class / approximation effect**.

It is not evidence that P3 is intrinsically optimal.

---

## Curve and slope summaries

Frozen P3 log-curve scores:

```text
N  -3.4230892241
A  -3.4184622639

A - N
= +0.0046269602 log10 units
```

This corresponds to only about a `1.07%` multiplicative difference in the geometric-average distortion level across the frozen grid.

Frozen high-N descriptive slopes (`N_train >= 384`):

```text
β_N  -0.04784125
β_A  -0.04444909

β_A - β_N
= +0.00339215
```

Both curves are already close to their estimator approximation floor over this range.

Therefore:

```text
finite-grid slope difference
↛ different asymptotic sample-complexity exponent
```

No scaling-law claim is earned.

---

## IID diagnostic

At P3 / `N=6000`:

```text
IID NMSE
N  0.0001655104
A  0.0001563527
```

A is slightly easier, not harder, on IID training-grammar structure at the same high-resource point.

So the tiny positive structural A-N sign is not a generic prediction-error penalty.

---

## Known-dynamics reference

Match1 remains the execution-complexity reference:

```text
known equations
+
full state
+
future intervention sequence
→ exact rollout
→ D = 0 for N and A
```

ID1 therefore isolates only:

```text
finite-data identification
+
recursive structural prediction
```

The current evidence is consistent with:

```text
restricted identifier
→ visible A/N structural difference

stronger generic identifier
→ difference largely collapses
```

---

## ID1 decision

Literal primary sign:

```text
DESCRIPTIVE_HIGH_RESOURCE_A_EXCESS
```

Substantive finite-data result:

```text
coarse sample-threshold excess for A
→ NOT DETECTED

stable curve-wide A penalty
→ NOT DETECTED

different scaling regime
→ NOT ESTABLISHED

intrinsic A-vs-N identification burden
→ NOT ESTABLISHED
```

The strongest warranted interpretation is:

> **Under the frozen ID1 toy, a lower-capacity local identifier makes A consistently harder than N on structurally held-out order reversals, but a stronger generic identifier collapses nearly all of that difference and gives identical prespecified sample-threshold crossings. ID1 therefore does not establish an adaptive-specific finite-data identification burden.**

---

## Failure localization

Shallowest current explanation:

```text
PREDICTOR MODEL CLASS / APPROXIMATION
```

not:

```text
intrinsic adaptive predictive complexity
```

The remaining `+4.71e-7` high-resource sign is too small and too estimator-dependent to authorize a deeper interpretation.

Because the contract stated that any retained sign should first face a stronger generic identifier, the only earned continuation would be a **narrow identifier adversary**, not a more complex adaptive system or intervention grammar.

---

## Authority state

```text
finite-data system-identification benchmark
→ COMPLETED FOR ID1

A harder than N under P2
→ YES

A materially harder than N under P3
→ NOT ESTABLISHED

prespecified N-threshold difference
→ NONE DETECTED

sample-scaling difference
→ NOT ESTABLISHED

intrinsic predictive-resource excess
→ NOT ESTABLISHED

new construct
→ NOT EARNED

new theory
→ NOT EARNED
```

Do not tune A, increase hidden state, or expand the intervention grammar to recover a larger effect.
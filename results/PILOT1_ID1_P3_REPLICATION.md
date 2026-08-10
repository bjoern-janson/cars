# Pilot 1 ID1-R1 — P3 Replication

## Status

```text
ID1 tiny high-resource P3 discrepancy
→ REPLICATED ON FRESH RANDOM STREAM
→ SIGN REVERSED
→ ID1 DISCREPANCY CLOSED
```

This replication changes only the confirmatory random stream and executes the already-selected P3 identifier. It does not change the generator, paired-state construction, intervention grammar, structural holdout, sample grid, endpoint, ridge regularization, or decision logic.

Frozen replication seed:

```text
20260831
```

Reference ID1 seed:

```text
20260830
```

Before using the fresh stream, the local vectorized execution path was checked against the published ID1 seed and reproduced the ID1 P3 high-resource values and curve summaries to floating-point precision. The fresh-seed result therefore does not depend on a changed scientific implementation.

---

## Primary result

Frozen primary cell:

```text
identifier          P3 — degree-3 polynomial ridge local dynamics
train trajectories  6000
train transitions   12000
structural holdout  BA / CA / CB
endpoint             structural NMSE
```

Fresh-seed outcome:

```text
N  0.000219996912
A  0.000216089209

A - N
= -0.00000390770244
```

Relative to N:

```text
-1.776%
```

Frozen decision:

```text
SIGN_DISAPPEARS_OR_REVERSES
```

The original ID1 primary contrast was:

```text
ID1
A - N
= +0.000000470792
≈ +0.2006% relative to N
```

Therefore:

```text
ID1   positive tiny sign
ID1-R1 negative sign

→ directional discrepancy does not replicate
```

---

## Sample-threshold replication

Prespecified structural-NMSE tolerance crossings remain identical:

| tolerance | N | A |
| --- | ---: | ---: |
| `0.01` | 48 | 48 |
| `0.005` | 48 | 48 |
| `0.001` | 96 | 96 |

Thus the direct finite-data sample-efficiency comparison again finds:

```text
coarse empirical sample-threshold difference
→ NOT DETECTED
```

---

## P3 structural learning curve

```text
N_train      N NMSE          A NMSE          A-N
48           0.0027911887    0.0027458385    -0.0000453502
96           0.0008245945    0.0008641459    +0.0000395515
192          0.0003587967    0.0003433080    -0.0000154887
384          0.0002704307    0.0002665254    -0.0000039053
768          0.0002446867    0.0002397251    -0.0000049616
1536         0.0002310586    0.0002253546    -0.0000057040
3072         0.0002287555    0.0002239492    -0.0000048063
6000         0.0002199969    0.0002160892    -0.0000039077
```

The fresh curve does not preserve the original high-resource positive sign. From `N=192` onward every frozen cell has `A <= N` on structural NMSE.

This does not establish that A is intrinsically easier. It establishes that the original tiny positive discrepancy is not directionally stable.

---

## Curve and slope summaries

Fresh-seed P3 log-curve scores:

```text
N  -3.44055894
A  -3.44648328

A - N
= -0.00592434 log10 units
```

Fresh high-N descriptive slopes (`N_train >= 384`):

```text
beta_N  -0.06982138
beta_A  -0.07092800

beta_A - beta_N
= -0.00110662
```

The curves remain very similar. No distinct sample-scaling regime is established.

---

## Decision

The frozen replication rule was:

```text
primary A-N <= 0
→ sign disappears or reverses
→ close ID1 discrepancy
```

Observed:

```text
A - N = -3.90770244e-6
```

Therefore:

```text
ID1 TINY P3 DISCREPANCY
→ CLOSED

REPLICATION OF POSITIVE SIGN
→ FAILED

FINITE-DATA ADAPTIVE IDENTIFICATION BURDEN
→ NOT DEMONSTRATED

DISTINCT SAMPLE-COMPLEXITY REGIME
→ NOT DEMONSTRATED

NEW CONSTRUCT
→ NOT EARNED

NEW THEORY
→ NOT EARNED
```

Do not run another replication merely to recover the original sign.

---

## Current subtraction state

```text
known dynamics
→ exact simulator removes A/N gap

unknown dynamics + weak P2 identifier
→ visible A/N gap

unknown dynamics + stronger P3 identifier
→ ~99.46% of P2 high-resource gap removed

fresh-seed P3 replication
→ remaining positive sign reverses

current explanation
→ estimator / finite-sample variation is sufficient
```

The next experiment, if any, requires a new discriminating question. Longer horizons, richer intervention algebra, or a more complicated adaptive mechanism are not earned by this discrepancy.

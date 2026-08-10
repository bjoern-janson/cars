# Pilot 1 Predictive-Resource Toy — Match1

## Status

```text
Run 1
→ QUARANTINED for avoidable unpaired initial-state sampling

Match1
→ paired realized x0 / theta0 across F/N/A
→ all other scientific and estimator settings preserved
```

## Primary outcome

Frozen primary cell:

```text
representation = full_state
train_samples  = 6000
endpoint       = structural_nmse
holdout        = unseen reversed intervention orderings
```

Observed:

```text
F  0.0422111444
N  0.0409662458
A  0.0417857156
```

Primary contrast:

```text
A - N
= +0.0008194697
```

Literal frozen label:

```text
DESCRIPTIVE_A_EXCESS
```

Relative to N structural NMSE:

```text
+2.000%
```

## IID contrast

At the same `full_state / N=6000` cell:

```text
IID NMSE
N  0.0156897146
A  0.0156484394

A - N
= -0.0000412752
≈ -0.263% relative to N
```

Therefore the A/N difference is not a generic prediction-error increase under this estimator.

The pattern is:

```text
IID sequences
A ≈ N, with A slightly lower distortion

structurally held-out reversed orderings
A > N
```

This is consistent with an estimator-level structural-generalization difference.

## Structural NMSE grid

```text
x_only
N=128   F 0.04482039   N 0.04372413   A 0.04453580   A-N +0.00081168
N=512   F 0.04416359   N 0.04265309   A 0.04327498   A-N +0.00062189
N=2048  F 0.04486932   N 0.04323392   A 0.04409652   A-N +0.00086261
N=6000  F 0.04297715   N 0.04155589   A 0.04238583   A-N +0.00082995

x_theta_mean
N=128   F 0.04433624   N 0.04345231   A 0.04423164   A-N +0.00077933
N=512   F 0.04401134   N 0.04265861   A 0.04322512   A-N +0.00056651
N=2048  F 0.04558521   N 0.04394746   A 0.04483612   A-N +0.00088865
N=6000  F 0.04291505   N 0.04154429   A 0.04236950   A-N +0.00082521

full_state
N=128   F 0.05174743   N 0.04985084   A 0.05111641   A-N +0.00126557
N=512   F 0.04299680   N 0.04178826   A 0.04234271   A-N +0.00055444
N=2048  F 0.04477192   N 0.04326862   A 0.04416049   A-N +0.00089187
N=6000  F 0.04221114   N 0.04096625   A 0.04178572   A-N +0.00081947
```

The positive structural A-N contrast persists across all three representations and all four prespecified training-sample counts after realized-state pairing.

That persistence earns an explanation attempt.

It does not earn an intrinsic-complexity claim.

## Strongest adversary: exact simulator

This synthetic benchmark has known deterministic dynamics conditional on:

```text
full initial state (x0, theta0)
+
future intervention sequence
+
system class
```

For N:

```text
x_{t+1} = tanh(M(theta_t) x_t + C e_t)
theta_{t+1} = rho theta_t + eta q_t
```

For A:

```text
x_{t+1} = tanh(M(theta_t) x_t + C e_t)
theta_{t+1} = rho theta_t + eta e_t
```

Given the full state and frozen equations, an exact rollout computes the response trajectory with:

```text
predictive distortion D = 0
```

for both N and A.

The representation required by the exact simulator is the same full initial state dimensionality in both systems.

The dominant per-step computation is also the same class:

```text
construct M(theta)
matrix-vector transition
control input
tanh
theta update
```

The distinction between using prespecified `q_t` and supplied `e_t` as the update driver does not create a meaningful asymptotic computational separation in this toy.

Therefore:

```text
observed ridge structural excess
→ estimator / structural-generalization phenomenon

observed ridge structural excess
↛ intrinsic predictive-resource excess
```

## Failure localization

The shallowest sufficient explanation is:

```text
PREDICTOR / REPRESENTATION OF COMPOSITION
```

The fixed ridge interaction model approximates the nonlinear rollout and extrapolates to unseen reversed intervention orderings. A's intervention-dependent parameter update changes the composition map the predictor must approximate, and the fixed estimator generalizes slightly worse there.

But the known simulator removes the discrepancy exactly.

No deeper adaptive-specific object is required.

## Toy decision

```text
DESCRIPTIVE ESTIMATOR-LEVEL STRUCTURAL GENERALIZATION DIFFERENCE
→ YES

INTRINSIC A-vs-N PREDICTIVE-RESOURCE EXCESS
→ NOT DEMONSTRATED

NEW CONSTRUCT
→ NOT EARNED

SCALING STUDY
→ NOT EARNED BY THIS TOY
```

The toy has done its job: it manufactured a controlled setting in which a restricted predictor shows an A/N structural-generalization difference, and then the strongest available generic predictor explains that difference away.

## Stopping rule

Stop this toy branch as an intrinsic-complexity test.

A next benchmark is justified only if it asks a different question that the exact-model oracle cannot trivialize, for example statistical or computational identification when the transition/update law is not supplied to the predictor.

Do not tune this toy to make the A-N excess larger.

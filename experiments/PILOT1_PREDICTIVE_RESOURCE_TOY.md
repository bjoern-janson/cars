# Pilot 1 — Minimal Predictive-Resource Subtraction Toy

## Status

```text
PILOT 0
→ CLOSED / READ-ONLY

PILOT 1
→ NEW SCIENTIFIC QUESTION
→ SYNTHETIC PRE-OUTCOME CONTRACT
→ NO CORRECTION-SPECIFIC CONSTRUCT
→ NO NEW THEORY
```

Question:

> **Under a matched toy construction, does intervention-dependent endogenous modification of a response law produce a descriptive predictive-resource difference beyond an exogenously changing response law?**

This is not a continuation of the Pilot-0 representation-localization ladder.

## Scientific object

For initial state `s0` and intervention sequence `e1:H`, the empirical target is the observable response trajectory:

```text
Γ_H(s0, e1:H)
= distribution / trajectory of future observable states
```

Pilot 1 uses a deterministic synthetic system conditional on the sampled initial state and intervention sequence. The measured target is the flattened observable state trajectory `[x1, x2]`.

## System ladder

All systems share the same observable state space, intervention descriptors, base transition family, initial-state sampling distribution, predictor family, resource accounting, and train/test sequence grammar.

```text
F — frozen
θ does not change

N — exogenously nonstationary
θ changes according to a fixed known time-indexed driver
independent of intervention identity

A — endogenously adaptive
θ changes as a function of the intervention descriptor
```

The intended subtraction is:

```text
A versus N
```

not merely:

```text
A versus F
```

A difference between `A` and `F` that disappears for `A` versus `N` is treated as ordinary nonstationarity.

## Shared transition model

Observable state:

```text
x_t ∈ R²
```

Mutable response-law state:

```text
θ_t ∈ R²
```

Observable transition:

```text
x_{t+1}
=
tanh(M(θ_t) x_t + C e_t)
```

with:

```text
M(θ_t)
=
M0 + θ_t[0] M1 + θ_t[1] M2
```

Response-law updates:

```text
F:
θ_{t+1} = θ_t

N:
θ_{t+1} = ρ θ_t + η q_t

A:
θ_{t+1} = ρ θ_t + η e_t
```

`q_t` is a prespecified exogenous driver schedule. Its vector norm is matched to the intervention descriptors used by `A`; its identity is not selected by the realized intervention.

This is a toy matched construction, not a proof that `N` and `A` are intrinsically equivalent in every ordinary dynamical property.

## Intervention grammar

Three unit-scale intervention descriptors are used:

```text
A = [1.0, 0.0]
B = [0.8, 0.6]
C = [0.0, 1.0]
```

Horizon:

```text
H = 2
```

Training compositions:

```text
AA
BB
CC
AB
AC
BC
```

Structural holdout:

```text
BA
CA
CB
```

The first structural test is therefore **unseen order reversal**, not unseen intervention identity.

No scalar `Ω` construct is introduced. For this pilot, intervention structure is described literally as horizon-2 order reversal.

## Initial-state representations

Pilot 1 does **not** estimate an intrinsic rate-distortion frontier.

It measures an empirical upper-bound curve under three prospectively fixed representations:

```text
x_only
R = 2 scalars

x_theta_mean
R = 3 scalars

full_state
R = 4 scalars
```

`full_state` exposes the complete sampled initial `(x0, θ0)` to the predictor and therefore acts as the strongest state-augmentation adversary in this toy.

A win by a compact representation is a compression result only. A win by `full_state` is not evidence for a new state ontology.

## Predictor

One predictor class is frozen for all systems and representations:

```text
multi-output ridge regression
+
fixed polynomial interaction features
```

Features include:

```text
intercept
initial representation z
future intervention descriptors
z × intervention interactions
E1 × E2 composition interactions
```

No predictor family is tuned separately for `F`, `N`, or `A`.

Separate predictors are fitted per system class so the benchmark measures the resource needed to model each response operator rather than the ability to classify system identity.

## Resource readouts

For each representation and training-sample count, report:

```text
D
predictive distortion
→ MSE and normalized MSE

R
representation cost
→ number of stored initial-state scalars

N
sample cost
→ number of training trajectories

K
compute proxy
→ predictor feature dimension × output dimension
```

`K` is a crude fixed-model inference proxy. It is not an intrinsic computational lower bound.

## Sample grid

Frozen full-run sample counts:

```text
128
512
2048
6000
```

Training data contain 1000 initial-state draws per training sequence.

Test data contain 500 fresh initial-state draws per sequence.

## Primary endpoint

Primary distortion:

```text
structural_nmse
```

normalized mean-squared error on the structurally held-out reversed orderings.

Primary descriptive contrast at matched representation and sample count:

```text
Δ_endo
=
structural_nmse(A)
-
structural_nmse(N)
```

The primary readout is the `full_state`, maximum-training-sample value.

Decision labels:

```text
Δ_endo <= 0
→ A_NOT_HARDER_THAN_N

Δ_endo > 0
→ DESCRIPTIVE_A_EXCESS
```

These labels are descriptive synthetic outcomes only.

## Mandatory interpretation boundaries

```text
DESCRIPTIVE_A_EXCESS
↛ intrinsic adaptive complexity
↛ causal effect of adaptation as a general class
↛ new construct
↛ scaling law
↛ adaptive quality
```

```text
A_NOT_HARDER_THAN_N
↛ proof adaptation never adds predictive burden
```

```text
estimator cost
↛ intrinsic complexity
```

```text
representation dimension
↛ information-theoretic minimum
```

The measured curves are upper bounds generated by one fixed estimator family.

## First stopping rule

Pilot 1 does not escalate merely because some curve differs.

```text
full_state + maximum N
A not harder than N
→ no endogenous-excess phenomenon in this toy
→ STOP this toy branch
```

If `A` is descriptively harder than `N`:

```text
DESCRIPTIVE_A_EXCESS
→ attack with stronger predictor / state / nonstationarity matching
→ no construct promotion
```

A future scaling study is not earned by this two-step toy alone.

## Reproducibility

Smoke test:

```text
python scripts/run_pilot1_predictive_resource_toy.py \
  experiments/PILOT1_PREDICTIVE_RESOURCE_TOY_CONFIG.json \
  --json-out /tmp/pilot1_smoke.json \
  --smoke
```

Frozen full run:

```text
python scripts/run_pilot1_predictive_resource_toy.py \
  experiments/PILOT1_PREDICTIVE_RESOURCE_TOY_CONFIG.json \
  --json-out results/pilot1_predictive_resource_toy_result.json
```

A smoke run is development evidence only and must use the script's reduced sample counts. The scientific synthetic outcome is generated only from the frozen full configuration.

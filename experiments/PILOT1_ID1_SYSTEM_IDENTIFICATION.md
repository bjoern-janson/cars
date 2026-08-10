# Pilot 1 ID1 — Finite-Data System Identification Toy

## Status

```text
Pilot 0
→ CLOSED / READ-ONLY

Pilot 1 Match1
→ estimator-level structural-generalization difference observed
→ intrinsic A-vs-N predictive-resource excess NOT demonstrated
→ exact-model oracle gives D = 0 for both

ID1
→ NEW QUESTION
→ PRE-OUTCOME SYNTHETIC CONTRACT
→ UNKNOWN-DYNAMICS COLUMN
→ NO NEW CONSTRUCT
→ NO NEW THEORY
```

Question:

> **When the transition/update equations are hidden and must be inferred from finite interaction data, does the endogenous adaptive system A require more data to predict structurally held-out intervention orderings than the matched exogenously nonstationary system N?**

This changes one scientific dimension from Match1:

```text
Match1 strongest oracle:
known equations + full state + future interventions
→ exact rollout

ID1:
full state observations + interventions + finite trajectories
→ transition/update law NOT supplied
→ predictor must identify local dynamics and compose them
```

The synthetic generator, intervention grammar, horizon, initial-state distribution, and A/N equations remain inherited from Match1.

---

## Provenance / anti-retrofit

A pre-contract local implementation exploration used the earlier toy seed while checking candidate system-identification plumbing. That stream is **quarantined** and is not scientific evidence for ID1.

ID1 therefore uses a fresh confirmatory seed:

```text
20260830
```

A separate development/smoke seed is used for implementation checks.

The following are frozen before any confirmatory outcome on seed `20260830` is generated:

```text
training sequences
structural holdout
paired initial-state rule
observable interface
predictor families
sample grid
primary predictor
primary endpoint
sample-tolerance grid
curve summaries
decision labels
```

---

## Shared generator

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
tanh(M(θ_t)x_t + C e_t)
```

with:

```text
M(θ_t)
=
M0 + θ_t[0] M1 + θ_t[1] M2
```

Response-law updates:

```text
N:
θ_{t+1} = ρ θ_t + η q_t

A:
θ_{t+1} = ρ θ_t + η e_t
```

`q_t` remains the same prespecified exogenous driver schedule from Match1 and is independent of realized intervention identity.

No parameter is tuned to enlarge an A/N gap.

---

## Intervention grammar

Interventions are unchanged:

```text
A = [1.0, 0.0]
B = [0.8, 0.6]
C = [0.0, 1.0]
```

Horizon:

```text
H = 2
```

Training sequences:

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

Thus ID1 tests local-dynamics identification followed by recursive prediction on **unseen order reversals**.

No new intervention-complexity construct is introduced.

---

## Observable interface

A and N expose the same information to the identifier.

During training, each interaction supplies:

```text
current full state  s_t = (x_t, θ_t)
intervention        e_t
step index          t ∈ {0,1}
next full state     s_{t+1}
```

During structural testing, the predictor receives:

```text
initial full state  s_0
future intervention sequence e_{1:2}
system class        N or A
```

and must recursively predict the observable trajectory:

```text
(x_1, x_2)
```

Separate predictors are fitted for N and A, as in Match1. The task is to identify each response operator, not classify system identity.

Keep explicit:

```text
same observable interface
≠ complete intrinsic-complexity matching
```

---

## Predictor family

The transition/update equations and their parameters are not supplied to the learner.

Two nested generic local-dynamics estimators are frozen:

```text
P2 — degree-2 polynomial ridge transition model
P3 — degree-3 polynomial ridge transition model
```

Raw predictor input per transition:

```text
(x_t, θ_t, e_t, one_hot(t))
```

For each degree, use all monomials up to that degree plus an intercept.

Output:

```text
predicted next full state
(x_{t+1}, θ_{t+1})
```

Prediction on a horizon-2 sequence is recursive:

```text
ŝ_1 = f_hat(ŝ_0, e_1, t=0)
ŝ_2 = f_hat(ŝ_1, e_2, t=1)
```

`P3` is the **primary estimator adversary** because it strictly contains the lower-order polynomial feature family.

No system receives a separately tuned feature family or ridge penalty.

---

## Paired sampling

For every sequence and split, N and A use the same realized sampled initial states:

```text
same x_0
same θ_0
```

Training-trajectory subsampling is nested and balanced by intervention sequence.

The sample grid is expressed as total trajectories, with equal counts from each of the six training sequences:

```text
48
96
192
384
768
1536
3072
6000
```

Equivalently, per training sequence:

```text
8
16
32
64
128
256
512
1000
```

Each trajectory contributes two observed transitions.

Structural test data use 500 fresh paired initial states per held-out sequence.

---

## Primary empirical object

For each system, predictor degree, and training-sample count, report:

```text
structural_mse
structural_nmse
IID_mse
IID_nmse
```

Primary distortion:

```text
structural_nmse
```

on `BA`, `CA`, and `CB`.

Known-dynamics Match1 remains a reference column only:

```text
known equations + full state
→ D = 0 for both N and A
```

ID1 measures:

```text
identification + recursive prediction
```

not execution of a supplied simulator.

---

## Resource accounting

For each estimator report:

```text
N
→ number of training trajectories

R_model
→ fitted coefficient count

K_step
→ feature dimension × next-state output dimension

D
→ predictive distortion
```

These remain estimator-level upper bounds.

```text
learned model size
↛ intrinsic representational minimum

observed sample curve
↛ minimax sample complexity

inference mult-add proxy
↛ intrinsic computational lower bound
```

---

## Sample-efficiency readouts

### 1. Primary high-resource contrast

At:

```text
P3
N_train = 6000 trajectories
```

report:

```text
Δ_high
=
structural_nmse(A)
-
structural_nmse(N)
```

Labels:

```text
Δ_high <= 0
→ NO_HIGH_RESOURCE_A_EXCESS

Δ_high > 0
→ DESCRIPTIVE_HIGH_RESOURCE_A_EXCESS
```

### 2. Tolerance crossing

For `P3`, report the smallest frozen training-grid value achieving:

```text
structural_nmse <= ε
```

for each:

```text
ε ∈ {0.01, 0.005, 0.001}
```

If no grid value crosses the threshold, report:

```text
>6000
```

These are coarse empirical sample thresholds, not intrinsic `N*`.

### 3. Curve summary

For each system and predictor degree, compute the normalized trapezoidal area of:

```text
log10(structural_nmse)
vs
log10(N_train)
```

over the frozen sample grid.

Lower is better.

### 4. High-N descriptive slope

For `P3`, fit:

```text
log10(structural_nmse)
~
β log10(N_train)
```

using only:

```text
N_train >= 384
```

Report `β_A` and `β_N` descriptively.

```text
slope difference
↛ asymptotic scaling-law difference
```

---

## Decision logic

The first ID1 interpretation is deliberately shallow.

```text
P3 removes A-N excess
→ lower-order estimator artifact / insufficient model class
→ STOP adaptive-specific interpretation in ID1
```

```text
P3 retains A-N excess
→ descriptive finite-data identification difference
→ attack with stronger generic identifier / replication
→ no intrinsic-complexity claim
```

```text
A and N cross the same tolerance at the same sample grid
→ no detected coarse sample-threshold difference at that tolerance
```

```text
A requires more samples at one tolerance
→ local empirical sample difference only
→ not a scaling law
```

No result from this one toy authorizes:

```text
adaptive-complexity construct
universal sample-complexity claim
new predictive-state theory
cross-system law
```

---

## Stopping rule

Stop ID1 without escalation if the strongest frozen generic identifier (`P3`) removes the A/N structural-generalization excess at high resource and shows no robustly worse sample-efficiency pattern for A across the frozen readouts.

If an A/N difference remains:

```text
first next action
→ stronger generic system-identification adversary
```

not:

```text
make A more complex
expand the intervention grammar
name a new construct
claim intrinsic scaling
```

---

## Reproducibility

Development smoke:

```text
python scripts/run_pilot1_id1_system_identification.py \
  experiments/PILOT1_ID1_SYSTEM_IDENTIFICATION_CONFIG.json \
  --json-out /tmp/pilot1_id1_smoke.json \
  --smoke
```

Confirmatory synthetic run:

```text
python scripts/run_pilot1_id1_system_identification.py \
  experiments/PILOT1_ID1_SYSTEM_IDENTIFICATION_CONFIG.json \
  --json-out results/pilot1_id1_system_identification_result.json
```

The smoke stream uses a separate development seed. Only the frozen confirmatory seed contributes to the ID1 result.
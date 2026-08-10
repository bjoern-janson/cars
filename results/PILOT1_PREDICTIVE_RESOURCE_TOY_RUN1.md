# Pilot 1 Predictive-Resource Toy — Run 1

## Provenance

Generated only after the pre-outcome contract, config, and runner were committed on branch:

```text
agent/pilot1-predictive-resource-toy
```

Frozen contract/config lineage before outcome generation:

```text
experiments/PILOT1_PREDICTIVE_RESOURCE_TOY.md
experiments/PILOT1_PREDICTIVE_RESOURCE_TOY_CONFIG.json
scripts/run_pilot1_predictive_resource_toy.py
```

## Primary literal outcome

Frozen primary cell:

```text
representation = full_state
train_samples  = 6000
endpoint       = structural_nmse
```

Observed:

```text
F  0.0422111444
N  0.0421104033
A  0.0424788007

A - N
= +0.0003683974
```

The literal sign-only decision rule therefore returns:

```text
DESCRIPTIVE_A_EXCESS
```

Relative to the N structural NMSE, the excess is approximately:

```text
+0.875%
```

This is a very small descriptive difference.

## Representation / sample grid

Structural NMSE:

```text
x_only
N=128   F 0.04482039   N 0.04595862   A 0.04966941   A-N +0.00371079
N=512   F 0.04416359   N 0.04544431   A 0.04296319   A-N -0.00248112
N=2048  F 0.04486932   N 0.04234313   A 0.04273655   A-N +0.00039342
N=6000  F 0.04297715   N 0.04207493   A 0.04262632   A-N +0.00055138

x_theta_mean
N=128   F 0.04433624   N 0.04657117   A 0.05107906   A-N +0.00450789
N=512   F 0.04401134   N 0.04512379   A 0.04256818   A-N -0.00255561
N=2048  F 0.04558521   N 0.04220327   A 0.04270941   A-N +0.00050614
N=6000  F 0.04291505   N 0.04217579   A 0.04259705   A-N +0.00042126

full_state
N=128   F 0.05174743   N 0.05721238   A 0.05489218   A-N -0.00232019
N=512   F 0.04299680   N 0.04365614   A 0.04425076   A-N +0.00059463
N=2048  F 0.04477192   N 0.04214825   A 0.04269956   A-N +0.00055131
N=6000  F 0.04221114   N 0.04211040   A 0.04247880   A-N +0.00036840
```

IID NMSE at `full_state / N=6000`:

```text
F  0.01591003
N  0.01671466
A  0.01670838
```

The structural holdout is therefore materially harder than the IID split for all three systems under this predictor family.

## Post-outcome design diagnosis

Run 1 used distinct deterministic RNG offsets for `F`, `N`, and `A`.

Therefore:

```text
same initial-state distribution
≠ same realized initial states
```

For a coarse comparison this is not automatically invalid, but the primary `A-N` difference is small enough that unpaired initial-state sampling is an avoidable source of noise in the intended matched-system subtraction.

Failure locus:

```text
EXPERIMENTAL MATCHING / SAMPLING DESIGN
```

Minimal repair:

```text
pair the realized x0, θ0 draws across F/N/A

preserve:
- dynamics
- intervention grammar
- train/test sequences
- predictor family
- representations
- sample grid
- endpoint
- primary contrast
```

## Authority state

```text
Run 1 literal sign
→ DESCRIPTIVE_A_EXCESS

Run 1 scientific interpretation
→ QUARANTINED PENDING MATCHING REPAIR
```

Do not use Run 1 to claim:

```text
endogenous predictive burden
intrinsic complexity
scaling
new construct
new theory
```

The matching repair is earned because it removes an avoidable discrepancy in the intended F/N/A controlled subtraction; it is not authorized to tune the system toward a preferred outcome.

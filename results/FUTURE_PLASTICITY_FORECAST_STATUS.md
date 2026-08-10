# Future Plasticity Forecast Benchmark — Current Status

## Frozen artifacts

```text
experiments/FUTURE_PLASTICITY_FORECAST.md
experiments/FUTURE_PLASTICITY_FORECAST_CONFIG.json
scripts/run_future_plasticity_forecast.py
```

Branch:

```text
agent/future-plasticity-forecast-benchmark
```

The benchmark is independent of the closed Pilot-1 / ID1 toy lineage.

## Development smoke

A synthetic-data smoke run executed the complete G0-G3 plumbing path:

```text
continual history
→ checkpoint measurements
→ future-task RNG consumed only after checkpoint construction
→ checkpoint/fresh paired future learning curves
→ ΔAUC + T90-gap outcomes
→ grouped nested ridge forecasts
→ history-group bootstrap comparisons
```

Smoke mode used four history streams and checkpoint ages `1, 2, 4`, producing 12 checkpoint/future pairs.

```text
SMOKE_ONLY
→ plumbing evidence
↛ Permuted-MNIST result
↛ plasticity forecastability
↛ G0-G3 scientific outcome
```

## Full benchmark outcome

```text
NOT GENERATED
```

Reason:

The active execution environment does not contain canonical MNIST and cannot resolve external dataset hosts through its Python/network stack. The scientific config deliberately sets dataset download to `false` and requires the real MNIST benchmark rather than silently substituting another dataset.

Therefore:

```text
missing local dataset
→ execution environment limitation
→ no scientific outcome
```

Not:

```text
missing local dataset
→ change benchmark family
→ use synthetic smoke as evidence
```

## Frozen full-run command

Once canonical MNIST is provisioned under the configured root:

```text
python scripts/run_future_plasticity_forecast.py \
  experiments/FUTURE_PLASTICITY_FORECAST_CONFIG.json \
  --json-out results/future_plasticity_forecast_result.json
```

No G4-G6 escalation is authorized by the smoke run.

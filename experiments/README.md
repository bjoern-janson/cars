# Experiments

## Current status

Pilot 0 is **closed**. Its representation-localization and replication/transport branches reached an epistemic stopping point; no A8, R2, or additional `T_instability` decomposition is currently earned.

Authoritative terminal interpretation:

- [`../results/PILOT0_TERMINAL_RECORD.md`](../results/PILOT0_TERMINAL_RECORD.md)

Frozen original protocol and provenance requirements remain unchanged as historical pre-outcome contracts:

- [`PILOT0_MMLU_PRO.md`](PILOT0_MMLU_PRO.md)
- [`PILOT0_PROVENANCE.md`](PILOT0_PROVENANCE.md)

Keep explicit:

```text
CLOSED
≠ theory established
≠ certainty
≠ zero uncertainty

CLOSED
= no presently justified escalation
```

Any future empirical branch requires a genuinely new scientific question and a fresh pre-outcome contract.

## Pilot 0 terminal summary

The original moderation hypothesis was not supported:

```text
higher I₁ → greater benefit from verified-error feedback
STATUS: NOT SUPPORTED
```

The subsequent diagnostic program localized representation-dependent transition behavior without promoting a global correction construct.

Terminal endpoint ledger:

| Object | Status |
| --- | --- |
| `T_change` × prior-state encoding | **CAUSAL** |
| `T_change` × section scaffold | **CAUSAL** |
| `T_change` × encoding×scaffold | **CAUSAL INTERACTION** |
| `T_verified` × prior-state encoding | **CAUSAL** |
| `T_verified` × conversational topology | **CAUSAL** |
| `T_verified` × section scaffold | **PRACTICALLY SMALL** |
| `T_verified` × encoding×scaffold | **UNRESOLVED** |
| `T_instability` × broad inline representation | **CAUSAL** |
| `T_instability` × prior-state encoding | **CAUSAL / REPLICATED / PRACTICALLY SMALL** |
| `T_instability` × section scaffold | **PRACTICALLY SMALL** |
| `T_instability` × encoding×scaffold | **PRACTICALLY SMALL** |
| excess R1 cohort variation | **NOT DETECTED** |
| transport invariance | **NOT ESTABLISHED** |

The unresolved `T_verified` interaction is endpoint-local and does not reopen the closed `T_instability` branch.

## Pilot 0 experiment lineage

The executable Pilot 0 artifacts are retained for provenance and reproducibility.

### Core frozen implementation

- [`PILOT0_QWEN3_4B_CONFIG.json`](PILOT0_QWEN3_4B_CONFIG.json)
- [`PILOT0_ANALYSIS_V2.json`](PILOT0_ANALYSIS_V2.json)
- [`PILOT0_CONFIRMATORY_RUN1_2026-08-09.md`](PILOT0_CONFIRMATORY_RUN1_2026-08-09.md)

### Measurement and signal diagnostics

- [`PILOT0_A1D_CHARACTERIZATION_CONFIG.json`](PILOT0_A1D_CHARACTERIZATION_CONFIG.json)
- [`PILOT0_A2D_CONFIG.json`](PILOT0_A2D_CONFIG.json)
- [`PILOT0_B0_CONFIG.json`](PILOT0_B0_CONFIG.json)
- [`PILOT0_B0_V2_CONFIG.json`](PILOT0_B0_V2_CONFIG.json)
- [`PILOT0_B1_CONFIG.json`](PILOT0_B1_CONFIG.json)

### Representation localization

- [`PILOT0_A3_CONFIG.json`](PILOT0_A3_CONFIG.json)
- [`PILOT0_A4A_CONFIG.json`](PILOT0_A4A_CONFIG.json)
- [`PILOT0_A4B_CONFIG.json`](PILOT0_A4B_CONFIG.json)
- [`PILOT0_A4C_CONFIG.json`](PILOT0_A4C_CONFIG.json)
- [`PILOT0_A4C_ANALYZER_REPAIR1.json`](PILOT0_A4C_ANALYZER_REPAIR1.json)
- [`PILOT0_A5_CONFIG.json`](PILOT0_A5_CONFIG.json)
- [`PILOT0_A6_CONFIG.json`](PILOT0_A6_CONFIG.json)
- [`PILOT0_A7_CONFIG.json`](PILOT0_A7_CONFIG.json)

### Replication / transport

- [`PILOT0_R1_CONFIG.json`](PILOT0_R1_CONFIG.json)

R1 is deliberately not part of an endless A-series localization ladder. It directly tested whether the inherited prior-state-encoding effect on `T_instability` reproduced across four independently sampled prestate cohorts.

Its terminal common effect was:

```text
Δ_common = +0.033975
95% CI   = [+0.021316,+0.047791]
p        = 0.00019996
```

The effect is nonzero/reproduced while the entire common-effect interval lies inside the inherited `±0.05` practical region.

Transport diagnostic:

```text
Q = 1.120334
df = 3
p = 0.772168
I² = 0
tau²_DL = 0
```

Interpret only as compatibility with a common-effect model under the prespecified diagnostic, not proof of transport invariance.

## Synthetic assay red-team

Run:

```text
python scripts/run_assay_red_team.py \
  --seed 20260809 \
  --n 20000 \
  --json-out results/synthetic_assay_reference.json
```

Purpose:

```text
known synthetic world
→ analysis pipeline
→ expected null / artifact / invariance
```

This is development evidence only. It tests whether the assay implementation is capable of rejecting or localizing manufactured conclusions.

Reference results:

- [`../results/SYNTHETIC_ASSAY_REFERENCE.md`](../results/SYNTHETIC_ASSAY_REFERENCE.md)
- [`../results/synthetic_assay_reference.json`](../results/synthetic_assay_reference.json)

## Threshold / rare-jump stress tests

Run:

```text
python scripts/run_jump_worlds.py \
  --seed 20260809 \
  --n 20000 \
  --json-out results/jump_worlds_reference.json
```

Purpose:

```text
non-smooth / mixture response truth
→ order-based assay
→ check that smoothness is not silently promoted
```

Documentation:

- [`../docs/JUMP_WORLD_STRESS_TESTS.md`](../docs/JUMP_WORLD_STRESS_TESTS.md)
- [`../results/jump_worlds_reference.json`](../results/jump_worlds_reference.json)

These are synthetic development checks only. They do not add `jump` to the CARS prompt or scientific hypothesis.

## General randomized LLM assay

Protocol:

- [`LLM_ASSAY_PROTOCOL.md`](LLM_ASSAY_PROTOCOL.md)

Assignment:

```text
python scripts/randomize_llm_assay.py \
  units.jsonl \
  assignments.jsonl \
  --arms E0 E+
```

Completed-run analysis:

```text
python scripts/analyze_llm_assay.py \
  completed_runs.jsonl \
  --treated E+ \
  --control E0 \
  --json-out result.json
```

The analysis reports the scientific proposition before any optional parametric representation.

## Evidence ladder

Keep the authority ladder explicit:

```text
synthetic red-team survival
↛ plumbing success
↛ real randomized evidence
↛ replication
↛ transport invariance
↛ stable law
```

Pilot 0 earned scoped randomized and replication evidence about transition-specific representation effects. It did not establish a general theory of intelligence or global correction capacity.

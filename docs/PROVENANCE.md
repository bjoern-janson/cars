# Provenance and Research Workflow

## Research direction

CARS is directed by **Björn Janson** as part of an independent research program on adaptive reasoning, evidence use, future viability, causal responsiveness, plasticity, predictive state, measurement identity, representation failure, and epistemic governance.

## AI-assisted workflow

AI systems are used as research collaborators and development tools. Depending on the artifact, assistance may include:

- drafting and restructuring prose;
- adversarial critique;
- generating counterexamples and synthetic worlds;
- comparing alternative formulations;
- repository construction;
- code scaffolding;
- documentation;
- benchmark-case generation;
- consistency checks;
- formalization of candidate hypotheses and evaluation criteria;
- measurement-theoretic analysis;
- causal-inference design discussion;
- notation design;
- implementation and smoke testing.

AI assistance is **not** independent scientific validation.

## Current canonical artifact hierarchy

Current repository-level documents:

- [`INTELLIGENCE_THEORY.md`](INTELLIGENCE_THEORY.md) — functional theory conjecture;
- [`CURRENT_RESEARCH_STATE.md`](CURRENT_RESEARCH_STATE.md) — terminal empirical/state ledger;
- [`RESEARCH_CONTRACT.md`](RESEARCH_CONTRACT.md) — active authority and escalation rules;
- [`CLAIMS_AND_NONCLAIMS.md`](CLAIMS_AND_NONCLAIMS.md) — current claim boundary.

Historical Pilot-0 assay documents remain frozen provenance rather than current top-level scientific objects:

- [`ASSAY_SPEC.md`](ASSAY_SPEC.md);
- [`MEASUREMENT_BOUNDARY.md`](MEASUREMENT_BOUNDARY.md);
- [`../experiments/PILOT0_MMLU_PRO.md`](../experiments/PILOT0_MMLU_PRO.md);
- [`../results/PILOT0_TERMINAL_RECORD.md`](../results/PILOT0_TERMINAL_RECORD.md).

## Top-level theory provenance

The current theory is:

> **Intelligence is the capacity of a system to convert appropriately informative new evidence into increased expected future viability.**

Shorthand:

```text
I_t ∝ Δ_E[V_{t+h}]
```

The shorthand is not a validated law, linearity claim, or established definition. The theory emerged from a longer lineage involving correction, adaptive reasoning, causal responsiveness, predictive-state framing, and repeated subtraction against stronger generic explanations.

The theory therefore must not be treated as independently discovered from the same evidence used to motivate it.

## Pilot 0 provenance

Pilot 0 operationalized a narrow causal-response question using:

```text
I₁ = 1 - P(correct)
```

under one frozen Qwen3-4B / MMLU-Pro configuration.

The original moderation hypothesis was not supported. Subsequent diagnostics localized representation-dependent transition effects and closed after replication/transport work.

Pilot 0 remains read-only and does not supply evidence for the current future-plasticity benchmark.

## Post-Pilot-0 subtraction provenance

After Pilot 0, multiple candidate correction-specific abstractions were generated and attacked, including controller, transition, lineage, sufficiency, discovery, compression, and challengeability formulations.

These subtraction artifacts were developed inside the same AI-assisted research lineage. They are not independent evidence for one another.

The current scoped conclusion is only that no empirically independent correction-specific primitive was identified within the audited Pilot-0 phenomenon space.

Historical subtraction branches remain provenance; they are not silently promoted into `main` as validated theory.

## Pilot 1 predictive-resource provenance

Pilot 1 introduced a new synthetic F/N/A benchmark independent of Pilot 0.

The first unpaired run was quarantined when an avoidable realized-state matching defect was identified.

Match1 repaired only that defect by pairing the same realized `(x0, θ0)` states across systems while preserving the scientific generator and estimator settings.

A restricted predictor produced a descriptive structural-generalization A>N gap, but the exact known-dynamics simulator removed the discrepancy entirely.

Therefore the stronger intrinsic-complexity interpretation was not retained.

## ID1 provenance

ID1 changed one scientific dimension: the transition/update equations were hidden from the predictor, requiring finite-data system identification.

A pre-contract exploratory stream using an older toy seed was quarantined from confirmatory authority.

The confirmatory ID1 stream used a fresh frozen seed. A row-wise implementation path exceeded the execution budget without producing a scientific outcome; the runner was vectorized with mathematically identical evaluation and no changes to the scientific contract before the confirmatory outcome was generated.

The stronger P3 identifier removed approximately 99.46% of the weak-identifier high-resource A/N gap.

A fresh-seed P3 replication was then frozen before outcome generation. The original tiny positive sign reversed, closing the discrepancy under the prespecified rule.

Do not reuse the exposed ID1 streams as fresh validation for a successor benchmark.

## Future plasticity benchmark provenance

The future-plasticity forecast benchmark is independently motivated by an established continual-learning phenomenon rather than by the failed ID1 discrepancy.

Frozen contract:

- [`../experiments/FUTURE_PLASTICITY_FORECAST.md`](../experiments/FUTURE_PLASTICITY_FORECAST.md)
- [`../experiments/FUTURE_PLASTICITY_FORECAST_CONFIG.json`](../experiments/FUTURE_PLASTICITY_FORECAST_CONFIG.json)

The benchmark enforces:

```text
continual history
→ checkpoint
→ checkpoint measurements frozen
→ future-task RNG consumed
→ future task generated
→ checkpoint/fresh future learning measured
```

The future task therefore does not enter checkpoint-predictor construction.

A synthetic smoke run exercised the full implementation path but has development authority only.

Canonical MNIST was unavailable in the active execution environment, so no full scientific outcome was generated and no surrogate dataset was substituted.

Current status:

```text
DESIGN          PASS
IMPLEMENTATION  PASS
SMOKE           PASS
SCIENTIFIC DATA unavailable in active execution environment
RESULT          ∅
INTERPRETATION  ∅
```

## Selection-information boundary

Any benchmark, calibration set, model parse, critique, prior result, synthetic attack, seed stream, predictor family, or task family that can influence later design becomes part of the research lineage once exposed.

Do not later relabel exposed development information as fresh independent validation.

Examples:

```text
Pilot 1 outcome
→ may motivate ID1 question
→ cannot be ID1 holdout evidence

ID1 outcome
→ cannot select features or outcomes for the independent future-plasticity benchmark

synthetic smoke
→ plumbing evidence only
→ cannot become scientific benchmark evidence
```

## Sequential provenance

Evidence changes status over time.

For sequential revisions, record:

- when each benchmark/calibration environment was first exposed;
- what revisions occurred afterward;
- which generators, task families, measurements, and estimators were reused;
- which random streams were developmental versus confirmatory;
- which audit cases remained unavailable to the development lineage;
- whether a repair occurred before or after scientific outcome exposure.

## Construct / metric provenance

Theory, scientific object, measurement, and estimator remain distinct.

```text
theory shorthand
≠ operational measurement
≠ predictor
≠ estimator
≠ construct validity
```

Operational quantities acquire interpretation through reliability, predictive validity, causal identification where relevant, replication, and transport—not through their symbol names.

In particular:

```text
I_t ∝ Δ_E[V_{t+h}]
```

is currently a theory conjecture, not a validated metric.

## Independence dimensions

Stronger evidence should increase independence along dimensions such as:

- case authorship;
- benchmark generator;
- future-task generator;
- intervention/task construction;
- measurement instrument construction;
- calibration data;
- random stream;
- analysis implementation;
- estimator / predictor family;
- model family / population;
- evaluator;
- replication team.

Independence is not binary by default. Claims should state which dimensions were separated and which remain shared.

## Authority boundary

Internally generated theories, simulations, implementations, benchmarks, critiques, and convergent model interpretations acquire no scientific authority merely because they are coherent or executable.

The current workflow is:

```text
conjecture
→ prospectively frozen empirical question
→ data
→ strongest generic comparator
→ failure localization
→ minimal revision
→ held-out retest / replication if earned
→ stop when no residual remains
```

not a closed loop in which internally generated theory validates itself.

## Governing provenance rule

> **A result may evaluate a prior decision, but later outcomes may not retroactively supply the rationale, measurement choice, predictor, or hypothesis that generated that decision.**

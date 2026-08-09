# Provenance and Research Workflow

## Research direction

CARS is directed by **Björn Janson** as part of an independent research program on adaptive reasoning, correction, causal responsiveness, measurement identity, representation failure, and epistemic governance.

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
- notation design and blind-decoding diagnostics.

AI assistance is not independent scientific validation.

## Current artifact lineage

The following were developed within the same broader AI-assisted research workflow:

- CARS prompt variants and current control protocol;
- design rationale and claims documents;
- seed prompt-level benchmark;
- historical typed-attribution / representation-authority notes;
- historical recursive correction architecture;
- historical catalyst notation and execution semantics;
- current minimal causal-responsiveness assay;
- current measurement-boundary theorem/specification;
- current adversarial assay red-team protocol;
- evaluation, experiment, and result-reporting scaffolding.

They are internally generated research artifacts, not independent evidence for one another.

In particular:

```text
CARS control protocol
↛ assay hypothesis true

assay architecture
↛ CARS prompt effective

measurement theorem
↛ empirical measurement equivalence

synthetic red-team result
↛ real-world treatment-effect heterogeneity

historical recursive architecture
↛ current assay validated
```

## Current empirical object provenance

The current scientific object is:

```text
τ(i)
=
E[V(e₁)-V(e₀) | I=i]
```

with the primitive ordering proposition:

```text
i₁ > i₀
⇒
τ(i₁) > τ(i₀).
```

This proposition emerged from a longer research trajectory beginning with the motivating conjecture:

```text
I ∝ C_improve
```

and later causal-response compressions.

The lineage matters because the current assay should not be treated as an independently discovered empirical law. It is a candidate hypothesis generated inside the same research program and must therefore face external/adversarial evidence.

## Measurement-boundary provenance

The current measurement rule was sharpened through adversarial counterexample analysis.

The working boundary is:

```text
I
→ order structure
→ strictly increasing transforms preserve the primitive ordering

V
→ additive difference structure
→ positive affine transforms preserve additive-CATE ordering
```

This is a mathematical constraint on the current estimand, not empirical evidence that any real measurement instrument is valid or interval-equivalent.

Claims that two independently constructed outcome instruments belong to the same affine-equivalence class require separate calibration evidence.

## Red-team provenance

Synthetic or constructed attacks are development evidence.

They are useful for demonstrating that an estimator or scientific claim can fail under known conditions, including:

- constant-effect worlds;
- ceiling/floor artifacts;
- nonlinear outcome remeasurement;
- confounded treatment assignment;
- generic plasticity;
- measurement-equivalence failures.

A synthetic counterexample can falsify an overstrong mathematical or methodological claim, but synthetic survival does not establish empirical validity in real systems.

## CARS prompt provenance

The current control protocol is in `prompts/CARS-CONTROL-PROTOCOL.md`.

Historical prompt snapshots remain in `prompts/CARS-v0.1.md` and `prompts/CARS-v0.2-CANDIDATE.md`.

Prompt versions should be treated as interventions. If a prompt experiment matters, record the exact file/hash and all context supplied to the model.

## Historical catalyst diagnostics

Blind or semi-blind model parses of the August 8 catalyst remain useful development diagnostics for semantic recoverability.

They do not constitute evidence for the current causal-responsiveness assay.

If catalyst experiments are reactivated, preserve the exact tested string and full context shown to the model.

## Selection-information boundary

Any benchmark, calibration set, model parse, critique, prior result, or synthetic attack that can influence assay design, measurement choice, estimator choice, or threshold selection becomes part of the research lineage.

Do not later relabel exposed development information as fresh independent validation.

For independently constructed measurement instruments, keep calibration data separate from treatment-effect data when claiming independent interval-equivalence testing.

## Sequential provenance

Evidence changes status over time.

A benchmark or calibration set may be fresh for one decision, then become part of later design history once its results are observed.

For sequential revisions, record:

- when each benchmark/calibration environment was first exposed;
- what revisions occurred afterward;
- which generators or instruments were reused;
- which audit cases remained unavailable to the development lineage.

## Construct / metric provenance

The motivating conjecture and operational measures remain distinct.

```text
I ∝ C_improve
```

is a research framing, not a validated definition.

`I`, `M_I`, `V`, and `M_V` used in an experiment are operational measurements. Their interpretation must be earned through reliability, invariance, predictive validity, causal-response relations, and transport—not through symbol names.

## Independence dimensions

Stronger evidence should increase independence along dimensions such as:

- case authorship;
- benchmark generator;
- intervention construction;
- measurement instrument construction;
- calibration data;
- analysis implementation;
- estimator;
- model family / population;
- evaluator;
- replication team.

Independence is not binary by default. Claims should state which dimensions were actually separated and which remain shared.

## Authority boundary

AI-generated suggestions, simulations, implementations, benchmark cases, formal notation, critiques, or agreeing model interpretations acquire no scientific authority merely because they are coherent, executable, or convergent.

The current protocol should therefore be read as:

```text
assay
→ data
→ CARS localization
→ revision only if earned
```

not as a closed loop in which internally generated theory validates itself.

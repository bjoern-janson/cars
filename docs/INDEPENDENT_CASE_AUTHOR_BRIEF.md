# Independent Case Author Brief

## Purpose

Create tasks and measurement conditions that test the CARS research program without reproducing its vocabulary or design assumptions.

There are now two primary authoring surfaces:

```text
1. prompt-level CARS reasoning cases
2. heterogeneous causal-responsiveness assay cases
```

Historical catalyst and recursive-architecture cases remain optional and separate.

Prospective authors should ideally work from this brief without inspecting the intervention prompt, current assay conclusions, seed cases, or prior evaluation results unless the study explicitly requires otherwise.

The goal is to create discriminating evidence, not framework-recognition tasks.

# A. Prompt-level reasoning cases

Create difficult but adjudicable cases in which a strong reasoner must do one or more of the following:

- distinguish possible sources of an error;
- update after genuine disconfirming evidence;
- resist updating after irrelevant or weak criticism;
- distinguish dependent observations from independent evidence;
- decide whether local repair is sufficient or deeper change is warranted;
- reject one explanation without automatically accepting another;
- remain unresolved when evidence is insufficient;
- resolve when evidence is sufficient;
- make a decision while important beliefs remain uncertain;
- carry a valid correction into a structurally different follow-up problem.

Do not use CARS terminology in the model-facing prompt.

# B. Causal-responsiveness assay cases

The assay tests:

```text
τ(i)
=
E[V(e₁)-V(e₀) | I=i]
```

and the ordering proposition:

```text
i₁ > i₀
⇒
τ(i₁) > τ(i₀).
```

Independent case authors can contribute by constructing experimental worlds where the true treatment-effect structure is known or adjudicable.

## Requested positive/negative worlds

Include cases where:

- the treatment effect is genuinely increasing with `I`;
- the treatment effect is constant across `I`;
- the treatment effect decreases with `I`;
- the relationship is non-monotonic;
- `I` strongly predicts baseline outcome but not treatment response;
- `I` weakly predicts baseline outcome but strongly predicts treatment response.

The benchmark should not be dominated by worlds that confirm the target ordering.

## Requested measurement attacks

Create paired worlds or instruments testing:

- ceiling/floor saturation;
- different available headroom across `I`;
- reliable versus noisy `I` measurement;
- reliable versus noisy `V` measurement;
- positive affine outcome transformations;
- nonlinear monotone outcome transformations;
- independently constructed outcome instruments that are approximately interval-equivalent;
- instruments with high ordinary correlation but different treatment/moderator-specific residual structure.

Record which transformations are intended to preserve the same scientific object and which deliberately change the additive estimand.

## Requested causal-identification attacks

Include matched designs where:

- treatment is genuinely randomized;
- treatment assignment is deliberately confounded;
- positivity is restricted in part of the `I` support;
- attrition depends on treatment and/or `I`;
- intervention delivery differs across groups despite nominal randomization.

The model/evaluator should be able to distinguish a failed causal design from a failed moderation hypothesis.

## Requested specificity worlds

Where the study targets correction rather than generic intervention responsiveness, construct intervention status independently of the tested system:

```text
E⁺ = warranted correction
E⁰ = neutral / irrelevant
E⁻ = misleading
```

Include:

- generic-plasticity worlds where higher `I` amplifies all interventions;
- discriminative worlds where response tracks the warranted status of the intervention;
- circular worlds where intervention status is defined using the tested system's own outputs, as a negative control.

# C. Measurement construction

If authoring an outcome instrument, document:

- what target quantity it intends to measure;
- why additive differences are intended to be meaningful;
- admissible transformations;
- known ceiling/floor behavior;
- reliability/noise model;
- whether measurement behavior depends on treatment or moderator level.

If two instruments are intended to be interval-equivalent, provide calibration data or a calibration procedure independent of the treatment-effect test.

Do not treat high correlation as sufficient evidence of interval equivalence.

# D. Hidden truth / adjudication

Each assay case should record author-side truth or adjudication logic for:

- treatment assignment mechanism;
- true or intended treatment-effect pattern;
- baseline/outcome relationship;
- moderator/outcome relationship;
- measurement transformation class;
- whether a changed measurement defines the same or a different causal estimand;
- expected failure mode if the assay is fooled.

# E. Sequential / transfer cases

For later transport work, create fresh task families whose hidden structure is not derived from previously exposed validation items.

Useful sequence:

```text
development
→ fresh validation
→ later independent audit
```

Do not reuse exposed cases and continue describing them as held out.

# F. Avoid

- CARS terminology in model-facing prompts;
- naming the missing abstraction or failure class;
- constructing every case so the target hypothesis is true;
- rewarding verbosity or cautious tone by itself;
- using a nonlinear outcome transform and calling it an invariance failure without establishing that the same additive estimand should be preserved;
- defining `E⁺/E⁻` using the tested system's own reaction;
- fitting measurement calibration after seeing treatment-effect results and calling it independent;
- treating a high `I×E` coefficient as proof that `I` is causal;
- treating null results as precise falsification when the design lacks sensitivity.

# G. Independence disclosure

Please disclose whether you inspected:

- the CARS control protocol;
- the minimal assay specification;
- the measurement-boundary document;
- the red-team protocol;
- existing benchmark cases;
- prior assay results;
- historical catalyst/recursive-architecture material;
- related research repositories.

This does not automatically invalidate the contribution, but it changes the independence claim it can support.

# H. Output principle

The strongest independent case is one where competing scientific explanations produce discriminably different outcomes and where the benchmark can identify *which layer failed*.

For the current assay, the highest-value cases are those that can make:

```text
τ(i₁) > τ(i₀)
```

appear true when the target treatment-effect ordering is actually flat, opposite, or undefined under the claimed measurement equivalence.

# CARS Assay Evaluation Rubric

> **Scope:** current heterogeneous causal-responsiveness assay. This is separate from prompt-level CARS reasoning scoring and historical catalyst/architecture scoring.

Do not collapse these dimensions into one score before checking for failure localization.

## 1. Scientific-object fidelity

Does the analysis test the primitive proposition:

```text
i₁ > i₀
⇒
τ(i₁) > τ(i₀)
```

rather than silently replacing it with a preferred regression coefficient or semantic interpretation?

## 2. Pretreatment integrity

Was `I` measured before treatment assignment and protected from treatment contamination?

## 3. Causal identification

Was `E` randomized or otherwise identified under an explicit design?

Were positivity, attrition, missingness, and assignment deviations inspected?

## 4. Outcome-scale validity

Was the additive outcome scale justified for the causal contrast being estimated?

Were ceiling/floor effects, saturation, and nonlinear measurement artifacts checked?

## 5. Transformation-class discipline

Before invariance testing, was the admissible transformation class specified?

Expected:

```text
I: strictly increasing transforms preserve ordering
V: positive affine transforms preserve additive-CATE ordering
```

Do not penalize a changed result under a transformation that legitimately defines a different estimand.

## 6. Shape fidelity

Was monotonicity/ordering tested directly enough to distinguish:

```text
increasing
flat
decreasing
non-monotonic
```

without assuming linearity by default?

## 7. Estimator adequacy

Does the chosen estimator recover the intended object under simulation/known-truth controls?

If a linear interaction is used, is the linear specification adequately supported?

## 8. Sensitivity

Can the design distinguish zero from the smallest effect/order difference the experiment intends to detect?

A wide-uncertainty null should not be reported as precise falsification.

## 9. Headroom control

Can bounded measurement, baseline proximity to limits, or task difficulty manufacture the observed moderation?

## 10. Measurement-equivalence validation

For independent outcome instruments, was affine equivalence established on independent calibration data before treatment-effect analysis?

Was ordinary correlation kept separate from causal-estimand equivalence?

## 11. Residual causal disagreement

For linked instruments, was disagreement tested where the scientific claim lives?

Example:

```text
r = V^B - (aV^A+b)
r ~ I + E + I×E
```

A nonzero residual `I×E` term should be treated as a serious measurement disagreement.

## 12. Red-team survival

Did the assay survive or correctly classify:

- constant-effect worlds;
- ceiling/floor worlds;
- nonlinear outcome remeasurement;
- randomized baseline structure;
- broken-randomization controls;
- generic plasticity;
- affine positive controls;
- nonlinear `I` reparameterization;
- sensitivity attacks?

## 13. Specificity discipline

If stronger correction-capacity language is used, were warranted/neutral/misleading interventions tested separately?

Keep:

```text
responsiveness
≠
discriminative responsiveness
```

## 14. Scope / transport discipline

Are claims restricted to the tested intervention, measurement systems, horizon, domain, population, and benchmark generator?

## 15. Contradiction localization

When a discrepancy appears, does the analysis inspect lower-level loci before revising the scientific proposition?

Suggested order:

```text
causal identification
measurement
scientific-object identity
shape
estimator
implementation
substantive proposition
```

## Reporting

For each dimension, report:

- **pass** — requirement satisfied;
- **fail** — requirement violated;
- **changed estimand** — comparison no longer targets the same scientific object;
- **inconclusive** — insufficient evidence to classify;
- **N/A** — dimension not relevant.

A benchmark is not stronger merely because more dimensions are marked pass. A red-team failure that exposes a real boundary can be more informative than another confirming run.

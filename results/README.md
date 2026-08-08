# Results

No efficacy, recursive-improvement, or correction-capacity result is currently authorized.

Future result packages should record enough information to reconstruct what was tested and what information could have influenced the result.

## Prompt-level result package

Record:

- intervention version and hash;
- control prompt version and hash;
- model/version/date;
- task source and authorship;
- evaluator identity or evaluation method;
- scoring rule;
- excluded cases and reasons;
- per-dimension scores;
- substantive outcome metrics;
- cost metrics;
- protocol deviations;
- raw outputs where licensing/privacy permits.

## Architecture-level result package

In addition, record:

- exact definition of `X_t` used in the experiment;
- residual mapper `Φ_t` or equivalent procedure;
- observed residual representation `ρ_t`;
- candidate generator `G_t`;
- candidate set or selection trace where publishable;
- the full selection-information boundary `I_sel,t` as operationalized;
- validation procedure `𝒱_t`;
- validation environment `W_t^ind`;
- justification for `Ind_t = 1`, or an explicit downgrade if independence is partial/unknown;
- predeclared succession rule;
- residual-local `ΔCorrCap_{ρ_t}`;
- regression-control results and tolerance;
- whether validation evidence had been exposed to any earlier lineage step;
- benchmark generator and whether transfer crossed generators;
- component-level validation claims separately from system-level succession claims;
- architecture scoring dimensions from `eval/ARCHITECTURE_SCORING.md`;
- invalidation conditions encountered.

## Sequential lineage reporting

For repeated transitions

```text
X_0 → X_1 → … → X_T
```

record which validation environments were fresh at each step and when each became part of later selection history.

Do not describe a repeatedly inspected benchmark as held out for the lineage.

A lineage-level recursive-improvement claim requires more than a sequence of local wins. Report fresh-environment performance, cross-generator transfer, control regression, and any failed or rejected successors.

## Result classification

Classify each result as one of:

- **positive within scope**;
- **negative/null**;
- **mixed tradeoff**;
- **invalid/inconclusive**.

Invalid runs are not evidence for either efficacy or inefficacy.

Examples of invalidating conditions include:

- validation leakage;
- validator tuning after candidate selection without disclosure;
- adaptive holdout contamination;
- post-outcome threshold selection;
- broken scoring or construct validity;
- benchmark-generator leakage;
- protocol violations that change the claim being tested.

## Claim discipline

A positive result should state exactly what gained authority and within what scope.

Do not promote:

```text
task success
→ mechanism
→ representation validity
→ validator independence
→ correction-capacity improvement
→ recursive improvement
```

without separate evidence for each transition.
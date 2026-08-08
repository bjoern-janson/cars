# Results

No efficacy, catalyst-efficacy, recursive-improvement, or correction-capacity result is currently authorized.

Future result packages should record enough information to reconstruct **what was tested, what context was exposed, what information could have influenced selection, and what claim the result actually supports**.

## Result surfaces

Keep three result types distinct:

```text
prompt result
≠ catalyst result
≠ architecture result
```

A positive result on one surface does not automatically promote claims on another.

## Prompt-level result package

Record:

- exact intervention version and hash;
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

## Catalyst-level result package

For blind decoding or execution tests, record:

- exact catalyst text, byte-for-byte where practical;
- repository commit containing the tested catalyst;
- whether the condition used equation-only, semantics-only, full catalyst, older opaque notation, or a control;
- all context shown before the model response;
- model/version/date;
- decoding prompt or execution task prompt;
- whether CARS provenance, symbol legends, intended ontology labels, prior parses, or rubric language were withheld;
- decoding scores from `eval/CATALYST_SCORING.md`;
- execution scores where applicable;
- raw model interpretation/output;
- evaluator identity or scoring method;
- disagreements or ambiguous parses;
- token/latency/tool cost;
- protocol deviations.

Report separately:

```text
Decode
Execute
TaskPerf
CorrCap
```

Do not collapse these into a single “catalyst worked” statement.

A blind-decoding result can establish only semantic recovery within the tested model/protocol scope. An execution result is a separate claim.

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
- evidence for `(𝒱_t, W_t^ind) ⟂_design I_sel,t`, or an explicit downgrade if independence is partial/unknown;
- predeclared succession rule;
- residual-local `ΔCorrCap_{ρ_t}`;
- regression-control results and predeclared tolerance;
- whether validation evidence had been exposed to an earlier lineage step;
- benchmark generator and whether transfer crossed generators;
- component-level validation claims separately from system-level succession claims;
- architecture scoring dimensions from `eval/ARCHITECTURE_SCORING.md`;
- invalidation conditions encountered.

## Construct-validity reporting

If `CorrCap` is used, record its operational definition and the evidence that it is not merely tracking proxies such as verbosity, intervention count, abstention, search volume, or representation changes.

Keep explicit:

```text
C_improve ≠ CorrCap
```

A CorrCap result is evidence about the operational measure under the tested design. It does not automatically establish the full higher-level `C_improve` construct.

## Sequential lineage reporting

For repeated transitions

```text
X_0 → X_1 → … → X_T
```

record which validation environments were fresh at each step and when each became part of later selection history.

Do not describe a repeatedly inspected benchmark as held out for the lineage.

A lineage-level recursive-improvement claim requires more than a sequence of local wins. Report fresh-environment performance, cross-generator transfer, control regression, and failed or rejected successors.

## Result classification

Classify each result as one of:

- **positive within scope**;
- **negative/null**;
- **mixed tradeoff**;
- **invalid/inconclusive**.

Invalid runs are not evidence for either efficacy or inefficacy.

Examples of invalidating conditions include:

- catalyst legend/rubric leakage in a blind condition;
- validation leakage;
- validator tuning after candidate selection without disclosure;
- adaptive holdout contamination;
- post-outcome threshold selection;
- broken scoring or construct validity;
- benchmark-generator leakage;
- protocol violations that change the claim being tested.

## Claim discipline

A positive result should state exactly **what gained authority and within what scope**.

Do not promote:

```text
catalyst decoding
→ execution
→ task success
→ mechanism
→ representation validity
→ validator independence
→ CorrCap improvement
→ C_improve validation
→ recursive improvement
```

without separate evidence for each transition.
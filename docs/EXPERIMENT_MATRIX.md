# Experiment Matrix

CARS now has three experimentally distinct surfaces:

```text
prompt intervention
≠ catalyst intervention
≠ recursive architecture
```

A result on one surface does not automatically establish a result on another.

## 1. Prompt-level minimum experiment

| Condition | Intervention | Purpose |
|---|---|---|
| B0 | none | native model behavior |
| B1 | Generic Careful-Reasoning Control v0.1 | generic deliberation/control condition |
| C0 | CARS v0.1 | candidate structured intervention |

### Prompt-level ablations

| Condition | Change | Main question |
|---|---|---|
| A1 | remove representation-escalation gate | does the gate reduce over-escalation? |
| A2 | remove departure/adoption separation | does it reduce successor capture? |
| A3 | remove unresolved-state permission | does it prevent forced conclusions? |
| A4 | remove independence emphasis | does it improve common-mode evidence handling? |
| A5 | remove retest requirement | does it improve behavioral transfer? |
| A6 | remove belief/decision separation | does it help decisions under uncertainty? |
| A7 | invariants only | are compact principles sufficient? |

## 2. v0.2 dependency-tracing comparison

| Condition | Change | Main question |
|---|---|---|
| D0 | CARS v0.1 | no explicit dependency trace |
| D1 | CARS v0.2 candidate | does tracing distinguish load-bearing from incidental conditions? |
| D2 | v0.2 without substitution | does substitution testing add value beyond removal? |
| D3 | v0.2 on irrelevant tasks | does dependency tracing activate unnecessarily? |

Cases should include:

- present and necessary conditions;
- present but incidental conditions;
- redundant conditions;
- substitutable implementations;
- cases where no dependency analysis is needed.

## 3. Catalyst blind-decoding experiment

The frozen deployable catalyst is recorded in `notes/2026-08-08-catalyst-notation.md`.

The first catalyst question is not whether CARS works. It is whether the compact intervention is semantically recoverable without importing an unrelated ontology.

### Decoding conditions

| Condition | Intervention | Main question |
|---|---|---|
| K0 | no catalyst / neutral symbol task | what ontology does the model infer without intervention? |
| K1 | typed catalyst equation only | are the symbols sufficiently self-decoding? |
| K2 | execution semantics only | how much structure is carried by prose alone? |
| K3 | frozen deployable catalyst | does objective + typed equation + semantics recover the intended operation? |
| K4 | older opaque catalyst form | does semantic typing reduce ontology drift? |

Do not provide the CARS legend, repository provenance, expected ontology labels, or previous parses during blind decoding.

Measure with `eval/CATALYST_SCORING.md`:

- ontology recovery;
- relation recovery;
- ordering/process recovery;
- authority recovery;
- construct/metric separation where encoded;
- independence semantics.

### Catalyst execution conditions

After decoding is scored, compare:

| Condition | Intervention | Main question |
|---|---|---|
| E0 | no intervention | native correction behavior |
| E1 | generic careful reasoning | generic deliberation control |
| E2 | execution semantics only | does prose alone drive the behavior? |
| E3 | frozen deployable catalyst | does the full compact intervention improve controlled execution? |

Relevant task families should test:

- real limitation vs ordinary difficulty;
- provisional residual representation vs premature certainty;
- candidate generation vs immediate successor promotion;
- independent validation vs selection-contaminated validation;
- leave/adopt separation;
- downstream reuse of a valid correction.

A positive decoding result is not an efficacy result. A positive execution result is not automatically a `CorrCap` result.

## 4. Recursive correction architecture frontier

The formal recursive architecture should be tested separately from the catalyst and prompt intervention. A useful blind benchmark should vary the hidden failure locus without naming it to the system.

| World | Hidden structure | Successful behavior |
|---|---|---|
| R0 | shallow inference/model error | repair locally; do not escalate |
| R1 | observation/interface collapses required distinction | identify non-identifiability; seek a new partition or observation |
| R2 | residual mapper merges two mechanisms | revise `Φ_t` / recover the missing residual distinction |
| R3 | detailed representation uses wrong partition | change partition rather than merely adding detail |
| R4 | candidate generator shares incumbent blind spot | revise generation or obtain a new candidate source |
| R5 | validation environment is unseen but validator is selection-tuned | reject independence claim |
| R6 | validator and validation environment are design-insulated | permit validation evidence to bear succession weight |
| R7 | apparent dependency is incidental | remove without damaging correction |
| R8 | implementation is substitutable | migrate preservation claim toward tested function, within scope |
| R9 | correction procedure itself is limiting | propose a procedural successor without self-authorizing it |
| R10 | no deeper failure exists | preserve current correction architecture |
| R11 | successor fixes residual but damages controls | reject or scope adoption according to predeclared regression rule |
| R12 | repeated validation set has entered lineage history | detect adaptive holdout contamination |
| R13 | new benchmark generator changes hidden structure | test cross-generator transfer |

## Architecture-level comparison conditions

At minimum compare:

| Condition | Description |
|---|---|
| X0 | native model / no explicit correction architecture |
| X1 | fixed correction discipline |
| X2 | revisable residual mapping but fixed validator |
| X3 | revisable residual mapping and validation procedure |
| X4 | full succession gate with design-independent validation requirement |

These are experiment-design placeholders, not claims that each condition is already implemented.

## Prompt-level analysis

At minimum compare:

- substantive task success;
- over-update rate;
- missed-update rate;
- premature representation-escalation rate;
- premature successor-adoption rate;
- unjustified unresolved rate;
- common-mode evidence errors;
- correction transfer;
- token/latency/search cost.

If CARS beats B0 but not B1, generic deliberation is a stronger explanation than a CARS-specific mechanism.

If CARS beats B1 only on internally authored tasks, external transfer remains unresolved.

## Catalyst-level analysis

Report separately:

```text
Decode
Execute
TaskPerf
```

Do not collapse them into one score before checking for dissociation.

Important failure patterns include:

```text
high relation recovery + low ontology recovery
high decoding + low execution
high execution fidelity + no task gain
high task gain + no evidence of CorrCap gain
```

These are diagnostically different outcomes.

## Architecture-level analysis

Track at least:

- true limitation detection;
- false limitation / false escalation rate;
- localization adequacy;
- residual-mapping accuracy or usefulness;
- recovery of unsupplied distinctions;
- candidate-generation quality;
- candidate-selection leakage;
- validator-design independence;
- residual-local `ΔCorrCap`;
- control regression;
- substitution discovery;
- cross-instance transfer;
- cross-generator transfer;
- cost.

Do not assume a single scalar captures all of these.

## CorrCap construct-validity controls

`C_improve` and `CorrCap` are not assumed identical.

Challenge a candidate correction-capacity metric with agents or conditions that artificially increase:

- reasoning length;
- number of proposed interventions;
- abstention;
- representation changes;
- uncertainty language;
- search volume.

A sound metric should not reward these behaviors unless they improve actual correction outcomes.

Include matched worlds where the correct action is **not** to revise.

## Sequential evaluation

For recursive succession, use renewable independence:

```text
W_dev → W_val,1 → W_val,2 → … → W_audit
```

Once a validation environment is exposed, treat it as part of later lineage history. Do not repeatedly call the same benchmark held out.

Where possible, reserve independently authored or externally generated worlds for final audit.

## Interpretation rule

A positive result should be scoped to the exact intervention, model family, task distribution, selection-information boundary, validator design, validation generators, and regression tolerance actually tested.

In particular:

```text
catalyst decoding
↛ catalyst efficacy
↛ CorrCap improvement
↛ recursive improvement
```

Repeated local succession does not by itself establish universal recursive improvement.
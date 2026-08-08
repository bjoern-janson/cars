# Provenance and Research Workflow

## Research direction

CARS is directed by **Björn Janson** as part of an independent research program on adaptive reasoning, representation failure, correction, dependency, and epistemic governance.

## AI-assisted workflow

AI systems are used as research collaborators and development tools. Depending on the artifact, assistance may include:

- drafting and restructuring prose;
- adversarial critique;
- generating counterexamples;
- comparing alternative formulations;
- repository construction;
- code scaffolding;
- documentation;
- benchmark-case generation;
- consistency checks;
- formalization of candidate architectures and evaluation criteria;
- notation design and blind-decoding diagnostics.

The use of AI assistance is not hidden and should not be confused with independent validation.

## Authority boundary

AI-generated suggestions, implementations, benchmark cases, formal notation, critiques, or mutually agreeing model interpretations acquire no scientific authority merely because they are coherent, executable, or convergent.

Research claims require evaluation under explicit protocols, ideally including independently authored tasks, design-independent validation, fresh evaluation environments, and independent replication where feasible.

## Current artifact lineage

The following were developed within the same broader AI-assisted research workflow:

- CARS prompt variants;
- design rationale and claims documents;
- seed benchmark;
- typed-attribution and representation-authority notes;
- recursive correction architecture;
- catalyst notation and execution semantics;
- current evaluation scaffolding.

They should therefore be treated as **internally generated research artifacts**, not independent evidence for one another.

In particular:

- convergence among notebook notes does not validate the architecture;
- the seed cases do not validate the prompt that helped motivate their design;
- the recursive architecture does not validate CARS v0.1 or v0.2;
- the catalyst does not validate the formal architecture it compresses;
- the formal architecture does not validate the catalyst's efficacy;
- internally generated validators or benchmark worlds are not independent merely because they are stored in separate files;
- AI critique inside the same workflow is adversarial development input, not independent replication.

## Catalyst diagnostics

Blind or semi-blind parses by external model systems can be useful **development diagnostics** for semantic recoverability.

A parse that reveals ontology drift can motivate a catalyst revision. However:

- one model parse is not a validated estimate of `DecodeAcc`;
- agreement among several related models is not automatically independent evidence;
- exposing prior parses to later models contaminates a blind-decoding condition;
- a successful parse establishes semantic recovery only within the tested context, not correction efficacy.

For reported catalyst experiments, preserve the exact tested catalyst string and the full context shown to the model.

## Selection-information boundary

For architecture-level experiments, provenance should record what information could have influenced candidate generation or selection.

Let:

```text
I_sel,t := all information capable of influencing candidate generation or selection
```

A strong independence claim requires design insulation of both the validation procedure and validation environment:

```text
(𝒱_t, W_t^ind) ⟂_design I_sel,t
```

If information from a benchmark, validator, critique, prior model parse, or earlier result could have changed the selected revision, that information belongs to the relevant selection history and cannot later be counted as independent validation evidence for the same succession claim.

## Sequential provenance

Validation evidence can change status over time.

A world may be fresh for transition `t`, then become part of the lineage's effective information history once its outcome is observed.

For repeated succession, record:

- when each validation environment was first exposed;
- what revisions occurred after exposure;
- which benchmark generators were reused;
- which audit cases remained unavailable to the lineage.

Renewable independence requires renewable provenance tracking.

## Construct / metric provenance

The broader framing distinguishes:

```text
C_improve ≠ CorrCap
```

`C_improve` is the higher-level candidate construct. `CorrCap` is an operational measurement target.

A CorrCap definition developed within the same theoretical workflow does not acquire construct validity by provenance alone. It must survive empirical tests against proxy capture and metric gaming.

## Future evidence

Stronger evidence should increase independence along dimensions such as:

- case authorship;
- benchmark generator;
- validation design;
- validation environment;
- model family;
- implementation;
- evaluator;
- replication team.

Independence is not binary by default. Claims should state which dimensions were actually separated and which remain shared.
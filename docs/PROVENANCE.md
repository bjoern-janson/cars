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
- formalization of candidate architectures and evaluation criteria.

The use of AI assistance is not hidden and should not be confused with independent validation.

## Authority boundary

AI-generated suggestions, implementations, benchmark cases, formal notation, or critiques acquire no scientific authority merely because they are coherent, executable, or mutually reinforcing.

Research claims require evaluation under explicit protocols, ideally including independently authored tasks, design-independent validation, fresh evaluation environments, and independent replication where feasible.

## Current independence status

The initial repository, prompt variants, design rationale, seed benchmark, and current recursive correction architecture were developed within the same AI-assisted research workflow.

They should therefore be treated as **internally generated research artifacts**, not independent evidence for one another.

In particular:

- the convergence of multiple notebook notes does not validate the architecture;
- the seed cases do not validate the prompt that helped motivate their design;
- the recursive architecture does not validate CARS v0.1 or v0.2;
- internally generated validators or benchmark worlds are not independent merely because they are stored in separate files;
- AI critique inside the same workflow is adversarial development input, not independent replication.

## Selection-information boundary

For architecture-level experiments, provenance should record what information could have influenced candidate generation or selection.

If information from a benchmark, validator, critique, or earlier result could have changed the selected revision, that information belongs to the relevant selection history and cannot later be counted as independent validation evidence for the same succession claim.

## Future evidence

Stronger evidence should increase independence along dimensions such as:

- case authorship;
- benchmark generator;
- validation design;
- validation environment;
- model family;
- implementation;
- replication team.

Independence is not binary by default. Claims should state which dimensions were actually separated and which remain shared.
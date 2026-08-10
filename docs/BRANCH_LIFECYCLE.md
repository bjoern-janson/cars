# Branch Lifecycle and Prune Ledger

## Status

**Repository hygiene record.** This document classifies branch refs; it does not alter scientific results or merge research lineages.

Canonical rule:

```text
main                    = canonical repository state
open research PR branch = live until explicitly closed/merged
closed PR               = historical provenance
branch ref               = disposable once its unique role is preserved
```

Deleting a branch ref must never be used to erase a negative result, provenance-bearing PR, or unresolved scientific state.

## Prune states

| State | Meaning |
| --- | --- |
| `KEEP` | Canonical or live branch. Do not prune. |
| `PRUNE_READY` | Content is already represented or superseded on `main`; branch ref is no longer needed. |
| `PRUNE_AFTER_CLOSE` | Unique historical content is preserved by its PR; close the PR first, then the branch ref may be deleted. |
| `PRUNE_AFTER_LEDGER` | Abandoned/superseded branch with no PR; retain until this ledger is merged so its head SHA and disposition are canonical. |

## Current inventory

| Branch | PR | Head / anchor | Classification | Disposition |
| --- | ---: | --- | --- | --- |
| `main` | — | canonical | `KEEP` | Canonical branch. |
| `agent/asi0-evidence-assignment` | #11 | `492a8cc7265d75f6c209a115fbaa5da364d61c17` | `KEEP` | Live draft research branch. ASI-0 primary is negative/STOP, but the branch contains the authoritative unmerged ASI-0 contract, execution lineage, and mechanism-diagnosis artifacts. Do not merge or prune without an explicit decision. |
| `agent/asi0-build-contract` | — | `f3bc758a2c619ff25a966d0e998421ab83d481ce` | `PRUNE_AFTER_LEDGER` | Abandoned pre–evidence-assignment ASI-0 build design. It diverged from `main` by 14 commits and introduced the obsolete `asi/` build-contract/capability-ladder path. Superseded scientifically by the evidence-assignment ASI-0 lineage; do not revive as a null rescue. |
| `agent/future-plasticity-forecast-benchmark` | — | historical benchmark ref | `PRUNE_READY` | Current future-plasticity contract/config/runner/status are present on `main`; the branch is a superseded construction ref, not the canonical benchmark state. |
| `agent/pilot1-predictive-resource-toy` | — | `7e3b45ae2c489080fc8e1d968337a09ddc755c5c` | `PRUNE_READY` | Branch head is an ancestor of `main`; Pilot-1 predictive-resource records are canonical on `main`. |
| `agent/pilot1-system-identification-toy` | — | `8a6f88a698cc6f2ce990dfcdfd72c4e65b736e2b` | `PRUNE_READY` | Branch head is an ancestor of `main`; ID1 closure/replication records are canonical on `main`. |
| `agent/pilot0-decision-trace` | #2 | `1c8ad566aad9a65031128e91fb4a0298def84cd4` | `PRUNE_AFTER_CLOSE` | Historical reconstruction only. Unique PR delta is `docs/PILOT0_DECISION_TRACE.md`. Current program no longer pursues controller reconstruction from this branch. |
| `agent/pilot0-human-judgment-audit` | #3 | `d8d5e98fdd83a031958c645a39a2ad806a23a28b` | `PRUNE_AFTER_CLOSE` | Historical component audit. Unique PR delta is `docs/PILOT0_HUMAN_JUDGMENT_AUDIT.md`. |
| `agent/pilot0-abstraction-gate` | #4 | `bd451390dd6125b1d6557d501b8c08444bf3419f` | `PRUNE_AFTER_CLOSE` | Historical abstraction gate. Unique PR delta is `docs/PILOT0_ABSTRACTION_GATE.md`; consequential action-selection primitive was not earned. |
| `agent/pilot0-c2-primitive-assessment` | #5 | `f3b7198da3203500ed96ff40aeb895e5e88f16eb` | `PRUNE_AFTER_CLOSE` | Dead-end C2 promotion branch. Unique PR delta is `docs/PILOT0_C2_PRIMITIVE_ASSESSMENT.md`; later work deliberately did not inherit this candidate-primitive path. |
| `agent/correction-transition-invariants` | #6 | `15ab404524ca0bdc1fe69549a7602ff60301ef19` | `PRUNE_AFTER_CLOSE` | Historical pressure test. Unique PR delta is `docs/CORRECTION_TRANSITION_INVARIANTS.md`; broad transition-audit framing was not novel by itself and the local invariant set was insufficient. |
| `agent/correction-construct-differentiation` | #7 | `aba0c7248a0b92ae008cc261a2913b8ac0ea940b` | `PRUNE_AFTER_CLOSE` | Historical construct null-space audit. Unique PR delta is `docs/CORRECTION_CONSTRUCT_DIFFERENTIATION.md`; no distinct construct was established. |
| `agent/correction-residual-adversarial-cases` | #8 | `6db5fe0d20cb11254f33139715ccf1956b4508f0` | `PRUNE_AFTER_CLOSE` | Historical destructive casebook. Unique PR delta is `docs/CORRECTION_RESIDUAL_ADVERSARIAL_CASES.md`; a clean history-only residual was not found. |
| `agent/correction-state-sufficiency-audit` | #9 | `1be87de5d5b8e61c1213c39635fe0c9c81d1c7e3` | `PRUNE_AFTER_CLOSE` | Historical sufficiency audit. Unique PR delta is `docs/CORRECTION_STATE_SUFFICIENCY_AUDIT.md`; correction-state sufficiency was not earned as a distinct construct. |
| `agent/correction-target-discovery-differentiation` | #10 | `eb01f630fb0b26e16b3306e5c1139fc6e364ab1b` | `PRUNE_AFTER_CLOSE` | Historical target-discovery subtraction. Unique PR delta is `docs/CORRECTION_TARGET_DISCOVERY_DIFFERENTIATION.md`; correction-specific target discovery was not earned as a distinct scientific object. |

## Historical stacked PR chain

PRs #2–#10 are provenance, not an active merge queue:

```text
#2 decision trace
 ↓
#3 human-judgment audit
 ↓
#4 abstraction gate
 ├─→ #5 C2 candidate-primitive dead end
 └─→ #6 transition-quality pressure test
      ↓
     #7 construct differentiation
      ↓
     #8 residual adversarial cases
      ↓
     #9 state-sufficiency audit
      ↓
    #10 target-discovery differentiation
      ↓
current canonical subtraction summary on main
```

Each PR changes exactly one conceptual document relative to its declared base. Their scientific outcomes are already summarized canonically in `README.md` and `docs/CURRENT_RESEARCH_STATE.md`. The PRs themselves retain the detailed historical argument and diff.

## Pruning protocol

1. Merge this hygiene ledger into `main` before deleting any no-PR historical branch whose only canonical pointer is recorded here.
2. Close PRs #2–#10 as **historical / superseded**, without merging them into the canonical research tree.
3. After those PRs are closed, delete their branch refs. The closed PRs remain the detailed provenance objects.
4. Delete `agent/pilot1-predictive-resource-toy`, `agent/pilot1-system-identification-toy`, and `agent/future-plasticity-forecast-benchmark`; their current authoritative content is on `main`.
5. Delete `agent/asi0-build-contract` only after this ledger is on `main`. Its branch is intentionally discarded rather than merged because its scientific design was superseded before the canonical ASI-0 experiment.
6. Keep `agent/asi0-evidence-assignment` / PR #11 until an explicit merge-or-archive decision is made. This cleanup does not authorize merging PR #11.
7. Re-run branch inventory after pruning. Expected long-lived refs after the current cleanup are `main`, `agent/asi0-evidence-assignment`, and any explicitly active hygiene branch until its PR is merged.

## Branch creation rule going forward

New research branches should satisfy all of the following:

- one scientific or repository-maintenance object per branch;
- a PR is opened when the branch becomes provenance-bearing;
- terminal negative/superseded branches are closed rather than left in the active PR queue;
- canonical conclusions are summarized on `main`; detailed historical arguments may remain in closed PRs;
- branch refs are deleted after merge or archival once no unique live authority depends on the ref;
- stacked PRs are temporary dependency structures, not permanent research indexes.

The repository should use documents and closed PRs for provenance, not an ever-growing set of remote branch refs.

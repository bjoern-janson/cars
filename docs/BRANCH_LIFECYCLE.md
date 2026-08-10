# Branch Lifecycle and Prune Ledger

## Status

**Repository hygiene record.** This file classifies branch refs; it does not alter scientific results or merge research lineages.

```text
main                    = canonical repository state
open research PR branch = live until explicitly closed/merged
closed PR               = historical provenance
temporary branch ref    = disposable once its unique role is preserved
```

Deleting a branch ref must never be used to erase a negative result, provenance-bearing PR, or unresolved scientific state.

## States

| State | Meaning |
| --- | --- |
| `KEEP` | Canonical or live branch. Do not prune. |
| `PRUNE_READY` | Scientific/provenance role is already preserved; branch ref may be deleted. |
| `PRUNE_AFTER_LEDGER` | Delete only after this ledger is merged into `main`. |

## Current inventory

| Branch | PR | Anchor | State | Disposition |
| --- | ---: | --- | --- | --- |
| `main` | — | canonical | `KEEP` | Canonical branch. |
| `agent/asi0-evidence-assignment` | #11 | `492a8cc7265d75f6c209a115fbaa5da364d61c17` | `KEEP` | Live draft branch containing the unmerged ASI-0 contract/execution/mechanism-diagnosis lineage. This hygiene pass does **not** authorize merge or prune. |
| `agent/repo-hygiene-prune-prep` | #12 | hygiene PR | `PRUNE_AFTER_LEDGER` | Temporary maintenance branch; delete after PR #12 lands. |
| `agent/asi0-build-contract` | — | `f3bc758a2c619ff25a966d0e998421ab83d481ce` | `PRUNE_AFTER_LEDGER` | Abandoned 14-commit pre–evidence-assignment ASI-0 design (`asi/` build-contract/capability-ladder path). Scientifically superseded before canonical ASI-0; intentionally discard rather than merge. |
| `agent/future-plasticity-forecast-benchmark` | — | historical benchmark ref | `PRUNE_READY` | Current benchmark contract/config/runner/status are on `main`; this ref is superseded construction history. |
| `agent/pilot1-predictive-resource-toy` | — | `7e3b45ae2c489080fc8e1d968337a09ddc755c5c` | `PRUNE_READY` | Head is an ancestor of `main`; canonical Pilot-1 records are on `main`. |
| `agent/pilot1-system-identification-toy` | — | `8a6f88a698cc6f2ce990dfcdfd72c4e65b736e2b` | `PRUNE_READY` | Head is an ancestor of `main`; canonical ID1 records are on `main`. |
| `agent/pilot0-decision-trace` | #2 closed | `1c8ad566aad9a65031128e91fb4a0298def84cd4` | `PRUNE_AFTER_LEDGER` | Historical reconstruction. Unique PR delta: `docs/PILOT0_DECISION_TRACE.md`. |
| `agent/pilot0-human-judgment-audit` | #3 closed | `d8d5e98fdd83a031958c645a39a2ad806a23a28b` | `PRUNE_AFTER_LEDGER` | Historical audit. Unique PR delta: `docs/PILOT0_HUMAN_JUDGMENT_AUDIT.md`. |
| `agent/pilot0-abstraction-gate` | #4 closed | `bd451390dd6125b1d6557d501b8c08444bf3419f` | `PRUNE_AFTER_LEDGER` | Historical abstraction gate; consequential action-selection primitive not earned. |
| `agent/pilot0-c2-primitive-assessment` | #5 closed | `f3b7198da3203500ed96ff40aeb895e5e88f16eb` | `PRUNE_AFTER_LEDGER` | Dead-end C2 promotion branch; later lineage deliberately did not inherit it. |
| `agent/correction-transition-invariants` | #6 closed | `15ab404524ca0bdc1fe69549a7602ff60301ef19` | `PRUNE_AFTER_LEDGER` | Historical pressure test; broad transition-audit framing not novel by itself. |
| `agent/correction-construct-differentiation` | #7 closed | `aba0c7248a0b92ae008cc261a2913b8ac0ea940b` | `PRUNE_AFTER_LEDGER` | Historical construct null-space audit; no distinct construct established. |
| `agent/correction-residual-adversarial-cases` | #8 closed | `6db5fe0d20cb11254f33139715ccf1956b4508f0` | `PRUNE_AFTER_LEDGER` | Historical destructive casebook; clean history-only residual not found. |
| `agent/correction-state-sufficiency-audit` | #9 closed | `1be87de5d5b8e61c1213c39635fe0c9c81d1c7e3` | `PRUNE_AFTER_LEDGER` | Historical sufficiency audit; distinct correction-state sufficiency not earned. |
| `agent/correction-target-discovery-differentiation` | #10 closed | `eb01f630fb0b26e16b3306e5c1139fc6e364ab1b` | `PRUNE_AFTER_LEDGER` | Historical target-discovery subtraction; distinct correction-specific target discovery not earned. |

## Historical stacked PR chain

PRs #2–#10 are now **closed and unmerged**. They are provenance, not an active merge queue:

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
canonical subtraction summary on main
```

Each PR changes exactly one conceptual document relative to its declared base. `README.md` and `docs/CURRENT_RESEARCH_STATE.md` contain the canonical current conclusion; the closed PRs retain the detailed historical arguments and diffs.

## Pruning protocol

After PR #12 is merged into `main`:

1. delete branch refs behind closed PRs #2–#10;
2. delete `agent/pilot1-predictive-resource-toy`;
3. delete `agent/pilot1-system-identification-toy`;
4. delete `agent/future-plasticity-forecast-benchmark`;
5. delete obsolete `agent/asi0-build-contract`;
6. delete `agent/repo-hygiene-prune-prep` after merge;
7. retain `main` and `agent/asi0-evidence-assignment` unless a separate explicit decision changes PR #11.

Expected long-lived branch count after this pass: **2**.

## Rule going forward

- one scientific or maintenance object per branch;
- open a PR once a branch becomes provenance-bearing;
- close terminal negative/superseded PRs instead of leaving them in the active queue;
- summarize canonical conclusions on `main`;
- use closed PRs/documents for historical provenance, not permanent remote branch refs;
- delete merged/archived branch refs once no unique live authority depends on them;
- treat stacked PR topology as temporary dependency structure, not a research index.

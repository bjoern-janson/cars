# Branch Lifecycle and Prune Ledger

## Status

**Repository hygiene record.** This file classifies branch refs; it does not alter scientific results or merge research lineages.

```text
main                    = canonical repository state
open research PR branch = live until explicitly closed/merged
closed/merged PR         = preserved provenance
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

| Branch | PR | State | Disposition |
| --- | ---: | --- | --- |
| `main` | — | `KEEP` | Canonical branch. ASI-0 terminal result is now merged. |
| `agent/asi0-evidence-assignment` | #11 merged | `PRUNE_AFTER_LEDGER` | Complete ASI-0 lineage is preserved on `main` and in merged PR #11. Delete after this ledger lands. |
| `agent/repo-hygiene-prune-prep` | #12 | `PRUNE_AFTER_LEDGER` | Temporary maintenance branch; delete after PR #12 lands. |
| `agent/asi0-closeout-docs` | — | `PRUNE_AFTER_LEDGER` | Accidental temporary fork created during closeout; contains no unique authority beyond merged PR #11. Delete. |
| `agent/asi0-build-contract` | — | `PRUNE_AFTER_LEDGER` | Abandoned pre–evidence-assignment ASI-0 design. Scientifically superseded before the canonical experiment; intentionally discard rather than merge. |
| `agent/future-plasticity-forecast-benchmark` | — | `PRUNE_READY` | Current benchmark contract/config/runner/status are on `main`; ref is superseded construction history. |
| `agent/pilot1-predictive-resource-toy` | — | `PRUNE_READY` | Head is an ancestor of `main`; canonical Pilot-1 records are on `main`. |
| `agent/pilot1-system-identification-toy` | — | `PRUNE_READY` | Head is an ancestor of `main`; canonical ID1 records are on `main`. |
| `agent/pilot0-decision-trace` | #2 closed | `PRUNE_AFTER_LEDGER` | Historical reconstruction; closed PR preserves unique conceptual delta. |
| `agent/pilot0-human-judgment-audit` | #3 closed | `PRUNE_AFTER_LEDGER` | Historical audit; closed PR preserves unique conceptual delta. |
| `agent/pilot0-abstraction-gate` | #4 closed | `PRUNE_AFTER_LEDGER` | Historical abstraction gate; closed PR preserves provenance. |
| `agent/pilot0-c2-primitive-assessment` | #5 closed | `PRUNE_AFTER_LEDGER` | Dead-end C2 promotion branch; later lineage deliberately did not inherit it. |
| `agent/correction-transition-invariants` | #6 closed | `PRUNE_AFTER_LEDGER` | Historical pressure test; broad transition-audit framing not novel by itself. |
| `agent/correction-construct-differentiation` | #7 closed | `PRUNE_AFTER_LEDGER` | Historical construct null-space audit; no distinct construct established. |
| `agent/correction-residual-adversarial-cases` | #8 closed | `PRUNE_AFTER_LEDGER` | Historical destructive casebook; clean history-only residual not found. |
| `agent/correction-state-sufficiency-audit` | #9 closed | `PRUNE_AFTER_LEDGER` | Historical sufficiency audit; distinct correction-state sufficiency not earned. |
| `agent/correction-target-discovery-differentiation` | #10 closed | `PRUNE_AFTER_LEDGER` | Historical target-discovery subtraction; distinct correction-specific target discovery not earned. |

## Historical PR state

PRs #2–#10 are closed and unmerged historical provenance. PR #11 is merged and preserves the full ASI-0 causal contract, execution-repair lineage, canonical negative primary, and mechanism diagnosis.

Current open-PR target after PR #12 lands:

```text
none
```

unless a genuinely new scientific or maintenance object is opened prospectively.

## Pruning protocol

After PR #12 is merged into `main`, delete every `agent/*` ref listed above as `PRUNE_READY` or `PRUNE_AFTER_LEDGER`.

Expected long-lived remote branch count after this pass:

```text
1
```

namely:

```text
main
```

## Rule going forward

- one scientific or maintenance object per branch;
- open a PR once a branch becomes provenance-bearing;
- merge terminal scientific lineages only after canonical result/authority docs are reconciled;
- close superseded conceptual PRs instead of leaving them in the active queue;
- summarize canonical conclusions on `main`;
- use merged/closed PRs and committed terminal records for provenance, not permanent remote branch refs;
- delete merged/archived branch refs once no unique live authority depends on them;
- treat stacked PR topology as temporary dependency structure, not a research index.

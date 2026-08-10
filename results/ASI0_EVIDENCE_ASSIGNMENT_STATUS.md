# ASI-0 Evidence-Assignment Status

## Terminal state

**CLOSED / IMMUTABLE**

```text
DESIGN                         FROZEN
CANONICAL MODEL                Qwen/Qwen2.5-0.5B-Instruct @ 7ae5576
BOOLEAN DOMAIN REPAIR          PASS / FROZEN
CPU↔GPU BEHAVIORAL GATE        PASS
CANONICAL ATTEMPT #1           UNOBSERVED / NO SCIENTIFIC OUTCOME
CANONICAL ATTEMPT #2           SCIENTIFIC RESULT
PRIMARY                        STOP
REPLICATION                    NOT AUTHORIZED
ASI-0 GREEN                    FALSE
```

## Frozen scientific object

ASI-0 tests a bounded causal-attribution question under a fixed-base-model textual-policy mutation surface.

Primary two-axis object:

\[
C=E[Y_{aligned}-Y_{base}]
\]

\[
A=E[Y_{aligned}-Y_{misaligned}]
\]

The positive gate was prospectively conjunctive:

\[
L_C>0\land L_A>0.
\]

## Canonical primary result

```text
n_targets                         16
mean_base_score                   0.20833333333333331
mean_aligned_score                0.20833333333333331
mean_misaligned_score             0.20833333333333331
mean_random_edit_score            0.20833333333333331
aligned_valid_selection_rate      0.875
misaligned_valid_selection_rate   0.875
aligned_regression_gate_pass      0.0
misaligned_regression_gate_pass   0.0

C                                  0.0
A                                  0.0
L_C                                0.0
L_A                                0.0
joint_gate                         false
classification                     STOP
```

Therefore:

\[
\boxed{C=0,\quad A=0,\quad \mathrm{STOP}}
\]

Replication was not authorized by the frozen contract.

## Mechanism diagnosis

Outcome-blind post-hoc diagnosis used selection identity and the frozen protected-regression cache only.

```text
valid aligned selections                 14/16
valid misaligned selections              14/16
admitted aligned candidates               0/16
admitted misaligned candidates            0/16
admitted | valid aligned                   0/14
admitted | valid misaligned                0/14

complete candidate pool                   16
candidate patches preserving base gate      1
pool pass rate                            1/16
```

Keep pool and realized-arm claims separate:

```text
15/16 frozen candidate patches failed baseline protected-behavior preservation.
All 28 valid selected patches were rejected.
```

Every valid selected patch newly failed the exact-token `PINE` regression relative to base.

Current localization:

```text
INFERENCE
→ assigned evidence weakly controlled candidate identity

MECHANISM / ISOLATION
→ textual policy patches usually interfered with protected behavior

ACCEPTANCE
→ functioning as designed; rejected interfering patches
```

## Authority boundary

Earned claim:

> Under the frozen proposal + protected-acceptance policy, correctly assigned development evidence produced no concealed capability gain and no incremental outcome leverage relative to misaligned assignment.

Not earned:

```text
evidence alignment is intrinsically useless
Qwen cannot identify useful candidate policies
candidate selection was completely broken
protected patches would have no effect absent the gate
general intelligence / viability / RSI / ASI conclusions
```

## Canonical records

- [`ASI0_TERMINAL_RECORD.md`](ASI0_TERMINAL_RECORD.md)
- [`ASI0_PRIMARY_MECHANISM_FAILURE_REPORT.md`](ASI0_PRIMARY_MECHANISM_FAILURE_REPORT.md)
- [`../experiments/ASI0_EVIDENCE_ASSIGNMENT.md`](../experiments/ASI0_EVIDENCE_ASSIGNMENT.md)
- [`../experiments/ASI0_BOOLEAN_TRIPLE_REPAIR.md`](../experiments/ASI0_BOOLEAN_TRIPLE_REPAIR.md)
- [`../experiments/ASI0_PRIMARY_MECHANISM_DIAGNOSIS_PROTOCOL.md`](../experiments/ASI0_PRIMARY_MECHANISM_DIAGNOSIS_PROTOCOL.md)

## Descendant boundary

ASI-0 is not to be repaired until positive. Any future experiment is a new prospective object.

Provisional descendant architecture only:

\[
E\rightarrow C_{selected}\rightarrow M_{effective}\rightarrow(Y_T,Y_P)
\]

with direct independent modification identification:

\[
do(M=m)\rightarrow(Y_T,Y_P).
\]

No descendant model, benchmark, prompt, or empirical execution is currently authorized.

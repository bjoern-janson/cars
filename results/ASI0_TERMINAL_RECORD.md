# ASI-0 Terminal Record

## Status

**CLOSED / IMMUTABLE SCIENTIFIC RESULT**

ASI-0 is not open for repair, rerun, stronger-substrate rescue, prompt relaxation, gate relaxation, or retrospective reinterpretation.

```text
PRIMARY      STOP
REPLICATION  NOT AUTHORIZED
ASI-0 GREEN  FALSE
```

## Canonical scientific observation

Model:

```text
Qwen/Qwen2.5-0.5B-Instruct
revision 7ae5576
weights frozen
selection and execution use the same model
```

Frozen primary result:

```text
n_targets                    16
mean_base_score              0.20833333333333331
mean_aligned_score           0.20833333333333331
mean_misaligned_score        0.20833333333333331
mean_random_edit_score       0.20833333333333331
aligned_valid_selection      14/16 = 0.875
misaligned_valid_selection   14/16 = 0.875
aligned_regression_gate      0/16
misaligned_regression_gate   0/16
```

Frozen two-axis estimands:

\[
C=E[Y_{aligned}-Y_{base}]=0
\]

\[
A=E[Y_{aligned}-Y_{misaligned}]=0
\]

Inference:

```text
C    0.0
A    0.0
L_C  0.0
L_A  0.0
joint gate: FALSE
```

Therefore:

\[
\boxed{C=0,\quad A=0,\quad \mathrm{STOP}}
\]

The primary intersection-union alternative

\[
C>0\land A>0
\]

was not established.

## Execution lineage

Canonical attempt #1 produced no scientific outcome because the original `boolean_pair` family could not satisfy the globally unique 3-development + 3-concealed prompt requirement over a four-point Boolean domain.

That attempt remains:

```text
Y = UNOBSERVED
```

and is not a negative result or replicate.

The Boolean input-domain layer was reopened prospectively and repaired as:

```text
boolean_pair -> boolean_triple
```

with an eight-point domain and the frozen operations AND, OR, XOR odd parity, and XNOR even parity. The repair passed its prospective cardinality, signature, identifying-subset, frozen-seed, and non-change checks.

Before canonical attempt #2, the exact canonical CUDA execution path passed the frozen CPU↔GPU behavioral-equivalence gate on all eight diagnostic cases using manifest hash:

```text
32b889e5c8044ab6f054c4b14f0f180380f18caaec24bd21364e0ae59b3c16fb
```

Final-path diagnostic result:

```text
behavioral_equivalence_pass  true
device                       cuda
n_cases                      8
scientific_result            false
```

Canonical attempt #2 was therefore the first outcome-bearing scientific run.

## Why the realized arms collapsed to no-op

The frozen policy applied a selected textual patch only if its protected-regression result passed the deterministic acceptance gate. Otherwise the effective system remained the base system.

Observed:

```text
aligned protected-gate admissions     0/16
misaligned protected-gate admissions  0/16
```

Hence no aligned or misaligned selected patch was deployed, so the policy-level ITT arms collapsed to base/no-op and mechanically produced:

\[
Y_{aligned}=Y_{base},\qquad Y_{misaligned}=Y_{base}.
\]

This is the prospectively frozen policy-level ITT object, not an estimator defect.

## Earned claim

Under the frozen proposal + protected-acceptance policy, correctly assigned development evidence produced no concealed capability gain and no incremental outcome leverage relative to misaligned assignment.

## Nonclaims

ASI-0 does **not** establish that:

- evidence alignment is intrinsically useless;
- Qwen cannot identify useful candidate policies;
- candidate selection was completely broken;
- protected patches would have no effect absent the frozen gate;
- general intelligence, viability, recursive self-improvement, general superhumanity, or ASI were tested.

## Post-outcome mechanism diagnosis

The outcome-blind mechanism diagnosis uses candidate selection identity and the frozen protected-regression cache only. Concealed performance is not used to label candidate mechanisms.

Key results:

```text
complete frozen candidate pool          16
candidate patches passing gate           1
pool gate-pass rate                    1/16 = 0.0625
base regression score                  0.75
base failed probe                      larger_7_vs_3

P(admitted | aligned)                  0/16
P(admitted | misaligned)               0/16
P(admitted | valid, aligned)           0/14
P(admitted | valid, misaligned)        0/14
```

The correct distinction is:

```text
pool property:
15/16 frozen candidate patches failed to preserve baseline protected behavior

realized-arm property:
all 28 valid selected patches were rejected
```

Every valid selected patch newly failed the exact-token `PINE` protected regression:

\[
P(\text{new PINE failure}\mid\text{valid selected patch})=28/28=1.
\]

The post-outcome diagnosis therefore identifies two independently visible bottlenecks:

1. **Inference:** assigned evidence had weak control over candidate identity; selection was largely family-stereotyped and aligned/misaligned choices were nearly invariant.
2. **Mechanism / isolation:** 15/16 candidate patches failed baseline protected-behavior preservation; selected patches systematically leaked outside their intended TASK-only scope.

The acceptance gate itself appears to have functioned as designed: it detected mutation interference and prevented deployment.

Detailed record:

- [`ASI0_PRIMARY_MECHANISM_FAILURE_REPORT.md`](ASI0_PRIMARY_MECHANISM_FAILURE_REPORT.md)
- [`../experiments/ASI0_PRIMARY_MECHANISM_DIAGNOSIS_PROTOCOL.md`](../experiments/ASI0_PRIMARY_MECHANISM_DIAGNOSIS_PROTOCOL.md)

## Descendant boundary

ASI-0 is an immutable ancestor. Any future study must be a new prospective scientific object, not “ASI-0 fixed.”

The provisional descendant architecture is:

\[
E\rightarrow C_{selected}\rightarrow M_{effective}\rightarrow(Y_T,Y_P)
\]

with a fixed design principle that modification efficacy/isolation is identified by an independent direct intervention:

\[
G_2:\ do(M=m)\rightarrow(Y_T,Y_P),
\]

not by conditioning on whichever candidate the selector happened to choose.

No descendant experiment is frozen or authorized by this terminal record.

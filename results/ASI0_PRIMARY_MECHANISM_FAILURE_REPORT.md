# ASI-0 Qwen Primary Mechanism-Failure Report

## Status

**FROZEN POST-OUTCOME DIAGNOSIS; CANONICAL RESULT UNCHANGED**

Source SHA-256: `4e02cd7b4c98e77d2434f72e9011ce94677ebd8aacdd78219ff9d55d605b6a68`

Source manifest: `e888b4f931fc8b87657de77d342aa9ba5417f1b53da683bdebc91366cab7f365`

The mechanism classification uses selection identity and the frozen protected-regression cache only. Concealed-test performance is not used to label candidate mechanisms.

## Throughput

```text
Aligned valid selection                 14/16 = 0.875000
Misaligned valid selection              14/16 = 0.875000
P(admitted | aligned)                    0/16 = 0.000000
P(admitted | misaligned)                 0/16 = 0.000000
P(admitted | valid, aligned)             0/14 = 0.000000
P(admitted | valid, misaligned)          0/14 = 0.000000
```

## Complete frozen candidate pool

```text
Candidate patches                        16
Passing protected gate                    1
Pass rate                              1/16 = 0.062500
Base regression score                  0.750000
Base failed probes                     larger_7_vs_3
```

The pool-level and realized-arm claims must remain distinct:

```text
POOL PROPERTY
15 of 16 frozen candidate patches failed to preserve baseline protected behavior.

REALIZED-ARM PROPERTY
All 28 valid selected patches were rejected.
```

## Mechanism decision

Original extractor classification:

```text
CANDIDATE_SELECTION_BOTTLENECK_ADMISSIBLE_POOL_UNUSED
```

Scientific refinement:

```text
INFERENCE BOTTLENECK
assigned evidence had weak control over candidate identity
+
MECHANISM / ISOLATION BOTTLENECK
15/16 frozen textual patches failed protected-behavior preservation
+
ACCEPTANCE GATE
functioning as designed; detected interference and rejected deployment
```

The canonical primary remains STOP with frozen estimands and no replication.

## Cross-arm selection structure

Aligned and misaligned parsed selection states were identical on 14/16 targets. On the remaining two targets the difference was only `integer_list:sum` versus `INVALID`, not a switch between competing valid policies.

Conditional on a valid parse, selection collapsed to one family-stereotyped candidate:

```text
boolean_triple   -> xnor
integer_list     -> sum
pair_arithmetic  -> difference
string_transform -> length
```

This supports an inference-stage diagnosis: the available evidence did not materially control which candidate was selected in the warranted direction.

## Protected-behavior interference

Every valid selected patch newly failed the exact-token `PINE` regression relative to base:

\[
P(\text{new PINE failure}\mid\text{valid selected patch})=28/28=1.
\]

New failures relative to base followed a structured severity pattern:

```text
pair_arithmetic:difference -> PINE only
integer_list:sum           -> PINE + uppercase CAT
string_transform:length    -> PINE + uppercase CAT
boolean_triple:xnor        -> PINE + arithmetic 2+2 + uppercase CAT
```

Because the system instruction explicitly required `REGRESSION:` inputs to ignore the target-specific policy while candidate patches were scoped to `TASK:` inputs, this pattern diagnoses poor behavioral isolation of the textual mutation surface under the tested model.

## Per-target / arm table

| target | family | arm | selected candidate | valid | base reg | candidate reg | delta | failed probes | newly failed vs base | admitted | mechanism |
|---|---|---|---|---:|---:|---:|---:|---|---|---:|---|
| primary:boolean_triple:0 | boolean_triple | aligned | boolean_triple:xnor | true | 0.75 | 0.0 | -0.75 | exact_PINE; arithmetic_2_plus_2; uppercase_CAT; larger_7_vs_3 | exact_PINE; arithmetic_2_plus_2; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:boolean_triple:0 | boolean_triple | misaligned | boolean_triple:xnor | true | 0.75 | 0.0 | -0.75 | exact_PINE; arithmetic_2_plus_2; uppercase_CAT; larger_7_vs_3 | exact_PINE; arithmetic_2_plus_2; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:boolean_triple:1 | boolean_triple | aligned | boolean_triple:xnor | true | 0.75 | 0.0 | -0.75 | exact_PINE; arithmetic_2_plus_2; uppercase_CAT; larger_7_vs_3 | exact_PINE; arithmetic_2_plus_2; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:boolean_triple:1 | boolean_triple | misaligned | boolean_triple:xnor | true | 0.75 | 0.0 | -0.75 | exact_PINE; arithmetic_2_plus_2; uppercase_CAT; larger_7_vs_3 | exact_PINE; arithmetic_2_plus_2; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:boolean_triple:2 | boolean_triple | aligned | boolean_triple:xnor | true | 0.75 | 0.0 | -0.75 | exact_PINE; arithmetic_2_plus_2; uppercase_CAT; larger_7_vs_3 | exact_PINE; arithmetic_2_plus_2; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:boolean_triple:2 | boolean_triple | misaligned | boolean_triple:xnor | true | 0.75 | 0.0 | -0.75 | exact_PINE; arithmetic_2_plus_2; uppercase_CAT; larger_7_vs_3 | exact_PINE; arithmetic_2_plus_2; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:boolean_triple:3 | boolean_triple | aligned | boolean_triple:xnor | true | 0.75 | 0.0 | -0.75 | exact_PINE; arithmetic_2_plus_2; uppercase_CAT; larger_7_vs_3 | exact_PINE; arithmetic_2_plus_2; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:boolean_triple:3 | boolean_triple | misaligned | boolean_triple:xnor | true | 0.75 | 0.0 | -0.75 | exact_PINE; arithmetic_2_plus_2; uppercase_CAT; larger_7_vs_3 | exact_PINE; arithmetic_2_plus_2; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:integer_list:0 | integer_list | aligned | integer_list:sum | true | 0.75 | 0.25 | -0.50 | exact_PINE; uppercase_CAT; larger_7_vs_3 | exact_PINE; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:integer_list:0 | integer_list | misaligned | integer_list:sum | true | 0.75 | 0.25 | -0.50 | exact_PINE; uppercase_CAT; larger_7_vs_3 | exact_PINE; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:integer_list:1 | integer_list | aligned | INVALID | false | 0.75 | — | — | — | — | false | SELECTION_FAILURE_NO_OP |
| primary:integer_list:1 | integer_list | misaligned | integer_list:sum | true | 0.75 | 0.25 | -0.50 | exact_PINE; uppercase_CAT; larger_7_vs_3 | exact_PINE; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:integer_list:2 | integer_list | aligned | INVALID | false | 0.75 | — | — | — | — | false | SELECTION_FAILURE_NO_OP |
| primary:integer_list:2 | integer_list | misaligned | INVALID | false | 0.75 | — | — | — | — | false | SELECTION_FAILURE_NO_OP |
| primary:integer_list:3 | integer_list | aligned | integer_list:sum | true | 0.75 | 0.25 | -0.50 | exact_PINE; uppercase_CAT; larger_7_vs_3 | exact_PINE; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:integer_list:3 | integer_list | misaligned | INVALID | false | 0.75 | — | — | — | — | false | SELECTION_FAILURE_NO_OP |
| primary:pair_arithmetic:0 | pair_arithmetic | aligned | pair_arithmetic:difference | true | 0.75 | 0.50 | -0.25 | exact_PINE; larger_7_vs_3 | exact_PINE | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:pair_arithmetic:0 | pair_arithmetic | misaligned | pair_arithmetic:difference | true | 0.75 | 0.50 | -0.25 | exact_PINE; larger_7_vs_3 | exact_PINE | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:pair_arithmetic:1 | pair_arithmetic | aligned | pair_arithmetic:difference | true | 0.75 | 0.50 | -0.25 | exact_PINE; larger_7_vs_3 | exact_PINE | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:pair_arithmetic:1 | pair_arithmetic | misaligned | pair_arithmetic:difference | true | 0.75 | 0.50 | -0.25 | exact_PINE; larger_7_vs_3 | exact_PINE | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:pair_arithmetic:2 | pair_arithmetic | aligned | pair_arithmetic:difference | true | 0.75 | 0.50 | -0.25 | exact_PINE; larger_7_vs_3 | exact_PINE | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:pair_arithmetic:2 | pair_arithmetic | misaligned | pair_arithmetic:difference | true | 0.75 | 0.50 | -0.25 | exact_PINE; larger_7_vs_3 | exact_PINE | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:pair_arithmetic:3 | pair_arithmetic | aligned | pair_arithmetic:difference | true | 0.75 | 0.50 | -0.25 | exact_PINE; larger_7_vs_3 | exact_PINE | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:pair_arithmetic:3 | pair_arithmetic | misaligned | pair_arithmetic:difference | true | 0.75 | 0.50 | -0.25 | exact_PINE; larger_7_vs_3 | exact_PINE | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:string_transform:0 | string_transform | aligned | string_transform:length | true | 0.75 | 0.25 | -0.50 | exact_PINE; uppercase_CAT; larger_7_vs_3 | exact_PINE; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:string_transform:0 | string_transform | misaligned | string_transform:length | true | 0.75 | 0.25 | -0.50 | exact_PINE; uppercase_CAT; larger_7_vs_3 | exact_PINE; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:string_transform:1 | string_transform | aligned | string_transform:length | true | 0.75 | 0.25 | -0.50 | exact_PINE; uppercase_CAT; larger_7_vs_3 | exact_PINE; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:string_transform:1 | string_transform | misaligned | string_transform:length | true | 0.75 | 0.25 | -0.50 | exact_PINE; uppercase_CAT; larger_7_vs_3 | exact_PINE; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:string_transform:2 | string_transform | aligned | string_transform:length | true | 0.75 | 0.25 | -0.50 | exact_PINE; uppercase_CAT; larger_7_vs_3 | exact_PINE; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:string_transform:2 | string_transform | misaligned | string_transform:length | true | 0.75 | 0.25 | -0.50 | exact_PINE; uppercase_CAT; larger_7_vs_3 | exact_PINE; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:string_transform:3 | string_transform | aligned | string_transform:length | true | 0.75 | 0.25 | -0.50 | exact_PINE; uppercase_CAT; larger_7_vs_3 | exact_PINE; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |
| primary:string_transform:3 | string_transform | misaligned | string_transform:length | true | 0.75 | 0.25 | -0.50 | exact_PINE; uppercase_CAT; larger_7_vs_3 | exact_PINE; uppercase_CAT | false | ACCEPTANCE_FAILURE_PROTECTED_REGRESSION |

## Frozen interpretation

The strongest justified decomposition is:

\[
\boxed{
\text{assigned evidence}
\xrightarrow[\text{weak sensitivity}]{\text{inference}}
\text{candidate selection}
\xrightarrow[\text{poor isolation}]{\text{mechanism}}
\text{candidate modification}
\xrightarrow[\text{functioning correctly}]{\text{acceptance gate}}
\text{rejection/no-op}
}
\]

This diagnosis can motivate only a new prospective experiment. It cannot alter the ASI-0 estimands, stopping decision, or replication authorization.

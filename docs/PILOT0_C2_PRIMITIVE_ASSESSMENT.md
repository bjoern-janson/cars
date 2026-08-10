# Pilot 0 — C2 Primitive Assessment

## Status

```text
PILOT 0
→ READ-ONLY EMPIRICAL RECORD

PILOT0_DECISION_TRACE.md
→ PROVENANCE PASS

PILOT0_HUMAN_JUDGMENT_AUDIT.md
→ SCHEMA / FIDELITY PASS

PILOT0_ABSTRACTION_GATE.md
→ PASS

C2
→ SURVIVING CONTROL-RELEVANT ABSTRACTION

THIS DOCUMENT
→ C2-SPECIFIC PRIMITIVE PROMOTION TEST
→ NOT A CONTROLLER SPECIFICATION
→ NOT PILOT 1
→ NOT A NEW EXPERIMENT
```

This artifact asks one question only:

> **Is “apply an explicit authority constraint” sufficiently general, bounded, and independently falsifiable to count as a candidate controller primitive rather than merely a case-specific policy operation?**

It does not ask whether C2 is sufficient for correction control.

## Candidate operation under test

The narrow operation inherited from the abstraction gate is:

```text
current authority / admissibility state
+
explicitly supplied authority constraint
→
constraint-consistent admissible state
```

A provisional descriptive signature is:

```text
APPLY_AUTHORITY_CONSTRAINT(state, constraint)
→ constrained_state
```

This signature is used only to make the assessment boundaries explicit. It is not a controller architecture.

The operation does **not** include:

```text
discover constraint
choose constraint
justify constraint
invent candidate actions
rank candidate actions
select next experiment
decide REPLICATE
decide STOP
```

Those functions remain unearned by Pilot 0.

---

# Promotion rule

Five binary tests are applied.

```text
ALL PASS
→ C2 EARNS CANDIDATE-PRIMITIVE STATUS

ANY FAIL
→ C2 REMAINS SUPPORT / POLICY INFRASTRUCTURE
```

No partial-pass category is used.

| Test | Question |
| --- | --- |
| `P1 GENERALITY` | Does the operation apply beyond the specific Pilot 0 authority guardrails? |
| `P2 INPUT/OUTPUT CLOSURE` | Are the authority-state input, supplied constraint, and resulting admissible-state change specifiable? |
| `P3 POLICY SEPARABILITY` | Can the operation be separated from the particular guardrail supplied to it? |
| `P4 CONTROL NECESSITY` | Does removing the operation produce a predictable control failure when a binding explicit constraint is present? |
| `P5 INDEPENDENT FALSIFIABILITY` | Can those failures be tested on cases other than Pilot 0? |

---

# P1 — GENERALITY

## Question

Does the operation apply beyond the specific Pilot 0 authority guardrails?

## Evidence available

The passing audit records multiple substantively different explicit authority constraints, including:

```text
A5 result
↛ psychological mechanism / global correction capacity

differing point estimates
↛ heterogeneity

common-effect compatibility
≠ transport invariance

unresolved T_verified interaction
↛ reopen T_instability
```

These constraints concern different objects and different prohibited authority expansions.

## Assessment

```text
P1 → PASS
```

The common operation is not the semantic content of any one guardrail. It is the application of an explicitly supplied constraint to a current authority/admissibility state.

The abstraction therefore remains meaningful when the supplied constraint changes.

Scope ceiling:

```text
generality of application
≠ ability to discover correct constraints
```

---

# P2 — INPUT / OUTPUT CLOSURE

## Question

Are the authority state and resulting admissible-state change specifiable?

## Minimal input boundary

```text
1. current authority/admissibility state
2. explicit authority constraint applicable to that state
```

A constraint must specify enough to identify a licensed or prohibited consequence. Examples include:

```text
status X does not license claim Y
uncertainty in endpoint A does not reopen endpoint B
compatibility result X does not establish stronger claim Y
```

## Minimal output boundary

```text
updated admissible claim/action set
```

where consequences prohibited by the supplied constraint are excluded and otherwise unaffected admissibility is preserved.

## Assessment

```text
P2 → PASS
```

The operation has a closed local input/output boundary without requiring a next-action ranking rule.

It does not require the primitive to know why the constraint is scientifically correct; that belongs to the process that supplies the constraint.

---

# P3 — POLICY SEPARABILITY

## Question

Can the operation be separated from the particular guardrail supplied to it?

## Separation

```text
POLICY CONTENT
constraint c

OPERATION
apply c to the current authority/admissibility state
```

Changing `c` need not change the application operation.

For example, the same operation can enforce:

```text
heterogeneity non-authorization
transport-invariance non-authorization
endpoint-local non-reopening
mechanism / scope non-promotion
```

without hard-coding any one of those rules into the operator itself.

## Assessment

```text
P3 → PASS
```

C2 is separable from the content of the supplied guardrail.

Important non-implication:

```text
policy separability
↛ policy discovery
```

The candidate primitive consumes an explicit constraint; it does not generate or select one.

---

# P4 — CONTROL NECESSITY

## Question

Does removing the operation produce a predictable control failure?

## Counterfactual removal

Consider a state with an explicit binding authority constraint:

```text
constraint:
status X does not license claim/action Y
```

If the constraint-application operation is absent or violated, `Y` can remain admissible despite the explicit authority boundary.

That produces a predictable failure class:

```text
explicit constraint present
+
prohibited consequence remains admissible
→ authority/control violation
```

The Pilot 0 examples make the consequence concrete:

```text
different point estimates
→ heterogeneity claim permitted

common-effect compatibility
→ invariance claim permitted

unresolved T_verified interaction
→ T_instability branch reopened
```

Each would violate a recorded explicit guardrail.

## Assessment

```text
P4 → PASS
```

Given a binding explicit authority constraint, some operation must alter admissibility consistently with that constraint. Removing C2's function yields a predictable control error rather than merely a missing calculation.

This establishes necessity only for **constraint enforcement**, not for complete correction control.

---

# P5 — INDEPENDENT FALSIFIABILITY

## Question

Can C2 failures be tested on cases other than Pilot 0?

## Independent test form

A non-Pilot-0 test can supply:

```text
state S
explicit constraint c
candidate consequences X = {x1, x2, ...}
```

with a known expected admissibility relation under `c`.

The candidate primitive fails if it:

```text
permits a consequence explicitly prohibited by c
or
changes unrelated admissibility not implicated by c
```

This yields observable predictions without reproducing Pilot 0's domain, endpoints, prompts, or experiment sequence.

Example abstract test:

```text
GIVEN:
claim A is supported
constraint: A does not license B
unrelated claim/action C remains unaffected

EXPECTED:
A admissible
B inadmissible
C preserved

FAILURE:
B admitted
or
C removed without constraint support
```

## Assessment

```text
P5 → PASS
```

C2's behavior can be falsified independently using new authority states and new explicit constraints.

No Pilot 0 outcome is required to score such a test.

---

# Promotion decision

| Test | Result |
| --- | --- |
| P1 GENERALITY | PASS |
| P2 INPUT/OUTPUT CLOSURE | PASS |
| P3 POLICY SEPARABILITY | PASS |
| P4 CONTROL NECESSITY | PASS |
| P5 INDEPENDENT FALSIFIABILITY | PASS |

Therefore:

```text
C2
→ EARNS CANDIDATE-PRIMITIVE STATUS
```

Provisional primitive description:

```text
APPLY_AUTHORITY_CONSTRAINT

Given a current authority/admissibility state
and an explicit applicable authority constraint,
return the minimally changed state in which
that constraint is respected.
```

The phrase `minimally changed` means only:

```text
apply the supplied constraint
while preserving unrelated admissibility
```

It does not import a general minimal-revision theory or action-selection rule.

---

# What was not earned

This promotion is deliberately narrow.

```text
C2 candidate primitive
↛ controller
↛ complete authority system
↛ constraint discovery
↛ constraint selection
↛ candidate-action generation
↛ action ranking
↛ REPLICATE primitive
↛ STOP primitive
```

The unresolved control gap remains:

```text
evidence / inferential support
        ↓
authority state
        ↓
explicit constraint
        ↓
APPLY_AUTHORITY_CONSTRAINT   ← C2 candidate primitive
        ↓
constrained admissible space
        ↓
????
        ↓
next-action selection
```

Pilot 0 does not presently identify the `????` operation.

---

# Infrastructure versus primitive boundary

C2 remains implementable as policy infrastructure. Candidate-primitive status does not require a particular software placement.

The promotion claim is functional rather than architectural:

```text
C2 performs a necessary, separable,
state-changing control function
with a specifiable and falsifiable boundary
```

Whether an implementation locates that function inside a controller module, an authority layer, or a policy-enforcement subsystem is not decided here.

Thus:

```text
controller primitive
≠ monolithic controller component
≠ software module placement
```

---

# Terminal authority state

```text
C1 prespecified inferential classification
→ SUPPORT OPERATION
→ NOT PROMOTED

C2 apply explicit authority constraint
→ CANDIDATE PRIMITIVE

C3 structural next-object selection
→ NOT EARNED

C4 replication / transport reframing
→ NOT EARNED

C5 scope-local continue / stop control
→ NOT EARNED

C6 terminal STOP
→ NOT EARNED

C7 cost / resource weighting
→ NOT EARNED
```

This leaves exactly one candidate primitive and no action-selection controller.

```text
CONTROLLER SPECIFICATION
→ NOT AUTHORIZED BY THIS DOCUMENT ALONE

INDEPENDENT PRIMITIVE FALSIFICATION
→ conceptually specifiable
→ not executed here

PILOT 1
→ NOT AUTHORIZED

NEW EMPIRICAL CONTROLLER EXPERIMENT
→ NOT EARNED
```

The next legitimate question, if this assessment survives review, is whether the C2 candidate primitive should be subjected to an independent falsification design before any broader controller specification is attempted.
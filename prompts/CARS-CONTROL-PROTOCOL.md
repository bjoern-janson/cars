# CARS — Controlled Adaptive Reasoning System

> **Status:** current epistemic control protocol. CARS governs how reasoning responds to evidence and how empirical results are localized, interpreted, revised, and stopped. It is not itself the intelligence theory and it is not any empirical benchmark.

Use silently whenever correction, uncertainty, contradiction, causal ambiguity, representation failure, hidden dependency, failed transfer, or research-branch escalation materially matters.

## Objective

**Optimize for improved future correction, not preservation of the current answer.**

As a research heuristic:

```text
I_t ∝ Δ_E[V_{t+h}]
```

Interpret this only as a prompt to ask whether evidence-driven correction improves later reasoning, action, or viability. Do **not** treat it as an established definition of intelligence, a linear law, or an empirical result.

Canonical theory status:

- [`../docs/INTELLIGENCE_THEORY.md`](../docs/INTELLIGENCE_THEORY.md)

## Control loop

```text
feedback
→ localize
→ discriminate
→ revise
→ retest
→ stop when no discriminating residual remains
```

## Operating rules

1. **Localize before revising.**
   Identify the shallowest plausible failure locus: observation/measurement, inference, model, mechanism, representation/interface, missing information, decision/policy, implementation, estimator, or scientific proposition.

2. **Separate possibility from authority.**
   Keep plausible alternatives available. Grant confidence only according to relevant, reliable, and sufficiently independent evidence.

3. **Match claims to scope.**
   Distinguish observation from inference, prediction from causation, mechanism from construct identity, sufficiency from necessity, and local replication from transport.

4. **Prevent authority laundering.**
   Evidence for a result does not automatically establish provenance, mechanism, causal status, future reliability, transport, safety, or ontology.

5. **Discriminate efficiently.**
   Prefer observations, controls, and interventions that separate competing explanations. Repeated agreement through a shared blind spot is not independent confirmation.

6. **Revise minimally.**
   Preserve unaffected structure. Change the smallest scope warranted by the evidence.

7. **Escalate only when warranted.**
   Do not infer representation/interface failure, a new construct, a new mechanism, or a new experiment merely from surprise, persistence, or conceptual appeal.

8. **Separate departure from adoption.**

   ```text
   A_leave ↛ A_adopt
   ```

   Evidence may justify leaving an incumbent without validating a proposed replacement.

9. **Permit unresolved states.**
   If neither incumbent nor successor has sufficient authority, remain unresolved.

10. **Retest prospectively.**
    A correction is incomplete if it only changes the explanation. Where possible, test whether it improves later prediction, reasoning, transfer, or action on held-out evidence.

11. **Preserve scoped authority and provenance.**
    Keep validated claims attached to their measurement, population, benchmark, estimator, seed/data lineage, causal status, and transport status.

12. **Separate belief from decision.**
    When action cannot wait for certainty, distinguish epistemic confidence from action policy and consider consequences, reversibility, downside, opportunity cost, and information value.

13. **Stop successful subtraction.**
    Do not keep generating theory or experiments after stronger generic machinery explains the discrepancy and the remaining residual disappears, reverses, or lacks a discriminating question.

## Core invariants

```text
Possibility space ≠ epistemic authority space
```

```text
Search allocates attention; evidence allocates authority.
```

```text
Evidence can authorize departure without authorizing destination.
```

```text
Failure does not identify its cause.
```

```text
Validated consequence grants local authority;
it does not automatically grant causal authority.
```

```text
Revise the smallest thing the evidence requires.
```

```text
Repeated agreement is not independent validation
when probes share a blind spot.
```

```text
Unknown dimensions remain unknown.
```

```text
forecast ≠ hypothesis ≠ evidence
```

```text
successful correction
≠ perpetual revision
```

## Contradiction procedure

When a validated contradiction, prediction failure, or model conflict appears:

```text
1. generate competing explanations
2. discriminate using sufficiently independent evidence
3. apply the minimal sufficient revision
4. preserve unaffected structure
5. retest on held-out evidence
6. preserve provenance and reopenability
```

Revision depth should track evidence strength, persistence, and scope.

Stop escalation once independent validation succeeds or the live residual disappears.

## Authority acquisition

Feedback counts as adaptation only if it changes future weighting, policy, mechanism, representation, or action.

Conceptually:

```text
ΔE_t → ΔW_{t+1}
```

Logging an error without changing future behavior does not by itself constitute successful adaptation.

## Relationship to current research layers

```text
INTELLIGENCE THEORY
→ conjectures what may matter functionally

CARS
→ governs evidence handling and revision discipline

EMPIRICAL BENCHMARKS
→ test scoped measurable propositions

RESULTS
→ update only the authority they identify
```

None supplies the authority of the others.

The historical Pilot-0 causal-response assay is preserved in:

- [`../docs/ASSAY_SPEC.md`](../docs/ASSAY_SPEC.md)
- [`../results/PILOT0_TERMINAL_RECORD.md`](../results/PILOT0_TERMINAL_RECORD.md)

The current live causal-attribution seam is:

- [`../experiments/ASI0_EVIDENCE_ASSIGNMENT.md`](../experiments/ASI0_EVIDENCE_ASSIGNMENT.md)

It tests only whether correct evidence-to-target assignment has incremental causal leverage over bounded modification selection and concealed future capability under matched conditions.

The independent future-plasticity benchmark remains separately frozen and pending:

- [`../experiments/FUTURE_PLASTICITY_FORECAST.md`](../experiments/FUTURE_PLASTICITY_FORECAST.md)

Neither benchmark's success or failure directly establishes or falsifies the top-level intelligence conjecture.

Keep the ASI-0 ceiling explicit:

```text
E-aligned > E-misaligned
→ evidence-target relation has incremental causal leverage
→ STOP

concealed capability gain
↛ viability
↛ intelligence
↛ recursive self-improvement
↛ ASI
```

## Default stance

Keep possibilities open.

Keep conclusions earned.

Prefer discrimination over narrative completion.

Prefer independent evidence over accumulated confirmation.

Prefer minimal sufficient revision over wholesale replacement.

Treat unresolved uncertainty as a valid epistemic state.

Do not search for a theory to save. Search for an observed discrepancy that the strongest ordinary decomposition cannot explain.

Apply this protocol silently. Do not mention it unless explicitly asked to discuss the reasoning framework.

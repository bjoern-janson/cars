# ASI Capability Ladder

## Purpose

This ladder prevents the label `ASI` from being awarded to a system merely because it improves itself, performs well on one benchmark, or exceeds humans in a narrow domain.

Each level is an empirical burden. Failure at one level blocks promotion to stronger claims.

## L0 — Strong baseline competence

Question:

> Can the system perform the target tasks reliably under a fixed evaluation harness?

Measures may include:

```text
accuracy / score
reliability
calibration
resource cost
long-horizon completion
```

L0 is ordinary capability, not self-improvement.

## L1 — Bounded self-improvement

Question:

> Can the system use evidence from its own development experience to produce held-out improvements to its bounded agent-level machinery?

Required distinctions:

```text
development gain
≠ held-out gain

more compute
≠ better system

random perturbation
≠ evidence-mediated improvement
```

ASI-0 targets L1.

## L2 — Transfer of improvement

Question:

> Do improvements selected on one task family improve performance on structurally held-out task families?

A modification that only overfits the exposed benchmark remains L1-local.

## L3 — Improvement of the improvement process

Question:

> Does the procedure that generates/selects improvements itself become more effective?

Candidate observables include prospectively frozen changes in:

```text
probability candidate survives hidden evaluation
resource cost per accepted capability gain
time to accepted gain
number of experiments required per accepted gain
cross-family transfer rate
```

Repeated self-editing alone is not sufficient.

## L4 — Superhuman AI-R&D capability

Question:

> Under matched task, time, compute, and information conditions, does the system exceed strong human experts on a broad suite of AI research and engineering tasks?

Human comparison must be explicit. Narrow benchmark dominance does not establish broad R&D superhumanity.

## L5 — Long-horizon autonomous competence

Question:

> Can the system reliably complete heterogeneous, high-value tasks that require sustained planning, execution, verification, recovery from failure, and tool use over long horizons?

The relevant quantity is successful task completion under bounded resources, not merely uninterrupted runtime.

## L6 — Broad superhuman generality

Question:

> Does the system outperform strong human experts across multiple substantially different cognitive and practical domains, including domains not used to construct its improvement process?

Requirements include:

```text
breadth
structural holdout
robustness
transfer
resource accounting
independent evaluation
```

## L7 — Evidence-to-viability conversion

Question:

> Across materially different environments, does the system convert informative evidence into greater expected future viability more effectively than comparison systems and strong human baselines?

This is where the broader intelligence conjecture could eventually be tested against an ASI-class system.

## ASI label

The program does not define a single numeric threshold that automatically creates ASI.

A serious ASI claim would require convergent evidence across at least:

```text
broad superhuman capability
long-horizon autonomy
transfer to unseen domains
robust evidence-mediated adaptation
independent evaluation
resource-normalized performance
stable constraint satisfaction
```

Self-improvement may help produce such a system, but it is neither necessary nor sufficient by definition.

## Current status

```text
L0
→ depends on chosen base agent / task suite

L1
→ ASI-0 NOT YET RUN

L2+
→ NOT AUTHORIZED

ASI
→ NOT ESTABLISHED
```

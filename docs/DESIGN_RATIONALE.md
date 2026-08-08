# Design Rationale

CARS is designed around a tension: systems must remain correctable without becoming either rigid or novelty-seeking.

This document explains the reasoning constraints behind the prompt work, catalyst intervention, and current research architecture. The architecture remains hypothetical; these are design commitments to test, not demonstrated properties.

## 1. Localize before revising

A failure signal says that something went wrong. It usually does not identify the cause. Observation failures, inference failures, model failures, representation failures, missing information, mechanism uncertainty, and decision errors require different corrections.

The architecture therefore treats the current residual representation as provisional:

```text
ρ_t = Φ_t(E_t)
```

`ρ_t` is what the current residual mapper makes of the evidence, not the hidden truth itself.

## 2. Possibility is cheap; authority is expensive

Language models can generate many coherent hypotheses. Coherence and availability are not evidence. CARS therefore permits hypothesis generation while separately governing confidence and adoption.

Candidate generation expands the possibility space. It does not grant succession authority.

## 3. Scope leakage is a common failure

Evidence often identifies less than the explanation built around it. A valid observation can coexist with unknown mechanism, uncertain provenance, weak prediction, or limited transfer.

Correction-capacity claims should remain indexed to the residual and evaluation scope that generated them rather than being promoted into global competence claims.

## 4. Repeated evidence can share one failure mode

Many agreeing probes can be less informative than one structurally independent discriminator when all probes inherit the same blind spot.

The same concern applies to validation. An unseen validation environment is not independent enough if the validation procedure itself was tuned after seeing candidate-selection information.

## 5. Minimal revision is a hypothesis, not an automatic result

Wholesale updates can destroy valid structure, so limited revision is preferable when evidence supports it. But “minimum sufficient revision” should not be assumed before candidate space and sufficiency have actually been tested.

The research architecture therefore distinguishes candidate revision from validated successor. Minimality, when claimed, must itself be earned through removal, perturbation, substitution, ablation, or comparable evidence.

## 6. Representation change is an escalation path

A system should not infer that its representation is inadequate simply because a task is surprising or difficult. Representation change becomes warranted only when evidence supports non-identifiability or insufficiency relative to plausible within-representation explanations.

A representation can be highly detailed and still collapse the distinction needed by the target claim.

> **Resolution is not explanatory authority.**

## 7. Rejecting one model does not validate another

The transition from incumbent failure to successor adoption is a major authority leak. CARS explicitly permits the state:

> The incumbent is insufficient; no replacement is yet justified.

Compactly:

```text
A_leave ↛ A_adopt
```

This applies to models, representations, residual mappings, candidate generators, validation procedures, and the correction process itself.

## 8. Correction is prospective

A retrospective explanation can sound excellent without changing future reasoning. CARS treats changed future reasoning/action and transfer as stronger evidence of correction than narrative repair alone.

The current architecture strengthens this by requiring improvement on the residual that triggered revision rather than relying only on global average gains.

## 9. Decisions can be necessary before beliefs are settled

Epistemic uncertainty need not imply paralysis. CARS separates belief state from action selection so reversible or low-downside actions can proceed without pretending uncertainty vanished.

## 10. Historical participation is not functional necessity

A condition can be present during every observed success without being load-bearing. A component can also be sufficient without being necessary when another component can substitute for it.

Dependency claims therefore require discriminating interventions. When successful substitutions exist, preservation authority should migrate away from the historical implementation toward the tested functional relation, within scope.

## 11. Validation machinery is part of the correction surface

The validator is not a privileged oracle.

```text
𝒱_t := validation procedure
V_t^ind := 𝒱_t(R_cand,t ; W_t^ind)
```

The validation procedure can itself be inadequate or contaminated. If revised, it must face the same separation between departure and adoption as any other component.

## 12. Independence is relative to selection information

Independence should be stated at the protocol level, not inferred merely because a different dataset was used.

Let `I_sel,t` contain all information capable of affecting candidate generation or selection. The stronger condition is:

```text
(𝒱_t, W_t^ind) ⟂_design I_sel,t
```

Practical rule:

> **If information could have changed which revision was generated or selected, it cannot later be counted as independent validation evidence for that revision.**

## 13. Local component validity and system succession are different claims

A component revision may be enabling rather than immediately outcome-improving. It should therefore be validated against the function it claims to improve.

The full successor makes the stronger claim and must demonstrate improved correction capacity on the triggering residual, while avoiding unacceptable regression on unaffected controls.

This prevents both extremes:

- rejecting useful enabling revisions because they do not immediately move the terminal metric;
- accepting a complete successor because one local component improved in isolation.

## 14. No correction-surface component receives epistemic immunity

The current state may include:

```text
X_t = (C_t, O_t, M_t, Φ_t, G_t, 𝒱_t, …)
```

Any of these can become the limiting factor. The architecture is recursively corrigible only if successors to these components must themselves earn adoption through independent evidence.

The intended recursion is controlled succession:

```text
propose successor
→ validate independently
→ grant only scoped adoption authority
→ retest future correction capacity
```

## 15. Formal notation and catalyst notation have different jobs

A formal representation and a reasoning intervention should not be optimized as though they were the same artifact.

```text
formal notation = representation
catalyst notation = intervention
execution semantics = operational instruction
```

The formal architecture should maximize precision and auditability. The catalyst should minimize semantic reconstruction while preserving the intended operational distinctions. Execution semantics should tell the system what to do without forcing it to reconstruct the theory.

This yields the notebook's current three-layer stack:

```text
Catalyst activates
→ Formalism constrains
→ Semantics executes
```

A catalyst is therefore not validated because it looks elegant. Its notation must survive blind semantic-recovery tests.

## 16. Semantic recovery and execution are separate

A model can decode a catalyst correctly without using it correctly, and can use a procedure faithfully without improving outcomes.

Keep the following non-implications explicit:

```text
semantic recovery
↛ faithful execution
↛ task improvement
↛ CorrCap improvement
↛ recursive improvement
```

The evaluation stack should preserve these distinctions rather than compressing them into one “works / does not work” judgment.

## 17. The construct must not become its own metric

The broader framing uses:

```text
I ∝ C_improve
```

where `C_improve` is the candidate construct “capacity to convert feedback into increased future correctability / viability.”

`CorrCap` is an operational measurement target, not the construct itself:

```text
C_improve ≠ CorrCap
```

This prevents the theory from granting its preferred metric unearned construct validity.

A `CorrCap` measure must survive tests for gaming, proxy capture, benchmark dependence, and false escalation before it can support stronger claims about future correctability.

## 18. Stopping is part of the method

Once a representation is coherent enough to test, further polishing can have lower information value than exposure to adversarial evidence.

The current catalyst therefore follows:

```text
freeze
→ blind test
→ measure decoding
→ measure correction
→ revise only if evidence warrants
```

This is not a claim that the current form is correct. It is a commitment to let empirical failure, rather than aesthetic preference, drive the next substantive revision.

## Governing research question

The architecture should ultimately be judged by whether it survives attempts to make its own authority system certify a bad successor—not by whether its internal story is coherent.
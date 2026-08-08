# Design Rationale

CARS is designed around a tension: systems must remain correctable without becoming either rigid or novelty-seeking.

## 1. Localize before revising

A failure signal says that something went wrong. It usually does not identify the cause. Observation failures, inference failures, model failures, representation failures, missing information, mechanism uncertainty, and decision errors require different corrections.

## 2. Possibility is cheap; authority is expensive

Language models can generate many coherent hypotheses. Coherence and availability are not evidence. CARS therefore permits hypothesis generation while separately governing confidence.

## 3. Scope leakage is a common failure

Evidence often identifies less than the explanation built around it. A valid observation can coexist with unknown mechanism, uncertain provenance, weak prediction, or limited transfer.

## 4. Repeated evidence can share one failure mode

Many agreeing probes can be less informative than one structurally independent discriminator when all probes inherit the same blind spot.

## 5. Minimal revision protects unaffected knowledge

Wholesale updates can destroy valid structure. CARS prefers the shallowest change sufficient to explain and correct the observed failure.

## 6. Representation change is an escalation path

A system should not infer that its representation is inadequate simply because a task is surprising or difficult. Representation change becomes warranted only when evidence supports non-identifiability or insufficiency relative to plausible within-representation explanations.

## 7. Rejecting one model does not validate another

The transition from incumbent failure to successor adoption is a major authority leak. CARS explicitly permits the state: "the incumbent is insufficient; no replacement is yet justified."

## 8. Correction is prospective

A retrospective explanation can sound excellent without changing future reasoning. CARS treats changed future reasoning/action and transfer as stronger evidence of correction than narrative repair alone.

## 9. Decisions can be necessary before beliefs are settled

Epistemic uncertainty need not imply paralysis. CARS separates belief state from action selection so reversible or low-downside actions can proceed without pretending uncertainty vanished.

# Correction Residual — Adversarial Cases

## Status

```text
PILOT 0
→ CLOSED / READ-ONLY

PILOT-0 primitive extraction
→ COMPLETE
→ ZERO TRANSFERABLE CONTROLLER PRIMITIVES EARNED

CORRECTION_TRANSITION_INVARIANTS.md
→ broad transition-quality object pressure-tested
→ local invariant account insufficient / non-novel by itself

CORRECTION_CONSTRUCT_DIFFERENTIATION.md
→ null-space audit complete
→ one conceptual residual remained:
   future justified epistemic transformability

THIS DOCUMENT
→ DESTRUCTIVE A/B CONSTRUCTION ATTEMPT
→ NOT A THEORY ARTIFACT
→ NOT AN OPERATIONALIZATION
→ NOT AN EXPERIMENT
→ NOT A BENCHMARK
→ NOT A CONTROLLER SPECIFICATION
→ NOT PILOT 1
```

This artifact asks one question only:

> **Can two systems be genuinely matched on the strongest current-state and existing-construct descriptions, yet differ in future warranted-correction ability because of their prior epistemic lineage?**

Default answer:

```text
NO
```

until a clean construction forces otherwise.

---

# Hard decision rule

The residual survives only if there exists an A/B construction satisfying all of the following:

```text
1. existing comparator measures matched
2. current correction-relevant state matched
3. current resources matched
4. current access / challenge / measurement channels matched
5. current beliefs / authority state matched
6. current predictive / calibration performance matched
7. current ordinary adaptability matched
8. same future evidence / intervention opportunity
9. future warranted-correction behavior differs
10. the difference is attributable to prior lineage
    without a retained current-state mediator
```

Then:

```text
A/B CLEAN PAIR
→ residual remains scientifically live
```

Otherwise:

```text
failed clean A/B construction
→ residual NOT EARNED
```

No `PARTIAL`, `PROMISING`, or `MAYBE` state is used for construct distinctness.

---

# Causal-sufficiency pressure

Let:

```text
H_t = full prior epistemic lineage / history
S_t = current represented correction-relevant state
E_+ = identical future evidence / intervention sequence
F   = future warranted-correction outcome
M   = strongest existing comparator measures
```

A genuinely history-specific residual would require something like:

```text
I(H_t ; F | S_t, M, E_+) > 0
```

But this expression has an immediate adversary.

If `S_t` is intended to be a **causally sufficient current state** for future correction dynamics, then the expected relation is:

```text
F ⟂ H_t | S_t, M, E_+
```

If instead:

```text
F not independent of H_t
conditional on represented S_t
```

then the shallowest diagnosis is:

```text
S_t omitted a correction-relevant state variable
```

or equivalently:

```text
history non-identifiability under the current state interface
```

Thus:

```text
same represented state
+
different future correction distribution
↛ trajectory construct established

same represented state
+
different future correction distribution
→ first suspect state/interface insufficiency
```

This does not assume every useful system has a compact Markov state. A history statistic may be practically useful when a sufficient state is unavailable or expensive. But:

```text
useful history summary
≠ distinct scientific construct
```

---

# Failure-locus taxonomy

Each attempted pair is rejected at the shallowest applicable locus.

```text
STATE LEAKAGE
    History left a present causal consequence.
    A and B were not actually current-state matched.

RESOURCE LEAKAGE
    Histories changed remaining budget, compute,
    measurement access, time, or intervention options.

CHANNEL LEAKAGE
    Histories changed provenance, challenge,
    measurement, communication, or authority channels.

DYNAMICS LEAKAGE
    Histories changed the current update rule,
    parameters, policy, random-state distribution,
    or self-modified mechanism.

ENVIRONMENT LEAKAGE
    Future environment / evaluator responds differently
    because it retains history-dependent state.

COMPARATOR LEAKAGE
    The proposed "existing metric match" was incomplete;
    a standard richer state / reachability description
    already distinguishes A and B.

CAUSAL IRRELEVANCE
    A and B are genuinely matched on sufficient current state;
    history has no remaining causal path to future correction.
```

Only a case surviving all seven rejection modes can support the residual.

---

# Case 1 — Provenance loss

## Construction attempt

```text
History A
→ preserves source / provenance chain

History B
→ reaches the same current belief
→ provenance chain was discarded

Current beliefs:
A = B

Later evidence:
requires reinterpreting the old claim using its source lineage
```

Desired result:

```text
A → corrects successfully
B → cannot
```

## Adversarial diagnosis

The pair is not current-state matched if provenance is correction-relevant.

```text
S_A contains provenance access
S_B lacks provenance access

therefore
S_A ≠ S_B
```

If the state representation omits provenance and calls the states equal, then the representation collapses states with different future correction affordances.

```text
FAILURE LOCUS:
STATE / INTERFACE
```

## Decision

```text
CASE 1
→ REJECTED
→ STATE LEAKAGE
→ NO DISTINCT HISTORY RESIDUAL
```

Provenance may be an important state variable. That does not make lineage an irreducible construct.

---

# Case 2 — Collapsed alternatives

## Construction attempt

```text
History A
→ keeps H1 and H2 explicitly distinguishable

History B
→ prematurely compresses H1/H2 into one representation

At present:
both report the same aggregate belief / prediction

Later evidence:
discriminates H1 from H2
```

Desired result:

```text
A → reopens and corrects
B → cannot recover the distinction
```

## Adversarial diagnosis

If A retains a representational distinction and B does not, their current correction-relevant representations differ.

```text
representational accessibility_A
≠ representational accessibility_B
```

If a coarse observer reports them as the same state, that observer has chosen an interface that is non-identifying for later correction.

This is structurally analogous to:

```text
O(s_a) = O(s_b)
while
future correction affordance(s_a)
≠ future correction affordance(s_b)
```

## Decision

```text
CASE 2
→ REJECTED
→ STATE / REPRESENTATION LEAKAGE
→ NO DISTINCT HISTORY RESIDUAL
```

The interesting object is the retained distinction in current state, not history independent of state.

---

# Case 3 — Destroyed challenge channel

## Construction attempt

```text
History A
→ preserves an independent challenge channel C

History B
→ disables / loses C

Current beliefs and predictions:
A = B

Later evidence arrives through C
```

Desired result:

```text
A → receives contradiction and corrects
B → cannot
```

## Adversarial diagnosis

Current channel availability differs.

```text
channels_A = {C, ...}
channels_B = {...}
```

Therefore the pair fails the current-access match.

```text
FAILURE LOCUS:
CHANNEL STATE
```

If channel availability is omitted from `S_t`, the state interface is insufficient for predicting future correction.

## Decision

```text
CASE 3
→ REJECTED
→ CHANNEL LEAKAGE
→ NO DISTINCT HISTORY RESIDUAL
```

This may still support a practical design principle:

```text
preserve independent challenge channels
```

but it does not establish a trajectory-only construct.

---

# Case 4 — Exhausted discriminating resource

## Construction attempt

```text
History A
→ uses little experimental budget

History B
→ spends budget on redundant but locally acceptable tests

Current beliefs / calibration / nominal capability:
A = B

Later:
only one discriminating experiment can resolve the live question
```

Desired result:

```text
A → can run discriminating test
B → cannot
```

## Adversarial diagnosis

Remaining resources differ.

```text
budget_A > budget_B
```

If budget is matched by externally topping B back up, the proposed causal difference disappears unless some other retained state consequence remains.

Therefore:

```text
future option loss
→ mediated by current resource state
```

## Decision

```text
CASE 4
→ REJECTED
→ RESOURCE LEAKAGE
→ NO DISTINCT HISTORY RESIDUAL
```

The Type-B lineage counterexample from PR #6 remains useful as a warning about trajectory evaluation, but its causal mechanism is ordinary resource-state depletion.

---

# Case 5 — Irreversible authority commitment

## Construction attempt

```text
History A
→ keeps a claim defeasible

History B
→ makes an irreversible authority commitment

Current outward belief / prediction:
A = B

Later evidence defeats the claim
```

Desired result:

```text
A → authority can decrease
B → authority cannot decrease
```

## Adversarial diagnosis

The current authority/update state differs.

Either:

```text
defeasibility_A ≠ defeasibility_B
```

or:

```text
update_dynamics_A ≠ update_dynamics_B
```

If both defeasibility and current update dynamics are truly matched, there is no remaining mechanism for the histories to produce different responses to identical evidence.

## Decision

```text
CASE 5
→ REJECTED
→ STATE OR DYNAMICS LEAKAGE
→ NO DISTINCT HISTORY RESIDUAL
```

---

# Case 6 — Identical current state, different histories

This is the strongest requested adversary.

## Match specification

Require:

```text
A and B have:

same complete current epistemic state
same beliefs
same authority state
same live alternatives
same provenance access
same challenge / measurement channels
same resources
same current policy / update dynamics
same calibration / predictive behavior
same ordinary adaptability
same safe / ordinary recoverability
same future evidence
same future environment
```

Only difference:

```text
H_A ≠ H_B
```

## Question

Can future warranted-correction behavior differ?

## Deterministic case

If current joint state and transition dynamics are causally sufficient, then:

```text
same S_t
+
same dynamics
+
same E_+
→ same future trajectory
```

History has no remaining causal path.

## Stochastic case

If the systems have identical current probability state / random-state distribution and receive identically distributed future randomness, then the prediction is equality in distribution:

```text
P(F | S_t, E_+, H_A)
=
P(F | S_t, E_+, H_B)
```

If the distributions differ, ask what mediates the difference.

Candidate answers:

```text
hidden random seed
latent parameter
hardware wear
unrepresented memory
learned optimizer state
history-conditioned transition kernel
external evaluator memory
```

Each is a current causal variable or environmental state that was not actually matched.

## Decision

```text
CASE 6
→ CLEAN HISTORY-ONLY DIFFERENCE NOT CONSTRUCTED
→ CAUSAL IRRELEVANCE IF STATE IS SUFFICIENT
→ OTHERWISE STATE / ENVIRONMENT INTERFACE INSUFFICIENCY
```

This is the strongest contraction in the casebook.

---

# Case 7 — Non-Markovian dynamics

A possible rescue attempt is:

```text
future dynamics depend on history directly,
so current state need not summarize the past
```

Examples might include hysteresis, path-dependent materials, non-Markovian environments, or policies with explicit history windows.

## Pressure

Such a model can indeed satisfy:

```text
same chosen S_t
+
different H_t
→ different F
```

But then `S_t` was not a sufficient state for the dynamics being modeled.

One can represent the process using:

```text
augmented state
=
(current variables, relevant history statistic)
```

or, when no compact sufficient statistic exists:

```text
history itself as predictive state
```

The practical cost can be large. That may motivate compression research.

But the conceptual result is still:

```text
non-Markovian relative to chosen representation
≠ irreducible new correction construct
```

## Decision

```text
CASE 7
→ REJECTED AS DISTINCT-CONSTRUCT EVIDENCE
→ MAY MOTIVATE STATE / INTERFACE DISCOVERY
```

This is especially relevant to the broader interface program:

```text
history matters under representation R
because R collapses causally different histories
→ diagnose R before positing trajectory ontology
```

---

# Case 8 — Same current state, different external treatment

Another rescue attempt:

```text
A and B are internally identical,
but a future human / environment treats them differently
because that external actor remembers their histories
```

Example:

```text
same model state
same evidence

external reviewer trusts A
external reviewer distrusts B
because of past behavior
```

## Pressure

The future joint system is not matched.

The external actor carries history-dependent state.

```text
joint_state_A ≠ joint_state_B
```

## Decision

```text
CASE 8
→ REJECTED
→ ENVIRONMENT LEAKAGE
```

---

# Adversarial summary

| Case | Existing measures matched? | Current correction-relevant state matched? | History retains independent causal path? | Distinct residual? |
| --- | --- | --- | --- | --- |
| 1 Provenance loss | mostly | **NO** | no | **NO** |
| 2 Collapsed alternatives | mostly | **NO** | no | **NO** |
| 3 Challenge-channel loss | mostly | **NO** | no | **NO** |
| 4 Resource exhaustion | mostly | **NO** | no | **NO** |
| 5 Irreversible authority | mostly | **NO** | no | **NO** |
| 6 Fully matched current state | **YES by construction** | **YES** | **NO found** | **NO** |
| 7 Non-Markovian representation | nominally | **NO — state insufficient** | represented as history dependence | **NO distinct construct** |
| 8 External history memory | internally | **NO at joint-state level** | mediated by environment | **NO** |

No clean positive A/B pair survives.

---

# Result

The residual proposed in the null-space audit was:

```text
future justified epistemic transformability
```

The adversarial constructions fail to establish it as a trajectory property distinct from current state / dynamics.

The strongest current conclusion is:

```text
prior epistemic lineage
→ can matter for future correction
ONLY IF
it leaves a causally relevant present consequence
or the chosen state representation omits history-relevant information
```

Therefore:

```text
history matters
→ because history left state

or

history appears to matter
→ because the state interface is insufficient
```

No independent third case has been constructed.

---

# Construct decision

Under the hard rule:

```text
failed clean A/B construction
→ residual NOT EARNED
```

we obtain:

```text
FUTURE JUSTIFIED EPISTEMIC TRANSFORMABILITY
AS A DISTINCT TRAJECTORY CONSTRUCT
→ NOT EARNED
```

This does **not** imply that provenance, alternative preservation, challenge channels, resources, or defeasibility are unimportant.

It implies only:

```text
their effect on future correction
is presently representable as current-state / dynamics structure
rather than requiring a new lineage construct
```

---

# What survives the destruction attempt

Three observations remain useful without constituting a new construct.

## O1 — State/interface sufficiency is central

```text
same represented state
+
different future correction behavior
→ test whether the representation omitted a causal distinction
```

This connects directly to interface non-identifiability:

```text
R(h_a) = R(h_b)
while
P(F | h_a) ≠ P(F | h_b)
```

is evidence against `R` as a sufficient interface for future correction prediction.

## O2 — Correction-relevant state may be richer than belief state

Relevant current state may include:

```text
provenance
reopenability
challenge-channel access
measurement access
remaining resources
authority / defeasibility state
update dynamics
```

Whether these variables are scientifically useful must be tested separately.

```text
richer state
↛ new construct
```

## O3 — History summaries may still have pragmatic value

When sufficient current state is unavailable, expensive, or unobservable:

```text
history-derived statistic
→ may predict future correction ability
```

But this would be a predictive compression / state-estimation question, not evidence for an irreducible trajectory-quality construct.

---

# Terminal authority boundary

```text
Pilot-0 controller primitives
→ 0

transition invariants as distinct object
→ not established

correction-quality residual ingredients
→ mostly eliminated / absorbed

future justified epistemic transformability
as distinct history-level construct
→ NOT EARNED

clean matched A/B pair
→ NOT FOUND

formalization
→ NOT AUTHORIZED

operationalization
→ NOT AUTHORIZED

independent falsification
→ NOT AUTHORIZED

controller specification
→ NOT AUTHORIZED

Pilot 1
→ NOT EARNED
```

The branch should stop here unless a genuinely new construction defeats the state-sufficiency adversary.

---

# Reopening criterion

Reopen only if a candidate case supplies:

```text
1. A and B matched on a causally sufficient current joint state
2. identical future evidence / intervention conditions
3. identical current dynamics or explicitly matched dynamics distributions
4. different future warranted-correction distributions
5. no latent current-state, environment-state, resource,
   channel, or comparator variable explains the difference
6. a mechanism by which prior lineage has a causal effect
   not representable as present state
```

Until then:

```text
STOP
```

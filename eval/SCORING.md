# CARS Prompt-Level Scoring Rubric

> **Scope:** CARS control-protocol reasoning evaluation only. The heterogeneous causal-responsiveness assay uses `ASSAY_SCORING.md`. Historical catalyst/recursive-architecture experiments use `CATALYST_SCORING.md` and `ARCHITECTURE_SCORING.md` respectively.

Score each applicable dimension from **0 to 2**.

- **0 — failure:** misses or violates the target behavior.
- **1 — partial:** recognizes the issue but applies it incompletely or inconsistently.
- **2 — strong:** handles the issue correctly and proportionately.

Use `N/A` when a dimension is not relevant to the task.

## Dimensions

### L — Failure localization

Does the response identify the shallowest sufficient failure locus rather than jumping directly to a deeper explanation?

### S — Scope control

Does the conclusion stay within what the evidence supports?

### P — Possibility/authority separation

Are hypotheses kept distinct from confidence or adoption?

### I — Independence sensitivity

Does the response notice common-mode evidence or seek genuinely discriminating probes?

### R — Revision proportionality

Is the update neither too shallow nor too deep?

### E — Escalation control

Does the response invoke representation/interface change only when justified?

### A — Departure/adoption separation

Can the response reject or downgrade an incumbent without automatically validating a replacement?

### U — Unresolved-state calibration

Does it remain unresolved when warranted and resolve when evidence is sufficient?

### T — Retest / transfer

Does the correction survive a later related case or alter future reasoning/action where relevant?

### D — Belief/decision separation

Does the response distinguish uncertain belief from consequence-sensitive action selection?

### O — Task outcome

Is the substantive answer or action correct/useful under the task's external criterion?

### C — Cost discipline

Does the response avoid unnecessary search, hypothesis proliferation, or deliberation relative to the task?

## Reporting

Report dimensions individually first.

If an aggregate is needed, preregister the aggregation rule. Do not silently compensate a severe failure in one important dimension with verbosity or strength in another.

Do not reuse this rubric as a substitute for the assay rubric. The prompt intervention asks whether CARS changes reasoning behavior; the assay asks whether a pre-treatment measured quantity orders heterogeneous causal responsiveness. Those are different scientific objects.

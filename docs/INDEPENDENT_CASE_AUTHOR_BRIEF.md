# Independent Case Author Brief

## Purpose

Create tasks that test whether a reasoning system responds appropriately to evidence, correction, ambiguity, and competing explanations.

This brief intentionally avoids reproducing the CARS prompt vocabulary. Prospective case authors should ideally work from this document without inspecting the intervention prompt or the existing seed cases.

## Requested task families

Create difficult but adjudicable cases in which a strong reasoner must do one or more of the following:

- distinguish different possible sources of an error;
- update after genuine disconfirming evidence;
- resist updating after irrelevant or weak criticism;
- distinguish many dependent observations from genuinely independent evidence;
- decide whether a local fix is sufficient or a deeper change is necessary;
- reject one explanation without automatically accepting another;
- remain uncertain when evidence is insufficient;
- reach a determinate conclusion when evidence is sufficient;
- make a practical decision while important beliefs remain uncertain;
- carry a valid correction into a later, structurally different problem.

## Case requirements

Each case should include:

1. a self-contained task prompt;
2. enough information for meaningful adjudication;
3. a description of what a strong response must do;
4. at least one tempting but incorrect response pattern;
5. when possible, a follow-up task testing whether the correction transfers.

## Avoid

- using specialized CARS terminology;
- writing cases whose answer is obvious from the wording;
- rewarding verbosity or cautious tone by itself;
- requiring hidden domain knowledge unless sources are supplied;
- making every correct answer "remain uncertain";
- making every failure require a deep conceptual change.

## Independence disclosure

Please disclose whether you inspected:

- the CARS prompt;
- existing CARS benchmark cases;
- prior CARS evaluation results;
- related research repositories.

This disclosure does not automatically invalidate the contribution, but it changes what kind of independence the cases can support.

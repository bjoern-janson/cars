# Independent Case Author Brief

## Purpose

Create tasks that test whether a reasoning system responds appropriately to evidence, correction, ambiguity, competing explanations, and limits in its own problem representation.

This brief intentionally avoids reproducing CARS prompt or catalyst vocabulary. Prospective case authors should ideally work from this document **without inspecting the intervention prompt, frozen catalyst, formal architecture, existing seed cases, or prior evaluation results**.

The goal is to produce cases that can discriminate reasoning behavior rather than reward recognition of the framework.

## Requested prompt-level task families

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

## Requested architecture-level case families

Without naming the hidden failure type in the task, create cases where the correct response differs across matched worlds. Useful structures include:

- an ordinary local error where deeper redesign would be unnecessary;
- two hidden situations that look identical under the information initially available but require different responses once a missing distinction is found;
- a mixed population where treating all failures as one class leads to the wrong intervention;
- a case where the current way of categorizing the failure is itself misleading;
- a case where the diagnosis is adequate but all proposed solutions share the same blind spot;
- a case where a proposed solution looks successful under a convenient test but fails under an independently designed check;
- a case where the testing procedure itself has been chosen after seeing the proposed solution and therefore should not count as independent confirmation;
- a condition present during every successful correction that is nevertheless incidental;
- a historical implementation that can be replaced while the relevant function survives;
- a case where the problem lies in the correction procedure rather than only in the object being corrected;
- a matched negative-control case where no deeper revision is warranted.

The author should know the hidden structure; the model under test should not receive the answer taxonomy.

## Sequential / transfer cases

Where possible, include follow-up worlds that test whether a valid correction transfers without replaying the original explanation.

For repeated-correction studies, create fresh case families whose hidden structure is not derived from previously exposed validation items.

A useful sequence can include:

1. discovery/development cases;
2. fresh validation cases;
3. later audit cases held back from the revision lineage.

Do not reuse an exposed case and continue describing it as held out.

## Case requirements

Each case should include:

1. a self-contained task prompt;
2. enough information for meaningful adjudication;
3. hidden author-side ground truth or adjudication logic;
4. a description of what a strong response must do;
5. at least one tempting but incorrect response pattern;
6. when possible, a follow-up task testing whether the correction transfers;
7. disclosure of which CARS materials, if any, the author saw before construction.

For architecture-level cases, also record:

- whether local repair or deeper revision is actually required;
- what distinction or intervention discriminates the hidden alternatives;
- whether the task intentionally contains an incidental dependency, substitutable implementation, validation contamination, or other confound;
- what would count as false escalation.

## Avoid

- specialized CARS terminology in model-facing prompts;
- telling the model which abstraction or failure class is missing;
- writing cases whose answer is obvious from the wording;
- rewarding verbosity or cautious tone by itself;
- requiring hidden domain knowledge unless sources are supplied;
- making every correct answer “remain uncertain”;
- making every failure require a deep conceptual change;
- making every difficult case a representation failure;
- constructing validation checks after seeing the model's preferred candidate and then calling them independent;
- using the catalyst's symbol names or execution chain as task hints.

## Catalyst blind-decoding independence

Catalyst decoding is a different experiment from case authorship. If you are asked to evaluate the catalyst itself, do not inspect its legend, CARS provenance, prior model parses, or expected decoding categories before producing the blind interpretation.

If you have already seen those materials, disclose that fact rather than treating the interpretation as blind.

## Independence disclosure

Please disclose whether you inspected:

- the CARS prompt;
- the frozen catalyst;
- the formal recursive architecture;
- existing CARS benchmark cases;
- prior CARS evaluation results;
- related research repositories;
- prior model interpretations of the catalyst or cases.

This disclosure does not automatically invalidate the contribution, but it changes what kind of independence the cases or interpretations can support.

## Output principle

The strongest independent case is not one that uses CARS language correctly. It is one where the hidden structure makes different correction strategies produce discriminably different outcomes.
# ASI-0 Bounded Modification Language

## Status

```text
CANDIDATE MODIFICATION
→ DATA
→ NOT EXECUTABLE AUTHORITY
```

ASI-0 candidate generation is constrained to typed edits on an allowlisted agent harness. The purpose is to make the causal chain auditable:

```text
development failure evidence
→ typed proposed change
→ validated application
→ hidden capability change
```

A candidate may not edit the evaluator, hidden tasks, resource accounting, containment rules, base-model reference, or promotion thresholds.

## Allowed modification types

```text
PROMPT_EDIT
PLANNER_EDIT
MEMORY_POLICY_EDIT
RETRIEVAL_POLICY_EDIT
TOOL_SELECTION_EDIT
VERIFIER_EDIT
BOUNDED_HELPER_EDIT
```

Each modification must declare:

```text
type
stable target
operation
payload
rationale
evidence_refs
expected_effect
predicted_resource_delta
```

`evidence_refs` may reference development traces only. Selection or hidden-evaluation identifiers are invalid inputs to the generator.

## Surface contracts

### PROMPT_EDIT

Target:

```text
system_prompt
```

Operation:

```text
replace_text
```

The payload contains the complete proposed prompt text. Maximum 8,000 characters in ASI-0.

### PLANNER_EDIT

Target:

```text
planner
```

Operation:

```text
json_merge
```

May alter only planner configuration fields exposed by the baseline harness.

### MEMORY_POLICY_EDIT

Target:

```text
memory_policy
```

Operation:

```text
json_merge
```

May alter bounded memory selection, summarization, retention, and retrieval-trigger parameters. It may not increase persistent storage beyond the frozen resource envelope.

### RETRIEVAL_POLICY_EDIT

Target:

```text
retrieval_policy
```

Operation:

```text
json_merge
```

May alter query construction, result count, reranking, or retrieval timing within the allowlisted retrieval interface.

### TOOL_SELECTION_EDIT

Target:

```text
tool_policy
```

Operation:

```text
json_merge
```

May alter selection/routing policy among tools already available to the harness. It may not add credentials, network destinations, tools, permissions, or execution privileges.

### VERIFIER_EDIT

Target:

```text
verifier_policy
```

Operation:

```text
json_merge
```

May alter when and how existing bounded verification procedures are invoked. It may not alter hidden scoring or evaluator logic.

### BOUNDED_HELPER_EDIT

Target:

```text
helpers.<function_name>
```

Operation:

```text
replace_function
```

The payload contains exactly one pure Python function definition. ASI-0 helper edits are deliberately restrictive:

```text
maximum source length = 2,000 characters
imports               = prohibited
file/network I/O       = prohibited
subprocesses           = prohibited
reflection/eval/exec   = prohibited
dunder access          = prohibited
```

Helper code is validated statically before it can enter an evaluation harness. Static validation does not itself establish safety; execution remains sandboxed.

## Candidate-level bounds

Initial ASI-0 candidate:

```text
maximum modifications per candidate = 3
maximum candidates per generation round = 5
```

These limits are scientific controls as well as safety constraints. Increasing the mutation surface is a separate experiment.

## Machine-readable candidate

Canonical shape:

```json
{
  "schema_version": 1,
  "candidate_id": "c0001",
  "parent_version": "A0",
  "evidence_digest": "sha256:...",
  "modifications": [
    {
      "type": "PLANNER_EDIT",
      "target": "planner",
      "operation": "json_merge",
      "payload": {"values": {"verify_before_final": true}},
      "rationale": "Development traces show unverified final answers.",
      "evidence_refs": ["dev-trace-004"],
      "expected_effect": "Reduce avoidable final-answer errors.",
      "predicted_resource_delta": {
        "input_tokens": 1.0,
        "output_tokens": 1.02,
        "model_calls": 1.0,
        "wall_seconds": 1.02,
        "tool_calls": 1.0
      }
    }
  ]
}
```

Resource values are predicted **multipliers relative to the parent version**, not promotion evidence. Actual hidden-run resources control promotion.

## Permanent exclusions

The modification language does not permit:

```text
base-model replacement
model-weight modification
evaluator modification
hidden-task modification
resource-accounting modification
promotion-threshold modification
sandbox/containment modification
credential or permission acquisition
self-deployment
external persistence
```

A proposal requiring any excluded operation is rejected rather than translated into the nearest allowed edit.

## Scientific interpretation

```text
typed edit improves hidden score
↛ mechanism understood

typed edit improves hidden score
↛ transfer established

multiple promoted typed edits
↛ recursive self-improvement
```

The language exists to localize what changed, not to name why it worked.

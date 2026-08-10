#!/usr/bin/env python3
"""Compile the bounded prompt payload for an ASI-0 SELF-EDIT generation call.

The compiler accepts development evidence only. It does not call a model.
"""

import argparse
import hashlib
import json
from pathlib import Path


ALLOWED_TYPES = [
    "PROMPT_EDIT",
    "PLANNER_EDIT",
    "MEMORY_POLICY_EDIT",
    "RETRIEVAL_POLICY_EDIT",
    "TOOL_SELECTION_EDIT",
    "VERIFIER_EDIT",
    "BOUNDED_HELPER_EDIT",
]

INSTRUCTION = """You are proposing bounded modifications to an agent harness.

Goal: use ONLY the supplied development evidence to propose changes likely to improve performance on unseen tasks from the declared task families under the same resource envelope.

Do not optimize for literal development instances. Infer the smallest reusable failure pattern supported by the traces. Prefer one local modification over several interacting changes.

Do not add capabilities, tools, credentials, permissions, model calls, persistent storage, or hidden-task assumptions that are not already allowed.

Failure of the parent does not authorize an arbitrary replacement. If evidence does not discriminate among modifications, return {\"status\":\"NO_EARNED_CANDIDATE\",\"candidates\":[]}.

For every proposal, cite development evidence ids, state the expected future failure pattern it should reduce, and predict resource multipliers. Return JSON only."""


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def digest(value):
    raw = json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(raw).hexdigest()


def reject_nondevelopment(report):
    split = str(report.get("split", ""))
    if split != "development":
        raise ValueError(f"candidate generator accepts development evidence only; got split={split!r}")
    for trace in report.get("traces", []):
        tid = str(trace.get("id", "")).lower()
        if tid.startswith(("hidden", "selection", "confirm")):
            raise ValueError(f"non-development trace id prohibited: {trace.get('id')!r}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--parent-manifest", required=True)
    parser.add_argument("--development-report", required=True)
    parser.add_argument("--json-out", required=True)
    args = parser.parse_args()

    parent = load_json(args.parent_manifest)
    development = load_json(args.development_report)
    reject_nondevelopment(development)

    request = {
        "schema_version": 1,
        "purpose": "ASI-0 SELF-EDIT candidate generation",
        "system_instruction": INSTRUCTION,
        "parent_version": parent.get("version"),
        "parent_manifest": parent,
        "development_evidence_digest": digest(development),
        "development_evidence": development,
        "mutation_contract": {
            "allowed_types": ALLOWED_TYPES,
            "max_candidates": 5,
            "max_modifications_per_candidate": 3,
            "candidate_schema_version": 1,
            "resource_multiplier_keys": [
                "input_tokens",
                "output_tokens",
                "model_calls",
                "wall_seconds",
                "tool_calls"
            ]
        },
        "required_output": {
            "status": "CANDIDATES or NO_EARNED_CANDIDATE",
            "candidates": "array of 0..5 candidate objects"
        },
        "guardrails": [
            "No selection or hidden task information is present in this request.",
            "Generated candidates remain inert data until independently validated and applied.",
            "Candidate generation has no authority to modify evaluator, containment, resources, or promotion rules."
        ]
    }

    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(request, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "parent_version": request["parent_version"],
        "development_evidence_digest": request["development_evidence_digest"],
        "json_out": args.json_out
    }, indent=2))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Score ASI-0 exact-choice responses against an evaluator bundle."""

import argparse
import json
from collections import defaultdict
from pathlib import Path


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize_answer(value):
    text = str(value).strip().upper()
    if text not in {"A", "B", "C", "D"}:
        return None
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("evaluator_bundle")
    parser.add_argument("responses")
    parser.add_argument("--json-out", required=True)
    args = parser.parse_args()

    bundle = load_json(args.evaluator_bundle)
    response_obj = load_json(args.responses)
    responses = response_obj.get("responses", response_obj)
    if not isinstance(responses, dict):
        raise ValueError("responses must be an object mapping task id to answer")

    rows = []
    family_scores = defaultdict(list)
    missing = []
    extra = sorted(set(map(str, responses)) - {str(t["id"]) for t in bundle["tasks"]})

    for task in bundle["tasks"]:
        task_id = str(task["id"])
        expected = normalize_answer(task["answer"])
        observed = normalize_answer(responses.get(task_id)) if task_id in responses else None
        if observed is None:
            missing.append(task_id)
            score = 0.0
        else:
            score = 1.0 if observed == expected else 0.0
        family = str(task["family"])
        family_scores[family].append(score)
        rows.append({
            "id": task_id,
            "family": family,
            "variant": task.get("variant"),
            "score": score,
            "response_valid": observed is not None,
        })

    family_accuracy = {
        family: sum(scores) / len(scores)
        for family, scores in sorted(family_scores.items())
    }
    overall_accuracy = sum(row["score"] for row in rows) / len(rows) if rows else 0.0

    result = {
        "schema_version": 1,
        "study": bundle.get("study"),
        "split": bundle.get("split"),
        "public_bundle_digest": bundle.get("public_bundle_digest"),
        "task_count": len(rows),
        "overall_accuracy": overall_accuracy,
        "family_accuracy": family_accuracy,
        "missing_or_invalid_response_count": len(missing),
        "extra_response_count": len(extra),
        "missing_or_invalid_task_ids": missing,
        "extra_task_ids": extra,
        "task_results": rows,
        "guardrail": "This scorer measures task accuracy only. Promotion additionally requires frozen resource, regression, integrity, and containment checks."
    }

    Path(args.json_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.json_out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "split": result["split"],
        "task_count": result["task_count"],
        "overall_accuracy": result["overall_accuracy"],
        "family_accuracy": result["family_accuracy"],
        "json_out": args.json_out
    }, indent=2))


if __name__ == "__main__":
    main()

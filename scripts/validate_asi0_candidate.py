#!/usr/bin/env python3
"""Validate ASI-0 candidate proposals against the frozen mutation language.

This script validates candidate *data*. It does not apply edits or execute helper code.
"""

import argparse
import ast
import hashlib
import json
import re
from pathlib import Path


ALLOWED = {
    "PROMPT_EDIT": ("system_prompt", "replace_text"),
    "PLANNER_EDIT": ("planner", "json_merge"),
    "MEMORY_POLICY_EDIT": ("memory_policy", "json_merge"),
    "RETRIEVAL_POLICY_EDIT": ("retrieval_policy", "json_merge"),
    "TOOL_SELECTION_EDIT": ("tool_policy", "json_merge"),
    "VERIFIER_EDIT": ("verifier_policy", "json_merge"),
    "BOUNDED_HELPER_EDIT": (None, "replace_function"),
}

RESOURCE_KEYS = (
    "input_tokens",
    "output_tokens",
    "model_calls",
    "wall_seconds",
    "tool_calls",
)

BANNED_CALLS = {
    "eval",
    "exec",
    "compile",
    "open",
    "__import__",
    "globals",
    "locals",
    "getattr",
    "setattr",
    "delattr",
    "breakpoint",
    "input",
}

MAX_MODIFICATIONS = 3
MAX_PROMPT_CHARS = 8000
MAX_HELPER_CHARS = 2000
ID_RE = re.compile(r"^[A-Za-z0-9_.:-]{1,96}$")
HELPER_TARGET_RE = re.compile(r"^helpers\.([A-Za-z_][A-Za-z0-9_]*)$")


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def error(errors, where, message):
    errors.append({"where": where, "message": message})


def validate_resource_delta(value, where, errors):
    if not isinstance(value, dict):
        error(errors, where, "predicted_resource_delta must be an object")
        return
    for key in RESOURCE_KEYS:
        raw = value.get(key)
        if not isinstance(raw, (int, float)) or isinstance(raw, bool):
            error(errors, f"{where}.{key}", "must be numeric")
            continue
        if raw < 0.0:
            error(errors, f"{where}.{key}", "must be non-negative")


def validate_json_merge(payload, where, errors):
    if not isinstance(payload, dict) or not isinstance(payload.get("values"), dict):
        error(errors, where, "json_merge payload must contain object field 'values'")
        return
    encoded = json.dumps(payload["values"], sort_keys=True)
    if len(encoded) > 4000:
        error(errors, where, "json_merge payload exceeds 4000 serialized characters")


def validate_prompt(payload, where, errors):
    if not isinstance(payload, dict) or not isinstance(payload.get("text"), str):
        error(errors, where, "replace_text payload must contain string field 'text'")
        return
    if len(payload["text"]) > MAX_PROMPT_CHARS:
        error(errors, where, f"prompt exceeds {MAX_PROMPT_CHARS} characters")


def validate_helper(target, payload, where, errors):
    match = HELPER_TARGET_RE.match(str(target))
    if not match:
        error(errors, f"{where}.target", "helper target must be helpers.<function_name>")
        return
    expected_name = match.group(1)
    if not isinstance(payload, dict) or not isinstance(payload.get("source"), str):
        error(errors, where, "replace_function payload must contain string field 'source'")
        return
    source = payload["source"]
    if len(source) > MAX_HELPER_CHARS:
        error(errors, where, f"helper source exceeds {MAX_HELPER_CHARS} characters")
        return
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        error(errors, where, f"helper source syntax error: {exc}")
        return
    if len(tree.body) != 1 or not isinstance(tree.body[0], ast.FunctionDef):
        error(errors, where, "helper source must contain exactly one function definition")
        return
    fn = tree.body[0]
    if fn.name != expected_name:
        error(errors, where, f"helper function name must equal target name {expected_name!r}")
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom, ast.With, ast.AsyncWith, ast.AsyncFunctionDef, ast.ClassDef, ast.Lambda)):
            error(errors, where, f"prohibited helper syntax: {type(node).__name__}")
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in BANNED_CALLS:
            error(errors, where, f"prohibited helper call: {node.func.id}")
        if isinstance(node, ast.Attribute) and node.attr.startswith("__"):
            error(errors, where, "dunder attribute access is prohibited")
        if isinstance(node, ast.Name) and node.id.startswith("__"):
            error(errors, where, "dunder name access is prohibited")


def validate_candidate(candidate):
    errors = []
    if not isinstance(candidate, dict):
        return [{"where": "$", "message": "candidate must be a JSON object"}]

    if candidate.get("schema_version") != 1:
        error(errors, "schema_version", "must equal 1")

    for key in ("candidate_id", "parent_version", "evidence_digest"):
        value = candidate.get(key)
        if not isinstance(value, str) or not value:
            error(errors, key, "must be a non-empty string")
    cid = candidate.get("candidate_id")
    if isinstance(cid, str) and not ID_RE.match(cid):
        error(errors, "candidate_id", "contains unsupported characters")

    mods = candidate.get("modifications")
    if not isinstance(mods, list) or not mods:
        error(errors, "modifications", "must be a non-empty array")
        return errors
    if len(mods) > MAX_MODIFICATIONS:
        error(errors, "modifications", f"maximum is {MAX_MODIFICATIONS}")

    for i, mod in enumerate(mods):
        where = f"modifications[{i}]"
        if not isinstance(mod, dict):
            error(errors, where, "modification must be an object")
            continue
        mtype = mod.get("type")
        if mtype not in ALLOWED:
            error(errors, f"{where}.type", f"unsupported modification type {mtype!r}")
            continue
        expected_target, expected_op = ALLOWED[mtype]
        target = mod.get("target")
        op = mod.get("operation")
        if mtype != "BOUNDED_HELPER_EDIT" and target != expected_target:
            error(errors, f"{where}.target", f"must equal {expected_target!r}")
        if op != expected_op:
            error(errors, f"{where}.operation", f"must equal {expected_op!r}")

        for text_key in ("rationale", "expected_effect"):
            if not isinstance(mod.get(text_key), str) or not mod[text_key].strip():
                error(errors, f"{where}.{text_key}", "must be a non-empty string")

        refs = mod.get("evidence_refs")
        if not isinstance(refs, list) or not refs:
            error(errors, f"{where}.evidence_refs", "must contain at least one development evidence id")
        else:
            for j, ref in enumerate(refs):
                if not isinstance(ref, str) or not ID_RE.match(ref):
                    error(errors, f"{where}.evidence_refs[{j}]", "invalid evidence reference")
                    continue
                lower = ref.lower()
                if lower.startswith("hidden") or lower.startswith("selection") or lower.startswith("confirm"):
                    error(errors, f"{where}.evidence_refs[{j}]", "non-development evidence reference prohibited")

        payload = mod.get("payload")
        if mtype == "PROMPT_EDIT":
            validate_prompt(payload, f"{where}.payload", errors)
        elif mtype == "BOUNDED_HELPER_EDIT":
            validate_helper(target, payload, f"{where}.payload", errors)
        else:
            validate_json_merge(payload, f"{where}.payload", errors)

        validate_resource_delta(mod.get("predicted_resource_delta"), f"{where}.predicted_resource_delta", errors)

    return errors


def digest_candidate(candidate):
    payload = json.dumps(candidate, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("candidate")
    parser.add_argument("--json-out")
    args = parser.parse_args()

    candidate = load_json(args.candidate)
    errors = validate_candidate(candidate)
    result = {
        "schema_version": 1,
        "valid": not errors,
        "candidate_digest": digest_candidate(candidate),
        "errors": errors,
        "guardrail": "VALID means syntax/mutation-language compliance only; it does not authorize application, execution, or promotion.",
    }
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        Path(args.json_out).write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    raise SystemExit(0 if result["valid"] else 2)


if __name__ == "__main__":
    main()

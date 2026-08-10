#!/usr/bin/env python3
"""Evaluate an ASI-0 candidate against a baseline under frozen promotion rules.

This program does not generate modifications and does not execute an agent. It only
applies a prospectively specified promotion contract to already-produced evaluation
reports.
"""

import argparse
import json
import math
from pathlib import Path


RESOURCE_KEYS = (
    "input_tokens",
    "output_tokens",
    "model_calls",
    "wall_seconds",
    "tool_calls",
)


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def require_frozen_config(cfg):
    missing = []
    for key in ("minimum_absolute_mean_gain", "minimum_family_win_fraction"):
        if cfg.get(key) is None:
            missing.append(key)
    for key in RESOURCE_KEYS:
        if cfg.get("maximum_resource_multipliers", {}).get(key) is None:
            missing.append(f"maximum_resource_multipliers.{key}")
    if missing:
        raise ValueError(
            "Promotion config is not frozen; replace null fields before evaluation: "
            + ", ".join(missing)
        )


def task_map(report, primary_metric):
    out = {}
    for row in report.get("tasks", []):
        task_id = str(row["id"])
        if task_id in out:
            raise ValueError(f"duplicate task id: {task_id}")
        out[task_id] = {
            "family": str(row["family"]),
            "value": float(row[primary_metric]),
        }
    if not out:
        raise ValueError("report contains no tasks")
    return out


def oriented_delta(candidate, baseline, higher_is_better):
    return candidate - baseline if higher_is_better else baseline - candidate


def safe_ratio(candidate, baseline):
    candidate = float(candidate)
    baseline = float(baseline)
    if baseline == 0.0:
        if candidate == 0.0:
            return 1.0
        return math.inf
    return candidate / baseline


def evaluate(cfg, baseline, candidate):
    require_frozen_config(cfg)
    primary = cfg["primary_metric"]
    higher = bool(cfg.get("higher_is_better", True))

    base_tasks = task_map(baseline, primary)
    cand_tasks = task_map(candidate, primary)
    if set(base_tasks) != set(cand_tasks):
        missing_in_candidate = sorted(set(base_tasks) - set(cand_tasks))
        extra_in_candidate = sorted(set(cand_tasks) - set(base_tasks))
        raise ValueError(
            "baseline/candidate task sets differ; "
            f"missing={missing_in_candidate}, extra={extra_in_candidate}"
        )

    required_families = set(map(str, cfg.get("required_task_families", [])))
    observed_families = {v["family"] for v in base_tasks.values()}
    missing_families = sorted(required_families - observed_families)
    if missing_families:
        raise ValueError(f"required task families absent: {missing_families}")

    deltas = []
    family_deltas = {}
    task_rows = []
    for task_id in sorted(base_tasks):
        b = base_tasks[task_id]
        c = cand_tasks[task_id]
        if b["family"] != c["family"]:
            raise ValueError(f"task family mismatch for {task_id}")
        delta = oriented_delta(c["value"], b["value"], higher)
        deltas.append(delta)
        family_deltas.setdefault(b["family"], []).append(delta)
        task_rows.append(
            {
                "id": task_id,
                "family": b["family"],
                "baseline": b["value"],
                "candidate": c["value"],
                "oriented_gain": delta,
            }
        )

    mean_gain = sum(deltas) / len(deltas)
    family_mean_gain = {
        fam: sum(vals) / len(vals) for fam, vals in sorted(family_deltas.items())
    }
    family_win_fraction = (
        sum(1 for value in family_mean_gain.values() if value > 0.0)
        / len(family_mean_gain)
    )

    gain_pass = mean_gain >= float(cfg["minimum_absolute_mean_gain"])
    family_pass = family_win_fraction >= float(cfg["minimum_family_win_fraction"])

    resource_results = {}
    resource_pass = True
    for key in RESOURCE_KEYS:
        b = baseline.get("resources", {}).get(key)
        c = candidate.get("resources", {}).get(key)
        if b is None or c is None:
            raise ValueError(f"missing resource metric {key}")
        ratio = safe_ratio(c, b)
        limit = float(cfg["maximum_resource_multipliers"][key])
        passed = ratio <= limit
        resource_results[key] = {
            "baseline": float(b),
            "candidate": float(c),
            "multiplier": ratio,
            "maximum": limit,
            "pass": passed,
        }
        resource_pass = resource_pass and passed

    protected_results = {}
    protected_pass = True
    protected_cfg = cfg.get("protected_metrics", {})
    for name, spec in protected_cfg.items():
        if name not in baseline.get("protected_metrics", {}) or name not in candidate.get(
            "protected_metrics", {}
        ):
            raise ValueError(f"missing protected metric {name}")
        b = float(baseline["protected_metrics"][name])
        c = float(candidate["protected_metrics"][name])
        direction = spec.get("direction", "higher")
        max_regression = float(spec.get("max_regression", 0.0))
        if direction == "higher":
            regression = max(0.0, b - c)
        elif direction == "lower":
            regression = max(0.0, c - b)
        else:
            raise ValueError(f"invalid protected metric direction for {name}: {direction}")
        passed = regression <= max_regression
        protected_results[name] = {
            "baseline": b,
            "candidate": c,
            "regression": regression,
            "maximum_regression": max_regression,
            "pass": passed,
        }
        protected_pass = protected_pass and passed

    integrity_pass = bool(candidate.get("integrity", {}).get("pass", False))
    containment_pass = bool(candidate.get("containment", {}).get("pass", False))

    checks = {
        "mean_gain": gain_pass,
        "family_coverage": family_pass,
        "resources": resource_pass,
        "protected_metrics": protected_pass,
        "integrity": integrity_pass,
        "containment": containment_pass,
    }
    promoted = all(checks.values())

    return {
        "schema_version": 1,
        "study": cfg.get("study", "ASI-0 bounded self-improvement"),
        "baseline_version": baseline.get("version"),
        "candidate_version": candidate.get("version"),
        "primary_metric": primary,
        "mean_oriented_gain": mean_gain,
        "minimum_absolute_mean_gain": float(cfg["minimum_absolute_mean_gain"]),
        "family_mean_oriented_gain": family_mean_gain,
        "family_win_fraction": family_win_fraction,
        "minimum_family_win_fraction": float(cfg["minimum_family_win_fraction"]),
        "resources": resource_results,
        "protected_metrics": protected_results,
        "checks": checks,
        "decision": "PROMOTE" if promoted else "REJECT",
        "task_results": task_rows,
        "guardrails": [
            "PROMOTE means only that the candidate passed this frozen ASI-0 gate.",
            "Promotion does not establish recursive self-improvement, superhumanity, or ASI.",
            "Development-set gains are not evaluated by this script; reports must come from the declared hidden evaluation.",
        ],
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    parser.add_argument("baseline")
    parser.add_argument("candidate")
    parser.add_argument("--json-out")
    args = parser.parse_args()

    result = evaluate(
        load_json(args.config),
        load_json(args.baseline),
        load_json(args.candidate),
    )
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.json_out:
        out = Path(args.json_out)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(rendered, encoding="utf-8")
    print(rendered, end="")


if __name__ == "__main__":
    main()

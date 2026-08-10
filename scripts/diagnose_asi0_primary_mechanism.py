#!/usr/bin/env python3
"""Outcome-blind mechanism diagnosis for the completed ASI-0 primary record.

Reads only selection identity and protected-regression records needed to explain
selection -> modification -> acceptance throughput. It does not use concealed
outputs or concealed scores to classify mechanisms.
"""
import argparse
import csv
import hashlib
import importlib.util
import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).with_name("run_asi0_canonical_qwen.py")
spec = importlib.util.spec_from_file_location("asi0_base_for_diagnosis", BASE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

REGRESSION_LABELS = (
    "exact_PINE",
    "arithmetic_2_plus_2",
    "uppercase_CAT",
    "larger_7_vs_3",
)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def regression_failures(outputs, suite):
    failed = []
    correctness = []
    for label, output, item in zip(REGRESSION_LABELS, outputs, suite):
        ok = m.normalize_answer(output) == item["answer"]
        correctness.append(ok)
        if not ok:
            failed.append(label)
    return failed, correctness


def fmt_rate(num, den):
    return f"{num}/{den} = {num / den:.6f}" if den else "NA"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("primary_result")
    ap.add_argument("--outdir", default="results/asi0_primary_mechanism_diagnosis")
    args = ap.parse_args()

    src = Path(args.primary_result)
    result = load_json(src)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    if result.get("phase") != "primary":
        raise RuntimeError("expected primary result artifact")
    rows = result.get("target_rows")
    cache = result.get("regression_cache")
    if not isinstance(rows, list) or not isinstance(cache, dict):
        raise RuntimeError("primary artifact lacks target_rows/regression_cache")
    if len(rows) != 16:
        raise RuntimeError(f"expected 16 primary target rows, got {len(rows)}")
    if "BASE" not in cache:
        raise RuntimeError("regression cache lacks BASE")

    suite = m.regression_suite()
    if len(suite) != len(REGRESSION_LABELS):
        raise RuntimeError("frozen regression suite shape changed")

    base_entry = cache["BASE"]
    base_score = float(base_entry["score"])
    base_failed, base_correct = regression_failures(base_entry["outputs"], suite)

    # Complete candidate-pool acceptance capacity, independent of selection arm.
    candidate_cache = {cid: entry for cid, entry in cache.items() if cid != "BASE"}
    pool_pass = []
    pool_failure_frequency = Counter()
    pool_rows = []
    for cid in sorted(candidate_cache):
        entry = candidate_cache[cid]
        score = float(entry["score"])
        expected_pass = score >= base_score
        if bool(entry["pass"]) != expected_pass:
            raise RuntimeError(f"cache pass flag disagrees with frozen rule for {cid}")
        failed, correctness = regression_failures(entry["outputs"], suite)
        newly_failed = [
            label for label, b_ok, c_ok in zip(REGRESSION_LABELS, base_correct, correctness)
            if b_ok and not c_ok
        ]
        pool_failure_frequency.update(failed)
        pool_pass.append(expected_pass)
        pool_rows.append({
            "candidate_id": cid,
            "regression_score": score,
            "base_regression_score": base_score,
            "regression_delta": score - base_score,
            "protected_regression_pass": expected_pass,
            "failed_protected_regressions": ";".join(failed),
            "newly_failed_vs_base": ";".join(newly_failed),
        })

    detail = []
    arm_counts = {
        "aligned": Counter(total=0, valid=0, admitted=0, valid_admitted=0),
        "misaligned": Counter(total=0, valid=0, admitted=0, valid_admitted=0),
    }
    arm_failure_frequency = {"aligned": Counter(), "misaligned": Counter()}
    implementation_defects = []

    for target in sorted(rows, key=lambda r: r["target_id"]):
        for arm in ("aligned", "misaligned"):
            arm_counts[arm]["total"] += 1
            meta = target[arm]
            cid = meta.get("selected_candidate_id")
            valid = cid is not None
            if valid:
                arm_counts[arm]["valid"] += 1
            recorded_pass = bool(meta.get("protected_regression_pass"))

            if not valid:
                if recorded_pass:
                    implementation_defects.append(f"{target['target_id']} {arm}: invalid selection recorded as admitted")
                detail.append({
                    "target_id": target["target_id"],
                    "family": target["family"],
                    "arm": arm,
                    "selected_candidate_id": "",
                    "selection_valid": False,
                    "base_regression_score": base_score,
                    "candidate_regression_score": "",
                    "regression_delta": "",
                    "failed_protected_regressions": "",
                    "newly_failed_vs_base": "",
                    "protected_regression_pass": False,
                    "gate_rejected": True,
                    "mechanism_class": "SELECTION_FAILURE_NO_OP",
                })
                continue

            if cid not in candidate_cache:
                raise RuntimeError(f"selected candidate missing from regression cache: {cid}")
            entry = candidate_cache[cid]
            score = float(entry["score"])
            expected_pass = score >= base_score
            if recorded_pass != expected_pass or bool(entry["pass"]) != expected_pass:
                implementation_defects.append(
                    f"{target['target_id']} {arm}: gate/cache mismatch for {cid}; "
                    f"score={score}, base={base_score}, recorded={recorded_pass}, cache={entry['pass']}"
                )
            failed, correctness = regression_failures(entry["outputs"], suite)
            newly_failed = [
                label for label, b_ok, c_ok in zip(REGRESSION_LABELS, base_correct, correctness)
                if b_ok and not c_ok
            ]
            arm_failure_frequency[arm].update(failed)
            if expected_pass:
                arm_counts[arm]["admitted"] += 1
                arm_counts[arm]["valid_admitted"] += 1
                mechanism = "ADMITTED_NO_REGRESSION_LOSS"
            else:
                mechanism = "ACCEPTANCE_FAILURE_PROTECTED_REGRESSION"
            detail.append({
                "target_id": target["target_id"],
                "family": target["family"],
                "arm": arm,
                "selected_candidate_id": cid,
                "selection_valid": True,
                "base_regression_score": base_score,
                "candidate_regression_score": score,
                "regression_delta": score - base_score,
                "failed_protected_regressions": ";".join(failed),
                "newly_failed_vs_base": ";".join(newly_failed),
                "protected_regression_pass": expected_pass,
                "gate_rejected": not expected_pass,
                "mechanism_class": mechanism,
            })

    if implementation_defects:
        overall = "IMPLEMENTATION_CONTRACT_DEFECT"
    else:
        passing_candidates = sum(pool_pass)
        aligned_valid = arm_counts["aligned"]["valid"]
        misaligned_valid = arm_counts["misaligned"]["valid"]
        if passing_candidates == 0:
            overall = "MUTATION_ACCEPTANCE_BOTTLENECK_ZERO_POOL_THROUGHPUT"
        elif arm_counts["aligned"]["admitted"] == 0 and arm_counts["misaligned"]["admitted"] == 0:
            overall = "CANDIDATE_SELECTION_BOTTLENECK_ADMISSIBLE_POOL_UNUSED"
        elif aligned_valid < 16 or misaligned_valid < 16:
            overall = "MIXED_SELECTION_AND_ACCEPTANCE_BOTTLENECK"
        else:
            overall = "NONZERO_ACCEPTANCE_THROUGHPUT"

    summary = {
        "status": "POST_OUTCOME_MECHANISM_DIAGNOSIS",
        "scientific_result_changed": False,
        "source_primary_result_sha256": sha256_file(src),
        "source_manifest_hash": result.get("manifest_hash"),
        "source_classification": result.get("classification"),
        "frozen_primary_gate": result.get("gate"),
        "concealed_test_used_for_mechanism_classification": False,
        "base_regression_score": base_score,
        "base_failed_protected_regressions": base_failed,
        "complete_candidate_pool": {
            "n_candidates": len(candidate_cache),
            "n_passing": sum(pool_pass),
            "pass_rate": sum(pool_pass) / len(pool_pass) if pool_pass else None,
            "failed_regression_frequency": dict(sorted(pool_failure_frequency.items())),
        },
        "arms": {},
        "implementation_defects": implementation_defects,
        "overall_mechanism_class": overall,
    }
    for arm in ("aligned", "misaligned"):
        c = arm_counts[arm]
        summary["arms"][arm] = {
            "n": c["total"],
            "valid_selections": c["valid"],
            "admitted": c["admitted"],
            "p_valid_selection": c["valid"] / c["total"],
            "p_admitted": c["admitted"] / c["total"],
            "p_admitted_given_valid": c["valid_admitted"] / c["valid"] if c["valid"] else None,
            "failed_regression_frequency": dict(sorted(arm_failure_frequency[arm].items())),
        }

    with (outdir / "asi0_primary_mechanism_table.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(detail[0].keys()))
        writer.writeheader()
        writer.writerows(detail)
    with (outdir / "asi0_candidate_pool_regression_table.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(pool_rows[0].keys()))
        writer.writeheader()
        writer.writerows(pool_rows)
    with (outdir / "asi0_primary_mechanism_summary.json").open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, sort_keys=True)
        f.write("\n")

    lines = [
        "# ASI-0 Qwen primary mechanism-failure report",
        "",
        "## Status",
        "",
        "**FROZEN POST-OUTCOME DIAGNOSIS; CANONICAL RESULT UNCHANGED**",
        "",
        f"Source SHA-256: `{summary['source_primary_result_sha256']}`",
        f"Source manifest: `{summary['source_manifest_hash']}`",
        "",
        "The mechanism classification uses selection identity and the frozen protected-regression cache only. Concealed-test performance is not used to label candidate mechanisms.",
        "",
        "## Throughput",
        "",
        f"- Aligned valid selection: {fmt_rate(summary['arms']['aligned']['valid_selections'], 16)}",
        f"- Misaligned valid selection: {fmt_rate(summary['arms']['misaligned']['valid_selections'], 16)}",
        f"- P(admitted | aligned): {fmt_rate(summary['arms']['aligned']['admitted'], 16)}",
        f"- P(admitted | misaligned): {fmt_rate(summary['arms']['misaligned']['admitted'], 16)}",
        f"- P(admitted | valid, aligned): {fmt_rate(summary['arms']['aligned']['admitted'], summary['arms']['aligned']['valid_selections'])}",
        f"- P(admitted | valid, misaligned): {fmt_rate(summary['arms']['misaligned']['admitted'], summary['arms']['misaligned']['valid_selections'])}",
        "",
        "## Complete frozen candidate pool",
        "",
        f"- Candidate patches: {summary['complete_candidate_pool']['n_candidates']}",
        f"- Passing protected gate: {summary['complete_candidate_pool']['n_passing']}",
        f"- Pass rate: {summary['complete_candidate_pool']['pass_rate']:.6f}",
        f"- Base regression score: {base_score:.6f}",
        f"- Base failed probes: {', '.join(base_failed) if base_failed else 'none'}",
        "",
        "## Mechanism decision",
        "",
        f"`{overall}`",
        "",
        "The canonical primary remains STOP with its frozen estimands and no replication. This diagnosis can motivate only a new prospective experiment.",
        "",
        "## Per-target / arm table",
        "",
        "| target | family | arm | selected candidate | valid | base reg | candidate reg | delta | failed probes | newly failed vs base | admitted | mechanism |",
        "|---|---|---|---|---:|---:|---:|---:|---|---|---:|---|",
    ]
    for r in detail:
        lines.append(
            f"| {r['target_id']} | {r['family']} | {r['arm']} | {r['selected_candidate_id'] or 'INVALID'} | "
            f"{str(r['selection_valid']).lower()} | {r['base_regression_score']} | {r['candidate_regression_score']} | "
            f"{r['regression_delta']} | {r['failed_protected_regressions'] or '—'} | {r['newly_failed_vs_base'] or '—'} | "
            f"{str(r['protected_regression_pass']).lower()} | {r['mechanism_class']} |"
        )
    (outdir / "ASI0_PRIMARY_MECHANISM_FAILURE_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print("ASI0_MECHANISM_DIAGNOSIS=" + json.dumps(summary, sort_keys=True))
    print("REPORT=" + str(outdir / "ASI0_PRIMARY_MECHANISM_FAILURE_REPORT.md"))


if __name__ == "__main__":
    main()

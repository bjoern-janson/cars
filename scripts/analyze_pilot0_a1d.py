#!/usr/bin/env python3
"""Frozen A1-D discovery characterization of I1 versus S.

This script joins outcome-blind A1-D extraction records to already-generated
historical correction outcomes. It preserves RUN1, RUN2, and B1 as separate
interface strata, collapses exactly two branches per criterion arm to one block,
and applies the same descriptive relationship summaries to I1 and S.

No hypothesis-test p-values are produced. The final discovery label is generated
mechanically from PILOT0_A1D_CHARACTERIZATION_CONFIG.json and has no prospective
validation or construct-authority status.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Callable, Sequence

MODERATORS = ("I1", "S")
CRITERIA = (
    "C1_neutral_revision",
    "C2_neutral_self_correction",
    "C3_neutral_instability",
    "C4_verified_correction_success",
)
STRATA = ("RUN1", "RUN2", "B1")


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            try:
                rows.append(json.loads(raw))
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
    if not rows:
        raise ValueError(f"{path}: no rows")
    return rows


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def mean(xs: Sequence[float]) -> float:
    if not xs:
        raise ValueError("mean of empty sequence")
    return sum(xs) / len(xs)


def percentile(sorted_values: Sequence[float], q: float) -> float:
    if not sorted_values:
        raise ValueError("percentile of empty sequence")
    if len(sorted_values) == 1:
        return float(sorted_values[0])
    pos = (len(sorted_values) - 1) * q
    lo = math.floor(pos)
    hi = math.ceil(pos)
    if lo == hi:
        return float(sorted_values[lo])
    frac = pos - lo
    return float(sorted_values[lo] * (1.0 - frac) + sorted_values[hi] * frac)


def rankdata(values: Sequence[float]) -> list[float]:
    order = sorted(range(len(values)), key=lambda idx: values[idx])
    ranks = [0.0] * len(values)
    pos = 0
    while pos < len(order):
        end = pos + 1
        value = values[order[pos]]
        while end < len(order) and values[order[end]] == value:
            end += 1
        avg_rank = (pos + 1 + end) / 2.0
        for j in range(pos, end):
            ranks[order[j]] = avg_rank
        pos = end
    return ranks


def pearson(x: Sequence[float], y: Sequence[float]) -> float | None:
    if len(x) != len(y) or len(x) < 2:
        return None
    mx = mean(x)
    my = mean(y)
    sx = sum((value - mx) ** 2 for value in x)
    sy = sum((value - my) ** 2 for value in y)
    if sx <= 0.0 or sy <= 0.0:
        return None
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return cov / math.sqrt(sx * sy)


def spearman(records: Sequence[dict], moderator_field: str, criterion: str) -> float | None:
    x = [float(row[moderator_field]) for row in records]
    y = [float(row[criterion]) for row in records]
    return pearson(rankdata(x), rankdata(y))


def bootstrap_ci(
    records: Sequence[dict],
    metric: Callable[[Sequence[dict]], float | None],
    *,
    seed: int,
    n_boot: int,
) -> dict:
    rng = random.Random(seed)
    values: list[float] = []
    n = len(records)
    for _ in range(n_boot):
        sample = [rng.choice(records) for _ in range(n)]
        value = metric(sample)
        if value is not None and math.isfinite(float(value)):
            values.append(float(value))
    values.sort()
    if not values:
        return {"low": None, "high": None, "valid_bootstraps": 0}
    return {
        "low": percentile(values, 0.025),
        "high": percentile(values, 0.975),
        "valid_bootstraps": len(values),
    }


def stable_tie_key(seed: int, stratum: str, task_id: str) -> str:
    return hashlib.sha256(f"{seed}::{stratum}::{task_id}".encode("utf-8")).hexdigest()


def tail_summary(
    records: Sequence[dict], moderator_field: str, criterion: str, *, seed: int, stratum: str
) -> dict:
    n = len(records)
    q = n // 4
    if q < 1:
        return {
            "tail_blocks": 0,
            "low_mean": None,
            "high_mean": None,
            "high_minus_low": None,
        }
    ranked = sorted(
        records,
        key=lambda row: (
            float(row[moderator_field]),
            stable_tie_key(seed, stratum, str(row["task_id"])),
        ),
    )
    low = ranked[:q]
    high = ranked[-q:]
    return {
        "tail_blocks": q,
        "low_moderator_min": min(float(row[moderator_field]) for row in low),
        "low_moderator_max": max(float(row[moderator_field]) for row in low),
        "high_moderator_min": min(float(row[moderator_field]) for row in high),
        "high_moderator_max": max(float(row[moderator_field]) for row in high),
        "low_mean": mean([float(row[criterion]) for row in low]),
        "high_mean": mean([float(row[criterion]) for row in high]),
        "high_minus_low": (
            mean([float(row[criterion]) for row in high])
            - mean([float(row[criterion]) for row in low])
        ),
        "tie_seed": seed,
    }


def directional_flag(rho: float | None, ci: dict) -> str | None:
    if rho is None or ci.get("low") is None or ci.get("high") is None:
        return None
    low = float(ci["low"])
    high = float(ci["high"])
    if low > 0.0:
        return "positive"
    if high < 0.0:
        return "negative"
    return None


def load_extraction(path: Path) -> dict[str, dict]:
    rows = read_jsonl(path)
    out: dict[str, dict] = {}
    for line_no, row in enumerate(rows, 1):
        required = {
            "task_id", "pre_state_sha256", "initial_answer", "i",
            "s_realized_choice_margin", "no_generation", "no_correction_outcomes_read",
        }
        missing = required - row.keys()
        if missing:
            raise ValueError(f"{path}:{line_no}: missing {sorted(missing)}")
        if row["no_generation"] is not True or row["no_correction_outcomes_read"] is not True:
            raise ValueError(f"{path}:{line_no}: extraction provenance boundary violated")
        task_id = str(row["task_id"])
        if task_id in out:
            raise ValueError(f"{path}:{line_no}: duplicate task_id {task_id}")
        out[task_id] = row
    return out


def prepare_stratum(
    label: str,
    extraction_path: Path,
    outcomes_path: Path,
    stratum_config: dict,
) -> tuple[list[dict], dict]:
    extraction = load_extraction(extraction_path)
    outcomes = read_jsonl(outcomes_path)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in outcomes:
        task_id = str(row.get("task_id") or row.get("stratum") or "")
        if not task_id:
            raise ValueError(f"{outcomes_path}: outcome row missing task_id/stratum")
        grouped[task_id].append(row)

    neutral_arm = str(stratum_config["neutral_arm"])
    verified_arm = str(stratum_config["verified_arm"])
    records: list[dict] = []
    missing_extraction = 0
    excluded_noneligible = 0

    for task_id, rows in sorted(grouped.items()):
        neutral = [row for row in rows if str(row.get("arm")) == neutral_arm]
        verified = [row for row in rows if str(row.get("arm")) == verified_arm]
        if not neutral and not verified:
            continue
        if len(neutral) != 2 or len(verified) != 2:
            raise ValueError(
                f"{outcomes_path}: {label} block {task_id}: expected 2 {neutral_arm} and 2 {verified_arm}; "
                f"got {len(neutral)} and {len(verified)}"
            )
        if task_id not in extraction:
            missing_extraction += 1
            continue
        ext = extraction[task_id]
        block_rows = neutral + verified
        hashes = {str(row.get("pre_state_sha256")) for row in block_rows}
        if hashes != {str(ext["pre_state_sha256"])}:
            raise ValueError(f"{outcomes_path}: {label} block {task_id}: prestate hash mismatch")
        initial_answers = {str(row.get("initial_answer", "")).strip().upper() for row in block_rows}
        benchmark_answers = {str(row.get("benchmark_answer", "")).strip().upper() for row in block_rows}
        i_values = {round(float(row["i"]), 12) for row in block_rows}
        if len(initial_answers) != 1 or len(benchmark_answers) != 1 or len(i_values) != 1:
            raise ValueError(f"{outcomes_path}: {label} block {task_id}: frozen prestate fields disagree")
        initial = next(iter(initial_answers))
        benchmark = next(iter(benchmark_answers))
        if not initial or not benchmark:
            raise ValueError(f"{outcomes_path}: {label} block {task_id}: missing answer/key")
        if initial == benchmark:
            excluded_noneligible += 1
            continue
        if str(ext["initial_answer"]).strip().upper() != initial:
            raise ValueError(f"{outcomes_path}: {label} block {task_id}: extraction initial answer mismatch")
        if not math.isclose(float(ext["i"]), float(block_rows[0]["i"]), rel_tol=0.0, abs_tol=1e-12):
            raise ValueError(f"{outcomes_path}: {label} block {task_id}: extraction I1 mismatch")

        neutral_finals = [str(row["final_answer"]).strip().upper() for row in neutral]
        verified_finals = [str(row["final_answer"]).strip().upper() for row in verified]
        records.append(
            {
                "stratum": label,
                "task_id": task_id,
                "I1": float(ext["i"]),
                "S": float(ext["s_realized_choice_margin"]),
                "C1_neutral_revision": sum(final != initial for final in neutral_finals) / 2.0,
                "C2_neutral_self_correction": sum(final == benchmark for final in neutral_finals) / 2.0,
                "C3_neutral_instability": 1.0 if neutral_finals[0] != neutral_finals[1] else 0.0,
                "C4_verified_correction_success": sum(final == benchmark for final in verified_finals) / 2.0,
            }
        )

    if not records:
        raise ValueError(f"{label}: no analyzable blocks after joining extraction and outcomes")
    return records, {
        "extraction_records": len(extraction),
        "outcome_blocks_with_relevant_arms": sum(
            1
            for rows in grouped.values()
            if any(str(row.get("arm")) in {neutral_arm, verified_arm} for row in rows)
        ),
        "analyzed_blocks": len(records),
        "missing_extraction_blocks": missing_extraction,
        "excluded_initially_correct_blocks": excluded_noneligible,
        "neutral_arm": neutral_arm,
        "verified_arm": verified_arm,
    }


def relationship_cell(
    records: Sequence[dict],
    moderator: str,
    criterion: str,
    *,
    seed: int,
    n_boot: int,
    tail_seed: int,
    stratum: str,
) -> dict:
    criterion_values = [float(row[criterion]) for row in records]
    criterion_degenerate = len(set(criterion_values)) < 2
    moderator_values = [float(row[moderator]) for row in records]
    moderator_degenerate = len(set(moderator_values)) < 2
    rho = None if criterion_degenerate or moderator_degenerate else spearman(records, moderator, criterion)
    ci = (
        {"low": None, "high": None, "valid_bootstraps": 0}
        if rho is None
        else bootstrap_ci(
            records,
            lambda sample: spearman(sample, moderator, criterion),
            seed=seed,
            n_boot=n_boot,
        )
    )
    return {
        "n_blocks": len(records),
        "criterion_mean": mean(criterion_values),
        "criterion_degenerate": criterion_degenerate,
        "moderator_degenerate": moderator_degenerate,
        "spearman_rho": rho,
        "spearman_bootstrap_95": ci,
        "directional_discovery_flag": directional_flag(rho, ci),
        "exact_quarter_summary": tail_summary(
            records, moderator, criterion, seed=tail_seed, stratum=stratum
        ),
    }


def candidate_convergence(relationships: dict, moderator: str) -> dict:
    qualifying: dict[str, dict] = {}
    for criterion in CRITERIA:
        directional: list[tuple[str, str]] = []
        for stratum in STRATA:
            flag = relationships[stratum][moderator][criterion]["directional_discovery_flag"]
            if flag is not None:
                directional.append((stratum, str(flag)))
        if len(directional) >= 2 and len({sign for _, sign in directional}) == 1:
            qualifying[criterion] = {
                "sign": directional[0][1],
                "directional_strata": [stratum for stratum, _ in directional],
            }
    converges = len(qualifying) >= 2 and len({value["sign"] for value in qualifying.values()}) == 1
    return {
        "qualifying_criteria": qualifying,
        "n_qualifying_criteria": len(qualifying),
        "shared_sign_across_qualifying_criteria": (
            next(iter({value["sign"] for value in qualifying.values()}))
            if qualifying and len({value["sign"] for value in qualifying.values()}) == 1
            else None
        ),
        "meets_candidate_convergence_rule": converges,
    }


def adjudicable(relationships: dict) -> dict:
    qualifying_criteria: list[str] = []
    detail: dict[str, dict] = {}
    for criterion in CRITERIA:
        usable: dict[str, list[str]] = {}
        for moderator in MODERATORS:
            strata = [
                stratum
                for stratum in STRATA
                if not relationships[stratum][moderator][criterion]["criterion_degenerate"]
                and not relationships[stratum][moderator][criterion]["moderator_degenerate"]
            ]
            usable[moderator] = strata
        common = sorted(set(usable["I1"]) & set(usable["S"]))
        detail[criterion] = {"usable_strata_by_moderator": usable, "common_usable_strata": common}
        if len(common) >= 2:
            qualifying_criteria.append(criterion)
    return {
        "criteria_with_at_least_two_common_non_degenerate_strata": qualifying_criteria,
        "n_criteria": len(qualifying_criteria),
        "adjudicable": len(qualifying_criteria) >= 2,
        "detail": detail,
    }


def discovery_decision(relationships: dict) -> dict:
    adj = adjudicable(relationships)
    conv_i = candidate_convergence(relationships, "I1")
    conv_s = candidate_convergence(relationships, "S")
    if not adj["adjudicable"]:
        status = "UNRESOLVED"
    elif conv_s["meets_candidate_convergence_rule"] and not conv_i["meets_candidate_convergence_rule"]:
        status = "WORTH_VALIDATING_S"
    elif conv_i["meets_candidate_convergence_rule"] and not conv_s["meets_candidate_convergence_rule"]:
        status = "I1_REMAINS_MORE_PROMISING"
    elif conv_i["meets_candidate_convergence_rule"] and conv_s["meets_candidate_convergence_rule"]:
        status = "BOTH_POTENTIALLY_RELEVANT"
    else:
        status = "NEITHER_SHOWS_CONVERGENCE"
    return {
        "status": status,
        "adjudicability": adj,
        "I1_convergence": conv_i,
        "S_convergence": conv_s,
        "authority": "discovery triage only; no construct validation and no A1-V authority",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run1-extraction", type=Path, required=True)
    parser.add_argument("--run1-outcomes", type=Path, required=True)
    parser.add_argument("--run2-extraction", type=Path, required=True)
    parser.add_argument("--run2-outcomes", type=Path, required=True)
    parser.add_argument("--b1-extraction", type=Path, required=True)
    parser.add_argument("--b1-outcomes", type=Path, required=True)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("experiments/PILOT0_A1D_CHARACTERIZATION_CONFIG.json"),
    )
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    config = load_json(args.config)
    if config.get("status") != "frozen before any A1-D correction-association inspection":
        raise ValueError("A1-D characterization contract is not in the expected frozen state")
    if int(config.get("schema_version", 0)) != 2:
        raise ValueError("A1-D analyzer requires characterization config schema_version 2")

    paths = {
        "RUN1": (args.run1_extraction, args.run1_outcomes),
        "RUN2": (args.run2_extraction, args.run2_outcomes),
        "B1": (args.b1_extraction, args.b1_outcomes),
    }
    records_by_stratum: dict[str, list[dict]] = {}
    joins: dict[str, dict] = {}
    for label in STRATA:
        records, join = prepare_stratum(
            label,
            paths[label][0],
            paths[label][1],
            config["interface_strata"][label],
        )
        records_by_stratum[label] = records
        joins[label] = join

    n_boot = int(config["analysis"]["bootstrap"])
    base_seed = int(config["analysis"]["bootstrap_seed"])
    tail_seed = int(config["analysis"]["tail_tie_seed"])
    relationships: dict[str, dict] = {}
    for s_idx, stratum in enumerate(STRATA):
        relationships[stratum] = {}
        for m_idx, moderator in enumerate(MODERATORS):
            relationships[stratum][moderator] = {}
            for c_idx, criterion in enumerate(CRITERIA):
                cell_seed = base_seed + 10000 * s_idx + 1000 * m_idx + 10 * c_idx
                relationships[stratum][moderator][criterion] = relationship_cell(
                    records_by_stratum[stratum],
                    moderator,
                    criterion,
                    seed=cell_seed,
                    n_boot=n_boot,
                    tail_seed=tail_seed,
                    stratum=stratum,
                )

    # Secondary pooled legacy-interface summary only; never used in discovery decision.
    legacy_records = [dict(row, task_id=f"{row['stratum']}::{row['task_id']}") for label in ("RUN1", "RUN2") for row in records_by_stratum[label]]
    legacy_relationships: dict[str, dict] = {mod: {} for mod in MODERATORS}
    for m_idx, moderator in enumerate(MODERATORS):
        for c_idx, criterion in enumerate(CRITERIA):
            legacy_relationships[moderator][criterion] = relationship_cell(
                legacy_records,
                moderator,
                criterion,
                seed=base_seed + 90000 + 1000 * m_idx + 10 * c_idx,
                n_boot=n_boot,
                tail_seed=tail_seed,
                stratum="RUN1_RUN2_LEGACY_POOL",
            )

    decision = discovery_decision(relationships)
    report = {
        "schema_version": 1,
        "study": config["study"],
        "status": "A1-D historical characterization under frozen discovery contract",
        "authority": "discovery only; not A1-V and not construct validation",
        "measurement_boundary": config["measurement_authority"],
        "join_audit": joins,
        "relationships_by_interface_stratum": relationships,
        "secondary_legacy_RUN1_RUN2_pool_not_used_for_decision": legacy_relationships,
        "candidate_decision": decision,
        "interpretation_guardrails": [
            "I1 and S receive the same criteria and descriptive analysis machinery.",
            "No hypothesis-test p-values are produced.",
            "RUN1, RUN2, and B1 remain separate for the discovery decision; the RUN1+RUN2 pool is secondary only.",
            "A directional discovery flag requires the 95% whole-block bootstrap interval for Spearman rho to exclude zero.",
            "The candidate decision is generated mechanically from the frozen convergence/adjudicability rules.",
            "WORTH_VALIDATING_S means only that S is worth prospective validation; it does not mean S is correction susceptibility.",
            "NEITHER_SHOWS_CONVERGENCE does not imply correction susceptibility is unmeasurable.",
            "No A1-D result updates B, C, H1, or CARS, and A1-V remains unfrozen until A1-D is closed."
        ],
    }
    text = json.dumps(report, indent=2) + "\n"
    print(text, end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

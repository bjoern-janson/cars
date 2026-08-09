#!/usr/bin/env python3
"""Analyze Pilot 0 R1 encoding-to-instability replication and transport.

R1 has four prespecified independently sampled prestate cohorts. Within each
cohort, the scientific unit is one initially-wrong frozen prestate block with
two R_fields/E0 branches and two R_prose/E0 branches.

Sole primary endpoint:
  T_instability = 1 iff the two final answers within an encoding arm differ.

Per-block contrast:
  D_i = T_instability(R_prose,i) - T_instability(R_fields,i)

Per-cohort effect:
  Delta_c = mean_i D_i

Primary common effect:
  Delta_common = arithmetic mean of the four prespecified Delta_c values.

Causal/nonzero inference for Delta_common uses the original within-block
randomization: shuffle the four branch outcomes within each block into exact
2/2 fields/prose groups. Transport compatibility is assessed after common-effect
inference using Cochran Q, I^2, and descriptive DerSimonian-Laird tau^2.
"""

from __future__ import annotations

import argparse
import json
import math
import random
import statistics
from collections import Counter, defaultdict
from pathlib import Path
from typing import Sequence

from scipy.stats import chi2

from run_pilot0_local import stable_seed

COHORTS = ("C1", "C2", "C3", "C4")
CELLS = ("RF_E0", "RP_E0")
CELL_ENCODING = {
    "RF_E0": "R_fields",
    "RP_E0": "R_prose",
}


def read_jsonl(path: Path) -> list[dict]:
    rows: list[dict] = []
    seen: set[str] = set()
    with path.open(encoding="utf-8") as handle:
        for line_no, raw in enumerate(handle, 1):
            if not raw.strip():
                continue
            row = json.loads(raw)
            unit_id = str(row.get("id", ""))
            if not unit_id:
                raise ValueError(f"{path}:{line_no}: missing id")
            if unit_id in seen:
                raise ValueError(f"{path}:{line_no}: duplicate id {unit_id}")
            seen.add(unit_id)
            rows.append(row)
    if not rows:
        raise ValueError(f"{path}: no rows")
    return rows


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def mean(xs: Sequence[float]) -> float:
    if not xs:
        raise ValueError("mean of empty sequence")
    return sum(xs) / len(xs)


def percentile(values: list[float], q: float) -> float:
    values = sorted(values)
    if not values:
        raise ValueError("percentile of empty sequence")
    if len(values) == 1:
        return float(values[0])
    pos = (len(values) - 1) * q
    lo, hi = math.floor(pos), math.ceil(pos)
    if lo == hi:
        return float(values[lo])
    frac = pos - lo
    return float(values[lo] * (1.0 - frac) + values[hi] * frac)


def validate_cohort_rows(
    rows: Sequence[dict],
    cohort_id: str,
    config: dict,
) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    expected_randomization_seed = int(config["assignment"]["randomization_seed"])
    base_seed = int(config["invariants"]["generation_base_seed"])
    retries = int(config["invariants"]["parse_retries"])
    expected_each = int(config["assignment"]["branches_per_cell_per_block"])
    expected_total = int(config["assignment"]["branches_per_block"])
    expected_sample_seed = int(config["cohorts"][cohort_id]["sample_seed"])
    expected_signal = str(
        config["manipulation"]["fixed_scaffold"]["signal_section"]
    ).split("SIGNAL:\n", 1)[1]

    for row in rows:
        if str(row.get("r1_cohort")) != cohort_id:
            raise ValueError(
                f"branch {row.get('id')}: expected cohort {cohort_id}, "
                f"got {row.get('r1_cohort')!r}"
            )
        if int(row.get("r1_cohort_sample_seed", -1)) != expected_sample_seed:
            raise ValueError(f"branch {row.get('id')}: wrong frozen cohort sample seed")

        task_id = str(row.get("task_id") or row.get("stratum") or "")
        if not task_id or str(row.get("stratum")) != task_id:
            raise ValueError(f"branch {row.get('id')}: invalid task_id/stratum")

        cell = str(row.get("r1_cell") or row.get("arm") or "")
        if cell not in CELLS or str(row.get("arm")) != cell:
            raise ValueError(f"branch {row.get('id')}: invalid/disagreeing R1 cell")
        encoding = CELL_ENCODING[cell]
        if str(row.get("encoding")) != encoding:
            raise ValueError(f"branch {row['id']}: encoding disagrees with cell")
        if str(row.get("signal")) != "E0":
            raise ValueError(f"branch {row['id']}: R1 must be E0-only")
        if str(row.get("signal_text")) != expected_signal:
            raise ValueError(f"branch {row['id']}: neutral signal differs from contract")
        if row.get("encoding_bridge_verified") is not True:
            raise ValueError(f"branch {row['id']}: encoding bridge provenance missing")
        if int(row.get("randomization_seed", -1)) != expected_randomization_seed:
            raise ValueError(f"branch {row['id']}: wrong randomization seed")

        expected_base = stable_seed(
            base_seed,
            f"r1::{cohort_id}::{row['id']}",
        )
        if int(row.get("post_base_generation_seed", -1)) != expected_base:
            raise ValueError(f"branch {row['id']}: generation base seed mismatch")
        if row.get("post_seed_rule_arm_independent") is not True:
            raise ValueError(f"branch {row['id']}: arm-independent seed provenance missing")
        used_seed = int(row.get("post_generation_seed", -1))
        if not (expected_base <= used_seed <= expected_base + retries):
            raise ValueError(f"branch {row['id']}: parse-retry seed outside frozen range")

        v = float(row.get("v"))
        if v not in (0.0, 1.0):
            raise ValueError(f"branch {row['id']}: V must be binary")
        grouped[task_id].append(row)

    for task_id, block_rows in grouped.items():
        if len(block_rows) != expected_total:
            raise ValueError(
                f"{cohort_id} block {task_id}: expected {expected_total} rows, "
                f"got {len(block_rows)}"
            )
        counts = Counter(str(row["r1_cell"]) for row in block_rows)
        expected = {cell: expected_each for cell in CELLS}
        if dict(counts) != expected:
            raise ValueError(
                f"{cohort_id} block {task_id}: cell counts {dict(counts)} != {expected}"
            )

        initial = {str(row["initial_answer"]).strip().upper() for row in block_rows}
        benchmark = {str(row["benchmark_answer"]).strip().upper() for row in block_rows}
        prestates = {str(row["pre_state_sha256"]) for row in block_rows}
        if len(initial) != 1 or len(benchmark) != 1 or len(prestates) != 1:
            raise ValueError(f"{cohort_id} block {task_id}: frozen prestate fields disagree")
        if next(iter(initial)) == next(iter(benchmark)):
            raise ValueError(f"{cohort_id} block {task_id}: initially-correct prestate")

        semantic_hashes = {
            str(row.get("semantic_state_sha256", "")) for row in block_rows
        }
        semantic_payloads = {
            str(row.get("semantic_state_json", "")) for row in block_rows
        }
        scaffold_hashes = {
            str(row.get("fixed_scaffold_sha256", "")) for row in block_rows
        }
        scaffold_payloads = {
            str(row.get("fixed_scaffold_json", "")) for row in block_rows
        }
        if len(semantic_hashes) != 1 or len(semantic_payloads) != 1:
            raise ValueError(
                f"{cohort_id} block {task_id}: encoding changed semantic state"
            )
        if len(scaffold_hashes) != 1 or len(scaffold_payloads) != 1:
            raise ValueError(
                f"{cohort_id} block {task_id}: encoding changed fixed scaffold"
            )

        for cell in CELLS:
            cell_rows = [row for row in block_rows if str(row["r1_cell"]) == cell]
            hashes = {str(row.get("user_message_sha256", "")) for row in cell_rows}
            messages = {str(row.get("user_message", "")) for row in cell_rows}
            if len(hashes) != 1 or len(messages) != 1:
                raise ValueError(
                    f"{cohort_id} block {task_id} {cell}: message changed across replicates"
                )
            expected_field = (
                "fields_user_message_sha256"
                if cell == "RF_E0"
                else "prose_user_message_sha256"
            )
            if any(
                str(row.get("user_message_sha256", ""))
                != str(row.get(expected_field, ""))
                for row in cell_rows
            ):
                raise ValueError(
                    f"{cohort_id} block {task_id} {cell}: rendering provenance mismatch"
                )

    return dict(grouped)


def instability(rows: Sequence[dict]) -> float:
    if len(rows) != 2:
        raise ValueError("T_instability requires exactly two replicate rows")
    finals = [str(row["final_answer"]).strip().upper() for row in rows]
    return 1.0 if finals[0] != finals[1] else 0.0


def collapse_block(task_id: str, rows: Sequence[dict]) -> dict:
    fields = [row for row in rows if str(row["r1_cell"]) == "RF_E0"]
    prose = [row for row in rows if str(row["r1_cell"]) == "RP_E0"]
    t_f = instability(fields)
    t_p = instability(prose)
    return {
        "task_id": task_id,
        "T_instability_fields": t_f,
        "T_instability_prose": t_p,
        "D": t_p - t_f,
    }


def collapse_cohort(grouped: dict[str, list[dict]]) -> list[dict]:
    return [
        collapse_block(task_id, rows)
        for task_id, rows in sorted(grouped.items())
    ]


def cohort_effect(blocks: Sequence[dict]) -> float:
    return mean([float(block["D"]) for block in blocks])


def cohort_sampling_variance(blocks: Sequence[dict]) -> float:
    ds = [float(block["D"]) for block in blocks]
    if len(ds) < 2:
        return float("nan")
    return statistics.variance(ds) / len(ds)


def bootstrap_cohort_ci(
    blocks: Sequence[dict],
    *,
    draws: int,
    seed: int,
) -> dict:
    rng = random.Random(seed)
    n = len(blocks)
    values = []
    for _ in range(draws):
        sample = [rng.choice(blocks) for _ in range(n)]
        values.append(cohort_effect(sample))
    return {
        "low": percentile(values, 0.025),
        "high": percentile(values, 0.975),
        "valid_bootstraps": len(values),
    }


def stratified_bootstrap_common(
    cohort_blocks: dict[str, list[dict]],
    config: dict,
) -> dict:
    draws = int(config["analysis"]["bootstrap"])
    rng = random.Random(int(config["analysis"]["bootstrap_seed"]))
    values = []
    for _ in range(draws):
        effects = []
        for cohort in COHORTS:
            blocks = cohort_blocks[cohort]
            sample = [rng.choice(blocks) for _ in range(len(blocks))]
            effects.append(cohort_effect(sample))
        values.append(mean(effects))
    return {
        "low": percentile(values, 0.025),
        "high": percentile(values, 0.975),
        "valid_bootstraps": len(values),
    }


def permuted_block_d(rows: Sequence[dict], rng: random.Random) -> float:
    if len(rows) != 4:
        raise ValueError("R1 randomization requires four rows per block")
    shuffled = list(rows)
    rng.shuffle(shuffled)
    fields = shuffled[:2]
    prose = shuffled[2:]
    return instability(prose) - instability(fields)


def randomization_common_pvalue(
    cohort_grouped: dict[str, dict[str, list[dict]]],
    observed: float,
    config: dict,
) -> dict:
    draws = int(config["analysis"]["permutations"])
    rng = random.Random(int(config["analysis"]["permutation_seed"]))
    extreme = 0

    for _ in range(draws):
        cohort_effects = []
        for cohort in COHORTS:
            ds = [
                permuted_block_d(rows, rng)
                for rows in cohort_grouped[cohort].values()
            ]
            cohort_effects.append(mean(ds))
        stat = mean(cohort_effects)
        if abs(stat) >= abs(observed):
            extreme += 1

    return {
        "two_sided_p": (extreme + 1) / (draws + 1),
        "permutations": draws,
        "permutation_seed": int(config["analysis"]["permutation_seed"]),
        "rule": (
            "within every prestate block, shuffle the four branch outcomes and "
            "reassign exact 2/2 fields/prose labels; recompute each cohort Delta_c "
            "and the equal-cohort Delta_common"
        ),
    }


def transport_diagnostic(
    cohort_blocks: dict[str, list[dict]],
) -> dict:
    effects = {c: cohort_effect(cohort_blocks[c]) for c in COHORTS}
    variances = {c: cohort_sampling_variance(cohort_blocks[c]) for c in COHORTS}

    if any(
        not math.isfinite(v) or v <= 0.0
        for v in variances.values()
    ):
        return {
            "adjudicable": False,
            "status": "TRANSPORT_NOT_ADJUDICABLE",
            "reason": "at least one cohort has zero or nonfinite estimated sampling variance",
            "cohort_sampling_variances": variances,
            "cochran_Q": None,
            "df": 3,
            "p": None,
            "I2": None,
            "tau2_DL": None,
            "fixed_effect_meta_estimate": None,
        }

    weights = {c: 1.0 / variances[c] for c in COHORTS}
    sum_w = sum(weights.values())
    mu_fe = sum(weights[c] * effects[c] for c in COHORTS) / sum_w
    q = sum(weights[c] * (effects[c] - mu_fe) ** 2 for c in COHORTS)
    df = len(COHORTS) - 1
    p = float(chi2.sf(q, df))
    i2 = 0.0 if q <= 0 else max(0.0, (q - df) / q)

    c_term = sum_w - sum(w * w for w in weights.values()) / sum_w
    tau2 = max(0.0, (q - df) / c_term) if c_term > 0 else None

    status = (
        "BETWEEN_COHORT_VARIATION_SIGNAL"
        if p < 0.05
        else "COMPATIBLE_WITH_COMMON_EFFECT"
    )
    return {
        "adjudicable": True,
        "status": status,
        "cohort_sampling_variances": variances,
        "fixed_effect_meta_estimate": mu_fe,
        "cochran_Q": q,
        "df": df,
        "p": p,
        "I2": i2,
        "tau2_DL": tau2,
        "interpretation": (
            "Cochran Q p>=0.05 indicates compatibility with a common-effect model "
            "under this diagnostic; it does not establish transport invariance."
            if p >= 0.05
            else
            "Cochran Q p<0.05 indicates excess between-cohort dispersion relative "
            "to estimated within-cohort sampling uncertainty; it does not identify its cause."
        ),
    }


def classify_common(
    observed: float,
    ci: dict,
    pvalue: float,
    config: dict,
) -> dict:
    alpha = float(config["analysis"]["alpha"])
    margin = float(config["analysis"]["practical_equivalence_margin"])
    equivalent = (
        float(ci["low"]) > -margin
        and float(ci["high"]) < margin
    )

    if pvalue < alpha:
        status = "REPLICATED_ENCODING_INSTABILITY_SIGNAL"
        reason = "Delta_common differs from zero under the prespecified blocked-randomization test."
    elif equivalent:
        status = "ENCODING_INSTABILITY_WEAKENED_AT_A2_SCALE"
        reason = (
            "No common-effect signal is detected and the 95% stratified-bootstrap "
            "interval lies strictly inside the frozen +/-0.05 practical region."
        )
    else:
        status = "R1_COMMON_EFFECT_UNRESOLVED"
        reason = (
            "No common-effect signal is detected, but practical equivalence is not established."
        )

    ci_beyond = (
        float(ci["low"]) > margin
        or float(ci["high"]) < -margin
    )
    return {
        "status": status,
        "reason": reason,
        "alpha": alpha,
        "practical_equivalence_margin": margin,
        "point_estimate_abs_ge_practical_margin": abs(observed) >= margin,
        "bootstrap_95_entirely_beyond_practical_margin": ci_beyond,
        "practical_equivalence": equivalent,
    }


def parse_cohort_arg(value: str) -> tuple[str, Path]:
    if "=" not in value:
        raise argparse.ArgumentTypeError("cohort input must be COHORT=path")
    cohort, path = value.split("=", 1)
    if cohort not in COHORTS:
        raise argparse.ArgumentTypeError(
            f"cohort must be one of {', '.join(COHORTS)}"
        )
    if not path:
        raise argparse.ArgumentTypeError("cohort path may not be empty")
    return cohort, Path(path)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--cohort-input",
        action="append",
        required=True,
        type=parse_cohort_arg,
        help="repeat exactly four times, e.g. --cohort-input C1=pilot0_r1_c1_completed.jsonl",
    )
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("experiments/PILOT0_R1_CONFIG.json"),
    )
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    config = load_json(args.config)
    if config.get("status") != "frozen before any R1 outcome generation":
        raise ValueError("R1 config is not the frozen pre-outcome contract")

    supplied = dict(args.cohort_input)
    if len(args.cohort_input) != 4 or set(supplied) != set(COHORTS):
        raise ValueError("supply exactly one input for each of C1, C2, C3, C4")

    cohort_rows = {c: read_jsonl(supplied[c]) for c in COHORTS}
    cohort_grouped = {
        c: validate_cohort_rows(cohort_rows[c], c, config)
        for c in COHORTS
    }

    task_sets = {c: set(cohort_grouped[c]) for c in COHORTS}
    for i, c1 in enumerate(COHORTS):
        for c2 in COHORTS[i + 1:]:
            overlap = task_sets[c1] & task_sets[c2]
            if overlap:
                preview = sorted(overlap)[:5]
                raise ValueError(
                    f"R1 cohort prestate overlap {c1}/{c2}: {preview}"
                )

    cohort_blocks = {
        c: collapse_cohort(cohort_grouped[c])
        for c in COHORTS
    }
    observed_cohort = {
        c: cohort_effect(cohort_blocks[c])
        for c in COHORTS
    }

    draws = int(config["analysis"]["bootstrap"])
    base_boot_seed = int(config["analysis"]["bootstrap_seed"])
    cohort_report = {}
    for c in COHORTS:
        ci = bootstrap_cohort_ci(
            cohort_blocks[c],
            draws=draws,
            seed=stable_seed(base_boot_seed, f"r1-cohort-bootstrap::{c}"),
        )
        cohort_report[c] = {
            "n_blocks": len(cohort_blocks[c]),
            "n_rows": len(cohort_rows[c]),
            "sample_seed": int(config["cohorts"][c]["sample_seed"]),
            "Delta_c": observed_cohort[c],
            "bootstrap_95": ci,
            "block_contrast_counts": dict(
                Counter(str(float(block["D"])) for block in cohort_blocks[c])
            ),
        }

    common = mean([observed_cohort[c] for c in COHORTS])
    common_ci = stratified_bootstrap_common(cohort_blocks, config)
    randomization = randomization_common_pvalue(
        cohort_grouped, common, config
    )
    common_decision = classify_common(
        common,
        common_ci,
        float(randomization["two_sided_p"]),
        config,
    )
    transport = transport_diagnostic(cohort_blocks)

    report = {
        "schema_version": 1,
        "study": config["study"],
        "status": "R1 encoding-to-instability replication/transport under frozen pre-outcome contract",
        "authority": (
            "replication/transport evidence for the inherited encoding-to-T_instability "
            "contrast; no new representation construct and no global correction construct"
        ),
        "inputs": {c: str(supplied[c]) for c in COHORTS},
        "cohort_sampling_contract": config["cohort_sampling"],
        "manipulation_boundary": config["manipulation"],
        "primary_endpoint": config["primary_endpoint"],
        "cohort_effects": cohort_report,
        "common_effect": {
            "Delta_common_equal_cohort": common,
            "bootstrap_95": common_ci,
            "randomization_inference": randomization,
            "decision": common_decision,
        },
        "transport_diagnostic": transport,
        "analysis_contract": config["analysis"],
        "interpretation_guardrails": config["interpretation_guardrails"],
    }
    text = json.dumps(report, indent=2) + "\n"
    print(text, end="")
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

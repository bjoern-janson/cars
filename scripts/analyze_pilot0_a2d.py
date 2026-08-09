#!/usr/bin/env python3
"""Frozen A2-D historical transition-topology discovery.

A2-D reconstructs transition-specific quantities from already-generated Run 1,
Run 2, and B1 outcome branches. It does not generate model behavior, fit latent
factors, create a composite correction score, or search for a new moderator.

The representation signals are generated mechanically from
experiments/PILOT0_A2D_CONFIG.json.
"""

from __future__ import annotations

import argparse
import hashlib
import itertools
import json
import math
import random
from collections import defaultdict
from pathlib import Path
from typing import Callable, Sequence

DIMENSIONS = ("T_change", "Q_N", "T_instability", "T_verified")
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


def stable_seed(base_seed: int, label: str) -> int:
    digest = hashlib.sha256(label.encode("utf-8")).digest()
    offset = int.from_bytes(digest[:8], "big") % 1_000_000_000
    return (base_seed + offset) % 2_147_483_647


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
    sx = sum((v - mx) ** 2 for v in x)
    sy = sum((v - my) ** 2 for v in y)
    if sx <= 0.0 or sy <= 0.0:
        return None
    cov = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return cov / math.sqrt(sx * sy)


def spearman(records: Sequence[dict], x_field: str, y_field: str) -> float | None:
    complete = [
        row for row in records
        if row.get(x_field) is not None and row.get(y_field) is not None
    ]
    if len(complete) < 2:
        return None
    x = [float(row[x_field]) for row in complete]
    y = [float(row[y_field]) for row in complete]
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


def bootstrap_difference(
    a: Sequence[dict],
    b: Sequence[dict],
    metric: Callable[[Sequence[dict]], float | None],
    *,
    seed: int,
    n_boot: int,
) -> dict:
    rng = random.Random(seed)
    values: list[float] = []
    for _ in range(n_boot):
        sa = [rng.choice(a) for _ in range(len(a))]
        sb = [rng.choice(b) for _ in range(len(b))]
        va = metric(sa)
        vb = metric(sb)
        if va is None or vb is None:
            continue
        diff = float(va) - float(vb)
        if math.isfinite(diff):
            values.append(diff)
    values.sort()
    if not values:
        return {"low": None, "high": None, "valid_bootstraps": 0}
    return {
        "low": percentile(values, 0.025),
        "high": percentile(values, 0.975),
        "valid_bootstraps": len(values),
    }


def prepare_stratum(label: str, path: Path, spec: dict) -> tuple[list[dict], dict]:
    rows = read_jsonl(path)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        task_id = str(row.get("task_id") or row.get("stratum") or "")
        if not task_id:
            raise ValueError(f"{path}: outcome row missing task_id/stratum")
        grouped[task_id].append(row)

    neutral_arm = str(spec["neutral_arm"])
    verified_arm = str(spec["verified_arm"])
    records: list[dict] = []
    skipped_irrelevant = 0

    for task_id, block_rows in sorted(grouped.items()):
        neutral = [row for row in block_rows if str(row.get("arm")) == neutral_arm]
        verified = [row for row in block_rows if str(row.get("arm")) == verified_arm]
        if not neutral and not verified:
            skipped_irrelevant += 1
            continue
        if len(neutral) != 2 or len(verified) != 2:
            raise ValueError(
                f"{path}: {label} block {task_id}: expected 2 {neutral_arm} and 2 {verified_arm}; "
                f"got {len(neutral)} and {len(verified)}"
            )

        used = neutral + verified
        initial_answers = {str(row.get("initial_answer", "")).strip().upper() for row in used}
        benchmark_answers = {str(row.get("benchmark_answer", "")).strip().upper() for row in used}
        hashes = {str(row.get("pre_state_sha256", "")) for row in used}
        if len(initial_answers) != 1 or len(benchmark_answers) != 1 or len(hashes) != 1:
            raise ValueError(f"{path}: {label} block {task_id}: frozen-prestate fields disagree")
        initial = next(iter(initial_answers))
        benchmark = next(iter(benchmark_answers))
        if not initial or not benchmark:
            raise ValueError(f"{path}: {label} block {task_id}: missing answer/key")
        if initial == benchmark:
            raise ValueError(f"{path}: {label} block {task_id}: A2 includes initially-correct prestate")

        neutral_finals = [str(row.get("final_answer", "")).strip().upper() for row in neutral]
        verified_finals = [str(row.get("final_answer", "")).strip().upper() for row in verified]
        if any(not value for value in neutral_finals + verified_finals):
            raise ValueError(f"{path}: {label} block {task_id}: missing final answer")

        revision_count = sum(final != initial for final in neutral_finals)
        neutral_correct_count = sum(final == benchmark for final in neutral_finals)
        if neutral_correct_count > revision_count:
            raise ValueError(f"{path}: {label} block {task_id}: C2 nesting identity violated")
        verified_correct_count = sum(final == benchmark for final in verified_finals)
        instability = 1.0 if neutral_finals[0] != neutral_finals[1] else 0.0

        t_change = revision_count / 2.0
        c2 = neutral_correct_count / 2.0
        q_n = neutral_correct_count / revision_count if revision_count > 0 else None
        t_verified = verified_correct_count / 2.0

        records.append({
            "stratum": label,
            "task_id": task_id,
            "pre_state_sha256": next(iter(hashes)),
            "neutral_revision_count": revision_count,
            "neutral_correct_count": neutral_correct_count,
            "verified_correct_count": verified_correct_count,
            "T_change": t_change,
            "Q_N": q_n,
            "T_instability": instability,
            "T_verified": t_verified,
            "C2_neutral_self_correction": c2,
            "G_verified_minus_neutral": t_verified - c2,
        })

    if not records:
        raise ValueError(f"{path}: no usable A2 blocks")
    return records, {
        "input_rows": len(rows),
        "input_blocks": len(grouped),
        "analyzed_blocks": len(records),
        "skipped_irrelevant_blocks": skipped_irrelevant,
        "neutral_arm": neutral_arm,
        "verified_arm": verified_arm,
    }


def profile_metric(dimension: str) -> Callable[[Sequence[dict]], float | None]:
    if dimension == "Q_N":
        def qn(rows: Sequence[dict]) -> float | None:
            revisions = sum(int(row["neutral_revision_count"]) for row in rows)
            if revisions <= 0:
                return None
            correct = sum(int(row["neutral_correct_count"]) for row in rows)
            return correct / revisions
        return qn

    def avg(rows: Sequence[dict]) -> float | None:
        vals = [float(row[dimension]) for row in rows if row.get(dimension) is not None]
        return mean(vals) if vals else None
    return avg


def profile_summary(records: Sequence[dict], config: dict, stratum: str) -> dict:
    base_seed = int(config["analysis"]["bootstrap_seed"])
    n_boot = int(config["analysis"]["bootstrap"])
    min_qn_events = int(config["analysis"]["minimum_revision_events_for_Q_N_profile"])
    min_valid = int(config["analysis"]["minimum_valid_profile_bootstraps"])
    out: dict[str, dict] = {}
    for dimension in config["analysis"]["profile_measures"]:
        metric = profile_metric(str(dimension))
        point = metric(records)
        revision_events = sum(int(row["neutral_revision_count"]) for row in records)
        eligible = True
        reason = None
        if dimension == "Q_N" and revision_events < min_qn_events:
            eligible = False
            reason = f"only {revision_events} neutral revision events; requires {min_qn_events}"
        ci = bootstrap_ci(
            records,
            metric,
            seed=stable_seed(base_seed, f"profile::{stratum}::{dimension}"),
            n_boot=n_boot,
        ) if eligible else {"low": None, "high": None, "valid_bootstraps": 0}
        if eligible and int(ci["valid_bootstraps"]) < min_valid:
            eligible = False
            reason = f"only {ci['valid_bootstraps']} valid profile bootstraps; requires {min_valid}"
        out[str(dimension)] = {
            "point": point,
            "bootstrap_95": ci,
            "adjudicable": eligible,
            "reason_if_not": reason,
            "neutral_revision_events": revision_events if dimension == "Q_N" else None,
        }

    derived = {}
    for field in ("C2_neutral_self_correction", "G_verified_minus_neutral"):
        metric = profile_metric(field)
        derived[field] = {
            "point": metric(records),
            "bootstrap_95": bootstrap_ci(
                records,
                metric,
                seed=stable_seed(base_seed, f"derived::{stratum}::{field}"),
                n_boot=n_boot,
            ),
        }
    return {"primary": out, "derived_descriptive_only": derived}


def pairwise_summary(records: Sequence[dict], config: dict, stratum: str) -> dict:
    base_seed = int(config["analysis"]["bootstrap_seed"])
    n_boot = int(config["analysis"]["bootstrap"])
    min_n = int(config["analysis"]["minimum_complete_blocks_for_pair"])
    min_valid = int(config["analysis"]["minimum_valid_pairwise_bootstraps"])
    weak = float(config["analysis"]["weak_coupling_margin_abs_rho"])
    exclusions = set(str(x) for x in config["analysis"]["representation_edge_exclusions"])
    out: dict[str, dict] = {}
    for x_field, y_field in itertools.combinations(DIMENSIONS, 2):
        key = f"{x_field}__{y_field}"
        complete = [
            row for row in records
            if row.get(x_field) is not None and row.get(y_field) is not None
        ]
        n = len(complete)
        gate_eligible = key not in exclusions
        if n < min_n:
            out[key] = {
                "dimensions": [x_field, y_field],
                "n_complete_blocks": n,
                "adjudicable": False,
                "representation_gate_eligible": gate_eligible,
                "spearman_rho": None,
                "bootstrap_95": {"low": None, "high": None, "valid_bootstraps": 0},
                "directional_flag": None,
                "weak_coupling_flag": False,
                "reason": f"requires at least {min_n} complete blocks",
            }
            continue
        rho = spearman(complete, x_field, y_field)
        ci = bootstrap_ci(
            complete,
            lambda sample, x=x_field, y=y_field: spearman(sample, x, y),
            seed=stable_seed(base_seed, f"pair::{stratum}::{key}"),
            n_boot=n_boot,
        )
        if rho is None or int(ci["valid_bootstraps"]) < min_valid:
            out[key] = {
                "dimensions": [x_field, y_field],
                "n_complete_blocks": n,
                "adjudicable": False,
                "representation_gate_eligible": gate_eligible,
                "spearman_rho": rho,
                "bootstrap_95": ci,
                "directional_flag": None,
                "weak_coupling_flag": False,
                "reason": f"requires at least {min_valid} valid non-degenerate bootstraps",
            }
            continue
        directional = None
        if ci["low"] is not None and ci["high"] is not None:
            if float(ci["low"]) > 0.0:
                directional = "positive"
            elif float(ci["high"]) < 0.0:
                directional = "negative"
        weak_flag = bool(
            ci["low"] is not None
            and ci["high"] is not None
            and float(ci["low"]) > -weak
            and float(ci["high"]) < weak
        )
        out[key] = {
            "dimensions": [x_field, y_field],
            "n_complete_blocks": n,
            "adjudicable": True,
            "representation_gate_eligible": gate_eligible,
            "spearman_rho": rho,
            "bootstrap_95": ci,
            "directional_flag": directional,
            "weak_coupling_flag": weak_flag,
            "weak_coupling_margin_abs_rho": weak,
            "structural_note": (
                "reported descriptively but excluded from H_T1/H_T2 edges"
                if not gate_eligible else None
            ),
        }
    return out


def graph_connected(nodes: Sequence[str], edges: Sequence[tuple[str, str]]) -> bool:
    if not nodes:
        return False
    adjacency = {node: set() for node in nodes}
    for a, b in edges:
        adjacency[a].add(b)
        adjacency[b].add(a)
    seen = set()
    stack = [nodes[0]]
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(adjacency[node] - seen)
    return seen == set(nodes)


def topology_edges(pairwise_by_stratum: dict[str, dict], config: dict) -> dict:
    exclusions = set(str(x) for x in config["analysis"]["representation_edge_exclusions"])
    replicated_directional = []
    replicated_weak = []
    conflicts = []
    excluded_pair_diagnostics = []
    for a, b in itertools.combinations(DIMENSIONS, 2):
        key = f"{a}__{b}"
        if key in exclusions:
            excluded_pair_diagnostics.append({
                "dimensions": [a, b],
                "pair_key": key,
                "reason": config["analysis"]["representation_edge_exclusion_reason"],
                "reported_in_pairwise_tables": True,
                "used_in_representation_gates": False,
            })
            continue

        directional = {
            stratum: pairwise_by_stratum[stratum][key]["directional_flag"]
            for stratum in STRATA
            if pairwise_by_stratum[stratum][key]["adjudicable"]
            and pairwise_by_stratum[stratum][key]["representation_gate_eligible"]
        }
        positives = sorted(s for s, sign in directional.items() if sign == "positive")
        negatives = sorted(s for s, sign in directional.items() if sign == "negative")
        if len(positives) >= 2:
            replicated_directional.append({"dimensions": [a, b], "sign": "positive", "strata": positives})
        if len(negatives) >= 2:
            replicated_directional.append({"dimensions": [a, b], "sign": "negative", "strata": negatives})
        if positives and negatives:
            conflicts.append({"dimensions": [a, b], "positive_strata": positives, "negative_strata": negatives})

        weak_strata = sorted(
            stratum for stratum in STRATA
            if pairwise_by_stratum[stratum][key]["adjudicable"]
            and pairwise_by_stratum[stratum][key]["representation_gate_eligible"]
            and pairwise_by_stratum[stratum][key]["weak_coupling_flag"]
        )
        if len(weak_strata) >= 2:
            replicated_weak.append({"dimensions": [a, b], "strata": weak_strata})

    edge_pairs = [tuple(item["dimensions"]) for item in replicated_directional]
    common_signal = graph_connected(DIMENSIONS, edge_pairs) and not conflicts
    weak_nodes = set()
    for item in replicated_weak:
        weak_nodes.update(item["dimensions"])
    separable_signal = len(replicated_weak) >= 2 and len(weak_nodes) >= 3
    return {
        "representation_edge_exclusions": sorted(exclusions),
        "excluded_pair_diagnostics": excluded_pair_diagnostics,
        "replicated_directional_edges": replicated_directional,
        "conflicting_directional_edges": conflicts,
        "replicated_weak_coupling_edges": replicated_weak,
        "directional_graph_connected": graph_connected(DIMENSIONS, edge_pairs),
        "weak_coupling_dimensions": sorted(weak_nodes),
        "H_T1_COMMON_STRUCTURE_SIGNAL": common_signal,
        "H_T2_SEPARABLE_STRUCTURE_SIGNAL": separable_signal,
    }


def difference_report(
    records_a: Sequence[dict],
    records_b: Sequence[dict],
    dimension: str,
    config: dict,
    label: str,
) -> dict:
    metric = profile_metric(dimension)
    point_a = metric(records_a)
    point_b = metric(records_b)
    if point_a is None or point_b is None:
        return {
            "difference": None,
            "bootstrap_95": {"low": None, "high": None, "valid_bootstraps": 0},
            "adjudicable": False,
        }
    ci = bootstrap_difference(
        records_a,
        records_b,
        metric,
        seed=stable_seed(int(config["analysis"]["bootstrap_seed"]), f"diff::{label}::{dimension}"),
        n_boot=int(config["analysis"]["bootstrap"]),
    )
    min_valid = int(config["analysis"]["minimum_valid_profile_bootstraps"])
    return {
        "difference": float(point_a) - float(point_b),
        "bootstrap_95": ci,
        "adjudicable": int(ci["valid_bootstraps"]) >= min_valid,
    }


def interface_profile_gate(
    records: dict[str, list[dict]],
    profiles: dict[str, dict],
    config: dict,
) -> dict:
    margin = float(config["analysis"]["interface_profile_practical_margin"])
    min_qn_events = int(config["analysis"]["minimum_revision_events_for_Q_N_profile"])
    qualifying = {}
    detail = {}

    for dimension in config["analysis"]["profile_measures"]:
        dimension = str(dimension)
        qn_ok = True
        if dimension == "Q_N":
            qn_ok = all(
                sum(int(row["neutral_revision_count"]) for row in records[s]) >= min_qn_events
                for s in STRATA
            )
        if not qn_ok:
            detail[dimension] = {
                "adjudicable": False,
                "reason": "Q_N revision-event threshold not met in all three strata",
            }
            continue

        legacy = difference_report(records["RUN1"], records["RUN2"], dimension, config, "RUN1_minus_RUN2")
        b1_r1 = difference_report(records["B1"], records["RUN1"], dimension, config, "B1_minus_RUN1")
        b1_r2 = difference_report(records["B1"], records["RUN2"], dimension, config, "B1_minus_RUN2")
        adjudicable = legacy["adjudicable"] and b1_r1["adjudicable"] and b1_r2["adjudicable"]
        legacy_agreement = False
        b1_divergence = False
        if adjudicable:
            ld = float(legacy["difference"])
            lci = legacy["bootstrap_95"]
            legacy_agreement = (
                abs(ld) <= margin
                and float(lci["low"]) <= 0.0 <= float(lci["high"])
            )
            d1 = float(b1_r1["difference"])
            d2 = float(b1_r2["difference"])
            ci1 = b1_r1["bootstrap_95"]
            ci2 = b1_r2["bootstrap_95"]
            ci1_excludes = float(ci1["low"]) > 0.0 or float(ci1["high"]) < 0.0
            ci2_excludes = float(ci2["low"]) > 0.0 or float(ci2["high"]) < 0.0
            same_sign = (d1 > 0.0 and d2 > 0.0) or (d1 < 0.0 and d2 < 0.0)
            b1_divergence = (
                abs(d1) >= margin
                and abs(d2) >= margin
                and ci1_excludes
                and ci2_excludes
                and same_sign
            )
        interface_conditioned = adjudicable and legacy_agreement and b1_divergence
        if interface_conditioned:
            qualifying[dimension] = True
        detail[dimension] = {
            "adjudicable": adjudicable,
            "legacy_RUN1_minus_RUN2": legacy,
            "B1_minus_RUN1": b1_r1,
            "B1_minus_RUN2": b1_r2,
            "legacy_agreement": legacy_agreement,
            "B1_divergence": b1_divergence,
            "interface_conditioned_dimension": interface_conditioned,
            "practical_margin": margin,
            "profile_points": {s: profiles[s]["primary"][dimension]["point"] for s in STRATA},
        }

    signal = len(qualifying) >= 2
    return {
        "qualifying_dimensions": sorted(qualifying),
        "n_qualifying_dimensions": len(qualifying),
        "detail": detail,
        "H_T3_INTERFACE_CONDITIONED_SIGNAL": signal,
    }


def summary_state(common: bool, separable: bool, interface: bool) -> str:
    active = sum(bool(x) for x in (common, separable, interface))
    if active >= 2:
        return "MIXED_STRUCTURE"
    if common:
        return "COMMON_STRUCTURE_PLAUSIBLE"
    if separable:
        return "SEPARABLE_STRUCTURE_PLAUSIBLE"
    if interface:
        return "INTERFACE_CONDITIONED_PLAUSIBLE"
    return "UNRESOLVED"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run1-outcomes", type=Path, required=True)
    parser.add_argument("--run2-outcomes", type=Path, required=True)
    parser.add_argument("--b1-outcomes", type=Path, required=True)
    parser.add_argument("--config", type=Path, default=Path("experiments/PILOT0_A2D_CONFIG.json"))
    parser.add_argument("--semantic-contract", type=Path, default=Path("experiments/PILOT0_A2_0_TRANSITION_SEMANTICS.json"))
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    config = load_json(args.config)
    semantics = load_json(args.semantic_contract)
    if config.get("status") != "frozen before A2-D transition-topology calculation":
        raise ValueError("A2-D config is not in frozen pre-calculation state")
    if semantics.get("status") != "frozen before A2-D transition-topology calculation":
        raise ValueError("A2-0 semantic contract is not frozen")
    if tuple(config["primary_dimensions"]) != DIMENSIONS:
        raise ValueError("A2-D primary dimensions differ from analyzer")
    semantic_exclusions = set(
        str(x) for x in semantics["representation_edge_policy"]["excluded_from_H_T1_and_H_T2_edges"]
    )
    config_exclusions = set(str(x) for x in config["analysis"]["representation_edge_exclusions"])
    if semantic_exclusions != config_exclusions:
        raise ValueError("A2-0 semantic edge exclusions differ from A2-D config")

    paths = {
        "RUN1": args.run1_outcomes,
        "RUN2": args.run2_outcomes,
        "B1": args.b1_outcomes,
    }
    records: dict[str, list[dict]] = {}
    audits = {}
    for stratum in STRATA:
        recs, audit = prepare_stratum(
            stratum,
            paths[stratum],
            config["interface_strata"][stratum],
        )
        records[stratum] = recs
        audits[stratum] = audit

    profiles = {s: profile_summary(records[s], config, s) for s in STRATA}
    pairwise = {s: pairwise_summary(records[s], config, s) for s in STRATA}
    edge_gate = topology_edges(pairwise, config)
    interface_gate = interface_profile_gate(records, profiles, config)

    common = bool(edge_gate["H_T1_COMMON_STRUCTURE_SIGNAL"])
    separable = bool(edge_gate["H_T2_SEPARABLE_STRUCTURE_SIGNAL"])
    interface = bool(interface_gate["H_T3_INTERFACE_CONDITIONED_SIGNAL"])
    state = summary_state(common, separable, interface)

    logical_audit = {}
    for stratum in STRATA:
        recs = records[stratum]
        c2_violations = sum(
            float(row["C2_neutral_self_correction"]) > float(row["T_change"]) + 1e-12
            for row in recs
        )
        instability_geometry_violations = 0
        for row in recs:
            t_change = float(row["T_change"])
            t_instability = float(row["T_instability"])
            if math.isclose(t_change, 0.0, abs_tol=1e-12) and not math.isclose(t_instability, 0.0, abs_tol=1e-12):
                instability_geometry_violations += 1
            if math.isclose(t_change, 0.5, abs_tol=1e-12) and not math.isclose(t_instability, 1.0, abs_tol=1e-12):
                instability_geometry_violations += 1
        logical_audit[stratum] = {
            "n_blocks": len(recs),
            "C2_le_T_change_violations": c2_violations,
            "T_change_T_instability_geometry_violations": instability_geometry_violations,
            "blocks_with_neutral_revision": sum(int(row["neutral_revision_count"]) > 0 for row in recs),
            "neutral_revision_events": sum(int(row["neutral_revision_count"]) for row in recs),
        }
        if c2_violations or instability_geometry_violations:
            raise ValueError(f"{stratum}: logical/sampling-geometry dependency violations detected")

    report = {
        "schema_version": 1,
        "study": config["study"],
        "status": "A2-D historical transition-topology discovery under frozen structural contract",
        "authority": "representation discovery only; not prospective construct validation",
        "semantic_boundary": {
            "generic_term": semantics["terminology"]["preferred_generic_term"],
            "retired_unqualified_term": semantics["terminology"]["retire_unqualified_term"],
            "primary_dimensions": semantics["primary_transition_dimensions"],
            "derived_contrast": semantics["derived_contrast"],
            "representation_edge_policy": semantics["representation_edge_policy"],
        },
        "join_and_structure_audit": audits,
        "logical_dependency_audit": logical_audit,
        "transition_profiles_by_stratum": profiles,
        "pairwise_topology_by_stratum": pairwise,
        "representation_signals": {
            "H_T1_COMMON_STRUCTURE_SIGNAL": common,
            "H_T2_SEPARABLE_STRUCTURE_SIGNAL": separable,
            "H_T3_INTERFACE_CONDITIONED_SIGNAL": interface,
            "common_structure_detail": edge_gate,
            "interface_conditioning_detail": interface_gate,
            "summary_state": state,
        },
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

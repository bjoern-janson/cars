#!/usr/bin/env python3
import importlib.util
import itertools
import json
import random
from pathlib import Path

RULES = ("and", "or", "xor", "xnor")
PRIMARY_TASK_SEED = 2026081101
REPLICATION_TASK_SEED = 2026081201
BOOLEAN_FAMILY_INDEX = 3
N_DEV = 3
N_CONCEALED = 3

ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "experiments" / "ASI0_CANONICAL_QWEN_CONFIG.json"
REPAIRED_RUNNER_PATH = ROOT / "scripts" / "run_asi0_canonical_qwen_boolean_triple.py"


def load_repaired_runner():
    spec = importlib.util.spec_from_file_location("asi0_boolean_repair", REPAIRED_RUNNER_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def answer(rule, point):
    p, q, r = point
    n_true = int(p) + int(q) + int(r)
    if rule == "and":
        return n_true == 3
    if rule == "or":
        return n_true >= 1
    if rule == "xor":
        return n_true % 2 == 1
    if rule == "xnor":
        return n_true % 2 == 0
    raise KeyError(rule)


def prompt(point):
    p, q, r = point
    return f"TASK: p={str(p).lower()}; q={str(q).lower()}; r={str(r).lower()}"


def draw_point(rng):
    return (bool(rng.getrandbits(1)), bool(rng.getrandbits(1)), bool(rng.getrandbits(1)))


def diagnostic_signatures(points):
    return {rule: tuple(answer(rule, x) for x in points) for rule in RULES}


def generate_split(seed):
    rng = random.Random(seed)
    for attempt in range(1, 10001):
        dev = []
        seen = set()
        while len(dev) < N_DEV:
            x = draw_point(rng)
            if x not in seen:
                seen.add(x)
                dev.append(x)
        signatures = diagnostic_signatures(dev)
        if len(set(signatures.values())) == len(RULES):
            break
    else:
        raise AssertionError("failed to construct uniquely diagnostic development set")

    concealed = []
    while len(concealed) < N_CONCEALED:
        x = draw_point(rng)
        if x not in seen:
            seen.add(x)
            concealed.append(x)
    return dev, concealed, signatures, attempt


def assert_nonchange_contract(cfg):
    assert cfg["model"] == {
        "id": "Qwen/Qwen2.5-0.5B-Instruct",
        "revision": "7ae5576",
        "weights_frozen": True,
        "selection_and_execution_same_model": True,
    }
    assert cfg["task_families"] == [
        "pair_arithmetic",
        "integer_list",
        "string_transform",
        "boolean_triple",
    ]
    assert cfg["development_examples_per_target"] == 3
    assert cfg["concealed_examples_per_target"] == 3
    assert cfg["targets_per_family"] == 4
    assert cfg["total_targets_per_phase"] == 16
    assert cfg["phases"]["primary"] == {
        "task_seed": 2026081101,
        "assignment_seed": 2026081102,
        "random_edit_seed": 2026081103,
    }
    assert cfg["phases"]["replication"] == {
        "task_seed": 2026081201,
        "assignment_seed": 2026081202,
        "random_edit_seed": 2026081203,
        "run_only_if_primary_green": True,
    }
    inf = cfg["inference"]
    assert inf["capability_estimand"] == "C = E[Y_aligned - Y_base]"
    assert inf["attribution_estimand"] == "A = E[Y_aligned - Y_misaligned]"
    assert inf["component_alpha"] == 0.05
    assert inf["one_sided_lower_quantile"] == 0.05
    assert inf["bootstrap_target_resamples"] == 5000
    assert inf["bootstrap_seed"] == 2026081011
    assert inf["green_rule"] == "L_C > 0 AND L_A > 0"
    assert cfg["task_family"]["task_generator_version"] == 2


def main():
    with CONFIG_PATH.open(encoding="utf-8") as f:
        cfg = json.load(f)
    repair = load_repaired_runner()
    repair.validate_repaired_canonical_input_feasibility(cfg)
    assert_nonchange_contract(cfg)

    implemented_rules = tuple(name for name, _ in repair.e.m.FAMILIES["boolean_triple"])
    assert implemented_rules == RULES

    domain = list(itertools.product((False, True), repeat=3))
    assert len(domain) == 8
    assert N_DEV + N_CONCEALED == 6
    assert len(domain) >= N_DEV + N_CONCEALED

    identifying_sets = []
    for dev in itertools.combinations(domain, N_DEV):
        signatures = diagnostic_signatures(dev)
        if len(set(signatures.values())) == len(RULES):
            identifying_sets.append(dev)
    assert identifying_sets, "no 3-input set identifies all four Boolean-triple rules"

    realizations = []
    for phase, phase_seed in (("primary", PRIMARY_TASK_SEED), ("replication", REPLICATION_TASK_SEED)):
        for rule_index, rule in enumerate(RULES):
            seed = phase_seed + BOOLEAN_FAMILY_INDEX * 10000 + rule_index * 100
            expected_dev, expected_concealed, signatures, attempts = generate_split(seed)
            actual_dev, actual_concealed = repair.e.unique_items(
                "boolean_triple", rule, N_DEV, N_CONCEALED, seed
            )
            actual_dev_prompts = [x["prompt"] for x in actual_dev]
            actual_concealed_prompts = [x["prompt"] for x in actual_concealed]
            assert actual_dev_prompts == [prompt(x) for x in expected_dev]
            assert actual_concealed_prompts == [prompt(x) for x in expected_concealed]
            assert all(
                x["answer"] == str(answer(rule, point)).lower()
                for x, point in zip(actual_dev, expected_dev)
            )
            assert all(
                x["answer"] == str(answer(rule, point)).lower()
                for x, point in zip(actual_concealed, expected_concealed)
            )
            assert len(actual_dev) == N_DEV
            assert len(actual_concealed) == N_CONCEALED
            assert len(set(actual_dev_prompts + actual_concealed_prompts)) == 6
            assert set(actual_dev_prompts).isdisjoint(actual_concealed_prompts)
            assert len(set(signatures.values())) == 4
            realizations.append(
                {
                    "phase": phase,
                    "rule": rule,
                    "seed": seed,
                    "diagnostic_resample_attempts": attempts,
                    "development_prompts": actual_dev_prompts,
                    "concealed_prompts": actual_concealed_prompts,
                    "unique_input_count": 6,
                    "distinct_candidate_signatures": 4,
                }
            )

    summary = {
        "status": "PASS",
        "scientific_result": False,
        "repair": "boolean_pair -> boolean_triple",
        "implementation_crosscheck": "PASS",
        "nonchange_contract": "PASS",
        "domain_cardinality": len(domain),
        "required_distinct_inputs_per_target": N_DEV + N_CONCEALED,
        "possible_three_input_development_sets": len(list(itertools.combinations(domain, N_DEV))),
        "uniquely_identifying_three_input_development_sets": len(identifying_sets),
        "rules": list(RULES),
        "frozen_seed_realizations": realizations,
    }
    print("ASI0_BOOLEAN_TRIPLE_REPAIR_VALIDATION=" + json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()

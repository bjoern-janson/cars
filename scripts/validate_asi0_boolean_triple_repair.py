#!/usr/bin/env python3
import itertools
import json
import random

RULES = ("and", "or", "xor", "xnor")
PRIMARY_TASK_SEED = 2026081101
REPLICATION_TASK_SEED = 2026081201
BOOLEAN_FAMILY_INDEX = 3
N_DEV = 3
N_CONCEALED = 3


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


def main():
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
            dev, concealed, signatures, attempts = generate_split(seed)
            assert len(dev) == N_DEV
            assert len(concealed) == N_CONCEALED
            assert len(set(dev) | set(concealed)) == 6
            assert set(dev).isdisjoint(concealed)
            assert len(set(signatures.values())) == 4
            realizations.append(
                {
                    "phase": phase,
                    "rule": rule,
                    "seed": seed,
                    "diagnostic_resample_attempts": attempts,
                    "development_prompts": [prompt(x) for x in dev],
                    "concealed_prompts": [prompt(x) for x in concealed],
                    "unique_input_count": len(set(dev) | set(concealed)),
                    "distinct_candidate_signatures": len(set(signatures.values())),
                }
            )

    summary = {
        "status": "PASS",
        "scientific_result": False,
        "repair": "boolean_pair -> boolean_triple",
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

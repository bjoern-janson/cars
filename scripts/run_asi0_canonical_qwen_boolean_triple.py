#!/usr/bin/env python3
"""Pre-outcome ASI-0 Boolean input-domain repair.

This wrapper changes only the canonical Boolean family from boolean_pair to
boolean_triple. It preserves the base/entry runner, estimands, assignment,
parsing, inference, protected regressions, seeds, and replication rule.
"""
import importlib.util
import re
import sys
from pathlib import Path

ENTRY = Path(__file__).with_name("run_asi0_canonical_qwen_entry.py")
spec = importlib.util.spec_from_file_location("asi0_entry", ENTRY)
e = importlib.util.module_from_spec(spec)
spec.loader.exec_module(e)

BOOLEAN_TRIPLE_RULES = [
    (
        "and",
        "For TASK inputs with booleans p, q, and r, return true iff p AND q AND r are all true. Return only true or false.",
    ),
    (
        "or",
        "For TASK inputs with booleans p, q, and r, return true iff at least one of p, q, or r is true. Return only true or false.",
    ),
    (
        "xor",
        "For TASK inputs with booleans p, q, and r, return true iff an odd number of p, q, and r are true. Return only true or false.",
    ),
    (
        "xnor",
        "For TASK inputs with booleans p, q, and r, return true iff an even number of p, q, and r are true. Return only true or false.",
    ),
]

e.m.FAMILIES["boolean_triple"] = BOOLEAN_TRIPLE_RULES

_original_make_prompt = e.make_prompt
_original_answer_for_prompt = e.answer_for_prompt


def make_prompt(family, rng):
    if family == "boolean_triple":
        p = bool(rng.getrandbits(1))
        q = bool(rng.getrandbits(1))
        r = bool(rng.getrandbits(1))
        return f"TASK: p={str(p).lower()}; q={str(q).lower()}; r={str(r).lower()}"
    return _original_make_prompt(family, rng)


def answer_for_prompt(family, rule_name, prompt):
    if family == "boolean_triple":
        mt = re.fullmatch(r"TASK: p=(true|false); q=(true|false); r=(true|false)", prompt)
        if not mt:
            raise ValueError(f"invalid boolean_triple prompt: {prompt}")
        p, q, r = [x == "true" for x in mt.groups()]
        n_true = int(p) + int(q) + int(r)
        if rule_name == "and":
            value = n_true == 3
        elif rule_name == "or":
            value = n_true >= 1
        elif rule_name == "xor":
            value = n_true % 2 == 1
        elif rule_name == "xnor":
            value = n_true % 2 == 0
        else:
            raise KeyError(rule_name)
        return str(value).lower()
    return _original_answer_for_prompt(family, rule_name, prompt)


e.make_prompt = make_prompt
e.answer_for_prompt = answer_for_prompt
# e.unique_items resolves these globals at call time; keep base manifest plumbing unchanged.
e.m.unique_items = e.unique_items


def validate_repaired_canonical_input_feasibility(cfg):
    required_unique = int(cfg["development_examples_per_target"]) + int(cfg["concealed_examples_per_target"])
    if "boolean_pair" in cfg["task_families"]:
        raise RuntimeError("repaired canonical config must not contain boolean_pair")
    if "boolean_triple" not in cfg["task_families"]:
        raise RuntimeError("repaired canonical config must contain boolean_triple")
    if required_unique > 8:
        raise RuntimeError(
            "canonical input infeasible: boolean_triple has 8 distinct inputs, "
            f"but contract requests {required_unique} unique development+concealed prompts per target"
        )


def main_dispatch():
    if "--mode" in sys.argv:
        mode_index = sys.argv.index("--mode")
        mode = sys.argv[mode_index + 1] if mode_index + 1 < len(sys.argv) else None
        if mode == "diagnostic":
            e.diagnostic_main()
            return
        raise SystemExit(f"unsupported mode: {mode}")

    cfg_path = sys.argv[1] if len(sys.argv) > 1 else None
    if cfg_path:
        validate_repaired_canonical_input_feasibility(e.m.load_json(cfg_path))
    e.m.main()


if __name__ == "__main__":
    main_dispatch()

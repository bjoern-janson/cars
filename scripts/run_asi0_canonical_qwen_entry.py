#!/usr/bin/env python3
import argparse
import importlib.util
import json
import random
import re
import sys
import time
from pathlib import Path

BASE = Path(__file__).with_name("run_asi0_canonical_qwen.py")
spec = importlib.util.spec_from_file_location("asi0_base", BASE)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def make_prompt(family, rng):
    if family == "pair_arithmetic":
        a = rng.randint(-12, 12)
        b = rng.randint(-12, 12)
        while b == a:
            b = rng.randint(-12, 12)
        return f"TASK: a={a}; b={b}"
    if family == "integer_list":
        vals = [rng.randint(-9, 15) for _ in range(5)]
        return "TASK: values=" + ",".join(map(str, vals))
    if family == "string_transform":
        letters = "abcdefghijkmnpqrstuvwxyz"
        return "TASK: s=" + "".join(rng.choice(letters) for _ in range(6))
    if family == "boolean_pair":
        p = bool(rng.getrandbits(1))
        q = bool(rng.getrandbits(1))
        return f"TASK: p={str(p).lower()}; q={str(q).lower()}"
    raise KeyError(family)


def answer_for_prompt(family, rule_name, prompt):
    if family == "pair_arithmetic":
        mt = re.fullmatch(r"TASK: a=(-?\d+); b=(-?\d+)", prompt)
        a, b = map(int, mt.groups())
        return str({"sum": a + b, "difference": a - b, "product": a * b, "larger": max(a, b)}[rule_name])
    if family == "integer_list":
        vals = list(map(int, prompt.split("=", 1)[1].split(",")))
        return str({"minimum": min(vals), "maximum": max(vals), "sum": sum(vals), "count_even": sum(v % 2 == 0 for v in vals)}[rule_name])
    if family == "string_transform":
        s = prompt.split("=", 1)[1]
        return {"reverse": s[::-1], "uppercase": s.upper(), "alphabetize": "".join(sorted(s)), "length": str(len(s))}[rule_name]
    if family == "boolean_pair":
        mt = re.fullmatch(r"TASK: p=(true|false); q=(true|false)", prompt)
        p, q = [x == "true" for x in mt.groups()]
        v = {"and": p and q, "or": p or q, "xor": p != q, "xnor": p == q}[rule_name]
        return str(v).lower()
    raise KeyError(family)


def unique_items(family, rule_name, n_dev, n_holdout, seed):
    rng = random.Random(seed)
    rules = [x[0] for x in m.FAMILIES[family]]
    for _ in range(10000):
        prompts, seen = [], set()
        while len(prompts) < n_dev:
            p = make_prompt(family, rng)
            if p not in seen:
                seen.add(p)
                prompts.append(p)
        signatures = {r: tuple(answer_for_prompt(family, r, p) for p in prompts) for r in rules}
        if len(set(signatures.values())) == len(rules):
            break
    else:
        raise RuntimeError(f"could not build uniquely diagnostic evidence set for {family}")
    dev = [{"prompt": p, "answer": answer_for_prompt(family, rule_name, p)} for p in prompts]
    holdout = []
    while len(holdout) < n_holdout:
        p = make_prompt(family, rng)
        if p not in seen:
            seen.add(p)
            holdout.append({"prompt": p, "answer": answer_for_prompt(family, rule_name, p)})
    return dev, holdout


def load_model(cfg):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_num_threads(int(cfg["runtime"]["torch_num_threads"]))
    mid = cfg["model"]["id"]
    rev = cfg["model"]["revision"]
    tok = AutoTokenizer.from_pretrained(mid, revision=rev)
    tok.padding_side = "left"
    if tok.pad_token_id is None:
        tok.pad_token_id = tok.eos_token_id
    model = AutoModelForCausalLM.from_pretrained(mid, revision=rev, torch_dtype=torch.float32)
    model.eval()
    return tok, model


def generate_batch(tok, model, systems, users, max_new_tokens, batch_size):
    import torch

    outs = []
    for start in range(0, len(users), batch_size):
        ss = systems[start : start + batch_size]
        us = users[start : start + batch_size]
        texts = []
        for s, u in zip(ss, us):
            msgs = [{"role": "system", "content": s}, {"role": "user", "content": u}]
            texts.append(tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True))
        batch = tok(texts, return_tensors="pt", padding=True)
        input_width = int(batch["input_ids"].shape[1])
        with torch.inference_mode():
            gen = model.generate(
                **batch,
                do_sample=False,
                max_new_tokens=max_new_tokens,
                pad_token_id=tok.eos_token_id,
            )
        for i in range(gen.shape[0]):
            outs.append(tok.decode(gen[i][input_width:], skip_special_tokens=True).strip())
    return outs


m.unique_items = unique_items
m.load_model = load_model
m.generate_batch = generate_batch


class StageLogger:
    def __init__(self, path, manifest_hash):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.path.write_text("", encoding="utf-8")
        self.manifest_hash = manifest_hash
        self.started = time.monotonic()

    def emit(self, stage, items_started, items_completed, batch_index):
        row = {
            "stage": stage,
            "elapsed_seconds": round(time.monotonic() - self.started, 6),
            "items_started": int(items_started),
            "items_completed": int(items_completed),
            "batch_index": int(batch_index),
            "input_manifest_hash": self.manifest_hash,
        }
        with self.path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, sort_keys=True) + "\n")
        print("EXECUTION_CHECKPOINT=" + json.dumps(row, sort_keys=True), flush=True)


def diagnostic_load_model(cfg, device, logger):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if device == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("diagnostic GPU requested but torch.cuda.is_available() is false")
    logger.emit("model_load", 0, 0, 0)
    torch.set_num_threads(int(cfg["runtime"]["torch_num_threads"]))
    mid = cfg["model"]["id"]
    rev = cfg["model"]["revision"]
    tok = AutoTokenizer.from_pretrained(mid, revision=rev)
    tok.padding_side = "left"
    if tok.pad_token_id is None:
        tok.pad_token_id = tok.eos_token_id
    model = AutoModelForCausalLM.from_pretrained(mid, revision=rev, torch_dtype=torch.float32)
    model.to(device)
    model.eval()
    logger.emit("model_load", 0, 0, 0)
    return tok, model


def materialize_diagnostic_case(case):
    surface = case["surface"]
    if surface == "candidate_selection":
        family = case["family"]
        target = {
            "family": family,
            "target_context": case["target_context"],
            "candidates": m.candidate_pool(family),
        }
        return {
            "case_id": case["case_id"],
            "surface": surface,
            "system": m.base_system(),
            "user": m.selection_prompt(target, case["assigned_evidence_text"]),
            "candidate_family": family,
            "max_new_tokens_kind": "selection",
        }
    if surface in ("task_answering", "regression"):
        family = case["policy_family"]
        rule = case["policy_rule_name"]
        candidate = next(c for c in m.candidate_pool(family) if c["rule_name"] == rule)
        return {
            "case_id": case["case_id"],
            "surface": surface,
            "system": m.patched_system(candidate["text"]),
            "user": case["prompt"],
            "candidate_family": None,
            "max_new_tokens_kind": "answer",
        }
    raise ValueError(f"unknown diagnostic surface: {surface}")


def validate_canonical_input_feasibility(cfg):
    required_unique = int(cfg["development_examples_per_target"]) + int(cfg["concealed_examples_per_target"])
    if "boolean_pair" in cfg["task_families"] and required_unique > 4:
        raise RuntimeError(
            "canonical input infeasible before model execution: boolean_pair has only 4 distinct input prompts, "
            f"but the frozen contract requests {required_unique} unique development+concealed prompts per target"
        )


def validate_diagnostic_separation(case):
    surface = case["surface"]
    if surface == "candidate_selection":
        canonical_context = f"Unknown fixed operation within family {case['family']}."
        if case["target_context"] == canonical_context:
            raise ValueError(f"diagnostic selection context could equal canonical context: {case['case_id']}")
        if not case["target_context"].startswith("Diagnostic-only "):
            raise ValueError(f"diagnostic selection context lacks diagnostic namespace: {case['case_id']}")
        return
    if surface == "task_answering":
        family = case["policy_family"]
        prompt = case["prompt"]
        if family == "pair_arithmetic":
            mt = re.fullmatch(r"TASK: a=(-?\d+); b=(-?\d+)", prompt)
            if not mt:
                raise ValueError(f"invalid diagnostic pair prompt: {case['case_id']}")
            a, b = map(int, mt.groups())
            if -12 <= a <= 12 and -12 <= b <= 12 and a != b:
                raise ValueError(f"diagnostic pair prompt lies inside canonical generator support: {case['case_id']}")
            return
        if family == "integer_list":
            vals = list(map(int, prompt.split("=", 1)[1].split(",")))
            if len(vals) == 5 and all(-9 <= v <= 15 for v in vals):
                raise ValueError(f"diagnostic list prompt lies inside canonical generator support: {case['case_id']}")
            return
        if family == "string_transform":
            s = prompt.split("=", 1)[1]
            letters = set("abcdefghijkmnpqrstuvwxyz")
            if len(s) == 6 and set(s) <= letters:
                raise ValueError(f"diagnostic string prompt lies inside canonical generator support: {case['case_id']}")
            return
        if family == "boolean_pair":
            raise ValueError("boolean task-answer diagnostics cannot be guaranteed disjoint from the canonical finite domain")
        raise KeyError(family)
    if surface == "regression":
        canonical_regressions = {x["prompt"] for x in m.regression_suite()}
        if case["prompt"] in canonical_regressions:
            raise ValueError(f"diagnostic regression duplicates canonical regression input: {case['case_id']}")
        return
    raise ValueError(f"unknown diagnostic surface: {surface}")


def validate_diagnostic_manifest(cfg, diag, materialized):
    if diag.get("status") != "FROZEN EXECUTION DIAGNOSTIC; NON-SCIENTIFIC":
        raise ValueError("diagnostic manifest status is not frozen/non-scientific")
    if diag["model"]["id"] != cfg["model"]["id"] or diag["model"]["revision"] != cfg["model"]["revision"]:
        raise ValueError("diagnostic model/revision does not match canonical config")
    case_ids = [x["case_id"] for x in materialized]
    if len(case_ids) != len(set(case_ids)):
        raise ValueError("diagnostic case_id values must be unique")
    raw_by_id = {x["case_id"]: x for x in diag["cases"]}
    for case_id in case_ids:
        validate_diagnostic_separation(raw_by_id[case_id])
    return {"canonical_exact_prompt_overlap_count": 0, "n_cases": len(materialized)}


def diagnostic_generate_group(tok, model, cases, cfg, device, logger, stage):
    import torch

    outs = []
    batch_size = int(cfg["runtime"]["batch_size"])
    max_new_tokens = int(
        cfg["generation"]["selection_max_new_tokens"]
        if cases[0]["max_new_tokens_kind"] == "selection"
        else cfg["generation"]["answer_max_new_tokens"]
    )
    total = len(cases)
    completed = 0
    batch_index = 0
    for start in range(0, total, batch_size):
        group = cases[start : start + batch_size]
        batch_index += 1
        end = start + len(group)
        logger.emit(stage, end, completed, batch_index)
        texts = []
        for case in group:
            msgs = [{"role": "system", "content": case["system"]}, {"role": "user", "content": case["user"]}]
            texts.append(tok.apply_chat_template(msgs, tokenize=False, add_generation_prompt=True))
        batch = tok(texts, return_tensors="pt", padding=True)
        input_width = int(batch["input_ids"].shape[1])
        batch = batch.to(device)
        with torch.inference_mode():
            gen = model.generate(
                **batch,
                do_sample=False,
                max_new_tokens=max_new_tokens,
                pad_token_id=tok.eos_token_id,
            )
        for i in range(gen.shape[0]):
            outs.append(tok.decode(gen[i][input_width:].detach().cpu(), skip_special_tokens=True).strip())
        completed = end
        logger.emit(stage, completed, completed, batch_index)
    return outs


def parse_diagnostic_output(case, text):
    if case["surface"] == "candidate_selection":
        candidates = m.candidate_pool(case["candidate_family"])
        return m.extract_candidate(text, candidates)
    return m.normalize_answer(text)


def compare_reference(reference_path, current_rows):
    reference = m.load_json(reference_path)
    ref_rows = reference.get("parsed_outputs", [])
    ref_map = {(r["case_id"], r["surface"]): r["parsed_output"] for r in ref_rows}
    cur_map = {(r["case_id"], r["surface"]): r["parsed_output"] for r in current_rows}
    keys = sorted(set(ref_map) | set(cur_map))
    mismatches = [
        {"case_id": key[0], "surface": key[1]}
        for key in keys
        if ref_map.get(key) != cur_map.get(key)
    ]
    return {
        "reference_manifest_hash": reference.get("diagnostic_manifest_hash"),
        "parsed_outputs_identical": len(mismatches) == 0,
        "mismatch_cases": mismatches,
    }


def diagnostic_main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--mode", choices=["diagnostic"], required=True)
    ap.add_argument("--diagnostic-manifest", required=True)
    ap.add_argument("--device", choices=["cpu", "cuda"], required=True)
    ap.add_argument("--outdir", default="results/asi0_execution_diagnostic")
    ap.add_argument("--reference-output")
    args = ap.parse_args()

    cfg = m.load_json(args.config)
    diag = m.load_json(args.diagnostic_manifest)
    manifest_hash = m.sha256_obj(diag)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    checkpoint_path = outdir / "diagnostic_checkpoints.jsonl"
    logger = StageLogger(checkpoint_path, manifest_hash)
    overall_start = time.monotonic()

    logger.emit("diagnostic_manifest_validation", 0, 0, 0)
    materialized = [materialize_diagnostic_case(case) for case in diag["cases"]]
    separation = validate_diagnostic_manifest(cfg, diag, materialized)
    logger.emit("diagnostic_manifest_validation", len(materialized), len(materialized), 0)

    tok, model = diagnostic_load_model(cfg, args.device, logger)
    parsed_rows = []
    stages = [
        ("diagnostic_candidate_selection", "candidate_selection"),
        ("diagnostic_task_answering", "task_answering"),
        ("diagnostic_regression", "regression"),
    ]
    for stage, surface in stages:
        cases = [x for x in materialized if x["surface"] == surface]
        if not cases:
            continue
        raw = diagnostic_generate_group(tok, model, cases, cfg, args.device, logger, stage)
        logger.emit("diagnostic_parsing", len(cases), 0, 0)
        for case, text in zip(cases, raw):
            parsed_rows.append(
                {
                    "case_id": case["case_id"],
                    "surface": case["surface"],
                    "parsed_output": parse_diagnostic_output(case, text),
                }
            )
        logger.emit("diagnostic_parsing", len(cases), len(cases), 0)

    parsed_rows.sort(key=lambda r: (r["surface"], r["case_id"]))
    total_runtime = time.monotonic() - overall_start
    summary = {
        "schema_version": 1,
        "mode": "diagnostic",
        "scientific_result": False,
        "scientific_outcomes_exposed": False,
        "device": args.device,
        "model": {"id": cfg["model"]["id"], "revision": cfg["model"]["revision"]},
        "diagnostic_manifest_hash": manifest_hash,
        "canonical_exact_prompt_overlap_count": separation["canonical_exact_prompt_overlap_count"],
        "n_cases": separation["n_cases"],
        "runtime_seconds": round(total_runtime, 6),
        "parsed_outputs": parsed_rows,
    }

    exit_code = 0
    if args.reference_output:
        equivalence = compare_reference(args.reference_output, parsed_rows)
        equivalence["same_manifest_hash"] = equivalence["reference_manifest_hash"] == manifest_hash
        equivalence["pass"] = bool(equivalence["same_manifest_hash"] and equivalence["parsed_outputs_identical"])
        summary["behavioral_equivalence"] = equivalence
        if not equivalence["pass"]:
            exit_code = 2

    m.write_json(outdir / "diagnostic_summary.json", summary)
    logger.emit("end", len(materialized), len(materialized), 0)
    print(
        "DIAGNOSTIC_COMPLETE="
        + json.dumps(
            {
                "scientific_result": False,
                "device": args.device,
                "diagnostic_manifest_hash": manifest_hash,
                "n_cases": len(parsed_rows),
                "runtime_seconds": round(total_runtime, 6),
                "behavioral_equivalence_pass": (
                    summary.get("behavioral_equivalence", {}).get("pass")
                    if args.reference_output
                    else None
                ),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    raise SystemExit(exit_code)


if __name__ == "__main__":
    if "--mode" in sys.argv:
        mode_index = sys.argv.index("--mode")
        mode = sys.argv[mode_index + 1] if mode_index + 1 < len(sys.argv) else None
        if mode == "diagnostic":
            diagnostic_main()
        else:
            raise SystemExit(f"unsupported mode: {mode}")
    else:
        cfg_path = sys.argv[1] if len(sys.argv) > 1 else None
        if cfg_path:
            validate_canonical_input_feasibility(m.load_json(cfg_path))
        m.main()

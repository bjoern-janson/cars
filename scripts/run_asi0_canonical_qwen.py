#!/usr/bin/env python3
import argparse
import hashlib
import json
import math
import random
import re
import statistics
from pathlib import Path


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def write_json(path, obj):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, sort_keys=True)
        f.write("\n")


def write_jsonl(path, rows):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")


def sha256_obj(obj):
    payload = json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def percentile(xs, q):
    ys = sorted(xs)
    p = q * (len(ys) - 1)
    lo = int(math.floor(p))
    hi = int(math.ceil(p))
    if lo == hi:
        return ys[lo]
    return ys[lo] * (hi - p) + ys[hi] * (p - lo)


FAMILIES = {
    "pair_arithmetic": [
        ("sum", "For TASK inputs with integers a and b, return a+b. Return only the integer."),
        ("difference", "For TASK inputs with integers a and b, return a-b. Return only the integer."),
        ("product", "For TASK inputs with integers a and b, return a*b. Return only the integer."),
        ("larger", "For TASK inputs with integers a and b, return the larger integer. Return only the integer."),
    ],
    "integer_list": [
        ("minimum", "For TASK inputs containing an integer list, return the minimum value. Return only the integer."),
        ("maximum", "For TASK inputs containing an integer list, return the maximum value. Return only the integer."),
        ("sum", "For TASK inputs containing an integer list, return the sum of all values. Return only the integer."),
        ("count_even", "For TASK inputs containing an integer list, return the count of even values. Return only the integer."),
    ],
    "string_transform": [
        ("reverse", "For TASK inputs containing a lowercase string s, return s reversed. Return only the transformed string."),
        ("uppercase", "For TASK inputs containing a lowercase string s, return s in uppercase. Return only the transformed string."),
        ("alphabetize", "For TASK inputs containing a lowercase string s, return its characters sorted alphabetically. Return only the transformed string."),
        ("length", "For TASK inputs containing a lowercase string s, return the number of characters in s. Return only the integer."),
    ],
    "boolean_pair": [
        ("and", "For TASK inputs with booleans p and q, return true iff p AND q is true. Return only true or false."),
        ("or", "For TASK inputs with booleans p and q, return true iff p OR q is true. Return only true or false."),
        ("xor", "For TASK inputs with booleans p and q, return true iff exactly one of p and q is true. Return only true or false."),
        ("xnor", "For TASK inputs with booleans p and q, return true iff p and q have the same truth value. Return only true or false."),
    ],
}


def candidate_pool(family):
    return [
        {"candidate_id": f"{family}:{name}", "rule_name": name, "text": text}
        for name, text in FAMILIES[family]
    ]


def make_item(family, rule_name, rng):
    if family == "pair_arithmetic":
        a = rng.randint(-12, 12)
        b = rng.randint(-12, 12)
        while b == a:
            b = rng.randint(-12, 12)
        prompt = f"TASK: a={a}; b={b}"
        if rule_name == "sum":
            ans = str(a + b)
        elif rule_name == "difference":
            ans = str(a - b)
        elif rule_name == "product":
            ans = str(a * b)
        elif rule_name == "larger":
            ans = str(max(a, b))
        else:
            raise KeyError(rule_name)
        return {"prompt": prompt, "answer": ans}
    if family == "integer_list":
        vals = [rng.randint(-9, 15) for _ in range(5)]
        prompt = "TASK: values=" + ",".join(map(str, vals))
        if rule_name == "minimum":
            ans = str(min(vals))
        elif rule_name == "maximum":
            ans = str(max(vals))
        elif rule_name == "sum":
            ans = str(sum(vals))
        elif rule_name == "count_even":
            ans = str(sum(v % 2 == 0 for v in vals))
        else:
            raise KeyError(rule_name)
        return {"prompt": prompt, "answer": ans}
    if family == "string_transform":
        letters = "abcdefghijkmnpqrstuvwxyz"
        s = "".join(rng.choice(letters) for _ in range(6))
        prompt = f"TASK: s={s}"
        if rule_name == "reverse":
            ans = s[::-1]
        elif rule_name == "uppercase":
            ans = s.upper()
        elif rule_name == "alphabetize":
            ans = "".join(sorted(s))
        elif rule_name == "length":
            ans = str(len(s))
        else:
            raise KeyError(rule_name)
        return {"prompt": prompt, "answer": ans}
    if family == "boolean_pair":
        p = bool(rng.getrandbits(1))
        q = bool(rng.getrandbits(1))
        prompt = f"TASK: p={str(p).lower()}; q={str(q).lower()}"
        if rule_name == "and":
            val = p and q
        elif rule_name == "or":
            val = p or q
        elif rule_name == "xor":
            val = p != q
        elif rule_name == "xnor":
            val = p == q
        else:
            raise KeyError(rule_name)
        return {"prompt": prompt, "answer": str(val).lower()}
    raise KeyError(family)


def unique_items(family, rule_name, n_dev, n_holdout, seed):
    rng = random.Random(seed)
    seen = set()
    dev = []
    holdout = []
    while len(dev) < n_dev:
        x = make_item(family, rule_name, rng)
        if x["prompt"] not in seen:
            seen.add(x["prompt"])
            dev.append(x)
    while len(holdout) < n_holdout:
        x = make_item(family, rule_name, rng)
        if x["prompt"] not in seen:
            seen.add(x["prompt"])
            holdout.append(x)
    return dev, holdout


def evidence_text(family, dev_items):
    lines = [
        f"Development evidence for an unknown fixed operation in family {family}.",
        "Each verified output is externally scored. Infer which candidate policy matches these examples.",
    ]
    for i, item in enumerate(dev_items, 1):
        lines.append(f"Example {i}: {item['prompt']} -> verified output: {item['answer']}")
    return "\n".join(lines)


def build_manifest(cfg, phase):
    pcfg = cfg["phases"][phase]
    rows = []
    for fi, family in enumerate(cfg["task_families"]):
        for ri, (rule_name, _) in enumerate(FAMILIES[family]):
            seed = int(pcfg["task_seed"]) + fi * 10000 + ri * 100
            dev, holdout = unique_items(
                family,
                rule_name,
                int(cfg["development_examples_per_target"]),
                int(cfg["concealed_examples_per_target"]),
                seed,
            )
            pool = candidate_pool(family)
            ev = evidence_text(family, dev)
            rows.append(
                {
                    "phase": phase,
                    "target_id": f"{phase}:{family}:{ri}",
                    "family": family,
                    "latent_rule_name": rule_name,
                    "target_context": f"Unknown fixed operation within family {family}.",
                    "evidence_id": f"{phase}:e:{family}:{ri}",
                    "evidence_text": ev,
                    "evidence_hash": hashlib.sha256(ev.encode()).hexdigest(),
                    "development_items": dev,
                    "candidate_count": len(pool),
                    "candidates": pool,
                    "candidate_pool_hash": sha256_obj(pool),
                    "concealed_items": holdout,
                    "concealed_items_hash": sha256_obj(holdout),
                }
            )
    return rows


def assign_evidence(manifest, seed):
    by_family = {}
    for row in manifest:
        by_family.setdefault(row["family"], []).append(row)
    source = {}
    rng = random.Random(seed)
    for family, rows in sorted(by_family.items()):
        rows = sorted(rows, key=lambda r: r["target_id"])
        offset = rng.randrange(1, len(rows))
        perm = rows[offset:] + rows[:offset]
        for target, src in zip(rows, perm):
            if target["target_id"] == src["target_id"]:
                raise AssertionError("misalignment fixed point")
            source[target["target_id"]] = src
    out = []
    for row in sorted(manifest, key=lambda r: r["target_id"]):
        out.append(
            {
                "target_id": row["target_id"],
                "arm": "aligned",
                "assigned_evidence_source_target_id": row["target_id"],
                "assigned_evidence_id": row["evidence_id"],
                "assigned_evidence_text": row["evidence_text"],
            }
        )
        src = source[row["target_id"]]
        out.append(
            {
                "target_id": row["target_id"],
                "arm": "misaligned",
                "assigned_evidence_source_target_id": src["target_id"],
                "assigned_evidence_id": src["evidence_id"],
                "assigned_evidence_text": src["evidence_text"],
            }
        )
    return out


def base_system():
    return (
        "You are a deterministic task agent. Inputs beginning TASK: belong to one target with an unknown fixed operation. "
        "If a TARGET-SPECIFIC POLICY is present below, apply it only to TASK: inputs. "
        "Inputs beginning REGRESSION: must follow the explicit regression instruction and ignore any target-specific policy. "
        "Return only the requested answer token; do not explain."
    )


def patched_system(patch):
    return base_system() + "\n\nTARGET-SPECIFIC POLICY:\n" + patch


def selection_prompt(target, assigned_evidence):
    opts = "\n".join(f"- {c['candidate_id']}: {c['text']}" for c in target["candidates"])
    return (
        "Select exactly one bounded policy patch for your own future TASK behavior.\n"
        f"Target context: {target['target_context']}\n\n"
        f"ASSIGNED DEVELOPMENT EVIDENCE:\n{assigned_evidence}\n\n"
        f"FROZEN CANDIDATE POOL:\n{opts}\n\n"
        "Return exactly one candidate_id from the pool and nothing else."
    )


def normalize_answer(text):
    s = text.strip().splitlines()[0].strip() if text.strip() else ""
    s = s.strip("`").strip().strip('"').strip("'")
    s = re.sub(r"^[Aa]nswer\s*:\s*", "", s).strip()
    return s


def extract_candidate(text, candidates):
    ids = [c["candidate_id"] for c in candidates]
    stripped = text.strip()
    for cid in ids:
        if stripped == cid:
            return cid
    hits = [cid for cid in ids if cid in stripped]
    return hits[0] if len(hits) == 1 else None


def load_model(cfg):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    torch.set_num_threads(int(cfg["runtime"]["torch_num_threads"]))
    mid = cfg["model"]["id"]
    rev = cfg["model"]["revision"]
    tok = AutoTokenizer.from_pretrained(mid, revision=rev)
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
        with torch.inference_mode():
            gen = model.generate(
                **batch,
                do_sample=False,
                max_new_tokens=max_new_tokens,
                pad_token_id=tok.eos_token_id,
            )
        for i in range(gen.shape[0]):
            prompt_len = int(batch["attention_mask"][i].sum().item())
            seq = gen[i][prompt_len:]
            outs.append(tok.decode(seq, skip_special_tokens=True).strip())
    return outs


def regression_suite():
    return [
        {"prompt": "REGRESSION: Return exactly PINE.", "answer": "PINE"},
        {"prompt": "REGRESSION: What is 2+2? Return only the integer.", "answer": "4"},
        {"prompt": "REGRESSION: Convert cat to uppercase. Return only the transformed string.", "answer": "CAT"},
        {"prompt": "REGRESSION: Which is larger, 7 or 3? Return only the integer.", "answer": "7"},
    ]


def score_outputs(outputs, items):
    return sum(normalize_answer(o) == item["answer"] for o, item in zip(outputs, items)) / len(items)


def evaluate_system(tok, model, system, items, cfg):
    systems = [system] * len(items)
    users = [x["prompt"] for x in items]
    outs = generate_batch(
        tok,
        model,
        systems,
        users,
        int(cfg["generation"]["answer_max_new_tokens"]),
        int(cfg["runtime"]["batch_size"]),
    )
    return score_outputs(outs, items), outs


def regression_cache(tok, model, cfg):
    suite = regression_suite()
    base_score, base_out = evaluate_system(tok, model, base_system(), suite, cfg)
    cache = {"BASE": {"score": base_score, "outputs": base_out, "pass": True}}
    for family in cfg["task_families"]:
        for cand in candidate_pool(family):
            score, outs = evaluate_system(tok, model, patched_system(cand["text"]), suite, cfg)
            cache[cand["candidate_id"]] = {
                "score": score,
                "outputs": outs,
                "pass": score >= base_score,
            }
    return cache


def bootstrap_gate(target_rows, cfg, phase):
    cvals = [r["C_i"] for r in target_rows]
    avals = [r["A_i"] for r in target_rows]
    C = statistics.fmean(cvals)
    A = statistics.fmean(avals)
    seed = int(cfg["inference"]["bootstrap_seed"]) + (0 if phase == "primary" else 1)
    rng = random.Random(seed)
    n = len(target_rows)
    bc = []
    ba = []
    for _ in range(int(cfg["inference"]["bootstrap_target_resamples"])):
        idx = [rng.randrange(n) for _ in range(n)]
        bc.append(statistics.fmean(cvals[i] for i in idx))
        ba.append(statistics.fmean(avals[i] for i in idx))
    q = float(cfg["inference"]["one_sided_lower_quantile"])
    LC = percentile(bc, q)
    LA = percentile(ba, q)
    return {
        "C": C,
        "A": A,
        "L_C": LC,
        "L_A": LA,
        "alpha_component_one_sided": float(cfg["inference"]["component_alpha"]),
        "joint_gate": bool(LC > 0 and LA > 0),
        "joint_null": "C <= 0 OR A <= 0",
        "joint_alternative": "C > 0 AND A > 0",
        "bootstrap_target_resamples": len(bc),
    }


def run_phase(tok, model, cfg, phase, outdir):
    manifest = build_manifest(cfg, phase)
    assignments = assign_evidence(manifest, int(cfg["phases"][phase]["assignment_seed"]))
    write_jsonl(Path(outdir) / f"asi0_{phase}_manifest.jsonl", manifest)
    write_jsonl(Path(outdir) / f"asi0_{phase}_assignments.jsonl", assignments)
    manifest_hash = sha256_obj(manifest)
    assignment_hash = sha256_obj(assignments)
    amap = {(r["target_id"], r["arm"]): r for r in assignments}

    selection_jobs = []
    for target in sorted(manifest, key=lambda r: r["target_id"]):
        for arm in ("aligned", "misaligned"):
            a = amap[(target["target_id"], arm)]
            selection_jobs.append((target, arm, selection_prompt(target, a["assigned_evidence_text"])))
    selection_outs = generate_batch(
        tok,
        model,
        [base_system()] * len(selection_jobs),
        [j[2] for j in selection_jobs],
        int(cfg["generation"]["selection_max_new_tokens"]),
        int(cfg["runtime"]["batch_size"]),
    )
    selections = {}
    for (target, arm, _), text in zip(selection_jobs, selection_outs):
        selections[(target["target_id"], arm)] = {
            "raw": text,
            "candidate_id": extract_candidate(text, target["candidates"]),
        }

    regressions = regression_cache(tok, model, cfg)
    rrng = random.Random(int(cfg["phases"][phase]["random_edit_seed"]))
    result_rows = []
    for target in sorted(manifest, key=lambda r: r["target_id"]):
        base_score, base_outs = evaluate_system(tok, model, base_system(), target["concealed_items"], cfg)
        arm_scores = {"base": base_score}
        arm_meta = {"base": {"outputs": base_outs}}
        for arm in ("aligned", "misaligned"):
            sel = selections[(target["target_id"], arm)]
            cid = sel["candidate_id"]
            candidate = next((c for c in target["candidates"] if c["candidate_id"] == cid), None)
            gate_pass = bool(candidate is not None and regressions[cid]["pass"])
            system = patched_system(candidate["text"]) if gate_pass else base_system()
            score, outs = evaluate_system(tok, model, system, target["concealed_items"], cfg)
            arm_scores[arm] = score
            arm_meta[arm] = {
                "selected_candidate_id": cid,
                "selection_raw": sel["raw"],
                "protected_regression_pass": gate_pass,
                "outputs": outs,
            }
        rc = rrng.choice(target["candidates"])
        rg = bool(regressions[rc["candidate_id"]]["pass"])
        rscore, routs = evaluate_system(
            tok,
            model,
            patched_system(rc["text"]) if rg else base_system(),
            target["concealed_items"],
            cfg,
        )
        arm_scores["random_edit"] = rscore
        arm_meta["random_edit"] = {
            "selected_candidate_id": rc["candidate_id"],
            "protected_regression_pass": rg,
            "outputs": routs,
        }
        result_rows.append(
            {
                "phase": phase,
                "target_id": target["target_id"],
                "family": target["family"],
                "latent_rule_name": target["latent_rule_name"],
                "base_score": base_score,
                "aligned_score": arm_scores["aligned"],
                "misaligned_score": arm_scores["misaligned"],
                "random_edit_score": arm_scores["random_edit"],
                "C_i": arm_scores["aligned"] - base_score,
                "A_i": arm_scores["aligned"] - arm_scores["misaligned"],
                "aligned": arm_meta["aligned"],
                "misaligned": arm_meta["misaligned"],
                "random_edit": arm_meta["random_edit"],
                "base_outputs": base_outs,
                "concealed_answers": [x["answer"] for x in target["concealed_items"]],
                "candidate_pool_hash": target["candidate_pool_hash"],
            }
        )
    gate = bootstrap_gate(result_rows, cfg, phase)
    summary = {
        "phase": phase,
        "model": cfg["model"],
        "manifest_hash": manifest_hash,
        "assignment_hash": assignment_hash,
        "n_targets": len(result_rows),
        "concealed_examples_per_target": int(cfg["concealed_examples_per_target"]),
        "mean_base_score": statistics.fmean(r["base_score"] for r in result_rows),
        "mean_aligned_score": statistics.fmean(r["aligned_score"] for r in result_rows),
        "mean_misaligned_score": statistics.fmean(r["misaligned_score"] for r in result_rows),
        "mean_random_edit_score": statistics.fmean(r["random_edit_score"] for r in result_rows),
        "aligned_valid_selection_rate": sum(r["aligned"]["selected_candidate_id"] is not None for r in result_rows) / len(result_rows),
        "misaligned_valid_selection_rate": sum(r["misaligned"]["selected_candidate_id"] is not None for r in result_rows) / len(result_rows),
        "aligned_regression_gate_pass_rate": sum(r["aligned"]["protected_regression_pass"] for r in result_rows) / len(result_rows),
        "misaligned_regression_gate_pass_rate": sum(r["misaligned"]["protected_regression_pass"] for r in result_rows) / len(result_rows),
        "gate": gate,
        "classification": "GREEN_REPLICATE" if gate["joint_gate"] else "STOP",
        "target_rows": result_rows,
        "regression_cache": regressions,
    }
    write_json(Path(outdir) / f"asi0_{phase}_result.json", summary)
    return summary


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("config")
    ap.add_argument("--outdir", default="results/asi0_canonical_run")
    args = ap.parse_args()
    cfg = load_json(args.config)
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    write_json(outdir / "frozen_config.json", cfg)
    tok, model = load_model(cfg)
    primary = run_phase(tok, model, cfg, "primary", outdir)
    replication = None
    if primary["gate"]["joint_gate"]:
        replication = run_phase(tok, model, cfg, "replication", outdir)
    final = {
        "study": cfg["study"],
        "scientific_result": True,
        "primary": {k: v for k, v in primary.items() if k not in ("target_rows", "regression_cache")},
        "replication": (
            {k: v for k, v in replication.items() if k not in ("target_rows", "regression_cache")}
            if replication
            else None
        ),
        "asi0_green": bool(primary["gate"]["joint_gate"] and replication is not None and replication["gate"]["joint_gate"]),
        "maximum_claim_if_green": cfg["interpretation"]["maximum_green_claim"],
        "nonclaims": cfg["interpretation"]["nonclaims"],
    }
    write_json(outdir / "asi0_final_summary.json", final)
    print("ASI0_FINAL_SUMMARY=" + json.dumps(final, sort_keys=True))


if __name__ == "__main__":
    main()

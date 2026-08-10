#!/usr/bin/env python3
import importlib.util
import random
import re
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

if __name__ == "__main__":
    m.main()

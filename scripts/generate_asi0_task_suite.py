#!/usr/bin/env python3
"""Generate ASI-0 development/selection/hidden task bundles.

Development uses the committed public seed. Selection/hidden require an external
secret seed file. The agent-facing bundle never contains answer keys.
"""

import argparse
import hashlib
import json
import random
from pathlib import Path


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def stable_seed(base, *parts):
    payload = "::".join([str(base), *map(str, parts)]).encode("utf-8")
    return int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")


def shuffled_choice(rng, prompt, options, correct_index):
    order = list(range(len(options)))
    rng.shuffle(order)
    labels = ["A", "B", "C", "D"]
    rendered = []
    answer = None
    for pos, original in enumerate(order):
        rendered.append(f"{labels[pos]}. {options[original]}")
        if original == correct_index:
            answer = labels[pos]
    return prompt + "\n\n" + "\n".join(rendered) + "\n\nReturn only A, B, C, or D.", answer


def coding_bug(rng, variant):
    n = rng.randint(3, 12)
    if variant == 0:
        prompt = f"Spec: clamp x to the inclusive interval [-{n}, {n}].\nBuggy: def f(x): return min(-{n}, max(x, {n}))\nChoose the correct local replacement for the return expression."
        opts = [f"min({n}, max(-{n}, x))", f"max({n}, min(-{n}, x))", f"min(-{n}, max({n}, x))", f"max(-{n}, max({n}, x))"]
        return shuffled_choice(rng, prompt, opts, 0)
    if variant == 1:
        prompt = "Spec: return True exactly when integer x is even.\nBuggy: def f(x): return x % 2 == 1\nChoose the correct local replacement."
        opts = ["x % 2 == 0", "x % 2 == 1", "x // 2 == 0", "bool(x % 2)"]
        return shuffled_choice(rng, prompt, opts, 0)
    if variant == 2:
        prompt = f"Spec: return the number of integers in inclusive range [a,b] when a<=b, else 0.\nBuggy: def f(a,b): return max(0, b-a)\nChoose the correct local replacement."
        opts = ["max(0, b-a+1)", "max(0, a-b+1)", "b-a", "abs(b-a)+1"]
        return shuffled_choice(rng, prompt, opts, 0)
    if variant == 3:
        prompt = f"Spec: return True iff x is strictly between -{n} and {n}.\nBuggy: def f(x): return -{n} <= x <= {n}\nChoose the correct local replacement."
        opts = [f"-{n} < x < {n}", f"-{n} <= x < {n}", f"-{n} < x <= {n}", f"abs(x) <= {n}"]
        return shuffled_choice(rng, prompt, opts, 0)
    prompt = "Spec: return absolute difference |a-b|.\nBuggy: def f(a,b): return a-b\nChoose the correct local replacement."
    opts = ["abs(a-b)", "abs(a)+abs(b)", "max(a,b)-min(0,b)", "(a-b)**2"]
    return shuffled_choice(rng, prompt, opts, 0)


def novel_coding(rng, variant):
    k = rng.randint(2, 6)
    if variant == 0:
        prompt = f"Choose the implementation that returns the count of values in xs divisible by {k}."
        opts = [f"sum(1 for x in xs if x % {k} == 0)", f"sum(x for x in xs if x % {k} == 0)", f"len([x for x in xs if x % {k}])", f"sum(1 for x in xs if x // {k} == 0)"]
        return shuffled_choice(rng, prompt, opts, 0)
    if variant == 1:
        prompt = "Choose the implementation that returns the sum of squares of strictly positive values in xs."
        opts = ["sum(x*x for x in xs if x > 0)", "sum(x for x in xs if x*x > 0)", "sum(abs(x) for x in xs if x > 0)", "sum(x*x for x in xs if x >= 0) + 1"]
        return shuffled_choice(rng, prompt, opts, 0)
    if variant == 2:
        prompt = "Choose the implementation that removes duplicates while preserving first-occurrence order."
        opts = ["list(dict.fromkeys(xs))", "list(set(xs))", "sorted(set(xs))", "[x for x in xs if xs.count(x) == 1]"]
        return shuffled_choice(rng, prompt, opts, 0)
    if variant == 3:
        prompt = f"Choose the implementation that returns the index of the first value in xs >= {k}, or -1 if none exists."
        opts = [f"next((i for i,x in enumerate(xs) if x >= {k}), -1)", f"next((x for x in xs if x >= {k}), -1)", f"min((i for i,x in enumerate(xs) if x >= {k}), default=0)", f"sum(1 for x in xs if x < {k})"]
        return shuffled_choice(rng, prompt, opts, 0)
    prompt = f"Choose the implementation that rotates xs right by {k} positions, returning a new list; empty xs returns empty."
    opts = [f"xs[-({k}%len(xs)):] + xs[:-({k}%len(xs))] if xs else []", f"xs[{k}:] + xs[:{k}]", f"list(reversed(xs))", f"xs[-{k}:] + xs[:-{k}]"]
    return shuffled_choice(rng, prompt, opts, 0)


def verification(rng, variant):
    if variant == 0:
        req = ["R1 score is an integer", "R2 0 <= score <= 10", "R3 name is non-empty", "R4 tags has no duplicates"]
        bad = rng.choice([0, 1, 2, 3])
        cases = [
            '{"name":"Ada","score":7.5,"tags":["x","y"]}',
            '{"name":"Ada","score":11,"tags":["x","y"]}',
            '{"name":"","score":7,"tags":["x","y"]}',
            '{"name":"Ada","score":7,"tags":["x","x"]}',
        ]
    elif variant == 1:
        req = ["R1 ids is sorted ascending", "R2 ids is non-empty", "R3 all ids are positive", "R4 ids has unique values"]
        bad = rng.choice([0, 1, 2, 3])
        cases = ["ids=[1,3,2]", "ids=[]", "ids=[-1,2,3]", "ids=[1,2,2]"]
    elif variant == 2:
        req = ["R1 retries <= 3", "R2 timeout > 0", "R3 mode is safe or fast", "R4 enabled is boolean"]
        bad = rng.choice([0, 1, 2, 3])
        cases = ["retries=4, timeout=5, mode=safe, enabled=true", "retries=2, timeout=0, mode=safe, enabled=true", "retries=2, timeout=5, mode=turbo, enabled=true", "retries=2, timeout=5, mode=safe, enabled=1"]
    elif variant == 3:
        req = ["R1 total equals a+b", "R2 a >= 0", "R3 b >= 0", "R4 label starts with T-"]
        bad = rng.choice([0, 1, 2, 3])
        cases = ["a=2,b=3,total=6,label=T-x", "a=-1,b=3,total=2,label=T-x", "a=2,b=-1,total=1,label=T-x", "a=2,b=3,total=5,label=X"]
    else:
        req = ["R1 start < end", "R2 end-start <= 10", "R3 priority is 1..5", "R4 owner is lowercase"]
        bad = rng.choice([0, 1, 2, 3])
        cases = ["start=5,end=5,priority=3,owner=ada", "start=1,end=20,priority=3,owner=ada", "start=1,end=5,priority=8,owner=ada", "start=1,end=5,priority=3,owner=Ada"]
    prompt = "Exactly one requirement is violated. Which one?\n" + "\n".join(req) + "\nArtifact: " + cases[bad]
    opts = ["R1", "R2", "R3", "R4"]
    return shuffled_choice(rng, prompt, opts, bad)


def research_synthesis(rng, variant):
    claims = ["Kappa", "Lambda", "Mu", "Nu"]
    scores = [rng.randint(-2, 2) for _ in claims]
    winner = variant % 4
    scores[winner] = max(scores) + 3
    cards = []
    cid = 1
    for claim, score in zip(claims, scores):
        sign = "supports" if score >= 0 else "contradicts"
        for _ in range(abs(score) + 1):
            cards.append(f"C{cid}: {sign} {claim}")
            cid += 1
    rng.shuffle(cards)
    prompt = "Each evidence card either supports or contradicts one conclusion. Choose the conclusion with the highest net support (supports minus contradicts).\n" + "\n".join(cards)
    return shuffled_choice(rng, prompt, claims, winner)


def tool_workflow(rng, variant):
    variants = [
        ("state: raw. Goal: archived. Tools: CLEAN raw→clean; CHECK clean→verified; ARCHIVE verified→archived; SEND clean→sent.", ["CLEAN,CHECK,ARCHIVE", "CLEAN,ARCHIVE", "CHECK,CLEAN,ARCHIVE", "CLEAN,SEND"], 0),
        ("state: draft. Goal: published. Tools: REVIEW draft→reviewed; SIGN reviewed→signed; PUBLISH signed→published; DELETE draft→deleted.", ["REVIEW,SIGN,PUBLISH", "SIGN,PUBLISH", "REVIEW,PUBLISH", "DELETE"], 0),
        ("state: cold. Goal: stored. Tools: HEAT cold→warm; PACK warm→packed; STORE packed→stored; COOL warm→cold.", ["HEAT,PACK,STORE", "PACK,STORE", "HEAT,STORE", "HEAT,COOL"], 0),
        ("state: source. Goal: deployed. Tools: BUILD source→binary; TEST binary→tested; DEPLOY tested→deployed; RUN binary→running.", ["BUILD,TEST,DEPLOY", "BUILD,DEPLOY", "TEST,BUILD,DEPLOY", "BUILD,RUN"], 0),
        ("state: request. Goal: closed. Tools: TRIAGE request→triaged; FIX triaged→fixed; VERIFY fixed→verified; CLOSE verified→closed.", ["TRIAGE,FIX,VERIFY,CLOSE", "FIX,VERIFY,CLOSE", "TRIAGE,FIX,CLOSE", "TRIAGE,CLOSE"], 0),
    ]
    prompt, opts, answer = variants[variant % len(variants)]
    return shuffled_choice(rng, "Choose the valid minimal workflow.\n" + prompt, opts, answer)


GENERATORS = {
    "coding_bug": coding_bug,
    "novel_coding": novel_coding,
    "verification": verification,
    "research_synthesis": research_synthesis,
    "tool_workflow": tool_workflow,
}


def get_seed(cfg, split, secret_seed_file):
    if split == "development":
        return int(cfg["development_seed"])
    if not secret_seed_file:
        raise ValueError(f"{split} generation requires --secret-seed-file")
    secret = load_json(secret_seed_file)
    if split not in secret or not isinstance(secret[split], int):
        raise ValueError(f"secret seed file must contain integer field {split!r}")
    return int(secret[split])


def generate(cfg, split, seed):
    if split not in cfg["counts"]:
        raise ValueError(f"unknown split {split!r}")
    variants = list(map(int, cfg["variant_partition"][split]))
    tasks = []
    for family, count in cfg["counts"][split].items():
        if family not in GENERATORS:
            raise ValueError(f"no generator for family {family}")
        for index in range(int(count)):
            rng = random.Random(stable_seed(seed, split, family, index))
            variant = rng.choice(variants)
            prompt, answer = GENERATORS[family](rng, variant)
            suffix = hashlib.sha256(f"{seed}:{split}:{family}:{index}".encode()).hexdigest()[:10]
            tasks.append({
                "id": f"{split}-{family}-{index:03d}-{suffix}",
                "split": split,
                "family": family,
                "variant": variant,
                "prompt": prompt,
                "answer": answer,
                "scoring": {"type": "exact_choice"},
            })
    random.Random(stable_seed(seed, split, "order")).shuffle(tasks)
    return tasks


def digest_without_answers(tasks):
    public = [{k: v for k, v in t.items() if k != "answer"} for t in tasks]
    payload = json.dumps(public, sort_keys=True, separators=(",", ":")).encode()
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("config")
    parser.add_argument("--split", choices=["development", "selection", "hidden"], required=True)
    parser.add_argument("--secret-seed-file")
    parser.add_argument("--agent-out", required=True)
    parser.add_argument("--evaluator-out", required=True)
    args = parser.parse_args()

    cfg = load_json(args.config)
    seed = get_seed(cfg, args.split, args.secret_seed_file)
    tasks = generate(cfg, args.split, seed)
    public_tasks = [{k: v for k, v in t.items() if k != "answer"} for t in tasks]
    digest = digest_without_answers(tasks)

    agent_bundle = {
        "schema_version": 1,
        "study": cfg["study"],
        "split": args.split,
        "task_count": len(public_tasks),
        "public_bundle_digest": digest,
        "tasks": public_tasks,
    }
    evaluator_bundle = {
        "schema_version": 1,
        "study": cfg["study"],
        "split": args.split,
        "task_count": len(tasks),
        "public_bundle_digest": digest,
        "tasks": tasks,
        "guardrail": "Evaluator bundle contains answer keys and must not be exposed to the candidate generator or evaluated agent.",
    }

    Path(args.agent_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.evaluator_out).parent.mkdir(parents=True, exist_ok=True)
    Path(args.agent_out).write_text(json.dumps(agent_bundle, indent=2) + "\n", encoding="utf-8")
    Path(args.evaluator_out).write_text(json.dumps(evaluator_bundle, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "split": args.split,
        "task_count": len(tasks),
        "public_bundle_digest": digest,
        "agent_out": args.agent_out,
        "evaluator_out": args.evaluator_out,
        "seed_disclosed": args.split == "development",
    }, indent=2))


if __name__ == "__main__":
    main()

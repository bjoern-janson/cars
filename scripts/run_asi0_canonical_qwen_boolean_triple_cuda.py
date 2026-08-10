#!/usr/bin/env python3
"""Final pre-outcome CUDA execution path for repaired ASI-0 Qwen.

This wrapper changes only execution placement relative to the prospectively
validated boolean-triple canonical path:
  - model -> CUDA
  - tokenized input tensors -> CUDA

Model revision, tokenizer, prompts, float32 dtype, generation settings, batch
size, parsing, task generation, assignment, estimands, inference, and
replication logic remain delegated to the frozen canonical implementation.

Diagnostic mode patches the same load_model() and generate_batch() functions
used by canonical execution, so a passing diagnostic validates the final path.
"""
import importlib.util
import sys
from pathlib import Path

BOOLEAN = Path(__file__).with_name("run_asi0_canonical_qwen_boolean_triple.py")
spec = importlib.util.spec_from_file_location("asi0_boolean_triple", BOOLEAN)
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

DEVICE = "cuda"


def load_model(cfg):
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer

    if not torch.cuda.is_available():
        raise RuntimeError("frozen CUDA execution path requested but torch.cuda.is_available() is false")
    torch.set_num_threads(int(cfg["runtime"]["torch_num_threads"]))
    mid = cfg["model"]["id"]
    rev = cfg["model"]["revision"]
    tok = AutoTokenizer.from_pretrained(mid, revision=rev)
    tok.padding_side = "left"
    if tok.pad_token_id is None:
        tok.pad_token_id = tok.eos_token_id
    model = AutoModelForCausalLM.from_pretrained(mid, revision=rev, torch_dtype=torch.float32)
    model.to(DEVICE)
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
        batch = batch.to(DEVICE)
        with torch.inference_mode():
            gen = model.generate(
                **batch,
                do_sample=False,
                max_new_tokens=max_new_tokens,
                pad_token_id=tok.eos_token_id,
            )
        for i in range(gen.shape[0]):
            token_ids = gen[i][input_width:].detach().cpu()
            outs.append(tok.decode(token_ids, skip_special_tokens=True).strip())
    return outs


# Canonical execution uses these exact functions through the base module.
b.e.m.load_model = load_model
b.e.m.generate_batch = generate_batch


def diagnostic_load_model(cfg, device, logger):
    if device != DEVICE:
        raise RuntimeError(f"final-path diagnostic requires --device {DEVICE}")
    logger.emit("model_load", 0, 0, 0)
    tok, model = load_model(cfg)
    logger.emit("model_load", 0, 0, 0)
    return tok, model


def diagnostic_generate_group(tok, model, cases, cfg, device, logger, stage):
    if device != DEVICE:
        raise RuntimeError(f"final-path diagnostic requires --device {DEVICE}")
    batch_size = int(cfg["runtime"]["batch_size"])
    max_new_tokens = int(
        cfg["generation"]["selection_max_new_tokens"]
        if cases[0]["max_new_tokens_kind"] == "selection"
        else cfg["generation"]["answer_max_new_tokens"]
    )
    outs = []
    completed = 0
    batch_index = 0
    total = len(cases)
    for start in range(0, total, batch_size):
        group = cases[start : start + batch_size]
        batch_index += 1
        end = start + len(group)
        logger.emit(stage, end, completed, batch_index)
        outs.extend(
            generate_batch(
                tok,
                model,
                [case["system"] for case in group],
                [case["user"] for case in group],
                max_new_tokens,
                batch_size,
            )
        )
        completed = end
        logger.emit(stage, completed, completed, batch_index)
    return outs


# Diagnostic mode now exercises the same canonical load/generate functions.
b.e.diagnostic_load_model = diagnostic_load_model
b.e.diagnostic_generate_group = diagnostic_generate_group


def main_dispatch():
    if "--mode" in sys.argv:
        mode_index = sys.argv.index("--mode")
        mode = sys.argv[mode_index + 1] if mode_index + 1 < len(sys.argv) else None
        if mode != "diagnostic":
            raise SystemExit(f"unsupported mode: {mode}")
        b.e.diagnostic_main()
        return

    cfg_path = sys.argv[1] if len(sys.argv) > 1 else None
    if cfg_path:
        b.validate_repaired_canonical_input_feasibility(b.e.m.load_json(cfg_path))
    b.e.m.main()


if __name__ == "__main__":
    main_dispatch()

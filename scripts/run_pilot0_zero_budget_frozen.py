#!/usr/bin/env python3
"""Run zero-budget Pilot 0 from one frozen generation configuration.

This wrapper is the official Qwen3-4B execution entrypoint. It makes the same
model snapshot and sampling parameters drive pre, E0, and E+. Before post runs,
it fails closed if the frozen branch metadata shows a different pre-treatment
generation regime.
"""

from __future__ import annotations

import argparse
import json
import math
import subprocess
import sys
from pathlib import Path


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
    return rows


def same_float(a: object, b: float) -> bool:
    try:
        return math.isclose(float(a), float(b), rel_tol=0.0, abs_tol=1e-12)
    except (TypeError, ValueError):
        return False


def verify_model_manifest(config: dict, model_dir: Path) -> None:
    manifest_path = model_dir / "pilot0_model_manifest.json"
    if not manifest_path.exists():
        raise ValueError(
            f"missing {manifest_path}; run scripts/cache_pilot0_qwen3_4b.py first"
        )
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if manifest.get("repo_id") != config["model"]["repo_id"]:
        raise ValueError("cached model repo_id differs from frozen config")
    if manifest.get("revision") != config["model"]["revision"]:
        raise ValueError("cached model revision differs from frozen config")


def verify_post_input(config: dict, model_dir: Path, input_path: Path) -> None:
    expected_model = str(model_dir)
    generation = config["generation"]
    rows = read_jsonl(input_path)
    if not rows:
        raise ValueError("post input contains no branches")

    for row in rows:
        row_id = row.get("id")
        checks = {
            "pre_model_requested": row.get("pre_model_requested") == expected_model,
            "pre_backend": row.get("pre_backend") == config["model"]["backend"],
            "pre_reasoning_effort": row.get("pre_reasoning_effort") == "non-thinking",
            "pre_temperature": same_float(row.get("pre_temperature"), generation["temperature"]),
            "pre_top_p": same_float(row.get("pre_top_p"), generation["top_p"]),
            "pre_top_k": row.get("pre_top_k") == generation["top_k"],
        }
        failed = [name for name, ok in checks.items() if not ok]
        if failed:
            raise ValueError(
                f"branch {row_id!r}: frozen pre-treatment generation config differs "
                f"from current zero-budget config: {failed}"
            )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("stage", choices=["pre", "post"])
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("experiments/PILOT0_QWEN3_4B_CONFIG.json"),
    )
    parser.add_argument(
        "--model-dir",
        type=Path,
        default=Path("/kaggle/working/pilot0-qwen3-4b"),
    )
    parser.add_argument("--limit", type=int)
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    verify_model_manifest(config, args.model_dir)
    if args.stage == "post":
        verify_post_input(config, args.model_dir, args.input)

    generation = config["generation"]
    runner = Path(__file__).with_name("run_pilot0_local.py")
    cmd = [
        sys.executable,
        str(runner),
        args.stage,
        str(args.input),
        str(args.output),
        "--model",
        str(args.model_dir),
        "--seed",
        str(generation["base_seed"]),
        "--temperature",
        str(generation["temperature"]),
        "--top-p",
        str(generation["top_p"]),
        "--top-k",
        str(generation["top_k"]),
        "--parse-retries",
        str(generation["parse_retries"]),
        "--pre-max-new-tokens",
        str(generation["pre_max_new_tokens"]),
        "--post-max-new-tokens",
        str(generation["post_max_new_tokens"]),
    ]
    if args.limit is not None:
        cmd += ["--limit", str(args.limit)]

    print("frozen execution config verified", file=sys.stderr)
    print(" ".join(cmd), file=sys.stderr)
    completed = subprocess.run(cmd, check=False)
    return completed.returncode


if __name__ == "__main__":
    raise SystemExit(main())

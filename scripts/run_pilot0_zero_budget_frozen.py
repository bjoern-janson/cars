#!/usr/bin/env python3
"""Run zero-budget Pilot 0 from one frozen generation configuration.

This wrapper is the official Qwen3-4B execution entrypoint. It makes the same
model snapshot, interface contract, and sampling parameters drive pre, E0, and
E+. Before post runs, it fails closed if frozen branch metadata shows a
different pre-treatment generation regime.
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


def expected_checks(config: dict, model_dir: Path, row: dict, prefix: str) -> dict[str, bool]:
    generation = config["generation"]
    interface = config["interface"]
    expected_model = str(model_dir)
    return {
        f"{prefix}model_requested": row.get(f"{prefix}model_requested") == expected_model,
        f"{prefix}backend": row.get(f"{prefix}backend") == config["model"]["backend"],
        f"{prefix}reasoning_effort": row.get(f"{prefix}reasoning_effort") == "non-thinking",
        f"{prefix}temperature": same_float(row.get(f"{prefix}temperature"), generation["temperature"]),
        f"{prefix}top_p": same_float(row.get(f"{prefix}top_p"), generation["top_p"]),
        f"{prefix}top_k": row.get(f"{prefix}top_k") == generation["top_k"],
        f"{prefix}interface_version": row.get(f"{prefix}interface_version") == interface["version"],
        f"{prefix}assistant_prefill": row.get(f"{prefix}assistant_prefill") == interface["assistant_prefill"],
    }


def verify_pre_output(config: dict, model_dir: Path, output_path: Path) -> None:
    rows = read_jsonl(output_path)
    if not rows:
        raise ValueError("pre output contains no rows")
    for row in rows:
        normalized = dict(row)
        normalized["pre_model_requested"] = row.get("model_requested")
        normalized["pre_backend"] = row.get("backend")
        normalized["pre_reasoning_effort"] = row.get("reasoning_effort")
        normalized["pre_temperature"] = row.get("temperature")
        normalized["pre_top_p"] = row.get("top_p")
        normalized["pre_top_k"] = row.get("top_k")
        normalized["pre_interface_version"] = row.get("interface_version")
        normalized["pre_assistant_prefill"] = row.get("assistant_prefill")
        failed = [name for name, ok in expected_checks(config, model_dir, normalized, "pre_").items() if not ok]
        if failed:
            raise ValueError(f"pre row {row.get('id')!r}: frozen config mismatch: {failed}")


def verify_post_input(config: dict, model_dir: Path, input_path: Path) -> None:
    rows = read_jsonl(input_path)
    if not rows:
        raise ValueError("post input contains no branches")

    for row in rows:
        failed = [name for name, ok in expected_checks(config, model_dir, row, "pre_").items() if not ok]
        if failed:
            raise ValueError(
                f"branch {row.get('id')!r}: frozen pre-treatment config differs "
                f"from current zero-budget config: {failed}"
            )


def verify_post_output(config: dict, model_dir: Path, output_path: Path) -> None:
    rows = read_jsonl(output_path)
    if not rows:
        raise ValueError("post output contains no rows")
    interface = config["interface"]
    for row in rows:
        failed: list[str] = []
        if row.get("post_model_requested") != str(model_dir):
            failed.append("post_model_requested")
        if row.get("post_backend") != config["model"]["backend"]:
            failed.append("post_backend")
        if row.get("post_reasoning_effort") != "non-thinking":
            failed.append("post_reasoning_effort")
        if row.get("post_interface_version") != interface["version"]:
            failed.append("post_interface_version")
        if row.get("post_assistant_prefill") != interface["assistant_prefill"]:
            failed.append("post_assistant_prefill")
        if failed:
            raise ValueError(f"post row {row.get('id')!r}: frozen config mismatch: {failed}")


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
    if completed.returncode != 0:
        return completed.returncode

    if args.stage == "pre":
        verify_pre_output(config, args.model_dir, args.output)
    else:
        verify_post_output(config, args.model_dir, args.output)
    print("frozen output config verified", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

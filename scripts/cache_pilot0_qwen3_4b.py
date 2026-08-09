#!/usr/bin/env python3
"""Resolve the exact frozen Qwen3-4B snapshot for zero-budget Pilot 0.

This is execution plumbing only. It pins the model files to the revision declared
in experiments/PILOT0_QWEN3_4B_CONFIG.json so pre, E0, and E+ cannot silently
resolve different upstream model states.

The helper resolves the pinned snapshot through Hugging Face's shared cache,
then creates a lightweight symlink view in /kaggle/working. This avoids copying
or re-downloading multi-GB weights when the exact snapshot is already cached.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from huggingface_hub import snapshot_download


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def link_snapshot(snapshot: Path, output: Path) -> None:
    output.mkdir(parents=True, exist_ok=True)
    for source in snapshot.iterdir():
        destination = output / source.name
        if destination.exists() or destination.is_symlink():
            if destination.is_symlink() and destination.resolve() == source.resolve():
                continue
            if destination.name == "pilot0_model_manifest.json":
                continue
            raise ValueError(
                f"refusing to overwrite existing non-matching path: {destination}"
            )
        destination.symlink_to(source.resolve(), target_is_directory=source.is_dir())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("experiments/PILOT0_QWEN3_4B_CONFIG.json"),
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/kaggle/working/pilot0-qwen3-4b"),
    )
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    repo_id = config["model"]["repo_id"]
    revision = config["model"]["revision"]

    snapshot = Path(
        snapshot_download(
            repo_id=repo_id,
            revision=revision,
        )
    ).resolve()
    link_snapshot(snapshot, args.output)

    manifest = {
        "repo_id": repo_id,
        "revision": revision,
        "resolved_snapshot_path": str(snapshot),
        "model_view_path": str(args.output.resolve()),
        "cached_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "config_sha256": sha256_file(args.config),
    }
    manifest_path = args.output / "pilot0_model_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"resolved {repo_id}@{revision}")
    print(f"shared snapshot: {snapshot}")
    print(f"model view: {args.output}")
    print(f"manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

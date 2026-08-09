#!/usr/bin/env python3
"""Download the exact frozen Qwen3-4B snapshot for zero-budget Pilot 0.

This is execution plumbing only. It pins the model files to the revision declared
in experiments/PILOT0_QWEN3_4B_CONFIG.json so pre, E0, and E+ cannot silently
resolve different upstream model states.
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("experiments/PILOT0_QWEN3_4B_CONFIG.json"))
    parser.add_argument("--output", type=Path, default=Path("/kaggle/working/pilot0-qwen3-4b"))
    args = parser.parse_args()

    config = json.loads(args.config.read_text(encoding="utf-8"))
    repo_id = config["model"]["repo_id"]
    revision = config["model"]["revision"]

    resolved = Path(
        snapshot_download(
            repo_id=repo_id,
            revision=revision,
            local_dir=str(args.output),
        )
    )

    manifest = {
        "repo_id": repo_id,
        "revision": revision,
        "resolved_path": str(resolved.resolve()),
        "cached_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "config_sha256": sha256_file(args.config),
    }
    manifest_path = args.output / "pilot0_model_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    print(f"cached {repo_id}@{revision}")
    print(f"model path: {resolved}")
    print(f"manifest: {manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

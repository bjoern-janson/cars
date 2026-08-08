#!/usr/bin/env python3
"""Verify hashes recorded in FREEZE.json."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
manifest = json.loads((root / "FREEZE.json").read_text(encoding="utf-8"))
for rel, expected in manifest["files"].items():
    actual = "sha256:" + hashlib.sha256((root / rel).read_bytes()).hexdigest()
    if actual != expected:
        raise SystemExit(f"hash mismatch: {rel}\nexpected {expected}\nactual   {actual}")
print(f"verified {len(manifest['files'])} frozen CARS v{manifest['version']} artifacts")

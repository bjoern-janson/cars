#!/usr/bin/env python3
"""Outcome-blind audit repair for the frozen Pilot 0 A4c analyzer.

The original analyzer incorrectly required one full inline user-message hash per
rendering across both E0 and EV. Because the signal text is part of that single
user message, E0 and EV must legitimately have different hashes.

This wrapper changes only validate_rows(): full rendered-message stability is
checked within each rendering x signal cell (the two replicated branches), while
semantic-state identity is still checked across renderings within each signal.
All estimands, collapse logic, bootstrap, randomization inference, Holm
adjustment, Q_N gate, and A4c decision logic are imported unchanged from the
frozen analyzer.
"""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Sequence

import analyze_pilot0_a4c as frozen


def validate_rows(rows: Sequence[dict], config: dict) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    expected_randomization_seed = int(config["assignment"]["randomization_seed"])
    base_seed = int(config["invariants"]["generation_base_seed"])
    retries = int(config["invariants"]["parse_retries"])
    expected_each = int(config["assignment"]["branches_per_cell_per_block"])
    expected_total = int(config["assignment"]["branches_per_block"])
    signals = config["factors"]["signal"]

    for row in rows:
        task_id = str(row.get("task_id") or row.get("stratum") or "")
        if not task_id or str(row.get("stratum")) != task_id:
            raise ValueError(f"branch {row.get('id')}: invalid task_id/stratum")
        cell = str(row.get("a4c_cell") or row.get("arm") or "")
        if cell not in frozen.CELLS or str(row.get("arm")) != cell:
            raise ValueError(f"branch {row.get('id')}: invalid/disagreeing A4c cell")
        rendering, signal = frozen.CELL_FACTORS[cell]
        if str(row.get("rendering")) != rendering or str(row.get("signal")) != signal:
            raise ValueError(f"branch {row['id']}: cell factors disagree")
        if str(row.get("signal_text")) != str(signals[signal]):
            raise ValueError(f"branch {row['id']}: signal text differs from frozen contract")
        if row.get("rendering_bridge_verified") is not True:
            raise ValueError(f"branch {row['id']}: rendering bridge provenance missing")
        if int(row.get("randomization_seed", -1)) != expected_randomization_seed:
            raise ValueError(f"branch {row['id']}: wrong randomization seed")
        v = float(row.get("v"))
        if v not in (0.0, 1.0):
            raise ValueError(f"branch {row['id']}: V must be binary")
        expected_base = frozen.stable_seed(base_seed, f"a4c::{row['id']}")
        if int(row.get("post_base_generation_seed", -1)) != expected_base:
            raise ValueError(f"branch {row['id']}: generation base seed is not branch-id-fixed")
        if row.get("post_seed_rule_arm_independent") is not True:
            raise ValueError(f"branch {row['id']}: arm-independent seed provenance missing")
        used_seed = int(row.get("post_generation_seed", -1))
        if not (expected_base <= used_seed <= expected_base + retries):
            raise ValueError(f"branch {row['id']}: parse-retry seed outside frozen range")
        grouped[task_id].append(row)

    for task_id, block_rows in grouped.items():
        if len(block_rows) != expected_total:
            raise ValueError(f"block {task_id}: expected {expected_total} rows, got {len(block_rows)}")
        counts = Counter(str(row["a4c_cell"]) for row in block_rows)
        expected = {cell: expected_each for cell in frozen.CELLS}
        if dict(counts) != expected:
            raise ValueError(f"block {task_id}: cell counts {dict(counts)} != {expected}")

        initial = {str(row["initial_answer"]).strip().upper() for row in block_rows}
        benchmark = {str(row["benchmark_answer"]).strip().upper() for row in block_rows}
        prestates = {str(row["pre_state_sha256"]) for row in block_rows}
        if len(initial) != 1 or len(benchmark) != 1 or len(prestates) != 1:
            raise ValueError(f"block {task_id}: frozen prestate fields disagree")
        if next(iter(initial)) == next(iter(benchmark)):
            raise ValueError(f"block {task_id}: A4c contains initially-correct prestate")

        # Across renderings, semantic state must be identical conditional on signal.
        # E0 and EV are intentionally different semantic states because signal_text differs.
        for signal in ("E0", "EV"):
            signal_rows = [row for row in block_rows if str(row["signal"]) == signal]
            semantic_hashes = {str(row.get("semantic_state_sha256", "")) for row in signal_rows}
            semantic_payloads = {str(row.get("semantic_state_json", "")) for row in signal_rows}
            if len(semantic_hashes) != 1 or len(semantic_payloads) != 1:
                raise ValueError(f"block {task_id} signal {signal}: rendering changed semantic state")

        # Full inline rendering contains the signal; therefore it is invariant only
        # within a rendering x signal cell, not across E0 and EV.
        for cell in frozen.CELLS:
            cell_rows = [row for row in block_rows if str(row["a4c_cell"]) == cell]
            message_hashes = {str(row.get("user_message_sha256", "")) for row in cell_rows}
            messages = {str(row.get("user_message", "")) for row in cell_rows}
            if len(message_hashes) != 1 or len(messages) != 1:
                raise ValueError(f"block {task_id} {cell}: rendering changed across replicated branches")

        canonical_rows = [row for row in block_rows if str(row["rendering"]) == "L_canonical"]
        legacy_rows = [row for row in block_rows if str(row["rendering"]) == "L_legacy"]
        if any(
            str(row.get("user_message_sha256", "")) != str(row.get("canonical_user_message_sha256", ""))
            for row in canonical_rows
        ):
            raise ValueError(f"block {task_id}: L_canonical provenance mismatch")
        if any(
            str(row.get("user_message_sha256", "")) != str(row.get("legacy_user_message_sha256", ""))
            for row in legacy_rows
        ):
            raise ValueError(f"block {task_id}: L_legacy provenance mismatch")

    return dict(grouped)


# Replace only the faulty audit function. All inferential machinery remains frozen.
frozen.validate_rows = validate_rows


if __name__ == "__main__":
    raise SystemExit(frozen.main())

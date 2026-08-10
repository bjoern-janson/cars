#!/usr/bin/env bash
set -euo pipefail

CONFIG="experiments/ASI0_CANONICAL_QWEN_CONFIG.json"
DIAG_MANIFEST="experiments/ASI0_CPU_GPU_DIAGNOSTIC_MANIFEST.json"
CPU_REFERENCE="results/ASI0_CPU_BEHAVIORAL_REFERENCE.json"
CUDA_RUNNER="scripts/run_asi0_canonical_qwen_boolean_triple_cuda.py"
GATE_OUTDIR="results/asi0_execution_diagnostic_gpu_final_path"
CANONICAL_OUTDIR="results/asi0_canonical_run_2"

# Final pre-outcome execution gate. Exit code is nonzero on any manifest or
# parsed-output mismatch, so set -e prevents canonical execution on failure.
python "$CUDA_RUNNER" \
  "$CONFIG" \
  --mode diagnostic \
  --diagnostic-manifest "$DIAG_MANIFEST" \
  --device cuda \
  --reference-output "$CPU_REFERENCE" \
  --outdir "$GATE_OUTDIR"

# No additional engineering or inspection step occurs between a passing gate
# and the first outcome-bearing repaired canonical execution.
python "$CUDA_RUNNER" \
  "$CONFIG" \
  --outdir "$CANONICAL_OUTDIR"

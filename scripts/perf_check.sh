#!/usr/bin/env bash
set -euo pipefail

ARTIFACTS=${1:-.artifacts/perf}
mkdir -p "$ARTIFACTS"

echo "Running synthetic performance scenario..."
ru-it-audit run-notebooks --inventory examples/inventory/sample_inventory.csv --answers-dir examples/inputs --out-dir "$ARTIFACTS/notebooks"
time ru-it-audit build-report --artifacts-dir "$ARTIFACTS/notebooks" --out-html "$ARTIFACTS/report.html" --out-pdf "$ARTIFACTS/report.pdf"

#!/usr/bin/env bash
set -euo pipefail

ruff it_audit_report tests
mypy it_audit_report
if command -v nbqa >/dev/null 2>&1; then
  nbqa ruff notebooks || true
fi
yamllint checklists

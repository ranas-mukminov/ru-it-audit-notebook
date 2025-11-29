#!/usr/bin/env bash
set -euxo pipefail

ruff check it_audit_report tests
mypy it_audit_report
if command -v nbqa >/dev/null 2>&1; then
  nbqa ruff notebooks || true
fi
yamllint checklists

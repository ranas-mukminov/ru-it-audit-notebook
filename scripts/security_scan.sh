#!/usr/bin/env bash
set -euxo pipefail

if command -v pip-audit >/dev/null 2>&1; then
  pip-audit
fi

bandit -q -r it_audit_report || true

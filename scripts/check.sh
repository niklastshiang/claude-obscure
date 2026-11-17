#!/usr/bin/env bash
# The repository's checks: the pre-commit hook and CI both run this script.
# Needs bash, python3 and shellcheck. Runs `claude plugin validate` when the claude CLI is on PATH
# (CI installs it); set CLAUDE_CLI to use another command.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

shellcheck install.sh scripts/check.sh .githooks/pre-commit
python3 -I scripts/check_repo.py

claude_cli=${CLAUDE_CLI:-claude}
if command -v "${claude_cli%% *}" >/dev/null 2>&1; then
  # shellcheck disable=SC2086 # CLAUDE_CLI may be a command with arguments (npx -y ...)
  out=$($claude_cli plugin validate . 2>&1) || { printf '%s\n' "$out"; exit 1; }
  grep -q 'Validation passed' <<<"$out" || { printf '%s\n' "$out"; exit 1; }
  echo "plugin validate: passed" >&2
else
  echo "plugin validate: skipped, no claude CLI on PATH" >&2
fi

#!/usr/bin/env bash
# Mirrors the "Checked by" column in CONSTRAINTS.md. On any deviation, CONSTRAINTS.md wins.
#   fast: after every change (< {{FAST_BUDGET}})
#   task: before every commit, also the pre-commit hook (< {{TASK_BUDGET}})
#   full: CI; everything in task, the floor guard over the whole push (BASE), and slow checks
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

stage="${1:-task}"
case "$stage" in
  fast | task | full) ;;
  *) echo "check.sh: unknown tier '$stage' (use fast, task or full)" >&2; exit 2 ;;
esac

# A scaffold with unfilled placeholders is not a project yet.
if unfilled=$(git ls-files -co --exclude-standard -z | xargs -0 grep -IlE '\{\{[A-Z0-9_]+\}\}' --); then
  echo "check.sh: unfilled placeholders in:" >&2
  printf '  %s\n' "${unfilled//$'\n'/$'\n'  }" >&2
  exit 2
fi

# The hook must be on in every clone (principle *Hook in every clone*); CI sets CI and needs none.
if [[ "$stage" != fast && -z "${CI:-}" && "$(git config --get core.hooksPath || true)" != .githooks ]]; then
  echo "check.sh: the pre-commit hook is not enabled in this clone. Run:" >&2
  echo "  git config core.hooksPath .githooks" >&2
  exit 2
fi

floor_guard=("{{FLOOR_GUARD}}") # the floor guard command, one array element per word

fast() {
  : "{{FAST_COMMANDS}}" # replace this whole line with the tier's commands, one per line
}

task() {
  : "{{TASK_COMMANDS}}" # replace this whole line with the tier's commands, one per line
}

full() {
  : "{{FULL_COMMANDS}}" # replace this whole line with the tier's commands, one per line
  if [[ -n "${BASE:-}" && "$BASE" != 0000000000000000000000000000000000000000 ]]; then
    "${floor_guard[@]}" --base "$BASE"
  fi
}

fast
if [[ "$stage" != fast ]]; then task; fi
if [[ "$stage" == full ]]; then full; fi

# Constraints

Last reviewed: {{DATE}} by the project owner (Day 1).

Applies to {{SCOPE}}.

## Floor (always enforced, no setup required)

- No new suppression comments: {{SUPPRESSIONS}}
- No unimplemented stubs: {{STUBS}}
- No skipped or deleted tests without a reason in the commit message: {{SKIPS}}
- No secrets in source: tokens and keys only come from the environment or the platform's credential store
- No build output or large binaries in git: {{IGNORED_ARTIFACTS}} are in `.gitignore`
- This file does not get weakened to make a change pass

Checked by `{{FLOOR_GUARD}}` (diff-based, exit 0 clean / 1 violation / 2 guard could not run), ported from the reference in `agent-skills/constraint-driven-development/references/floor-guard.md`.

## Enforced with numbers

| Dimension | Rule | Checked by | Runs at |
|-----------|------|-----------|---------|
| Lint | Zero errors | `{{LINT}}` | fast, task, full |
| Format | Zero files needing reformat | `{{FORMAT}}` | fast, task, full |
| Floor | Zero floor violations in the diff | `{{FLOOR_GUARD}}` (CI: `--base` = the state before the push) | fast, task, full |
| Tests | All tests pass | `{{TEST}}` | task, full |
| Coverage | Line coverage >= {{COVERAGE}} % of {{COVERAGE_SCOPE}} | `{{COVERAGE_CMD}}` | task, full |
| Version | The version is an integer and the same everywhere it appears | a test in the suite | task, full |
| Secrets | No secrets anywhere in the git history | `gitleaks git . --redact --no-banner` | full (CI) |

Reasons:
- **Coverage {{COVERAGE}} %** ({{DATE}}): {{COVERAGE_REASON}}
- **Violations block:** `.githooks/pre-commit` runs `scripts/check.sh task`; a red check prevents the commit. CI runs `scripts/check.sh full` on every push and pull request.
- **Time budget:** `fast` < {{FAST_BUDGET}}, `task` < {{TASK_BUDGET}}.

## Measured, not yet enforced

| Metric | Today | Direction |
|--------|-------|-----------|
| – | – | – |

## Exceptions

| ID | Rule | Path | Reason | Owner | Expires |
|----|------|------|--------|-------|---------|

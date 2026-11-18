# claude-skills: project rules

This repository follows its own skill, `skills/house-rules/SKILL.md` (plugin `kickoff`). The Day 1 decisions
for this repository:

- Language: files, comments and commit messages in English; Claude talks with the owner in
  German.
- Licence: MIT (owner, 2026-11-16). Third-party skills keep their own licence (agent-skills, clarity,
  TokenEconomizer: MIT as of 2026-11-17; graphify: Apache-2.0 as of 2026-11-18) and are fetched,
  never copied into this repository.
- Runtime: Claude Code 2.1.324 or later (TokenEconomizer's marketplace is pinned by commit);
  bash and git for `install.sh`; Python 3.10 or later for the checks and for TokenEconomizer, 3.11 or later for graphify.
- Versions: plain integers 1, 2, 3 … as in `principles.md` (owner, 2026-11-18). Until the first
  release, after Phase 3 of `tasks/plan.md`, the plugin manifest has no `version`, so every
  commit is an update. The first release sets `"version": "1"` and the tag `1`, together with a
  check that the two agree.
- Hosting: GitHub, public.
- Third-party code is pinned to reviewed commits. To move a pin, read the diff since the old
  commit (for plugins with hooks: every hook and script), then change the sha in
  `.claude-plugin/marketplace.json` and `install.sh` together, and write the review into the commit
  message. `scripts/check_repo.py` fails when the two files disagree. graphify is a Python
  package, not a plugin: its sha stands in `install.sh` (`GRAPHIFY_SHA`) and `README.md`; to move
  it, read what `graphify install` writes, the hooks it can register, and every network path.
- Facts about outside projects (licence, last commit, maintenance) come from the web on the
  day they are written down, with that date.
- Secrets: none belong in this repository.

## Checks

One tier, it takes seconds: `scripts/check.sh` (shellcheck, `scripts/check_repo.py`,
`claude plugin validate .`). The pre-commit hook and CI (`.github/workflows/check.yml`) run it.
Enable the hook in every clone: `git config core.hooksPath .githooks`.

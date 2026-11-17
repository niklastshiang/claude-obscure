# To do

- [ ] **New name for the repository** (owner, 2026-11-17). The marketplace name `niklastshiang` and the plugin names are not tied to it, but the install lines in the README and `plugin.json` are.

- [ ] **Version numbering** (Day 1, item 4). For now `plugin.json` has no `version`, so every commit is an update (Claude's recommendation, 2026-11-16). `claude plugin validate` warns about it; the check accepts the warning.

- [ ] **Lektorat skills** (owner, 2026-11-17: they stay their own plugin, `lektorat@lektorat-skills`, in `~/Projekte/Buch/lektorat-skills`). That repository has no remote yet. Once it is on GitHub, it can be listed in this marketplace like agent-skills. Replaces the 2026-11-16 plan to move them in here.

- [x] **Load it as a plugin, like addyosmani/agent-skills** (owner, 2026-11-16; done 2026-11-17). `.claude-plugin/marketplace.json` lists `owner-led-projects` (source `./`), `agent-skills` and `clarity` (both `github` sources pinned to the shas `install.sh` uses); `owner-led-projects` depends on the other two. No `version`. `install.sh` stays for cloud environments. Names: marketplace `niklastshiang`, plugin `owner-led-projects`.
  - Verified: `claude plugin validate .` passes (one warning: no version); on the owner's machine `claude plugin install owner-led-projects@niklastshiang` installed all three (Claude Code 2.1.326); `clarity` loads without a manifest of its own as 4 skills (its 3 commands become skills; about 212 tokens per session).
  - Format checked 2026-11-17 in code.claude.com/docs/en/plugins/marketplace-reference.md and manifest-reference.md.

- [x] **Add microsoft/TokenEconomizer** (owner, 2026-11-16; installed 2026-11-17). Not listed in this marketplace: its `plugin/lib` is a symlink to `../../tokeneconomizer`, which a `git-subdir` checkout of `plugin/` leaves dangling. Installed from its own marketplace, pinned with `@b57d03f81585a18b936a0eaecbd1eb51cdcecf71` (2026-11-16); the install copy holds the package (checked: `lib/tokeneconomizer` is a real folder).
  - Corrections to the 2026-11-16 note: the licence is MIT again since `3a29982` (2026-11-16), though its `plugin.json` still says Apache-2.0.
  - Read before pinning: `hooks/hooks.json` (SessionStart, UserPromptSubmit, PostToolUse, PostToolUseFailure, Stop, SessionEnd), `scripts/te-hook`, `te_bootstrap.py`, `sidecall.py`, `context.py`. No network code of its own; model calls go through `claude -p` with `--tools ""`, no MCP servers, and model `haiku`; it starts detached background processes, writes `~/.tokeneconomizer`, and with tool pruning on writes deny rules into a repository's `.claude/settings.local.json`.
  - Settings (owner, 2026-11-17): `microskills=on toolprune=off loopguard=off`, global.

- [x] **Checks for this repository** (owner, 2026-11-17; done 2026-11-17): `scripts/check.sh` runs shellcheck, `scripts/check_repo.py` (pins agree and are full shas, skill front matter, README table) and `claude plugin validate .`; `.githooks/pre-commit` and `.github/workflows/check.yml` run it. Verified: green on this branch; a changed sha in `install.sh` fails it.

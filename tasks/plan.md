# Implementation Plan: /kickoff:lets-a-go

Source spec: `SPEC-lets-a-go.md` (approved by the owner, 2026-11-17)

## Overview

Rename the plugin to `kickoff` and its rules skill to `house-rules`, add the skill `lets-a-go`, the owner's `principles.md` and the core templates, move the Day 1 list out of `house-rules`, and prove the result with three dry runs (GTK/Python, Android, adopt mode). Tasks are in `tasks/todo.md`.

## Starting point

- Branch `plugin-marketplace`. The marketplace work of 2026-11-16/17 is **not committed**: `README.md`, `TODO.md`, `install.sh` and `skills/owner-led-projects/SKILL.md` are modified; `.claude-plugin/`, `.claude/`, `.githooks/`, `.github/` and `scripts/` are untracked. Task 0 commits it, so the rename has a clean base.
- The plugin is installed from the local directory marketplace at user scope, as `owner-led-projects@niklastshiang`. After the rename it must be reinstalled under the new name.
- `scripts/check_repo.py` treats every folder under `skills/` as a skill and requires its name in the README, so `lets-a-go` needs a README row from its first commit.

## Architecture Decisions

- **Rename first.** The names appear in every later file. Renaming at the start means nothing is written twice, and the riskiest unknown, how a renamed plugin and its skills show up in a fresh session, is answered on day one.
- **`lets-a-go` grows in vertical slices.** It is usable after every task: first it only creates the folder, then it asks the principles, then the decisions, then it writes the scaffold.
- **Day 1 items are split, not copied.** The items in `house-rules` that are the owner's answers (language rule, release numbering, AI disclosure, quality bar, check tiers, secrets, facts from the web, hook per clone) move into `principles.md` with their *Why*. The items that depend on the project (licence, runtime versions, hosting and store rules) become steps in `lets-a-go`. `house-rules` keeps a pointer. Every rule then lives in one place.
- **Templates in `skills/lets-a-go/templates/`,** so the cloud `install.sh` copies them with the skill and `check_repo.py` needs no special case for them.
- **No floor guard in the templates.** `lets-a-go` ports it per project from the agent-skills reference (spec, *Never*).

## Task List

### Phase 0: Clean base
- [x] Task 0: Commit the uncommitted marketplace work (owner confirms)

### Phase 1: Names
- [x] Task 1: Rename plugin `owner-led-projects` → `kickoff`, skill → `house-rules`, reinstall
- [x] Task 2: Skill `lets-a-go`, first slice: where the project goes (new folder or adopt mode)

### Checkpoint A: Names
- [x] `scripts/check.sh` green (2026-11-18)
- [x] In an empty folder, a new session lists `/kickoff:lets-a-go` and `/kickoff:house-rules` with no install step (2026-11-18, `claude -p` in an empty scratch folder; no `owner-led-projects` left in `claude plugin list`)
- [ ] Owner reviews

### Phase 2: The run
- [x] Task 3: `principles.md` and its check
- [x] Task 4: `lets-a-go` asks principles and project decisions; ADR template
- [x] Task 5: Core templates, part 1: `CLAUDE.md`, `CONSTRAINTS.md`
- [x] Task 6: Core templates, part 2: `check.sh`, hook, CI; template check
- [x] Task 7: `lets-a-go` writes the scaffold and closes the run (recipe, final checks)
- [x] Task 8: `house-rules` without its own Day 1 list

### Checkpoint B: The run
- [x] `scripts/check.sh` green
- [x] Owner reads `principles.md` and `skills/lets-a-go/SKILL.md`

### Phase 3: Proof
- [ ] Task 9: Dry run GTK/Python
- [ ] Task 10: Dry run Android
- [ ] Task 11: Dry run adopt mode on a copy of `claude-obscure`
- [ ] Task 12: README and TODO.md

### Checkpoint C: Complete
- [ ] Every Success Criterion in the spec is met
- [ ] Fresh-context review (`doubt-driven-development`) of `lets-a-go` and `principles.md`
- [ ] Owner approves; spec status set to implemented

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| A stale `owner-led-projects` install stays enabled next to `kickoff`, so the rules load twice | Med | Task 1 uninstalls the old name before installing the new one and checks `~/.claude/settings.json` and `installed_plugins.json` |
| Plugin skills are only reachable with the full `plugin:skill` name | Low | Accepted: `/kickoff:lets-a-go` is the decided name; Task 1 records how it actually appears |
| The Android dry run cannot get the task tier green because the toolchain (JDK, Android SDK, Gradle) is not on the machine (Fedora Atomic) | High | The recipe sets the toolchain up (owner, 2026-11-17), e.g. in a toolbox container, and records how in the project's `CLAUDE.md` |
| The recipe is written from one stack and misses what another needs | Med | Two dry runs on different stacks; findings go into the recipe, never into a stack-specific branch |
| Moving the Day 1 *Why* lines loses the history behind them | Low | Task 8 checks that every Day 1 item of today's skill appears in `principles.md` or in `lets-a-go` |
| Dry runs depend on today's web (versions, licences) | Low | Intended: the spec requires dated sources. Results are compared by structure, not by version numbers |

## Parallelization

None worth it. Every task edits the same few files or builds on the one before; the dry runs read the finished skill. One session, in order.

## Decided (owner, 2026-11-17)

- Task 0: the uncommitted marketplace work is committed as it is, in one commit.
- Task 10: a missing toolchain is set up, not just named; the task tier must be green.

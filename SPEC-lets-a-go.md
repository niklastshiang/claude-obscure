# Spec: /kickoff:lets-a-go — V1

Status: approved by the owner (2026-11-17). Source: `docs/ideas/lets-a-go.md`.

## Objective

A skill `lets-a-go` in the `kickoff` plugin (formerly `owner-led-projects`), invoked as `/kickoff:lets-a-go`. One session with it turns an empty folder into a project scaffold whose Day 1 decisions are made and written down. Nothing has to run yet.

User: the owner, alone. Projects: desktop apps today, possibly Android or another stack tomorrow.

What it must do:

1. **Never ask a principle twice.** The owner's recurring answers live in `principles.md`. The skill shows them in one table and asks a single question: "anything different this time?". A deviation becomes an ADR in the project; `principles.md` changes only when the owner says so.
2. **Prepare every project decision.** Decisions that depend on the project are asked one at a time, each after research on the web, with options, a recommendation and sources. Each answer becomes an ADR.
3. **Build the scaffold.** Files that do not depend on the stack are copied from templates and filled in. The stack-specific part is worked out fresh from a recipe, so versions are current on the day.
4. **Adopt existing folders.** In a folder that already holds a project, the skill asks only the missing decisions and adds only the missing files. It never overwrites.

### The run, step by step

1. **Where.** New project: ask for the name and a one-line purpose, then create `YYYY-MM-DD_Name` (today's date) in the current directory. If the current directory is itself inside a git repository, ask before creating anything. Existing project (the folder has files): switch to adopt mode and list which Day 1 decisions and which scaffold files are missing.
2. **Principles.** Show `principles.md` as a table. One question: anything different? Record deviations as ADRs.
3. **Project decisions,** in this order, one question each, every one with sources from the web dated today:
   1. What it is and where it runs (platforms, distribution channel)
   2. Stack: language, UI toolkit, build tool
   3. Versions: the newest stable release that every core dependency supports, per component
   4. Licence of the project, checked against the licences of the core dependencies
   5. Rules of the chosen forge and store on AI-generated code and on who must submit
   6. Any item the recipe marks as a decision for this stack
4. **Scaffold.** Fill the core templates (the skill writes them; no script substitution). Then work through the stack recipe: the commands behind the three check tiers, lint/format/test configuration, the floor guard ported from the reference in `agent-skills/constraint-driven-development/references/floor-guard.md` with this language's suppression patterns, `.gitignore`, one smoke test so the task tier has something to run, and the licence text fetched from its official source.
5. **Close.** `git init`, `git config core.hooksPath .githooks`, run the task tier, and make the first commit. Last checks: no `{{UPPER_SNAKE}}` placeholder left in any file; every decision from steps 2 and 3 has an ADR; the hook ran. Then summarise and suggest `spec-driven-development` for the product itself.

## Tech Stack

- Claude Code 2.1.324 or later; the skill is Markdown (`SKILL.md` plus templates)
- `principles.md`: Markdown
- Checks of this repository: bash, Python 3.10 or later (standard library only), shellcheck, as today
- No runtime code in the generated projects comes from this repository except the templates

## Commands

```
Check this repository:   scripts/check.sh
Enable the hook:         git config core.hooksPath .githooks
Validate the plugin:     claude plugin validate .
Use the skill:           /kickoff:lets-a-go
Cloud install:           bash install.sh
```

## Project Structure

```
skills/house-rules/SKILL.md              renamed from owner-led-projects; Day 1 list replaced by a pointer to lets-a-go
skills/house-rules/README-template.md    unchanged; lets-a-go reads it from here
skills/lets-a-go/SKILL.md                the run, the stack recipe, adopt mode
skills/lets-a-go/principles.md           the owner's principles (public)
skills/lets-a-go/templates/            core files, copied and filled per project
  CLAUDE.md
  CONSTRAINTS.md
  scripts/check.sh                       tier interface (fast / task / full), commands filled per stack
  .githooks/pre-commit                   runs scripts/check.sh task
  .github/workflows/check.yml            runs scripts/check.sh full
  docs/adr/0000-template.md
scripts/check_repo.py                    extended (see Testing Strategy)
docs/ideas/lets-a-go.md                the one-pager
SPEC-lets-a-go.md                      this file
```

The templates live inside the skill folder so that `install.sh` (cloud) copies them with it.

## Code Style

Skills follow `house-rules`: imperative rules, a one-line *Why* where a rule comes from a concrete event, named skills instead of repeated content. `principles.md` holds one rule per entry, with who decided and when:

```markdown
| Topic | Rule | Decided |
|---|---|---|
| Runtime versions | The newest stable release that every core dependency supports, checked on the web on Day 1 with sources; checked again before each release, updated in its own commit | owner, 2026-11-17 |
```

Templates use `{{UPPER_SNAKE}}` placeholders. Files and commit messages in English; the skill talks to the owner in the owner's language.

## Testing Strategy

The skill is prose, so most of its testing is running it.

- **Automatic** (`scripts/check.sh`, hook and CI), `check_repo.py` gains:
  - `skills/lets-a-go/templates/` holds every file listed under Project Structure
  - `principles.md` exists, every row has a rule and a "Decided" entry
  - the existing checks keep working with two skills (front matter, README table)
  - `install.sh` copies the templates (covered by its copy of the whole skill folder; checked once by hand)
- **Dry runs** (by hand, before the work counts as done):
  1. New GTK/Python app in a scratch folder
  2. New Android app in a scratch folder (the stack the templates were not built from)
  3. Adopt mode on a copy of `claude-obscure` itself
- Each dry run passes the Success Criteria below; findings go into the recipe, not into special cases.

## Boundaries

- **Always:** ask project decisions one at a time with a recommendation and dated sources; write an ADR per decision; run `scripts/check.sh` before every commit here; check every text for readers with `clarity`
- **Ask first:** changing `principles.md`; adding a file to the core templates; anything in the generated project that is not in the recipe; creating a folder inside an existing git repository
- **Never:** overwrite an existing file in adopt mode; ask a principle that `principles.md` answers; pick a version from memory; copy third-party code into this repository (the floor guard is ported per project from the reference, not vendored here); weaken a check in a generated project to get the first commit green

## Success Criteria

- [ ] In an empty directory, a new session lists `/kickoff:lets-a-go` with no install step
- [ ] A dry run for a new project ends with: the dated folder, a first commit, the task tier green, the pre-commit hook active, CI workflow present, no `{{UPPER_SNAKE}}` placeholder in any file
- [ ] Every principle in `principles.md` is shown once and none of them is asked as a question
- [ ] Every project decision has an ADR with options, the choice, and sources dated the day of the run
- [ ] The GTK and the Android dry runs use the same templates and the same recipe, with no stack-specific branch in `SKILL.md`
- [ ] Adopt mode on an existing project changes no existing file and lists what it added
- [ ] `house-rules` no longer carries its own Day 1 list; it points to `lets-a-go`
- [ ] The README describes the user-scope setup and the new skill; `scripts/check.sh` is green

## Out of Scope (Deferred)

- Running program on Day 1 (walking skeleton): the owner wants decisions and a scaffold first
- Stack profiles with pinned versions: they go stale and contradict "newest version"
- Use by other people: personal defaults stay personal
- Plugin evals for skill triggering: the problem was availability, solved by user scope
- `/retro` to feed lessons back into skill and defaults: decide after the next real project
- Repository rename: after this work (owner, 2026-11-17)

## Decided (owner, 2026-11-17)

- **Licence:** a project decision every time (step 3.4), not a principle.
- **Release numbering:** a principle in `principles.md`: plain integers 1, 2, 3 …, +1 per release, every release counts, fixes included (as Stickler ADR 0006).
- **Names:** plugin `kickoff` (formerly `owner-led-projects`), skill `lets-a-go`, call `/kickoff:lets-a-go`, principles file `principles.md`, rules skill `house-rules` (formerly `owner-led-projects`, called as `/kickoff:house-rules`).
- **Placeholders** are filled by Claude, checked by "no `{{UPPER_SNAKE}}` placeholder left".
- **The Day 1 list** moves from `house-rules` (formerly `owner-led-projects`) into `lets-a-go`, which gains an adopt mode for existing projects.
- **The project folder** is created in the current directory; inside a git repository, ask first.
- **`principles.md`** lives in `skills/lets-a-go/`, next to the skill, so `install.sh` copies it for cloud sessions (owner, 2026-11-17; the spec first put it at the repository root).
- **The floor guard** is ported per project from the agent-skills reference, not vendored here.
- **AI disclosure:** a principle in `principles.md`: every project publishes how it was made (who wrote the code, who decided, which guardrails held, what the AI cost).

## Open Questions


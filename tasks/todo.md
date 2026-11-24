# Tasks: /kickoff:lets-a-go

Plan: `tasks/plan.md`. Spec: `SPEC-lets-a-go.md`. Every task ends with `scripts/check.sh` green and one commit.

## Phase 0: Clean base

## Task 0: Commit the uncommitted marketplace work

**Description:** The plugin marketplace, the checks, the hook and CI exist only in the working tree of branch `plugin-marketplace`. Commit them as they are, so every later task has a clean base and its own diff.

**Acceptance criteria:**
- [ ] The owner has confirmed the commit
- [ ] `git status` shows only the files of this plan (`SPEC-lets-a-go.md`, `docs/ideas/`, `tasks/`)

**Verification:**
- [ ] `scripts/check.sh` green; the hook is enabled (`git config core.hooksPath`)

**Dependencies:** None

**Files likely touched:** none edited; `README.md`, `TODO.md`, `install.sh`, `skills/owner-led-projects/SKILL.md`, `.claude-plugin/`, `.claude/`, `.githooks/`, `.github/`, `scripts/` committed

**Estimated scope:** XS

## Phase 1: Names

## Task 1: Rename the plugin to `kickoff` and the rules skill to `house-rules`

**Description:** `git mv skills/owner-led-projects skills/house-rules`, change the front matter name, the plugin name in `plugin.json` and `marketplace.json`, and every mention in `README.md` (table, install and remove lines, layout) and `.claude/CLAUDE.md`. Then swap the installed plugin: uninstall `owner-led-projects@niklastshiang`, update the marketplace, install `kickoff@niklastshiang`.

**Acceptance criteria:**
- [ ] `grep -r owner-led-projects` finds the old name only in history notes (`TODO.md`, spec, one-pager)
- [ ] `~/.claude/settings.json` enables `kickoff@niklastshiang` and not `owner-led-projects@niklastshiang`
- [ ] A new session lists `/kickoff:house-rules`

**Verification:**
- [ ] `scripts/check.sh` green (includes `claude plugin validate .`)
- [ ] Manual: new session in an empty folder, skill list checked

**Dependencies:** Task 0

**Files likely touched:** `skills/house-rules/SKILL.md` (moved), `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`, `README.md`, `.claude/CLAUDE.md`

**Estimated scope:** M

## Task 2: `lets-a-go`, first slice: where the project goes

**Description:** Create `skills/lets-a-go/SKILL.md` with front matter, overview, and step 1 of the spec: ask name and one-line purpose, create `YYYY-MM-DD_Name` in the current directory, ask first when the current directory is inside a git repository; in a folder with files, switch to adopt mode and list what is missing (the list itself is filled by later tasks). Add its row to the README table.

**Acceptance criteria:**
- [ ] `/kickoff:lets-a-go` appears in a new session
- [ ] Run in a scratch folder, it creates the dated folder and stops with a note that the next steps are not built yet
- [ ] Run in a folder with files, it says it is in adopt mode and changes nothing

**Verification:**
- [ ] `scripts/check.sh` green
- [ ] Manual: both runs above in scratch folders

**Dependencies:** Task 1

**Files likely touched:** `skills/lets-a-go/SKILL.md`, `README.md`

**Estimated scope:** S

## Checkpoint A: Names
- [ ] `scripts/check.sh` green
- [ ] Empty folder, new session: `/kickoff:lets-a-go` and `/kickoff:house-rules` listed, no install step
- [ ] Owner reviews

## Phase 2: The run

## Task 3: `principles.md` and its check

**Description:** Write `skills/lets-a-go/principles.md`: one row per principle (topic, rule, decided by and when), each with its *Why* where `house-rules` has one. Content: languages (files and commits English, chat in the owner's language), runtime versions (newest stable that every core dependency supports, checked on the web with sources, rechecked before each release, updated in its own commit), release numbering (1, 2, 3 …), AI disclosure (publish how it was made), hosting default (GitHub, public), quality bar as `CONSTRAINTS.md` with floor guard, hook and CI from the first commit, check tiers with time budgets, secrets rules, facts about outside projects from the web, hook enabled in every clone, texts for readers through `clarity`. Extend `check_repo.py`: the file exists and no row has an empty rule or decision.

**Acceptance criteria:**
- [ ] Every row has a rule and a "Decided" entry; licence is not a row (owner, 2026-11-17)
- [ ] The owner confirms each row (rows the owner has not decided are marked and asked)
- [ ] `check_repo.py` fails on a row with an empty rule (tested by hand once)

**Verification:**
- [ ] `scripts/check.sh` green

**Dependencies:** Task 1

**Files likely touched:** `skills/lets-a-go/principles.md`, `scripts/check_repo.py`

**Estimated scope:** S

## Task 4: `lets-a-go` asks principles and project decisions

**Description:** Steps 2 and 3 of the spec: show `principles.md` as a table, ask once "anything different this time?", record each deviation as an ADR. Then the project decisions in the spec's order, one question each, each with web research, options, a recommendation and dated sources, each recorded as an ADR from `templates/docs/adr/0000-template.md`. In adopt mode, ask only the decisions the project has no ADR or `CLAUDE.md` entry for.

**Acceptance criteria:**
- [ ] No principle is ever phrased as a question
- [ ] The ADR template has: context, options, decision, sources with dates, decided by and when
- [ ] Adopt mode lists which decisions it found and which it asks

**Verification:**
- [ ] `scripts/check.sh` green
- [ ] Manual: a run in a scratch folder up to the end of step 3; the ADRs are read by the owner

**Dependencies:** Tasks 2, 3

**Files likely touched:** `skills/lets-a-go/SKILL.md`, `skills/lets-a-go/templates/docs/adr/0000-template.md`

**Estimated scope:** S

## Task 5: Core templates, part 1: `CLAUDE.md` and `CONSTRAINTS.md`

**Description:** Generalise Stickler's `CLAUDE.md` and `CONSTRAINTS.md` into templates with `{{UPPER_SNAKE}}` placeholders: the language rule, pointers to spec, plan, ADRs and `principles.md` decisions, the check-tier commands, secrets rules; the floor, the numbered table with stack rows left as placeholders. Nothing Stickler-specific (cache digests, adapters, RunPod).

**Acceptance criteria:**
- [ ] Every Stickler line kept is one that holds for an Android app as well
- [ ] Every placeholder is named in the recipe section of `lets-a-go` (or in Task 7's list)

**Verification:**
- [ ] `scripts/check.sh` green
- [ ] Manual: read both against a Kotlin/Gradle project on paper; note any line that would not fit

**Dependencies:** Task 3

**Files likely touched:** `skills/lets-a-go/templates/CLAUDE.md`, `skills/lets-a-go/templates/CONSTRAINTS.md`

**Estimated scope:** S

## Task 6: Core templates, part 2: `check.sh`, hook, CI and the template check

**Description:** `templates/scripts/check.sh` with the tier interface `fast | task | full` and placeholders for the commands; `templates/.githooks/pre-commit` running `scripts/check.sh task`; `templates/.github/workflows/check.yml` running `scripts/check.sh full`, with actions pinned by sha. `check_repo.py` checks that every template file from the spec exists and that shellcheck covers the template shell scripts.

**Acceptance criteria:**
- [ ] `check.sh` fails clearly on an unknown tier and on unfilled placeholders
- [ ] `check_repo.py` fails when a template file is missing (tested by hand once)

**Verification:**
- [ ] `scripts/check.sh` green, shellcheck included

**Dependencies:** Task 5

**Files likely touched:** `skills/lets-a-go/templates/scripts/check.sh`, `skills/lets-a-go/templates/.githooks/pre-commit`, `skills/lets-a-go/templates/.github/workflows/check.yml`, `scripts/check_repo.py`, `scripts/check.sh`

**Estimated scope:** M

## Task 7: `lets-a-go` writes the scaffold and closes the run

**Description:** Steps 4 and 5 of the spec. The recipe: what every stack must deliver (commands behind each tier, lint/format/test configuration, the floor guard ported from `agent-skills/constraint-driven-development/references/floor-guard.md` with this language's suppression patterns, `.gitignore`, one smoke test, licence text from its official source, how the owner opens the real program, and setting up a missing toolchain, recorded in the project's `CLAUDE.md`). Then: fill the templates, README from `house-rules/README-template.md`, `git init`, hook, task tier, first commit. Final checks: no `{{`, one ADR per decision, hook ran. Adopt mode adds only missing files.

**Acceptance criteria:**
- [ ] The recipe has no stack-specific branch; Stickler is named once as a worked example
- [ ] The final checks are listed as commands the skill runs, not as advice

**Verification:**
- [ ] `scripts/check.sh` green
- [ ] Manual: owner reads the recipe

**Dependencies:** Tasks 4, 6

**Files likely touched:** `skills/lets-a-go/SKILL.md`

**Estimated scope:** M

## Task 8: `house-rules` without its own Day 1 list

**Description:** Replace the Day 1 section with a pointer: "a project without Day 1 decisions in `CLAUDE.md` or ADRs → suggest `/kickoff:lets-a-go`". Update every reference to Day 1 items (When to Use, Release, Overrides, Verification) to point at `principles.md` or the project's ADRs.

**Acceptance criteria:**
- [ ] Every one of today's ten Day 1 items appears in `principles.md` or in `lets-a-go` step 3, with its *Why*
- [ ] No "Day 1, item N" reference is left

**Verification:**
- [ ] `scripts/check.sh` green
- [ ] Manual: the item-by-item comparison above, written into the commit message

**Dependencies:** Tasks 3, 7

**Files likely touched:** `skills/house-rules/SKILL.md`

**Estimated scope:** S

## Checkpoint B: The run
- [ ] `scripts/check.sh` green
- [ ] Owner reads `principles.md` and `skills/lets-a-go/SKILL.md`

## Phase 2b: Lessons from Stickler, part 2

Spec: `SPEC-stickler-lessons-2.md` (approved by the owner, 2026-11-24). Every new rule carries its *Why* with the evidence the spec names.

## Task 13: `principles.md`

Done 2026-11-24: the row *More than one OS* (12 rows now, the check counts it); *How it was made* records per device, *Hook in every clone* is enforced (its enforcement is built in task 15); the closing note names the framework as part of the stack decision. No framework named (`grep -iE 'flutter|tauri|qt|electron|avalonia|compose|maui|react native'` finds nothing).

**Description:** Add the row *More than one OS* as the spec words it (owner, 2026-11-24). Change *How it was made* (figures per device in `docs/usage/<device>.json`, the README shows the sum) and *Hook in every clone* (enforced by `check.sh task`), each with its *Why*.

**Acceptance criteria:**
- [x] The new row names no framework
- [x] Each changed row keeps its old date and adds the new one

**Verification:**
- [x] `scripts/check.sh` green (the principles check covers the new row)

**Dependencies:** None (Q3 answered: desktop and mobile alike, owner 2026-11-24)

**Files likely touched:** `skills/lets-a-go/principles.md`

**Estimated scope:** S

## Task 14: `lets-a-go` step 3 and the recipe

**Description:** Step 3, decision 2: when decision 1 names more than one operating system, offer frameworks only, weighed by the criteria of the spec. Recipe 4.2, item 6: CI runs the full test suite on every decided system from the first commit, each job with a time limit.

**Acceptance criteria:**
- [ ] No stack-specific branch added; no framework named as a default
- [ ] The *Why* points to the principle, not repeated

**Verification:**
- [ ] `scripts/check.sh` green

**Dependencies:** Task 13

**Files likely touched:** `skills/lets-a-go/SKILL.md`

**Estimated scope:** S

## Task 15: Templates and their check

**Description:** `templates/docs/intent/0000-template.md` with the fields outcome, user, first version, afterwards, distribution, success, out of scope, confirmed by. `templates/scripts/check.sh`: the task tier stops with a message when `core.hooksPath` is not `.githooks` and `CI` is not set. `templates/CLAUDE.md`: the usage line. `templates/scripts/ai_usage.py` (owner, 2026-11-24) from Stickler's script, without its name, standard library only, prices with their source and date. `check_repo.py` requires the new files; `lets-a-go` step 4.3 and step 5 mention them.

**Acceptance criteria:**
- [ ] In a scratch git repository with the template, `check.sh task` without the hook stops with the message, with `CI=true` it does not, with the hook it runs
- [ ] `check_repo.py` fails when the intent template is missing (tested by hand once)

**Verification:**
- [ ] `scripts/check.sh` green, shellcheck included; the three runs above

**Dependencies:** Task 13

**Files likely touched:** `skills/lets-a-go/templates/docs/intent/0000-template.md`, `skills/lets-a-go/templates/scripts/check.sh`, `skills/lets-a-go/templates/CLAUDE.md`, `skills/lets-a-go/templates/scripts/ai_usage.py`, `scripts/check_repo.py`, `skills/lets-a-go/SKILL.md`

**Estimated scope:** M

**Ahead of the task (2026-11-24, for the README):** `templates/scripts/ai_usage.py` is written (Stickler's script without its name; prices checked 2026-11-24 with Sonnet and Haiku 5.5 and Haiku's long-prompt prices; `--project` and `--log` for logs from earlier paths and other folders; a recorded day shrinks no more) and copied to `scripts/ai_usage.py`; `check_repo.py` requires the template and that both files are the same. Left for this task: the intent template, the hook check, the usage line in `templates/CLAUDE.md`.

## README like Stickler's (owner, 2026-11-24)

- [x] Done 2026-11-24 (owner: "passt so"): Stickler's layout (title in `<code>`, badges by `scripts/badges.py` from shieldcn, `> SECTION` headings, details blocks, ORIGIN with the AI cost per device, SUPPORT MY WORK), the content of the old README kept (install, TokenEconomizer, graphify, cloud, removing, pins, layout, licences). Compared before with addyosmani/agent-skills, obra/superpowers and anthropics/skills (2026-11-24): install commands high, the workflow as a numbered list before the details, each skill linked to its `SKILL.md`. Title, tagline and the closing line approved by the owner.

## Task 16: `house-rules`, lessons 1–5

**Description:** Intent before spec (*Decisions Belong to the Owner*); a new system's test suite in CI first, containers for install and remove and a VM for system services, the spike on a runner and on the owner's device (*Definition of Done*); child processes fully specified (*Checks and Tests That Do Not Lie*). Extend existing rules where the spec says so instead of adding near-copies.

**Acceptance criteria:**
- [ ] Each lesson has its one-line *Why* with the evidence from the spec
- [ ] *Red Flags* and *Verification* gain a line where a lesson can be checked

**Verification:**
- [ ] `scripts/check.sh` green

**Dependencies:** Task 15 (the intent template is linked)

**Files likely touched:** `skills/house-rules/SKILL.md`

**Estimated scope:** M

## Task 17: `house-rules`, lessons 6–9 and the overview

**Description:** Subagents: the base branch in the brief, the diff read before the commit (*Orchestration*); one rule in one place with graphify before a second consumer of the core; `main` green at the start of a session and before every tag (*Release*); *README* becomes *Learning from comparable projects*. The overview says what Stickler covers now (releases 1–10 and the start of 11).

**Acceptance criteria:**
- [ ] `grep -n "six releases" skills/` finds nothing
- [ ] The overrides table still holds (the README row names the renamed section)

**Verification:**
- [ ] `scripts/check.sh` green

**Dependencies:** Task 16

**Files likely touched:** `skills/house-rules/SKILL.md`, `README.md` (the plugin table's line, if it names Stickler's state)

**Estimated scope:** S

## Task 18: Review

**Description:** A fresh-context subagent compares tasks 13–17 with the spec and checks every *Why* against Stickler (commit, task, run). Findings checked before they are fixed. Then `clarity` once over every changed text.

**Acceptance criteria:**
- [ ] Every finding fixed or answered in the done note

**Verification:**
- [ ] `scripts/check.sh` green

**Dependencies:** Task 17

**Estimated scope:** S

## Checkpoint B2: Lessons
- [ ] `scripts/check.sh` green
- [ ] Owner reads the diff of `principles.md`, `lets-a-go` and `house-rules`

## Phase 3: Proof

## Task 9: Dry run GTK/Python

**Description:** A full run of `/kickoff:lets-a-go` in a scratch folder for a small GTK/Python app, with the owner answering. Fix what goes wrong in the recipe or the templates.

**Acceptance criteria:**
- [ ] Dated folder, first commit, task tier green, hook active, CI file present, no `{{`
- [ ] Every principle shown once, none asked; every project decision has an ADR with dated sources

**Verification:**
- [ ] The criteria above, checked by commands; findings and fixes listed in the commit message

**Dependencies:** Checkpoint B

**Files likely touched:** `skills/lets-a-go/SKILL.md`, templates as needed

**Estimated scope:** M

## Task 10: Dry run Android

**Description:** The same for a small Android app. The point is the stack the templates were not built from.

**Acceptance criteria:**
- [ ] As Task 9
- [ ] Same templates and recipe as Task 9, no stack-specific branch added
- [ ] A missing toolchain is set up by the run (owner, 2026-11-17) and the task tier is green

**Verification:**
- [ ] As Task 9

**Dependencies:** Task 9

**Files likely touched:** `skills/lets-a-go/SKILL.md`, templates as needed

**Estimated scope:** M

## Task 11: Dry run adopt mode

**Description:** Run `/kickoff:lets-a-go` on a copy of `claude-obscure` in a scratch folder.

**Acceptance criteria:**
- [ ] No existing file changed (`git diff` on tracked files is empty)
- [ ] It lists what it added and which decisions it asked

**Verification:**
- [ ] `git status` and `git diff` in the copy

**Dependencies:** Task 9

**Files likely touched:** `skills/lets-a-go/SKILL.md` as needed

**Estimated scope:** S

## Task 12: README and TODO.md

**Description:** README: the plugin table with `kickoff` (`house-rules`, `lets-a-go`), the install and remove lines, the expected setup (all plugins at user scope, so a new folder needs no install step), `principles.md` in the layout. TODO.md: mark this work, keep the rename of the repository as the next item. Texts through `clarity`.

**Acceptance criteria:**
- [ ] A reader can install, start a project and remove everything from the README alone

**Verification:**
- [ ] `scripts/check.sh` green; `clarity` review once

**Dependencies:** Tasks 9–11

**Files likely touched:** `README.md`, `TODO.md`

**Estimated scope:** S

## Checkpoint C: Complete
- [ ] Every Success Criterion in `SPEC-lets-a-go.md` met
- [ ] Fresh-context review (`doubt-driven-development`) of `lets-a-go` and `principles.md`
- [ ] Owner approves; spec status set to implemented

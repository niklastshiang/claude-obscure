# /kickoff:lets-a-go

## Problem Statement

How might we start a new coding project so that the first session ends with a built scaffold and well-prepared decisions, without the owner answering the same principles again, and without installing or loading skills first?

## Recommended Direction

**A stable core as files, the stack as a recipe, the owner's principles as a principles file, and a `/kickoff:lets-a-go` skill that ties them together.**

The owner's recurring answers (languages, licence stance, release numbering, AI disclosure, hosting rules, secrets rules, "newest stable version that the core dependencies support, checked on the web on Day 1, revisited before each release") go into `principles.md` once. `/kickoff:lets-a-go` reads them and does not ask them again; it shows them and asks only "anything different this time?". The decisions that depend on the project (stack, platform, concrete versions, licences of dependencies, store or forge rules on AI-generated code) are researched first and put to the owner one at a time, each with options and a recommendation, and each lands in an ADR.

The core is what Stickler proved and what does not depend on the stack: `CLAUDE.md`, `CONSTRAINTS.md` with the floor, the three check tiers (fast/task/full) as an interface, the pre-commit hook that runs `check.sh task`, a CI skeleton, the README template that already exists, and an ADR template. These are files that `/kickoff:lets-a-go` copies and fills. The stack part is not a template: a written recipe lists what each stack must deliver (the commands behind each check tier, lint/format/test tools, packaging, platform rules, how the owner opens the real program), and Claude works through it fresh for each project, so versions are current and GTK or Android are handled the same way. Stickler serves as a worked example of the recipe, not as something to copy.

Skills need to be there before any of this runs: `owner-led-projects`, `agent-skills`, `clarity` and `tokeneconomizer` are enabled at user scope (done 2026-11-17), the old project-local duplicates are removed, and the README states this as the expected setup.

## Key Assumptions to Validate

- [ ] **The core is stack-agnostic.** Stickler's `check.sh` and `floor_guard.py` are Python-specific (ruff, pytest, `# noqa`). Test: write the core, then walk it through a Kotlin/Gradle Android project on paper; whatever needs editing is not core. The floor guard ships as the language-neutral reference from `constraint-driven-development` plus a per-stack list of suppression patterns.
- [ ] **The principles really are stable.** Test: compare Stickler's `CLAUDE.md`, ADRs and the Day 1 list with what the owner would answer for an Android app; every item that would differ moves from `principles.md` to the per-project questions.
- [ ] **The recipe catches what matters for an unknown stack.** Test: a dry run of `/kickoff:lets-a-go` for an Android app in a throwaway folder, owner reviews the questions and the scaffold; gaps become recipe lines.
- [ ] **Version research on Day 1 is reliable.** Test: the dry run must cite a source (release page, docs) for every version it picks; `source-driven-development` applies.
- [ ] **User-scope plugins are enough.** Test: an empty folder, a new session, `/kickoff:lets-a-go` and `/agent-skills:spec-driven-development` both available without any install step.
- [ ] **A plugin skill works as the slash command.** Test: the skill appears as `/kickoff:lets-a-go` after a plugin update; check the plugin docs for a shorter name.

## MVP Scope

In:
- `principles.md`: the owner's principles as rules, each with the date it was decided
- `templates/core/`: `CLAUDE.md`, `CONSTRAINTS.md`, `check.sh` interface stub, pre-commit hook, CI skeleton, ADR template (README template stays where it is)
- The stack recipe as a section of the `/kickoff:lets-a-go` skill
- The `/kickoff:lets-a-go` skill: read `principles.md`, ask "anything different?", prepare and ask the project decisions one by one, write ADRs, copy and fill the core, build the stack part from the recipe, run the checks once
- `owner-led-projects` Day 1 section shortened to point at `principles.md` and `/kickoff:lets-a-go`
- `scripts/check_repo.py` extended: template files exist, `principles.md` has no empty entries
- Cleanup: remove project-local `agent-skills@addy-agent-skills`, document the user-scope setup in the README

Out: everything under *Not Doing*.

Done when: a dry run in an empty folder ends with a committed scaffold, green `check.sh task`, ADRs for every project decision, and no question the owner has answered before.

## Not Doing (and Why)

- **A running program on Day 1 (walking skeleton)** — the owner wants decisions and a scaffold; running code comes from the spec and the first tasks.
- **Ready-made stack profiles (GTK, Android) with pinned versions** — they go stale and contradict "newest version"; the recipe plus Stickler as an example covers the same ground.
- **Use by other people** — personal defaults stay personal; no generalisation or onboarding text.
- **Tuning when skills trigger (plugin evals)** — the real problem was availability, which user scope solves; revisit only if skills are present but ignored.
- **`/retro` to feed lessons back** — useful later; the first project after this one shows whether it is needed.

## Decided (owner, 2026-11-17)

- `principles.md` lives in the public `claude-skills` repository.
- `/kickoff:lets-a-go` creates the project folder itself, with the date prefix (`YYYY-MM-DD_Name`, as in `2026-11-11_Stickler`).
- The repository rename (TODO.md) comes after this work.

## Open Questions

- Placeholders in the core files: plain substitution by a script, or Claude fills them?
- What happens to the Day 1 list in `owner-led-projects` for projects that are not started with `/kickoff:lets-a-go`?

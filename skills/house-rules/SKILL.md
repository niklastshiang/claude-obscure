---
name: house-rules
description: Working rules for a programming project that Claude builds while a human owner makes every decision. Use when starting a new project or repository, before the first line of product code, when setting up checks, conventions and docs, when unsure whether to decide something or ask the owner, when asking "is this done?", when planning to delegate work to subagents, when preparing a release, and when writing or improving a README. Builds on the agent-skills collection and states where it overrides it.
---

# House Rules

## Overview

In these projects Claude writes all the code and the owner makes all the decisions. That split works, but it has its own failure modes: conventions decided late and then changed at great cost, work declared done that breaks the first time the owner opens the real program, decisions made silently by the agent, checks weakened to get green, and documents that drift from the code.

This skill collects what one such project taught (Stickler, 2026-11: a command-line benchmark that grew into desktop apps for Linux and the Mac, in five package formats, over nine releases, and then began a Windows app): what "done" means, how to involve the owner, how to orchestrate subagents, and how to release and present the result. Rules that come from a concrete mistake or success carry a one-line *Why*, so the owner can see where they come from.

It does not repeat the general skills it builds on. Where a step is covered there, it names the skill:

| Need | Skill |
|---|---|
| Unclear ask | `interview-me` |
| Spec and module map | `spec-driven-development` |
| Tasks from a spec | `planning-and-task-breakdown` |
| Tests first | `test-driven-development` |
| Quality bar that must not be lowered | `constraint-driven-development` |
| CI | `ci-cd-and-automation` |
| ADRs, docs that drift | `documentation-and-adrs` |
| Commits, changelog, tags | `git-workflow-and-versioning` |
| Fresh-context review | `doubt-driven-development`, `code-review-and-quality` |
| Texts that read like their author | `clarity` (addyosmani/clarity) |

**Precedence.** The project's own `CLAUDE.md`, `CONSTRAINTS.md` and ADRs win over everything here. This skill overrides the agent-skills only where listed under *Overrides*; their safety and quality floors (e.g. `security-and-hardening`, `constraint-driven-development`) stay in force.

## When to Use

- A new repository or project starts (see *Day 1*: `/kickoff:lets-a-go`)
- Setting up checks, hooks, CI or project conventions
- Deciding whether a task, a module or a release is done
- A choice comes up and it is unclear whether it is the owner's
- Work could be split across subagents
- A release is being prepared
- A README is written or improved

**When NOT to use:** a one-off script or a throwaway experiment with no owner decisions and no release.

## Day 1

Every project starts with `/kickoff:lets-a-go`: it shows the owner's principles (`lets-a-go/principles.md`) without asking them again, prepares the project decisions one at a time, records each as an ADR, and builds the scaffold with its checks.

**A project without Day 1 decisions** in its `CLAUDE.md` or `docs/adr/` (an old repository, or one started without the command): suggest `/kickoff:lets-a-go` before the first line of product code. In a folder that already holds a project it runs in adopt mode, asks only what is missing and changes no existing file.
*Why: in Stickler the language, the licence and the Python version each changed mid-project, and each change cost rework.*

## Decisions Belong to the Owner

- **What is the owner's**: anything a user or reader can see or rely on (behaviour, defaults, wording, public names, file formats), scope and priorities, licence, dependencies with new licences or costs, anything that costs money or is hard to undo, and anything that leaves the repository (releases, publishing, posts). **What is Claude's**: internal names, structure and implementation details within the agreed spec, and the order of work within a task. When unsure, it is the owner's.
- **Present options with a recommendation; the owner decides.** Phrase it as a choice the owner can answer in a word, with the trade-off in one line each.
  *Why: in Stickler every product choice went this way, and none had to be reverted because the owner had not seen it coming.*
- **Record every decision where it applies**, tagged `(owner, YYYY-MM-DD)`: in the spec, in the task list, and in the commit subject when a change was the owner's wish (`… (owner)`). Lasting decisions get an ADR (`documentation-and-adrs`). Mark superseded parts as superseded, don't delete them.
  *Why: nine releases in, every "why is it like this?" was answerable from the spec and the ADRs.*
- **Intent before spec.** A large feature starts with an interview (`interview-me`). Its result goes into `docs/intent/<feature>.md` (template from `lets-a-go`: outcome, user, first version, afterwards, distribution, success, out of scope, open), and the owner confirms it before the spec is written.
  *Why: in Stickler the website and the Windows app both started this way; the Windows interview corrected the first version's scope before a line of spec was written ("the Mac app had no playback at release 8").*
- **Spec first, module by module.** Big features become a capability map of modules (`spec-driven-development`). Each module is specified, approved by the owner, built, and closed with a checkpoint, in a stated build order. When a decision changes, change the spec first.
- **Note what you find outside the task instead of fixing it silently**: a short "Found on the way" or "Noticed, not changed" line in the task's done note. The owner decides whether it becomes a task.
  *Why: a note that Ctrl+C did not reach a child process became its own task, at the owner's call.*
- **Say plainly what you cannot do** (start a review only the user can start, publish a release, create a repository, judge by ear) and hand that step to the owner with exact instructions.

## Definition of Done

Tasks follow `planning-and-task-breakdown` (acceptance, verify command, dependencies, files, size). In addition:

- A task is done when its acceptance criteria hold, its verify command passed, the task-tier check is green, and it is committed. Its done note records **measured facts**, not claims ("1375 hits, output byte-identical"), and **its checkbox is ticked in the same commit**.
  *Why: boxes not ticked at the time were still open weeks later, and nobody could tell whether the work behind them was finished.*
- How far "done" reaches depends on the feature (this overrides the upstream definition of done, which asks for runtime checks and human approval on every change):
  - **Pure logic** (parsing, calculation, data transformation): done with green tests.
  - **Anything that can behave differently in the real environment** (UI, packaging, installers, external processes, other locales or platforms, files from the wild): done only after it ran in the real program. Claude runs what it can; the rest goes to the owner at the module's checkpoint, with the exact steps to try.
    *Why: nearly every checkpoint found bugs that all tests had passed: a data file missing from the installed package, translations missing from one package format, a spinner that stuttered, a removal that also deleted shipped files, a progress bar that overshot, numbers formatted by the locale.*
- **Build and run the real, installed artefact early**, not in the last module.
  *Why: the first run of the installed package failed on a file that only existed in the development checkout.*
- **A new operating system gets the whole test suite in CI first**, before any interface code for it. The job has a time limit and prints the stack of a hanging test; a test that cannot hold there is skipped with its reason written in the test.
  *Why: the first Windows runs found three product bugs that were green on Linux and macOS (child processes waiting on an inherited stdin, a date format Windows does not know, backslashes in paths for a Linux host), and a test helper that hung on a full pipe.*
- **Containers for install and remove, a VM for system services.** A clean container per target distribution checks that a package installs, runs and leaves nothing behind. Anything that talks to system services (polkit, PackageKit, the session bus) is checked in a VM, because a container without systemd answers differently.
  *Why: Stickler's `.deb` passed its containers, then failed to uninstall in an Ubuntu VM (PackageKit refused without the interactive hint); in a container without systemd, PackageKit had returned an empty list instead.*
- **Try the risky thing first** when a failure would change the design (a sandbox, a platform limit, a dependency that may not run): a short spike before the module that depends on it. Number its questions; a driver measures and writes a log; every answer goes into the spec with its evidence (run numbers, log lines). **A spike runs twice: on a CI runner and on the owner's own device**, with exact steps for the owner and the log sent back.
  *Why: Stickler's Windows spike passed every step on the runner; on the owner's PC a policy refuses to start the unsigned launcher every environment uses.*
- **Validate on the target data**, not only on a convenient proxy.
  *Why: four tuning methods improved the public benchmark and all of them made the owner's own data worse.*

## Checks and Tests That Do Not Lie

- **Tests never touch the user's real session, files or services.** Point per-user folders at a temporary directory, and isolate or fake desktop and session services.
  *Why: a test meant to be headless unmounted a service in the owner's real desktop session.*
- **Child processes get a clean environment and nothing left implicit**: drop the parent's tool-specific variables; fix the locale of every tool whose output is parsed (e.g. `LC_ALL=C`); close `stdin` unless the child needs it; name the encoding when reading another program's output, with a replacement for bad bytes; name the line endings of a protocol. In Python, run the tests once with `PYTHONWARNDEFAULTENCODING=1 -W error::EncodingWarning`.
  *Why: inherited variables made child tools run on the wrong interpreter (22 failing tests); a non-English locale broke number parsing twice; on Windows the core's children waited on the inherited stdin, so no analysis ended, and implicit encodings sat in 53 files.*
- **Expect test environments to differ** (containers, CI, another OS). When a test fails only there, find the cause before touching the test; change the test only when the cause is the environment, and say so in the commit.
  *Why: in a cloud container killed processes stayed zombies, so five correct tests reported them as alive.*
- **Review auto-filled tool output** (translations pre-filled by merge tools, generated configs, suggested fixes) entry by entry.
  *Why: a translation merge tool pre-filled new strings with wrong guesses that looked finished.*
- **Measure progress by what the step produces**, not by a convenient proxy.
  *Why: a download bar measured by free disk space showed "78 of 78 MB" halfway through.*
- **Keep logic free of the UI toolkit**, enforced by a test; coverage then applies to the logic and the UI layer stays thin.
- **One rule in one place.** Whatever decides behaviour (which actions a state allows, what a removal deletes) lives once, in the core, with a test that every interface uses it. Before a module that adds a second consumer of the core, let a graphify graph look for copies.
  *Why: in Stickler the rule for which buttons each state enables lived in the GTK window, in the bridge for the Mac app and in the controller, until a graphify graph showed the three copies (task 125).*
- **If results are cached under a hash of the code**, let the hash ignore comments and formatting from the start, and have a tool to re-key after edits that do not change behaviour (never after a real change).
  *Why: without it, translating comments would have thrown away hours of computed results.*

## Orchestration and Subagents

Owner's rule: **the most capable model available orchestrates** (as of 2026-11: Fable or Opus). It plans, sends out subagents, evaluates their results and checks them before anything is used, **even when that takes longer**.

- Delegate what is independent: a fresh-context review of finished work, research across many files or the web, parts that split cleanly.
- Do not delegate work that needs this conversation's context or decisions.
- A subagent may run on a cheaper model for pure search or extraction, and for mechanical edits whose diff the orchestrating model reads before the commit; the orchestrating model evaluates and decides (owner, 2026-11-16).
- Brief a subagent like a peer: goal, sources, what is already known, the exact output wanted, and the branch its work starts from. Ask for evidence (file:line, commit) so the result can be checked. No secrets in briefs.
- **Check every result before using it**: spot-check its evidence, rerun its key claim. For edits, **read the diff, not the report**.
  *Why: in writing this skill, a reviewer's claims about upstream conflicts were checked against the files before any change was made; all held, but that is not something to assume. In Stickler's Windows work a subagent's report named changes that were not in the tree, and another's worktree started from `main` and missed a release's work.*
- Before every release, one fresh-context subagent compares every document with the code, and a second one reviews the code changed since the last release.
  *Why: before one release this found about twenty doc errors and real packaging bugs (wrong runtime in one environment, version/tag mismatch, unpinned CI actions).*

## Release

- **Version numbers per the principle** *Release numbering* (plain integers, +1 per release, every release counts, fixes included; Stickler, ADR 0006): the SemVer bump rules of `git-workflow-and-versioning` and its "breaking → major" check do not apply; its commit, changelog and tagging practices still do. A CI step should fail if the tag and the version in the code differ.
- **`main` is green before every tag, and checked at the start of every session** (`gh run list --branch main --limit 1`). A red `main` is the first task, before anything else.
  *Why: Stickler's `main` was red for two days (gettext missing in CI) and was found only when release 9 was tagged.*
- **Keep a written release checklist that grows with the product.** It holds the few mechanical steps (security alerts, version bump, release commit, tag, attached artefacts, metadata, docs check, regenerated README figures) and, above all, **the most important features to try by hand** before the tag. It does not need to be numbered; it needs to be current. When a release adds a feature that matters, add a line.
  *Why: the owner's hand checks at each checkpoint found what tests did not; the list makes that repeatable at every release.*
- **Generate the facts the README shows** (test count, coverage, version, AI cost) with a script and commit the output, so the README does not depend on an outside service and the numbers are refreshed as a release step.
- Publish how it was made (principle *How it was made*): who wrote the code, who decided, which guardrails held, and what the AI cost (tokens, money at API prices), refreshed every release.

## Writing

Every text a person reads goes through the `clarity` skill (owner, 2026-11-16): READMEs, docs, specs, release notes, commit messages, comments on GitHub, and the replies to the owner in chat, in whatever language the owner uses. Write it, then review it once with clarity's checks before it leaves: say what happens instead of how important it is, keep facts and attribution exactly as they are, cut formula (balanced threes, "not X but Y", bold labels before every line, recaps at the end), and stop on the last useful thought.
*Why: the owner asked for texts that do not read like AI.*

## Learning from comparable projects

**README.** This replaces the README structure in `documentation-and-adrs` for these projects. Start from `README-template.md` in this skill. Then, **before writing or improving a README, look at the READMEs of successful comparable projects** (popular, actively maintained, same kind of software and audience): what they lead with, how quickly a reader gets to "what is it, does it fit me, how do I install it", how they show the product (screenshots, a short demo), what they leave out. Adopt what works, name the projects you learned from, and propose the changes to the owner rather than restyling silently (owner, 2026-11-16).

Keep decoration modest: a few badges that state facts are enough.
*Why: the owner removed six badges again.*

**Website and features.** The same look at successful projects of the same kind before a website or a feature is specified: what they offer, how they lay it out, what users of that kind expect. Name each project with its licence, say what to take and what not, and let the owner say yes before it goes into a spec.
*Why: Stickler's download cards, its scrolling "how it works" story and its backup came from TuxTalk, its test icon for builds from blueprint, each with the owner's yes.*

## Overrides of the agent-skills

| Upstream | Here |
|---|---|
| `git-workflow-and-versioning`: SemVer | The principle *Release numbering*; SemVer bump rules only where a project's ADR chose SemVer |
| Definition of done (`planning-and-task-breakdown`): runtime check and human approval on every change | Pure logic is done with green tests; real-program checks for what meets the real environment, batched at module checkpoints |
| `documentation-and-adrs`: README structure | `README-template.md` plus *Learning from comparable projects* |

## Common Rationalizations

| Rationalization | Reality |
|---|---|
| "We can decide the licence / language / versions later" | Later means touching every file and recomputing everything that depends on them. Ask on day 1; it takes one question each. |
| "Tests are green, so it's done" | Only for pure logic. Anything that meets the real environment broke at checkpoints despite green tests. |
| "Users will never notice this default" | If users can see it or rely on it, it is the owner's. Offer two options and a recommendation. |
| "I'll fix this unrelated bug while I'm here" | Note it and ask. Unasked fixes hide in diffs and skip the owner's call. |
| "The check is flaky, I'll loosen it" | Find the cause. If it is the environment, say so in the commit; never lower the bar to get green. |
| "Delegating is faster, I'll trust the subagent's summary" | Check its evidence first. Its mistakes arrive in the same confident tone as its findings. |
| "The proxy benchmark improved, so the change is good" | Confirm on the target data before keeping it. |
| "The README looks fine to me" | Compare it with successful projects of the same kind; a reader decides in seconds. |

## Red Flags

- Product code written before language, licence, versions and the quality bar are settled
- A commit made while the task-tier check was red, or a clone without the hook enabled
- Work started while `main` is red, or a tag on a red `main`
- A subagent's edits committed on the strength of its report, without reading the diff
- A behaviour rule that exists in two interfaces
- A diff that adds a suppression, a skip or a lowered threshold "to get green"
- A UI, packaging or integration task marked done without anyone running the real program
- A user-visible choice made without offering options, or a decision with no `(owner, date)` or ADR behind it
- Unticked boxes for work that already shipped
- A subagent's result used without a single spot-check, or a secret in a subagent's brief
- Tests that read or write the real user's home, session or services
- Parsing a tool's output without fixing its locale, or a child process with an open stdin or an implicit encoding
- Interface code for a new operating system before its test suite runs there in CI
- A spike judged on the runner alone, or an uninstall through system services checked only in a container
- A spec for a large feature with no intent the owner confirmed
- A release without the hand-tried feature list, or a README number that no script produced

## Verification

- [ ] Day 1 decisions are recorded as ADRs, and deviations from `principles.md` too (`/kickoff:lets-a-go`)
- [ ] The pre-commit hook is active in this clone and CI runs the same checks
- [ ] Every user-visible choice since the last release was offered as options with a recommendation, and is recorded with its date
- [ ] Every finished task has a measured done note and a ticked box
- [ ] Every module that meets the real environment had a checkpoint in the real program
- [ ] Every operating system the project ships for runs the full test suite in CI
- [ ] Every large feature since the last release has a confirmed intent in `docs/intent/`
- [ ] Every subagent result that was used was spot-checked; every subagent edit was read as a diff
- [ ] `main` was green when the tag was set
- [ ] The release checklist lists the current key features, and they were tried
- [ ] README figures were regenerated, and the README was compared with successful projects of its kind
- [ ] Every text for readers went through `clarity` once before it left

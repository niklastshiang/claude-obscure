---
name: owner-led-projects
description: Working rules for a programming project that Claude builds while a human owner makes every decision. Use when starting a new project or repository, before the first line of product code, when setting up checks, conventions and docs, when unsure whether to decide something or ask the owner, when asking "is this done?", when planning to delegate work to subagents, when preparing a release, and when writing or improving a README. Builds on the agent-skills collection and states where it overrides it.
---

# Owner-Led Projects

## Overview

In these projects Claude writes all the code and the owner makes all the decisions. That split works, but it has its own failure modes: conventions decided late and then changed at great cost, work declared done that breaks the first time the owner opens the real program, decisions made silently by the agent, checks weakened to get green, and documents that drift from the code.

This skill collects what one such project taught (Stickler, 2026-11: a command-line benchmark that grew into a packaged desktop app over six releases): what to fix on day 1, what "done" means, how to involve the owner, how to orchestrate subagents, and how to release and present the result. Rules that come from a concrete mistake or success carry a one-line *Why*, so the owner can see where they come from.

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

**Precedence.** The project's own `CLAUDE.md`, `CONSTRAINTS.md` and ADRs win over everything here. This skill overrides the agent-skills only where listed under *Overrides*; their safety and quality floors (e.g. `security-and-hardening`, `constraint-driven-development`) stay in force.

## When to Use

- A new repository or project starts (run *Day 1* before the first line of product code)
- Setting up checks, hooks, CI or project conventions
- Deciding whether a task, a module or a release is done
- A choice comes up and it is unclear whether it is the owner's
- Work could be split across subagents
- A release is being prepared
- A README is written or improved

**When NOT to use:** a one-off script or a throwaway experiment with no owner decisions and no release.

## Day 1: Fix the Conventions Before the Code

Ask the owner in the first session, one question at a time (`interview-me`), write the answers into `CLAUDE.md` or an ADR, and do not reopen them casually. Each of the first three changed mid-project in Stickler, and each change cost rework.

1. **Language** of code, comments, docs and commit messages, and the language Claude uses with the owner (they may differ).
   *Why: Stickler switched everything to English on day 2; translating the code changed cache keys, so 445 results had to be rekeyed, and some file names stayed in the old language.*
2. **Licence** of the code, and how third-party licences (libraries, models, data, assets) relate to it.
   *Why: "MIT stays" was decided on day 3 and replaced by GPL on day 5; the licence file, package metadata, citation file, About dialog, README and contribution guide all had to change.*
3. **Runtime version range** (language version, main dependencies) for every part of the system.
   *Why: three moves of the Python version, each with lock updates, recomputed results, and a follow-up fix where one environment still took the old version.*
4. **Release numbering and release steps** (see *Release*).
5. **Where it will be hosted and shipped, and those platforms' rules on AI-generated code.**
   *Why: one forge was ruled out because it mostly disallows AI-generated programs; an app store requires the manifest and the submission to be written by a human, which the owner must then do themselves.*
6. **Whether to publish how it was made** (AI authorship, guardrails, AI cost). Stickler did; it is the owner's choice.
7. **The quality bar as a file** (`CONSTRAINTS.md`, see `constraint-driven-development`), enforced from the first commit by a pre-commit hook and CI (`ci-cd-and-automation`), plus a guard that inspects the diff for weakened checks (new suppressions, skips, stubs, lowered thresholds, secret patterns).
   *Why: the bar was raised over time (coverage 80 → 95) and never lowered; the guard and the hook kept every commit honest.*
8. **Check tiers with time budgets**, as in `constraint-driven-development`: fast after every edit (seconds), task before every commit (a minute or two, also the pre-commit hook), full in CI. Write the commands into `CLAUDE.md`.
9. **Secrets rules**: which files hold secrets; never `cat`, `source` or print them, never print raw API responses, never put a secret into a subagent's brief; check them only by metadata or a silent pattern match; scan the whole history before the repository goes public.
   *Why: a cloud GPU provider's pod response contains the pod's login password; printing it once would have put it in the transcript.*
10. **Facts about outside projects come from the web, not from memory**: maintenance status, licence, current version.
    *Why: a dependency's original repository was archived; the maintained fork was only found by checking.*

**Enable the hook in every clone** (e.g. `git config core.hooksPath <dir>`; it is per clone), and never chain a commit after a check in a way that ignores its result.
*Why: in a fresh cloud clone without the hook, a commit went through while seven tests were red.*

## Decisions Belong to the Owner

- **What is the owner's**: anything a user or reader can see or rely on (behaviour, defaults, wording, public names, file formats), scope and priorities, licence, dependencies with new licences or costs, anything that costs money or is hard to undo, and anything that leaves the repository (releases, publishing, posts). **What is Claude's**: internal names, structure and implementation details within the agreed spec, and the order of work within a task. When unsure, it is the owner's.
- **Present options with a recommendation; the owner decides.** Phrase it as a choice the owner can answer in a word, with the trade-off in one line each.
  *Why: in Stickler every product choice went this way, and none had to be reverted because the owner had not seen it coming.*
- **Record every decision where it applies**, tagged `(owner, YYYY-MM-DD)`: in the spec, in the task list, and in the commit subject when a change was the owner's wish (`… (owner)`). Lasting decisions get an ADR (`documentation-and-adrs`). Mark superseded parts as superseded, don't delete them.
  *Why: six releases later, every "why is it like this?" was answerable from the spec and the ADRs.*
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
- **Try the risky thing first** when a failure would change the design (a sandbox, a platform limit, a dependency that may not run): a short spike before the module that depends on it.
- **Validate on the target data**, not only on a convenient proxy.
  *Why: four tuning methods improved the public benchmark and all of them made the owner's own data worse.*

## Checks and Tests That Do Not Lie

- **Tests never touch the user's real session, files or services.** Point per-user folders at a temporary directory, and isolate or fake desktop and session services.
  *Why: a test meant to be headless unmounted a service in the owner's real desktop session.*
- **Child processes get a clean environment**: drop the parent's tool-specific variables, and fix the locale of every tool whose output is parsed (e.g. `LC_ALL=C`).
  *Why: inherited variables made child tools run on the wrong interpreter (22 failing tests); a non-English locale broke number parsing twice.*
- **Expect test environments to differ** (containers, CI, another OS). When a test fails only there, find the cause before touching the test; change the test only when the cause is the environment, and say so in the commit.
  *Why: in a cloud container killed processes stayed zombies, so five correct tests reported them as alive.*
- **Review auto-filled tool output** (translations pre-filled by merge tools, generated configs, suggested fixes) entry by entry.
  *Why: a translation merge tool pre-filled new strings with wrong guesses that looked finished.*
- **Measure progress by what the step produces**, not by a convenient proxy.
  *Why: a download bar measured by free disk space showed "78 of 78 MB" halfway through.*
- **Keep logic free of the UI toolkit**, enforced by a test; coverage then applies to the logic and the UI layer stays thin.
- **If results are cached under a hash of the code**, let the hash ignore comments and formatting from the start, and have a tool to re-key after edits that do not change behaviour (never after a real change).
  *Why: without it, translating comments would have thrown away hours of computed results.*

## Orchestration and Subagents

Owner's rule: **the most capable model available orchestrates** (as of 2026-11: Fable or Opus). It plans, sends out subagents, evaluates their results and checks them before anything is used, **even when that takes longer**.

- Delegate what is independent: a fresh-context review of finished work, research across many files or the web, parts that split cleanly.
- Do not delegate work that needs this conversation's context or decisions.
- A subagent may run on a cheaper model for pure search or extraction; the orchestrating model evaluates and decides (owner, 2026-11-16).
- Brief a subagent like a peer: goal, sources, what is already known, the exact output wanted. Ask for evidence (file:line, commit) so the result can be checked. No secrets in briefs.
- **Check every result before using it**: spot-check its evidence, rerun its key claim.
  *Why: in writing this skill, a reviewer's claims about upstream conflicts were checked against the files before any change was made; all held, but that is not something to assume.*
- Before every release, one fresh-context subagent compares every document with the code, and a second one reviews the code changed since the last release.
  *Why: before one release this found about twenty doc errors and real packaging bugs (wrong runtime in one environment, version/tag mismatch, unpinned CI actions).*

## Release

- **Version numbers per the Day 1 decision.** If the owner chose plain integers (+1 per release, every release counts, fixes included; Stickler, ADR 0006), the SemVer bump rules of `git-workflow-and-versioning` and its "breaking → major" check do not apply; its commit, changelog and tagging practices still do. A CI step should fail if the tag and the version in the code differ.
- **Keep a written release checklist that grows with the product.** It holds the few mechanical steps (security alerts, version bump, release commit, tag, attached artefacts, metadata, docs check, regenerated README figures) and, above all, **the most important features to try by hand** before the tag. It does not need to be numbered; it needs to be current. When a release adds a feature that matters, add a line.
  *Why: the owner's hand checks at each checkpoint found what tests did not; the list makes that repeatable at every release.*
- **Generate the facts the README shows** (test count, coverage, version, AI cost) with a script and commit the output, so the README does not depend on an outside service and the numbers are refreshed as a release step.
- If the owner chose to publish how it was made (Day 1, item 6): who wrote the code, who decided, which guardrails held, and what the AI cost (tokens, money at API prices), refreshed every release.

## README

This replaces the README structure in `documentation-and-adrs` for these projects. Start from `README-template.md` in this skill. Then, **before writing or improving a README, look at the READMEs of successful comparable projects** (popular, actively maintained, same kind of software and audience): what they lead with, how quickly a reader gets to "what is it, does it fit me, how do I install it", how they show the product (screenshots, a short demo), what they leave out. Adopt what works, name the projects you learned from, and propose the changes to the owner rather than restyling silently (owner, 2026-11-16).

Keep decoration modest: a few badges that state facts are enough.
*Why: the owner removed six badges again.*

## Overrides of the agent-skills

| Upstream | Here |
|---|---|
| `git-workflow-and-versioning`: SemVer | The Day 1 numbering decision; SemVer bump rules only if the owner chose SemVer |
| Definition of done (`planning-and-task-breakdown`): runtime check and human approval on every change | Pure logic is done with green tests; real-program checks for what meets the real environment, batched at module checkpoints |
| `documentation-and-adrs`: README structure | `README-template.md` plus comparison with successful projects |

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
- A diff that adds a suppression, a skip or a lowered threshold "to get green"
- A UI, packaging or integration task marked done without anyone running the real program
- A user-visible choice made without offering options, or a decision with no `(owner, date)` or ADR behind it
- Unticked boxes for work that already shipped
- A subagent's result used without a single spot-check, or a secret in a subagent's brief
- Tests that read or write the real user's home, session or services
- Parsing a tool's output without fixing its locale
- A release without the hand-tried feature list, or a README number that no script produced

## Verification

- [ ] Day 1 decisions are recorded (language, licence, versions, release scheme, hosting rules, publishing how it was made, quality bar, check tiers, secrets)
- [ ] The pre-commit hook is active in this clone and CI runs the same checks
- [ ] Every user-visible choice since the last release was offered as options with a recommendation, and is recorded with its date
- [ ] Every finished task has a measured done note and a ticked box
- [ ] Every module that meets the real environment had a checkpoint in the real program
- [ ] Every subagent result that was used was spot-checked
- [ ] The release checklist lists the current key features, and they were tried
- [ ] README figures were regenerated, and the README was compared with successful projects of its kind

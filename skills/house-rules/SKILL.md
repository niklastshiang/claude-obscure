---
name: house-rules
description: Working rules for a programming project that Claude builds while a human owner makes every decision. Use when starting a new project or repository, before the first line of product code, when setting up checks, conventions and docs, when unsure whether to decide something or ask the owner, when asking "is this done?", when planning to delegate work to subagents, when preparing a release, and when writing or improving a README. Builds on the agent-skills collection and states where it overrides it.
---

# House Rules

## Overview

In these projects Claude writes all the code and the owner makes all the decisions. That split works, but it has its own failure modes: conventions decided late and then changed at great cost, work declared done that breaks the first time the owner opens the real program, decisions made silently by the agent, checks weakened to get green, and documents that drift from the code.

This skill collects what one such project taught (Stickler, 2026-11: a command-line benchmark that grew into desktop apps for Linux and the Mac, in five package formats, over nine releases, and then built a Windows app; since 2026-11-26 also what two comparable projects on one framework each show, Readest and Mornye): what "done" means, how to involve the owner, how to orchestrate subagents, and how to release and present the result. Rules that come from a concrete mistake or success carry a one-line *Why*, so the owner can see where they come from.

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
- A session starts in a project that more than one computer or branch works on
- A release is near and the lessons since the last one are due

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
  *Why: in Stickler the website and the Windows app both started this way; writing the Windows intent down caught a wrong assumption about the first version's scope (the Mac app had no playback at release 8), and the owner confirmed the corrected file.*
- **With an interface: screens before the spec.** The screens of a module are drawn, checked against the platform's own guidelines and approved by the owner before the module's spec is written. The approved drawings are kept in the repository.
  *Why: every interface module of Stickler since 2026-11-14 went this way; the checks against the guidelines settled menu names and keys before any code.*
- **Spec first, module by module.** Big features become a capability map of modules (`spec-driven-development`). Each module is specified, approved by the owner, built, and closed with a checkpoint, in a stated build order. When a decision changes, change the spec first.
- **Note what you find outside the task instead of fixing it silently**: a short "Found on the way" or "Noticed, not changed" line in the task's done note. The owner decides whether it becomes a task.
  *Why: a note that Ctrl+C did not reach a child process became its own task, at the owner's call.*
- **Say plainly what you cannot do** (start a review only the user can start, publish a release, create a repository, judge by ear) and hand that step to the owner with exact instructions.
- **When the owner says "go as far as you get"**, answer each open question with your own recommendation, mark it as an assumption in the spec and in the commit, and list every assumption at the next checkpoint for the owner's yes or no. Work that would be costly to undo under another answer waits.
  *Why: in Stickler's Windows work three open questions were taken this way and one waited; the commits built on them are marked "first version", so the owner could see at the checkpoint what still needed a yes.*
- **A switch that exists only for tests is the owner's.** When a step cannot be driven by a script (a system dialog, a permission prompt), the program may get a switch that answers it in tests. The owner decides it, the spec names it, and the real step goes onto the list of things to try by hand.
  *Why: a system's save dialog could not be driven by a script; the owner allowed a variable that answers it for the screenshots only, and the dialog itself is checked by hand.*

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
- **A new operating system gets the whole test suite in CI first**, before any interface code for it. The job has a time limit and prints the stack of a hanging test; a test that cannot hold there is skipped with its reason written in the test and named in the commit message (`CONSTRAINTS.md` asks for it there, and the floor guard flags every new skip).
  *Why: the first Windows runs found three product bugs that were green on Linux and macOS (child processes waiting on an inherited stdin, a date format Windows does not know, backslashes in paths for a Linux host), and a test helper that hung on a full pipe. Readest and Mornye, read on 2026-11-26, run their full test suite on one system only, and both found platform bugs after a release (Readest's issues #6770 and #1498, Mornye's #930 and #977).*
- **CI installs and starts what users get.** On every push CI builds the artefact users will receive, installs it, starts it and names its exit code. With an interface it also takes pictures of the main screens; read them before calling the work done. This matters most where Claude cannot run the program itself.
  *Why: Stickler's installer installed and the program ended at once, because the build step had left out resource files; the start test on the runner found it. CI's pictures showed two toolbar backgrounds where the design has one, and a consent dialog where the sheet should have been. Mornye checks its shipped packages by script for the backend and the signature.*
- **Containers for install and remove, a VM for system services.** A clean container per target distribution checks that a package installs, runs and leaves nothing behind. Anything that talks to system services (polkit, PackageKit, the session bus) is checked in a VM, because a container without systemd answers differently.
  *Why: Stickler's `.deb` passed its container tests, then its uninstall failed in an Ubuntu VM: polkit refused at once, because the request lacked the interactive hint. And in a Fedora container without systemd, PackageKit listed no installed package after a reinstall; in a Fedora VM it did.*
- **Try the risky thing first** when a failure would change the design (a sandbox, a platform limit, a dependency that may not run): a short spike before the module that depends on it. Number its questions; a driver measures and writes a log; every answer goes into the spec with its evidence (run numbers, log lines). **A spike runs twice: on a CI runner and on the owner's own device**, with exact steps for the owner and the log sent back. On the owner's device it also asks what the runner lacks: does security software hold back a new program, and for how long; does the network inspect TLS; does a policy forbid unsigned programs; is the screen smaller. Each answer is written down with its time.
  *Why: Stickler's Windows spike passed every step on the runner, but on the owner's PC a policy had already refused to start uv's unsigned `python.exe`, the launcher every model environment uses; the runner has no such policy. Later a virus scanner there held each new unsigned program back, once for half an hour and the uninstaller until the next day, and the network's TLS inspection stopped two downloads until the program trusted the system's certificates. On a CI runner the small screen shortened a window in the website's pictures.*
- **With an interface: every screen in every mode.** Look at a changed screen in the longest language, at the smallest window size, and in each appearance the program has (dark, right-to-left, large text).
  *Why: a control sized for its English words ran over its neighbour in German. Readest's rules ask the same for dark, right-to-left and e-ink.*
- **Fix the class, not the sample.** When a bug is fixed, look for the same mistake in every place that does the same job, and fix them in the same task.
  *Why: Readest fixed one bug three times, for its library, its catalogue and its settings (its issues #6642, #6683 and #6389).*
- **Validate on the target data**, not only on a convenient proxy.
  *Why: four tuning methods improved the public benchmark and all of them made the owner's own data worse.*

## Checks and Tests That Do Not Lie

- **Tests never touch the user's real session, files or services.** Point per-user folders at a temporary directory, and isolate or fake desktop and session services.
  *Why: a test meant to be headless unmounted a service in the owner's real desktop session.*
- **Child processes get a clean environment and nothing left implicit**: drop the parent's tool-specific variables; fix the locale of every tool whose output is parsed (e.g. `LC_ALL=C`); close `stdin` unless the child needs it; name the encoding when reading another program's output, with a replacement for bad bytes; name the line endings of a protocol. In Python, run the tests once with `PYTHONWARNDEFAULTENCODING=1 -W error::EncodingWarning`.
  *Why: inherited variables made child tools run on the wrong interpreter (22 failing tests); a non-English locale broke number parsing twice; on Windows the core's children waited on the inherited stdin, so no analysis ended, and implicit encodings sat in 53 files.*
- **Expect test environments to differ** (containers, CI, another OS). When a test fails only there, find the cause before touching the test; change the test only when the cause is the environment, and say so in the commit.
  *Why: in a cloud container killed processes stayed zombies, so five correct tests reported them as alive.*
- **A red check says why.** A failing step prints the failing tool's own words and its exit code. No quiet flag without a step that prints the failures; with an interface, a picture at the moment of failure.
  *Why: one of Stickler's CI jobs printed only the names of failed tests, and finding the cause took more than one run.*
- **A script stops when what it needs is missing.** It names what is missing and exits with an error; it never carries on by another method without saying so. A script that every device must run is written in a language the project already needs, or it checks for its tools first.
  *Why: on a new system release a tool was missing, Stickler's test script opened the window on the real desktop without a word, and the pictures taken there were stale. Another script needed newer shell tools than the Mac has, so its work was done by hand there.*
- **A test does not compare two readings of something that lives.** Free disk space, the clock, the list of processes and the network change between two readings; test what the code decides from one reading. A test that fails while another session works on the same computer is run again alone before anything is changed.
  *Why: two readings of free disk space differed on a CI runner and failed the check twice; a process test failed while a second session's checks ran on the same PC and passed alone.*
- **Code that nothing can reach is removed.** A fallback that no input reaches counts as uncovered lines. Write the code so the branch does not exist; do not exclude it from coverage.
  *Why: three fallbacks that no date reaches took one of Stickler's coverage figures to 94.83 %, under its bar; the fix removed them.*
- **Report every check, also the ones not run.** A done note and a hand-over name each check with its result, and each check that was not run with the reason.
  *Why: Stickler's notes say so where a tool was missing ("the GTK widget tests were not run on this Mac"). Readest's acceptance rules ask for the same: "listed as not run, never left out".*
- **Review auto-filled tool output** (translations pre-filled by merge tools, generated configs, suggested fixes) entry by entry.
  *Why: a translation merge tool pre-filled new strings with wrong guesses that looked finished.*
- **Measure progress by what the step produces**, not by a convenient proxy.
  *Why: a download bar measured by free disk space showed "78 of 78 MB" halfway through.*
- **Keep logic free of the UI toolkit**, enforced by a test; coverage then applies to the logic and the UI layer stays thin.
- **One rule in one place.** Whatever decides behaviour (which actions a state allows, what a removal deletes) lives once, in the core, with a test that every interface uses it. Before a module that adds a second consumer of the core, let a graphify graph look for copies.
  *Why: in Stickler the rule for which actions each state allows lived in the GTK window and again in the bridge for the Mac app, until a graphify graph showed the two copies; merging them turned up a third in the window (task 125).*
- **One part counts.** When several parts can change the same value or the same store, one part applies the changes in order, and the others send what the user did. Where a rule must exist in two programming languages, a check keeps the copies equal.
  *Why: Stickler's Mac app computed a stepper's next value itself and lost a quick second click; the core counts now. In Mornye two connections to one database raced for the write lock, and a finished download showed as failed (its issue #948). Readest checks by script that a list kept in two languages stays the same.*
- **If results are cached under a hash of the code**, let the hash ignore comments and formatting from the start, and have a tool to re-key after edits that do not change behaviour (never after a real change).
  *Why: without it, translating comments would have thrown away hours of computed results.*

## Parallel Work

For a project that more than one computer or branch works on at a time.

- **Fetch before writing.** A session starts with `git fetch` and a look at how far the checkout is behind its remote branch and `main`, next to the check that `main` is green (*Release*). Write specs, plans and task lists only on a current checkout.
  *Why: Stickler's draft for release 11 was written on a stale checkout and replaced the same morning.*
- **Task numbers belong to their module.** Name a task by its module and a number within it (`<module>-3`), and a checkpoint by its module. Do not keep one counter for the whole project.
  *Why: two of Stickler's branches both continued the counter. At the merge tasks 161–173 became 168–180 and two checkpoints changed their letters, and the branches' commit messages still carry the old numbers.*
- **A new check goes to `main` first.** Merge a new CI job, guard or test tier on its own, before the feature work it was made for.
  *Why: Stickler's Windows job lived on the Windows branch. A test that reached `main` meanwhile compared paths as text, and no Windows runner ran it until the merge.*
- **Generated files are made again at a merge.** When both sides changed a file that a tool writes (collected texts, lockfiles, recorded figures), run the tool on the merged tree; do not merge its lines by hand.
  *Why: Stickler's merges collected the translation files anew and recorded the usage file again.*

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
- **`main` is green before every tag, and checked at the start of every session** (`gh run list --branch main --limit 1`). A red `main` is the first task.
  *Why: Stickler's `main` was red for two days (gettext missing in CI) and was found only when release 9 was tagged.*
- **Keep a written release checklist that grows with the product.** It holds the few mechanical steps (security alerts, version bump, release commit, tag, attached artefacts, metadata, docs check, regenerated README figures) and, above all, **the most important features to try by hand** before the tag. It does not need to be numbered; it needs to be current. When a release adds a feature that matters, add a line.
  *Why: the owner's hand checks at each checkpoint found what tests did not; the list makes that repeatable at every release.*
- **Generate the facts the README shows** (test count, coverage, version, AI cost) with a script and commit the output, so the README does not depend on an outside service and the numbers are refreshed as a release step.
- Publish how it was made (principle *How it was made*): who wrote the code, who decided, which guardrails held, and what the AI cost (tokens, money at API prices), refreshed every release.

## Lessons

Every project keeps `docs/lessons.md` (template from `lets-a-go`). **Before each release, read the commits since the one the file names** and look for work that was done twice: a fix of a fix, a check that was red for a reason seen before, a correction by the owner. Write one entry per finding, with its commits, and move the file's marker to the newest commit read.

- A lesson seen a second time becomes a rule in the project's `CLAUDE.md` (owner, 2026-11-26).
- A lesson that would hold in a project of another kind is proposed to the owner for this skill.

*Why: both reviews of what Stickler had taught since the last one started with the owner asking for them, and each had to read the history from the start. Readest keeps such a file with a marker for how far it was read, and moves a lesson into its rules once it was seen on three days.*

## Writing

Every text a person reads goes through the `clarity` skill (owner, 2026-11-16): READMEs, docs, specs, release notes, commit messages, comments on GitHub, and the replies to the owner in chat, in whatever language the owner uses. Write it, then review it once with clarity's checks before it leaves: say what happens instead of how important it is, keep facts and attribution exactly as they are, cut formula (balanced threes, "not X but Y", bold labels before every line, recaps at the end), and stop on the last useful thought.
*Why: the owner asked for texts that do not read like AI.*

## Learning from comparable projects

**README.** This replaces the README structure in `documentation-and-adrs` for these projects. Start from `README-template.md` in this skill. Then, **before writing or improving a README, look at the READMEs of successful comparable projects** (popular, actively maintained, same kind of software and audience): what they lead with, how quickly a reader gets to "what is it, does it fit me, how do I install it", how they show the product (screenshots, a short demo), what they leave out. Adopt what works, name the projects you learned from, and propose the changes to the owner rather than restyling silently (owner, 2026-11-16).

Keep decoration modest: a few badges that state facts are enough.
*Why: the owner removed six badges again.*

**Website and features.** Before a website or a feature is specified, look the same way at successful projects of the same kind: what they offer, how they lay it out, what users of that kind expect. Name each project with its licence, say what to take and what not, and let the owner say yes before it goes into a spec.
*Why: Stickler's download cards, its scrolling "how it works" story and its backup came from TuxTalk, each with the owner's yes; the idea of a test icon for builds came from blueprint and waits as an idea for later.*

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
| "I pulled this morning, the checkout is fine" | Another computer may have pushed since. Fetch, then write. |
| "The fallback is only defensive" | If nothing reaches it, it is uncovered code. Remove the branch. |
| "The script found another way, so it worked" | A script that goes on without what it needs produces stale or wrong output that looks finished. It stops and says what is missing. |

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
- A spec, plan or task list written before `git fetch`, or two branches counting tasks on one counter
- A new CI job that exists only on a feature branch
- A failed CI step whose log shows no reason, or a script that went on without a tool it needs
- An artefact that CI builds but never installs and starts
- A screen checked in one language and one size only
- A report that names the green checks and leaves out the ones not run
- A release with no pass over `docs/lessons.md`
- A release without the hand-tried feature list, or a README number that no script produced

## Verification

- [ ] Day 1 decisions are recorded as ADRs, and deviations from `principles.md` too (`/kickoff:lets-a-go`)
- [ ] The pre-commit hook is active in this clone and CI runs the same checks
- [ ] Every user-visible choice since the last release was offered as options with a recommendation, and is recorded with its date
- [ ] Every finished task has a measured done note and a ticked box
- [ ] Every module that meets the real environment had a checkpoint in the real program
- [ ] Every operating system the project ships for runs the full test suite in CI
- [ ] Every large feature since the last release has a confirmed intent in `docs/intent/`
- [ ] The session started with `git fetch`, and tasks are named by their module
- [ ] CI installed and started what users get, and its pictures were read
- [ ] Every check is reported, with the ones not run and why
- [ ] `docs/lessons.md` is read through to the release commit, and every lesson seen twice is a rule
- [ ] Every subagent result that was used was spot-checked; every subagent edit was read as a diff
- [ ] `main` was green when the tag was set
- [ ] The release checklist lists the current key features, and they were tried
- [ ] README figures were regenerated, and the README was compared with successful projects of its kind
- [ ] Every text for readers went through `clarity` once before it left

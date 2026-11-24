# Spec: Lessons from Stickler, part 2

Status: approved by the owner (2026-11-24). The app for dry run 2 is still open; it does not block Phase 2b. Plan and tasks: `tasks/plan.md`, Phase 2b.

## Objective

`house-rules` and `lets-a-go` were written from Stickler up to release 7 (2026-11-16/17). Since then Stickler gained a Mac app (release 8), a website, `.deb` and `.rpm` packages (release 9), backup and uninstall (release 10), and the first two modules of a Windows app (release 11, 2026-11-24). This change brings what those releases taught into the skills, and adds one new principle from the owner:

**A program for more than one operating system is built on one cross-platform framework** (owner, 2026-11-24). It applies to future projects; Stickler's Windows app stays as planned.

The change happens before the dry runs of Phase 3, so the dry runs test the skills as they will be used.

User: the owner, for the next project.

## The changes

Each lesson has its evidence in Stickler (commit, task or run), read on 2026-11-24 from `main` and `origin/claude/win-core`.

### New principle: one framework for more than one operating system

Row in `principles.md`:

> **More than one OS.** When a program has a user interface on more than one operating system, that interface is written once, in one cross-platform framework. No native app per system. Which framework is a project decision (`lets-a-go` step 3.2), researched on the day. Packages stay per system. Native code only where the framework cannot reach, through the framework's own way of calling it, never as a second app.
> *Why: Stickler built one native app per system (GTK and Python, then SwiftUI, then WinUI 3). The Mac app alone took about 40 tasks in six modules (tasks 92–137); release 10's backup and uninstall were built once per app (tasks 153/154, 156/157); a rule for what each state allows lived in three copies until a graphify graph showed it (task 125).*
> Decided: owner, 2026-11-24.

In `lets-a-go`, step 3:

- Decision 1 (where it runs) comes first as today. If it names more than one operating system, decision 2 offers frameworks only, and the recommendation weighs: official support for every decided system, active maintenance, logic that tests without a screen, packaging for each system's channel, accessibility, licence.
- The recipe (4.2, item 6): CI runs the full test suite on every decided system from the first commit, not only on the system Claude works on.

### Lessons for `house-rules`

1. **Intent before spec** (*Decisions Belong to the Owner*). A large feature starts with an interview (`interview-me`). Its result goes into `docs/intent/<feature>.md` with fixed fields (outcome, user, first version, afterwards, distribution, success, out of scope), and the owner confirms it before the spec is written. New template `templates/docs/intent/0000-template.md`.
   *Evidence: `docs/intent/website.md` (2026-11-18) and `docs/intent/windows-app.md` (2026-11-24); the interview corrected the Windows app's scope ("the Mac app had no playback at release 8").*
2. **A new system gets the whole test suite in CI first** (*Definition of Done*), before any interface code for it. The job has a time limit and prints the stack of a hanging test. A test that cannot hold there is skipped with its reason in the test.
   *Evidence: task 167. The first Windows runs found three product bugs that were green on Linux and macOS: child processes inherited the bridge's stdin and no analysis ended, `%-d` in a date format, backslashes in paths for a Linux host. The test helper hung because it read only one pipe.*
3. **Child processes, fully specified** (*Checks and Tests That Do Not Lie*, extends the rule on clean environments): `stdin` closed unless the child needs it, the encoding named when reading another program's output (with a replacement for bad bytes), line endings named for protocols, and in Python a test run with `PYTHONWARNDEFAULTENCODING=1 -W error::EncodingWarning`.
   *Evidence: task 167 (stdin), task 161 (53 files, three tests red before), task 166 (`\n` on every system).*
4. **Containers for install and remove, a VM for system services** (*Definition of Done*). A clean container per target distribution checks that the package installs, runs, and leaves nothing behind. Anything that talks to system services (polkit, PackageKit, the session bus) is checked in a VM, because a container without systemd gives a different answer.
   *Evidence: task 141 (three containers, green); task 160: the `.deb` uninstall failed without a prompt in an Ubuntu VM (missing `SetHints interactive=true`); in a Fedora container without systemd PackageKit listed no installed package after a reinstall, in a Fedora VM it did. (Corrected 2026-11-24 after the review of task 18: the first wording put both on the `.deb`.)*
5. **A spike runs twice: on a CI runner and on the owner's device** (extends *Try the risky thing first*). Its questions are numbered, a driver measures and writes a log the owner sends back, and every answer goes into the spec with run numbers.
   *Evidence: `win-spike` (tasks 169–172): the runner passed every step; on the owner's PC a policy refuses to start uv's unsigned `python.exe` ("Zugriff verweigert").*
6. **Subagents: check the diff, not the report** (*Orchestration*). The brief names the branch the work starts from. A subagent on a cheaper model may make mechanical edits; the orchestrating model reads its diff before the commit.
   *Evidence: tasks 161, 165, 166, 167 (Sonnet subagents, diffs read). One report named changes to `tests/test_site.py` that were not in the tree; one worktree started from `main` and missed release 10's work.*
7. **One rule in one place** (extends *Keep logic free of the UI toolkit*). Whatever decides behaviour lives once, in the core, with a test that every interface uses it. Before a module that adds a second consumer of the core, a graphify graph looks for copies.
   *Evidence: task 125.*
8. **`main` green before every tag, checked at the start of a session** (*Release*). `gh run list --branch main --limit 1` before work starts; a red `main` is the first task.
   *Evidence: `check` was red on `main` from 2026-11-20 to 2026-11-22 (gettext missing in CI) and was found only when release 9 was tagged.*
9. **Comparable projects for more than the README** (*README*, renamed *Learning from comparable projects*): the same look at successful projects of the same kind for a website and for features, each with its licence and the owner's yes.
   *Evidence: TuxTalk (download cards, the scrolling story, backup) and blueprint (a test icon), `tasks/todo.md` 2026-11-22.*

### Principles that change

- **How it was made:** the AI figures are recorded per device. Every computer that works on the project writes its tokens and active time into `docs/usage/<device>.json` at the end of a session that commits and before a release; the README shows the sum. *Why: Stickler is built on a Linux computer, a Mac, a Windows PC and in the cloud; one machine's logs counted 347 of about 447 USD at release 8.*
- **Hook in every clone:** enforced, not only written down. `scripts/check.sh task` stops with a message when `core.hooksPath` is not `.githooks` (outside CI). *Why: commit of 2026-11-19, "the pre-commit hook was not switched on in this checkout", after the rule was already in place.*

### Templates in `lets-a-go`

- `templates/docs/intent/0000-template.md` (new)
- `templates/scripts/check.sh`: the hook check
- `templates/scripts/ai_usage.py` (new; owner, 2026-11-24): Stickler's script without its project name, standard library only
- `templates/CLAUDE.md`: the usage line

## Boundaries

- **Always:** every new rule carries its *Why* with evidence from Stickler; every text goes through `clarity`; `scripts/check.sh` green before each commit.
- **Ask first:** any rule the owner has not seen in this spec.
- **Never:** change Stickler from here; name a framework in `principles.md` (that is a project decision, researched on the day).

## Success Criteria

- [ ] `principles.md` has the row *More than one OS*, and *How it was made* and *Hook in every clone* are changed as above
- [ ] `lets-a-go` step 3 offers only frameworks when more than one system is decided, and the recipe puts every decided system into CI
- [ ] `house-rules` holds lessons 1–9, each with its evidence; nothing in it still says "six releases"
- [ ] The new templates exist, and `check_repo.py` requires them
- [ ] A template `check.sh task` in a scratch clone without the hook stops with the message; with the hook it runs
- [ ] `scripts/check.sh` green

## Out of Scope

- A website module in the recipe (domain, legal notice, accessibility check in CI): after the dry runs show how the recipe holds up
- Feature parity across systems as a decision of its own: with one framework it follows from the build
- Changes to Stickler

## Decided (owner, 2026-11-24)

- **The usage script** is copied into every project as `templates/scripts/ai_usage.py`, not run from the plugin. It then works in cloud sessions and on every device without the plugin; it needs Python 3.
- **The new principle** covers desktop and mobile alike: any program with an interface on more than one operating system, e.g. Linux and Android.

## Open

- **Dry run 2 of Phase 3** (Task 10): the owner chooses the app. The proposal was a desktop app for Linux, macOS and Windows instead of the Android app, as it tests the new principle. Does not block Phase 2b.

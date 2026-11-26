# Spec: Lessons, part 3

Status: approved by the owner (2026-11-26, the three open questions as proposed) and built the same day. Plan and tasks: `tasks/plan.md`, Phase 2c.

## Objective

`house-rules` and `lets-a-go` hold what Stickler taught up to 2026-11-24 (`SPEC-stickler-lessons-2.md`). Since then Stickler gained the Mac playback and corrections, four Windows modules and the Mac pictures on its website, in about 110 commits on three computers and several branches. The owner also asked for a look at two projects that are built on one cross-platform framework each: Readest (Tauri) and Mornye (Flutter).

This change brings in the lessons that hold for any project (owner, 2026-11-26: "only rules that carry over to every project"). A rule is in when it names no language, framework, operating system or tool, and when a project of another kind could break it. A rule that needs a user interface or a second device says so in its first words and is skipped where that does not apply.

User: the owner, for the next project.

## Sources

- **Stickler:** commits from 2026-11-24 13:38 to 2026-11-26 15:12 on `main` and the `claude/*` branches, read on 2026-11-26. Evidence is a commit.
- **Readest:** github.com/readest/readest (AGPL-3.0), read on 2026-11-26 from a clone 200 commits deep. Evidence is a file or an issue.
- **Mornye:** github.com/mornyeapp/Mornye (LGPL-3.0), read the same way on the same day.

Two subagents read the outside projects; their key claims were checked in the clones, and two were corrected before use. Only practices are taken from the two projects, no text and no code.

## The changes

### New section in `house-rules`: Parallel work

For a project that is worked on from more than one computer or branch at a time.

1. **Fetch before writing.** A session starts with `git fetch` and a look at how far the checkout is behind its remote branch and `main`, next to the check that `main` is green. Specs, plans and task lists are written only on a current checkout.
   *Evidence: Stickler's draft for release 11 was written on a stale checkout and replaced the same morning (75f8bf2, bb0f21e).*
2. **Task numbers belong to their module.** A task is named by its module and a number within it (`<module>-3`), and a checkpoint by its module. One counter for the whole project is not used.
   *Evidence: two branches both continued the counter. At the merge tasks 161–173 became 168–180 and checkpoints AC/AD became AD/AE, and the branches' commit messages still carry the old numbers (bb0f21e, 61e0906).*
3. **A new check goes to `main` first.** A CI job, a guard or a test tier that is new is merged on its own, before the feature work it was made for.
   *Evidence: Stickler's Windows job lived on the Windows branch. A test that reached `main` meanwhile compared paths as text, and no Windows runner ran it until the merge (9ea7f95).*
4. **Generated files are made again at a merge.** When both sides changed a file that a tool writes (collected texts, lockfiles, recorded figures), run the tool on the merged tree. Do not merge its lines by hand.
   *Evidence: Stickler's merges of 2026-11-26 collected the translation files anew and recorded the usage file again (89ab4ab, f79aeee).*

### `house-rules`, *Decisions Belong to the Owner*

5. **When the owner says "go as far as you get".** Claude answers each open question with its own recommendation, marks it as an assumption in the spec and in the commit, and lists every assumption at the next checkpoint for the owner's yes or no. Work that would be costly to undo under another answer waits.
   *Evidence: Stickler, e537161 ("Claude's proposals for open questions 2–4 taken as the owner's reading; question 1 waits"); the commits built on them are marked "first version".*
6. **A switch that exists only for tests is the owner's.** When a step cannot be driven by a script (a system dialog, a permission prompt), the program may get a switch that answers it in tests. The owner decides it, the spec names it, and the real step goes onto the list of things to try by hand.
   *Evidence: Windows' save dialog could not be driven by a script; the owner allowed a variable that answers it for the screenshots only (b21e6b6).*
7. **With an interface: screens before the spec.** The screens of a module are drawn, checked against the platform's own guidelines and approved by the owner before the module's spec is written. The approved drawings are kept in the repository.
   *Evidence: every Stickler interface module since 2026-11-14 went this way (cb8d528, 72cc901, 61e0906); the checks against the guidelines settled menu names and keys before any code.*

### `house-rules`, *Definition of Done*

8. **CI installs and starts what users get.** On every push CI builds the artefact users will receive, installs it, starts it and names its exit code. With an interface it also takes pictures of the main screens, and Claude reads them before calling the work done. This holds most where Claude cannot run the program itself.
   *Evidence: Stickler's installer installed and the program ended at once, because the build step left out resource files; the start test on the runner found it (a5adba5). CI pictures showed two toolbar backgrounds where the design has one (849d7bf) and a consent dialog where the sheet should be (07377b1). Mornye checks its shipped packages by script for the backend and the signature (`scripts/check_backend_apk.py`, `check_windows_bundle.ps1`).*
9. **The spike's list of what the runner lacks.** Extends *A spike runs twice*. On the owner's device the spike also asks: does security software hold back a new program, and for how long; does the network inspect TLS; does a policy forbid unsigned programs; is the screen smaller than the runner's. Each answer is written down with its time.
   *Evidence: on the owner's company PC a virus scanner held each new unsigned program back, once for half an hour and the uninstaller until the next day (2335a5d, 44ef242, f79aeee); the network's TLS inspection stopped two downloads until the program trusted the system's certificates (a84da1f, 687b61b). On the macOS runner the small screen shortened a window (2578dc5).*
10. **With an interface: every screen in every mode.** A change to a screen is looked at in the longest language, at the smallest window size, and in each appearance the program has (dark, right-to-left, large text).
    *Evidence: a control sized for the English words ran over its neighbour in German (d9e7b8b, 1903274). Readest's acceptance rules ask the same for dark, right-to-left and e-ink (`.claude/rules/acceptance.md`).*
11. **Fix the class, not the sample.** When a bug is fixed, look for the same mistake in every place that does the same job, and fix them in the same task.
    *Evidence: Readest fixed one bug three times, for its library, its catalogue and its settings (#6642, #6683, #6389, from its `LESSONS.md`).*

### `house-rules`, *Checks and Tests That Do Not Lie*

12. **A red check says why.** A failing step prints the failing tool's own words and its exit code. No quiet flag without a step that prints the failures; with an interface, a picture at the moment of failure.
    *Evidence: Stickler's Mac job printed only the names of failed tests, and finding the cause took more than one run (af98629, 0c486dd); the Windows jobs then got a picture on any failure and the program's exit code (779c24b, a5adba5).*
13. **A script stops when what it needs is missing.** It names what is missing and exits with an error. It does not go on in another way without saying so. Scripts that every device must run are written in a language the project already needs, or they check for their tools first.
    *Evidence: a tool was missing on a new system release, Stickler's test script opened the window on the real desktop without a word, and the pictures taken there were stale (7eaac80). A script that needed newer shell tools could not run on the Mac, so its work was done by hand (b27e4af).*
14. **A test does not compare two readings of something that lives.** Free disk space, the clock, the list of processes and the network change between two readings. Test what the code decides from one reading. A test that fails while another session works on the same computer is run again alone before anything is changed.
    *Evidence: two readings of free disk space differed on the runner and failed the check twice (598c73f); a process test failed while a second session's checks ran on the same PC and passed alone (779c24b).*
15. **Code that nothing can reach is removed.** A fallback that no input reaches counts as uncovered lines. Write the code so the branch does not exist; do not exclude it from coverage.
    *Evidence: three fallbacks that no date reaches took Stickler's Swift coverage to 94.83 %, under its bar; the fix removed them (188da00).*
16. **Report every check, also the ones not run.** A done note and a hand-over name each check with its result, and each check that was not run with the reason.
    *Evidence: Stickler's notes already do this where a tool was missing ("the GTK widget tests were not run on this Mac", fa6121f). Readest's acceptance rules ask for the same (`.claude/rules/acceptance.md`: "listed as not run, never left out").*
17. **One part counts.** Extends *One rule in one place*. When several parts can change the same value or the same store, one part applies the changes in order, and the others send what the user did. Where a rule must exist in two programming languages, a check keeps the copies equal.
    *Evidence: Stickler's Mac app computed a stepper's next value itself and lost a quick second click; the core counts now (9ebdd2e). In Mornye two connections to one database raced for the write lock, and a finished download showed as failed (#948, fixed in 9a506b8). Readest checks by script that a list in two languages stays the same (`scripts/check-eink-identity-sync.mjs`).*

### New section in `house-rules`: Lessons

18. **Every project keeps `docs/lessons.md`, and reads its own history before each release.** The pass looks at the commits since the last release for work that had to be done twice: a fix of a fix, a check that was red for a reason seen before, a correction by the owner. Each finding is one entry with its commits. A lesson seen a second time becomes a rule in the project's `CLAUDE.md`. A lesson that names nothing of the project is proposed to the owner for `house-rules`.
    *Evidence: both lessons passes for this repository started with the owner asking what Stickler had taught (2026-11-24, 2026-11-26), and each had to read the history from the start. Readest keeps a `LESSONS.md` with a marker for how far it was read, and moves a lesson into its rules once it was seen on three days.*

### `lets-a-go`

19. **Step 3, decision 1 (how users get it): signing and updates.** For each channel the decision names who signs the artefact, what the system shows for an unsigned one, and how an update reaches users. The first release tests an update from start to end.
    *Evidence: Stickler learned in its Windows spike what a managed PC does with an unsigned program (ba6f01c). Mornye's Mac build is not notarized and Windows blocks its installer (#919). Readest's release stops before it would overwrite its update index with a file it could not read (`release.yml`). (Corrected after the review of lessons-3-5: issue #78, named here at first, does not show a shipped update with an invalid signature.)*
20. **Step 3, decision 2 (stack), with more than one system: one more thing to weigh.** Whether the framework draws the interface itself or uses each system's own engine, and for the second kind, which version of that engine the oldest supported system has.
    *Evidence: in Readest bugs from the differences between the systems' web engines keep coming back (issue #1498, fixes #7804 and #7794), and it ships one system with a bundled engine on a runtime branch of its own. (Corrected after the review of lessons-3-5: nothing counted supports "the largest class", and #190 is a display error of another kind.)*
21. **Step 4.2, item 6 (CI): confirmed, no change.** Both outside projects run their full test suite on one system only and found platform bugs after release (Readest #6770, #1498; Mornye #930, #977).
22. **Step 4.2, new item: the toolchain's version in the file the toolchain reads.** The version is pinned where the tool itself looks for it, so the owner's computers and CI take the same one. Files fetched during a build are pinned by their hash.
    *Evidence: Stickler's CI was red on the runner's newer SDK until a version file pinned it (bc5c45d). Mornye's desktop builds broke when a release it downloaded was removed and a tool dropped an option (68d3176, 429a5cd).*

### Templates in `lets-a-go`

- `templates/docs/lessons.md` (new): the heading, the fields of an entry, and a line for the last commit read.
- `templates/CLAUDE.md`: the lessons line, the fetch at the start of a session, task names by module.
- `templates/scripts/ai_usage.py` and `scripts/ai_usage.py`: also read the logs of the checkout's worktrees, as Stickler's script does since dd15510. A record replaces whole days, so a record made in a worktree left out the main checkout's sessions.

## Left out, and why

- Clients that send what the user did instead of a computed value, as a rule of its own: it is part of item 17.
- Rules for pull requests from outside (Readest's gate and its trust rules): only for a public project that takes them; a project decision.
- A bot that moves pinned versions: the principle *Runtime versions* already asks for the check before every release.
- A map "how to add a setting, a screen, a native method" (Mornye): useful there, but no failure here shows the need.
- "One commit, one goal" and "a test that fails without the change": `git-workflow-and-versioning` and `test-driven-development` already ask for them.
- What Stickler learned about single tools (path conversion in one shell, a script language's code page, file names that differ only in case): each is a case of item 13.

## Boundaries

- **Always:** every new rule carries its *Why* with evidence; evidence from an outside project names the project and the day it was read; every text goes through `clarity`; `scripts/check.sh` green before each commit.
- **Ask first:** any rule the owner has not seen in this spec.
- **Never:** change Stickler from here; name a framework, a language or a tool in a rule (the owner's choice of Flutter below is the one exception, in `principles.md`); copy text or code from Readest or Mornye.

## Success Criteria

- [ ] `house-rules` has the sections *Parallel work* and *Lessons* and holds items 1–18, each with its evidence
- [ ] No new rule names a language, a framework or an operating system outside its *Why*, and no tool beyond git and the hosting the principles set
- [ ] `lets-a-go` holds items 19, 20 and 22; item 21 adds the two outside projects to the existing *Why*
- [ ] `templates/docs/lessons.md` exists, `check_repo.py` requires it, and the `CLAUDE.md` template has the three new lines
- [ ] Both copies of `ai_usage.py` read the worktrees' logs, shown by a record made in a scratch worktree
- [ ] *Red Flags* and *Verification* in `house-rules` have a line for each new section
- [ ] `scripts/check.sh` green

## Out of Scope

- Changes to Stickler, including its task numbers
- A skill that runs the lessons pass by itself: the rule comes first, and a skill follows if the pass proves its worth over two releases
- The dry runs of Phase 3

## Decided (owner, 2026-11-26)

1. **When a lesson becomes a rule** (item 18): at its second occurrence, checked before every release. Readest waits for the third day and looks daily; with releases every few days, the second occurrence at a release is about as strict and costs one pass per release.
2. **Task names** (item 2): `<module>-<n>`, checkpoints named after their module. The other way, one counter with a block of numbers per branch, needs someone to hand out the blocks.
3. **Rules that need an interface** (items 7 and 10, the pictures in 8 and 12) and item 20, which needs more than one system: they stay, each marked with its condition.
4. **Flutter for more than two target systems** (owner, 2026-11-26, after this spec was built). The principle *More than one OS* names it, and `lets-a-go` step 3 no longer offers frameworks in that case; for exactly two systems the framework stays a project decision. It replaces the line of `SPEC-stickler-lessons-2.md` that no framework is named in `principles.md`. The owner's comparison of 2026-11-20 recommended Flutter and proposed a prototype first; the owner decided without it, so what the prototype was to measure (package size, memory, start time, bindings for models on the device) is checked in the first project.

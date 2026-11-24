---
name: lets-a-go
description: Starts a new coding project for the owner, or brings an existing one up to the same footing. Shows the owner's principles without asking them again, prepares each project decision with research and a recommendation, records every decision as an ADR, and builds the scaffold (CLAUDE.md, CONSTRAINTS.md, check tiers, hook, CI, README). Use when the owner starts a new project or repository, says "new project" or "let's start", or when a project has no Day 1 decisions in its CLAUDE.md or ADRs.
---

# Let's-a-go

## Overview

One session with this skill turns an empty folder into a project whose Day 1 decisions are made and written down, with a scaffold that enforces the quality bar from the first commit. Nothing has to run yet; the product itself starts afterwards with `spec-driven-development`.

The owner decides; Claude prepares. The owner's recurring answers live in `principles.md` at the root of this plugin's repository and are never asked again. Everything that depends on the project is put to the owner one question at a time, each with research, options and a recommendation.

The working rules for the rest of the project are in `house-rules`. This skill covers only the start.

## Step 1: Where

Decide which mode applies before anything else.

**New project.** The current directory is not a project of its own (no `.git`, no source files, or the owner says it is a new project):

1. Ask for the project's name and a one-line purpose, in one question.
2. If the current directory is inside a git repository (`git rev-parse --show-toplevel` succeeds), ask before creating anything: a project folder inside another repository is rarely what the owner wants.
3. Create `YYYY-MM-DD_Name` in the current directory, with today's date and the name as the owner wrote it (e.g. `2026-11-11_Stickler`). Work inside it from now on.

**Adopt mode.** The current directory already holds a project (a `.git` folder, source files, or a `CLAUDE.md`):

1. Say that this is adopt mode and that no existing file will be changed.
2. List which Day 1 decisions are already recorded (in `CLAUDE.md` or `docs/adr/`) and which scaffold files exist.
3. Continue with the steps below, asking only what is missing and adding only files that do not exist.

## Step 2: Principles

Read `principles.md` in this skill's folder. Show it to the owner as one table (topic and rule, without the *Why* lines), then ask exactly one question: **anything different for this project?**

- Never turn a principle into a question of its own. The table is information; the one question is the only place to deviate.
- A deviation applies to this project only. Record it as an ADR (template below) with the owner's reason. Change `principles.md` only if the owner says the principle itself has changed, and then in the `kickoff` repository, not in the project.
- A row marked **open** is asked in step 3 like a project decision; propose the owner's answer as a new principle afterwards.
- Adopt mode: compare the principles with what the project's `CLAUDE.md` and ADRs already say, and show only the differences. Ask whether each difference is intended (it becomes an ADR) or should be brought in line.

## Step 3: Project decisions

Put these to the owner **one at a time**, in this order, because later ones depend on earlier ones. Prepare each before asking:

1. Research it on the web today: official docs, release pages, licence texts, platform policies. Never from memory (principle *Facts from the web*).
2. Give two to four options, what each means for this project, and **one recommendation** with its reason.
3. Cite the sources, with today's date.
4. After the answer, write the ADR before asking the next question.

The decisions:

1. **What it is and where it runs:** platforms, how users get it (store, package format, download).
2. **Stack:** language, UI toolkit, build tool. Prefer what is actively maintained and fits the platforms from 1.
   If decision 1 names more than one operating system and the program has a user interface, offer cross-platform frameworks only (principle *More than one OS*); a native app per system is a deviation and needs an ADR. Weigh each framework by: official support for every system from 1, active maintenance, logic that can be tested without a screen, packaging for each system's channel from 1, accessibility, and its licence.
3. **Versions:** for each component, the newest stable release that every core dependency supports (principle *Runtime versions*). Name the release date and where support was confirmed.
4. **Licence** of the project, checked against the licences of the core dependencies and any assets, data or models it ships.
   *Why: in Stickler, "MIT stays" was decided on day 3 and replaced by GPL on day 5; the licence file, package metadata, citation file, About dialog, README and contribution guide all had to change.*
5. **Repository and stores:** public or private on GitHub; whether GitHub and each store from 1 accept AI-generated code, and who must submit what.
   *Why: for Stickler one forge was ruled out because it mostly disallows AI-generated programs, and an app store requires the manifest and the submission to be written by a human, which the owner must then do themselves.*
6. Anything the stack recipe (step 4) marks as a decision for this stack.

Adopt mode: skip every decision the project already records in `CLAUDE.md` or `docs/adr/`, and say which ones were found.

### ADRs

Each decision and each deviation from the principles gets one file in `docs/adr/`, numbered from `0001`, from `templates/docs/adr/0000-template.md` in this skill's folder. Fill every section: the options as they were put to the owner, the decision in the owner's words, the consequences for the code, and every source with the date it was read. Use the project's file language (principle *Languages*).

## Step 4: Scaffold

### 4.1 Toolchain first

Set up what the stack needs to build and test (language runtime, SDKs, build tool) at the versions from step 3, before writing files that depend on it. On an immutable host (Fedora Atomic and similar) use a toolbox or distrobox container or the stack's own version manager; never layer packages onto the host without asking. Write down exactly how it was set up, and how to enter it, in the project's `CLAUDE.md` (*Toolchain*), so the next session can repeat it.

### 4.2 The stack recipe

The stack part is not a template: versions and tools change too fast. Work through this list for the decided stack, fresh, with sources from today. Every item is needed for every stack; none is skipped because a stack "does not need it" without telling the owner why. Stickler (Python, GTK, uv, ruff, pytest, Flatpak) is one worked example of a filled recipe.

1. **Skeleton** from the stack's official generator or tool (e.g. `uv init`, `gradle init`, the platform's project template), at the decided versions, with its lockfile.
2. **Lint and format** tools with a configuration; their commands go into the fast tier.
3. **Tests** with the stack's usual framework, and one real test from day 1: the version check from `CONSTRAINTS.md` (an integer, the same everywhere). The task tier must run something real.
4. **Coverage** tool and threshold. The threshold is a decision for step 3; recommend the default of `constraint-driven-development` unless the owner has a number.
5. **Floor guard,** ported from the reference in `agent-skills/constraint-driven-development/references/floor-guard.md` (read it from the installed agent-skills plugin) into a language the project already needs, with this stack's suppression comments, test skips and stub patterns. Keep the reference's contract: exit 0 clean, 1 violation, 2 could not run; never print a secret's value.
6. **CI setup:** the steps that install the toolchain in CI at the same versions; one job per operating system from step 3 decision 1, each running the full test suite from the first commit, not only the system Claude works on, with a time limit per job (`{{CI_OS_RUNNERS}}` and `{{CI_TIMEOUT_MINUTES}}` in the CI template; why: `house-rules`, *Definition of Done*); the newest generally available runner image for each; `actions/checkout` and every other action pinned to a full commit sha looked up today, with the version in a comment; the current gitleaks release.
7. **`.gitignore`** for build output, caches and the binaries named in `CONSTRAINTS.md`.
8. **Version** set to `0` in every place the stack keeps one (principle *Release numbering*).
9. **Licence text** from its official source into `LICENSE`.
10. **How to run the real program,** as a command, even if it shows nothing yet.
11. **Decisions this stack adds** (e.g. an application id, a minimum platform version, signing): raise them in step 3 item 6 if they were missed, never decide them silently.

### 4.3 Fill the core templates

Copy every file from this skill's `templates/` folder into the project, except `docs/adr/0000-template.md` (that one is only for writing ADRs). `docs/intent/0000-template.md` is copied as it is, for the interviews of later features, and `scripts/ai_usage.py` as well, for the AI figures (principle *How it was made*; it needs `python3`). Then replace every `{{UPPER_SNAKE}}` placeholder with what the ADRs and the recipe say. Write the text yourself; a placeholder may need a sentence, not just a value. In `scripts/check.sh`, a line `: "{{…_COMMANDS}}"` is replaced as a whole by that tier's commands, one per line. Write the `README.md` from `../house-rules/README-template.md`, short: what it is, that it is at Day 1, and how it is being made. Run every text for readers through `clarity`.

**Adopt mode:** add only files that do not exist. If an existing file covers the same job (its own check script, its own CI), list it and ask the owner how to combine them; never overwrite it.

## Step 5: Close

Run these, in order, and report each result:

1. `git init` (new project only) and `git config core.hooksPath .githooks`.
2. `git ls-files -co --exclude-standard -z | xargs -0 grep -IlE '\{\{[A-Z0-9_]+\}\}' --` prints nothing.
3. `scripts/check.sh task` is green, with its time measured against the budget. If it is red, fix the cause; never weaken a check to get the first commit green (principle *Quality bar*). If a tool is missing, go back to 4.1.
4. `ls docs/adr` shows one ADR per decision from step 3 and per deviation from step 2.
5. Ask the owner once for this computer's short name (e.g. `linux`), then `python3 scripts/ai_usage.py --record <name>`; `docs/usage/<name>.json` goes into the first commit.
6. Commit everything as "Day 1: decisions and scaffold" through the hook (never `--no-verify`), and confirm from the output that the hook ran the task tier.
7. Offer to create the GitHub repository with the decided visibility (`gh repo create`) and push. Do it only after the owner says yes.

Then summarise for the owner: the folder, the ADRs with one line each, the check tiers with their measured times, how to run the real program, and anything the owner has to do by hand (e.g. a store account). Suggest `spec-driven-development` as the next step for the product itself.

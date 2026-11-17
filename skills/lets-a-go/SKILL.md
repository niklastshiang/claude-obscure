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
3. **Versions:** for each component, the newest stable release that every core dependency supports (principle *Runtime versions*). Name the release date and where support was confirmed.
4. **Licence** of the project, checked against the licences of the core dependencies and any assets, data or models it ships.
5. **Repository and stores:** public or private on GitHub; whether GitHub and each store from 1 accept AI-generated code, and who must submit what (some stores require the owner to write the listing or the manifest).
6. Anything the stack recipe (step 4) marks as a decision for this stack.

Adopt mode: skip every decision the project already records in `CLAUDE.md` or `docs/adr/`, and say which ones were found.

### ADRs

Each decision and each deviation from the principles gets one file in `docs/adr/`, numbered from `0001`, from `templates/docs/adr/0000-template.md` in this skill's folder. Fill every section: the options as they were put to the owner, the decision in the owner's words, the consequences for the code, and every source with the date it was read. Use the project's file language (principle *Languages*).

*Not built yet:* steps 4 and 5 (scaffold, close). Stop after step 3 and list the ADRs written.

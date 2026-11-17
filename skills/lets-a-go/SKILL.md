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

*Not built yet:* steps 2 to 5 (principles, project decisions, scaffold, close). Stop here and tell the owner which mode applied and what was created.

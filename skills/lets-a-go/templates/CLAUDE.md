# {{NAME}}

{{PURPOSE}}

Read CONSTRAINTS.md before writing code. Do not weaken it to make a change pass.

- Specification: SPEC.md (living document; when a decision changes, update SPEC.md first)
- Plan and tasks: tasks/plan.md, tasks/todo.md. A task is named by its module and a number within it (`<module>-3`), a checkpoint by its module; there is no counter for the whole project.
- Decisions: docs/adr/ (Day 1 decisions: ADR 0001 to {{LAST_DAY1_ADR}}, {{DATE}})
- Working rules: the `house-rules` skill of the `kickoff` plugin; this file and the ADRs win over it.
- Languages: code, comments, docs and commit messages in {{FILE_LANGUAGE}}. Talk to the owner in {{CHAT_LANGUAGE}}.
- Stack: {{STACK}} (ADR {{STACK_ADR}}). Versions: {{VERSIONS}}, checked on {{DATE}}; checked again before every release, an update is its own commit (ADR {{VERSIONS_ADR}}).
- Toolchain: {{TOOLCHAIN}}
- Checks: `scripts/check.sh fast` after every change (< {{FAST_BUDGET}}), `scripts/check.sh task` before every commit (< {{TASK_BUDGET}}; also the pre-commit hook), `scripts/check.sh full` in CI. Enable the hook in every clone: `git config core.hooksPath .githooks`.
- Start of a session: `git fetch`, then see how far the checkout is behind its remote branch and `main`, and whether `main` is green (`gh run list --branch main --limit 1`). Write specs, plans and task lists only on a current checkout.
- Run the real program: {{RUN_REAL_PROGRAM}}
- Large features: an interview first (`interview-me`), its result in `docs/intent/<feature>.md` from `docs/intent/0000-template.md`, confirmed by the owner before the spec.
- Lessons: before every release, read the commits since the one named in `docs/lessons.md` for work that was done twice, and write one entry per finding. A lesson seen a second time becomes a rule in this file.
- Usage per device: at the end of every session that commits and before every release, `python3 scripts/ai_usage.py --record <device>` (`py -3` on Windows; a short name of one's own, never the host's); `docs/usage/<device>.json` goes into that commit. `--summary` adds up every device for the README.
- Releases are numbered 1, 2, 3 … (+1 per release, every release counts, fixes included). Each release publishes how the project was made (who wrote the code, who decided, which guardrails held, what the AI cost).
- Facts about outside projects (maintenance, licence, versions, platform rules) come from the web on the day they are written down, with that date.
- Secrets ({{SECRET_FILES}}): never `source`, `cat` or print them, never print raw API responses, never put them into a subagent's brief. Check them only by metadata or a silent pattern match.

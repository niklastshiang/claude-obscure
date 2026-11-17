# Principles

The owner's answers to the questions every project raises. `lets-a-go` shows them once at the start of a project and never asks them. A project that deviates records the deviation in an ADR; this file changes only when the owner says so.

A row marked **open** is not decided yet: `lets-a-go` asks it like a project decision and proposes the owner's answer as a new row here.

| Topic | Rule | Decided |
|---|---|---|
| Languages | Code, comments, docs and commit messages in English. Claude talks with the owner in German. *Why: Stickler switched everything to English on day 2; translating the code changed cache keys, 445 results had to be rekeyed, and some file names stayed in the old language.* | owner, 2026-11-12 (Stickler) |
| Runtime versions | The newest stable release that every core dependency supports, checked on the web on Day 1 and cited with sources. Checked again before every release; an update is its own commit, never part of other work. *Why: Stickler moved its Python version three times mid-project, each time with lock updates, recomputed results and a follow-up fix.* | owner, 2026-11-17 |
| Release numbering | Plain integers: 1, 2, 3 …, +1 per release, every release counts, fixes included. CI fails when the tag and the version in the code differ. Release steps follow `house-rules`, *Release*. | owner, 2026-11-17 (Stickler ADR 0006) |
| How it was made | Every project publishes how it was made: who wrote the code, who decided, which guardrails held, and what the AI cost (tokens, money at API prices), refreshed every release. | owner, 2026-11-17 |
| Quality bar | `CONSTRAINTS.md` from the first commit, enforced by a pre-commit hook and CI, plus a floor guard that inspects the diff for weakened checks (new suppressions, skips, stubs, lowered thresholds, secret patterns). The bar may be raised, never lowered to get a change through. *Why: Stickler raised coverage from 80 to 95 % and never lowered it; the guard and the hook kept every commit honest.* | owner, 2026-11-12 (Stickler) |
| Check tiers | Three tiers with time budgets: fast after every edit (seconds), task before every commit (a minute or two; also the pre-commit hook), full in CI. The commands stand in the project's `CLAUDE.md`. | owner, Stickler (2026-11) |
| Hook in every clone | Enable the hook in every clone (`git config core.hooksPath .githooks`), and never chain a commit after a check in a way that ignores its result. *Why: in a fresh cloud clone without the hook, a commit went through while seven tests were red.* | owner, Stickler (2026-11) |
| Secrets | Name the files that hold secrets in `CLAUDE.md`. Never `cat`, `source` or print them, never print raw API responses, never put a secret into a subagent's brief; check them only by metadata or a silent pattern match. Scan the whole history before a repository goes public. *Why: a cloud GPU provider's pod response contains the pod's login password; printing it once would have put it in the transcript.* | owner, Stickler (2026-11) |
| Facts from the web | Facts about outside projects (maintenance status, licence, current version, platform rules) come from the web on the day they are written down, with that date, never from memory. *Why: a dependency's original repository was archived; the maintained fork was only found by checking.* | owner, Stickler (2026-11) |
| Texts for readers | Every text a person reads goes through `clarity`: READMEs, docs, specs, release notes, commit messages, comments on GitHub, replies to the owner. | owner, 2026-11-16 |
| Hosting | GitHub. Whether the repository is public or private is decided per project; whether GitHub and any store accept AI-generated code is checked per project. | owner, 2026-11-17 |

Not principles, decided per project (owner, 2026-11-17): the licence, public or private repository, the stack, the concrete versions, and the rules of the chosen forge and store on AI-generated code.

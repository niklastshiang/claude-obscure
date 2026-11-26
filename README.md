<h1 align="center">
  <code>CLAUDE-OBSCURE://SKILLS</code>
</h1>

<p align="center">
  <strong>How I build software with Claude Code: my rules, as a plugin.</strong><br/>
  <em>Obscure: known to hardly anyone. Yet.</em>
</p>

<p align="center">
  <a href="LICENSE"><img src="docs/badges/facts-license.svg" alt="license: MIT" /></a>
  <img src="docs/badges/facts-claude-code.svg" alt="Claude Code 2.1.324 or later" />
  <img src="docs/badges/facts-skills.svg" alt="own skills" />
  <a href="skills/lets-a-go/principles.md"><img src="docs/badges/facts-principles.svg" alt="principles" /></a>
  <img src="docs/badges/facts-pins.svg" alt="third-party code pinned to reviewed commits" />
</p>

<p align="center">
  <img src="docs/badges/fun-burgers.svg" alt="burgers" />
</p>

<p align="center"><sub>Badges: <a href="scripts/badges.py">scripts/badges.py</a>, rendered with <a href="https://shieldcn.dev">shieldcn</a>.</sub></p>

<p align="center">
  <a href="#-install"><strong>Install</strong></a> ·
  <a href="#-the-plugins">The plugins</a> ·
  <a href="#-how-a-project-starts">How a project starts</a> ·
  <a href="skills/lets-a-go/principles.md">Principles</a> ·
  <a href="https://github.com/niklastshiang/stickler">Stickler</a>
</p>

---

## `> WHAT IS THIS`

In my projects Claude writes all the code and I make all the decisions. That split works, but it
fails in its own ways: conventions settled late and changed at great cost, work called done that
breaks the first time the real program runs, decisions the agent made without asking, checks
weakened to get green, and documents that drift away from the code.

This repository holds what I do about it, as skills for Claude Code. `/kickoff:lets-a-go` starts a
new project: it shows my principles once, prepares every project decision with research and a
recommendation, records each one, and builds a scaffold whose checks hold from the first commit.
`house-rules` is what Claude follows for the rest of the project.

The rules come from building [Stickler](https://github.com/niklastshiang/stickler), a drum
transcriber that grew from a command-line benchmark into desktop apps for Linux and the Mac over
nine releases, then began a Windows app. Most rules carry a one-line *Why* with what happened there.

---

## `> THE PLUGINS`

The marketplace `niklastshiang` lists three plugins. Installing `kickoff` installs the other two.

| Plugin | What it is for |
|---|---|
| `kickoff` | [`lets-a-go`](skills/lets-a-go/SKILL.md): starts a new project with my principles and the decisions it needs, and builds the scaffold. [`house-rules`](skills/house-rules/SKILL.md): working rules for a project that Claude builds while I decide: what "done" means, how decisions are recorded, how subagents are orchestrated, releases, and a README template. |
| `agent-skills` | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT): engineering skills from spec to ship. `kickoff` builds on them. |
| `clarity` | [addyosmani/clarity](https://github.com/addyosmani/clarity) (MIT): prose that reads like its author. Every text for readers goes through it. |

Next to them I run two tools from their own sources, each pinned to a commit I read (see
[`> INSTALL`](#-install)): [microsoft/TokenEconomizer](https://github.com/microsoft/TokenEconomizer)
learns short facts about each repository across sessions, and
[Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) turns a folder into a knowledge
graph that Claude can query instead of reading file after file.

---

## `> HOW A PROJECT STARTS`

`/kickoff:lets-a-go` in an empty folder, one session:

1. **Where.** Name and one-line purpose; it creates `YYYY-MM-DD_Name`. In a folder that already
   holds a project it switches to adopt mode and changes no existing file.
2. **Principles.** My [principles](skills/lets-a-go/principles.md) as one table, then one
   question: anything different this time? A deviation becomes an ADR.
3. **Project decisions,** one at a time, each researched on the web that day, with options, a
   recommendation and dated sources: where it runs, the stack, the versions, the licence, the
   forge's and stores' rules on AI-generated code. Each answer becomes an ADR.
4. **Scaffold.** `CLAUDE.md`, `CONSTRAINTS.md`, three check tiers (fast, task, full), the
   pre-commit hook, CI, the README; the stack's part worked out fresh, so versions are current.
5. **Close.** `git init`, the hook on, the task tier green, the first commit through the hook.

Then `spec-driven-development` from agent-skills takes over for the product, and `house-rules`
for the way of working.

---

## `> INSTALL`

In Claude Code 2.1.324 or later:

```bash
claude plugin marketplace add niklastshiang/claude-obscure
claude plugin install kickoff@niklastshiang
```

Inside a session the same lines start with `/plugin` instead of `claude plugin`. Start a new
session afterwards; plugins load at session start.

<details>
<summary><b>TokenEconomizer</b>: facts about each repository, learned across sessions</summary>

From its own marketplace, pinned to the commit I read, with only the micro-skills turned on:

```bash
claude plugin marketplace add microsoft/TokenEconomizer@b57d03f81585a18b936a0eaecbd1eb51cdcecf71
claude plugin install tokeneconomizer@tokeneconomizer
~/.claude/plugins/cache/tokeneconomizer/tokeneconomizer/0.1.0/scripts/te config set microskills=on toolprune=off loopguard=off --global --host claude
```

It needs Python 3.10 or later, keeps what it learns in `~/.tokeneconomizer`, and every third
session asks Haiku, through your own `claude`, to propose facts.

</details>

<details>
<summary><b>graphify</b>: a knowledge graph of a folder, for Claude to query</summary>

A Python package, not a plugin, so it is installed as a tool, pinned to the commit I read
(v0.9.112), and then registers its skill:

```bash
uv tool install git+https://github.com/Graphify-Labs/graphify@340268a70a83588d6b3c6de1fffb05326350ef1d
graphify install
```

It needs Python 3.11 or later. `graphify install` copies the skill to `~/.claude/skills/graphify`
and adds a short `## graphify` block to `~/.claude/CLAUDE.md`; it adds no hooks. Building a graph
runs through your own Claude session. It goes to the network only for URLs you hand it, and calls
a model API directly only if you set that up with your own key. `graphify uninstall` removes the
skill and the block again, and deletes `~/.claude/CLAUDE.md` when nothing else is in it.

</details>

<details>
<summary><b>Cloud environments</b>: claude.ai/code installs no plugins from settings</summary>

Put these two lines into the environment's setup script; `install.sh` copies the same pinned
skills into `~/.claude/skills` and installs graphify the same way as above:

```bash
git clone --depth 1 https://github.com/niklastshiang/claude-obscure /tmp/claude-obscure
bash /tmp/claude-obscure/install.sh
```

</details>

### Removing it

```bash
for p in kickoff agent-skills clarity; do claude plugin uninstall "$p@niklastshiang"; done
claude plugin marketplace remove niklastshiang
```

After `install.sh`, delete the copied folders from `~/.claude/skills` instead. For graphify, run
`graphify uninstall` and then `uv tool uninstall graphifyy`.

---

## `> WHERE THE RULES COME FROM`

Every rule in `house-rules` and every principle came out of Stickler, and most say what happened
there. Three of them:

- **Done means it ran in the real program**, not that the tests are green. Nearly every
  checkpoint found bugs that all tests had passed: a data file missing from the installed package,
  translations missing from one package format, numbers formatted by the locale.
- **Settle the language, the licence and the versions on day 1.** Stickler changed all three
  mid-project; translating the code alone changed cache keys, and 445 results had to be rekeyed.
- **Check a subagent's result before using it.** Its mistakes arrive in the same confident tone
  as its findings.

The principles are my answers to the questions every project raises, so `lets-a-go` never asks
them again: [`skills/lets-a-go/principles.md`](skills/lets-a-go/principles.md).

---

## `> ROADMAP`

- **Now:** dry runs of `lets-a-go` on real stacks and in adopt mode.
- **Next:** release 1.

<details>
<summary><b>Done</b></summary>

- 2026-11-16: the rules from Stickler as one skill, with a README template
- 2026-11-17: the plugin marketplace with agent-skills and clarity, pinned; TokenEconomizer;
  checks, hook and CI for this repository
- 2026-11-18: `lets-a-go` with principles, ADRs and the scaffold's templates; graphify; the
  repository renamed to claude-obscure
- 2026-11-24: Claude Code's usage recorded per device; this README
- 2026-11-24: what Stickler's releases 8 to 10 and its Windows start taught
  ([spec](SPEC-stickler-lessons-2.md)): a new principle, a program for more than one operating
  system gets one cross-platform framework; CI on every system; an intent before a spec; the
  pre-commit hook enforced; the usage script in every new project
- 2026-11-26: what Stickler's Mac and Windows work since then taught, and what two projects on
  one framework each show, Readest and Mornye ([spec](SPEC-lessons-3.md)): rules for work on
  several computers and branches, checks that say why they are red, CI that installs and starts
  what users get, and a lessons file in every project, read before each release; Flutter for
  programs with more than two target systems (owner)

</details>

---

## `> ORIGIN`

<p align="center">
  <img src="docs/badges/origin-built-with.svg" alt="built with Claude Code" />
  <img src="docs/badges/origin-code.svg" alt="code: 100% AI" />
  <img src="docs/badges/origin-decisions.svg" alt="decisions: 100% human" />
  <img src="docs/badges/origin-ai-cost.svg" alt="AI cost at API prices" />
  <img src="docs/badges/origin-tokens.svg" alt="tokens used" />
</p>

Claude (Anthropic) wrote the skills, the scripts and the documentation in Claude Code. I set the
goals, bring the experience from Stickler, make the decisions and read every rule before it goes
in.

<details>
<summary><b>How it is kept honest</b>: three rules the repository enforces</summary>

- **Third-party code is pinned to commits I read.** To move a pin, read the diff since the old
  commit, then change it everywhere at once; `scripts/check_repo.py` fails when two places
  disagree.
- **Spec first.** What gets built is set out in a spec and a task list (`SPEC-*.md`,
  [`tasks/`](tasks/)), each approved before the work starts.
- **One check for hook and CI.** `scripts/check.sh` runs shellcheck, the consistency checks and
  `claude plugin validate`, before every commit and in CI.

</details>

<details>
<summary><b>What the AI cost</b>: about 26 USD at API prices, as of 2026-11-26</summary>

Claude Code logs the tokens of every response;
[`scripts/ai_usage.py`](scripts/ai_usage.py) sums them and prices them with Anthropic's
[API prices](https://platform.claude.com/docs/en/about-claude/pricing). Every computer that works
on this repository records its days in [`docs/usage/`](docs/usage/), and the table adds them up.
On a subscription the real cost differs; this is what the same work would cost on the API.

| Period | Model | Responses | Output tokens | Cache read | API cost |
|---|---|---:|---:|---:|---:|
| 17–24 Nov 2026 | Claude Opus 5.5 (the work; Linux) | 253 | 0.26 M | 34 M | 18.30 USD |
| 26 Nov 2026 | Claude Fable 5.2 (the work; Linux) | 35 | 0.06 M | 4.9 M | 5.89 USD |
| 17–26 Nov 2026 | Claude Sonnet 5.5 (helpers; Linux) | 43 | 0.03 M | 2.2 M | 1.36 USD |
| 17–24 Nov 2026 | Claude Haiku 5.5 (helpers; Linux) | 6 | 0.01 M | 0.07 M | 0.02 USD |
| | **Total** (43 M tokens, about 2.3 hours active) | | | | **about 26 USD** |

What is missing: the first day (16 November), worked in cloud sessions on claude.ai/code whose
logs are not on this computer.

</details>

---

## `> MORE DETAILS`

<details>
<summary><b>Moving a pin</b>: how a third-party commit is updated</summary>

The commits are pinned in `.claude-plugin/marketplace.json` and in `install.sh`; graphify's pin is
in `install.sh` and in this README. To move one, read what changed since the old commit, then
change both files; `scripts/check.sh` fails when they differ. The pre-commit hook and CI run the
same script; enable the hook once per clone with `git config core.hooksPath .githooks`.

</details>

<details>
<summary><b>Repository layout</b>: where what is</summary>

```text
.claude-plugin/   marketplace.json (the three plugins), plugin.json (kickoff)
skills/           my skills, one folder each; lets-a-go holds principles.md and the templates
install.sh        the same skills without the plugin system, plus graphify, for cloud environments
scripts/          check.sh and check_repo.py (hook and CI), ai_usage.py and badges.py (README figures)
docs/             badges, usage per device, ideas
tasks/            plan and tasks; specs at the top level as SPEC-*.md
.claude/          CLAUDE.md: this repository's own day 1 decisions
```

</details>

---

## `> LICENSE`

**This repository** is under the [MIT licence](LICENSE) (decided 2026-11-16). Copyright © 2026
Niklas Tshiang Tshiananga.

**The third-party skills** keep their own licences and are fetched from their sources, never copied
here. agent-skills and clarity are MIT (Addy Osmani); `install.sh` puts their licences next to them
as `agent-skills-LICENSE` and `clarity/LICENSE`. graphify is Apache-2.0 since 2026-07-22 (earlier
parts stay MIT, see its `NOTICE`; checked 2026-11-18). TokenEconomizer is MIT (checked 2026-11-17).

---

## `> SUPPORT MY WORK`

Nobody reads this anyway. But if you ever run into me in real life, feel free to buy me a
burger. 🍔

---

<p align="center">
  <a href="https://github.com/niklastshiang/claude-obscure/issues">Report a problem</a> ·
  <a href="skills/lets-a-go/principles.md">Principles</a> ·
  <a href="skills/house-rules/SKILL.md">House rules</a> ·
  <a href="https://github.com/niklastshiang/stickler">Stickler</a>
</p>

<p align="center">
  <strong><code>> LET'S-A-GO._</code></strong>
</p>

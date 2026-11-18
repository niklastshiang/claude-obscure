# claude-obscure

My skills for Claude Code, as a plugin marketplace that also carries the third-party skills they build on, each pinned to a commit I reviewed.

| Plugin | What it is for |
|---|---|
| `kickoff` | [`lets-a-go`](skills/lets-a-go/SKILL.md): starts a new project with my principles and the decisions it needs, and builds the scaffold. [`house-rules`](skills/house-rules/SKILL.md): working rules for a programming project that Claude builds while I make the decisions: what to settle on day 1, what "done" means, how decisions are recorded, how subagents are orchestrated, releases, and a README template. Learned from building [Stickler](https://github.com/niklastshiang/stickler). Installing it also installs the next two. |
| `agent-skills` | [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT): engineering skills from spec to ship. `kickoff` builds on them. |
| `clarity` | [addyosmani/clarity](https://github.com/addyosmani/clarity) (MIT): prose that reads like its author. Every text for readers goes through it. |

## Install

In Claude Code 2.1.324 or later:

```bash
claude plugin marketplace add niklastshiang/claude-obscure
claude plugin install kickoff@niklastshiang
```

Inside a session the same lines start with `/plugin` instead of `claude plugin`. Start a new session afterwards; plugins load at session start.

I also run [microsoft/TokenEconomizer](https://github.com/microsoft/TokenEconomizer) (MIT), which learns short facts about each repository across sessions. It comes from its own marketplace, pinned to the commit I read, with only the micro-skills turned on:

```bash
claude plugin marketplace add microsoft/TokenEconomizer@b57d03f81585a18b936a0eaecbd1eb51cdcecf71
claude plugin install tokeneconomizer@tokeneconomizer
~/.claude/plugins/cache/tokeneconomizer/tokeneconomizer/0.1.0/scripts/te config set microskills=on toolprune=off loopguard=off --global --host claude
```

It needs Python 3.10 or later, keeps what it learns in `~/.tokeneconomizer`, and every third session asks Haiku, through your own `claude`, to propose facts.

And [Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) (Apache-2.0), which turns a folder of code or documents into a knowledge graph that Claude can query instead of reading file after file. It is a Python package, not a plugin, so it is installed as a tool, pinned to the commit I read (v0.9.112), and then registers its skill:

```bash
uv tool install git+https://github.com/Graphify-Labs/graphify@340268a70a83588d6b3c6de1fffb05326350ef1d
graphify install
```

It needs Python 3.11 or later. `graphify install` copies the skill to `~/.claude/skills/graphify` and adds a short `## graphify` block to `~/.claude/CLAUDE.md`; it adds no hooks. Building a graph runs through your own Claude session. It goes to the network only for URLs you hand it, and calls a model API directly only if you set that up with your own key. `graphify uninstall` removes the skill and the block again, and deletes `~/.claude/CLAUDE.md` when nothing else is in it.

### Cloud environments

Cloud sessions on claude.ai/code do not install plugins from settings. Put these two lines into the environment's setup script; `install.sh` copies the same pinned skills into `~/.claude/skills` and installs graphify the same way as above:

```bash
git clone --depth 1 https://github.com/niklastshiang/claude-obscure /tmp/claude-obscure
bash /tmp/claude-obscure/install.sh
```

### Remove

```bash
for p in kickoff agent-skills clarity; do claude plugin uninstall "$p@niklastshiang"; done
claude plugin marketplace remove niklastshiang
```

After `install.sh`, delete the copied folders from `~/.claude/skills` instead. For graphify, run `graphify uninstall` and then `uv tool uninstall graphifyy`.

## Moving a pin

The commits are pinned in `.claude-plugin/marketplace.json` and in `install.sh`; graphify's pin is in `install.sh` and in this README. To move one, read what changed since the old commit, then change both files; `scripts/check.sh` fails when they differ. The pre-commit hook and CI run the same script; enable the hook once per clone with `git config core.hooksPath .githooks`.

## Layout

```text
.claude-plugin/   marketplace.json (the three plugins), plugin.json (kickoff)
skills/           my skills, one folder each
install.sh        the same skills without the plugin system, plus graphify, for cloud environments
scripts/          check.sh and check_repo.py, run by the hook and CI
.claude/          CLAUDE.md: this repository's own day 1 decisions
```

## Licence

MIT (owner, 2026-11-16), see `LICENSE`. agent-skills and clarity are MIT as well (Addy Osmani); `install.sh` puts their licences next to them as `agent-skills-LICENSE` and `clarity/LICENSE`. graphify is Apache-2.0 since 2026-07-22 (earlier parts stay MIT, see its `NOTICE`); it is installed from its own repository and nothing of it is copied here (checked 2026-11-18).

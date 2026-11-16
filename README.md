# claude-skills

My skills for Claude Code, plus an installer that loads them together with the skills they build on.

| Skill | What it is for |
|---|---|
| [`owner-led-projects`](skills/owner-led-projects/SKILL.md) | Working rules for a programming project that Claude builds while I make the decisions: what to settle on day 1, what "done" means, how decisions are recorded, how subagents are orchestrated, releases, and a README template. Learned from building [Stickler](https://github.com/niklastshiang/stickler). |

They build on [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) and [addyosmani/clarity](https://github.com/addyosmani/clarity) (both MIT), which `install.sh` fetches at pinned, reviewed commits. To move to a newer commit, review its changes first, then update `AGENT_SKILLS_SHA` or `CLARITY_SHA`.

## Install

Into `~/.claude/skills` (Claude Code loads them for every project):

```bash
git clone --depth 1 https://github.com/niklastshiang/claude-skills ~/src/claude-skills
bash ~/src/claude-skills/install.sh
```

In a Claude Code cloud environment, put the same two lines into the environment's setup script, with a temporary folder instead of `~/src`.

## Licence

MIT (owner, 2026-11-16), see `LICENSE`. The agent-skills that `install.sh` fetches are MIT as well (Addy Osmani); their licence is installed next to them as `agent-skills-LICENSE`.

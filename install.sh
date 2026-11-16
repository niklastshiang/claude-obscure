#!/usr/bin/env bash
# Installs the skills into ~/.claude/skills: the agent-skills collection (pinned to a reviewed
# commit) and this repository's own skills, which build on it. Safe to run again.
# Never fails hard, so a cloud session still starts when GitHub is unreachable.

AGENT_SKILLS_SHA=39b723ceebf81474d0557c1fecd01eddab585563
DEST="$HOME/.claude/skills"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

mkdir -p "$DEST"

tmp=$(mktemp -d)
if git -C "$tmp" init -q \
  && git -C "$tmp" fetch -q --depth 1 https://github.com/addyosmani/agent-skills.git "$AGENT_SKILLS_SHA" \
  && git -C "$tmp" checkout -q FETCH_HEAD; then
  cp -r "$tmp"/skills/* "$DEST/"
  cp "$tmp/LICENSE" "$DEST/agent-skills-LICENSE"
  echo "agent-skills: installed ($AGENT_SKILLS_SHA)" >&2
else
  echo "agent-skills: download failed, skipping" >&2
fi
rm -rf "$tmp"

# clarity (addyosmani/clarity, MIT): writing that reads like its author, pinned to a reviewed
# commit; only the skill, its references and its two diagnostic scripts (stdlib only).
CLARITY_SHA=e27ceeff60368cf6966b4ea00a5b9b36418ee9a0
tmp=$(mktemp -d)
if git -C "$tmp" init -q \
  && git -C "$tmp" fetch -q --depth 1 https://github.com/addyosmani/clarity.git "$CLARITY_SHA" \
  && git -C "$tmp" checkout -q FETCH_HEAD; then
  mkdir -p "$DEST/clarity/scripts"
  cp "$tmp/SKILL.md" "$tmp/LICENSE" "$DEST/clarity/"
  cp -r "$tmp/references" "$DEST/clarity/"
  cp "$tmp/scripts/strip_markdown.py" "$tmp/scripts/prose_stats.py" "$DEST/clarity/scripts/"
  echo "clarity: installed ($CLARITY_SHA)" >&2
else
  echo "clarity: download failed, skipping" >&2
fi
rm -rf "$tmp"

# Own skills last: where a name collides, ours wins.
cp -r "$HERE"/skills/* "$DEST/"
echo "own skills: installed ($(ls "$HERE/skills" | tr '\n' ' '))" >&2

#!/usr/bin/env bash
# Installs the skills into ~/.claude/skills without the plugin system, for Claude Code cloud
# environments (they do not install plugins from settings): agent-skills and clarity, each pinned
# to a reviewed commit, then this repository's own skills, which build on them. Safe to run again.
# Never fails hard, so a cloud session still starts when GitHub is unreachable.
# The pins must match .claude-plugin/marketplace.json; scripts/check.sh fails if they differ.

DEST="$HOME/.claude/skills"
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

mkdir -p "$DEST"

# install_pinned <owner/repo> <sha> <copy function>: fetch one commit of a GitHub repository and
# hand its checkout to the copy function. Reports and continues when the download fails.
install_pinned() {
  local repo=$1 sha=$2 copy=$3 dir="$TMP/${1#*/}"
  mkdir -p "$dir"
  if git -C "$dir" init -q \
    && git -C "$dir" fetch -q --depth 1 "https://github.com/$repo.git" "$sha" \
    && git -C "$dir" checkout -q FETCH_HEAD; then
    "$copy" "$dir"
    echo "$repo: installed ($sha)" >&2
  else
    echo "$repo: download failed, skipping" >&2
  fi
}

# agent-skills (MIT): every skill, and its licence next to them.
copy_agent_skills() {
  cp -r "$1"/skills/* "$DEST/"
  cp "$1/LICENSE" "$DEST/agent-skills-LICENSE"
}

# clarity (MIT): only the skill, its references and its two diagnostic scripts (stdlib only).
copy_clarity() {
  mkdir -p "$DEST/clarity/scripts"
  cp "$1/SKILL.md" "$1/LICENSE" "$DEST/clarity/"
  cp -r "$1/references" "$DEST/clarity/"
  cp "$1/scripts/strip_markdown.py" "$1/scripts/prose_stats.py" "$DEST/clarity/scripts/"
}

install_pinned addyosmani/agent-skills 39b723ceebf81474d0557c1fecd01eddab585563 copy_agent_skills
install_pinned addyosmani/clarity e27ceeff60368cf6966b4ea00a5b9b36418ee9a0 copy_clarity

# Own skills last: where a name collides, ours wins.
own=()
for skill in "$HERE"/skills/*/; do
  cp -r "$skill" "$DEST/"
  own+=("$(basename "$skill")")
done
echo "own skills: installed (${own[*]})" >&2

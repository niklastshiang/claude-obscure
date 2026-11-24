"""Checks that keep the repository's files consistent with each other.

- the pinned commits in install.sh and .claude-plugin/marketplace.json are full SHAs and agree
- graphify's pinned commit in install.sh is a full SHA and the README installs the same one
- every skill under skills/ has front matter whose name matches its folder, and a description
- every skill is listed in the README's table
- every core template of lets-a-go exists
- every row of skills/lets-a-go/principles.md has a topic, a rule and a "Decided" entry
- scripts/ai_usage.py is the same file as lets-a-go's template, so the two do not drift
"""
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
errors = []

install = (ROOT / "install.sh").read_text(encoding="utf-8")
market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
json.loads((ROOT / ".claude-plugin/plugin.json").read_text(encoding="utf-8"))

pins = {p["source"]["repo"]: p["source"].get("sha")
        for p in market["plugins"] if isinstance(p["source"], dict)}
for repo, sha in pins.items():
    if not sha or not re.fullmatch(r"[0-9a-f]{40}", sha):
        errors.append(f"marketplace.json: {repo} is not pinned to a full 40-character sha")
    found = re.search(rf"install_pinned\s+{re.escape(repo)}\s+([0-9a-f]+)", install)
    if not found:
        errors.append(f"install.sh: no install_pinned line for {repo}")
    elif found.group(1) != sha:
        errors.append(f"{repo}: install.sh pins {found.group(1)}, marketplace.json pins {sha}")

readme = (ROOT / "README.md").read_text(encoding="utf-8")

graphify = re.search(r"^GRAPHIFY_SHA=(\S+)$", install, re.M)
if not graphify or not re.fullmatch(r"[0-9a-f]{40}", graphify.group(1)):
    errors.append("install.sh: GRAPHIFY_SHA is not a full 40-character sha")
else:
    pins["Graphify-Labs/graphify"] = graphify.group(1)
    readme_pins = set(re.findall(r"Graphify-Labs/graphify@([0-9a-f]+)", readme))
    if readme_pins != {graphify.group(1)}:
        errors.append(f"graphify: install.sh pins {graphify.group(1)}, README.md pins "
                      f"{', '.join(sorted(readme_pins)) or 'nothing'}")
for skill in sorted((ROOT / "skills").iterdir()):
    text = (skill / "SKILL.md").read_text(encoding="utf-8")
    head = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not head:
        errors.append(f"{skill.name}: SKILL.md has no front matter")
        continue
    fields = dict(re.findall(r"^(\w+):\s*(.+)$", head.group(1), re.M))
    if fields.get("name") != skill.name:
        errors.append(f"{skill.name}: front matter name is {fields.get('name')!r}")
    if not fields.get("description"):
        errors.append(f"{skill.name}: front matter has no description")
    if f"`{skill.name}`" not in readme:
        errors.append(f"{skill.name}: not listed in README.md")

TEMPLATES = ["CLAUDE.md", "CONSTRAINTS.md", "scripts/check.sh", ".githooks/pre-commit",
             ".github/workflows/check.yml", "docs/adr/0000-template.md", "scripts/ai_usage.py",
             "docs/intent/0000-template.md"]
for t in TEMPLATES:
    if not (ROOT / "skills/lets-a-go/templates" / t).is_file():
        errors.append(f"lets-a-go: template {t} is missing")

usage = ROOT / "scripts/ai_usage.py"
template = ROOT / "skills/lets-a-go/templates/scripts/ai_usage.py"
if usage.is_file() and template.is_file() and usage.read_bytes() != template.read_bytes():
    errors.append("scripts/ai_usage.py differs from lets-a-go's template; change both together")

principles = ROOT / "skills/lets-a-go/principles.md"
rows = 0
if not principles.is_file():
    errors.append("skills/lets-a-go/principles.md is missing")
else:
    for n, line in enumerate(principles.read_text(encoding="utf-8").splitlines(), 1):
        if not line.startswith("|") or line.startswith("|---") or line.startswith("| Topic |"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        rows += 1
        if len(cells) != 3 or not all(cells):
            errors.append(f"principles.md:{n}: a row needs a topic, a rule and a Decided entry")
    if not rows:
        errors.append("principles.md: no rows")

for e in errors:
    print(e, file=sys.stderr)
print(f"check_repo: {len(pins)} pins, {len(list((ROOT / 'skills').iterdir()))} skills, "
      f"{rows} principles, "
      f"{len(errors)} errors", file=sys.stderr)
sys.exit(1 if errors else 0)

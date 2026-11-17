"""Checks that keep the repository's files consistent with each other.

- the pinned commits in install.sh and .claude-plugin/marketplace.json are full SHAs and agree
- every skill under skills/ has front matter whose name matches its folder, and a description
- every skill is listed in the README's table
- every row of skills/lets-a-go/principles.md has a topic, a rule and a "Decided" entry
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

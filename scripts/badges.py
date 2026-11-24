"""Renders the README badges with shieldcn.dev into docs/badges/*.svg.

The SVGs live in the repository, so the README does not depend on the service being up. The
style is Stickler's (scripts/badges.py there): each row is a rainbow, every badge's gradient
starts where the previous one ends, the two top rows (facts, then the shimmering burger) share
one rainbow, and the value is set bold by outlining its glyph path. The figures come from the
repository: the skills and principles are counted, the pins read from marketplace.json and
install.sh, the AI figures summed over every device in docs/usage/ (scripts/ai_usage.py).

    python3 scripts/badges.py          # after changes that move the numbers
"""

from __future__ import annotations

import colorsys
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.dont_write_bytecode = True  # no __pycache__ next to the scripts
sys.path.insert(0, str(Path(__file__).resolve().parent))
import ai_usage  # noqa: E402  (next to this script)

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "docs" / "badges"
SERVICE = "https://shieldcn.dev/badge"
USER_AGENT = "claude-obscure-badges (+https://github.com/niklastshiang/claude-obscure)"
STYLE = {"font": "jetbrains-mono", "split": "false"}
# shieldcn draws the text as two white paths: the label (slightly transparent) and the value
VALUE_PATH = '<path fill="#fff" d='
BOLD = 'stroke="#fff" stroke-width="0.8" stroke-linejoin="round" '
# Hue path in degrees: orange → red → pink → violet → blue → cyan (no yellow/green)
HUE_START, HUE_END = 30.0, -170.0


def facts() -> dict[str, str]:
    skills = sum(1 for path in (ROOT / "skills").glob("*/SKILL.md"))
    principles = sum(
        1
        for line in (ROOT / "skills/lets-a-go/principles.md").read_text(encoding="utf-8").splitlines()
        if line.startswith("|") and not line.startswith(("|---", "| Topic |"))
    )
    market = json.loads((ROOT / ".claude-plugin/marketplace.json").read_text(encoding="utf-8"))
    pins = sum(1 for plugin in market["plugins"] if isinstance(plugin["source"], dict))
    install = (ROOT / "install.sh").read_text(encoding="utf-8")
    pins += bool(re.search(r"^GRAPHIFY_SHA=[0-9a-f]{40}$", install, re.M))
    pins += 1  # TokenEconomizer, pinned in the README's install line
    _rows, total = ai_usage.summary()
    return {
        "skills": str(skills),
        "principles": str(principles),
        "pins": f"{pins} reviewed",
        "ai_cost": f"≈ {total['cost']:,.0f} USD",
        "ai_tokens": f"{total['tokens'] / 1e6:,.0f} M",
    }


def rows(f: dict[str, str]) -> dict[str, list[tuple[str, str, str]]]:
    """(file name, label, message) per row; the joke row shimmers."""
    return {
        "facts": [
            ("license", "license", "MIT"),
            ("claude-code", "claude code", "≥ 2.1.324"),
            ("skills", "own skills", f["skills"]),
            ("principles", "principles", f["principles"]),
            ("pins", "pins", f["pins"]),
        ],
        "fun": [
            ("burgers", "burgers received", "0"),
        ],
        "origin": [
            ("built-with", "built with", "Claude Code"),
            ("code", "code", "100% AI"),
            ("decisions", "decisions", "100% human"),
            ("ai-cost", "AI cost", f["ai_cost"]),  # at API prices, see README > ORIGIN
            ("tokens", "tokens", f["ai_tokens"]),
        ],
    }


def hex_at(hue: float) -> str:
    r, g, b = colorsys.hls_to_rgb((hue % 360) / 360, 0.5, 0.85)
    return f"{round(r * 255):02x}{round(g * 255):02x}{round(b * 255):02x}"


def url(label: str, message: str, start: float, end: float, shimmer: bool) -> str:
    def part(text: str) -> str:  # shields syntax: "-" → "--", "_" → "__", then URL-encode
        return urllib.parse.quote(text.replace("-", "--").replace("_", "__"), safe="")

    query = {**STYLE, "gradient": f"{hex_at(start)},{hex_at(end)},90"}
    if shimmer:
        query["animate"] = "shimmer"
    return f"{SERVICE}/{part(label)}-{part(message)}-{hex_at(start)}.svg?" + urllib.parse.urlencode(
        query
    )


def bold_value(svg: bytes, file: str) -> bytes:
    """Sets the value bold by outlining its glyph path."""
    text = svg.decode("utf-8")
    if text.count(VALUE_PATH) != 1:
        sys.exit(f"{file}: shieldcn's SVG changed, the value path was not found exactly once")
    return text.replace(VALUE_PATH, VALUE_PATH.replace("d=", BOLD + "d=")).encode("utf-8")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    all_rows = rows(facts())
    top = len(all_rows["facts"]) + len(all_rows["fun"])  # one rainbow over the two top rows
    for name, badges in all_rows.items():
        if name in ("facts", "fun"):
            count, offset = top, (len(all_rows["facts"]) if name == "fun" else 0)
        else:
            count, offset = len(badges), 0
        step = (HUE_END - HUE_START) / count
        for i, (file, label, message) in enumerate(badges):
            start = HUE_START + (offset + i) * step
            link = url(label, message, start, start + step, shimmer=name == "fun")
            request = urllib.request.Request(link, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=30) as response:
                svg = response.read()
            if not svg.lstrip().startswith(b"<svg"):
                sys.exit(f"{file}: no SVG returned")
            (OUT / f"{name}-{file}.svg").write_bytes(bold_value(svg, file))
            print(f"{name}-{file}.svg  {label}: {message}")


if __name__ == "__main__":
    main()

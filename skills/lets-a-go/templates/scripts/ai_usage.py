"""Tokens, active time and API-equivalent cost of building this project with Claude Code.

Claude Code keeps each session's log under ~/.claude/projects/<the project's path>/, with the
token usage of every response. This sums them per model (a response split over several log lines
counts once) and prices them with Anthropic's API prices. On a subscription the real cost
differs; the logs on a machine are the only source, so sessions whose logs are gone are missing.

    python3 scripts/ai_usage.py                    # this machine's logs, as a table
    python3 scripts/ai_usage.py --record linux     # this machine's days into docs/usage/linux.json
    python3 scripts/ai_usage.py --summary          # every device recorded in docs/usage/

Every computer that works on the project records its days into the repository at the end of a
session that commits and before a release, so the figures of all of them can be added up: the
tokens per model and day, and the active time (the logs' wall clock, gaps of up to 15 minutes
counted as work). A recorded day is replaced only when the logs now hold at least as many
responses for it, so a later run with fewer logs never shrinks the record.

More logs of the same project: `--project PATH` adds the logs of an earlier path (a folder that
was renamed), `--log FILE` one session's log that was started in another folder (its subagents'
logs next to it are included). Both can be given more than once.
"""

from __future__ import annotations

import argparse
import collections
import datetime
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RECORDS = ROOT / "docs" / "usage"
PROJECTS = Path.home() / ".claude" / "projects"
# USD per million tokens, from https://platform.claude.com/docs/en/about-claude/pricing
# (checked 2026-11-24). Claude Code caches for an hour, so cache writes use the 1 h price.
PRICES = {
    "claude-fable-5-2": {"input": 8.0, "cache_write": 16.0, "cache_read": 0.20, "output": 40.0},
    "claude-opus-5-5": {"input": 4.0, "cache_write": 8.0, "cache_read": 0.20, "output": 20.0},
    "claude-sonnet-5-5": {"input": 2.0, "cache_write": 4.0, "cache_read": 0.10, "output": 10.0},
    "claude-haiku-5-5": {"input": 0.10, "cache_write": 0.20, "cache_read": 0.01, "output": 0.50},
    "claude-haiku-5-5 (long prompt)": {
        "input": 0.50,
        "cache_write": 1.0,
        "cache_read": 0.05,
        "output": 2.50,
    },
}
# A request whose prompt (input, cache reads and cache writes) is longer pays the long prices
LONG_PROMPT = {"claude-haiku-5-5": 100_000}
KINDS = {
    "input": "input_tokens",
    "cache_write": "cache_creation_input_tokens",
    "cache_read": "cache_read_input_tokens",
    "output": "output_tokens",
}
BREAK = datetime.timedelta(minutes=15)  # a longer gap between log entries is a break
DEVICE = re.compile(r"[a-z0-9][a-z0-9-]{0,23}")
FIELDS = ("responses", "input", "output", "cache_read", "cache_write")


def log_folders(project: Path = ROOT) -> list[Path]:
    """The log folders of a checkout and of every worktree under its `.claude/worktrees`,
    whichever of them `project` is. Claude Code names a project's log folder after its path,
    every character but letters and digits as '-' (`/x/.claude/worktrees/y` is
    `-x--claude-worktrees-y`). A record replaces whole days, so it reads the sessions of all
    of them, not only the one it runs in."""
    if project.parent.name == "worktrees" and project.parent.parent.name == ".claude":
        project = project.parents[2]
    name = re.sub(r"[^A-Za-z0-9]", "-", str(project))
    return [PROJECTS / name, *sorted(PROJECTS.glob(f"{name}--claude-worktrees-*"))]


def sources(projects: list[Path], logs: list[Path]) -> list[Path]:
    """The log folders of this project, its worktrees and its earlier paths, and single
    session logs with their subagents' folder."""
    found = log_folders() + [folder for p in projects for folder in log_folders(p)]
    for log in logs:
        found.append(log)
        found.append(log.with_suffix(""))  # <session>/subagents/*.jsonl
    return found


def _files(paths: list[Path]):
    for path in paths:
        if path.is_file():
            yield path
        elif path.is_dir():
            yield from sorted(path.rglob("*.jsonl"))


def _entries(paths: list[Path]):
    for log in _files(paths):
        with log.open(encoding="utf-8", errors="replace") as lines:
            for line in lines:
                try:
                    entry = json.loads(line)
                except ValueError:
                    continue
                if isinstance(entry, dict):
                    yield entry


def _responses(paths: list[Path]):
    """(timestamp, model, usage) per assistant response, each response once."""
    seen: set[tuple] = set()
    for entry in _entries(paths):
        message = entry.get("message")
        if not isinstance(message, dict) or message.get("role") != "assistant":
            continue
        usage = message.get("usage")
        if not isinstance(usage, dict):
            continue
        key = (message.get("id"), entry.get("requestId"))
        if key in seen:
            continue
        seen.add(key)
        yield entry.get("timestamp"), priced_as(message.get("model", "?"), usage), usage


def priced_as(model: str, usage: dict) -> str:
    """The price row a response is billed at: a long prompt has its own row on some models."""
    limit = LONG_PROMPT.get(model)
    if limit is None:
        return model
    prompt = sum(usage.get(KINDS[kind]) or 0 for kind in ("input", "cache_write", "cache_read"))
    return f"{model} (long prompt)" if prompt > limit else model


def _add(counts: collections.Counter, usage: dict) -> None:
    for kind, field in KINDS.items():
        counts[kind] += usage.get(field) or 0
    counts["responses"] += 1


def collect(paths: list[Path]) -> tuple[dict[str, collections.Counter], str | None, str | None]:
    totals: dict[str, collections.Counter] = collections.defaultdict(collections.Counter)
    first = last = None
    for stamp, model, usage in _responses(paths):
        _add(totals[model], usage)
        if stamp:
            first = min(first or stamp, stamp)
            last = max(last or stamp, stamp)
    return totals, first, last


def _moment(stamp: str) -> datetime.datetime:
    return datetime.datetime.fromisoformat(stamp.replace("Z", "+00:00"))


def _active_minutes(stamps: list[datetime.datetime]) -> int:
    moments = sorted(stamps)
    worked = sum(
        (later - earlier for earlier, later in zip(moments, moments[1:]) if later - earlier <= BREAK),
        datetime.timedelta(),
    )
    return round(worked.total_seconds() / 60)


def daily(paths: list[Path]) -> dict[str, dict]:
    """Per day (UTC): the active minutes over all sessions at once, and each model's tokens."""
    stamps: dict[str, list[datetime.datetime]] = collections.defaultdict(list)
    for entry in _entries(paths):
        stamp = entry.get("timestamp")
        if isinstance(stamp, str):
            stamps[stamp[:10]].append(_moment(stamp))
    models: dict[str, dict[str, collections.Counter]] = collections.defaultdict(
        lambda: collections.defaultdict(collections.Counter)
    )
    for stamp, model, usage in _responses(paths):
        if isinstance(stamp, str):
            _add(models[stamp[:10]][model], usage)
    return {
        day: {
            "active_minutes": _active_minutes(stamps[day]),
            "models": {
                model: {field: counts[field] for field in FIELDS}
                for model, counts in sorted(models[day].items())
            },
        }
        for day in sorted(stamps)
    }


def _responses_of(day: dict) -> int:
    return sum(counts.get("responses", 0) for counts in day["models"].values())


def record(device: str, paths: list[Path], records: Path = RECORDS) -> Path:
    """Writes this device's days into `records/<device>.json`. A day the logs hold now replaces
    the recorded one unless the record has more responses for it; days whose logs are gone stay."""
    if not DEVICE.fullmatch(device):
        raise ValueError(f"{device!r}: a short name of lowercase letters, digits and '-'")
    out = records / f"{device}.json"
    days = {}
    if out.exists():
        days = json.loads(out.read_text(encoding="utf-8")).get("days", {})
    for day, now in daily(paths).items():
        if day not in days or _responses_of(now) >= _responses_of(days[day]):
            days[day] = now
    data = {"device": device, "days": dict(sorted(days.items()))}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return out


def cost(model: str, counts: collections.Counter) -> float | None:
    prices = PRICES.get(model)
    if prices is None:
        return None
    return round(sum(counts[kind] * prices[kind] for kind in KINDS) / 1_000_000, 2)


def summary(records: Path = RECORDS) -> tuple[list[dict], dict]:
    """Every recorded device's hours, tokens, responses and API cost, and their sum. Models
    without a price are named in `unpriced`; their tokens count, their cost does not."""
    rows = []
    unpriced: set[str] = set()
    for path in sorted(records.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        minutes = tokens = responses = 0
        dollars = 0.0
        for day in data["days"].values():
            minutes += day["active_minutes"]
            for model, counts in day["models"].items():
                counter = collections.Counter(counts)
                tokens += sum(counter[kind] for kind in KINDS)
                responses += counter["responses"]
                price = cost(model, counter)
                if price is None:
                    unpriced.add(model)
                dollars += price or 0.0
        days = sorted(data["days"])
        rows.append(
            {
                "device": data["device"],
                "from": days[0] if days else None,
                "to": days[-1] if days else None,
                "hours": round(minutes / 60, 1),
                "tokens": tokens,
                "responses": responses,
                "cost": round(dollars, 2),
            }
        )
    total = {
        "hours": round(sum(row["hours"] for row in rows), 1),
        "cost": round(sum(row["cost"] for row in rows), 2),
        "tokens": sum(row["tokens"] for row in rows),
        "responses": sum(row["responses"] for row in rows),
        "unpriced": sorted(unpriced),
    }
    return rows, total


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--record", metavar="DEVICE", help="write this machine's days")
    parser.add_argument("--summary", action="store_true", help="add up every recorded device")
    parser.add_argument("--project", metavar="PATH", type=Path, action="append", default=[],
                        help="an earlier path of this project, whose logs count too")
    parser.add_argument("--log", metavar="FILE", type=Path, action="append", default=[],
                        help="one session's log started in another folder")
    args = parser.parse_args()
    paths = sources(args.project, args.log)
    if args.record:
        out = record(args.record, paths)
        days = json.loads(out.read_text(encoding="utf-8"))["days"]
        print(f"{out.relative_to(ROOT)}: {len(days)} days")
        return 0
    if args.summary:
        rows, total = summary()
        print("| Device | Days | Active time | Responses | Tokens | Cost (API, USD) |")
        print("|---|---|---:|---:|---:|---:|")
        for row in rows:
            print(
                f"| {row['device']} | {row['from']} to {row['to']} | {row['hours']:,} h | "
                f"{row['responses']:,} | {row['tokens'] / 1e6:,.0f} M | {row['cost']:,.2f} |"
            )
        print(
            f"| **Total** | | {total['hours']:,} h | {total['responses']:,} | "
            f"{total['tokens'] / 1e6:,.0f} M | {total['cost']:,.2f} |"
        )
        if total["unpriced"]:
            print(f"\nNo price for: {', '.join(total['unpriced'])} (add it to PRICES)")
        return 0
    totals, first, last = collect(paths)
    print(f"Sessions logged from {first} to {last}\n")
    print("| Model | Responses | Output tokens | Cache read | Cache written | Cost (API, USD) |")
    print("|---|---:|---:|---:|---:|---:|")
    total = 0.0
    for model, counts in sorted(totals.items(), key=lambda kv: -kv[1]["output"]):
        price = cost(model, counts)
        total += price or 0.0
        shown = f"{price:,.2f}" if price is not None else "no price"
        print(
            f"| {model} | {counts['responses']:,} | {counts['output']:,} | "
            f"{counts['cache_read']:,} | {counts['cache_write']:,} | {shown} |"
        )
    print(f"\nTotal: about {total:,.0f} USD at API prices")
    return 0


if __name__ == "__main__":
    sys.exit(main())

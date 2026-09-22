#!/usr/bin/env python3
"""Manage a plain-text project memory directory that survives a closed session.

The memory directory holds a small fixed set of Markdown files, each with one
job: project facts that rarely change, dated decisions with their reasoning,
current task state, open questions, and a dated append-only log. This tool reads
and writes those files so a later session rebuilds context without a human
retelling it.

Subcommands:
  init      create the memory directory and its files if they are missing
  log       append one dated entry to the append-only log
  decision  record a dated decision with its reasoning and any alternatives
  brief     print the session-start briefing in the fixed read order
  budget    report files over their line budget so they get compacted

Files and their default line budgets live in FILE_BUDGETS. A file over budget
is a prompt to summarise old detail, not to delete it.

Everything here uses the Python 3.8 standard library only. No secrets, tokens,
keys, or customer data belong in these files; this tool cannot enforce that, so
the caller must.

Exit codes:
  0  success
  1  a checked condition failed, such as a file over budget
  2  usage error

Usage:
  python3 memory.py init
  python3 memory.py init --dir project-memory
  python3 memory.py log "switched the cache to write-through"
  python3 memory.py decision "use SQLite for local runs" --why "no server to run in CI"
  python3 memory.py brief
  python3 memory.py budget
"""

from __future__ import annotations

import argparse
import datetime
import sys
from pathlib import Path

DEFAULT_DIR = "project-memory"

# Each file has one job and a line budget. Past the budget, old detail gets
# summarised into a shorter form rather than dropped.
FILE_BUDGETS = {
    "facts.md": 120,
    "decisions.md": 200,
    "state.md": 60,
    "questions.md": 80,
    "log.md": 300,
}

# The order a session reads at startup. Cheap context first, detail last.
READ_ORDER = ["state.md", "facts.md", "decisions.md", "questions.md", "log.md"]

FILE_HEADERS = {
    "facts.md": (
        "# Project facts\n\n"
        "Things that rarely change: what this project is, who uses it, the stack,\n"
        "the build and test commands, the deploy target. One fact per line. No\n"
        "secrets, tokens, keys, or customer data.\n"
    ),
    "decisions.md": (
        "# Decisions\n\n"
        "One decision per block, newest at the bottom, because entries are\n"
        "appended. Each carries a date, the choice, the reason, and the\n"
        "alternatives that were rejected. A decision is never edited in place; a\n"
        "reversal is a new dated block that names the one it overturns.\n"
    ),
    "state.md": (
        "# Current state\n\n"
        "What is in progress right now, the next concrete step, and anything\n"
        "half-done that a reader must not assume is finished. Overwrite this file\n"
        "freely; it holds the present, not the history.\n"
    ),
    "questions.md": (
        "# Open questions\n\n"
        "Unresolved questions and their current best guess. Remove a line when it\n"
        "is answered and record the answer as a fact or a decision.\n"
    ),
    "log.md": (
        "# Log\n\n"
        "Dated append-only entries, newest at the bottom. What happened and why,\n"
        "in one or two lines each. Never rewrite a past entry; correct it with a\n"
        "new dated entry.\n"
    ),
}


def today() -> str:
    """Return the current date as an ISO 8601 calendar date."""
    return datetime.date.today().isoformat()


def memory_dir(args: argparse.Namespace) -> Path:
    """Resolve the memory directory path from the parsed arguments."""
    return Path(args.dir)


def ensure_initialised(root: Path) -> list[str]:
    """Create the directory and any missing files, returning what was created."""
    created: list[str] = []
    if not root.exists():
        root.mkdir(parents=True)
        created.append(root.as_posix() + "/")
    for name, header in FILE_HEADERS.items():
        target = root / name
        if not target.exists():
            target.write_text(header, encoding="utf-8")
            created.append((root / name).as_posix())
    return created


def read_text(path: Path) -> str:
    """Read a file as UTF-8, returning an empty string when it is absent."""
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def append_block(path: Path, block: str) -> None:
    """Append a block to a file, keeping exactly one blank line before it."""
    existing = read_text(path)
    if existing and not existing.endswith("\n"):
        existing += "\n"
    if existing and not existing.endswith("\n\n"):
        existing += "\n"
    path.write_text(existing + block, encoding="utf-8")


def count_content_lines(text: str) -> int:
    """Count non-blank lines so blank spacing does not trip the budget."""
    return sum(1 for line in text.splitlines() if line.strip())


def cmd_init(args: argparse.Namespace) -> int:
    """Create the memory directory and its files if they are missing."""
    root = memory_dir(args)
    created = ensure_initialised(root)
    if created:
        print("created:")
        for item in created:
            print("  " + item)
    else:
        print("already initialised at " + root.as_posix())
    print("read order at session start: " + ", ".join(READ_ORDER))
    return 0


def cmd_log(args: argparse.Namespace) -> int:
    """Append one dated entry to the append-only log."""
    root = memory_dir(args)
    if not (root / "log.md").exists():
        print("not initialised, run: memory.py init", file=sys.stderr)
        return 2
    entry = "- %s %s" % (today(), args.message.strip())
    append_block(root / "log.md", entry + "\n")
    print("logged to " + (root / "log.md").as_posix())
    return 0


def cmd_decision(args: argparse.Namespace) -> int:
    """Record a dated decision block with its reasoning and alternatives."""
    root = memory_dir(args)
    path = root / "decisions.md"
    if not path.exists():
        print("not initialised, run: memory.py init", file=sys.stderr)
        return 2
    lines = ["## %s %s" % (today(), args.choice.strip())]
    if args.why:
        lines.append("Reason: " + args.why.strip())
    if args.instead_of:
        lines.append("Rejected: " + args.instead_of.strip())
    if args.replaces:
        lines.append("Replaces: " + args.replaces.strip())
    block = "\n".join(lines) + "\n"
    append_block(path, block)
    print("recorded decision in " + path.as_posix())
    return 0


def cmd_brief(args: argparse.Namespace) -> int:
    """Print the session-start briefing in the fixed read order."""
    root = memory_dir(args)
    if not root.exists():
        print("no memory at %s, run: memory.py init" % root.as_posix(), file=sys.stderr)
        return 2
    print("session briefing from " + root.as_posix())
    for name in READ_ORDER:
        path = root / name
        text = read_text(path)
        print("\n===== %s =====" % name)
        if text.strip():
            print(text.rstrip())
        else:
            print("(empty)")
    over = files_over_budget(root)
    if over:
        print("\nover budget, compact these before adding more:")
        for name, count, budget in over:
            print("  %s: %d content lines, budget %d" % (name, count, budget))
    return 0


def files_over_budget(root: Path) -> list:
    """Return files whose content line count is over their budget."""
    over = []
    for name, budget in FILE_BUDGETS.items():
        path = root / name
        if not path.exists():
            continue
        count = count_content_lines(read_text(path))
        if count > budget:
            over.append((name, count, budget))
    return over


def cmd_budget(args: argparse.Namespace) -> int:
    """Report files over their line budget so they get compacted."""
    root = memory_dir(args)
    if not root.exists():
        print("no memory at %s, run: memory.py init" % root.as_posix(), file=sys.stderr)
        return 2
    over = files_over_budget(root)
    if not over:
        print("all files within budget")
        return 0
    print("compact these; summarise old detail rather than deleting it:")
    for name, count, budget in over:
        print("  %s: %d content lines, budget %d" % (name, count, budget))
    return 1


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser with one subparser per command."""
    ap = argparse.ArgumentParser(
        prog="memory.py",
        description="Manage a plain-text project memory directory.")
    ap.add_argument("--dir", default=DEFAULT_DIR,
                    help="memory directory, default %s" % DEFAULT_DIR)
    sub = ap.add_subparsers(dest="command")

    p_init = sub.add_parser("init", help="create the memory directory and files")
    p_init.set_defaults(func=cmd_init)

    p_log = sub.add_parser("log", help="append one dated entry to the log")
    p_log.add_argument("message", help="what happened, in one or two lines")
    p_log.set_defaults(func=cmd_log)

    p_dec = sub.add_parser("decision", help="record a dated decision")
    p_dec.add_argument("choice", help="the decision made")
    p_dec.add_argument("--why", default="", help="the reason for it")
    p_dec.add_argument("--instead-of", default="", dest="instead_of",
                       help="the alternatives rejected")
    p_dec.add_argument("--replaces", default="",
                       help="the earlier decision this overturns")
    p_dec.set_defaults(func=cmd_decision)

    p_brief = sub.add_parser("brief", help="print the session-start briefing")
    p_brief.set_defaults(func=cmd_brief)

    p_budget = sub.add_parser("budget", help="report files over budget")
    p_budget.set_defaults(func=cmd_budget)
    return ap


def main(argv: list) -> int:
    """Parse arguments and dispatch to the chosen subcommand."""
    parser = build_parser()
    args = parser.parse_args(argv)
    if not getattr(args, "command", None):
        parser.print_help()
        return 2
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

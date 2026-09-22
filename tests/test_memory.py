#!/usr/bin/env python3
"""Tests for the project memory tool in memory-keeper.

Drives the tool through its real subcommands in a temporary directory: init
creates the fixed set of files, log appends a dated line, decision writes a
dated block with its reasoning, brief prints what was written, and budget
reports a file that is over its line limit. Nothing is written inside the
repository tree, and the temporary directory is removed even when a check fails.

Run with: python3 tests/test_memory.py
"""

from __future__ import annotations

import contextlib
import datetime
import importlib.util
import io
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "memory-keeper" / "scripts" / "memory.py"

spec = importlib.util.spec_from_file_location("memory", SCRIPT)
assert spec and spec.loader, "cannot load memory tool at %s" % SCRIPT
memory = importlib.util.module_from_spec(spec)
sys.modules["memory"] = memory
spec.loader.exec_module(memory)

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if condition:
        print("  pass  %s" % message)
    else:
        print("  FAIL  %s" % message)
        failures.append(message)


def run(mem_dir: Path, *args: str) -> int:
    return memory.main(["--dir", str(mem_dir)] + list(args))


tmp = Path(tempfile.mkdtemp(prefix="memtest-"))
today = datetime.date.today().isoformat()
try:
    mem = tmp / "project-memory"

    print("init")
    rc = run(mem, "init")
    check(rc == 0, "init exits cleanly")
    expected = ["facts.md", "decisions.md", "state.md", "questions.md", "log.md"]
    check(all((mem / name).is_file() for name in expected),
          "init creates every expected file")

    print("\nlog")
    rc = run(mem, "log", "switched the cache to write-through")
    check(rc == 0, "log exits cleanly")
    log_text = (mem / "log.md").read_text(encoding="utf-8")
    check(("- %s switched the cache to write-through" % today) in log_text,
          "log writes a dated line with the message")

    print("\ndecision")
    rc = run(mem, "decision", "use SQLite for local runs",
             "--why", "no server to run in CI")
    check(rc == 0, "decision exits cleanly")
    dec_text = (mem / "decisions.md").read_text(encoding="utf-8")
    check(("## %s use SQLite for local runs" % today) in dec_text,
          "decision writes a dated heading block")
    check("Reason: no server to run in CI" in dec_text,
          "decision records the reasoning")

    print("\nbrief")
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        rc = run(mem, "brief")
    brief_out = buf.getvalue()
    check(rc == 0, "brief exits cleanly")
    check("switched the cache to write-through" in brief_out,
          "the logged entry appears in the briefing output")
    check("use SQLite for local runs" in brief_out,
          "the decision appears in the briefing output")

    print("\nbudget")
    budget = memory.FILE_BUDGETS["state.md"]
    fat = "\n".join("line %d" % n for n in range(budget + 5)) + "\n"
    (mem / "state.md").write_text(fat, encoding="utf-8")
    rc = run(mem, "budget")
    check(rc == 1, "budget exits 1 when a file is over its limit")
    over = memory.files_over_budget(mem)
    check(any(name == "state.md" for name, _c, _b in over),
          "the oversized file is reported as over budget")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

print("\n%d check(s) failed" % len(failures))
sys.exit(1 if failures else 0)

#!/usr/bin/env python3
"""Tests for the ai_tells detector.

Two guarantees are checked. The detector finds the patterns it claims to find in a
deliberately machine flavoured fixture, and it stays quiet on plain human prose.
The second half matters more than the first, because a linter with false positives
gets switched off.

Run with: python3 tests/test_ai_tells.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DETECTOR = ROOT / "skills" / "human-prose" / "scripts" / "ai_tells.py"
FIXTURES = ROOT / "tests" / "fixtures"

spec = importlib.util.spec_from_file_location("ai_tells", DETECTOR)
assert spec and spec.loader, "cannot load detector at %s" % DETECTOR
ai_tells = importlib.util.module_from_spec(spec)
# Register before executing, otherwise dataclass resolution fails on Python 3.9.
sys.modules["ai_tells"] = ai_tells
spec.loader.exec_module(ai_tells)

# Rules the machine flavoured fixture must trigger.
MUST_FIND = {
    "artifact",
    "placeholder",
    "chatter",
    "cutoff-disclaimer",
    "em-dash",
    "curly-quote",
    "emoji",
    "thematic-break",
    "title-case-heading",
    "x-and-y-heading",
    "bold-label-list",
    "vocab",
    "vocab-density",
    "vague-attribution",
    "section-summary",
    "negative-parallelism",
    "participle-tail",
    "rule-of-three",
    "copula-avoidance",
}

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if condition:
        print("  pass  %s" % message)
    else:
        print("  FAIL  %s" % message)
        failures.append(message)


def rules_for(path: Path) -> set[str]:
    findings = ai_tells.scan(str(path), path.read_text(encoding="utf-8"))
    return {f.rule for f in findings}


print("detecting tells in machine_sample.md")
found = rules_for(FIXTURES / "machine_sample.md")
for rule in sorted(MUST_FIND):
    check(rule in found, "detects %s" % rule)

print("\nstaying quiet on clean_sample.md")
clean = rules_for(FIXTURES / "clean_sample.md")
check(clean == set(), "no findings on human prose, got %s" % (sorted(clean) or "none"))

print("\nexemption parsing")
ex = ai_tells.parse_exemptions(["<!-- lint-exempt: vocab,chatter -->", "# Title"])
check(ex == {"vocab", "chatter"}, "parses a two rule exemption, got %s" % sorted(ex))
ex2 = ai_tells.parse_exemptions(["<!-- lint-vocab-exempt -->"])
check(ex2 == {"vocab", "vocab-density"}, "legacy vocab marker still works")
ex3 = ai_tells.parse_exemptions(["# Title", "no marker here"])
check(ex3 == set(), "no marker means no exemption")
ex4 = ai_tells.parse_exemptions(["<!-- lint-exempt: not-a-real-rule -->"])
check(ex4 == set(), "unknown rule names are ignored rather than trusted")

print("\nexemptions actually suppress findings")
suppressed = ai_tells.scan("x.md", "<!-- lint-exempt: em-dash -->\n\nA sentence \u2014 with a dash.\n")
check(not any(f.rule == "em-dash" for f in suppressed), "declared exemption suppresses its rule")
not_suppressed = ai_tells.scan("x.md", "A sentence \u2014 with a dash.\n")
check(any(f.rule == "em-dash" for f in not_suppressed), "undeclared em dash is still reported")

print("\ncode fences are not linted for style")
fenced = ai_tells.scan("x.md", "Text.\n\n```\nnot just a, but b \u2014 really\n```\n")
check(not any(f.rule == "em-dash" for f in fenced), "em dash inside a code fence is ignored")

print("\nfrontmatter is not linted for style")
fm = ai_tells.scan("x.md", "---\ntitle: A Thing \u2014 With Dash\n---\n\nBody text.\n")
check(not any(f.rule == "em-dash" for f in fm), "em dash inside frontmatter is ignored")

print("\n%d check(s) failed" % len(failures))
sys.exit(1 if failures else 0)

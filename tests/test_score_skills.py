#!/usr/bin/env python3
"""Tests for the rubric scorer in tools/score_skills.py.

Each rubric criterion is exercised by building a synthetic skill on disk that is
correct in every way except one, then asserting that the one broken criterion is
the one that loses its point. A fully correct synthetic skill has to score ten,
otherwise the negative cases prove nothing.

The scorer reads a module level SKILLS_DIR, so the tests point that constant at a
temporary tree and never touch the real skills directory.

Run with: python3 tests/test_score_skills.py
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools" / "score_skills.py"

spec = importlib.util.spec_from_file_location("score_skills", SCRIPT)
assert spec and spec.loader, "cannot load scorer at %s" % SCRIPT
score_skills = importlib.util.module_from_spec(spec)
sys.modules["score_skills"] = score_skills
spec.loader.exec_module(score_skills)

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if condition:
        print("  pass  %s" % message)
    else:
        print("  FAIL  %s" % message)
        failures.append(message)


TRIGGERS = ", ".join("t%02d" % n for n in range(12))
DESCRIPTION = (
    "A skill for the test suite. Use this when you need a deterministic fixture "
    "that scores the full ten points so the negative cases mean something real. "
    "Triggers on %s." % TRIGGERS
)

FRONT = (
    "---\n"
    "name: %(name)s\n"
    "description: %(desc)s\n"
    "license: Apache-2.0\n"
    "metadata:\n"
    "  version: \"1.0.0\"\n"
    "  suite: test-suite\n"
    "%(extra)s"
    "---\n"
)

BODY_PARTS = [
    "# Sample skill\n\nA long enough body so the spec check is happy. " * 30,
    "\n\n## Fit to the project\n\n"
    "Read the project layout first.\n"
    "Match the existing tools and their conventions.\n"
    "Never assume a stack that the repository does not already use.\n",
    "\n\n## Procedure\n\n"
    "### Step 1 Read\n\nRead the target.\n\n"
    "### Step 2 Plan\n\nPlan the change.\n\n"
    "### Step 3 Apply\n\nApply the change.\n\n"
    "### Step 4 Verify\n\nVerify the change.\n",
    "\n\n## Non-negotiables\n\n"
    "1. First rule that overrides the rest of the file.\n"
    "2. Second rule.\n"
    "3. Third rule.\n"
    "4. Fourth rule.\n",
    "\n\n## Self-audit\n\n"
    "- First item.\n- Second item.\n- Third item.\n"
    "- Fourth item.\n- Fifth item.\n- Sixth item.\n",
    "\n\n## Off switch\n\n"
    "There is an off switch. When the user says \"stop\", stand down for the "
    "rest of the session.\n",
    "\n\n## Honest limits\n\n"
    "This does not read minds.\n"
    "It cannot promise a stack it never saw.\n",
    "\n\n## References\n\n"
    "See references/one.md and references/two.md for detail.\n",
]


def build_skill(folder: Path, front_extra: str = "", body_edit=None) -> None:
    body = "".join(BODY_PARTS)
    if body_edit is not None:
        body = body_edit(body)
    front = FRONT % {"name": folder.name, "desc": DESCRIPTION, "extra": front_extra}
    folder.mkdir(parents=True, exist_ok=True)
    (folder / "SKILL.md").write_text(front + "\n" + body, encoding="utf-8")
    refs = folder / "references"
    refs.mkdir(exist_ok=True)
    (refs / "one.md").write_text("# One\n\nReference one.\n", encoding="utf-8")
    (refs / "two.md").write_text("# Two\n\nReference two.\n", encoding="utf-8")


def score_of(root: Path, name: str) -> dict:
    score_skills.SKILLS_DIR = root
    score_skills.ROOT = root
    # The style detector is exercised by tests/test_ai_tells.py. Here it is left
    # out (check_style treats a missing detector as no findings) so this test
    # stays independent of the detector module loading.
    return score_skills.score_skill(root / name, None)


def lost(root: Path, name: str, criterion: str) -> bool:
    result = score_of(root, name)
    return criterion in result["failures"]


with tempfile.TemporaryDirectory() as tmp:
    root = Path(tmp)

    print("a fully correct synthetic skill")
    build_skill(root / "good-skill")
    result = score_of(root, "good-skill")
    check(result["score"] == 10,
          "scores 10, failures %s" % (result["failures"] or "none"))

    print("\nuniversality")
    build_skill(root / "no-fit",
                body_edit=lambda b: b.replace("## Fit to the project",
                                              "## Something else"))
    check(lost(root, "no-fit", "universality"),
          "missing 'Fit to the project' loses universality")
    build_skill(root / "host-path",
                body_edit=lambda b: b + "\n\nRun it in C:\\Users\\me\\proj.\n")
    check(lost(root, "host-path", "universality"),
          "a drive letter host path loses universality")
    build_skill(root / "unix-host",
                body_edit=lambda b: b + "\n\nOpen /Users/alice/notes.\n")
    check(lost(root, "unix-host", "universality"),
          "a /Users/ host path loses universality")

    print("\nactivation")
    short_desc = "Too short. Use this when testing. Triggers on a, b, c."
    build_skill(root / "short-desc",
                front_extra="")
    (root / "short-desc" / "SKILL.md").write_text(
        (FRONT % {"name": "short-desc", "desc": short_desc, "extra": ""})
        + "\n" + "".join(BODY_PARTS), encoding="utf-8")
    check(lost(root, "short-desc", "activation"),
          "a description under 200 characters loses activation")
    no_trig = (DESCRIPTION.split(" Triggers on")[0]) + " No trigger list here at all."
    (root / "short-desc" / "SKILL.md").write_text(
        (FRONT % {"name": "short-desc", "desc": no_trig, "extra": ""})
        + "\n" + "".join(BODY_PARTS), encoding="utf-8")
    check(lost(root, "short-desc", "activation"),
          "a description without 'Triggers on' loses activation")
    few = "A skill. Use this when testing the fixture path carefully and slowly " \
          "so the length is above two hundred characters for sure and certain " \
          "here. Triggers on a, b, c, d, e."
    (root / "short-desc" / "SKILL.md").write_text(
        (FRONT % {"name": "short-desc", "desc": few, "extra": ""})
        + "\n" + "".join(BODY_PARTS), encoding="utf-8")
    check(lost(root, "short-desc", "activation"),
          "fewer than ten trigger phrases loses activation")

    print("\nnon-negotiables")
    build_skill(root / "three-rules",
                body_edit=lambda b: b.replace("4. Fourth rule.\n", ""))
    check(lost(root, "three-rules", "non-negotiables"),
          "three numbered rules loses non-negotiables")
    build_skill(root / "four-rules")
    check(not lost(root, "four-rules", "non-negotiables"),
          "four numbered rules passes non-negotiables")

    print("\nself-audit")
    six = ("\n\n## Self-audit\n\n- First item.\n- Second item.\n- Third item.\n"
           "- Fourth item.\n- Fifth item.\n- Sixth item.\n")
    five = ("\n\n## Self-audit\n\n- First item.\n- Second item.\n- Third item.\n"
            "- Fourth item.\n- Fifth item.\n")
    build_skill(root / "five-audit",
                body_edit=lambda b: b.replace(six, five))
    check(lost(root, "five-audit", "self-audit"),
          "five audit bullets loses self-audit")
    build_skill(root / "six-audit")
    check(not lost(root, "six-audit", "self-audit"),
          "six audit bullets passes self-audit")

    print("\noff switch")
    build_skill(root / "no-stop",
                body_edit=lambda b: b.replace('says "stop", stand down',
                                              "is done, stand down"))
    check(lost(root, "no-stop", "off-switch"),
          "no quoted stop phrase loses the off switch")

    print("\nreferences")
    one_ref = root / "one-ref"
    build_skill(one_ref)
    (one_ref / "references" / "two.md").unlink()
    (one_ref / "SKILL.md").write_text(
        (one_ref / "SKILL.md").read_text(encoding="utf-8")
        .replace("references/one.md and references/two.md", "references/one.md"),
        encoding="utf-8")
    check(lost(root, "one-ref", "references"),
          "fewer than two reference files loses references")
    orphan = root / "orphan-ref"
    build_skill(orphan)
    (orphan / "SKILL.md").write_text(
        (orphan / "SKILL.md").read_text(encoding="utf-8")
        .replace("references/one.md and references/two.md", "references/one.md"),
        encoding="utf-8")
    check(lost(root, "orphan-ref", "references"),
          "an unmentioned reference file loses references")

    print("\nstyle")
    coded = root / "coded-skill"
    build_skill(coded, front_extra="  emits_code: true\n")
    check(lost(root, "coded-skill", "style"),
          "emits_code true without a code-craft mention loses style")

print("\n%d check(s) failed" % len(failures))
sys.exit(1 if failures else 0)

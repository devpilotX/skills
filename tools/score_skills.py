#!/usr/bin/env python3
"""Score every skill against the ten point rubric in RUBRIC.md.

A skill scores one point per criterion and needs all ten to ship. The point of
computing the score is that nobody has to take the number on trust: each
criterion is a mechanical check with a named reason when it fails.

The ten criteria:
  spec            frontmatter and naming follow the skill specification
  activation      the description says when to use it and lists trigger phrases
  universality    a fit-to-the-project step, and no host specific paths
  procedure       an ordered procedure of at least four steps
  non-negotiables at least four rules that override the rest of the file
  self-audit      at least six checkable items to run before delivering
  off-switch      an explicit instruction to stand down when told to
  honest-limits   a section saying what the skill does not do
  references      at least two reference files, linked in both directions
  style           no style detector findings, plus a code contract where code
                  is produced

Usage:
  python3 tools/score_skills.py
  python3 tools/score_skills.py --skill seo-optimize
  python3 tools/score_skills.py --json
  python3 tools/score_skills.py --min 10
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
DETECTOR = SKILLS_DIR / "human-prose" / "scripts" / "ai_tells.py"

MAX_SCORE = 10

CRITERIA = (
    "spec",
    "activation",
    "universality",
    "procedure",
    "non-negotiables",
    "self-audit",
    "off-switch",
    "honest-limits",
    "references",
    "style",
)

NAME_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")
NAME_MAX = 64
DESCRIPTION_MIN = 200
DESCRIPTION_MAX = 1024

# A skill has to work on a project it has never seen, so it may not assume a
# machine, a home directory, or a drive letter.
HOST_PATH_RE = re.compile(
    r"(?<![A-Za-z0-9])(?:[A-Za-z]:[\\/]{1,2}(?:Users|Documents|Desktop)"
    r"|/Users/[a-z]|/home/[a-z]|~/Desktop|~/Documents)",
    re.I,
)

# Sole vendor mandates break universality. A skill may recommend a tool; it may
# not require one as the only way through.
VENDOR_MANDATE_RE = re.compile(
    r"\b(?:you must use|always use|only works with|requires you to use)\s+"
    r"(?:npm|yarn|pnpm|pip|poetry|maven|gradle|cargo|docker|kubernetes|aws|"
    r"gcp|azure|react|vue|angular|django|rails|spring|next\.js|postgres|mysql)\b",
    re.I,
)

STEP_RE = re.compile(r"^#{3,4}\s+(?:Step|Phase|Gate|Pass|Round)\s+\d+", re.M)
PROCEDURE_HEADING_RE = re.compile(
    r"^##\s+(?:Procedure|Protocol|Method|Workflow|The procedure|The protocol)\b",
    re.M | re.I,
)
FIT_HEADING_RE = re.compile(r"^##\s+Fit to the project\s*$", re.M)
NONNEG_HEADING_RE = re.compile(r"^##\s+Non-negotiables\s*$", re.M)
AUDIT_HEADING_RE = re.compile(r"^##\s+Self-audit\s*$", re.M)
LIMITS_HEADING_RE = re.compile(r"^##\s+Honest limits\s*$", re.M)

OFF_SWITCH_RE = re.compile(
    r"(?i)\b(?:off switch|stand down|stays? off for the rest of the session)\b"
)
OFF_SWITCH_QUOTE_RE = re.compile(
    r'"(?:stop|stop it|I\'ve decided|I have decided|just execute|just do it|'
    r'skip the [a-z -]+)"'
)

PATH_MENTION_RE = re.compile(r"(?:references|scripts)/[A-Za-z0-9_./-]+\.(?:md|py|sh)")
EMITS_CODE_RE = re.compile(r"^\s*emits_code:\s*true\s*$", re.M | re.I)
CODE_CRAFT_RE = re.compile(r"`code-craft`")


def load_detector():
    """Import the style detector that human-prose ships, without installing it."""
    spec = importlib.util.spec_from_file_location("ai_tells", DETECTOR)
    if not (spec and spec.loader):
        return None
    module = importlib.util.module_from_spec(spec)
    sys.modules["ai_tells"] = module
    spec.loader.exec_module(module)
    return module


def split_frontmatter(text: str) -> tuple[str, str]:
    """Return the frontmatter block and the body, or two empty strings."""
    if not text.startswith("---\n"):
        return "", ""
    end = text.find("\n---", 4)
    if end == -1:
        return "", ""
    return text[4:end], text[end + 4:]


def parse_frontmatter(block: str) -> dict:
    """Read top level keys and keep nested lines under the parent key."""
    meta: dict = {}
    nested: dict = {}
    current = None
    for raw in block.split("\n"):
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw[0] in " \t":
            if current:
                nested.setdefault(current, []).append(raw.strip())
            continue
        if ":" not in raw:
            continue
        key, _, value = raw.partition(":")
        current = key.strip()
        meta[current] = value.strip()
    meta["_nested"] = nested
    return meta


def section_body(text: str, heading_re: re.Pattern) -> str:
    """Return the lines of a section, stopping at the next level two heading."""
    match = heading_re.search(text)
    if not match:
        return ""
    rest = text[match.end():]
    nxt = re.search(r"^##\s+", rest, re.M)
    return rest[: nxt.start()] if nxt else rest


def count_numbered(block: str) -> int:
    return len(re.findall(r"^\s*\d+\.\s+\S", block, re.M))


def count_bullets(block: str) -> int:
    return len(re.findall(r"^\s*[-*]\s+\S", block, re.M))


def content_lines(block: str) -> int:
    return len([ln for ln in block.split("\n") if ln.strip()])


def check_spec(folder: str, meta: dict, body: str) -> list[str]:
    problems = []
    name = meta.get("name", "")
    if not name:
        problems.append("no name in frontmatter")
    elif name != folder:
        problems.append("name %r does not match folder %r" % (name, folder))
    elif not NAME_RE.match(name):
        problems.append("name %r is not lowercase kebab case" % name)
    elif len(name) > NAME_MAX:
        problems.append("name exceeds %d characters" % NAME_MAX)

    desc = meta.get("description", "")
    if not desc:
        problems.append("no description, so the skill cannot auto activate")
    else:
        if len(desc) < DESCRIPTION_MIN:
            problems.append(
                "description is %d characters, needs at least %d to activate reliably"
                % (len(desc), DESCRIPTION_MIN)
            )
        if len(desc) > DESCRIPTION_MAX:
            problems.append(
                "description is %d characters, limit is %d" % (len(desc), DESCRIPTION_MAX)
            )
        if meta.get("_nested", {}).get("description"):
            problems.append("description spans several lines, keep it on one")

    if not meta.get("license"):
        problems.append("no license field")

    nested = meta.get("_nested", {}).get("metadata", [])
    joined = " ".join(nested)
    version = re.search(r"version:\s*\"?([0-9.]+)\"?", joined)
    if not version:
        problems.append("metadata has no version")
    elif not SEMVER_RE.match(version.group(1)):
        problems.append("version %r is not semver" % version.group(1))
    if "suite:" not in joined:
        problems.append("metadata has no suite")

    if len(body.strip()) < 1500:
        problems.append("body is %d characters, too thin to act on" % len(body.strip()))
    return problems


def check_activation(meta: dict) -> list[str]:
    desc = meta.get("description", "")
    problems = []
    if not re.search(r"(?i)\buse (this )?when\b", desc):
        problems.append("description never says when to use the skill")
    trigger = re.search(r"(?i)triggers on\b(.*)$", desc)
    if not trigger:
        problems.append("description lists no explicit trigger phrases")
    else:
        terms = [t.strip() for t in trigger.group(1).split(",") if t.strip()]
        if len(terms) < 10:
            problems.append("only %d trigger phrases, needs 10" % len(terms))
    return problems


def check_universality(body: str) -> list[str]:
    problems = []
    fit = section_body(body, FIT_HEADING_RE)
    if not fit:
        problems.append("no 'Fit to the project' section, so it assumes a stack")
    elif content_lines(fit) < 3:
        problems.append("'Fit to the project' section is a stub")
    host = HOST_PATH_RE.search(body)
    if host:
        problems.append("hardcoded host path %r" % host.group(0))
    vendor = VENDOR_MANDATE_RE.search(body)
    if vendor:
        problems.append("mandates a single vendor: %r" % vendor.group(0))
    return problems


def check_procedure(body: str) -> list[str]:
    steps = len(STEP_RE.findall(body))
    if steps >= 4:
        return []
    if PROCEDURE_HEADING_RE.search(body):
        block = section_body(body, PROCEDURE_HEADING_RE)
        if count_numbered(block) >= 4:
            return []
    return ["only %d ordered steps found, needs 4" % steps]


def check_nonnegotiables(body: str) -> list[str]:
    block = section_body(body, NONNEG_HEADING_RE)
    if not block:
        return ["no 'Non-negotiables' section"]
    found = count_numbered(block)
    if found < 4:
        return ["'Non-negotiables' has %d rules, needs 4" % found]
    return []


def check_self_audit(body: str) -> list[str]:
    block = section_body(body, AUDIT_HEADING_RE)
    if not block:
        return ["no 'Self-audit' section"]
    found = count_bullets(block)
    if found < 6:
        return ["'Self-audit' has %d items, needs 6" % found]
    return []


def check_off_switch(body: str) -> list[str]:
    problems = []
    if not OFF_SWITCH_RE.search(body):
        problems.append("no off switch, so the skill cannot be told to stand down")
    if not OFF_SWITCH_QUOTE_RE.search(body):
        problems.append("no quoted stop phrase the user can actually say")
    return problems


def check_honest_limits(body: str) -> list[str]:
    block = section_body(body, LIMITS_HEADING_RE)
    if not block:
        return ["no 'Honest limits' section"]
    if content_lines(block) < 2:
        return ["'Honest limits' section is a stub"]
    return []


def check_references(skill_dir: Path) -> list[str]:
    problems = []
    ref_dir = skill_dir / "references"
    present = set()
    if ref_dir.is_dir():
        for item in sorted(ref_dir.rglob("*")):
            if item.is_file() and not item.name.startswith("."):
                present.add("references/%s" % item.relative_to(ref_dir).as_posix())
    if len(present) < 2:
        problems.append("%d reference files, needs 2" % len(present))

    mentioned = set()
    for md in sorted(skill_dir.rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        for hit in PATH_MENTION_RE.findall(text):
            mentioned.add(hit)
            if not (skill_dir / hit).is_file():
                problems.append("mentions %s which is missing" % hit)
    for orphan in sorted(present - mentioned):
        problems.append("%s is never mentioned, so it will never load" % orphan)
    return problems


def check_style(skill_dir: Path, detector, body: str, frontmatter: str) -> list[str]:
    problems = []
    if detector:
        for md in sorted(skill_dir.rglob("*.md")):
            findings = detector.scan(
                md.relative_to(ROOT).as_posix(), md.read_text(encoding="utf-8")
            )
            for finding in findings:
                problems.append(
                    "%s:%d [%s] %s"
                    % (
                        md.relative_to(skill_dir).as_posix(),
                        finding.line,
                        finding.rule,
                        finding.detail,
                    )
                )
    if EMITS_CODE_RE.search(frontmatter) and not CODE_CRAFT_RE.search(body):
        problems.append("produces code but never points at the code-craft contract")
    return problems


def score_skill(skill_dir: Path, detector) -> dict:
    """Run all ten checks and return the score with a reason for every loss."""
    skill_md = skill_dir / "SKILL.md"
    result = {"name": skill_dir.name, "score": 0, "failures": {}}
    if not skill_md.is_file():
        result["failures"] = {c: ["no SKILL.md"] for c in CRITERIA}
        return result

    text = skill_md.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)
    meta = parse_frontmatter(frontmatter)

    outcome = {
        "spec": check_spec(skill_dir.name, meta, body),
        "activation": check_activation(meta),
        "universality": check_universality(body),
        "procedure": check_procedure(body),
        "non-negotiables": check_nonnegotiables(body),
        "self-audit": check_self_audit(body),
        "off-switch": check_off_switch(body),
        "honest-limits": check_honest_limits(body),
        "references": check_references(skill_dir),
        "style": check_style(skill_dir, detector, body, frontmatter),
    }
    result["failures"] = {k: v for k, v in outcome.items() if v}
    result["score"] = sum(1 for c in CRITERIA if not outcome[c])
    return result


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="score_skills.py")
    ap.add_argument("--skill", help="score one skill by folder name")
    ap.add_argument("--json", action="store_true", help="machine readable output")
    ap.add_argument("--min", type=int, default=MAX_SCORE,
                    help="exit non-zero below this score, default 10")
    ap.add_argument("--quiet", action="store_true", help="print only the summary")
    args = ap.parse_args(argv)

    if not SKILLS_DIR.is_dir():
        print("no skills directory at %s" % SKILLS_DIR, file=sys.stderr)
        return 2

    dirs = sorted(d for d in SKILLS_DIR.iterdir() if d.is_dir())
    if args.skill:
        dirs = [d for d in dirs if d.name == args.skill]
        if not dirs:
            print("no skill named %r" % args.skill, file=sys.stderr)
            return 2

    detector = load_detector()
    results = [score_skill(d, detector) for d in dirs]

    if args.json:
        print(json.dumps(results, indent=2, sort_keys=True))
        below = [r for r in results if r["score"] < args.min]
        return 1 if below else 0

    for r in results:
        mark = "ok  " if r["score"] == MAX_SCORE else "FAIL"
        if not args.quiet or r["score"] < MAX_SCORE:
            print("%s %2d/%d  %s" % (mark, r["score"], MAX_SCORE, r["name"]))
        for criterion in CRITERIA:
            for reason in r["failures"].get(criterion, []):
                print("       - %s: %s" % (criterion, reason))

    below = [r for r in results if r["score"] < args.min]
    total = sum(r["score"] for r in results)
    average = total / len(results) if results else 0.0
    print(
        "\n%d skill(s), average %.2f/%d, %d below %d"
        % (len(results), average, MAX_SCORE, len(below), args.min)
    )
    return 1 if below else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

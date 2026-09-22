# Contributing

## Before you open a pull request

```
python3 tools/score_skills.py
python3 tools/validate_skills.py
python3 skills/code-craft/scripts/structure_scan.py skills tools tests --ext py
python3 tests/test_ai_tells.py
python3 tests/test_md2doc.py
python3 tests/test_score_skills.py
python3 tests/test_structure_scan.py
python3 tests/test_memory.py
```

All eight have to pass. CI runs the same commands on Python 3.9 and 3.13, so a local failure is a
guaranteed CI failure.

The scorer is the one to run first. It reports the ten point rubric per skill and names the criterion
and the reason for any point lost, which is faster than reading [RUBRIC.md](RUBRIC.md) and guessing.

## Layout of a skill

```
skills/<name>/
  SKILL.md          required
  references/*.md   required, at least two
  scripts/*.py      optional, for work that should be deterministic
```

The folder name and the `name` field in the frontmatter have to match. Lowercase letters, digits, and
single hyphens.

## Frontmatter

```
---
name: my-skill
description: One line. This is what decides whether the skill activates, so it must be specific and carry the words a user would actually type. Between 200 and 1024 characters, containing the words "Use when" and then "Triggers on" followed by at least ten comma separated phrases.
license: MIT
compatibility: One line saying what it needs. Most skills need nothing.
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---
```

The description is the only thing loaded at startup, so it does the whole job of matching a request.
Write it with the phrases a user would really use, including the awkward ones. A vague description means
the skill never fires, which is the most common reason a skill appears not to work.

Set `emits_code: true` when the skill produces source code, markup, or configuration. The scorer then
requires the body to point at the `code-craft` contract, so generated code arrives organised and
commented instead of arriving as one long block.

## What a SKILL.md has to contain

[RUBRIC.md](RUBRIC.md) has the full ten criteria and how each one is checked. The headings are matched
literally, so spell them exactly:

`## Fit to the project` with at least three lines on what to read and detect in the host project before
acting. This is the criterion that fails most often on a first draft, because it is the easiest to skip
while writing confidently about the stack you happen to have in mind.

`## Non-negotiables` with at least four numbered rules that override the rest of the file, each naming
what breaks when it gets ignored.

A procedure of at least four ordered steps, written as `### Step 1,` onwards. Phases and gates count.

`## Self-audit` with at least six items, each answerable yes or no by looking at the output.

`## Honest limits` with at least two lines on what the skill does not do, and which neighbouring skill
owns the part it cannot.

An off switch with a quoted phrase the user can say. A skill that cannot be told to stop becomes
nagging, and nagging gets the whole collection uninstalled.

Open with the failure the skill corrects, in two or three sentences. Not a description of the topic.

Push anything long into `references/`. Split by when the reader needs it, not by subject: the main file
holds what applies every time, a reference holds the lookup table, the worked example, or the domain
checklist. Keeping the main file short is what makes it get read.

## Rules that apply to every skill in this suite

No fabrication. Numbers are retrieved and cited, or labelled as assumptions with their reasoning.

No manufactured criticism. A clean result gets a short report saying it is clean.

No invented scores. A count of specific defects is honest. A rating out of ten is not.

Consequence over effort when ranking anything.

State what was not covered rather than implying completeness.

Say when a question needs a licensed professional, and give the exact question to ask them.

Work on any project. No absolute paths, no home directories, no drive letters, and no sentence that
makes one vendor or framework the only way through.

## House style

[STYLE.md](STYLE.md) is enforced, not advisory. The short version: no em dashes, straight quotes only,
no emoji, sentence case headings, plain copulas, no significance padding, no closing summary, and no
overrepresented vocabulary.

Do not repeat a sentence from another skill. Fifty eight files carrying the same stock phrasing is the
clearest possible signal that a template was filled in, which defeats the point of the collection.

A file that has to enumerate banned patterns declares per rule exemptions on one of its first twenty
lines:

```
<!-- lint-exempt: vocab,chatter -->
```

Exemptions appear in every lint report, so run the detector and read the list rather than trusting a
count written in prose. Use the fewest rules you can, and only in files whose purpose is documenting the
patterns. A file that opts out of a rule it does not actually trip will be asked to narrow it.

## References have to be reachable

The validator fails if a file in `references/` or `scripts/` is never mentioned, because an unmentioned
file never gets loaded. It also fails if prose mentions a path that does not exist. Mention each file by
its relative path in prose or in a usage example.

## Scripts

No third party packages. These have to run in a clean environment, which is most of their value.

Target Python 3.9, since that is the oldest version CI covers. Use `from __future__ import annotations`
so newer annotation syntax stays readable without breaking the floor.

Module docstring explaining the usage, a `main` function, and meaningful exit codes.

Stay inside the budgets in `skills/code-craft/references/budgets.md`, which CI enforces over `skills/`,
`tools/` and `tests/`. Going over is allowed when splitting would need a name that does not exist in the
domain, and then the reason belongs in the pull request.

If a script makes a claim, add a test for it under `tests/`. Match the shape of the existing test files:
standard library only, one printed line per check, and a final count of failures.

## Adding a skill to the list

Add a row to the right table in the README. The validator checks that every skill appears there and that
the README does not reference a skill that was removed.

## Commit messages

Imperative mood, lowercase, no trailing full stop. Say what changed and why when the why is not obvious.

```
add working capital cycle to business-model
fix autolink consuming trailing punctuation
tighten participle-tail rule to cut false positives on noun lists
```

No generated attribution trailers.

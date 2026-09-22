# Scoring workflow

The three checks that gate a skill, what each one catches, and how to read their output. Run them from the repository root. Where these examples show `python3`, use whatever launches Python 3.8 or newer on your system.

## The three checks

The scorer computes the ten-point rubric score and names the reason for every point lost:

```
python3 tools/score_skills.py --skill your-skill
python3 tools/score_skills.py --json
```

The validator enforces the mechanical style rules on every commit and fails the build on any of them:

```
python3 tools/validate_skills.py
```

The detector reports stylistic markers of machine-written prose, graded high, medium, and low. Point it at the skill's Markdown files with the human-prose detector script and the `--pedantic` flag:

```
python3 <path-to>/ai_tells.py --pedantic skills/your-skill/SKILL.md
```

The target is the scorer at ten out of ten and the detector at zero high, zero medium, zero low under `--pedantic`. The scorer runs the detector internally for its style point, so a detector finding also costs a rubric point.

## Reading the scorer output

The scorer prints one line per skill with the score, then a bullet for each lost point naming the criterion and the reason. The reasons are specific: it will say only eight trigger phrases were found where ten are needed, or that a Fit to the project section is missing, or that a named reference file is never mentioned so it will never load. Fix the named cause; do not guess.

The references criterion checks the link in both directions. Every reference file has to be mentioned from a Markdown file in the skill, and every path mentioned has to exist. A file present but never mentioned fails, and a mention of a missing file fails, so add the reference and its mention together.

## Reading the detector output

Each finding gives a severity, a file and line, a rule name, and a short reason. The rule name tells you the pattern. Common ones on a first draft:

`vocab` flags an overrepresented word. The catalogue in the human-prose skill lists them; when one is flagged, replace it with the plain word it stands in for.

`copula-avoidance` flags a phrase that dodges a plain "is" or "has". When one is flagged, use "is" or "has" directly.

`em-dash`, `curly-quote`, and `en-dash` flag non-ASCII punctuation. Retype the character as ASCII, because a paste from a word processor is the usual source.

`participle-tail` flags a comment clause tacked onto a sentence end with a word like "ensuring" or "highlighting". Cut it or make it a plain clause.

`negative-parallelism` flags the "not X, but Y" contrast shape and its variants. Say the positive claim directly.

`bold-label-list` flags a bulleted list whose items open with a bold inline header. Use plain text labels or prose instead.

`final-newline` and `trailing-space` flag whitespace. End every file with exactly one newline and strip trailing spaces.

## Fix, do not exempt

The detector allows per-file, per-rule exemptions through an HTML comment, and every exemption prints in the report so none hides. Those exist for the files whose job is to document the banned patterns, such as the style guide itself. Do not add one to a new skill to reach the score. An exemption taken to pass leaves the residue the check was built to catch, and the report shows the exemption to anyone reading it. Fix the prose instead.

## Loop to closure

Run the scorer, read the named failures, fix them, and run it again. Run the detector, read the findings, fix the prose, and run it again. The checks are cheap, so the loop is short. Stop only when the scorer prints ten out of ten and the detector prints zero high, zero medium, zero low.

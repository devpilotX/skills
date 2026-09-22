# The rubric

Every skill in this repository scores ten out of ten, and the score is computed rather than claimed:

```
python3 tools/score_skills.py
python3 tools/score_skills.py --skill seo-optimize
python3 tools/score_skills.py --json
```

Ten criteria, one point each, all ten required. A skill at nine does not ship. The checks are
mechanical on purpose, because a rubric scored by opinion drifts within a week.

The criteria exist to answer one question: can a model that has never seen this project read the file
once and do the work without asking a human for anything it could have found out itself?

## 1. Spec

The name in the frontmatter matches the folder, in lowercase with single hyphens. The description sits
on one line between 200 and 1024 characters. A license field is present. The metadata block carries a
semantic version and the suite name. The body runs past 1500 characters, because anything shorter is a
preference rather than a procedure.

## 2. Activation

A skill nobody loads does nothing. The description has to say when to use it and then list the phrases
a user actually types, at least ten of them, after the words "Triggers on".

Write the triggers a user would say, not the terms an engineer would index. Someone with a slow page
types "site is slow", not "latency percentile regression".

## 3. Universality

Every skill carries a section headed exactly `## Fit to the project` with at least three lines of
content. It tells the reader how to detect what the project already uses and adapt to it, before
changing anything.

No absolute paths from anyone's machine. No home directories, no drive letters. No sentence that makes
one vendor, language, or framework the only way through. A skill may recommend a tool and has to work
without it.

This is the criterion that fails most often on a first draft, because it is the easiest to skip while
writing confidently about the stack you happen to be thinking about.

## 4. Procedure

At least four ordered steps, written as `### Step 1,` through `### Step 4,` or more, or as a numbered
list of four or more items under a procedure heading. Phases and gates count.

Each step says what to do and what to produce, in an order that survives being followed literally. A
list of topics is not a procedure.

## 5. Non-negotiables

A section headed `## Non-negotiables` with at least four numbered rules that override everything else
in the file. Each one names what breaks when it gets ignored.

These are the rules worth stating because a model under pressure to be helpful will otherwise trade
them away. Never invent a number. Reproduce before fixing. Measure before optimising.

## 6. Self-audit

A section headed `## Self-audit` with at least six items to check before delivering. Each item is
answerable yes or no by looking at the output.

An item like "the work is high quality" fails this test. An item like "every figure is cited or
labelled as an assumption" passes it.

## 7. Off switch

An explicit instruction to stand down, plus a quoted phrase the user can actually say, such as "stop"
or "just execute". The phrase has to appear in quotation marks so a reader can find it.

A skill that keeps applying itself after the user has declined becomes nagging, and nagging gets the
whole collection uninstalled. This is a usability requirement, not a courtesy.

## 8. Honest limits

A section headed `## Honest limits` with at least two lines saying what the skill does not do, where
its numbers come from, and which neighbouring skill or licensed professional owns the part it cannot.

A skill that claims no limits is lying about at least one.

## 9. References

At least two files under `references/`, every mention resolving to a real file, and every file
mentioned somewhere so nothing sits unreachable.

Split by when the reader needs the file, not by topic. The main file holds what applies every time.
A reference holds what applies sometimes: a lookup table, a worked example, a domain checklist, a
format specification. Keeping the main file short is what makes it get read.

## 10. Style

Zero findings from the detector at its strictest level across every Markdown file in the skill:

```
python3 skills/human-prose/scripts/ai_tells.py --pedantic skills/your-skill/*.md
```

The rules are in STYLE.md. Where a skill produces source code, its metadata sets `emits_code: true`
and its body points at the `code-craft` contract, so generated code arrives organised and commented
instead of arriving as one long block.

## Writing a new skill

Work in this order. Writing prose first and retrofitting the structure produces a file that passes the
checks and still reads as filler.

1. Name the failure. What does a competent person get wrong here, or what does a model get wrong by
   defaulting to the most probable answer? Write that in two sentences. If you cannot, the skill has no
   subject yet.
2. Write the procedure as bare steps, with the output of each one. No prose.
3. Write the non-negotiables by asking what a helpful assistant would trade away under pressure.
4. Write `## Fit to the project`: what to read, in what order, before acting.
5. Write the self-audit as questions with yes or no answers.
6. Write `## Honest limits`. Name the neighbouring skills that own what this one does not.
7. Move the lookup tables, the worked example, and the domain detail into `references/`.
8. Write the description last, once you know what the skill does. Collect the trigger phrases from how
   people actually complain about the problem.
9. Run the scorer, the validator, and the detector. Fix findings rather than working around them.

## What the rubric cannot check

A file can score ten and still be generic. This is not a worry, it is a measured result: a skill written
to be deliberately empty, about an imaginary subject, with the right headings and enough bullets and
clean prose, scores ten out of ten. The checks confirm that the parts are present and the prose is
clean; they cannot confirm that the procedure produces a better result than the model's default
behaviour.

So there is one more test, and it is a judgement call. Read the skill and ask what it stops the model
from doing. If the answer is nothing, the file is a description of good intentions. Delete it and start
from the failure it was supposed to prevent.

Treat the score as a floor, not a grade. It says a skill is structurally complete enough to be worth
reading, and says nothing about whether reading it was worthwhile.

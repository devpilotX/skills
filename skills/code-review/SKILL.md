---
name: code-review
description: Review a diff, pull request, or file for defects that matter, with a verdict and no filler. Use when the user asks to review code, review a PR or merge request, check a diff, look over an implementation, find bugs in code, or asks whether code is correct or safe to merge. Also use after writing a non-trivial change, before requesting human review. Reads the code before judging it, ranks findings by consequence rather than by how easy they are to spot, ignores anything a formatter or linter should catch, names the input that triggers each defect, and reports a clean change as clean instead of manufacturing style comments to look thorough. Triggers on review this code, review my PR, review my merge request, check this diff, find bugs, is this correct, is this safe to merge, code review, look over this implementation, does this have security holes, will this break callers, is this ready to ship.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Code review

Find the defects that cost something. Ignore the rest.

## Fit to the project

Read what the change lands in before judging the change.

1. Read the pull request or merge request description and the linked issue, then the commit messages on the branch. State what the author says the change does before you form your own view. A review that argues with a goal the author never had is noise.
2. Find the base branch the change targets and diff against its merge base, not against your local tip, so you review what actually merges. `git merge-base main HEAD` then `git diff` from that point keeps deleted and moved code in view.
3. Detect the checks the project already runs: a continuous integration config, a pre-commit hook file, a coverage gate, a lint or type config. Whatever those own is out of scope for your comments, because a machine already reports it on every push.
4. Read the two or three files the diff touches most, in full, so a finding about a changed function is grounded in how the function is called elsewhere. Read the tests next to those files to learn what behaviour the team already pins.
5. Where the project has settled no review conventions and has no continuous integration, say so in the report and review against the priority order below, and treat correctness and data safety as the bar.

## When to stay off

Skip the deep pass when the change is a version bump, a generated lockfile, a vendored dependency, a documentation typo, or a diff the author has flagged as work in progress and not for review yet. Reviewing a machine generated file line by line wastes the author's time and buries any real comment.

The off switch is saying "stop", "just execute", or "skip the review". It stays off for the rest of the session unless you ask for it again. A reviewer who keeps commenting after being told to stand down gets muted.

## What gets reviewed and what does not

Not reviewed, ever, because tooling belongs to tooling: formatting, import order, quote style, line
length, naming preferences that do not mislead, and anything a linter or formatter already decides. A
review comment about spacing is a wasted read.

Reviewed in this order of priority:

1. Correctness on the path the author intended.
2. Correctness on paths the author did not consider, which is where most real defects live.
3. Security consequences.
4. Data safety, including migrations, deletes, and anything irreversible.
5. Failure behaviour, including partial failure and retry.
6. Concurrency, ordering, and idempotency.
7. Resource handling, including unbounded growth and unclosed handles.
8. Interface and contract changes that break callers.
9. Test adequacy for this change specifically.
10. Clarity, but only where it will cause a future defect. Say why, or drop the comment.

## Non-negotiables

1. Read the code, including the surrounding context the diff does not show. A diff hides the caller, and the caller is often where the bug becomes real.
2. Every finding names the input, state, or sequence that triggers it. A finding without a trigger is a guess and gets labelled as one.
3. No manufactured findings. A clean change gets a short review saying it is clean and what was checked. The pressure to produce volume is the main way reviews become worthless.
4. Do not claim a test passes or fails without running it. Say which commands were run and what they printed.
5. Distinguish a defect from a preference. Both can be raised, and they must be labelled differently, because the author needs to know which ones are negotiable.
6. Review the change, not the person. No commentary on the author's judgement or skill.

## Procedure

### Step 1, establish intent

Read the description, the linked issue, and the tests. State in one sentence what this change is meant
to do. If the code does something else, that is the first finding, and it usually outranks everything
else.

If intent cannot be determined, ask. Reviewing without knowing the goal produces noise.

### Step 2, read the change in context

For each modified function, read the callers. For each modified interface, find every implementation
and every consumer. For each removed line, work out what depended on it.

```
git diff --stat main...HEAD
git log --oneline main...HEAD
grep -rn "functionName" --include="*.ts" .
```

Look at what the diff does not contain. A new field with no migration, a new branch with no test, a new
error type nobody catches, a new dependency with no lockfile change.

### Step 3, run what can be run

Tests, type checker, linter, build. Report the real output. A review that claims correctness without
running the suite is weaker than it sounds, and saying so is better than implying otherwise.

### Step 4, hunt the specific defect classes

Checklist in `references/defect-classes.md`, organised by the class of bug rather than by language, so
it applies to whatever stack is in front of you. Work it deliberately, because the defects that get
missed are the ones nobody thought to look for.

### Step 5, verify each finding before writing it

Ask what exact input triggers this, and what the consequence is. If the answer is "in some cases" or
"potentially", either find the case or move the item to observations.

Then check whether the codebase already handles it somewhere you have not read. Reporting a defect that
is handled two frames up is the most common way a review loses credibility.

### Step 6, report

```
VERDICT: APPROVE / APPROVE WITH FIXES / REQUEST CHANGES / NEEDS MORE CONTEXT
[One sentence. If REQUEST CHANGES, the blocking reason goes here.]

WHAT THIS CHANGE DOES
[One sentence, in your own words. If this does not match the description, say so.]

CHECKED
[Commands run and their output. Files read beyond the diff.]

BLOCKING
1. path/file.py:88 - [defect]
   Trigger: [exact input or sequence]
   Consequence: [what breaks and for whom]
   Fix: [the change]

NON-BLOCKING
[Same shape, condensed.]

PREFERENCES
[Clearly labelled as negotiable. Keep this section short or empty.]

TESTS
[What this change needs a test for, and whether it has one.]

NOT REVIEWED
[Anything skipped, and why.]
```

### Step 7, self-audit

- Every finding has a trigger and a consequence.
- No finding concerns formatting or anything a linter owns.
- Defects and preferences are labelled separately.
- Claims about tests are backed by output that was actually seen.
- The verdict is explicit.
- Anything unread is disclosed.
- If the change is clean, the review is short and says what was checked.

## Emitting code in a review

When you write a fix inline, the snippet has to read as well as the code around it. Follow the `code-craft` contract: match the file's existing names and structure, keep the fix to the smallest change that closes the finding, and do not restructure surrounding code inside a review comment. A fix that drags in a refactor stops being reviewable.

## Self-audit

- Every blocking finding names the exact input, state, or sequence that triggers it.
- No finding concerns formatting, import order, or anything the project's linter already reports.
- Defects and preferences carry different labels in the report.
- Every claim that a test passed or failed quotes the command and its output.
- The verdict is one of the four values and appears on the first line.
- Every file or path read beyond the diff is listed under CHECKED.
- A clean change gets a short review that names what was checked rather than a manufactured comment.
- The security pass covered object level authorisation, injection sinks, and secret exposure for this diff.

## Honest limits

This skill reviews a change for defects. It does not decide whether the change is worth making or whether the design behind it is sound, which is an architecture question that `arch-decide` owns. It reads tests for adequacy but does not write the missing ones, and `test-strategy` owns choosing what to test and building the suite.

The defect classes in `references/defect-classes.md` are a checklist, not a proof. A finding is a candidate until you have traced the trigger through the real code. A review that runs no tests reports correctness on reading alone, which is weaker than a review that ran the suite, and the report says which of the two it is. Whether the resulting code is clean enough to maintain is a separate judgement covered by `code-craft`.

The verdict wording and the report layout come from the conventions in `references/verdict-guide.md`. When a project has its own review template, adopt that instead and say so.

---
name: code-craft
description: Write source code a maintainer can read, in any language: files split by responsibility, functions short enough to hold in your head, names that say what the value is, and comments that explain why rather than restating syntax. Use when generating or editing code, when one file has grown past the point where a reader can find anything, when logic arrives as a single long block, when a review asks for readability work, or when code needs comments or docstrings before handover. Sets budgets for file length, function length, nesting depth and parameter count, separates decision logic from input and output, requires errors to carry context, and bans commented-out code, dead branches and decorative banners. Triggers on clean up this code, refactor for readability, organise this file, split this function, add comments, add docstrings, this file is too long, too much nesting, code smells, better naming, make this maintainable, code style, production quality code, one giant function.
license: MIT
compatibility: Any language and any project. The optional structure scanner needs Python 3.8 or newer and uses only the standard library.
metadata:
  version: 1.0.0
  suite: skills
---

# Code craft

Working code fails review for reasons that have nothing to do with whether it runs. One file carries
six responsibilities. One function runs two hundred lines with four levels of nesting. A variable
called `data` turns out to mean unpaid invoices from the last billing cycle. Comments restate the line
above them and go stale at the next edit.

Generated code fails this way more often than hand written code, because a model optimises for a
working answer in one pass and a reader needs the answer in pieces. The fix is to decide the shape
before writing, then measure the shape afterwards.

## Fit to the project

Read the project before writing any of it. Local convention beats this document every time.

1. Find the configuration that already decides layout: an editor config, a formatter config, a linter
   ruleset, a language specific style file. Adopt it exactly, including indent width and line length.
   Run the formatter the project already has rather than hand formatting to a different taste.
2. Read the two or three largest existing source files. Note how names are formed, how functions are
   grouped, whether the code prefers classes or plain functions, how errors are raised and wrapped,
   and which comment and docstring form is in use.
3. Put tests where the existing tests live, named the way they are named. A second test convention
   costs more than it adds.
4. Where the project has settled nothing, take the defaults in `references/budgets.md` and say which
   ones you applied in your report.

A file that matches a mediocre local convention beats a file that matches this document and nothing
else around it. Consistency is the property a reader actually depends on.

## When to stay off

Skip the full treatment for a one line change, a configuration value, a machine generated file, a
vendored dependency, or a script the user has already called throwaway. Reformatting a file you were
not asked to touch turns a small review into a large one and hides the real change in the diff.

Saying "stop", "just execute", or "skip the cleanup" is the off switch. It stays off for the rest of
the session unless invoked again.

## Non-negotiables

1. One reason to change per file. If a file holds request parsing, a pricing rule, a database write
   and a retry policy, four unrelated tickets will edit it and two of them will conflict.
2. No function past the length budget for its language, and no function past three levels of nesting.
   Both limits are in `references/budgets.md`. Extract a named helper instead of adding a level.
3. A comment earns its place by saying why, or by recording a constraint the code cannot state. A
   comment that restates the next line is deleted, not improved. Policy in
   `references/comment-policy.md`.
4. Never leave commented-out code, an unreachable branch, a debug print, or a leftover marker naming
   work you did not do. If it might be needed later, version control already has it.
5. Every error that crosses a boundary carries what failed, which input caused it, and what the
   caller can do about it. A bare re-raise with no context costs an hour at three in the morning.
6. Names describe the value, not the type or the position. `unpaid_invoices` over `list2`,
   `retry_after_seconds` over `timeout`, `is_expired` over `flag`. Units belong in the name when the
   value has units.
7. No decorative banners, no boxes drawn in asterisks, no section dividers made of repeated
   characters. They rot, they never match, and a function name does the same job.

## Procedure

### Step 1, decide the shape before typing

Write down, in one or two lines, what the unit of work is and where its boundaries sit. Name the files
you expect to create or touch and what each one owns. If you cannot say what a file owns in a short
phrase without the word "and", it owns too much.

For anything past a single function, decide three things first: where input arrives and gets
validated, where the decisions are made, and where results leave. Keeping those three apart is what
makes the decisions testable without a database or a network.

### Step 2, write the boundaries first

Write the signatures, the data shapes, and the error cases before the bodies. A signature with honest
types is a design document that the compiler or the test suite checks for you.

Give every function a single job and a name that says it. When the honest name contains "and", split
it.

### Step 3, fill in the bodies, shallow first

Handle the failure cases at the top and return early. Guard clauses flatten a function that would
otherwise nest four deep for no reason.

Keep the happy path at the leftmost indent level, so a reader can follow the normal case down the
page without tracking conditions.

Pull any block that needs a comment beginning "now we" into its own named function. The name replaces
the comment.

### Step 4, name everything a second time

Reread the code as someone who has not seen it. Rename anything that needed a moment of thought.
Renaming is the cheapest readability work available and the most often skipped.

Check that similar things are named similarly and different things are not. Two functions called
`process` and `handle` that do unrelated work are worse than no names.

### Step 5, comment only what the code cannot say

Add the why: the constraint from outside, the reason for the unusual choice, the bug this guards
against, the link to the specification or ticket that explains the rule. Add a docstring wherever the
project's convention expects one, saying what the function does, what it needs, what it gives back,
and what it raises.

Delete every comment that a reader could have produced by reading the line under it.

### Step 6, measure against the budgets

Run the project's formatter and linter. Fix what they report rather than arguing with them.

Then check the structure limits, either by reading or with the scanner:

```
python3 scripts/structure_scan.py src/
python3 scripts/structure_scan.py src/ --max-file 400 --max-function 50
python3 scripts/structure_scan.py src/ --json
```

The scanner reports files over the line budget, functions over the length budget, nesting past the
depth budget, and functions with too many parameters, for the languages listed in its help text. It
reads indentation and braces rather than parsing, so treat a finding as a prompt to look rather than a
verdict. A number over budget is a question, and sometimes the answer is that a long table of constants
belongs in one place.

### Step 7, report what you did

Say which files you created or changed and what each one owns. Name the budgets you applied and any
place you went over one deliberately, with the reason. If you adopted the project's existing
convention over the defaults here, say that too.

## What good structure looks like

Input validation at the edge, in one place per entry point, so the inside of the system can trust its
arguments.

Decisions in functions that take values and give back values. No clock, no network, no global state.
These are the parts worth testing and the parts that stay correct for years.

Input and output at the outside: the database call, the HTTP request, the file write, the log line.
Thin, boring, and easy to replace.

Configuration read once at startup into a typed structure, not read from the environment in the middle
of a decision.

Errors converted at each boundary into the vocabulary of the layer above, so a caller never has to
know that a failure came from a specific driver.

## Self-audit

- Every file has one reason to change, and its name says what that is.
- No function is over the length budget, and none nests past three levels.
- Every name says what the value is. No `data`, `temp`, `info`, `obj`, `val`, or numbered variables.
- Units appear in names where the value has units.
- Every comment says why, records a constraint, or is a docstring the project's convention expects.
- No commented-out code, no unreachable branch, no debug output, no leftover work marker.
- Errors carry the failing input and what the caller can do.
- The formatter and linter the project already has both run clean.
- Input handling, decisions, and output live in separate functions.
- The report names the files touched, what each owns, and any budget deliberately exceeded.

## Honest limits

The budgets in `references/budgets.md` are conventions, not findings. They come from what reviewers
tolerate in practice, and a project with different constraints should pick different numbers and write
them down. The value is in having a limit that is checked, more than in the specific figure.

The structure scanner reads indentation and counts braces. It does not parse, so it miscounts
multi-line strings in some languages, generated files, and heavily macro driven code. It is a way to
find candidates for review, and it cannot tell you whether a long function is wrong.

Readable code and correct code are different properties, and this skill only addresses the first. A
clear function with a wrong comparison is still a bug. Correctness belongs to `test-strategy` and
`code-review`.

Nothing here judges architecture. Whether the module boundaries are in the right place is a design
question that `arch-decide` handles.

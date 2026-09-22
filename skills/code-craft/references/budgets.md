# Structure budgets

Defaults to apply when the project has settled nothing. Pick different numbers if the project has a
reason, write them down, and check them the same way. A limit nobody measures is a preference.

## Why a number at all

A reviewer holds a limited amount of a file in their head at once. Past roughly one screen, they stop
reading a function and start scanning it, and scanning is where defects survive. The exact threshold is
a convention rather than a measurement, so the useful part is that it exists and gets checked.

## Per language defaults

Line counts exclude blank lines and comment-only lines. Function length counts the body.

| Language | File lines | Function lines | Max nesting | Max parameters |
|---|---|---|---|---|
| Python | 400 | 50 | 3 | 5 |
| JavaScript, TypeScript | 300 | 40 | 3 | 4 |
| Go | 500 | 60 | 3 | 5 |
| Java, Kotlin, C# | 400 | 40 | 3 | 5 |
| Rust | 500 | 60 | 3 | 5 |
| Ruby | 300 | 30 | 3 | 4 |
| PHP | 400 | 50 | 3 | 5 |
| C, C++ | 600 | 60 | 4 | 6 |
| Swift | 400 | 50 | 3 | 5 |
| Shell | 200 | 40 | 3 | 4 |
| SQL (one statement) | 150 | n/a | 4 subqueries | n/a |

Go and Rust get more room per file because both communities keep a package or module in fewer, larger
files by convention, and fighting that produces code the local reviewers dislike.

C and C++ get one extra nesting level because error handling without exceptions genuinely costs a
level.

## The limits that matter more than length

Nesting depth predicts defects better than length. A function of eighty flat lines reads faster than
one of thirty lines nested four deep. When only one limit can be enforced, enforce this one.

Parameter count past five usually means a missing structure. Group the arguments that travel together
and name the group.

Return points are fine in quantity when they are guard clauses at the top. They are hard to follow
when they are scattered through nested branches.

Cyclomatic complexity past ten in one function is a reliable prompt to split it. Most linters can
report this, and the project's linter should own it rather than this skill.

## Exceeding a budget on purpose

Some code is honestly long. A table of constants, a generated parser, an exhaustive match over forty
message types, or a single algorithm that loses clarity when cut in half. Going over is allowed when
all three of these hold:

1. Splitting it would need a name that does not exist in the domain.
2. The long part is one idea, not several stacked together.
3. You say in the report that you went over and why.

What does not qualify: a function that grew, a file that collected unrelated helpers, or a block of
branches that each handle a different feature.

## Files this does not apply to

Machine generated sources, vendored dependencies, database migrations produced by a tool, snapshot test
fixtures, and lock files. Leave them as the tool wrote them. Reformatting them creates a diff nobody
can review and breaks the tool's next run.

## Checking

The scanner at `scripts/structure_scan.py` reads these defaults and accepts overrides:

```
python3 scripts/structure_scan.py src/
python3 scripts/structure_scan.py src/ --max-file 300 --max-function 40 --max-depth 3
python3 scripts/structure_scan.py . --ext py,ts --json
```

Prefer the project's own linter where it already measures one of these. Two tools reporting the same
finding with different numbers wastes a reviewer's attention.

# Memory file format

This describes the memory directory precisely enough that a different tool, or a human with a text editor, can read and write it without the shipped CLI. The format is plain Markdown so it stays readable in a diff and in a code review.

## Directory layout

The memory directory is committed in the repository, in a tracked path. Its default name is `project-memory`, and it holds five files, each with one job:

```
project-memory/
  state.md
  facts.md
  decisions.md
  questions.md
  log.md
```

Nothing in these files is secret. A secret, token, key, password, or customer record must never appear, because the directory is committed and its history keeps whatever was written even after an edit.

## Read order at session start

Read in this order and stop once you can act:

1. `state.md`, the present moment, cheapest to load.
2. `facts.md`, the things that rarely change.
3. `decisions.md`, why the project is shaped the way it is.
4. `questions.md`, what is still open.
5. `log.md`, the recent tail for detail, read from the end backwards.

## Per file specification

Each file opens with a level one Markdown heading and a short description of its job. Line budgets are counted as non-blank lines. A file over budget gets compacted, not truncated.

state.md holds what is in progress now, the next concrete step, and any half-done change. It is overwritten freely because it holds the present, not history. Budget 60 lines.

facts.md holds one fact per line: what the project is, who uses it, the stack, the build and test commands, the deploy target. Budget 120 lines. A fact that stops being true is edited, because a fact is a current statement, not a dated event.

decisions.md holds one decision per block. A block is a level two heading of the form `## YYYY-MM-DD the choice`, followed by lines that begin `Reason:`, `Rejected:`, and optionally `Replaces:`. Blocks accumulate in the file in the order they were written. A decision is never edited after the fact; a reversal is a new block whose `Replaces:` line names the date and choice it overturns. Budget 200 lines.

questions.md holds one open question per line with its current best guess. A line is removed when the question is answered, and the answer is recorded as a fact or a decision. Budget 80 lines.

log.md holds dated append-only entries, one or two lines each, in the form `- YYYY-MM-DD what happened and why`. Newest entries sit at the bottom. A past entry is never rewritten; a correction is a new dated entry. Budget 300 lines.

## Date format

Every date is an ISO 8601 calendar date, `YYYY-MM-DD`, in the writer's local time zone. A consistent, sortable date is what lets a later reader order events without guessing.

## Worked example of a decision block

```
## 2026-03-14 store sessions in Redis
Reason: the web tier is stateless and needs shared session state across nodes
Rejected: sticky load balancer sessions, which break on a node restart
```

A later reversal:

```
## 2026-05-02 move sessions to signed cookies
Reason: Redis added an operational dependency we did not want for a small app
Replaces: 2026-03-14 store sessions in Redis
```

## Compaction

When a file passes its budget, replace a run of old low-value lines with one dated summary line that keeps the conclusion and drops the step-by-step. The rules of thumb for what to keep are in `read-protocol.md`. Decisions are never summarised away; only narrative around them in the log is. Record the compaction as a log entry naming the date range you summarised.

## Writing without the CLI

Any tool that can create a directory and append UTF-8 text to a Markdown file can maintain this store. Preserve the heading in each file, keep the date format, append rather than overwrite for the log and decisions, and end every file with exactly one newline.

---
name: debug-method
description: Find the cause of a bug by narrowing it down instead of guessing at fixes. Use when the user reports something broken, asks why their code fails, pastes an error or a stack trace, says it works locally but not in production, says it works sometimes, asks about a race condition or a memory leak or a heisenbug, or has already tried several fixes without success. Requires a reproduction before any fix, forms one hypothesis at a time with a prediction that can be wrong, changes one thing per experiment, and refuses to declare victory on a symptom that stopped appearing without an explanation. Distinguishes the cause from the trigger and writes down what was ruled out. Triggers on why is this broken, debug this, error message, stack trace, works locally but not in production, intermittent failure, race condition, memory leak, it works sometimes, I tried everything, flaky.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Debugging method

Guessing at fixes is slower than narrowing down, and it leaves behind changes nobody can justify. The
discipline is one hypothesis at a time with a prediction that could turn out wrong.

## Fit to the project

Learn how to run and observe the thing before you touch a line of it.

1. Find how the project runs and how it starts: a run script in the package manifest, a container compose file, a makefile target, a readme run section. Get it running in the state where the bug appears before you form any hypothesis.
2. Find where output goes. Look for a log configuration, a log directory, a structured logging setup, or the console the process writes to. Turn up the log level around the failing area if the project lets you, because a logged input at the failure point beats reasoning about what the input might be.
3. Find the last known good version. Read the deploy history, the changelog, or the tags, and ask when it last worked. A known good commit and a known bad commit turn the search into a bisection instead of a guessing game.
4. Detect what changed near the start of the symptom: recent commits, a dependency update in the lockfile, a config or environment change, a data migration. Most breakage in a system that used to work correlates with one of these.
5. Where the project documents none of this and you cannot tell how it runs or where it logs, say so and reproduce from the smallest command that triggers the failure, adding temporary logging at the failure point to get the first fact.

## When to stay off

Skip the full method for a one line typo with an obvious cause, a message the error text explains outright, or a case the user has already diagnosed and only wants typed out. Running a six step investigation on a missing import wastes the user's time.

The off switch is saying "stop", "just execute", or "skip the investigation". After that it holds
for the session unless you reopen the investigation.

## Non-negotiables

1. Reproduce before fixing. Without a reproduction there is no way to know the fix worked, and the most common outcome is a change that coincides with the symptom pausing.
2. One change per experiment. Changing three things and observing improvement teaches nothing about which one mattered, and often leaves two unnecessary changes in the code.
3. Write the prediction before running the experiment. A prediction that cannot be wrong is not an experiment, and unwritten predictions get retrofitted to whatever happened.
4. A symptom that stopped without an explanation is not fixed. Say so plainly. Intermittent bugs that disappear under observation return in production.
5. Read the actual error, all of it, including the cause chain and the line numbers. Skipping to a guess based on the first line is the most common wasted hour in debugging.
6. Keep a list of what has been ruled out and how. Without it the same ground gets covered twice, especially across a long session.
7. Distinguish the cause from the trigger. The trigger is the input that exposed it. The cause is why the code was wrong. Fixing only the trigger leaves the bug.

## Procedure

### Step 1, get the facts straight

What exactly happens, and what was expected instead? A vague report costs more than the debugging.

Which environment, which version, which commit? When did it last work? A working commit plus a broken
commit is the single most valuable pair of facts available, because it converts the problem into a search.

Is it everyone or one user, one tenant, one region, one device, one browser?

What changed near the start of it? A deploy, a configuration change, a dependency update, a data change, a
certificate expiry, a third party incident, or a clock change. Most breakage in previously working systems
correlates with a change.

Read the whole error text and the whole stack trace, from the innermost cause outwards.

### Step 2, reproduce

Reliably if possible. Intermittently if that is all there is, and then record the rate, because a change
from one in ten to one in a hundred looks like a fix and is not.

Shrink the reproduction. Remove inputs and steps until removing anything makes it stop. A small
reproduction usually identifies the cause on its own.

If it cannot be reproduced locally, add observability where it does happen rather than guessing. Logging
the inputs at the failure point is faster than reasoning about what they might be.

For anything intermittent, suspect the usual four: a race between two operations, a dependence on
ordering, a resource limit reached under load, or time and timezone behaviour.

### Step 3, bisect the space

Narrow along whichever axis is available.

In time, using version control. `git bisect` between a known good and known bad commit turns a hard
question into a handful of tests, and it is underused.

In the stack, by checking whether the data is correct at each layer. Find the first place it is wrong,
which is where to look, and not where the exception surfaced.

In the data, by finding which record triggers it. One bad row explains many mysterious failures.

In the configuration, by comparing environments field by field. When it works locally and not in
production, the difference is in that comparison: a version, a variable, a permission, a limit, a
concurrency level, or the data volume.

In the code, by removing halves until the smallest failing piece remains.

### Step 4, form and test one hypothesis

State it as a falsifiable claim. Something like: the handler reads the record before the transaction that
writes it has committed, so under concurrent requests it sees the previous value.

Write the prediction. If this is true, then running two requests simultaneously will show the stale value,
and adding a lock will stop it.

Run the experiment, change one thing, and record the result whether or not it matched.

When the prediction fails, the hypothesis was wrong. Record it as ruled out and move on. This is progress,
and treating it as failure is why people fall back to guessing.

### Step 5, confirm the cause

You have the cause when you can explain every observed symptom with it, including the part that seemed
odd, and when you can turn the bug on and off deliberately.

An explanation that covers most of the symptoms usually means there are two problems, or the wrong one was
found.

Being able to reintroduce the bug on demand is the strongest available evidence.

### Step 6, fix it properly

Write the failing test first, so there is proof the fix works and protection against its return.

Fix the cause, not the symptom. A null check where the null should never have arrived hides the real
defect.

Ask where else this pattern exists. One instance of a class of bug usually means several.

Check the fix does not break the case the original code was written for, which is a common regression when
the original intent was not understood.

### Step 7, report

State the cause, the trigger, the evidence, the fix, the test, and anything ruled out along the way.
Include where else the pattern might exist.

If the cause was never found and the symptom stopped, say that explicitly. A closed ticket with an
unexplained resolution is a bug waiting for a worse moment.

## Common causes worth checking early

Not the code at all: a configuration difference, an expired credential or certificate, a full disk, a
clock skew, a permission change, or a third party incident.

Caching, at any of the several layers involved, including the browser, a CDN, an application cache, a DNS
resolver and a build cache.

An old version still running somewhere, which makes a fix appear not to work.

Two versions running at once during a deploy, which produces symptoms that make no sense against either
version alone.

Character encoding, and a locale difference between environments.

A timezone or daylight saving boundary.

Silent truncation by a column length or a payload limit.

A retry that succeeded and left duplicate work behind.

## Self-audit

- A reproduction exists, with its rate if intermittent.
- Each experiment changed one thing, with the prediction written first.
- Ruled out list maintained.
- The cause explains every symptom, and the bug can be switched on and off.
- Cause fixed rather than symptom.
- A test fails before the fix and passes after.
- Other instances of the same pattern searched for.
- If the cause was not found, that is stated rather than implied to be resolved.

## Writing the instrumentation and the fix

The temporary logging you add to observe a failure, and the fix you land once the cause is confirmed,
follow the `code-craft` contract: name the logged values for what they are, keep the fix to the cause you
proved rather than the symptom you saw, and remove any probe you added to narrow the search. A worked
narrowing from stack trace to confirmed cause is in `references/worked-example.md`.

## Honest limits

This skill finds the cause of a bug. It does not decide what test should pin the cause once found, which
is `test-strategy`, and it does not restructure the code to make the fix safe to land, which is
`refactor-safely` when the fix needs a seam first. It stops at a confirmed cause and a failing test; the
readability of the fix itself is `code-craft`.

The narrowing axes and the early suspects come from patterns that recur across systems, not from a
measurement of this project. The intermittent bug playbook in `references/intermittent-bugs.md` lists the
usual causes of a failure that comes and goes; it is a place to start the search, not a diagnosis, and a
cause is confirmed only when you can switch the bug on and off on demand.

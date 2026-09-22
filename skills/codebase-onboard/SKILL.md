---
name: codebase-onboard
description: Build an accurate model of an unfamiliar codebase before changing it, in any language or framework. Get it running first, find the real entry points, trace one request or one job end to end, read the tests as the specification the authors enforced, use version control history to find files that change together, map the data stores and external services, and write down what you learned. Use when you inherit a repository, join a project, or must edit code you did not write. Triggers on new to this codebase, unfamiliar repo, inherited this project, where do i start, how does this app work, onboard me, understand this code, legacy system, no documentation, where is the entry point, trace a request, how is this deployed, what does this service do, first time in this repo.
license: MIT
compatibility: Any language, framework, and repository layout. The optional history commands assume git; equivalents exist for other version control systems.
metadata:
  version: 1.0.0
  suite: skills
---

# Codebase onboard

The common failure is editing an unfamiliar codebase from a partial reading and a confident guess. A change lands in a file that looked central but is dead, or it duplicates a helper that already exists three directories away, or it breaks a contract that only the tests knew about. The cost shows up in review or in production, long after the guess felt safe.

Reading alone cannot tell you which paths run, which files are load bearing, and which the team stopped touching years ago. This skill builds the model from evidence you can check, so the first change fits the system that exists rather than the one you imagined.

## Fit to the project

Read the project before you form any opinion about it.

1. Find how the project is built and run. Look for a package manifest, a build file, a container definition, a task runner, and any script named to set up or bootstrap. These name the real toolchain and the real commands, which beat any README that has gone stale.
2. Detect the shape from the top two levels of directories and the largest source files. Note whether it is one service or many, where configuration is read, and where the tests live. Match your notes to the vocabulary the code already uses.
3. Read the version control log for the last few months before you read the code in depth. The files that change most often and the authors who touch them tell you where the work happens and who to ask.
4. Where the project documents its own layout, in a contributing guide or an architecture note, read it and then verify it against the running system. Treat the document as a claim, not a fact.

## When to stay off

Skip the full onboarding for a one line fix in a file you already understand, a configuration value, a typo, or a repository you built last week. A change that touches one well understood file does not need a request traced end to end first.

The off switch is saying "stop", "just execute", or "skip the onboarding". Once you decline, it does
not raise the subject again this session.

## Non-negotiables

1. Get it running before you read deeply. A codebase you cannot start is a codebase you are guessing about, and a guessed model is the thing that produces the broken first change. If it will not run locally, say so and work from tests and history instead of pretending you have a running model.
2. Trace at least one real path end to end before editing. If you change code on a path you have not followed from entry to exit, you do not know what depends on the behaviour you are changing, and the regression surfaces somewhere you never looked.
3. Read the tests before you trust the code. Tests are the behaviour the authors chose to enforce, and a change that passes the existing tests but breaks an untested assumption is the failure this step prevents. If a file has no tests, treat every behaviour in it as undocumented and confirm it by running it.
4. Separate the documented architecture from the running one. Acting on a diagram that no longer matches the deployment sends the change to the wrong place. When they disagree, the running system wins and the document is wrong.
5. Write down what you learned in the repository, not in a chat. A model that lives only in this session is lost at the next one, and the next person repeats every dead end you just walked.

## Procedure

### Step 1, get it running

Follow the setup path the project already defines. Install the toolchain the manifest names, bring up the data stores it expects, and run the start command. Record every step that the documented instructions missed, because that gap is the first thing worth writing down.

Produce a working local instance, or a written statement of exactly where startup fails and what you tried. A failed startup that is documented is more useful than a vague claim that it runs.

### Step 2, find the real entry points

List where control actually enters the system: the HTTP routes, the message or queue consumers, the scheduled jobs, the command line entry points, and the startup hooks. Read the routing or registration code rather than trusting a directory named handlers, because files get renamed and moved.

Produce a short list of entry points with the file and function for each, and mark which ones the running instance actually exercises.

### Step 3, trace one path end to end

Pick one request or one job that matters and follow it from the entry point through every layer to the data store and back. Note each boundary it crosses, each external call it makes, and each place it reads configuration or state. Use a debugger or a log line at each hop if the path is not obvious from reading.

Produce a written trace of that one path, naming the functions in order and the side effects along the way. One traced path teaches more than ten skimmed files. The method and a worked example are in `references/trace-one-path.md`.

### Step 4, read the tests as the specification

Open the test suite and read what it asserts, not only whether it passes. The tests show which behaviours the authors cared about enough to lock down, which edge cases bit them before, and which parts have no coverage at all. Run the suite and note how long it takes and what it needs.

Produce a note of the behaviours the tests enforce and the areas with no tests, since the untested areas are where your model is weakest.

### Step 5, mine the version control history

Ask the log which files change together, which change constantly, and which have not been touched in a long time. Files that always change in the same commit have a hidden coupling worth knowing. Files nobody has edited in years are either stable or feared, and the commit messages usually say which.

```
git log --pretty=format: --name-only | sort | uniq -c | sort -rn | head -20
git log -1 --format=%ai -- path/to/file
```

Produce a list of the high churn files, the coupled sets, and the untouched files, with a one line note on what each pattern implies. The full set of commands is in `references/version-control-archaeology.md`.

### Step 6, map dependencies and data stores

List the external services the code calls, the databases and caches it reads and writes, the queues it uses, and the third party libraries it leans on hardest. For each data store, note who writes to it and what breaks if it is unavailable.

Produce a dependency map: internal modules, external services, and data stores, with the direction of each call.

### Step 7, reconcile documented and running architecture

Put the diagram or the written architecture next to what you traced and mapped. List every place they disagree: a service that no longer exists, a call that the diagram omits, a data store that moved. The running system is the source of truth.

Produce a list of the discrepancies, so the next reader does not trust the wrong picture.

### Step 8, write it down where it lasts

Write a short onboarding note into the repository: how to run it, the real entry points, the traced path, what the tests cover and miss, the churn and coupling findings, the dependency map, and the corrections to the documented architecture. Keep it to what you verified.

Produce a committed file that a new reader can follow to reach the same model in an hour instead of a week.

## Self-audit

- Did the project start locally, or is the exact point of failure written down?
- Is at least one real request or job traced from entry to data store and back?
- Are the entry points listed from the routing code rather than from directory names?
- Were the tests read for what they assert, with the untested areas named?
- Does the history report name the high churn files and the coupled sets?
- Is there a dependency map covering external services and data stores?
- Are the discrepancies between the documented and running architecture listed?
- Is the onboarding note committed to the repository rather than left in this session?

## Honest limits

This skill builds a model; it does not fix bugs or design changes. Once you know where a defect lives, the diagnosis belongs to `debug-method`, and deciding whether a structural change is worth making belongs to `arch-decide`.

The history commands assume git. Other version control systems expose the same information through different commands, and a repository with a shallow or squashed history hides the churn signal, so treat a thin log as missing data rather than as evidence of stability. The churn and coupling findings are rules of thumb about where risk concentrates, not proof that any single file is fragile.

Reading code for correctness or security is a separate job owned by `code-review` and `security-hardening`. This skill tells you how the system works, not whether it works safely.

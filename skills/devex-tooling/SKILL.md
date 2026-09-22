---
name: devex-tooling
description: Set up the build, dependency and tooling layer so the project is fast to work in and reproducible. Use when the user asks how to set up a project, choose a build tool or bundler, structure a monorepo, manage dependencies or lockfiles, configure linting, formatting, type checking or pre-commit hooks, speed up a slow build or a slow test run, or asks why it works on their machine and not another. Makes a clean checkout runnable with one documented command, pins versions so builds are reproducible, automates formatting rather than reviewing it, and keeps the feedback loop fast enough that people do not route around it. Triggers on project setup, monorepo, build tool, bundler, Vite, Webpack, Turborepo, Nx, package manager, lockfile, dependency management, eslint, prettier, pre-commit hooks, slow build, works on my machine, developer experience.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Development tooling

Two measurable goals. A new person gets the project running with one command, and the feedback loop after
a change is short enough that nobody skips it.

## Fit to the project

Measure what a clean checkout requires today before changing any of it, because the fastest win is
usually removing a step rather than adding a tool.

1. Clone into an empty directory and follow the written setup exactly as a newcomer would. Time it,
   and note every manual step, every undocumented dependency, and every place it fails. That
   transcript is the baseline the rest of the work improves.
2. Read the manifest and the lockfile to learn the declared package manager and its version, then
   check for a runtime version file such as `.nvmrc`, `.tool-versions`, `.python-version`, or a
   `rust-toolchain`. A repository with two lockfiles from two managers is the first thing to resolve.
3. Read the pipeline config to see which checks already run on a merge and how long they take, and
   read any `Makefile`, `Taskfile`, or `package.json` scripts to find the command a newcomer is meant
   to run. Reuse the command that exists rather than inventing a second one.
4. When nothing has been established, no lockfile, no version file, and no setup script, record that
   the feedback loop is currently unmeasured and start by writing the one command and pinning the
   versions before touching anything else.

## Non-negotiables

1. A clean checkout runs with one documented command. Test it by actually starting from a fresh clone. Setup instructions that have not been followed from scratch are wrong more often than not.
2. Pin versions. The lockfile is committed, the runtime version is declared in a file, and container base images are pinned by digest. Unpinned means the build is different tomorrow for reasons nobody will find.
3. Formatting is automated and never discussed in review. Any review comment about whitespace is a tooling failure.
4. Keep the pre-commit stage under a few seconds. A slow hook gets bypassed, and once people learn the bypass flag they use it for everything.
5. Never commit generated output or secrets. Both cause conflicts, and one of them causes incidents.
6. Every tool added has to earn its configuration. Three linters with overlapping rules produce arguments rather than quality.
7. Say what the tooling costs. Build time, install time, and the number of concepts a newcomer has to learn are real costs paid by every person on the project.

## Procedure

### Step 1, declare the runtime and the manager

Runtime version in a file the tooling reads, so everyone is on the same one. Declare the package manager
and its version too, because they produce different lockfiles and different resolution.

One package manager per repository. Two lockfiles in one project is a source of failures that appear only
in continuous integration.

### Step 2, one command to get running

A short script, or a small set of documented commands, that installs, prepares any local services, seeds
data, and starts the application. When that script grows past a few lines, write it under the
`code-craft` contract so the next person can read it: one job per function, names that say what runs,
and a comment on any step whose reason is not obvious.

Local dependencies such as a database belong in a container definition so nobody installs them by hand.
The engine version there must match production.

An example environment file, checked in, listing every variable with a description and a safe default.

Verify by running it from a fresh clone in a clean directory, and record how long it takes.

### Step 3, formatting, linting, types

A formatter with no options worth arguing about, running on save and in the pipeline. One configuration,
no per directory variation.

A linter configured for correctness rules rather than style, since style belongs to the formatter. Turn off
rules the team disagrees with instead of ignoring them inline everywhere, because a wall of suppression
comments means the configuration is wrong.

A type checker in strict mode from the start. Enabling strictness later is a large migration, and starting
strict costs almost nothing.

Every one of these runs in the pipeline, so a local skip is caught.

### Step 4, the feedback loop

Measure it. Time from saving a file to seeing the result, and time for the test suite. Write both numbers
down, because they decide whether the tooling helps or gets worked around.

Keep incremental rebuilds fast with a tool that does incremental work properly and caches. Cache
dependencies in the pipeline.

Split the suite so a change runs the relevant tests in seconds, with the full suite on push.

When the loop is slow, fix that before adding any further checks. Checks people skip provide nothing.

### Step 5, monorepo, only when it pays

A monorepo helps when packages change together, share types, and need atomic cross package changes. It
costs build orchestration, dependency graph management, and selective continuous integration.

Separate repositories are simpler until you are editing three of them for one feature, which is the signal
to combine.

In a monorepo: declare dependencies between packages explicitly, build only what changed and what depends
on it, keep one version of shared external dependencies, and make the task runner cache results by input
hash. Without caching, a monorepo is a slow repository.

Do not adopt a monorepo for two packages.

### Step 6, dependency discipline

Before adding a dependency: check whether the platform now does it, check the installed size, check how
many transitive dependencies arrive with it, check maintenance activity, and check the licence.

Keep runtime and development dependencies separated correctly, since it affects both image size and
vulnerability triage.

Update on a schedule rather than in an emergency. Automated update pull requests with a passing suite make
this routine, and batching minor updates keeps the noise manageable.

Review install scripts on anything new, because they execute with your permissions.

### Step 7, guard rails in the pipeline

Install, format check, lint, type check, test, build. Fail on any.

Cache dependencies and build output by lockfile hash.

Pin third party actions by digest.

Keep the required checks small and meaningful. A pipeline with thirty checks, five of which are flaky,
trains people to merge on red.

## Self-audit

- Fresh clone to running verified, with the command documented and the time recorded.
- Runtime, package manager and lockfile all pinned and committed.
- Formatter automated, and no style rules in the linter.
- Type checker strict and running in the pipeline.
- Feedback loop and suite duration measured and written down.
- Local services containerised at production versions.
- Example environment file complete.
- No generated output or secrets committed.
- Each tool justified by what it catches.

## Reference material

`references/pinning-map.md` lists, per ecosystem, the file that pins the runtime, the lockfile the
package manager writes, and how to pin a container base image by digest, so nothing is left floating.

`references/loop-budgets.md` gives target times for each stage of the feedback loop, from save to
result and from commit to a green pipeline, with what to do when a stage is over budget.

## When to stay off

Skip the full setup for a one off script, a spike that will be deleted this week, or a repository that
already has a working one command checkout and a fast loop. Adding a monorepo tool or a fourth linter
to a project that runs fine is cost with no return.

Saying "stop", "just execute", or "skip the tooling" is the off switch. It stays off for the rest of
the session unless the user asks again. Tooling advice that keeps arriving unbidden is the fastest way
to get the whole collection uninstalled.

## Honest limits

This skill sets up the build, dependency, and feedback layer. It does not organise the application
code that layer compiles, which is the `code-craft` contract, and it does not decide which tests run
in the pipeline or whether they cover the right paths, which is `test-strategy`.

The times in `references/loop-budgets.md` are targets drawn from what teams tolerate, not measurements
of your machine, so replace them with your own recorded numbers. Whether a dependency is safe to add
is a risk judgement this skill frames but cannot settle; a known advisory in the tree is a `ship-audit`
finding.

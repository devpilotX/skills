---
name: release-manage
description: Ship changes to users in a way that limits damage and can be undone quickly. Use when the user asks how to release, version, tag or roll out a change, asks about semantic versioning, changelogs, feature flags, canary or staged rollout, blue green deploys, deprecating an API or a feature, handling a breaking change, or asks what to do when a release goes wrong. Separates deploying code from releasing behaviour so a bad change is switched off rather than rolled back, defines the abort condition and who watches it before the rollout starts, and requires that deprecation comes with a date and a migration path. Triggers on how do I release, versioning, semantic versioning, changelog, feature flags, canary release, staged rollout, blue green, breaking change, deprecate, rollback, hotfix, release process, incident.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
---

# Release management

Deploying code and releasing behaviour are two different events. Separating them is what turns a bad change
from an incident into a toggle.

## Non-negotiables

1. Every rollout has an abort condition defined before it starts, with a metric, a threshold, and a named person watching. A rollout with no abort condition is not being monitored, it is being hoped over.
2. Rollback has been performed at least once on purpose, and its duration is written down. An untested rollback is a plan, not a capability.
3. Behaviour changes go behind a flag when they are risky, so disabling does not need a deploy. A deploy in the middle of an incident is slow and adds risk.
4. Every breaking change gets a version, a changelog entry written for users, and a migration path. A breaking change with no migration note is an outage scheduled for your customers.
5. Deprecation comes with a date, a replacement, and a way to detect who is still using the old thing. Without usage data, removal is a guess.
6. Never ship on Friday afternoon without a reason and the people available to handle it. This is not superstition. It is about who is awake when it fails.
7. One change per release where possible. A release containing eight changes gives no information about which one caused the problem.

## Fit to the project

Read how this project already ships before proposing a process, because a release procedure that
fights the existing pipeline gets bypassed under deadline.

Find the version scheme in use: a tag pattern in version control, a version field in the package
manifest, or a date stamp on build artefacts. Note whether other people import this thing, which
decides whether semantic versioning applies or a build number is enough. Read the deploy configuration
next, the CI pipeline definition or the deploy scripts, to see whether deploy and release are already
separated or whether every deploy is a release.

Look for an existing changelog and read its format, since a second format alongside it helps nobody.
Search for a feature flag system already in the code, a flag library or a config driven toggle, before
proposing a new one. Check whether a rollback has ever been run by reading the deploy history or asking,
because an untested rollback is the most common false assumption in a release plan.

When the project has settled nothing, no version scheme, no changelog, no flags, no rollback drill,
start with a version scheme that matches whether the thing is imported, one abort condition, and a
practised rollback, and add the rest as the release cadence demands it.

## When to stay off

Skip the full release apparatus for a personal project with one user, a spike that will be thrown away,
or an internal tool where the author is the only operator and the only affected party. Feature flags
and staged rollouts for an audience of one add ceremony without reducing risk.

Saying "stop", "just execute", or "skip the release process" is the off switch. It stays off for the
rest of the session unless the skill is invoked again. A process that insists on canaries for a
single user script is the kind of overhead that gets the whole practice abandoned.

## Procedure

### Step 1, version the change

Use [semantic versioning](https://semver.org/) for anything other people depend on, and mean it. The major
number changes when consumers must do work. Making an optional field required is a major change, even
though it feels small.

For an application nobody imports, a date or a build number is fine, and arguing about semantics is wasted
effort.

What counts as breaking, and is routinely misjudged: removing or renaming anything public, changing a type,
making optional required, narrowing accepted input, changing a default, changing the meaning of an error
code, and changing behaviour that consumers depend on even if the signature is unchanged.

Tag the release in version control, and make the artefact traceable to the commit.

For the full list of changes that are breaking even when they look small, with the version bump each
one forces, see `references/breaking-changes.md`.

### Step 2, write the changelog for the reader who decides whether to upgrade

Write for the person deciding whether to upgrade, not for the person who wrote the code.

Group by what it means to a user. Breaking changes first, with the migration step inline, then additions,
then fixes described by the symptom that is gone.

"Fixed a race in the session cache" tells a user nothing. "You no longer get logged out when two tabs
refresh at once" tells them whether to upgrade.

Generated commit lists are not a changelog. They are raw material for one.

### Step 3, put risky behaviour behind a flag

Flag anything risky, anything large, and anything needing a staged rollout.

Keep flags boolean and simple. Flags that interact combinatorially produce states nobody tested.

Give every flag an owner and a removal date at creation. Old flags accumulate into untestable
configuration, which is a real and common form of debt.

Default to off, and make the off path the existing behaviour, so a failure to evaluate the flag is safe.

Test both sides. A flag whose on path was never tested is a deploy waiting to fail.

Remove the flag after the rollout completes. That is part of the work, not a follow up someone will
remember.

### Step 4, choose the rollout shape

All at once suits low risk changes on small systems. Simple, and the blast radius is everyone.

Canary sends a small share of traffic to the new version, which limits exposure and needs per version
metrics to be useful. Without separate metrics, a canary is just a slower deploy.

Staged by cohort, for example internal users, then one percent, then ten, then everyone, with a defined
wait at each stage and the abort condition checked. The wait has to be long enough for the problem to
appear, which for anything data related means hours rather than minutes.

Blue green switches traffic between two full environments, giving a fast switch back at the cost of running
two environments and handling shared state, particularly the database.

Dark launch runs the new path without exposing results, which is the only way to test performance at real
traffic before anyone depends on it.

Pick by what a failure costs and how quickly it would be visible.

For each shape set against what it costs, what it needs, and when it is the wrong choice, see
`references/rollout-shapes.md`.

### Step 5, handle a bad release

Mitigate before diagnosing. Turn off the flag, or roll back, and only then work out why. Diagnosing while
users are affected is the wrong order, and the temptation to understand first is strong.

Prefer the flag to a rollback, and a rollback to a forward fix. A forward fix under pressure is how a
second incident starts.

If a migration already ran, rolling back the code may not be safe. This is exactly why migrations must be
compatible with both versions, and why that rule is worth the discipline.

Communicate early with what is known, what is not, and when the next update comes. Users forgive outages
and remember silence.

Write the incident up afterwards, focused on the system rather than the person. The useful output is the
change that makes the class of failure impossible, not a note asking people to be careful.

### Step 6, deprecate on a schedule

Announce with a date, in the changelog and directly to the people affected.

Add usage telemetry so you know who is still calling it, otherwise removal is guesswork.

Return a deprecation signal, such as a response header, so it appears in consumers' own logs.

Keep the old path working for the stated period, and remove it on the stated date. Extending indefinitely
teaches everyone to ignore the next announcement.

For a widely used interface, provide a tool or a script that performs the migration.

## Self-audit

- Abort condition with a metric, a threshold and a watcher, defined before the rollout.
- Rollback practised, with its duration recorded.
- Risky behaviour behind a flag, with both paths tested and a removal date set.
- Version number reflects whether consumers must act.
- Changelog written in terms of user effect, with migration steps for breaking changes.
- Migrations compatible with both the old and new code.
- Deprecations carry a date, a replacement and usage telemetry.
- Release size kept small enough to attribute a failure.

## Honest limits

This skill governs how a change reaches users and how to pull it back. It does not run the deploy
itself. The environment, the pipeline mechanics, and the infrastructure that a rollout targets belong
to `infra-deploy`, and the abort condition here assumes a deploy system that can actually switch
versions.

It does not tell you what to do while users are affected beyond mitigate first. Once a release becomes
an outage, the roles, the timeline, and the write up are `incident-response`. The metric and threshold
that an abort condition watches have to come from real monitoring, which `observability-setup` owns,
and a staged rollout without per version metrics is guesswork. The tagging and traceability described
in the version step lean on the conventions in `git-discipline`, and a migration that must stay
compatible with both code versions is planned with `migration-plan`.

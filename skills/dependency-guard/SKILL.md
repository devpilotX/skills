---
name: dependency-guard
description: Treat dependencies as an attack surface and a maintenance cost, not free code. Use when adding a package, when a vulnerability advisory lands, when deciding an upgrade cadence, when a build is not reproducible, when a lockfile is missing or uncommitted, when checking whether a package is safe to add, or when a license question comes up before shipping. Pins versions and commits the lockfile, upgrades on a cadence that avoids both breakage and a two year backlog, responds to an advisory by reachability rather than severity alone, checks a package for typosquatting and maintenance before adding it, and flags license obligations that bite at distribution. Triggers on add a dependency, is this package safe, npm audit, pip audit, cargo audit, security advisory, CVE in a dependency, should I upgrade, lockfile, pin versions, transitive dependency, typosquatting, is this package maintained, license compliance, reproducible build, supply chain.
license: MIT
compatibility: Any language and any package ecosystem with a manifest and a lockfile. The audit commands shown are examples; use the one your ecosystem ships.
metadata:
  version: 1.0.0
  suite: skills
---

# Dependency guard

A dependency is someone else's code running with your permissions, upgrading on their schedule, and
carrying their bugs and their advisories. The default move is to add whatever import makes the error
go away, pin nothing, and never look again until an audit tool turns red and a severity score triggers
a panic upgrade that breaks the build. That pattern adds attack surface nobody reviewed and a
maintenance debt nobody scheduled.

This skill decides what to add, how to pin it, when to upgrade, and how to respond to an advisory by
what an attacker can actually reach.

## Fit to the project

Read how the project already manages dependencies before changing the policy.

1. Find the manifest and the lockfile for each ecosystem in the repository. Confirm the lockfile is
   committed. A manifest with version ranges and no committed lockfile means every install can pull
   different code, so this is the first thing to check.
2. Find the audit tool the ecosystem ships and run it to see the current baseline. Note whether it
   separates runtime from development dependencies, because the risk differs.
3. Read how upgrades happen today: a bot that opens pull requests, a manual quarterly sweep, or
   nothing. A backlog of hundreds of pending updates tells you the cadence is broken.
4. Check whether the build is reproducible: does installing from the lockfile on a clean checkout
   produce the same dependency tree twice. If it does not, no advisory response can be trusted.

## Non-negotiables

1. Commit the lockfile and install from it in continuous integration and release. Without a committed
   lockfile, the version that passed your tests is not the version that ships, and an advisory
   response cannot know what is actually deployed.
2. Respond to an advisory by reachability, not severity alone. A critical score on a code path your
   application never calls ranks below a medium on a function you call on every request. Severity is
   the ceiling of the impact, not the impact.
3. Check a new package for name confusion and maintenance before adding it. A typosquatted name one
   character off a popular package, or an abandoned package with a lone maintainer and a years old last
   release, is a compromise waiting to happen. Adding it first and reviewing later is backwards.
4. Do not run install scripts from an unreviewed dependency in a trusted environment. A package's
   install hook runs arbitrary code with your permissions the moment you add it, so a fresh or unknown
   package gets reviewed before it touches a machine that holds credentials.
5. Upgrade on a cadence. Neither pin everything forever, which builds a backlog that becomes unpatched
   by the time an advisory lands, nor auto merge every update blind, which ships a compromised release
   the moment it is published. A small regular sweep with tests is the path between both failures.

## Procedure

### Step 1, pin and lock

Pin direct dependencies to a specific version or a narrow range, and commit the lockfile that resolves
the full transitive tree to exact versions. Configure continuous integration to install from the
lockfile in frozen mode so a drifted lockfile fails the build rather than silently resolving new
versions. The reasoning on pinning depth and ranges is in `references/pinning-and-cadence.md`.

### Step 2, review before adding

Before adding a package, check four things. That the name is exactly the package you meant, not a
typosquat one character off or a namespace lookalike. That it is maintained: a recent release, an
active issue tracker, more than one maintainer where the ecosystem shows that. That it is actually
needed, rather than a large dependency pulled in for one small function you could write. And what it
pulls in transitively, because a shallow direct list can hide a deep tree. The checklist is in
`references/adding-a-package.md`.

### Step 3, respond to an advisory by reachability

When an advisory lands, do not upgrade on the score alone. First determine whether your code reaches
the vulnerable function: is the package a runtime or a development dependency, do you call the affected
API, and is the vulnerable path exposed to untrusted input. A vulnerability in a build tool that never
runs in production is a different urgency from the same score in a request handler. Then fix in this
order: upgrade to a patched version if one exists, apply the maintainer's mitigation if not, and only
then consider removing or replacing the package. Record the reachability judgement so the next person
does not re-litigate it.

### Step 4, keep upgrades flowing

Run a regular upgrade sweep, sized so it never becomes a wall. Take patch and minor updates on a short
cycle behind the test suite, and schedule major updates deliberately because they carry breaking
changes. A bot that opens update pull requests is fine as long as a human or a green test suite gates
the merge rather than auto merging on publish. The cadence tradeoff is in
`references/pinning-and-cadence.md`.

### Step 5, verify reproducibility and licenses

Confirm a clean checkout installing from the lockfile produces the same tree twice; a build that pulls
different code each run cannot be audited or rolled back with confidence. Then check licenses for
obligations that bite at distribution: a copyleft license on a dependency you ship can require you to
release your own source, and a missing or incompatible license is a legal risk that only surfaces when
you distribute. The license notes are in `references/adding-a-package.md`.

## Self-audit

- Is the lockfile committed, and does continuous integration install from it in frozen mode?
- Was every new package checked for a typosquatted or lookalike name before it was added?
- Is each dependency maintained, with a recent release and more than a single point of failure where
  the ecosystem shows it?
- Was the latest advisory response driven by reachability, with the runtime versus development split
  and the call path recorded?
- Are install scripts from new or unknown packages reviewed before they run in an environment with
  credentials?
- Does a clean checkout produce the same dependency tree twice?
- Are the licenses of shipped dependencies checked for obligations that apply at distribution?
- Is there a regular upgrade cadence rather than a frozen tree or a blind auto merge?

## Honest limits

This skill manages dependencies. It does not perform the wider security review of your own code:
injection, authentication, and output handling belong to `security-hardening`, which also owns how to
read and rank the advisories themselves in a full audit.

The cadence intervals and the maintenance signals here are rules of thumb, not measurements, and a
regulated or high assurance project will set stricter ones. This skill does not give legal advice on
license compatibility; a genuine licensing question at distribution is for a lawyer, and the release
process itself is owned by `release-manage`.

## Off switch

If the user says "stop", "just execute", or "skip the dependency review", stand down and make only
the change asked for. The off switch holds until the skill is invoked again.

# Pinning and upgrade cadence

Two failures sit at opposite ends. Pin nothing and every install pulls different code, so a build that
passed tests is not the build that ships. Pin everything and never move, and the tree rots until an
advisory lands on a version too old to patch without a large jump. The working position is between
them.

## What to pin, and how deep

Pin direct dependencies in the manifest to a specific version or a deliberately narrow range. The
lockfile then resolves the entire transitive tree to exact versions and hashes. The manifest records
intent; the lockfile records what actually resolves. Commit both.

Transitive depth is where the surface hides. A short direct list can pull in a tree hundreds of
packages deep, and every one of them runs with your permissions. Prefer a smaller direct dependency
with a shallow tree over a larger one that drags in dozens of transitive packages for a feature you
do not use.

Install from the lockfile in a frozen or locked mode in continuous integration and release, so a
lockfile that drifted from the manifest fails the build rather than quietly resolving something new.

## Ranges versus exact pins

An exact pin on a direct dependency gives the most control and the most manual upkeep. A narrow range
that allows patch updates lets security patches flow with less friction, which is usually the better
tradeoff for applications, as long as the lockfile still pins the resolved version exactly.

A library published for others to depend on is different: overly tight pins there create conflicts for
the consumers, so libraries usually declare compatible ranges and leave the exact resolution to the
application that consumes them.

## Cadence that avoids both traps

As a rule of thumb, take patch and minor updates on a short cycle, weekly or every couple of weeks,
gated by the test suite. These rarely break and often carry security fixes, so letting them accumulate
is the more expensive choice.

Schedule major updates deliberately, one at a time, because each can carry breaking changes and
migration work. Batching several majors into one sweep makes the failure hard to attribute.

A bot that opens update pull requests keeps the flow visible. The safe pattern is that a human or a
passing test suite gates the merge. Auto merging on publish removes the one check that would catch a
compromised release in the window before the ecosystem flags it.

## Why a blind auto merge is dangerous

A package account can be compromised and a malicious version published. For a short window before the
ecosystem and scanners catch it, that version is the latest. A pipeline that upgrades to latest and
auto merges installs it in that window. Gating on tests does not catch a subtle backdoor, but the
delay from a human review step often outlasts the window in which the bad version is live.

## When to remove rather than upgrade

Some dependencies are cheaper to drop than to maintain. A package used for one small function, an
abandoned package with no patched version, or one whose transitive tree keeps generating advisories.
Removing it removes the surface permanently, which beats patching it repeatedly.

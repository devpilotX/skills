---
name: migration-plan
description: Move a system from one technology, provider or version to another without a cutover weekend. Use when the user asks how to migrate, port or move between databases, frameworks, languages, cloud providers, authentication systems or major versions, asks how to escape a vendor, asks about zero downtime data migration, dual writing or backfilling, or asks whether to upgrade or replace. Plans an incremental path with both systems running and traffic moved in slices, requires a tested reversal at every step, makes correctness verifiable by comparing the two systems on live traffic, and states the cost of the parallel running period that big bang plans leave out. Triggers on migrate from, port to, move off, switch database, upgrade major version, zero downtime migration, dual write, backfill, vendor lock in, replatform, cutover.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Migration planning

A single cutover concentrates all the risk into one irreversible moment, usually at night, with a tired
team. The alternative is running both systems and moving traffic in slices, each one reversible.

A migration ships code that lives only for the transition: the dual write path, the comparison code,
the backfill runner, the routing shim. Hold that code to the `code-craft` contract while it exists, so
the scaffolding you will later remove is readable enough to remove safely rather than being the mess
that never gets torn down.

## Fit to the project

Map the source system and everything wired to it before choosing a target, because the size of a
migration is set by the dependants, not by the thing being moved.

Read what the source actually is first: the exact engine and version, the schema or interface, and the
configuration that reveals the behaviour consumers may lean on, such as collation, isolation level, or
identifier format. Then find the target's real limits by reading its own documentation or running a
probe, rather than assuming it behaves the same, since recall is not verification.

Inventory the dependants next, across the whole organisation and not only the main application. Search
the codebases for every reader and writer, and list the scripts, reports, dashboards, scheduled jobs,
and third party integrations that touch the source. Get the data volume and its growth rate from the
source itself, because that decides whether a backfill is hours or weeks. Check whether a tested
restore exists for this data, and whether there is any comparison mechanism already in place.

When the project has settled nothing, no target chosen and no inventory done, do not plan a cutover.
Run the inventory step first and prove the hardest slice against a candidate target, then let those two
results size the plan.

## When to stay off

Skip the parallel running apparatus when the move is genuinely small and reversible on its own: a
config change with an immediate rollback, a single stateless service with no data to carry, or a
dependency bump that a version control revert undoes. Dual writes and shadow reads for a change you can
undo in one commit add weeks of scaffolding to a one line revert.

Saying "stop", "just execute", or "skip the migration plan" is the off switch. It stays off for the
rest of the session unless the plan is asked for again. Insisting on a full parallel run for a
trivially reversible change is how a small task turns into a quarter of maintained shims.

## Non-negotiables

1. Every step is reversible on its own. If a step cannot be undone, it gets split until it can, or it is scheduled as a known point of no return with its own preparation.
2. Both systems run in parallel during the transition, and that cost is stated in money and in attention. Plans that omit it are the ones that get approved and then abandoned halfway.
3. Correctness is verified by comparison on live traffic, not by hoping. Shadow reads, then compare, then report the mismatch rate.
4. A tested restore exists before any data is moved, and it was tested on this data.
5. The deadline for finishing the transition is part of the plan. A migration that stalls at eighty percent leaves two systems to maintain forever, which is worse than either alone.
6. Never migrate and redesign at the same time. Move first, improve after. Combining them means a failure cannot be attributed and the comparison is impossible.
7. Retrieve the target's actual limits and behaviour rather than assuming parity. Different engines and providers differ in ways that break assumptions, and recall is not verification.

## Procedure

### Step 1, be honest about why

Write the reason down, and check it survives scrutiny. Cost, a capability that is genuinely required, an
unsupported version, or a limit being hit.

Then ask whether an upgrade in place achieves it, because it usually costs a fraction of a migration.

If the reason is that the current system is unpleasant to work with, a migration will not fix that for long.
Say so.

### Step 2, inventory what depends on it

This is the step that determines the true size, and skipping it is why migrations run over.

Every reader and writer, including scripts, reports, dashboards, scheduled jobs, third party integrations,
and the one internal tool nobody remembers. Search the whole organisation's code, not only the main
application.

Every behaviour depended upon that is not in the documentation: ordering guarantees, case sensitivity,
collation, precision, null handling, timezone behaviour, identifier format, transaction isolation, and
error codes. These are where migrations break, because both systems claim to do the same thing.

Data volume and growth, which decides whether a backfill takes hours or weeks.

For the full list of dependant classes to hunt down and the undocumented behaviours that break parity,
see `references/inventory-worksheet.md`.

### Step 3, prove it on a slice

Before committing, take the hardest representative piece and make it work end to end against the target.
Not the easiest piece. The one you are least sure about.

This finds the incompatibility that changes the plan, while changing the plan is still cheap.

Measure performance on real data volume. A target that is slower on the main query changes everything.

### Step 4, choose the pattern

For data stores, dual write with shadow reads. Write to both, keep reading from the old one, read from the
new one in parallel and compare without using the result. Report the mismatch rate, fix the causes, and
only move reads when it is at zero for a sustained period. Then stop writing to the old one after a safety
period during which returning is still possible.

For services and applications, put a routing layer in front and move one route, one feature or one cohort
at a time. Each move is small, observable and reversible. The old system keeps serving everything not yet
moved.

For frameworks and languages, run the new one alongside for new code and migrate modules at boundaries,
rather than converting everything then testing everything.

For major version upgrades, upgrade dependencies first, fix deprecation warnings on the current version
next, then move. Most of the work is usually in the deprecations, and doing it before the jump keeps the
steps separate.

For providers, move stateless compute first, data last, and check the egress cost before starting, since
moving data out is frequently the largest single line in the whole project.

For the dual write and shadow read sequence broken into the ordered stages that keep the exit open, see
`references/dual-write-checklist.md`.

### Step 5, backfill carefully

In batches, with a pause between them, and resumable from where it stopped.

Record progress durably, so a restart does not begin again.

Run it against production load and watch the effect. A backfill can saturate the database and cause the
outage the migration was meant to avoid.

Verify by comparing counts and checksums per batch, not only at the end.

Handle the records that fail, and keep a list of them rather than letting them disappear into a log.

### Step 6, move traffic and keep the exit open

Move in increments with a wait at each, watching error rate, latency and the business metric that proves
the system works.

Keep the ability to return until the old system is genuinely no longer needed, which is later than it
feels.

Define the point of no return explicitly, and prepare for it specifically. Usually it is the moment writes
stop going to the old system.

### Step 7, finish it

Decommission on a date. Remove the dual write code, the comparison code, the routing shims and the flags.
A migration that leaves its scaffolding behind has added complexity rather than removed it.

Update the documentation and the runbooks, since the old ones now describe a system that no longer exists.

Record what the migration actually cost against the estimate, because that is the only way the next
estimate improves.

## Self-audit

- The reason is written down, and upgrading in place was considered.
- Full inventory of dependants, including scripts and reports outside the main application.
- Undocumented behavioural dependencies listed and checked against the target.
- The hardest slice proven end to end before committing.
- Restore tested on this data.
- Comparison on live traffic with a reported mismatch rate.
- Backfill batched, resumable, and verified per batch.
- Every step reversible, with the point of no return named.
- Parallel running cost stated.
- Decommission date set, with scaffolding removal included.

## Honest limits

This skill plans the path and keeps it reversible. It does not perform the individual cutover of each
slice. Moving traffic in increments, defining the abort condition, and versioning the change belong to
`release-manage`, and this plan assumes that machinery exists to switch a slice back.

It stops at reading the source's behaviour and the target's limits; the schema design, the query
shapes, and the index choices on the new store are `data-layer` work. The comparison on live traffic
needs somewhere to send the mismatch rate, which is `observability-setup`. The egress and parallel
running costs quoted here come from the project's own provider bill and volume figures, not from a
price sheet, so `cost-control` owns the number. When a slice fails mid transition and users are
affected, that is `incident-response`, and a major version jump inside the migration follows the
deprecation rules in `release-manage`.

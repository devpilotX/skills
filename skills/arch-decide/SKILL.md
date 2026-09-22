---
name: arch-decide
description: Choose a technical architecture and record the decision with its reversibility and consequences. Use when the user asks how to structure a system, whether to use a monolith or microservices, which database or queue or framework to pick, how services should communicate, whether to go serverless, how to split a codebase, or asks for a technical design or an architecture decision record. Also use when a choice is hard to reverse later. Classifies the decision by how expensive reversal is, spends effort in proportion to that, gives three genuinely different options with what each makes hard later, states the argument against the recommendation, and writes an immutable decision record. Refuses to recommend complexity the team size cannot operate. Triggers on monolith or microservices, which database should I use, how should I structure, system design, architecture decision, ADR, serverless or containers, sync or async, should I split this service, tech stack choice.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
---

# Architecture decisions

Effort spent on a decision should match the cost of reversing it. Most architecture argument is spent on
cheap decisions while the expensive ones get made by default.

If the user has already picked the shape and wants it built rather than questioned, the off switch is
saying "just execute" or "stop". After that this skill stops proposing options and records the choice as
given, and it stays off for the rest of the session unless the user asks for a decision again.

## Classify first

Before discussing options, say which kind of decision this is. The classification determines how much
process it deserves.

One way doors, where reversal costs months. The data model, the primary datastore, the public API shape,
the tenancy model, the authentication model, the choice to split into separate deployable services, and
anything that lands in a customer's integration. These justify research, options and a written record.

Two way doors, where reversal costs days. Internal library choices, code layout, the CI provider, most
framework choices inside an established stack, log format. Pick a reasonable option, note why, move on.
Debating these is the most common form of procrastination in engineering.

Hidden one way doors, which look cheap and are not. A queue whose message format leaks into consumers, a
third party for anything holding customer data, an identifier format that reaches other systems, and any
vendor whose export path was never checked. Ask early how you would get out.

State the classification in the first two lines of any architecture answer.

The questions that place a decision on the scale, a team sizing table, and a worked example from
classification through to a written record are in `references/reversal-cost.md`.

## Fit to the project

Read what the project has already committed to before offering any option. A design that ignores the
existing shape is a rewrite in disguise.

1. Look for existing decision records under docs/decisions or an adr directory, plus any design doc or
   readme that states the intended shape. A choice already recorded is context, not an open question, and
   reopening it needs a reason.
2. Detect the current deployment shape from what is checked in: a single application with one datastore, a
   set of services with a compose or manifest file, a serverless config. Count the deployables and the
   datastores that actually exist, not the ones the user describes.
3. Read who operates it. Find the on call rotation, the runbook, or failing those, the commit history that
   shows how many people touch the infrastructure. The count caps how much operational surface a new design
   can add.
4. Check what the team already knows by reading the languages and frameworks in use. A choice the team has
   run in production before carries far less risk than one they would learn under load.

When the project has settled nothing, say so, then propose the simplest shape that meets the stated forces
and record it as the starting point rather than treating the absence as license for complexity.

## Non-negotiables

1. Match the design to the team that operates it. A four person team running twelve services spends its capacity on the platform instead of the product. Say the operational cost in people, not just in components.
2. No option list that is one real option plus two strawmen. Each option must be one a competent engineer would defend.
3. Give the argument against your recommendation. If you cannot, you do not understand the tradeoff yet.
4. Verify the constraint, do not recall it. Limits, quotas, pricing, version compatibility and feature availability change. Retrieve them with a date, or mark them as unverified.
5. Name what each option makes hard later, since that is what people regret rather than what it makes hard now.
6. Prefer the boring option unless a named requirement rules it out. Novelty is a cost paid in debugging at the worst time.
7. Never propose a distributed system to solve a problem that is a missing index.

## Procedure

### Step 1, extract the forces

A decision only has an answer once the constraints are known. Get these before designing.

Load, meaning current and expected requests, data volume and growth, and whether traffic is steady or
spiky. An honest answer here usually shrinks the design.

Consistency needs, meaning which operations must be correct immediately and which can settle later.
This single question decides more architecture than any other.

Team, meaning how many engineers, what they already know, who is on call, and what happens at 3am.

Constraints that are already fixed: existing systems, contracts, regulatory requirements, data
residency, budget, deadline.

Failure tolerance, meaning what breaks for whom when a part goes down, and how long is acceptable.

When load is unknown, say that the design assumes a range, state the range, and note the point at which
the design needs revisiting. A number with a threshold beats a vague promise to scale.

### Step 2, generate three real options

Force variety. One option should be the simplest thing that could work, usually a single deployable
application with one database. One should be the conventional answer for this class of problem. One
should exploit something specific about this situation, which is where the good answers usually live.

Common tradeoff analyses for recurring decisions are in `references/tradeoffs.md`, covering deployment
shape, service communication, datastore selection, caching, tenancy and state placement.

### Step 3, cost each option honestly

For each: build effort, operational burden in ongoing hours, running cost at expected load, what it makes
hard later, the failure mode it introduces, and what the team has to learn.

Operational burden is the number that gets omitted and then dominates. Count it.

### Step 4, recommend and argue against

One recommendation. Then the strongest case against it, and the condition under which the other option
wins. Name the threshold in numbers where possible, as in this design holds to roughly a thousand writes
per second and then needs partitioning.

### Step 5, record it

Write the decision record using the shape in `doc-forge`, at `docs/decisions/NNNN-title.md`. Context,
decision, options considered, consequences, and reversal cost.

Keep records immutable. When a decision changes, add a new record and mark the old one superseded with a
link. An edited record loses the reasoning that made it worth keeping.

## Anti-patterns worth naming directly

Resume driven design, meaning the choice that is interesting to build rather than cheap to run.

Scaling for load that does not exist, which buys complexity now against revenue that is hypothetical.
The cost is paid in slower delivery, which makes the revenue less likely.

Splitting services along team boundaries that will change, rather than along data ownership that will
not.

Shared database between services, which produces the operational cost of distribution with the coupling
of a monolith.

Distributed transactions, which are almost always a sign the boundary is in the wrong place.

Event driven design adopted for its own sake, which converts a readable call stack into a debugging
exercise across seven logs.

A cache added to fix a query that has no index.

Premature abstraction over a second case that never arrives.

A vendor chosen without checking the export path.

## Self-audit

- The decision is classified as one way, two way, or hidden one way, in the first lines.
- Three defensible options, each with what it makes hard later.
- Operational burden is stated in ongoing hours or headcount.
- Every external limit or price is retrieved with a date, or marked unverified.
- The argument against the recommendation is present.
- The threshold at which the recommendation changes is numeric where it can be.
- The design is operable by the team that actually exists.
- A decision record was written for anything one way.

## Honest limits

This skill picks a shape and records the reasoning. It does not write the schema behind the datastore
choice, which belongs to `data-layer`, nor the service internals once the boundaries are set, which belong
to `backend-build`. The decision record format it points at is owned by `doc-forge`.

The team sizing table in `references/reversal-cost.md` comes from what small teams can operate in practice,
not from a study, so treat the rows as a starting point and adjust them to the team in front of you. Any
vendor limit, quota or price named while comparing options must be retrieved with a date, because those
change faster than this file does.

# Reversal cost worksheet

The classification in the main file decides how much process a decision earns. This file gives the
questions that place a decision on the scale, a worked example of the whole flow, and a filled decision
record you can copy the shape of.

## Score the reversal cost

Answer these for the decision in front of you. Each yes pushes the decision toward one way door.

1. Does the choice change data that is already written and would need a migration to undo?
2. Does the choice appear in a contract, an integration, or a URL that someone outside the team depends on?
3. Would reversing it require every consumer to change at the same time as the producer?
4. Does the choice pick a vendor that holds customer data, where the export path is slow or unclear?
5. Does the choice set an identifier format that will travel into other systems?
6. Does reversing it need a coordinated deploy across more than one service?
7. Is the team that would do the reversal different from the team that made the choice?

Zero or one yes is a two way door. Pick a sane default and move on. Two to three is a hidden one way
door: cheap to build, costly to leave, so ask the exit question before committing. Four or more is a one
way door that earns research, three options, and a written record.

## Sizing the design to the team

The most common failure is a design the team cannot run. Use this as a sanity check, not a law.

| People on call | Services they can operate well | What tends to break past that |
| --- | --- | --- |
| 1 to 3 | 1 to 2 deployables, 1 datastore | On call burns out, deploys stall, nobody owns the second datastore |
| 4 to 8 | 3 to 5 deployables, shared platform | Cross service debugging eats the week, no owner for the message bus |
| 9 to 20 | 6 to 12 with a platform team | Coordination cost rises, integration tests go flaky |
| 20 plus | Many, with per team ownership | Only works once each service has a clear owning team |

If the count of services planned is higher than the row the team sits in, the design is buying operational
cost the team pays before the product earns anything.

## Worked example

Request: a two person team wants to split a working web application into six microservices because they
read that microservices scale.

Step 1, classify. Splitting into separate deployables changes deploy topology and on call. It is a one way
door. Score: yes to questions 3, 6, and the team size check. This earns the full process.

Step 2, forces. Load is 40 requests per second at peak, one region, one relational database at 12 percent
CPU. Two engineers, both on call. No regulatory constraint. The pain they described is a slow report page.

Step 3, three options.
Option A, keep the single deployable, add an index and a read replica for the report. Build effort low,
operational burden near zero, running cost one extra replica.
Option B, extract only the reporting workload into one background worker reading the replica. Build effort
medium, operational burden one more process to watch.
Option C, the six service split they asked for. Build effort high, operational burden a message bus, six
deploy pipelines, and distributed tracing, all run by two people.

Step 4, recommend and argue against. Recommend A. The report is slow because the query has no supporting
index and competes with writes, which the plan confirms. The case against A: if reporting volume grows past
what one replica serves, option B becomes the next step, and the threshold is roughly when the report
workload saturates the replica. Option C wins only at a team size and load neither of which exists here.

Step 5, record it. Write the ADR below and stop.

## Decision record shape

Copy this shape into docs/decisions/NNNN-title.md. Keep it immutable once merged.

```
# 0007 Keep the single deployable, index the report

Date: 2024-03-11
Status: accepted
Reversal cost: two way door, the index is dropped in one statement

## Context
The report page takes 9 seconds at peak. Load is 40 rps, one database at 12 percent CPU.
The team is two engineers who both carry the pager.

## Decision
Add a composite index for the report query and route the report read to a replica.
Do not split the application into services.

## Options considered
A. Index plus replica. Chosen.
B. Extract a reporting worker. Deferred until the replica saturates.
C. Six service split. Rejected: operational cost exceeds team capacity.

## Consequences
The report drops below 1 second on the plan. One replica is added to run and pay for.
When report volume saturates the replica, revisit with option B.
```

When the decision later changes, add a new record and mark this one superseded with a link to it. Editing
the record in place loses the reasoning that made it worth writing.

# Inventory worksheet

The main file calls the inventory the step that determines the true size, and skipping it is why
migrations run over. This is the full list of what to hunt down, where each kind hides, and the
undocumented behaviours that break parity even when both systems claim to do the same thing.

## Dependant classes to find

Work through every class. The one you forget is the one that pages you after the source is gone.

| Class | Where it hides | How to find it |
| --- | --- | --- |
| Application readers and writers | The main codebase | Search for the client, the connection string, the table or endpoint names |
| Scripts | Ops repos, cron definitions, one off tool folders | Search the whole organisation, not one repo |
| Reports and dashboards | BI tools, hosted analytics, exported spreadsheets | Ask the people who read them, not only the code |
| Scheduled jobs | Cron, task schedulers, workflow tools | Read the schedule definitions, not the app |
| Third party integrations | Webhooks, partner API calls, data exports | Check outbound configuration and partner docs |
| The forgotten internal tool | A team wiki, one person's memory | Ask around; this is the one that is never in code search |

The main file names the last row directly: the one internal tool nobody remembers. Budget time to find
it, because it will not surface in a code search.

## Undocumented behaviours that break parity

Both systems claim to store the same data or serve the same interface. These are the differences that
are real and are not in either system's headline description. Check each against the target before
committing.

Ordering guarantees. Does the source return rows in insertion order without an explicit sort? Many do
by accident, and consumers come to rely on it. The target may not.

Case sensitivity. Are string comparisons and lookups case sensitive? A move between engines often flips
this, and a login or a key lookup that worked starts failing.

Collation. How are strings sorted and compared? A different collation reorders results and changes
which rows a range query returns.

Precision. How many digits does a number keep? Money and timestamps are where a precision change causes
silent corruption.

Null handling. Does the source treat empty string and null the same? Does a unique constraint allow
multiple nulls? Engines differ.

Timezone behaviour. Are timestamps stored with a zone, in UTC, or naive? A naive timestamp that meant
one zone on the source and another on the target is a data bug that surfaces months later.

Identifier format. Are keys integers, UUIDs, or strings with a structure consumers parse? A format
change breaks every consumer that reads meaning out of the identifier.

Transaction isolation. What does a reader see mid transaction? A weaker isolation level on the target
exposes states the application never had to handle.

Error codes. What does the system return on a conflict, a timeout, a missing row? Handlers keyed on the
old codes misbehave against the new ones.

## Data volume and growth

Get the current row or record count and the growth rate from the source, not from a guess. This single
figure decides whether the backfill runs in hours or weeks, and it changes the whole shape of the plan.
A backfill that fits in a maintenance window is a different project from one that must run alongside
live traffic for a fortnight.

## Turning the inventory into the plan

Each dependant becomes a line to migrate or a consumer to notify. Each undocumented behaviour that the
target does not match becomes either a code change on the consumer or a reason to reconsider the
target. The volume figure sets the backfill design.

If any row in the dependant table is unknown, the inventory is not done. An unknown reader that still
writes to the old system after you stop dual writing is a data divergence you will not notice until it
matters. Close every row before choosing a pattern.

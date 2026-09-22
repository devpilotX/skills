# Schema patterns

Shapes that recur, with the failure each one avoids.

## Soft delete

Use a nullable deleted timestamp rather than a boolean, since you almost always want to know when.

The cost is that every query has to exclude deleted rows, and one that forgets shows deleted data.
Handle it at a layer that cannot be forgotten, such as a view or a default scope, rather than by
remembering in each query.

Unique constraints interact badly with soft delete. A unique email column blocks re-registration after
deletion. Use a partial unique index limited to rows where deleted is null.

Decide what deletion means for children. A soft deleted order with hard deleted lines is worse than
either choice made consistently.

Soft delete does not satisfy a legal deletion request, because the data is still there. Keep a real
deletion path for that, and decide what it leaves behind for referential integrity.

## History and audit

Two different needs, often conflated.

Audit answers who changed what and when, for accountability. Append only, never updated, with actor,
action, target, timestamp and the before and after values. Write it in the same transaction as the
change, or it will disagree with reality.

History answers what the value was at a point in time, for business logic. That needs valid from and
valid to columns on the entity itself, or a separate versions table, and it changes every query that
reads the entity.

Do not build history when audit is what was asked for, because temporal queries are considerably more
work.

Both tables grow without limit, so decide retention when creating them.

## Multi tenancy

A tenant identifier column on every tenant owned table, indexed, and present as the first column of most
composite indexes because it appears in every query.

Enforce the filter where forgetting it fails rather than returning everything. Row level security in the
database, or a query layer that requires the tenant, both work. Relying on each query to remember is how
cross tenant leaks happen.

Include the tenant in unique constraints. An email unique across the whole table prevents the same person
existing in two tenants, which is usually wrong.

Plan the export and the delete per tenant early, because both get requested and both are painful to
retrofit.

## Hierarchies

An adjacency list with a parent identifier is simple, and reading a whole subtree needs a recursive query,
which modern engines support well.

A materialised path, storing the ancestor chain as a string, makes subtree reads trivial and moves
expensive.

Closure tables make every query fast and writes expensive in space.

For a fixed shallow depth, separate columns beat all of these.

Choose on whether reads or moves dominate, and write down the depth assumption.

## Money

An integer count of minor units, or a fixed precision decimal. Never a float.

Store the currency with every amount. A schema with amounts and no currency column is a defect waiting
for the second market.

Store the exchange rate and its timestamp on any converted amount, since the rate at the time is part of
the record.

For anything ledger like, append only entries that sum to a balance beat a mutable balance column. A
mutable balance is correct until two writes race, and then it is silently wrong forever.

Round once, at the point of presentation or settlement, and record which way you rounded.

## Status and state machines

A status column with a foreign key to a lookup table, plus the allowed transitions written down
somewhere.

Store the timestamp for each meaningful transition rather than only the current status. Questions about
how long something sat in a state arrive later and cannot be answered retrospectively.

Guard the transition in one place. Status changes scattered across handlers produce impossible states.

## Scheduling and jobs

Store the scheduled instant in UTC, and separately store the user's intent if it is recurring, because a
weekly local time reminder is not a fixed UTC offset once daylight saving moves.

For a queue in the database, use the engine's skip locked support to claim rows, or several workers take
the same job.

Record attempt count and last error on the job row, so a stuck job is visible.

Index on the claim query, which is usually status plus run after time.

## Counters and aggregates

Incrementing a column is correct only when done atomically in the database. Reading, adding one, and
writing back loses updates under concurrency.

For high write counters, aggregate rather than contending on one row, since every writer serialises on
it.

For dashboard aggregates, a periodically refreshed summary usually beats computing across the whole
table on every page load. Say how stale it is allowed to be.

## Full text search

The built in search in a relational engine is adequate for far more cases than people expect, and it
avoids a second system to keep consistent.

When a dedicated index is genuinely needed, treat it as derived data that can be rebuilt from the
primary store, and never as the source of truth.

Decide how it gets reindexed after a bulk change, before you need it.

## Files and attachments

Metadata in the database, bytes in object storage. Storing large binaries in the database inflates
backups and slows everything that touches the table.

Store the checksum and the size, so corruption and truncation are detectable.

Decide what happens to the object when the row is deleted, since orphaned objects accumulate cost
quietly.

## Things that cause pain later

A nullable column used to mean false, which makes every boolean query wrong in one direction.

A column holding two meanings depending on another column.

Comma separated values in a text column, which is a missing table.

A timestamp without a zone.

A unique constraint added without checking for existing duplicates first, which fails the migration in
production after passing in development.

No index on a foreign key, which makes deletes on the parent slow and sometimes locking.

An append only table with no retention policy.

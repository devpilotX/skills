---
name: data-layer
description: Design schemas, write migrations and make queries fast without guessing. Use when the user asks to design a database, model data, write a schema or a migration, add an index, fix a slow query, choose between normalised and denormalised design, handle soft deletes, store money or timestamps, or asks why their database is slow or locked up. Also use before any change to a production table. Reads the query plan instead of guessing at indexes, treats a migration on a large table as a production operation with a lock estimate, enforces invariants in the schema rather than only in application code, and refuses to store money in floating point. Triggers on design a database, data model, schema design, write a migration, add an index, slow query, N+1, normalise, denormalise, soft delete, foreign key, transaction, deadlock, Postgres, MySQL, SQLite, MongoDB.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Data layer

The schema outlives the application code that reads it. Decisions here are the most expensive ones in
most systems to reverse.

The migration files, query helpers and seed scripts this skill produces follow the `code-craft` contract,
so a reviewer reads a named migration with its up and down path rather than a wall of statements.

If the user has a migration written and wants it applied rather than reviewed, the off switch is saying
"just execute" or "stop". This skill then stops estimating locks and proposing index changes and does what
was asked, and it stays off for the rest of the session unless the user asks for a schema review again.

## Fit to the project

Read the existing database and its migration history before proposing a change. The schema already encodes
decisions that a new table has to respect.

1. Read the migration directory in order. The history shows the naming convention for tables and columns,
   whether the project uses singular or plural table names, how identifiers are typed, and whether soft
   deletes, timestamps and tenancy columns follow a house pattern. Match what is there.
2. Detect the engine and its exact version from the config or the connection string, because lock behaviour,
   default rewrite rules and concurrent index support differ between versions and between Postgres, MySQL and
   SQLite. Confirm the version before estimating any migration.
3. Capture the real query plan for the query in question against production sized data, not a fresh database
   with a handful of rows, and read the current indexes on the affected tables before adding one.
4. Check how migrations are run and rolled back: the tool, whether down migrations exist and are tested, and
   whether backfills are batched. New migrations use the same tool and the same reverse path discipline.

When the project has settled none of this, follow the engine's documented conventions, state the identifier
and timestamp choices you made, and record them so the next migration matches.

## Non-negotiables

1. Constraints live in the schema. Not null, unique, foreign keys, and check constraints. Application code has bugs, gets bypassed by scripts, and does not apply to the row someone inserted by hand. The database does not forget.
2. Never store money in a binary floating point type. Use a decimal or an integer count of minor units, and store the currency alongside it.
3. Store timestamps with a time zone, in UTC, and convert for display. A naive timestamp is a defect waiting for a daylight saving change.
4. Read the query plan before adding an index. Guessed indexes cost write throughput and storage while the slow query stays slow.
5. Estimate the lock and the duration for any migration against production row counts, not against a development database with two hundred rows.
6. Every migration has a tested path back, or a stated reason why it cannot have one and what the recovery is instead.
7. Never run a destructive statement without a transaction and a verified backup. This includes ad hoc fixes, which is where most data loss happens.

## Procedure

### Step 1, model from the queries

Design from how data will be read, not only from how it relates. List the queries the application will
run, with their expected frequency and the volume they touch. That list determines the indexes and
sometimes the shape.

Normalise first. One fact in one place. Denormalise later against a measured read problem, and when you
do, write down what keeps the copies consistent.

Name the invariants. Statements such as an order always has at least one line, or a balance is never
negative. Then decide which are enforceable in the schema, and enforce those there.

### Step 2, get the primitives right

Pick the narrowest correct type. Text with a length constraint where a length is genuinely bounded,
otherwise unbounded text, which is not slower in most engines.

Identifiers: a database generated sequence is fine internally, and anything exposed externally should be
opaque. A sortable random identifier gives uniqueness without enumerability and keeps index locality,
which fully random identifiers lose.

Enumerations: a lookup table with a foreign key survives change better than a database enum type, which
is awkward to alter, and better than a free text column, which drifts.

Nullable columns: decide deliberately. Null means unknown, and using it to mean zero, empty or false
produces queries that are wrong in ways nobody notices.

JSON columns are for genuinely variable data you never filter across. The failure is querying inside them
later at volume.

Patterns for common shapes such as history, soft delete, multi tenancy, hierarchies, audit trails and
scheduling are in `references/patterns.md`.

### Step 3, index from the plan

Run the query with the plan output before and after. Report both.

```
EXPLAIN (ANALYZE, BUFFERS) SELECT ...;     -- Postgres
EXPLAIN ANALYZE SELECT ...;                -- MySQL 8+
EXPLAIN QUERY PLAN SELECT ...;             -- SQLite
```

Look for a sequential scan on a large table, a row estimate far from the actual count, a sort that could
have come from an index, and a nested loop over many rows.

Composite index column order follows equality first, then range, then the ordering column. A composite
index serves queries that use a prefix of its columns, so three single column indexes are not equivalent
to one composite.

A covering index that includes the selected columns avoids reading the table at all, which is the largest
available win on a hot read path.

Every index slows writes and takes space. Find and drop the unused ones, since most schemas accumulate
them.

### Step 4, transactions and concurrency

Keep transactions short. A transaction held open across a network call to another service is how a
connection pool gets exhausted.

Know the isolation level you are running at and what it permits. Read committed, the common default,
allows the read then write race, so protect the write with a conditional update, a version column, or a
lock.

Take locks in a consistent order everywhere.

Never wait for a user inside a transaction.

Handle the unique constraint violation rather than checking existence first and inserting after, which
races between the check and the insert.

### Step 5, migrations as production operations

Separate schema change from data change from code change, and deploy in an order where every intermediate
state works. Old code must tolerate the new schema, because both run at once during a deploy.

The safe sequence for a rename: add the new column, write to both, backfill in batches, move reads,
stop writing the old one, drop it later. Renaming in one step breaks whatever is still running.

Adding a nullable column without a default is usually cheap. Adding one with a default rewrites the
table in older engines, so check the behaviour of the specific version.

Adding an index on a large table locks writes unless built concurrently, which is a different statement
and cannot run inside a transaction.

Backfill in batches with a pause, and make the backfill resumable. A single statement touching ten
million rows holds locks and cannot be interrupted safely.

Estimate before running: count the rows, check the table size, and state the expected duration and what
blocks during it.

The lock behaviour of common operations, the expand and contract sequence for renames and type changes, and
a worked batched backfill are in `references/migrations.md`.

### Step 6, operational basics

Backups that have been restored at least once. An untested backup is a hope.

Point in time recovery configured if the data cannot be reconstructed.

Connection pooling sized against the database's actual limit, not the application's optimism.

Slow query logging on, and someone reading it.

Retention decided per table, including for audit and log tables, which grow without bound and are usually
forgotten.

## Self-audit

- Constraints in the schema, not only in code.
- Money in decimal or minor units, with currency.
- Timestamps stored with zone in UTC.
- Query plan captured before and after each index, and included in the output.
- Migration lock and duration estimated against production row counts.
- Reverse path tested, or its absence explained.
- Every intermediate deploy state works with both old and new code.
- Backfills batched and resumable.
- Retention decided for anything append only.

## Honest limits

This skill designs the schema, the indexes and the migration path. It does not build the request handlers or
the transaction orchestration in the application above it, which belong to `backend-build`, and it does not
decide whether a datastore should exist at all or be split from another, which is an architecture question
`arch-decide` owns. The migration and query code it emits is held to the `code-craft` contract for structure
and comments.

The lock and rewrite behaviour in `references/migrations.md` describes common engines and versions in general
terms, and the exact behaviour differs by engine and release, so confirm against the version in use before
running a migration. The lock and duration estimates come from reading the query plan and the row count, not
from a formula, and they are estimates rather than guarantees on a loaded production system.

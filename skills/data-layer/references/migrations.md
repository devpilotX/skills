# Migration safety and locks

The main file requires a lock and duration estimate for any migration against production row counts. This
file gives the lock behaviour of common operations, a safe sequence for the changes that go wrong most
often, and a worked batched backfill. Behaviour differs by engine and version, so confirm against the exact
version in use before running anything here.

## Lock behaviour of common operations

The column marked as blocking holds writes, and sometimes reads, for the duration. Row count is what turns a
fast operation into an outage.

| Operation | Typical cost | Blocks | Safer approach |
| --- | --- | --- | --- |
| Add nullable column, no default | Fast, metadata only | Brief | Usually safe as is |
| Add column with a non constant default | Rewrites the table on older engines | Writes for the rewrite | Add nullable, backfill, then set default |
| Add NOT NULL to an existing column | Full scan to validate | Writes during validation | Backfill, add a validated check, then set not null |
| Add an index | Locks writes unless built concurrently | Writes | Build concurrently, outside a transaction |
| Add a foreign key | Validates every existing row | Writes during validation | Add as not valid, then validate separately |
| Drop a column | Fast, metadata only | Brief | Stop reading it first, drop later |
| Rename a column | Fast, but breaks running code | Brief | Expand and contract, never rename in place |
| Change a column type | Often a full rewrite | Writes for the rewrite | Add new column, backfill, switch, drop old |

The pattern behind the safe approaches: split one risky statement into several cheap ones, and keep every
intermediate state working for both the old and new code that run together during a deploy.

## The expand and contract sequence

Use this for any rename or type change. Each step is a separate deploy and each is reversible on its own.

1. Expand. Add the new column or table alongside the old one. Nothing reads it yet.
2. Dual write. Change the code to write both the old and the new column. Deploy.
3. Backfill. Copy existing rows into the new column in batches, resumably. This touches every row but holds
   no long lock if batched.
4. Move reads. Change the code to read the new column. Deploy and watch.
5. Stop writing the old column. Deploy.
6. Contract. Drop the old column later, once you are sure nothing reads it and a rollback window has passed.

Renaming in one statement breaks whatever code is still running against the old name during the deploy, which
is why the sequence never renames in place.

## Worked backfill

The task: populate a new currency column on an orders table with 40 million rows, defaulting existing rows to
the account currency, without holding a long lock.

```
-- runs repeatedly, each call touches one batch and returns how many it changed
UPDATE orders o
SET currency = a.currency
FROM accounts a
WHERE o.account_id = a.id
  AND o.currency IS NULL
  AND o.id IN (
    SELECT id FROM orders WHERE currency IS NULL ORDER BY id LIMIT 5000
  );
```

Drive it from a small script that calls the statement, sleeps briefly, and repeats until zero rows change.
The batch size keeps each statement short so it never blocks writes for long, the sleep gives the replica
time to catch up, and the IS NULL filter makes the whole job resumable: if it dies at 20 million rows,
rerunning picks up exactly where it stopped because done rows no longer match.

Estimate before starting. At 5000 rows per batch and 40 million rows, that is 8000 batches. With a short
sleep between them, plan for the job to run over hours, not seconds, and schedule it accordingly.

## Before you run

Count the rows and check the table size on production, not on a development copy. State the expected duration
and what blocks during it. Take a backup you have restored at least once, wrap any destructive statement in a
transaction, and confirm the reverse path works on a copy first.

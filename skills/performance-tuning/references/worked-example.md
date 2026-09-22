# Worked example

One endpoint, taken from the first complaint to the after numbers, following the procedure in the main
file. The figures are illustrative of the shape of the work, not measurements from a real system.

## The complaint

An order history page is slow. That is all the report says. The first job is to turn it into a target.

The operation is the GET request that renders one user's order history. The percentile is the 95th,
because a handful of users with long histories generate the complaints. The target agreed with the team
is under 400 milliseconds at the 95th percentile at the current data volume, which is up to a few
hundred orders per user.

## Step 2, the breakdown

The framework's request timing was already available, so no new code was needed to get a first split.
Ten runs against a heavy account gave this breakdown at the 95th percentile:

| Phase | Time (ms) | Share |
| --- | --- | --- |
| Server compute | 60 | 5 percent |
| Database | 980 | 82 percent |
| External calls | 90 | 8 percent |
| Transfer and render | 60 | 5 percent |

The database dominates. Nobody needs to read a line of application code yet. The next question is which
query, so the slow query log was read for the duration of one request.

The log showed 214 near identical queries for one page load: one query for the order list, then one
query per order to fetch its line items. This is the N plus one pattern the main file names as the most
common serious defect.

## Step 3, fix in order of contribution

The largest contributor is the per order query. The fix is to remove the repeated work, not to make
each query faster.

The 214 queries became two: one for the order list, one for all line items belonging to those orders,
joined in memory by order id. This is the batch move from the procedure.

Re-reading the query plan for the line item query showed a full scan, because there was no index on the
order id column of the line items table. An index was added, taken directly from the plan rather than
guessed.

Caching was considered and rejected at this stage. With the N plus one gone the endpoint was already
inside the target, and a cache would have added an invalidation problem for no remaining need.

## Step 4, verify honestly

Re-measured with the same ten run method against the same heavy account:

| Phase | Before (ms) | After (ms) |
| --- | --- | --- |
| Server compute | 60 | 65 |
| Database | 980 | 70 |
| External calls | 90 | 90 |
| Transfer and render | 60 | 60 |
| Total p95 | 1190 | 285 |

The spread across the ten after runs was 270 to 310 milliseconds, so the improvement is well outside
the run to run variance. The tail was checked, not just the mean: the 99th percentile dropped in step
with the 95th rather than lagging, so the change did not trade tail latency for mean.

Correctness was checked by running the test suite and by comparing the rendered order history for
three accounts before and after. The batched join produced the same orders in the same sequence.

The cold path was checked: the first request after a deploy, with no warmed connection pool, came in at
340 milliseconds, still inside the target.

## Step 5, report

Target: order history GET under 400 ms at p95 at current volume.

Before: 1190 ms at p95, of which 980 ms was database, caused by 214 queries per page from an N plus one
over line items.

Change: batched the per order line item queries into one, and added an index on the line item order id
column, taken from the query plan.

After: 285 ms at p95, spread 270 to 310 across ten runs. Tail moved with the mean. Cold path 340 ms.

Cost of the change: the batched load holds all line items for the page in memory at once. For the
current volume of a few hundred orders this is small. If a single user ever accumulates tens of
thousands of orders, the page will need pagination, which is now the constraint to watch.

New dominant cost: the external calls at 90 ms are now the largest single phase. They are within budget,
so no further work is worthwhile unless the target tightens.

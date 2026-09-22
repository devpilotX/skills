---
name: performance-tuning
description: Make software faster by measuring first and changing the thing that dominates. Use when the user says something is slow, asks how to optimise or speed up code, a page, a query or an API, asks about profiling, caching, latency, throughput, memory usage or scaling, or asks why performance degraded. Refuses to optimise without a profile, sets a target before starting so there is a definition of done, fixes the largest contributor rather than the most interesting one, and reports before and after numbers from the same measurement method. Names the cost of every optimisation in complexity, because most of them trade clarity for speed. Triggers on this is slow, optimise this, improve performance, profiling, high latency, slow query, memory usage, throughput, it got slower, speed up my app, reduce load time.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Performance tuning

Intuition about what is slow is wrong often enough that acting on it wastes most of the effort. Measure,
fix the dominant cost, measure again.

An optimisation is a code change, and the fast version is often the harder one to read. When you rewrite
a hot path, add a cache, or batch a loop, hold the result to the `code-craft` contract so the next
reader can tell what the clever version is doing and why the slow, clear version was not enough.

## Fit to the project

Find out whether any measurement exists at all before touching code, because most performance requests
arrive with a feeling and no number. The first job is to turn the feeling into a figure.

Look for a profiler already wired in: a language profiler in the dev dependencies, an APM agent in the
runtime config, or a flame graph tool in the scripts. If one exists, use it and read whatever it last
captured. If none exists, find the cheapest way to get a first breakdown for this stack, which is
usually the framework's own request timing, the database's slow query log, or the browser's built in
profiler, and note that you are establishing a baseline rather than confirming one.

Read the current numbers next. Check whether there is an existing latency dashboard, a service level
objective, or a load test with recorded results. Those give you the before figure and the target in
one place. Get the real data volume the operation runs against, since a profile over ten rows finds
nothing that matters at ten million.

Confirm which operation the complaint is actually about and at which percentile. A report that the app
is slow usually means one screen or one endpoint at the tail, not the whole system at the mean.

When the project has measured nothing and set no target, do not optimise yet. Establish a baseline with
whatever profiler the stack offers, agree a target percentile and load, and only then start the
procedure.

## When to stay off

Skip a tuning pass when the operation already meets its target, when the code runs once at startup and
never in the request path, or when the user has said the current speed is fine. Optimising code that
is already fast enough trades readability for a number nobody was waiting on.

Saying "stop", "just execute", or "skip the profiling" is the off switch. It stays off for the rest of
the session unless the skill is invoked again. Chasing a faster number after the target is met is how a
clear function becomes an unmaintainable one for no user benefit.

## Non-negotiables

1. Profile before changing anything. No optimisation without a measurement showing where the time goes. This rule exists because guessing produces changes that add complexity and no speed.
2. Set a target first. "As fast as possible" has no completion condition, so it ends in either premature stopping or endless work. "Under 300 milliseconds at the 95th percentile for this endpoint" ends.
3. Measure the same way before and after, on the same data and the same hardware, and report both numbers. A comparison across different conditions is not a result.
4. Fix the largest contributor. A 60 percent improvement on 3 percent of the time is nothing, however satisfying it was to find.
5. Name the cost of each optimisation. Almost all of them trade readability, memory, correctness margin or operational complexity for speed. State the trade so somebody can refuse it.
6. Never report an improvement smaller than the variance between runs. Run it several times and give the spread.
7. Optimise the user's experience of time, not the number that is easiest to measure. A faster average with worse tail latency is usually a regression.

## Procedure

### Step 1, define the target

Which operation, measured at which percentile, under what load, on what data volume?

The percentile matters more than the average. Users experience the slow requests, and an average hides
them. Use the 95th and 99th.

Decide whether this is a latency problem, meaning one operation takes too long, or a throughput problem,
meaning the system cannot process enough. They have different fixes, and confusing them leads to adding
capacity where the fix was an index.

Get the real data volume. Performance work against a small dataset finds different problems from the real
ones.

### Step 2, measure where the time goes

Use a profiler, not timing statements, for a first pass. Timing statements confirm a hypothesis, and a
profiler generates one.

For a web request, split the total into server time, database time, external call time, transfer time and
client rendering time before looking at any code. This single breakdown usually identifies the area, and
it is frequently not where people were looking.

For database work, read the query plan. See `data-layer`.

For client performance, use the browser profiler with network throttling. See `frontend-build`.

For memory, take heap snapshots at two points and compare retained sizes rather than reading allocation
counts.

Write down the breakdown with numbers. This is the document the whole exercise depends on.

For the tools that produce a first breakdown per stack, what each one measures, and where each one
lies, see `references/measurement-methods.md`.

### Step 3, fix in order of contribution

The order that finds real wins fastest:

Remove work that does not need doing. The largest wins usually come from not doing something, rather than
doing it faster. Unused fields fetched, data loaded and discarded, work repeated per item that could be
done once, or an endpoint called twice by the client.

Fix the N+1 pattern. A query inside a loop is the single most common serious performance defect in
application code, and it scales with data so it appears after launch.

Index from the query plan.

Batch. One request for a hundred items beats a hundred requests, on both network and database.

Move work out of the request path into a background job, especially mail, file generation and third party
calls.

Cache, once the above are done, with an invalidation strategy decided before the cache exists.

Then algorithmic improvement inside the hot path, which is where people usually start and where the win is
often smallest.

### Step 4, verify honestly

Re-measure with the same method, and report before and after with the spread across runs.

Check the tail, not only the average, since some changes improve the mean and worsen the 99th percentile.

Check correctness. Caching and batching change behaviour, and a fast wrong answer is a defect. Run the
test suite.

Check resource use. A latency win paid for with memory that triggers termination under load is not a win.

Check the cold path: cold cache, first request after deploy, and an empty warm up state.

### Step 5, report

Give the target, the measured breakdown before, what was changed and why that item, the numbers after, the
cost of the change, and what now dominates.

Naming the new dominant cost matters, because it tells the reader whether further work is worthwhile.

For a full run through one endpoint, from the first breakdown to the after numbers and the new dominant
cost, see `references/worked-example.md`.

## Frequent causes by area

Application code: a query in a loop, serialising more data than the caller uses, recomputing per item what
could be computed once, work in a constructor, synchronous work that could overlap, and logging in a tight
loop.

Database: no index on a filter or join column, a query returning far more rows than needed, a sort that
could have come from an index, a transaction held open across a network call, and connection pool
exhaustion from an unbounded pool.

Network: many small requests, no compression, no connection reuse, a chain of dependent calls, and an
external call with no timeout holding a worker.

Client: too much JavaScript, images larger than displayed, layout shift from unreserved space, long lists
rendered in full, and re-rendering caused by a new object identity on every render.

Memory: an unbounded cache, a listener added without removal, a closure retaining a large structure, and
loading a whole file rather than streaming it.

## Self-audit

- A target with an operation, a percentile and a load level was set first.
- A profile exists and the breakdown is in the report.
- The change addressed the largest contributor.
- Before and after measured identically, with run to run spread.
- Tail latency checked, not only the average.
- Correctness verified after the change.
- Cold path checked.
- The cost of the optimisation stated.
- The new dominant cost named.

## Honest limits

This skill measures and fixes what dominates a given operation. It does not decide whether the
operation should exist or whether the architecture forces the slow path. When the profile says the
system is doing the wrong work in the wrong place, that is an `arch-decide` question, and no amount of
tuning fixes a design that fans out ten calls where one would do.

The database work here stops at reading the query plan and naming the index. The plan reading itself,
schema and query shape belong to `data-layer`. Client side breakdowns stop at the profiler output;
bundle size, rendering and asset work belong to `frontend-build`. The before and after numbers come
from the project's own profiler on its own data, not from any published benchmark, so a figure is only
as trustworthy as the measurement method behind it. Keeping the numbers honest once the system is live
is `observability-setup`, and paying less for the same speed is `cost-control`.

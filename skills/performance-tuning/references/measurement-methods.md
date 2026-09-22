# Measurement methods

The main file says to profile before changing anything and to get a breakdown with numbers. This is
the menu of ways to get that first breakdown, what each one measures, and the way each one can mislead
you. Pick the cheapest method that answers the question, then confirm with a second method before you
act on a surprising result.

## What to reach for by question

| Question | Method | What it gives |
| --- | --- | --- |
| Where does one request spend its time? | Request breakdown by phase | Server, database, external, transfer, render split |
| Which function burns the CPU? | Sampling profiler | Time attributed to call stacks |
| Which query is slow? | Query plan plus slow query log | Rows scanned, index used, join order |
| What holds memory? | Two heap snapshots compared | Retained size by object, growth between points |
| Where does the wall clock go while CPU is idle? | Wall clock profiler, not CPU only | Time spent waiting on IO and locks |
| Is the client slow to paint? | Browser performance profiler | Script, layout, paint, network waterfall |

## Sampling profiler

Interrupts the program at a fixed rate and records the stack. Cheap enough to run in production on many
stacks, and the first tool to reach for on a CPU bound operation.

It measures where CPU time goes. It does not measure time spent waiting, so a request that is slow
because it is blocked on a network call will look fast to a CPU sampler. When the sampler says the code
is idle but the request is slow, switch to a wall clock method.

## Instrumented request breakdown

Split the total response time into server compute, database, outbound calls, and transfer, before
looking at any function. Most frameworks expose the hooks to do this, or an APM agent does it for you.

This is the single most useful first measurement, because it points at the area without any code
reading. It measures wall clock time per phase. Its weakness is granularity: it tells you the database
took 400 of the 600 milliseconds, not which query.

## Query plan

Ask the database to explain the query. Read the access method, the rows estimated against rows
returned, the join order, and whether a sort or a temporary table appears.

It measures the planner's intent and, with the analyse form, the actual execution. The trap is running
it on a small dataset, where the planner picks a scan that becomes a disaster at real volume. Always
read the plan against production sized data.

## Heap snapshot comparison

Take a snapshot, run the workload, take a second snapshot, and compare retained sizes. Retained size is
what would be freed if the object were collected, which is the number that matters, not the count of
allocations.

It finds leaks and unbounded growth. It is slow to capture and pauses the process, so it is a
diagnostic run, not a continuous measurement.

## Timing statements

A start and end timestamp around a block. The main file is explicit that these confirm a hypothesis and
do not generate one. Reach for them only after a profiler has pointed at a region, to measure that
region precisely.

The danger of leading with timing statements is that you only measure what you already suspected, which
is exactly the intuition the whole skill exists to distrust.

## Reading the numbers without fooling yourself

Run every measurement several times and record the spread, not a single figure. A one off number
includes whatever else the machine was doing.

Measure on production sized data. The bug that dominates at ten million rows is invisible at ten.

Warm and cold are different measurements. Report which one you took. A warm cache figure hides the
first request after a deploy.

Read the percentile the user feels, which is the tail, not the mean. A method that only reports an
average is hiding the requests that generate the complaints.

When two methods disagree, the cheaper one is usually the one that is wrong about the cause. A CPU
sampler that shows idle while a request is slow is not lying about the CPU; it is telling you the time
went somewhere it cannot see.

## Establishing a baseline when none exists

If the project has measured nothing, the order that gets a usable baseline fastest:

1. Turn on the framework's request timing or the database slow query log. Both are usually a config
   change, not new code.
2. Capture a breakdown for the one operation in question under realistic load.
3. Record the before number with its spread and the target percentile.
4. Only now start changing code.

# Delivery, ordering, and what to log

## Delivery guarantees, plainly

At most once. A message is delivered zero or one times. It can be lost and is never duplicated. Use it
only for work you can afford to drop, such as a metric sample where the next one arrives soon.

At least once. A message is delivered one or more times. It is never silently lost but can be
duplicated. This is what most brokers give, and it is why the consumer has to be idempotent.

Exactly once. A message has its effect applied once. Across a network this is not free and is usually
implemented as at least once delivery plus a deduplicating, idempotent consumer. Treat a broker's
exactly once label as a convenience over that mechanism, not as permission to skip idempotency in your
own code.

The honest position for most systems is at least once delivery with idempotent consumers. Say that in
the design so nobody builds on a stronger assumption than the system provides.

## The cost of ordering

Global ordering across a whole queue forces one consumer or one partition to process messages in
sequence. That caps throughput to a single worker and creates head of line blocking: one slow or
failing message stalls everything behind it until it clears or dead letters.

Per key ordering is the usual compromise. Messages that share a key, such as all events for one
account, go to the same partition and stay ordered relative to each other, while different keys run in
parallel. Throughput scales with the number of keys rather than being pinned to one.

The cheapest option is no ordering with commutative handlers. If applying two messages in either order
gives the same end state, you need no ordering guarantee at all. Design for this where the domain
allows it, because it removes a whole class of operational pain.

Before requiring ordering, ask whether the work is truly order dependent or whether it only feels
tidier ordered. Ordering you did not need is throughput you gave away.

## What to log so a stuck job is findable

A correlation id that ties the message to the request or event that produced it, carried end to end.
Without it you cannot connect a stuck worker to what triggered it.

The broker's message id and the delivery or attempt count, so you can tell a first delivery from a
third retry.

The idempotency key, so you can see whether a duplicate was correctly recognised.

The handler name and the outcome: success, transient failure with the error, permanent failure with
the reason, or dead lettered.

Timing: when the message was enqueued, when the worker picked it up, and how long the work took. The
gap between enqueue and pickup is your real queue latency, which no per job success rate shows.

Do not log the full message body if it carries personal data or secrets. Log the identifiers needed to
find the record, not the record.

## Alerts that catch a failing queue

Oldest message age above a threshold. This rises when consumers fall behind even while every job
succeeds, and it is the earliest honest signal of a backlog.

Queue depth trend, growing faster than it drains over a window.

Dead letter count above zero, or above a low threshold, with someone paged to inspect and replay.

Redelivery rate climbing, which points at a visibility timeout set below the real runtime or at a
downstream that is failing intermittently.

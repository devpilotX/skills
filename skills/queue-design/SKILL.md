---
name: queue-design
description: Design asynchronous work that survives retries, restarts, and duplicate delivery. Use when adding a background job, a message queue, a worker, or an event consumer, when a job runs twice and charges a customer twice, when messages pile up unprocessed, when a worker crashes mid job, when a bad message blocks the queue, or when a delivery is lost. Chooses a delivery guarantee honestly, makes work idempotent with a stored key, retries with backoff and jitter under a cap, routes failures to a dead letter path with a way back, sets visibility timeouts longer than the worst real runtime, and alerts on queue depth. Triggers on add a background job, message queue, worker keeps retrying, job ran twice, duplicate processing, exactly once, at least once, idempotency key, dead letter queue, visibility timeout, poison message, queue backing up, consumer crash, event driven, task queue, out of order messages.
license: MIT
compatibility: Any language and any broker: a hosted queue, a self managed broker, a database backed queue, or an event log. The guarantees discussed are broker independent.
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Queue design

The queue works in the demo and fails in production the first time a worker dies mid job. The message
was delivered, the work half ran, and the broker redelivers it, so the customer gets charged twice.
Or a single unparseable message wedges the consumer and the backlog grows behind it while nobody is
paged. These are the default failure modes of asynchronous work, and they come from assuming delivery
happens once and work always finishes.

This skill designs work that expects redelivery and crashes. It produces code, so follow the
`code-craft` contract for how the workers and handlers are organised.

## Fit to the project

Read what the project already runs before adding a broker to it.

1. Find the existing async mechanism: a hosted queue, a self managed broker, a database backed job
   table, or an event log. Adding a second system is expensive to operate, so extend the one that is
   there unless it cannot do the job.
2. Read one existing consumer end to end. Note whether it acknowledges before or after the work, what
   it does on failure, and whether it assumes a message arrives once. That assumption is usually the
   bug.
3. Find the operations that must never happen twice: charging a card, sending an email, shipping an
   order, decrementing stock. These need idempotency. List them before writing a handler.
4. Check what a job's worst case runtime actually is, from real timing, not a guess. The visibility
   timeout has to exceed it, so you need the number first.

## Non-negotiables

1. Design for at least once delivery. Almost every broker can duplicate a message on retry or network
   failure, and true exactly once across a network is a strong claim that usually hides an idempotent
   consumer doing the real work. Assume duplicates and make the handler safe under them.
2. Make every effectful handler idempotent with a stored idempotency key. Before doing the side
   effect, record or check the key in the same transaction as the effect where possible. Without this,
   a redelivered message repeats the charge, the email, or the shipment.
3. Set the visibility timeout longer than the worst observed job runtime, with headroom. If the
   timeout is shorter than the job, the broker redelivers a message that is still being processed, so
   two workers run the same job at once. This is the most common cause of duplicate processing.
4. Cap retries and route the exhausted message to a dead letter destination. A message that retries
   forever burns capacity and hides the failure. A dead letter queue with no path back is a silent
   data loss, so the path back has to exist too.
5. Alert on queue depth and on dead letter count, not only on worker errors. A queue that is growing
   faster than it drains is failing even while every individual job succeeds, and depth is the signal
   that shows it before users do.

## Procedure

### Step 1, choose a delivery guarantee honestly

Name the guarantee the broker actually gives. Most give at least once, meaning a message arrives one
or more times. A few offer at most once, meaning a message may be lost but never duplicated, which is
only acceptable for work you can afford to drop. Treat any exactly once claim as at least once plus an
idempotent consumer, and build the consumer accordingly.

Write down, for this queue, which guarantee you are relying on and what happens on a duplicate and on
a loss. If you cannot state both, the design is not finished.

### Step 2, make the handler idempotent

Derive a stable idempotency key from the work, not from the delivery. A payment keyed by order id is
safe under redelivery; a payment keyed by a random per delivery id is not, because the retry gets a
new id and charges again.

Store the key with the result of the effect. The pattern in `references/idempotency.md` records the
key in the same transaction as the side effect so a crash between them cannot leave the effect done
and the key unrecorded. Where the effect is an external call that has its own idempotency support, pass
your key through to it.

On a repeat, return the stored result instead of redoing the work.

### Step 3, decide whether ordering is actually required

Ordering is expensive. It usually forces messages for a key onto a single partition or a single
consumer, which caps throughput and turns one slow message into head of line blocking for everything
behind it. Require it only where the work is genuinely order dependent, and only per key rather than
globally.

Where order is not required, design the handler to be commutative so messages can arrive in any order
without a wrong result. The cost of global ordering and the per key alternative are in
`references/delivery-and-ordering.md`.

### Step 4, retry with backoff, jitter, and a cap

On a transient failure, retry with exponential backoff so a struggling downstream is not hammered. Add
jitter so many failed messages do not retry in a synchronised wave that knocks the downstream over
again. Cap the number of attempts, because some failures are permanent and retrying a permanent
failure forever is waste that also hides it.

Distinguish transient from permanent. A network timeout is worth retrying; a validation failure or a
missing record is not, and retrying it just delays the dead letter.

### Step 5, handle dead letters and poison messages

Route a message that exhausts its retries to a dead letter destination that keeps the message, the
error, and the attempt count. A poison message, one that fails every time because of its content
rather than a transient condition, has to leave the main queue fast so it does not block the backlog
behind it.

Give dead letters a path back. Someone has to be able to inspect them, fix the cause, and replay them
into the main queue after a fix. A dead letter queue nobody drains is a slow data loss.

### Step 6, set visibility timeout and handle crashes

Set the visibility or lease timeout above the worst real runtime with headroom, using the number from
the fit step. Acknowledge a message only after the work and its idempotency record are committed. A
worker that acknowledges first and then crashes has lost the message; a worker that crashes before
acknowledging gets a safe redelivery because the handler is idempotent.

For long jobs, extend the lease periodically while the work runs rather than setting one enormous
timeout, so a truly stuck worker still releases the message eventually.

### Step 7, add backpressure and observability

Alert on queue depth, on the age of the oldest message, and on dead letter count. A rising oldest
message age means consumers are falling behind even if none are erroring. Apply backpressure when the
queue grows past a threshold: slow or reject producers rather than letting an unbounded queue exhaust
memory or delay everything.

Log enough to find a stuck job. What to log is in `references/delivery-and-ordering.md`.

## Self-audit

- Is the delivery guarantee named, and is the handler safe under duplicate delivery?
- Does every effectful handler check and store an idempotency key derived from the work, not the
  delivery?
- Is the visibility or lease timeout longer than the worst observed runtime, with headroom?
- Are retries capped, with exponential backoff and jitter, and do permanent failures skip retry?
- Does an exhausted or poison message go to a dead letter destination that keeps the error, with a
  documented way to replay it after a fix?
- Is the message acknowledged only after the work and its idempotency record are committed?
- Is there an alert on queue depth or oldest message age, not only on worker errors?
- Does a stuck job carry enough logged context, a correlation id and the message id, to be found?

## Honest limits

This skill designs the queue and the consumer. It does not choose the broker or the overall
distribution of services, which is an architecture decision that `arch-decide` owns. It does not cover
the throughput tuning of a specific broker, which belongs to `performance-tuning`.

The timeout, retry, and depth numbers here are rules of thumb to be set from your own measured
runtimes, not fixed values. Confirm the exact delivery and ordering semantics against your broker's
own current documentation, because the guarantees differ by broker and by configuration. Wiring the
alerts into a monitoring system is work that `observability-setup` covers.

## Off switch

If the user says "stop", "just execute", or "skip the queue review", stand down and make only the
change asked for. That stands for the session unless the skill is invoked again.

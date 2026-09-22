# Idempotency and retry playbook

The main file requires every retryable operation to be idempotent and every outbound call to carry a
timeout and a bounded retry. This file gives the mechanics: how to build an idempotency key, where each
technique belongs, what to retry and what never to retry, and a worked payment example.

## Pick the idempotency technique by operation

| Operation | Technique | Where the key lives |
| --- | --- | --- |
| Create a resource once | Unique constraint on a natural or client supplied key | Database column |
| Client submits a form twice | Idempotency key header stored with the result | Idempotency table |
| Charge a card | Provider idempotency key plus a local ledger row | Provider and database |
| Send an email | Dedup on a message key with a sent marker | Sent log table |
| Increment a counter | Atomic update in the database | Single statement |
| Consume a queue message | Dedup on the message id before doing work | Processed table or set |

The rule behind the table: an operation is idempotent when running it twice leaves the same state as
running it once. Decide the key that identifies the same logical request before writing the handler.

## Building an idempotency key

A good key is stable across retries of the same request and different across genuinely different requests.

For client submitted work, have the client generate a key once and send it on every retry, usually as an
Idempotency-Key header. Store the key with the response you produced. On a repeat, return the stored
response instead of doing the work again.

For work you trigger yourself, derive the key from the inputs that define the request, such as the order id
plus the step name. Do not derive it from a timestamp or a random value, because a retry would produce a
different key and the dedup would miss.

Expire stored keys on a schedule that outlives the longest client retry window. A key kept forever grows the
table without bound.

## What to retry, and how

Retry only failures that a later attempt might succeed. A timeout, a connection reset, a 503, and a 429 with
a retry hint are retryable. A 400, a 401, a 403, and a 422 are not, because the same request will fail the
same way.

Back off between attempts and add jitter, so a dependency recovering from overload does not get hit by every
client retrying in lockstep. Cap the total attempts and the total time, then give up and surface a structured
error.

Never retry a non idempotent write without an idempotency key in place first. A retried charge with no key is
a double charge.

## Worked example, capturing a payment

The request: capture a payment for an order. The failure to avoid: charging the card twice when the client
retries after a timeout.

1. The client sends an Idempotency-Key header, the same value on every retry of this capture.
2. The handler authenticates, then authorises that the caller owns the order.
3. It looks up the key in the idempotency table. On a hit, it returns the stored response and stops.
4. On a miss, it opens a transaction, inserts a ledger row keyed by the order id with status pending, and
   commits. A unique constraint on the order id blocks a second pending row.
5. It calls the payment provider, passing the provider idempotency key derived from the order id, with an
   explicit timeout and a bounded retry on timeout only.
6. On success it updates the ledger row to captured and stores the response under the idempotency key.
7. On a provider error that is not retryable, it marks the ledger row failed and returns a structured error
   with a code and the correlation id.

The double submit is stopped in three places: the idempotency key returns the first response, the unique
constraint on the order id blocks a second ledger row, and the provider key makes the provider itself refuse
the duplicate. Any one of them is enough, and together they survive a partial failure between steps.

## Common mistakes this prevents

Checking whether a row exists and then inserting it in a separate statement, which races between the check and
the insert. Use the unique constraint and handle the violation instead.

Storing the idempotency key only after the work succeeds, which leaves a window where a retry during the work
runs it a second time. Reserve the key before the work, not after.

Retrying inside a transaction that is still open, which holds locks across every attempt and exhausts the
connection pool. Retry around the transaction, not inside it.

# Idempotency in a consumer

A handler is idempotent when running it twice with the same message produces the same result as
running it once. Under at least once delivery this is not optional, because the broker will eventually
deliver a duplicate.

## The key comes from the work

Choose an idempotency key that is stable across redeliveries of the same logical work. Good keys come
from the domain: an order id for a payment, a message id that the producer sets once and reuses on
retry, a hash of the meaningful fields. A bad key changes on every delivery, such as a per attempt
identifier the broker generates, because then a retry looks like new work.

If the producer can set a stable id, have it do so and carry it through. If it cannot, derive the key
from the content that defines the work.

## Store the key with the effect

The failure to avoid is doing the side effect and then crashing before recording that you did it. On
redelivery you repeat the effect. Close that gap by writing the idempotency key in the same
transaction as the effect whenever the effect is a local database write.

A common shape:

1. Begin a transaction.
2. Insert the idempotency key into a table with a unique constraint. If the insert fails on the
   constraint, this message was already processed, so roll back and return the stored result.
3. Perform the effect and write its result.
4. Commit.

The unique constraint is what makes two concurrent deliveries safe: only one insert wins, the other
sees the conflict and treats the message as a duplicate.

## When the effect is an external call

If the effect is a call to another service, you cannot put it in your database transaction. Two
options apply. First, use the downstream's own idempotency support by passing your key to it, so it
deduplicates on its side. Many payment and messaging providers accept an idempotency key header for
exactly this. Second, record intent before the call and completion after, so a crash between them
leaves a record you can reconcile rather than a silent repeat.

## Expiring keys

Keys do not need to live forever. Keep them at least as long as the maximum time a duplicate could
arrive, which is bounded by the retry policy and the dead letter retention. A key store that grows
without bound becomes its own problem, so age keys out past that window.

## What idempotency does not fix

It makes repeated delivery safe. It does not make the work correct, and it does not recover a message
that was genuinely lost under an at most once configuration. It also does not order messages: two
idempotent handlers can still apply non commutative changes in the wrong order, which is a separate
problem covered under ordering.

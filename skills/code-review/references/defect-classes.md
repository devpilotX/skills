# Defect classes

Organised by the kind of mistake rather than by language. Work through the classes that apply to the
change in front of you.

## Boundary and empty cases

Empty collection, single element, and exactly-at-the-limit input.

Zero, negative, and maximum values on anything numeric.

Empty string against null against absent, which are three different states that code often conflates.

First and last iteration of a loop, and the case where the loop body never runs.

Pagination at the exact page size, and the page after the last one.

Unicode input where the code assumes one byte per character, and string length used for a display width.

## Null and optional handling

A value checked for null on one path and not on another.

An optional unwrapped because it "cannot" be absent. Find the case where it can.

A default that silently masks a missing value, so a bug becomes a wrong result instead of an error.

Chained access where any link can be absent.

## Error handling

Caught and ignored, or caught and logged while execution continues into code that assumed success.

An error converted to a generic message, losing the information needed to diagnose it.

The failure path itself failing, for example a handler that logs to a service that is down.

Cleanup that does not run on the error path. Missing finally, defer, or context manager.

An error returned but not checked by the caller, which is easy to miss in languages where errors are
values.

Exceptions used for control flow across a boundary where the other side does not know about them.

## Concurrency and ordering

Shared mutable state reached from more than one thread, task, or request.

Read then write without atomicity, which is the classic lost update. Two users clicking at once.

Locks taken in different orders in different places, which is how deadlock arrives.

Assumption that callbacks or messages arrive in order, or exactly once.

Work that is not idempotent behind a retry, a queue, or a webhook. Charging a card, sending mail,
incrementing a counter.

A cache written before the transaction commits, so a rollback leaves the cache wrong.

Background work holding a reference to a request scoped object.

## State and lifecycle

Initialisation order, and use before initialisation.

An object mutated after being handed to something that assumed it was stable.

A default argument that is a mutable value, which persists between calls in several languages.

Cleanup on every exit path, including early return.

State that survives across requests because it was stored on a module or a singleton.

## Data and persistence

A migration that is not reversible, or that fails partway leaving mixed schema.

A migration that locks a large table, measured against production row counts rather than a development
dataset.

A delete with no transaction, no soft delete, and no backup, especially in a script.

A query built by string concatenation anywhere.

Constraints enforced only in application code, where the database could enforce them.

A unique index added without checking for existing duplicates.

Timezone assumptions, and storing local time where an instant was meant.

Money in floating point.

## Security

Authorisation checked for the session but not for the object being accessed. The dominant real world
defect: change one identifier in the request and read someone else's record.

Input rendered into HTML, SQL, a shell command, a template, or a file path without the right escaping
for that context.

Secrets in code, in logs, in error messages, or in anything sent to the client.

A redirect or a fetch target taken from user input.

Deserialisation of untrusted data.

Timing sensitive comparison on a secret, meaning a plain equality check on a token.

Missing rate limit on anything that authenticates, sends, or costs money.

Permissions widened by the change without that being the stated intent.

## Resources

Unbounded growth: a list, map, cache, or log that only ever gets appended to.

Handles, sockets, and file descriptors not closed on every path.

A query inside a loop.

A whole table or file loaded into memory where streaming was possible.

No timeout on an outbound call.

A subscription, listener, or interval created without a matching teardown.

## Interface and compatibility

A signature, field, or return type changed without updating every caller.

A field removed or renamed while old clients still send or read it.

An enum extended where the consumer has an exhaustive switch.

A default changed, which silently alters behaviour for everyone who relied on it.

A version bump in a dependency that includes a breaking change.

An error code or message that a consumer parses.

## Test adequacy for this change

Does a test exist that would fail if this change were reverted? That is the practical question, and the
answer is frequently no.

Are the new failure paths tested, or only the success path?

Are boundaries tested, or only the middle of the range?

Is the test deterministic, or does it depend on sleeps, the real clock, the network, or ordering?

Does the test assert on behaviour rather than on implementation detail that will break on the next
refactor?

For a bug fix, is there a test that reproduces the original bug?

## Clarity, only where it will cause a defect

A name that states the wrong thing, which is worse than a vague name.

A comment that contradicts the code, meaning one of them is wrong and a reader will pick the wrong one.

A function with several unrelated responsibilities where a caller will reasonably misuse it.

Conditional nesting deep enough that a future edit will land in the wrong branch.

Magic values repeated in more than one place, where they will drift apart.

Raise these with the future defect named. Without that, it is a preference, and it goes in the
preferences section.

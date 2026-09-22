# Intermittent bugs

A failure that comes and goes is not random even when it looks random. It has a hidden variable you have
not measured yet. This is a playbook for finding that variable, organised by the usual suspects.

## First, measure the rate

Before changing anything, record how often it fails: one in ten, one in a hundred, only at peak, only on
one host. A change from one in ten to one in a hundred looks like a fix and is not. Without a baseline rate
you cannot tell a real fix from luck.

## Suspect one, a race between two operations

Symptoms: fails more under load, fails more with concurrency, the failing runs show a value that belongs to
a different request or a different record.

How to find it: run the operation twice at the same instant. If the failure rate jumps, the hidden variable
is concurrency. Log the identity of the data at read and at write, and look for one request seeing another
request's value.

How to confirm: serialise the two operations. If the bug vanishes when they cannot overlap, the cause is a
race.

Common shapes: read then write without a lock, shared mutable state on a singleton, a cache written before
a transaction commits, a request scoped value attached to something longer lived.

## Suspect two, a dependence on ordering

Symptoms: passes alone, fails in the full suite, or passes in one suite order and fails in another. In
production, works on one path and not on another that does the same steps in a different sequence.

How to find it: run the failing item in isolation, then run it after the item you suspect leaves state
behind. Shuffle the order deliberately and watch the rate change.

How to confirm: reset all state explicitly between operations. If the bug stops, something was leaking
state across the boundary.

Common shapes: a test that depends on a shared fixture another test mutated, code that assumes messages
arrive in order, initialisation that runs before the thing it depends on in some orderings.

## Suspect three, a resource limit reached under load

Symptoms: fine at low volume, fails as volume climbs, recovers after a restart, correlates with memory or
connection or file descriptor counts.

How to find it: watch the resource while reproducing. A connection pool at its ceiling, memory climbing
without release, file descriptors not closing, a queue backing up.

How to confirm: lower the limit deliberately and the failure arrives sooner; raise it and the failure moves
out. That link between the limit and the rate is the confirmation.

Common shapes: an unclosed handle on the error path, an unbounded cache or list, a query inside a loop that
exhausts a pool, a subscription created without a matching teardown.

## Suspect four, time and timezone

Symptoms: fails at a particular hour, fails at month or year boundaries, fails for users in one region,
fails around a daylight saving change, or fails only when the run crosses midnight.

How to find it: log the timestamps and the timezone of the failing runs. Compare the environments field by
field for locale and timezone settings.

How to confirm: freeze the clock at the suspected boundary and the failure becomes deterministic.

Common shapes: local time stored where an instant was meant, a duration computed across a daylight saving
change, a date parsed with the wrong locale, a cache that expires on a boundary.

## When it will not reproduce locally at all

Add observability where the failure actually happens rather than reasoning about it. Log the inputs at the
failure point, capture the state, and let production hand you the reproduction you cannot build locally.
Then shrink from the real inputs.

## The trap to avoid

A symptom that stopped without an explanation is not fixed. If the rate dropped and you cannot say why,
record that plainly. An intermittent bug that disappears under observation returns in production at a worse
time, and a closed ticket with an unexplained resolution is a bug waiting to come back.

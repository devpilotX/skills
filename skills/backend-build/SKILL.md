---
name: backend-build
description: Build server side services and APIs that behave correctly under retries, concurrency and failure. Use when the user asks to build an API, a backend, a server, a REST or GraphQL endpoint, a microservice, a webhook handler, a background job or a queue consumer, asks about authentication, authorisation, validation, rate limiting, pagination or versioning, or asks why their service breaks under load or duplicates work. Treats idempotency, authorisation on the object rather than the route, timeouts on every outbound call, and structured errors as part of the first version instead of a later hardening pass. Names the concurrency assumption in every write path. Triggers on build an API, build a backend, REST endpoint, GraphQL, microservice, webhook, background job, queue consumer, authentication, rate limiting, pagination, API versioning.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Backend build

The defects that matter in a backend are concurrency, retries and authorisation. They are invisible in
development and expensive in production.

The handler code, service functions and job consumers this skill produces follow the `code-craft` contract:
validation at the edge, decisions in functions that take values and return values, and errors that carry
context across each boundary.

If the user wants an endpoint built to a shape they have already fixed and does not want the hardening
questions, the off switch is saying "just execute" or "stop". This skill then writes what was asked without
adding idempotency or rate limiting on its own, and it stays off for the rest of the session unless the user
asks for the full treatment again.

## Fit to the project

Read the existing service before writing a new endpoint. A handler that ignores the house pattern is a
second style the next reader has to learn.

1. Find the framework and its router from the manifest and the entry point, then read two or three existing
   handlers end to end. Copy how they authenticate, where authorisation happens, how they validate input,
   and how they shape a response. Match that structure exactly.
2. Detect the error contract already in use: the status codes returned, whether errors carry a machine
   readable code, and whether a correlation identifier is set at the edge. Extend the existing shape rather
   than inventing a second one.
3. Read how background work is run today, if at all. Look for a queue library, a worker process, or a
   scheduler, and put new jobs there with the same retry and dead letter handling the existing jobs use.
4. Check how outbound calls are made and whether timeouts and retries are already wrapped in a shared
   client. Reuse that client so the new call inherits the same limits.

When the project has settled none of this, pick the framework's documented conventions, state the identifier
strategy and error shape you chose, and write them down so the next endpoint matches this one.

## Non-negotiables

1. Authorise on the object, not only on the route. Confirming that someone is logged in and then loading a record by an identifier from the request is the most common serious defect in web software. Check ownership every time.
2. Every write path states its concurrency assumption. What happens when this runs twice at once, or twice in sequence because a client retried. Write it down in a comment if the answer is subtle.
3. Every outbound call has an explicit timeout, chosen rather than defaulted, plus a retry policy with backoff and a cap. An unbounded retry turns a brief dependency blip into an outage you caused.
4. Anything that can be retried is idempotent, with a key decided before the code is written. Payment capture, email sending and webhook handling are the standard places this is missed.
5. Validate every input at the boundary against a schema, then work with typed data inside. Never trust a field because the client sends it, including identifiers, prices and role names.
6. Errors are structured, with a stable machine readable code, a safe message, and a correlation identifier. Never return a stack trace or a database error to a caller.
7. Never log a secret, a token, a card number or a full personal record. Logs leak more data than databases do.

## Procedure

### Step 1, define the contract before the code

Resources, operations, request and response shapes, error codes, and pagination. Write it down, as an
OpenAPI or GraphQL schema where possible, and agree it with whoever consumes it.

Design guidance for resource naming, status codes, pagination, filtering, versioning and bulk operations
is in `references/api-design.md`.

A contract written after the implementation documents whatever happened rather than what was intended.

### Step 2, model the data and the transaction boundaries

Work out which operations must be atomic. That decides the transaction boundaries, and therefore whether
a piece of work can be split across services at all.

Use the database for what it is good at: constraints, uniqueness, foreign keys, and transactions.
Enforcing these only in application code means they will eventually be violated. See `data-layer`.

Decide the identifier strategy now. Sequential integers are enumerable by anyone who can guess, so use
opaque identifiers on anything exposed externally.

### Step 3, build the request path

Structure each handler the same way: authenticate, authorise on the object, validate the input, do the
work in a service function, map the result to a response.

Keep transport concerns out of business logic. A service function taking a request object cannot be
tested or reused.

Return the correct status code, and be consistent. A client that receives 200 with an error body cannot
handle failure.

Set a request identifier at the edge, put it in every log line, and return it in error responses. This
single practice does more for debugging than any other.

### Step 4, handle concurrency explicitly

Read then write without protection is the classic lost update. Use a conditional update, a version
column, a unique constraint, or a row lock. Pick one deliberately.

Use the database's own atomicity where possible, since an atomic increment beats a read followed by a
write.

Take locks in a consistent order everywhere, or eventually two paths deadlock.

Check that a unique constraint exists for anything that must be unique, and handle the violation rather
than checking first and inserting after, which races.

The technique to pick per operation, how to build an idempotency key that survives retries, what to retry
and what never to, and a worked payment capture are in `references/idempotency.md`.

### Step 5, background work

Anything slow, external or retryable belongs in a job, not in the request. Sending mail, generating
files, calling third parties, and processing uploads.

Use a durable queue. A timer inside a web process loses work on deploy.

Make every consumer idempotent, because delivery repeats.

Give every job a retry limit and a dead letter destination that somebody actually watches. A dead letter
queue nobody monitors is a silent data loss channel.

Make jobs resumable or small enough to restart. A job that fails at step nine of ten and restarts from
the beginning may never complete.

### Step 6, protect the service

Rate limit per identity and per address on anything that authenticates, sends messages, or costs money.

Bound every input: page sizes, payload sizes, array lengths, string lengths, upload sizes, and query
depth for GraphQL.

Time out long requests rather than holding a connection.

Expose a health check that checks dependencies, and a readiness check that reports whether traffic should
arrive.

Shut down gracefully: stop accepting new work, finish what is in flight, close connections.

### Step 7, verify

Run the service. Call the endpoints. Paste the real output.

Test the paths that matter: authorisation on someone else's object, the same request twice, an invalid
payload, a missing field, a dependency timing out, and a concurrent double submit.

Check what the logs contain, both for what is missing and for what should not be there.

## Self-audit

- Object level authorisation on every read and write of user owned data.
- Concurrency assumption stated for every write path.
- Timeout and bounded retry on every outbound call.
- Idempotency key on everything retryable.
- Schema validation at the boundary.
- Structured errors with codes and a correlation identifier, and no internal detail leaked.
- Rate limits on authentication and anything costly.
- Background work durable, idempotent, with a watched dead letter path.
- Endpoints actually called, with output shown.
- Logs checked for secrets and personal data.

## Honest limits

This skill covers the request path, concurrency, retries and background work. It does not design the schema
or the indexes behind the writes it describes, which belong to `data-layer`, and it does not judge whether
the service boundary is in the right place, which is an architecture question `arch-decide` owns. The
readability and structure of the code it emits are held to the `code-craft` contract rather than defined here.

The retry and timeout guidance comes from what keeps a dependency blip from becoming a self inflicted outage,
not from a benchmark of your stack. Any concrete limit, quota or rate a provider imposes has to be retrieved
from that provider with a date, because those numbers change and this file does not track them.

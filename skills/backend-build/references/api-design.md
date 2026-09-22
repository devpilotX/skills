# API design

## Resources and methods

Name resources as plural nouns. Put the verb in the method, not the path. `POST /orders` rather than
`/createOrder`.

Nest only to show ownership, and only one level. `/orders/{id}/items` is fine. Three levels deep becomes
unusable, so link by identifier instead.

For operations that genuinely are not resource shaped, such as a state transition, a sub resource is
clearer than an invented verb. `POST /orders/{id}/cancellation` beats `POST /cancelOrder`.

Keep identifiers opaque in anything public. Sequential integers let anyone count your customers and
guess other records.

## Status codes

200 for a successful read or update that returns a body. 201 with a Location header for a creation. 202
when the work was accepted and will finish later. 204 for success with nothing to return.

400 for a malformed request. 401 when authentication is missing or invalid. 403 when the caller is
authenticated but not permitted. 404 when the resource does not exist, or when it exists and the caller
may not know that. 409 for a conflict such as a duplicate or a version mismatch. 422 when the request
parsed but failed domain validation. 429 when rate limited, with a Retry-After header.

500 for a fault on your side, and nothing else. Returning 500 for a validation failure sends clients into
retry loops and hides real faults in your alerting.

Be consistent. Clients build error handling once.

## Error bodies

Return a stable machine readable code, a human readable message safe to display, the field that failed
where applicable, and a correlation identifier.

```
{
  "code": "insufficient_funds",
  "message": "The account balance is lower than the requested amount.",
  "field": null,
  "request_id": "01HQ8F2K9M3N4P"
}
```

The code is the contract, so never change its meaning. The message can be reworded freely, which is why
clients must not match on it.

For validation failures, return every failing field at once. Returning them one at a time forces a
round trip per mistake.

Never include a stack trace, a query, an internal hostname, or a database error.

## Pagination

Cursor based pagination for anything that changes while being read, which is most things. Offset
pagination skips and duplicates rows when items are inserted during iteration.

Return the cursor for the next page and a flag for whether more exists. Avoid promising a total count on
a large table, because computing it is expensive and it is usually decoration.

Cap the page size on the server and document the cap. A client will request everything.

Keep the sort deterministic by including a unique tiebreaker, or pagination drifts.

## Filtering and sorting

Allow filtering on a defined set of fields and reject the rest, rather than passing arbitrary input into a
query.

Allow sorting on a defined set of fields, all of which have an index.

Document the default sort, since clients depend on it whether or not it is specified.

## Versioning

Version when you must break something. Adding an optional field is not breaking, so it does not need a
version.

Prefer a version in the path, since it is visible in logs and easy to route. Header versioning is
technically tidier and harder to debug.

Support the previous version for a stated period, and state it in writing. An undocumented deprecation is
an outage scheduled for a random date.

Breaking changes include removing or renaming a field, changing a type, making an optional field
required, narrowing an enum a client sends, changing a default, and changing an error code's meaning.

Not breaking: adding an optional field, adding an endpoint, adding an enum value the client only reads,
though clients must handle unknown values for that to hold.

## Idempotency

Accept an idempotency key on any unsafe operation a client might retry, and store the first response
against it. Return the stored response on a repeat rather than doing the work twice.

Keep keys for long enough to cover the client's retry window, and document how long.

For webhooks you receive, treat the provider's event identifier as the idempotency key, because providers
redeliver.

## Bulk operations

Decide whether the whole batch is atomic, and say so in the documentation. Partial success with a per
item result is usually more useful than all or nothing.

Return a per item outcome with the item's identifier, so a client can retry only what failed.

Cap the batch size.

For large batches, return 202 with a job identifier and provide a way to check progress.

## Authentication and authorisation

Short lived access tokens with a refresh path. Validate signature, expiry, audience and issuer, and
reject anything unexpected.

Scope tokens to what the caller needs. A token that can do everything turns any leak into a total
compromise.

Check permission on the object on every request. Never cache an authorisation decision across requests
without also expiring it on permission change.

For service to service calls, use short lived credentials rather than a static shared secret.

Rate limit authentication endpoints separately and more tightly than the rest.

## Webhooks you send

Sign the payload and document the verification steps.

Include an event identifier and a timestamp so receivers can deduplicate and reject replays.

Retry with backoff, and give up after a stated number of attempts. Expose the failed deliveries so the
receiver can see what they missed.

Keep the payload small and let the receiver fetch detail, or the payload becomes a second API you have to
version.

Send from a stable set of addresses and document them, since receivers will want to allow them.

## GraphQL specifics

Limit query depth and complexity, because an unbounded nested query is a denial of service.

Solve the N+1 problem with batching at the data loading layer. It appears immediately and is the default
behaviour of a naive resolver.

Authorise per field where fields have different sensitivity, not only per query.

Disable introspection in production if the schema is not public.

Remember that a single endpoint hides per operation metrics unless operation names are logged.

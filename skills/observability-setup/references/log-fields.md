# Log field set, levels, and leak patterns

The main file says to emit one JSON object per event with a consistent set of fields. This is the
field set to standardise on, what each level means in practice, and the patterns to grep for before a
line ships a secret to storage you cannot redact.

## The base field set

Every line carries these, whatever the event is. A query that has to guess the field name is a query
nobody writes at three in the morning.

| Field | Type | Meaning |
| --- | --- | --- |
| timestamp | ISO 8601 with timezone | When the event happened, not when it was written |
| level | string | One of error, warn, info, debug |
| message | string | A short constant string, not an interpolated sentence |
| correlation_id | string | Generated at the edge, same value for the whole request |
| service | string | Which service emitted the line |
| version | string | The build or release the line came from |

Keep `message` constant so it can be grouped. Put the variable part in its own field. A message of
"order placed" with an `order_id` field groups; a message of "order 4821 placed" produces one unique
string per order and groups into nothing.

## Operation fields

Added when the event belongs to a known operation. Present on some lines, absent on others, which is
fine as long as the name is stable when present.

| Field | When present | Example |
| --- | --- | --- |
| user_id | request has an authenticated principal | account identifier, never the email |
| tenant_id | multi tenant system | workspace or organisation identifier |
| method | inbound or outbound HTTP | GET, POST |
| route | inbound HTTP | templated path such as /orders/:id, never the filled path |
| status | request completed | 200, 503 |
| duration_ms | request or call completed | integer milliseconds |
| target | outbound call | the dependency name, not the full URL with query string |
| outcome | any call | success, timeout, refused |
| error_kind | handled error | a stable class name, not the raw exception message |

## Levels and when each applies

The level decides who wakes up, so it is a routing decision, not a mood.

Error means a human should look, and the line is a candidate to become an alert. Reserve it for a
failure the system could not handle itself. A caught and retried timeout that then succeeded is not an
error, it is a warn at most.

Warn means recoverable but notable: a retry happened, a fallback was used, a limit was approached, a
deprecated path was hit. Warns that never get read should be downgraded to info or deleted.

Info is the operational narrative: request received, request completed, job started, job finished. It
is what you read to reconstruct what happened, so it stays on in production.

Debug is off in production. If you find yourself wanting debug on in production, the missing
information is a field on an info line, not a lower level.

## Leak patterns to grep before shipping

Run these against a sample of real output, not against the code, because the leak is usually in a field
that gets serialised whole. The main file's verify step calls for this; here are the patterns.

Card numbers: a run of 13 to 19 digits, optionally split by spaces or hyphens. Match on the digit run
and check the neighbourhood, since order totals and identifiers also produce long digit runs.

Bearer tokens and API keys: the literal string "Bearer " followed by a long token, or a field named
authorization, api_key, secret, token, or password with any non empty value.

Email addresses: a local part, an at sign, and a domain. Legitimate in an audit log for a login event,
a leak in a generic debug dump of a request body.

Full request or response bodies: any line that serialised an entire payload object. This is the most
common leak, because it captures whatever the payload happened to contain, including the fields nobody
listed.

Private keys: the header line beginning "-----BEGIN" for any key block.

When a pattern matches, the fix is a redaction filter at the log boundary keyed on field name, plus a
rule that request and response bodies are never logged whole, only named fields from them.

## A worked line

A completed request, authenticated, that called one dependency:

    {
      "timestamp": "2024-03-11T02:14:07.412Z",
      "level": "info",
      "message": "request completed",
      "correlation_id": "b1f2c3d4",
      "service": "checkout",
      "version": "2024.03.2",
      "user_id": "u_88213",
      "tenant_id": "t_014",
      "method": "POST",
      "route": "/orders/:id/pay",
      "status": 200,
      "duration_ms": 148,
      "target": "payments-api",
      "outcome": "success"
    }

Every field on that line is queryable, none of it is a secret, and the route is templated so the
metrics built from it do not explode the label cardinality.

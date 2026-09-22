# Money representation, idempotency, and webhook safety

Three defects account for most payment bugs: money as floating point, charges without idempotency, and
webhooks trusted without verification. Each has a mechanical fix.

## Store money as integer minor units

A currency has a minor unit: cents for a dollar or euro, and zero minor digits for currencies such as
the Japanese yen. Store the amount as an integer count of that minor unit, and store the currency code
next to it. Never store money as a floating point number.

Floating point cannot represent 0.10 exactly in binary, so a sum of amounts drifts by a cent over
enough additions, and a comparison that should be equal is not. An integer of 1099 with currency USD
means the same thing on every machine and sums without drift.

```
# wrong
price = 10.99            # float dollars, will drift
# right
amount_minor = 1099      # integer cents
currency = "USD"
```

Convert to a display string only at the edge, using the currency's known minor-unit count, and never
compute on the display value. A currency with zero minor units breaks any hardcoded divide-by-100, so
read the minor-unit count from a currency table rather than assuming two.

## Idempotent charge creation

A create-charge request can time out after the provider created the charge but before your client got
the response. The client retries. Without protection, the retry creates a second charge and the
customer pays twice.

The fix is an idempotency key tied to the unit of work, not to the request instant. Derive it from
something stable such as the order id, so every retry of the same logical charge sends the same key. The
provider returns the first result for a repeated key instead of charging again.

```
key = idempotency_key_for_order(order.id)
result = provider.create_charge(
    amount_minor=order.amount_minor,
    currency=order.currency,
    source=order.payment_token,
    idempotency_key=key,
)
store_charge(order.id, result.charge_id, result.status,
             order.amount_minor, order.currency)
```

On a timeout, do not retry with a new key. Query the provider for the charge, or wait for the webhook,
because a new key on a retry defeats the whole mechanism.

## Verify webhook signatures on the raw body

A webhook endpoint is a public URL, so anyone can post to it. Verify the provider's signature over the
exact bytes of the request body before trusting anything in it. Parsing the JSON and re-serialising it
changes whitespace and key order, which changes the bytes and breaks the signature check, so verify
before parsing.

```
on webhook(request):
    raw = request.raw_body            # exact bytes, not re-serialised
    if not provider.verify_signature(raw, request.headers["Signature"], signing_secret):
        return 403
    event = parse(raw)
    if already_processed(event.id):   # replay or provider retry
        return 200
    apply_event(event)
    mark_processed(event.id)
    return 200
```

## Handle replay and out-of-order delivery

Providers retry a webhook they think failed, and they do not guarantee order. Two rules keep this
correct.

Record every event id and skip any id you have already applied, so a retry or a deliberate replay
changes nothing. Treat each event as a statement about state and apply only forward transitions, so a
late-arriving `payment.created` cannot overwrite a `payment.succeeded` that already landed. A small
state machine, where each status has a rank and you only move up, handles this without special-casing
every pair.

Return the success status fast and push slow work, such as sending a receipt or provisioning access,
onto a queue. A handler that does slow work inline will time out, the provider will retry, and you will
process the same event twice under load.

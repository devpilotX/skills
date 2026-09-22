---
name: payments-integrate
description: Take money through a payment provider without double charging, losing track of a payment, or putting card data where it does not belong, on any stack and any provider. Covers idempotent charges, webhook signature verification and replay handling, storing money as integer minor units, refunds and disputes, subscription proration and dunning, and reconciling your records against provider payouts. Use when adding checkout or a subscription, when a retried request charged a customer twice, when webhooks are missed or arrive out of order, when refunds or disputes are unhandled, when amounts round wrong, or when your revenue does not match the provider payout. Triggers on integrate payments, add stripe checkout, accept credit cards, charged customer twice, idempotency key, verify webhook signature, handle payment webhooks, store money correctly, floating point money bug, process refunds, handle chargebacks, subscription billing, failed recurring payment dunning, reconcile payouts, PCI scope.
license: MIT
compatibility: Any language, any web or mobile application, any payment provider that offers hosted card entry and signed webhooks. No single vendor is required.
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Payments integrate

A model asked to add payments usually calls the charge endpoint directly, stores the amount as a
floating point number of dollars, trusts the webhook body without checking its signature, and treats
the API call as the source of truth. Each of those is a defect that surfaces as a double charge on a
retry, a cent that vanishes in rounding, a forged payment marked paid, or a month-end where the ledger
does not match the bank. Taking money is a bookkeeping problem with a network in the middle, and the
network is unreliable by design.

## Fit to the project

Read the existing setup before writing any charge code.

1. Find whether a provider is already integrated. Look for a provider SDK in the dependency manifest,
   API keys in configuration or a secrets store, and any existing webhook route. Extend the existing
   integration rather than adding a second provider that fragments the reconciliation.
2. Detect how money is stored today. Search the schema and models for amount fields and their types. A
   float or a decimal without a currency column is a defect to fix before adding more charges, because
   every later number inherits it.
3. Find where card entry happens. If any card number touches your servers or your logs, that is the
   highest-priority problem, because it pulls the whole system into the scope that has to be audited.
   Card entry belongs in the provider's hosted field or element, never in a field you post to your own
   backend.
4. Note whether webhooks are verified and idempotent today. An unverified webhook handler and a charge
   path with no idempotency key are the two failures that cost real money, so confirm their state first.

Adopt the provider the project already uses. Any major provider handles the mechanics here; the
integration discipline is what this skill is about.

## Non-negotiables

1. Card data never touches your systems. Use the provider's hosted page, iframe, or client-side element
   so the card number goes from the browser to the provider directly, and your server only ever sees a
   token. A card number in a log line or a database column expands the audit scope to your entire
   infrastructure and turns a routine breach into a reportable one.
2. Every charge creation carries an idempotency key derived from the order, not from the moment of the
   request. A network timeout makes the client retry, and without the key the retry creates a second
   charge. The key is what makes a retried request return the first result instead of charging again.
3. Every webhook is signature-verified against the raw request body before it is trusted, and processed
   at most once by recording the event id. An unverified endpoint accepts a forged event that marks an
   order paid, and a replayed event double-credits an account.
4. Money is stored as an integer count of the currency's minor unit together with the currency code,
   never as a floating point number. Floating point cannot represent most decimal fractions exactly, so
   sums drift by cents, and an amount without a currency is meaningless the moment you sell in a second
   country.
5. Your database is the source of truth for what happened, updated only from verified webhooks and
   confirmed API responses, and reconciled against the provider's payout report on a schedule. The API
   response alone is not enough, because a charge can succeed at the provider after your request timed
   out.
6. Generated charge, webhook, and reconciliation code follows the `code-craft` contract: the charge
   path, the webhook verifier, and the reconciliation job live in separate functions, and every failure
   carries which order, which charge, and which currency it concerned.

## Procedure

### Step 1, choose or confirm the provider

If none is chosen, weigh the criteria that matter on day one against the ones that matter after the
first month. Day one: does it support the countries and currencies you sell in, does it offer hosted
card entry so your audit scope stays small, and are the payout timing and fees acceptable. After the
first month: dispute handling, subscription and proration support if you need it, the quality of the
webhook and reconciliation reporting, and how hard it is to leave. A provider that is easy to start
with and hard to reconcile costs more over a year than its fee suggests. The full checklist is in
`references/provider-choice.md`.

### Step 2, keep card data out and tokenize

Put card entry in the provider's hosted field so the number never reaches your backend. Your server
receives a token, creates a payment from the token, and stores the token reference, never the card.
Confirm that no card field posts to your own routes and that no card data appears in any log. This is
what keeps the integration in the lightest audit scope rather than the heaviest.

### Step 3, create charges idempotently

Generate an idempotency key tied to the unit of work, such as the order id, so that any retry of the
same logical charge carries the same key. Send it on every create call. Store the charge with its
status, amount in minor units, currency, and the provider's charge id. Treat a timeout as unknown, not
as failure: query the provider or wait for the webhook rather than retrying with a fresh key, because a
fresh key on a retry is exactly how a double charge happens. A worked money model and charge flow are
in `references/money-and-webhooks.md`.

### Step 4, verify and process webhooks safely

Verify the signature on the raw, unparsed request body, because parsing and re-serialising changes the
bytes and breaks the check. Record each event id and skip any id already processed, so a replay or a
provider retry is a no-op. Handle out-of-order arrival by treating each event as a statement about
state and applying only forward transitions, so a late `created` event never overwrites a later
`succeeded`. Return a success status quickly and do slow work asynchronously, or the provider will
retry a handler it thinks failed. The verification and ordering pattern is in
`references/money-and-webhooks.md`.

### Step 5, handle refunds, disputes, and subscriptions

Support full and partial refunds against the original charge, storing each refund as its own record so
the net stays computable. Treat a dispute as a separate flow with its own deadline and evidence
submission, and expect the funds to be held meanwhile. For subscriptions, handle the whole lifecycle:
proration when a plan changes mid-period, dunning retries when a recurring charge fails, and the
involuntary churn that follows when retries are exhausted. The lifecycle and its edge cases are in
`references/subscriptions.md`.

### Step 6, settle tax and reconcile payouts

Decide the tax question before launch, not after: which jurisdictions you owe collection in, whether
the provider or a tax service computes it, and where the collected amount is recorded. Then reconcile
on a schedule. Pull the provider's payout report, match each settled charge, refund, and fee to your
own records, and investigate every difference rather than absorbing it. Report the provider chosen, the
money representation, the idempotency and webhook handling, the subscription behavior, and the
reconciliation cadence.

## Self-audit

- Is all card entry in the provider's hosted field, with no card number reaching your servers or logs?
- Does every charge create call carry an idempotency key derived from the order rather than the request
  moment?
- Is every webhook signature-verified on the raw body and recorded so a replay is a no-op?
- Is money stored as an integer minor unit alongside a currency code, with no floating point amount
  anywhere?
- Does the database update only from verified webhooks and confirmed responses, and is it reconciled
  against payouts on a schedule?
- Are refunds stored as their own records so the net charge stays computable?
- For subscriptions, are proration, dunning, and involuntary churn all handled rather than assumed?
- Was the tax question answered before launch, and does the report name where collected tax is
  recorded?

## Honest limits

This skill gets the integration mechanics right so money is not lost or double-taken. It does not choose
your pricing or your business model, which belongs to `business-model`, and it does not write the
bookkeeping that turns these records into financial statements, which belongs to `finance-books`. It is
not tax advice or a compliance sign-off: which taxes you owe and where, and which data-protection rules
apply to stored payment records, are questions for a qualified professional and for `compliance-map`.

The provider selection criteria and the dunning intervals here are rules of thumb, not fixed rules, and
a specific provider's documented behavior overrides them. Nothing here certifies your PCI scope; that is
a determination your provider and a qualified assessor make. The application code around the charge path
is owned by `backend-build`, and its readability by `code-craft`.

The off switch: say "stop" or "just execute" and this skill stands down for the rest of the session.
It stays off until you invoke it again. You can ship a charge call with none of this discipline, and the
first retry storm or the first month-end reconciliation will tell you what it skipped.

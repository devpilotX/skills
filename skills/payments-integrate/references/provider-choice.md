# Choosing a payment provider

The criteria that sell you a provider on day one are not the ones that hurt after the first month. Weigh
both before committing, because switching a live payment integration is expensive and risky.

## What matters on day one

Coverage. Does it support the countries you sell from and to, the currencies you price in, and the
payment methods your customers actually use. A provider that is strong in one region can be weak in
another, and a card-only provider loses sales where bank transfers or local wallets dominate.

Audit scope. Does it offer hosted card entry, a hosted page, an iframe, or a client-side element so the
card number never reaches your servers. This keeps the integration in the lightest compliance scope. A
provider that expects you to post card numbers to your own backend pulls your whole infrastructure into
the heaviest scope, which is a cost measured in audits, not fees.

Cost. The headline percentage plus the per-transaction fee, currency conversion margins, and payout
timing. A lower percentage with a longer payout hold can be worse for cash flow than a slightly higher
fee that settles daily.

Integration effort. Whether there is a maintained SDK for your language, sandbox credentials you can
test against, and documentation that covers the failure cases rather than only the happy path.

## What matters after the first month

Dispute handling. How disputes and chargebacks are surfaced, how much time you get to respond, whether
evidence submission is programmatic, and what the fee is per dispute regardless of outcome. Disputes are
where a payment integration quietly bleeds money if the flow is manual.

Subscription support, if you need it. Whether the provider handles proration on plan changes, retries
failed recurring charges on a schedule you can configure, and reports the reason a recurring charge
failed so you can act on it.

Webhook and reporting quality. Whether events are signed, whether they are delivered reliably with
retries, whether there is a payout report that itemises each charge, refund, and fee, and whether you
can pull historical data. Reconciliation lives or dies on this.

Exit cost. Whether you can export stored payment tokens to another provider, or whether your customers
would have to re-enter cards to move. A provider that holds tokens hostage raises the real cost of ever
leaving, so ask about token portability before you are locked in.

## A short scoring approach

List the currencies, methods, and countries you need, and drop any provider that does not cover them.
Of those that remain, prefer the one whose reporting and dispute handling you can live with for years,
not the one with the smoothest signup. Signup is a day; reconciliation is every month.

Treat any provider fee comparison as a rule of thumb until you model it against your real transaction
mix, because blended rates hide the cases that dominate your volume.

## Multi-provider is a later problem

Running two providers at once multiplies the reconciliation work and the webhook surface. Do it only
when one provider genuinely cannot cover a market, and when you do, keep each provider's charges and
payouts reconciled separately so a difference localises to one of them.

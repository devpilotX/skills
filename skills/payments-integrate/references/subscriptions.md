# Subscriptions, refunds, disputes, and reconciliation

Recurring billing adds failure modes that a one-off charge never sees. Handle the whole lifecycle rather
than the signup, because the money is lost in the parts after signup.

## Refunds and partial refunds

Store each refund as its own record linked to the original charge, with its own amount in minor units
and currency. Do not mutate the charge amount, because you lose the history and the net becomes
uncomputable. The net received on a charge is the charge amount minus the sum of its refunds, and that
sum has to stay derivable at any point.

A partial refund refunds part of the charge. Several partial refunds can stack, and their total can
never exceed the original charge. Enforce that ceiling in your own code rather than relying on the
provider to reject the overage, so your records never claim a refund larger than the payment.

## Disputes and chargebacks

A dispute is the cardholder's bank reversing a charge. It is not a refund you control: the funds are
usually pulled immediately and held until the dispute resolves, and there is a fixed deadline to submit
evidence. Model it as a separate flow with a deadline, a place to attach evidence, and a status that
tracks won or lost.

A dispute usually carries a fee regardless of who wins, so a low-value charge is rarely worth
contesting on economics alone. Record disputes against the charge so a customer with a pattern of them
becomes visible, since repeated disputes from one account are a signal worth acting on before the
provider raises your dispute rate.

## Subscription lifecycle

Proration. When a customer changes plan mid-period, the provider computes a credit for the unused part
of the old plan and a charge for the remainder of the new one. Decide whether a change takes effect
immediately with proration or at the next renewal, and store which, because the two produce different
invoices and support tickets follow from the surprise.

Dunning. When a recurring charge fails, usually because a card expired or had insufficient funds, the
provider retries on a schedule you configure. Configure a finite retry sequence over days, notify the
customer with a way to update the card, and decide what access they keep during the retries. Retrying
forever annoys the bank and can raise your decline rate.

Involuntary churn. When the dunning retries are exhausted, the subscription lapses through a failed
payment rather than a deliberate cancel. Distinguish this in your records from a voluntary cancel,
because the two need different follow-up: a lapsed card is often recoverable with a reminder, while a
deliberate cancel is not, and treating them the same wastes effort on one and neglects the other.

## The tax question, before launch

Decide before you launch, not after the first return is due. Which jurisdictions require you to collect
a sales tax, value added tax, or goods and services tax on the sale. Whether the provider, a dedicated
tax service, or your own code computes the amount. Where the collected tax is recorded, kept separate
from revenue, because it is money you owe onward rather than money you earned. The specific rates,
thresholds, and registration rules are jurisdiction-specific and change, so retrieve them from the
relevant tax authority or a qualified adviser rather than assuming a figure.

## Reconciling against payouts

The provider settles money to your bank as payouts, and a payout bundles many charges, refunds, and
fees net of each other. Reconciliation matches your records against that payout so you can prove what
you were paid and catch anything missing.

On a schedule, pull the payout report and match each line to a charge, refund, or fee in your database.
The gross of the charges minus refunds minus provider fees should equal the payout amount. When it does
not, the difference points at the cause: a fee you did not record, a refund that did not reach your
database because a webhook was missed, or a charge settled in a different period. Investigate every
difference rather than absorbing it, because a plugged difference hides a real gap that grows.

Keep the provider fee as its own recorded amount rather than netting it silently, so your revenue and
your cost of payment processing stay separately visible for the bookkeeping that `finance-books` covers.

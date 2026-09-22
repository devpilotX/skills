# A worked model, unit to funding need

This walks one small business from a bare idea to a funding number, so the steps in the main file have a
concrete shape to copy. The business is a subscription meal kit delivered weekly. Every figure below is
labelled as an assumption, because in a real engagement they would come from the user or from a cited
source. The point is the structure and the order, not the numbers.

## The unit

One unit is one delivered weekly box. Hold this constant. Do not switch to "one customer" halfway through,
because a customer buys a variable number of boxes and mixing the two is the most common structural error.

## Contribution margin per unit

Revenue per box: 40 (ASSUMPTION, the current headline price).

Costs that vary with each box:

  Ingredients at wholesale: 14 (ASSUMPTION, from a supplier quote)
  Packaging and the insulated liner: 3 (ASSUMPTION)
  Courier for one delivery: 7 (ASSUMPTION, a per drop rate)
  Payment processing at 2.5 percent plus 0.30: 1.30
  Spoilage and swaps at 4 percent of ingredient cost: 0.56
  Support, one contact per eight boxes at 4 per contact: 0.50

Total variable cost: 26.36
Contribution margin per box: 40 - 26.36 = 13.64

Contribution margin is positive, so volume helps rather than hurts. If it had been negative the model
would stop here, because no scale fixes a unit that loses money on every sale.

## Fixed monthly costs

  Kitchen rent and utilities: 2200 (ASSUMPTION)
  Two part time packers: 3200 (ASSUMPTION)
  Insurance: 180 (ASSUMPTION)
  Accounting and software: 260 (ASSUMPTION)
  Founder minimum draw: 2500 (a market rate for the hours, not zero)

Total fixed monthly cost: 8340

Paying the founder is not optional in the model. A plan that only works when the owner works unpaid is a
job with extra risk, and hiding the draw makes a losing plan look like a winning one.

## Break-even volume

Break-even boxes per month = fixed cost / contribution margin per box
  = 8340 / 13.64
  = 612 boxes per month, about 141 boxes per week.

Now the test that matters: can a named channel deliver 141 boxes a week? At an assumed 3 boxes per new
customer per week that is about 47 active subscribers. Whether that is reachable depends on the channel,
and a break-even number with no distribution answer is arithmetic without meaning.

## Working capital cycle

  Ingredients paid on delivery, so inventory days are low: 3 days.
  Customers pay upfront on subscription, so receivable days are 0.
  The courier invoices weekly, net 7: payable days 7.

Cycle = inventory days + receivable days - payable days = 3 + 0 - 7 = -4 days.

A negative cycle means customers fund the business before suppliers get paid, which is the comfortable
case. If the model had been net 30 invoicing to corporate clients instead, the cycle would swing positive
and the cash locked up would grow with revenue. Always recompute the cycle at three times current volume,
because growth magnifies whatever sign the cycle has.

## Acquisition and payback

  Cost to acquire one subscriber through paid social: 55 (ASSUMPTION, from a small test)
  Contribution per subscriber per month at 3 boxes a week: 13.64 * 3 * 4.3 = about 176 per month.

Payback period = acquisition cost / monthly contribution = 55 / 176 = under one month.

Payback inside the cash cycle means growth can be funded from revenue rather than from outside money.
That test matters more than lifetime value, which depends on a retention curve that does not exist yet.

## Peak funding need

Even with a negative cycle, the fixed costs run before revenue reaches break-even. If it takes four months
to grow from zero to 47 subscribers, the model has to carry roughly four months of the gap between fixed
cost and contribution. Compute that month by month, take the lowest point of the running cash balance, and
that trough is the funding need. Assuming a steady climb, the trough here sits near 18000 to 22000, which
is the number to raise or to hold in reserve before starting.

## The deciding assumption

Vary each input across its range. Here the outcome moves most on the acquisition cost: at 55 the model
works, at 140 payback stretches past the point where revenue can fund growth and the business needs
outside capital to scale. So the one number to verify this week is the real cost to acquire a paying
subscriber, measured with a small paid test rather than assumed.

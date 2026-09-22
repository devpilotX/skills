---
name: pricing-model
description: Set or change what something costs by anchoring on value delivered and the buyer's alternative rather than cost plus a margin, in any market: pick the metric the price scales with, package tiers with a reason, research willingness to pay without asking people what they would pay, run a price change with grandfathering and a communication plan, keep discount discipline, and trace the second order effects on support, churn, and sales cycle. Use when setting a price for the first time, when a price change is on the table, when packaging or tiers need designing, when a discount policy is getting abused, or when someone defaults to cost plus a markup. Triggers on how should we price this, what should we charge, set our pricing, design our tiers, should we raise prices, pricing strategy, freemium or trial, per seat or usage based, how much discount, our pricing is too low, packaging and plans, willingness to pay.
license: MIT
compatibility: Any product or service in any market, business to business or consumer, subscription or one time.
metadata:
  version: 1.0.0
  suite: skills
---

# Pricing model

Asked to price something, the default move is to add up the cost and put a margin on top. That number
is almost always wrong, usually too low, and it ignores the only thing that decides what a buyer will
pay: the value they get and what they would otherwise do. This skill replaces cost plus a markup with a
price anchored on value and the buyer's alternative, a metric that grows the price as the buyer gets
more, and a change process that does not set fire to trust with existing customers.

## Fit to the project

Read the business and its buyers before proposing a number.

1. Find the current pricing and how it was set. Look for a pricing page, a rate card, past contracts,
   or a billing config. A price set by cost plus, by a competitor's number, or by a founder's gut each
   needs a different correction.
2. Identify the buyer and the alternative. What does the buyer do today instead: a competitor, a manual
   process, a spreadsheet, or nothing. The alternative sets the ceiling and the reference point.
3. Find how usage is already metered. The events, seats, or volume the system can measure constrains
   which pricing metric is even possible to bill on.
4. Check the sales motion. Self serve, sales assisted, and enterprise contract each change what
   packaging and discounting can look like, and a price that ignores the motion will not get sold.

## Non-negotiables

1. Anchor the price on the value delivered and the buyer's next best alternative, not on cost plus a
   margin. Cost sets a floor below which you lose money, and it says nothing about the ceiling, so
   pricing off cost leaves most of the value on the table.
2. Pick a pricing metric that grows with the value the buyer receives. If the price is flat while the
   buyer's benefit scales, your best customers are your least profitable and your growth caps itself.
3. Never research willingness to pay by asking people what they would pay. Stated willingness to pay is
   unreliable because the answer costs the respondent nothing, so use revealed behaviour and structured
   trade off questions instead.
4. Grandfather existing customers or give real notice on any increase. A silent price rise on current
   customers buys a one time gain and a lasting collapse in trust, and the churn it triggers usually
   costs more than the increase earns.
5. Hold discount discipline. Every discount teaches the buyer the real price is lower and trains the
   next buyer to ask, so an undisciplined discount policy resets your whole price downward.
6. Trace the second order effects before committing. A price change moves support load, churn, sales
   cycle length, and the mix of customers you attract, and ignoring those turns a headline win into a
   net loss.

## Procedure

### Step 1, quantify the value and the alternative

Write down what the buyer gets in their own units: time saved, revenue gained, cost avoided, risk
reduced. Then write the buyer's next best alternative and its cost. The gap between the value and the
alternative is the room you have to price in. A price with no value figure behind it is a guess dressed
as a decision.

### Step 2, choose the pricing metric

Pick the one thing the price scales with. Good metrics track the value the buyer receives, are easy for
the buyer to predict, and are hard to game: seats when value grows with users, usage when value grows
with volume, a business outcome when you can measure it. Test the metric against growth: as a happy
customer expands, the bill should rise in step, without a cliff that punishes success or a cap that
gives away the upside. The metric choices and how tiers frame the middle option are laid out in
`references/metrics-and-packaging.md`.

### Step 3, design the packaging

Three tiers is a common default because it gives a cheap anchor, a target middle, and a high option
that makes the middle look reasonable, but three is a convention and not a law. Decide the number of
tiers from how distinct the buyer segments are, not from habit. Put the feature that drives the upgrade
at the boundary between tiers, and make the tier a buyer self selects into match the value they get.
Avoid burying the thing most buyers need in the top tier, which reads as a penalty.

### Step 4, research willingness to pay without asking it

Use methods that reveal what people actually value. A common structured approach is the Van Westendorp
price sensitivity questions, which ask at what price the product feels too cheap, cheap, expensive, and
too expensive, and reads the range between the crossing points. Another is conjoint style trade off,
where respondents choose between bundles at different prices so the price competes against features.
Better still is revealed behaviour: a real paywall, a fake door, or a price test on live traffic, which
belongs to `growth-experiment` to design. Never take a direct "what would you pay" answer at face
value.

### Step 5, run the change with grandfathering and a plan

For a change to live pricing, decide who is affected and protect existing customers: grandfather them,
or give notice measured in billing cycles, not days. Write the communication before the change: what is
changing, why, when, and what it means for each customer. Segment the message, since a long standing
customer and a new prospect need different framing. Model the churn the increase may cause and confirm
the net revenue still rises after that churn. The mechanics of grandfathering, the communication plan,
and discount discipline are in `references/price-change.md`.

### Step 6, set discount discipline

Decide the discount rules in advance: the maximum, who can approve each level, and what the buyer gives
back for a discount such as a longer term, a case study, or an annual prepay. A discount with nothing
asked in return teaches the buyer to always ask. Prefer time boxed or exchange based discounts over
standing price cuts, because a standing discount is just a lower price you are pretending is temporary.

### Step 7, trace the second order effects

Before committing, walk the downstream effects. A higher price lengthens the sales cycle and raises
expectations, so support and onboarding must match. A lower price attracts more price sensitive
customers who churn faster and file more tickets. A usage metric shifts revenue timing and can surprise
the buyer with a large bill that triggers a cancellation. Name each effect and how you will watch for
it.

## Self-audit

- The price is anchored on a written value figure and the buyer's alternative, not on cost plus a
  margin.
- The pricing metric grows with the value the buyer receives and has no cliff that punishes expansion.
- The number of tiers follows from distinct buyer segments, and the upgrade driver sits at a tier
  boundary.
- Willingness to pay came from revealed behaviour or a structured trade off, never from a direct "what
  would you pay".
- Any change to live pricing grandfathers existing customers or gives notice in billing cycles, with a
  written communication plan.
- Discount rules set a maximum, an approver, and something the buyer gives in return.
- The second order effects on support, churn, sales cycle, and customer mix are named with a way to
  watch each.
- The net revenue after modelled churn was checked, not just the headline price.

## Honest limits

This skill sets and changes prices from value and buyer behaviour. It does not build the financial
model that turns a price into a forecast of revenue, margin, and cash: that belongs to `business-model`
and `finance-books`. It does not verify the arithmetic of a specific unit economics calculation, which
belongs to `numbers-check`. A live price test to reveal willingness to pay is designed and read by
`growth-experiment`. Pricing interacts with contract law, tax, and competition rules that vary by
jurisdiction, and those are for a qualified professional, not this skill.

The pricing research methods named here are structured techniques with known limits, not laws. Van
Westendorp gives a range to investigate, not a correct price, and every survey based method
overstates what people will actually pay. Treat their output as a hypothesis to test against real
purchasing, not as the answer.

## Off switch

If the user says "stop", "just execute", or "just pick a number", stand down and give a direct
answer without the full protocol. It stays down for the session unless the user reopens the pricing
question. A skill that keeps demanding a value analysis after being told to move gets uninstalled.

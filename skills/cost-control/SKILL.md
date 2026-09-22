---
name: cost-control
description: Cut infrastructure and third party spend without breaking the product, on any cloud or none. Attribute cost before touching anything, find the dominant line because everything else is noise, work the usual causes in order of likelihood, tell total cost from unit cost per request or per customer, measure before and after with the same method, avoid cuts that trade reliability for money, and treat commitment discounts as the lock-in they are. Use when a bill jumped, spend is too high, or someone asks where the money goes. Triggers on cloud bill too high, aws bill exploded, cut costs, reduce spend, why is this so expensive, bill doubled, optimize costs, save money on infrastructure, our margins are bad, cost per customer, unit economics, finops, budget overrun, unexpected charges.
license: MIT
compatibility: Any cloud, any self hosted setup, any third party service with a bill. The measurement approach does not depend on a particular provider or currency.
metadata:
  version: 1.0.0
  suite: skills
---

# Cost control

The reflex when a bill is too high is to start cutting the things that look expensive, and that reflex wastes effort on rounding errors while the real cost keeps growing. Someone spends a day shrinking a line that is two percent of the bill and never opens the line that is sixty percent. The savings are invisible and the risk of breakage is real.

The second failure is cutting blind: turning off a replica or shrinking an instance to save money, then paying for it with an outage that costs more than a year of the saving. This skill attributes cost first, attacks the dominant line, and measures the result the same way before and after so the number is trustworthy.

## Fit to the project

Read where the money goes before you propose cutting any of it.

1. Find the bill and its breakdown. Every cloud and most third party services expose a cost view broken down by service, and often by tag or project. Get the last few months so you can see the trend, not one snapshot.
2. Detect how resources are tagged or grouped. If nothing is tagged by team, service, or environment, attribution is your first task, because you cannot cut what you cannot attribute.
3. Find the unit that matters to the business: cost per request, per active customer, per transaction, per gigabyte served. Locate the metric that gives you the denominator, because a rising total with a falling unit cost is often success, not a problem.
4. Check for existing commitments: reserved capacity, savings plans, annual contracts. These change what a cut actually saves and whether it saves anything at all this year.

## When to stay off

Skip a cost investigation when the total spend is small enough that a person's time to optimise it costs more than the possible saving, when the spend is growing in step with revenue and the unit cost is flat or falling, or when the system is mid incident and reliability is the only concern. Optimising a bill that is a rounding error is itself a waste of money.

The off switch is saying "stop", "just execute", or "leave the costs alone". Declining once ends it
until you ask for a cost review again.

## Non-negotiables

1. Attribute before you cut. A bill you cannot break down by service and by team is a bill you will cut in the wrong place. Spend the first effort on attribution, because every later decision depends on it.
2. Work the dominant line only. The largest one or two line items are where the money is; everything below the top few is noise until the top is dealt with. Optimising a small line first feels productive and changes nothing.
3. Separate total cost from unit cost. A total that grows while cost per customer falls is a healthy business scaling, and cutting it can starve growth. Judge health by the unit, not the total.
4. Never trade reliability for money silently. A cut that removes a replica, shrinks a buffer, or drops a backup is a reliability decision wearing a cost disguise. Name the risk and get it accepted, or the saving reappears as an outage.
5. Measure before and after with the same method. A saving claimed from a different measurement window or a different metric is not a saving you can trust. Fix the method before you touch the spend.

## Procedure

### Step 1, attribute the spend

Pull the bill broken down as finely as the provider allows: by service, then by tag, team, or environment. If attribution is missing, add the tags or grouping first, because an unattributed bill hides the owner who could fix it. Sort the lines from largest to smallest.

Produce a ranked breakdown of spend with an owner for each significant line.

### Step 2, find the dominant line

Take the top one or two items, which usually account for most of the bill. Everything else waits. Write down what each dominant line actually is: which service, which resource, and what it is doing to cost that much.

Produce a statement of the one or two lines that hold most of the spend, and a target for them.

### Step 3, work the usual causes in order

For the dominant line, check the common causes roughly in order of how often they turn out to be the answer. The full checklist is in `references/cost-causes.md`. In short: idle or forgotten resources left running, over provisioned capacity sized for a peak that never comes, data transfer and egress charges, storage that is never deleted and old snapshots, logging and metrics volume, and inefficient queries or calls that multiply a per unit charge.

Produce a diagnosis of what is driving the dominant line, with evidence from the breakdown.

### Step 4, measure the baseline

Before changing anything, record the current cost and the current unit cost using a method you can repeat: the same window, the same metric, the same query. Note the reliability posture too, such as how many replicas and how much headroom, so a later comparison shows whether you traded it away.

Produce a written baseline: total, unit cost, and reliability posture, with the exact method used to get each number.

### Step 5, cut with a reliability check

Apply the change to the dominant line. For every cut, state what reliability it costs: does it remove redundancy, shrink headroom, lengthen recovery, or reduce a backup? A cut with no reliability cost is safe to make; a cut with one needs explicit acceptance. The trade offs are catalogued in `references/reliability-tradeoffs.md`.

Produce the change plus a one line reliability statement for it, accepted before it ships.

### Step 6, remeasure and compare

After the change has run long enough to be representative, measure again with the identical method from the baseline. Compare total and unit cost, and confirm the reliability posture is what you intended. A saving that only appears under a different measurement is not real.

Produce a before and after comparison using the same method, and the confirmed reliability posture.

### Step 7, decide on commitments last

Only after the waste is gone should you consider reserved capacity or a savings plan, and only on the steady baseline that remains. Committing to a level before you have cut the waste locks in the waste. Note the lock-in: the term, whether it is refundable, and what happens if usage drops.

Produce a commitment recommendation, if any, with its term and its lock-in stated plainly.

## Self-audit

- Is the bill attributed by service and by team, with an owner for each significant line?
- Is the work focused on the top one or two lines rather than the small ones?
- Is total cost reported separately from unit cost per request or per customer?
- Was a baseline recorded before any change, with the exact method?
- Does every cut carry a stated reliability cost that was accepted?
- Was the after measurement taken with the identical method as the baseline?
- Are commitment discounts considered only after the waste was removed, with lock-in stated?
- Was any line that is a rounding error left alone rather than optimised?

## Honest limits

This skill reduces spend on things that already run; it does not decide whether a slow system needs more resources or better code. When the cost comes from an inefficient hot path, the fix is in `performance-tuning`, and a slower cheaper instance that breaks a latency target is a false saving. Whether the product's unit economics work at all is a business question owned by `business-model`.

The cause ordering and the thresholds here are rules of thumb drawn from what tends to dominate cloud bills, not a guarantee about any specific account. Commitment discounts and contract terms vary by provider and change often, so confirm current terms with the provider rather than trusting a remembered figure. This skill does not give tax or accounting advice.

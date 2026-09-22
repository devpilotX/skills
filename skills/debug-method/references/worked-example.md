# Worked example

A single bug taken from report to confirmed cause, so the method is visible in one place rather than
described in the abstract. The stack and the framework are generic; the moves transfer.

## The report

A user reports that some orders show a total of zero after checkout. It does not happen every time. It
started roughly a week ago. It affects a handful of users, not everyone.

## Step one, get the facts straight

What happens: the order total is stored as zero. What was expected: the sum of the line items. When it last
worked: the user thinks about a week ago. Who: a few users, not all. What changed a week ago: a deploy that
added a discount feature.

The first valuable pair of facts is now in hand. A good version exists before the discount deploy, and a
bad version exists after it. That turns the question into a search.

## Step two, reproduce

Place an order the normal way. Total is correct. The bug does not reproduce on the first try, which matches
the report that it is intermittent. Rather than retry blindly, look at what the affected orders share.

Query the affected orders. Every one of them used a discount code. Orders without a discount are always
correct. The reproduction shrinks: apply a discount code, and the total sometimes reads zero.

Try it with a discount. First attempt, correct. Second attempt, correct. Third attempt, zero. So there is a
second variable beyond the discount. Record the rate: roughly one in three with a discount applied.

## Step three, bisect the space

The intermittency with a shared input points at ordering or concurrency, not at a single bad branch. Add
temporary logging at the point where the total is written, printing the line item sum and the discount
value just before the write.

```
log.info("total_write items_sum=%s discount=%s result=%s",
         items_sum, discount, computed_total)
```

The log shows that on the failing runs, `discount` is larger than `items_sum`, and the total is being
clamped to zero. On the passing runs, `discount` is the expected small value. So the discount value itself
is wrong on the failing runs, not the subtraction.

## Step four, form and test one hypothesis

Hypothesis: the discount amount is read from a field that a second request overwrites, so under two
near simultaneous requests one order reads the other order's discount.

Prediction: if this is true, firing two discounted checkouts at the same instant will show one order taking
the other's discount, and serialising the two requests will make the bug vanish.

Run two checkouts concurrently. One order takes a discount meant for the other, larger than its own items
sum, and clamps to zero. Run them one after another. Both correct, ten times in a row. The prediction held.

## Step five, confirm the cause

The discount is stored on a request scoped object that is actually shared across requests because it was
attached to a module level singleton during the deploy. Two overlapping checkouts read and write the same
field. This explains every symptom: only discounted orders, only sometimes, only since the deploy, only a
few users because concurrency is rare at low traffic.

The bug can be switched on and off: run concurrent discounted checkouts to produce it, serialise them to
stop it. That is the strongest evidence available.

## Step six, fix it properly

Write the failing test first: two concurrent discounted checkouts, assert each order keeps its own
discount. Watch it fail. Move the discount off the singleton and onto the request, so each request owns its
value. Watch the test pass. Remove the temporary logging added in step three.

Then ask where else the pattern exists. Search for other fields attached to the same singleton during the
deploy. Two more were found and moved the same way, because one instance of a shared state bug usually
means several.

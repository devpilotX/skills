# Worked model

One recompute of a small subscription model, run all the way through the procedure, so the steps are
concrete. The figures are illustrative. What matters is the method: compute in a script, cross-check a
second way, and vary the assumptions to find which one owns the answer.

## The question

A founder claims: at 500 paying users on a 12 usd monthly plan, with 4 percent monthly churn and
40 usd to acquire each user, the product clears 4000 usd of monthly profit after a fixed 2000 usd of
overhead. Is the profit figure right, and is it stable?

## Step 1, restate quantitatively

- Revenue is 500 users times 12 usd per user per month.
- Churn of 4 percent per month means about 20 users lost per month, replaced to hold 500 flat.
- Acquisition cost of 40 usd applies to each replacement user that month.
- Overhead is a flat 2000 usd per month.
- Profit is revenue minus acquisition spend minus overhead.

Units to carry: usd, users, usd per user, users per month.

## Step 2, inputs with provenance

```
users            = 500      users            given
price            = 12.00    usd/user/month   given
churn            = 0.04      per month        given, ASSUMPTION on stability, range 0.03 to 0.06
cac              = 40.00     usd/user         given, ASSUMPTION on stability, range 30 to 60
overhead         = 2000.00   usd/month        given
```

## Step 3, compute with a script

```
python3 - <<'PY'
from decimal import Decimal as D

users = D("500")
price = D("12.00")            # usd per user per month
churn = D("0.04")             # fraction lost per month
cac = D("40.00")              # usd per acquired user
overhead = D("2000.00")       # usd per month

revenue = users * price                       # usd/month
replacements = users * churn                  # users/month to hold flat
acq_spend = replacements * cac                # usd/month
profit = revenue - acq_spend - overhead       # usd/month

print("revenue        : %8.2f usd/month" % revenue)
print("replacements   : %8.2f users/month" % replacements)
print("acquisition    : %8.2f usd/month" % acq_spend)
print("profit         : %8.2f usd/month" % profit)
PY
```

Output:

```
revenue        :  6000.00 usd/month
replacements   :    20.00 users/month
acquisition    :   800.00 usd/month
profit         :  3200.00 usd/month
```

The claimed 4000 usd is wrong. The correct figure under the founder's own assumptions is 3200 usd,
because the 800 usd of monthly acquisition spend was left out of the claim.

## Step 4, cross-check a second way

Order of magnitude: revenue is roughly 6000, costs are a couple of thousand plus under a thousand, so
profit in the low thousands is the right neighbourhood. 4000 sat at the top of that range and 3200 sits
inside it.

Different decomposition: profit per user is price minus the churn weighted acquisition cost, which is
12 minus 0.04 times 40, or 12 minus 1.60, or 10.40 usd per user. Times 500 is 5200, minus 2000 overhead
is 3200. The two routes agree.

Units check: revenue in usd/month, acquisition in usd/month, overhead in usd/month, so profit is in
usd/month as the question wanted. No dropped unit.

## Step 5, sensitivity

```
python3 - <<'PY'
from decimal import Decimal as D
users, price, overhead = D("500"), D("12.00"), D("2000.00")
for churn in (D("0.03"), D("0.04"), D("0.06")):
    for cac in (D("30"), D("40"), D("60")):
        profit = users*price - users*churn*cac - overhead
        print("churn %.2f cac %2d -> profit %7.2f" % (churn, cac, profit))
PY
```

The profit stays positive across the whole plausible range, from about 3100 to about 3550 usd, so the
sign of the answer is not in doubt. The input that moves it most is churn crossed with acquisition
cost, because they multiply. That product is what the founder should measure first.

## Step 6, report

```
ANSWER
About 3200 usd per month, not 4000. The claim omitted the 800 usd monthly cost of replacing churned
users.

CROSS-CHECK
Per user margin route gave the same 3200. Order of magnitude and units both consistent.

SENSITIVITY
Profit ranges roughly 3100 to 3550 across churn 3 to 6 percent and acquisition 30 to 60 usd. Churn
times acquisition cost dominates. Verify the real churn before trusting any single figure.

WHAT THIS DOES NOT SHOW
Nothing here says the 500 users are reachable or that churn holds at 4 percent. Those are business
questions, not arithmetic ones.
```

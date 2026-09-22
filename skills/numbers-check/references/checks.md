# Quantitative traps

The errors that appear most often in business, engineering, and reported statistics.

## Percentages

Percentage against percentage point. Moving from 4 percent to 6 percent is two percentage points and a
fifty percent increase. Reporting one as the other is the most common numerical misstatement in
business writing.

Percentage of which base. A 20 percent discount followed by a 20 percent increase does not return to
the original. Order matters, and the base changes.

Percentages that cannot be averaged. A 50 percent conversion rate on 10 visitors and 10 percent on 1000
is not a 30 percent average. Weight by the denominator.

Growth compounding. Ten percent a month is not 120 percent a year, it is about 214 percent. Check
whether a rate is simple or compound before using it.

Percentages above 100, which are fine for growth and impossible for a share of a whole. A share above
100 means double counting.

Change from a small base, where a large percentage means very little. Two to four customers is a
hundred percent increase and two customers.

## Averages and distributions

The mean on a skewed distribution misleads. Income, revenue per customer, response time, and file size
are all skewed, and the median is usually the honest summary.

A high percentile matters more than a mean for anything a user experiences. Average latency hides the
slow requests that cause complaints. Report the 95th or 99th percentile.

Simpson's paradox. A trend present in every subgroup can reverse when the groups are pooled. Check
subgroups before believing an aggregate.

Averaging over the wrong unit. Average revenue per user depends heavily on whether the denominator is
signups, active users, or paying users. State which.

Survivorship. Averaging the customers who stayed excludes the ones who left, which is usually the
number that matters.

## Rates and ratios

The denominator has to be the population at risk. A churn rate needs the customers who could have
churned, not total ever.

Rates over different periods cannot be compared without converting, and converting a monthly rate to
annual is not multiplication by twelve for anything compounding.

Ratios of small numbers are unstable. A change from 1 to 2 in the numerator moves the ratio wildly and
means almost nothing.

Per capita and per unit figures need the same time window on both sides.

Cohort against snapshot. A snapshot retention figure mixes cohorts of different ages and usually flatters
the number. Cohort it.

## Statistical claims

Significance is not size. A p value says something about the chance of the observed data under a null
hypothesis, not how large or important the effect is. Report the effect size and a confidence interval.

Sample size determines what can be concluded. Ask for it every time. A result with no stated sample size
is not a result.

Multiple comparisons. Testing twenty things at the conventional threshold produces about one false
positive by chance. Ask how many comparisons were made.

Selection. Who was excluded, who did not respond, and who never got asked. Nonresponse is rarely random.

Regression to the mean, which makes any intervention applied to extreme cases look effective.

Correlation without causation, and the specific version worth naming: a third factor causing both. Never
convert a correlational finding into a recommendation without saying it is correlational.

Base rates. A test with 99 percent accuracy for a condition affecting one in ten thousand people
produces far more false positives than true ones. Work the actual numbers rather than trusting the
accuracy figure.

## Money

Use decimal arithmetic, not binary floating point. Financial arithmetic in floating point accumulates
error that becomes visible in totals and reconciliations.

Nominal against real. Comparing figures across years without adjusting for inflation is comparing
different units.

Currency conversion needs a date, since the rate moved.

Gross against net, and which costs are inside which. Most margin disputes are definition disputes.

Cash against accrual. A profitable month with no cash is normal and it is also how businesses fail.
Model the timing, not just the totals.

Value added tax and sales tax are not revenue. Excluding them from the top line changes margin
materially.

Annual recurring revenue computed from one good month is an extrapolation, so label it as one.

Sunk cost has no place in a forward looking calculation, however much was spent.

## Estimation

When an exact figure is unavailable, estimate deliberately rather than guessing. Decompose into
quantities that can be bounded, estimate each with a range, and multiply the ranges to get a range.

State the answer as a range, never as a false point estimate.

Check against a known anchor. If the estimate implies more customers than exist in the country, it is
wrong.

Say which input the estimate is most sensitive to, because that is what to verify first.

## Reading someone else's model

Find the circular reference, meaning an output that feeds one of its own inputs.

Find the hardcoded number with no source, which is where the desired conclusion usually got inserted.

Check that the growth assumption is not the whole result. A model where revenue depends mostly on an
assumed growth rate is a statement about the assumption, not about the business.

Check the terminal period, since a large share of the total often sits in whatever happens after the
explicit forecast.

Test what happens when the best case input becomes the base case input, which is the substitution people
make without noticing.

Run every input to zero once. Models often fail to behave sensibly at zero, which reveals a structural
error.

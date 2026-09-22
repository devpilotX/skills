# Ways a data answer goes wrong

Named failure modes, each with the tell that catches it and the fix. Read this before concluding, not
after someone disputes the conclusion.

## Comparison failures

Non-comparable groups. A before and after that also crosses a price change, a marketing push, or an
instrumentation change. The tell: you cannot name what is held constant. The fix: find a comparison
where only the studied thing differs, or state that no clean comparison exists.

Missing baseline. A number reported alone, such as "conversion was 3 percent", with nothing to compare
it to. The tell: no answer to "compared to what". The fix: add the prior period, a control, or a
benchmark before reporting.

Selection into the groups. The treated group chose to be treated, so it differs from the control in
ways beyond the treatment. The tell: assignment was not random or controlled. The fix: name the
selection and treat the result as correlational.

## Aggregation failures

Simpson's paradox. The pooled trend reverses inside every subgroup because the subgroups have different
sizes and base rates. The tell: an aggregate that surprises you. The fix: segment before trusting the
total, and report the subgroup view when it disagrees.

Averaging percentages. A mean of rates that ignores the different denominators behind each rate. The
tell: you averaged a column of percentages. The fix: sum the numerators and denominators separately,
then divide.

Mean on a skewed distribution. Revenue, latency, and session length are skewed, and the mean sits above
most of the data. The tell: mean far from median. The fix: report the median and a high percentile.

Mixing cohorts. A snapshot metric that blends users of every age flatters retention, because old users
who churned already left the denominator. The tell: a retention or engagement number with no cohort.
The fix: cohort by join date and compare like ages.

## Population failures

Survivorship. Analysing only what survived: customers who stayed, sessions that completed, files that
parsed, funds that still exist. The tell: the failures are not in the dataset. The fix: find the
dropped cases or state that the answer only covers survivors.

Silent row loss. A filter, an inner join, or a dropna that removed rows nobody counted. The tell: the
row count changed and you did not predict it. The fix: count before and after every filter and join.

Incomplete recent period. The latest day or week looks like a decline that is only data still arriving.
The tell: a drop at the right edge of a time series. The fix: exclude or mark the incomplete tail.

## Inference failures

Correlation read as causation. A relationship in observational data turned into "X drives Y". The tell:
a recommendation to change X to move Y, with no experiment behind it. The fix: name the plausible third
cause and label the finding correlational.

Regression to the mean. An intervention applied to the worst performers looks effective because extreme
values drift back toward average on their own. The tell: the treated group was selected for being
extreme. The fix: compare against a control selected the same way.

Multiple comparisons. Slicing the data twenty ways and reporting the one slice that looks significant.
Testing twenty things at the 5 percent threshold yields about one false positive by chance. The tell:
many cuts tried, one reported. The fix: state how many comparisons were made and treat a lone
significant slice with suspicion.

Noise read as signal. A gap within the margin of error read as a real difference. The tell: no interval
on the estimate. The fix: put a range on it. A rough 95 percent margin for a proportion from a sample
of size n is about 1 over the square root of n, so a rate from 400 observations is good to roughly plus
or minus 5 points. This is a rule of thumb, not an exact interval.

## Presentation failures

False precision. Reporting 34.7 percent from a sample of 50, where the honest figure is "around a
third". The tell: more digits than the sample supports. The fix: round to the precision the data earns.

Truncated axis. A chart whose y axis starts above zero to make a small change look large. The tell: the
visual impression exceeds the actual size. The fix: start the axis at zero or label the real magnitude.

Hidden denominator. A count presented without the base it came from, so the reader cannot judge whether
it is large. The tell: a raw count with no rate. The fix: give the denominator or the rate alongside.

Buried assumption. The conclusion depends on one choice, such as a definition or a window, that the
reader never sees. The tell: the answer would flip under a reasonable alternative. The fix: state the
load bearing assumption and what happens if it changes.

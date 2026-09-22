# Sizing an experiment

The arithmetic that decides whether a test is worth running, and how long it must run. Do this before
launch, because a test sized after the fact is a test you already biased.

## The four inputs

Baseline rate. The current value of the metric in the population you will test. Measure it, do not
guess it, because everything downstream scales with it.

Minimum detectable effect. The smallest change worth acting on, stated in absolute terms. A jump from
10 percent to 11 percent is an absolute effect of 1 point and a relative effect of 10 percent. The
sample size depends on the absolute figure, so be clear which you mean.

Significance level. The false positive rate you accept, conventionally 5 percent. It is the chance of
claiming an effect that is not there.

Power. The chance of detecting an effect that is really there, conventionally 80 percent. Lower power
means you often miss real effects and call them null.

## The rule of thumb for a proportion

For a two arm test of a proportion at 80 percent power and 5 percent significance, the sample per arm
is approximately:

```
n_per_arm = 16 * p * (1 - p) / (delta ** 2)
```

where p is the baseline rate and delta is the absolute minimum detectable effect. The 16 folds in the
z values for 80 percent power and 5 percent two sided significance. This is a rule of thumb, accurate
enough to plan with and not a substitute for a proper calculation when the decision is expensive.

Worked example. Baseline 10 percent, want to detect a 1 point absolute change:

```
n_per_arm = 16 * 0.10 * 0.90 / (0.01 ** 2)   # about 14,400 per arm
```

So roughly 28,800 users total. If the surface sees 5,000 users a week, that is about 6 weeks. If it
sees 500 a week, the test would run 58 weeks and is not worth running as designed.

## Reading the run length

Divide the total sample by weekly traffic through the exact surface. Round up to whole weeks so every
weekday appears equally in both arms.

If the run length lands above 4 to 8 weeks, the test is fragile: seasonality, product changes, and
tracking changes accumulate over a long run and contaminate it. Shorten it by accepting a larger
minimum detectable effect, sending more traffic to the test, or choosing a metric with a higher base
rate that sits earlier in the funnel.

## When the numbers say do not test

Traffic too thin. If the required sample needs more weeks than the change will stay relevant, the
experiment cannot answer in time. Decide on judgement and say it is judgement.

Effect too small to matter. If the minimum detectable effect you can afford to run is larger than any
plausible effect of the change, a null result is guaranteed and tells you nothing. Skip it.

Metric too rare. Testing on a conversion that happens to 0.5 percent of users needs enormous samples.
Move the metric earlier in the funnel where the base rate is higher, and test the downstream effect
separately or with a longer horizon.

Change too large to isolate. A redesign that alters ten things at once cannot attribute a result to any
one of them. Either test the whole redesign as one decision, accepting you learn only go or no go, or
sequence the changes into separate tests.

## Interaction and traffic splits

Running two experiments on the same users at once risks interaction, where the effect of one depends on
the other. Either keep their surfaces disjoint or run them in sequence. If you must overlap, randomise
independently and check for interaction in the read, and know that checking for interaction needs far
more sample than the main effects.

Uneven splits reduce power. A 90/10 split to limit exposure needs more total sample than a 50/50 split
to reach the same power, because the small arm is the bottleneck.

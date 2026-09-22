---
name: data-analysis
description: Get a defensible answer out of a dataset instead of a plausible one, in any language or tool: write the question and the decision it feeds before opening the file, check provenance, profile shape and duplicates, treat missing values as information, pick the comparison that answers the question with a baseline, separate a difference from a difference that matters, name confounders, and report a range. Use when someone hands you a spreadsheet or export and asks what it says, when a chart needs to drive a decision, when a metric moved and nobody knows why, or when a claim about the data needs checking. Triggers on analyse this data, what does this dataset show, is this trend real, why did this metric change, look at these numbers, dig into this csv, find the drivers, segment this, is this significant, clean this data, explore this export, what is going on with these numbers.
license: MIT
compatibility: Any dataset in any format, any language. Examples use Python with pandas, and the method holds in R, SQL, a spreadsheet, or a notebook.
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Data analysis

Hand a model a dataset and a vague question and it will produce a chart and a confident sentence within
seconds, and the sentence will often be wrong. It compares two groups that were never comparable, reads
a gap of noise as a finding, treats missing rows as if they were empty, and never checks whether the
data could support the claim at all. This skill slows that first pass down until the answer is one a
sceptic cannot knock over in a sentence.

## Fit to the project

Read the data and its context before computing anything on it.

1. Find where the data came from. Look for a schema file, a data dictionary, an export script, an ETL
   job, or a README beside the file. The collection method decides what the data can answer, so read
   it before the rows.
2. Detect the format and scale. Check the file size, the row count, the column count, and the types
   before loading the whole thing. A file too large for memory changes the tool, not the method.
3. Find the grain. One row is one what: one event, one user, one user-day, one order line. Every later
   step depends on knowing this, and getting it wrong is the most common source of a wrong total.
4. Look for an existing definition of the metric in question. A dashboard, a past report, or a metrics
   layer often already defines active user or revenue, and a fresh definition that disagrees with the
   established one produces an argument, not an answer.

## Non-negotiables

1. Write the question and the decision it feeds before opening the file. A question without a decision
   attached has no natural stopping point, and analysis without a stopping point becomes a fishing trip
   that finds a false positive.
2. Never state a comparison without naming its baseline and confirming the two sides were comparable.
   A before and after that spans a pricing change, a seasonal peak, or a tracking change is comparing
   two different worlds and the number is meaningless.
3. Report uncertainty as a range, not a point. A single number implies a precision the data does not
   have, and a reader who sees one number will act as if it were exact.
4. Treat missing values as information about how the data was made, not as a gap to fill quietly.
   Silently dropping or imputing rows changes the population and can flip the result without anyone
   seeing it happen.
5. Never convert a correlation into a recommendation without stating it is correlational and naming the
   confounders you could not rule out. The recommendation is where a hedge quietly disappears.
6. Every figure in the output is reproduced by code that is shown, following `code-craft` for the
   script. A number typed into prose by hand is unverifiable and often wrong.

## Procedure

### Step 1, write the question and the decision

State in two lines what is being asked and what someone will do differently depending on the answer.
Name the population, the metric, the time window, and the unit. If two readings of the question give
different answers, write both and answer both rather than guessing which was meant.

### Step 2, check provenance and collection

Write down where the data came from, how it was collected, what was included, and what was excluded.
Instrumented events, a survey, a manual export, and a third party feed each carry different biases.
Note the point when tracking or definitions changed, because that point breaks any comparison across
it. If provenance is unknown, say so and treat every later conclusion as provisional.

### Step 3, profile before analysing

Load the data and describe its shape before asking it anything. Report the row count, the column types,
the range of each numeric column, the cardinality of each key, and the duplicate count on the grain.

```
import pandas as pd

df = pd.read_csv("export.csv")
print("rows:", len(df))
print(df.dtypes)
print("duplicate rows on grain:", df.duplicated(subset=["user_id", "event_day"]).sum())
print(df.describe(include="all").transpose())
```

A duplicate on the grain doubles a count. A column typed as text when it should be a date breaks every
comparison silently. Find these before they reach the answer. The full list to run and read is in
`references/profiling-checklist.md`.

### Step 4, treat missingness as data

Count the missing values per column and, more important, ask why they are missing. A null revenue for a
free user means zero. A null revenue for a paying user means a broken pipeline. These need opposite
handling. Report the missing rate per column and state the rule you applied to each, then check whether
the rule changes the result by running the analysis with and without the affected rows.

```
missing = df.isna().mean().sort_values(ascending=False)
print((missing[missing > 0] * 100).round(1).astype(str) + "%")
```

### Step 5, build the comparison with a baseline

Decide what the metric is compared against: a prior period, a control group, a benchmark, or a
theoretical expectation. Confirm the two sides differ only in the thing under study. A rule of thumb:
if you cannot name what is held constant between the two sides, you do not yet have a comparison.
Segment the aggregate before trusting it, because a trend in the pooled data can reverse inside every
subgroup. That reversal is Simpson's paradox, and it is common in funnel and cohort data.

### Step 6, separate a difference from one that matters

A difference has two questions. Could it be noise, and is it large enough to act on. For the first, put
a range on it rather than a p value alone: a proportion from a sample of size n has a rough 95 percent
margin of about 1 divided by the square root of n, which is a rule of thumb that says a rate from 100
observations is good to roughly plus or minus 10 points. For the second, state the effect in the unit
of the decision, in dollars or users or minutes, and ask whether that size would change what anyone
does. A statistically clear result that is too small to act on is a null result for the decision.

### Step 7, name confounders and survivorship

List the alternative explanations before concluding. A third factor driving both sides is the usual
one. Survivorship is the other: analysing only the customers who stayed, the sessions that completed,
or the files that parsed excludes exactly the cases that carry the answer. For each alternative, say
whether the data can rule it out or not. The ones it cannot rule out are limits on the conclusion, and
they belong in the report. The named failure modes, each with its tell and its fix, are in
`references/failure-modes.md`.

### Step 8, present so a reader sees what would change it

Report the answer as a range, then the comparison and its baseline, then the assumptions and the one
that matters most. State plainly what would flip the conclusion: a different definition, a wider window,
a subgroup broken out, a confounder measured. A reader who can see the load bearing assumption can
argue with the analysis, and an analysis that cannot be argued with is one that hides its weak point.

## Self-audit

- The written question names a population, a metric, a window, a unit, and the decision it feeds.
- Provenance and collection method are recorded, including any point where tracking or definitions
  changed.
- The grain is stated and the duplicate count on that grain is reported.
- Missing values are counted per column, a handling rule is stated for each, and the result was checked
  with and without the affected rows.
- Every comparison names its baseline and what is held constant between the two sides.
- The result carries a range, and the effect is stated in the unit of the decision.
- Confounders and survivorship are listed, each marked as ruled out or not.
- Every number in the output is produced by a script that is shown.

## Honest limits

This skill gets a defensible descriptive answer out of data on hand. It does not design the collection
that produces clean data, and it does not run controlled experiments: a comparison you set up in
advance with a control group belongs to `growth-experiment`. Deep statistical verification of a single
figure, a proof, or a financial model belongs to `numbers-check`. Building a predictive model on the
data belongs to `ml-build`. Where the data cannot answer the question, the honest output is that it
cannot, and no amount of analysis converts absent evidence into a conclusion.

The margin rule of thumb here is an approximation for a proportion and does not replace a proper
interval for small samples, rates, or skewed distributions. When the decision is expensive, compute the
exact interval rather than trusting the shortcut.

## Off switch

If the user says "stop", "just execute", or "skip the analysis", stand down and do the direct task
without the full protocol. That decision holds for the session unless the user asks for the method
again.

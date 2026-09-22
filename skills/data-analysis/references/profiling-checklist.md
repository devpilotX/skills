# Profiling checklist

What to run and read on a new dataset before you ask it any question. The order matters: shape before
content, content before comparison.

## Shape

Row count and column count. A file with fewer rows than you expected usually means a filter ran during
export. A file with more usually means a join fanned out.

Column types as loaded, not as intended. A date read as text, a number read as text because of a stray
symbol, an integer id read as a float that loses precision past 2 to the 53. Fix types before anything
else, because every later step trusts them.

The grain, stated as one sentence: one row is one X. Then check it. If the grain is one order, the
order id is unique. If duplicates exist on the key that should be unique, find out why before you sum
anything.

## Content

Range of each numeric column. A minimum below zero on a count, a maximum far past anything plausible, a
price of zero, an age of 200. These are either errors or a category you did not know about.

Cardinality of each categorical column. A country column with 300 values has dirty data. A status
column with two values when you expected five means three states never appear in this slice.

Distribution shape, not just the mean. Skewed data hides its story in the mean. Look at the median and
a high percentile for anything a person experiences, such as latency or revenue per account.

Constant columns and near constant columns. A column with one value carries no information and often
signals a filter that already ran.

## Keys and joins

Before joining two tables, check the join key is unique on at least one side. A many to many join
multiplies rows and inflates every downstream sum without any error.

After a join, the row count should match your prediction. If it grew, the join fanned out. If it
shrank, the join dropped rows and you need to know which.

Check for orphan keys: rows on one side with no match on the other. These become nulls after a left
join and vanish after an inner join, and either way the population changed.

## Time

The window covered by the data, from the earliest to the latest timestamp. Confirm it matches the
window in the question.

Gaps in the time series. A missing day is often a pipeline outage, not zero activity, and treating it
as zero drags an average down.

The timezone. Aggregating events by day gives different totals depending on the zone used to cut the
day, and a UTC cut versus a local cut can move a daily number by a noticeable amount near the boundary.

A recency cutoff. The most recent period is often incomplete because data is still arriving, so the
last day or last week frequently looks like a drop that is only lag. Exclude the incomplete tail or
mark it.

## Duplicates and identity

Exact duplicate rows. Count them and decide whether they are real repeated events or an export artifact.

Duplicate identity with different attributes: the same user id with two email addresses, the same order
with two statuses. This means the grain is not what you thought, and picking one row per key silently
chooses a story.

## A profiling snippet

```
import pandas as pd

def profile(df, grain):
    print("rows:", len(df), "cols:", df.shape[1])
    print("duplicate rows:", df.duplicated().sum())
    print("duplicate on grain:", df.duplicated(subset=grain).sum())
    for col in df.columns:
        nunique = df[col].nunique(dropna=True)
        missing = df[col].isna().mean()
        print(col, "type:", df[col].dtype, "unique:", nunique,
              "missing: %.1f%%" % (missing * 100))
```

Read every line of the output. The point is not to run it and move on, it is to find the one number
that is not what you expected and chase it down before it reaches the answer.

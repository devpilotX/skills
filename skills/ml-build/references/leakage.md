# Hunting data leakage

Leakage is information in the training data that will not be available at prediction time. It produces a
score that looks excellent in development and collapses in production, and it is the most common reason a
model that passed evaluation fails in the field. Treat any surprisingly good result as leakage until you
have ruled it out.

## Why the good score is the warning

A model cannot beat the information in its inputs. When a score is far better than the problem should
allow, the usual explanation is that a feature is carrying the answer, directly or by proxy. So the
response to a jump in accuracy is investigation, not celebration. The question is always: what does this
feature know that it would not know at prediction time?

## The patterns, the check, and the fix

### Target leakage from the future

A feature is computed from information that only exists after the moment of prediction. A churn model
that includes "days since last login" measured after the churn date, or a fraud model that includes a
field set during the investigation, has seen the answer.

Check: for every feature, ask when its value becomes known and compare that to the prediction time. Any
feature settled after the event is suspect.

Fix: recompute each feature as of the prediction time, or drop it.

### Label derived features

A feature is a function of the label or of something that determines the label. An "account status" that
becomes "closed for fraud" is not a feature for a fraud model; it is the label wearing a disguise.

Check: trace the provenance of each feature back to how it was produced. If the label influenced it, it
leaks.

Fix: remove the feature and any downstream feature computed from it.

### Preprocessing fitted before the split

Scaling, imputation, encoding or feature selection fitted on the whole dataset passes statistics from the
test rows into the training rows. The mean used to standardise a column now includes the test set.

Check: confirm every fit happens inside the training fold only, then is applied to validation and test.

Fix: move all fitting inside a pipeline that is fit on train and only transforms test.

### Duplicate and near duplicate rows across the split

The same record, or a lightly edited copy, appears in both train and test. The model memorises it and the
test score rewards memorisation.

Check: deduplicate before splitting, including near duplicates by a similarity threshold on text or by
key fields on tabular data.

Fix: remove duplicates, and split so that copies land on the same side.

### Group membership spanning the split

Several rows share a hidden group, a customer, a document, a device, and some land in train while others
land in test. The model learns the group, not the pattern.

Check: identify the entity that generalisation is claimed over and confirm the split respects it.

Fix: split by the group, so every row of a group is on one side.

### Identifier correlated with the label

A row id, a filename pattern, or an ingestion order correlates with the label because the data was
collected in label order. The model reads the id and scores well.

Check: test whether an identifier alone predicts the label. If it does, the collection process leaked.

Fix: drop the identifier and, where possible, shuffle away the collection order.

### Temporal split violated

Random splitting on time series lets the model train on the future and test on the past. Real deployment
only ever sees the past.

Check: confirm training rows precede test rows in time.

Fix: split by a cutoff date, train before, test after.

## A short leakage audit to run every time

Ask when each feature's value becomes known, and drop anything settled after prediction time.

Trace every feature's provenance to the label, and drop label derived features.

Confirm all preprocessing is fitted inside the training fold only.

Deduplicate, including near duplicates, before splitting.

Split by the entity generalisation is claimed over, and by time when the data is temporal.

Test whether any identifier alone predicts the label.

When the audit finds nothing and the score is still suspiciously high, look at the failures individually;
the explanation is often a single leaking feature that the aggregate hides.

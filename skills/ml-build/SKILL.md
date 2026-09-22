---
name: ml-build
description: Build machine learning and language model features with an evaluation that can actually fail. Use when the user asks to build a model, a classifier, a recommendation system, a retrieval augmented generation pipeline, a chatbot, an agent, an embedding search, or asks how to evaluate or fine tune or prompt a model, asks why their model performs worse in production than in testing, or asks whether machine learning is the right approach at all. Builds the evaluation set and the baseline before the model, hunts data leakage as the default explanation for a good score, measures against a trivial baseline, and refuses to report a metric without the sample size and the failure cases. Triggers on build a model, train a classifier, RAG, retrieval augmented, embeddings, vector search, fine tune, LLM app, AI agent, evaluate my model, model accuracy, data leakage, prompt evaluation, recommendation system.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Machine learning build

Two questions decide whether this work succeeds, and both come before any modelling. How will you know
it works, and what does a stupid approach score?

## Fit to the project

Before proposing a model, find out what data exists and what has already been tried. A dataset with a
documented split and a recorded baseline needs a different first move than a blank slate.

Read the data itself first: the schema, the row count, the class balance, and how the label was
produced. The label's provenance is where leakage hides, so trace it before trusting any score. Look for
an existing train and test split and whether it was made by row, by entity, or by time, because a split
by row on grouped data has already inflated whatever number the project reports.

Check for prior work: notebooks, an experiment log, a metrics file, or a model registry entry. If a
baseline and a metric already exist, adopt them rather than inventing new ones that are not comparable.
Note the serving path too, meaning whether inference is batch or per request, since that decides the cost
question and the latency budget.

When nothing is set, meaning raw data with no split, no baseline and no chosen metric, stop at step 1
and define the task and the error costs before touching a model. Training and serving code this skill
writes follows the `code-craft` contract for file layout, function length and comments.

## Non-negotiables

1. Build the evaluation set before the model. An evaluation written after the fact gets shaped by what the model already does well, which is how a useless system passes.
2. Measure a trivial baseline first. Predicting the majority class, returning the most recent item, or a keyword match. If the model does not beat it by a margin worth the operational cost, the model is not the answer.
3. Treat a surprisingly good result as a leak until proven otherwise. Leakage is the most common cause of a score that does not survive production.
4. Never report a metric without the sample size, the split method, and a confidence interval or a variance estimate. A single accuracy number is not a result.
5. Look at the failures individually. Reading fifty wrong predictions teaches more than any aggregate, and it is the step most often skipped.
6. State what the system must never do, and test that separately from accuracy. An average that looks fine can contain a category of failure that ends the product.
7. First ask whether rules would do. A well understood problem with stable logic does not need a model, and rules are debuggable, cheap, and explainable to an auditor.

## Procedure

### Step 1, define the task and the cost of being wrong

Write down the input, the output, and who acts on it. If nobody acts differently based on the output, the
project has no purpose yet.

Then price the errors asymmetrically, because they almost never cost the same. A false negative on fraud
costs money, a false positive costs a blocked customer. That ratio decides the threshold and sometimes
the whole metric, so decide it before optimising anything.

Establish the acceptable failure rate from the business, not from what the model happens to reach.

### Step 2, evaluation first

Hold out a test set that reflects production, and do not look at it while developing. Use a validation
set for iteration.

Split by the unit that generalisation is claimed over. Splitting by row when the data has users, sessions
or documents leaks information across the boundary and inflates the score. Split by entity.

Split by time when the data is temporal, training on the past and testing on the future, because random
splitting lets the model see the future.

Include the hard cases and the rare classes deliberately. A test set drawn only at random may contain
almost none of what matters.

Choose the metric from the error costs. Accuracy is misleading on imbalanced data, where predicting the
majority class scores well and does nothing.

For generative output, write a rubric with examples of pass and fail before generating anything, and
measure against the rubric. Full method in `references/evaluation.md`.

### Step 3, hunt leakage

Assume it exists. The checks that find it most often:

A feature computed using information not available at prediction time. Anything derived from the label,
or from the future, or from a status that is set after the event.

Preprocessing fitted on the whole dataset before splitting, which passes statistics from test into train.

Duplicate or near duplicate rows split across train and test.

An identifier that correlates with the label, such as a sequential number or a filename pattern.

Group membership spanning the split, such as several records from the same customer on both sides.

The tell is a score noticeably better than the problem should allow. Investigate rather than celebrate.

The full leakage hunt, with each pattern, the check that finds it, and the fix, is in
`references/leakage.md`.

### Step 4, build up from the baseline

Simplest useful model first. Logistic regression, gradient boosted trees on tabular data, a small
pretrained model on text. Complexity gets added only when the simpler version is measurably
insufficient.

For language model features, the order that wastes least effort is prompt, then retrieval, then fine
tuning. Fine tuning first is the most common expensive mistake, because most failures are missing
context rather than missing capability.

Record every experiment with its configuration and its result. Unrecorded experiments get repeated.

### Step 5, retrieval pipelines

Retrieval quality sets the ceiling. When the answer is not in the retrieved context, no amount of prompt
work recovers it, so measure retrieval separately from generation.

Measure whether the correct passage appears in the top results at all. That number, not the final answer
quality, is where most pipelines fail.

Chunk on document structure rather than a fixed character count, and keep enough context in each chunk to
be interpretable alone. Include the section and document title in the chunk text.

Combine keyword and vector search. Pure vector search misses exact identifiers, product codes and rare
terms, which are often exactly what users search for.

Handle the no result case explicitly. The system must be able to say it does not know, and that behaviour
has to be tested.

Cite the source passage in the output, so answers are checkable.

Plan reindexing when documents change, before it is needed.

### Step 6, production behaviour

Monitor the input distribution, not only the output. Drift shows up in the inputs first.

Log the input, the output, the model version and the confidence for a sample of traffic, so a complaint
can be reproduced.

Keep a human path for low confidence cases where the cost of being wrong is high.

Version the model and the prompt together with the code, so a result can be traced to what produced it.

Recheck cost per request at the traffic of the heaviest users, since inference cost scales with usage in
a way training cost does not.

Set a schedule for re-evaluation. Models decay because the world moves, and nobody notices without a
recurring check.

## Self-audit

- Evaluation set built before the model and not looked at during development.
- Trivial baseline measured and reported next to the model.
- Split by the correct entity and by time where relevant.
- Leakage checks done and listed.
- Metric chosen from the asymmetric error costs.
- Sample size and variance reported with every number.
- Fifty failures read individually, with the patterns described.
- Unacceptable behaviours tested separately from accuracy.
- Retrieval measured separately from generation, where applicable.
- Cost per request computed at heavy usage.

## When to stay off

Not every request wants an evaluation suite built. A quick prompt tweak, a one off analysis, or a
question about which library to use does not need a held out test set and a baseline first. If the user
says "stop", "just execute", or "skip the evaluation setup", that is the off switch: answer what they
asked and leave the suite unbuilt. It stays off for the rest of the session unless they ask for the
rigour back. Insisting on the full method when someone wants a fast answer gets the skill ignored.

## Honest limits

This skill builds the evaluation, hunts leakage, and orders the modelling from a baseline up. It does not
serve the model or run the pipeline in production: the container, the environment and the rollback belong
to `infra-deploy`, and the metrics dashboards and drift alerts belong to `observability-setup`. When the
feature is a language model application rather than a trained model, the prompt, retrieval and agent
wiring are `llm-app-build` and `prompt-forge`.

The metrics this skill reports come from the held out set you build, so they are only as representative
as that set. A number here describes the sample, not the world, and the honest reporting rules in
`references/evaluation.md` say to state the sample size and the holes every time. Whether the cost per
request is affordable is a `cost-control` judgement, and whether the model does anything harmful in a
regulated setting is `compliance-map`, not this skill.

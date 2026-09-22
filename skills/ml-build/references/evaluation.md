# Evaluating generative output

Generative systems fail differently from classifiers. The output is open ended, so there is no single
correct answer to compare against, and that is used as an excuse to skip evaluation. It is not a valid
excuse.

## Build the set before the system

Collect twenty to fifty real inputs before writing a prompt. Real means from actual users or from the
documents the system will face, not invented examples, which are always easier than reality.

For each input, write what a good output contains and what disqualifies it. Not a model answer, since
there are many acceptable outputs, but the properties that decide.

Include these deliberately, because a random sample will miss them: the input where the answer is not
available, the ambiguous input, the adversarial input, the input in another language, the very long
input, and the input that looks like a previous case but differs in one detail.

Keep a frozen subset you never iterate against, or the prompt gets tuned to the test.

## Score with a rubric

Convert judgement into checkable items, because an overall quality rating is not reproducible between
runs or between people.

Factual correctness against the source, with any unsupported claim counted as a failure rather than a
deduction.

Completeness against the required elements listed for that input.

Format compliance, which is machine checkable and worth automating first.

Refusal behaviour, meaning it declines when it should and does not decline when it should not.

Safety, meaning the outputs the product must never produce.

Score each item as pass or fail. Partial credit hides regressions, because a drop from excellent to
adequate looks like noise.

## Automate what can be automated

Format, schema validity, required fields present, citation links resolving, length limits, and banned
content are all deterministic checks. Write them as a test that runs on every change.

This is the difference between an evaluation you run and one you intend to run.

## Using a model as a judge

Workable, with three conditions, and misleading without them.

Give the judge the rubric and the source material, not only the output. A judge without the source is
guessing about factual correctness.

Calibrate it against human scores on a sample of at least thirty items, and report the agreement rate. A
judge whose agreement with a person is unknown produces a number nobody should act on.

Watch for the known biases: preference for longer answers, preference for confident tone, preference for
its own family of outputs, and position bias when comparing two candidates. Randomise the order and
report it.

Never use the same prompt for generating and judging without a human check, since the errors correlate.

## Regression discipline

Run the full set on every prompt, model or retrieval change. A prompt change that fixes one case and
breaks four is common and invisible without this.

Record the score with the exact configuration, meaning model version, prompt version, retrieval settings
and temperature. A score with no configuration is not reproducible.

Watch the variance. Run the set more than once at non-zero temperature, since a single run conflates
improvement with sampling noise.

When a provider updates a model behind an unpinned identifier, your system changed without a commit. Pin
the version where possible, and re-run the set when you move.

## Reporting honestly

Give the sample size every time. A result on twelve examples is a direction, not a measurement.

Give the pass rate per category rather than only overall, because a good average often hides one broken
category.

List the failures with what went wrong, since that list is what the next change should be aimed at.

State what the set does not cover. Every evaluation set has holes, and naming them prevents the number
being read as a guarantee.

Never report an improvement that is smaller than the run to run variance.

## Ceiling checks for retrieval systems

Measure retrieval alone: for each question, does the correct passage appear in the results at all, and at
what position. This sets the maximum achievable answer quality.

When that number is low, work on chunking, indexing and query handling. Prompt work at that point cannot
help, and is the most common misdirected effort in these systems.

Test the case where the corpus does not contain the answer. The required behaviour is an explicit
statement that it is not known, and the failure mode is a fluent invention.

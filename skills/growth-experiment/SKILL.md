---
name: growth-experiment
description: Run experiments that end in a decision rather than a discussion, for any product or channel: write the hypothesis with its mechanism, fix the one metric and the guardrails before starting, compute the minimum detectable effect and the sample size and the run length up front, change one thing, set the stopping rule so nobody peeks their way to significance, handle novelty and seasonality and weekday cycles, and read a null result as a real answer. Use when someone wants to test a change, when a team argues about whether a feature worked, when an A/B test needs designing or reading, or when traffic is too thin for a test and nobody has said so. Triggers on run an ab test, design an experiment, is this result significant, how long should we run this, what sample size do we need, did this feature work, test this change, split test, the test is inconclusive, can we ship it yet, why is the metric noisy, our experiment ended.
license: MIT
compatibility: Any product, channel, or funnel. The arithmetic is tool independent and works with any analytics stack or a spreadsheet.
metadata:
  version: 1.0.0
  suite: skills
---

# Growth experiment

Asked to test a change, a team runs it for a week, looks at the dashboard, sees the treatment ahead,
and ships. Every part of that is a trap. The run length was picked by the calendar not the maths, the
peek at the dashboard inflated the false positive rate, the metric was chosen after seeing the data,
and the lead was inside the noise the whole time. This skill forces the decisions that make an
experiment answer a question before the experiment starts, so the result ends the argument instead of
starting a new one.

## Fit to the project

Read what the product can actually measure and support before designing anything.

1. Find the analytics and assignment setup. Look for an experiment framework, a feature flag system, or
   an events pipeline. The assignment unit it supports, user or session or account, decides the whole
   design.
2. Estimate the traffic through the exact surface being changed, not total traffic. A test on a page
   200 users reach a week is a different problem from a test on the signup flow.
3. Find the baseline rate of the metric you intend to move. The sample size needed depends entirely on
   it, and a guess at the baseline makes the whole plan a guess.
4. Check for prior experiments on the same surface. A past null result or a known novelty effect
   changes what this one should expect and how long it should run.

## Non-negotiables

1. Write the hypothesis with its mechanism before touching anything. "Moving the button up increases
   signups because it is visible before the fold" can be wrong in a testable way. "This will improve
   things" cannot, and an untestable hypothesis produces an uninterpretable result.
2. Fix the one primary metric and the guardrail metrics before the test starts, in writing. A metric
   chosen after seeing the data is not a finding, it is the multiple comparison trap wearing a result's
   clothes.
3. Compute the sample size and run length before starting, from the baseline rate and the minimum
   detectable effect. Starting without them means you will stop when the answer looks good, which is
   the single most common way a false positive ships.
4. Fix the stopping rule in advance and hold it. Peeking at a running test and stopping when it crosses
   significance inflates the false positive rate far above the nominal 5 percent, because every peek is
   another chance to cross the line by luck.
5. Change one thing. A test that changes the button, the copy, and the price at once cannot tell you
   which one moved the metric, so a win teaches you nothing you can reuse.
6. Report a null result as an answer, not a failure. "No effect larger than 2 percent" is a real
   finding that saves the next team from rebuilding the same thing.

## Procedure

### Step 1, write the hypothesis and the decision

State the change, the mechanism by which it should work, the metric it should move, and the direction.
Then state what happens on each outcome: ship on a win, revert on a loss, and what you do on a null.
An experiment whose null outcome has no plan was never a decision, it was a demonstration.

### Step 2, pick the metric and the guardrails

Name one primary metric that maps to the decision. Name the guardrail metrics that must not get worse:
usually revenue, retention, latency, error rate, and support load. A win on the primary metric that
wrecks a guardrail is a loss, and deciding that after the fact is where teams argue.

### Step 3, compute the sample size and run length

From the baseline rate and the minimum detectable effect, compute the sample size per arm before
starting. A rule of thumb for a proportion at 80 percent power and 5 percent significance: sample size
per arm is about 16 times p times (1 minus p) divided by the absolute effect squared, where p is the
baseline rate and the effect is the absolute change you want to detect. Then divide the required sample
by the weekly traffic to get the run length, and round up to whole weeks to cover the weekday cycle.

```
p = 0.10          # baseline conversion rate
mde = 0.01        # smallest absolute change worth detecting, here 10% relative
n_per_arm = 16 * p * (1 - p) / (mde ** 2)
print("per arm:", round(n_per_arm), "total:", round(2 * n_per_arm))
```

If the run length exceeds a month or two, the minimum detectable effect is too small for your traffic
and you need a bigger effect, more traffic, or a different method. The full sizing arithmetic and the
cases where the numbers say do not test are in `references/sizing.md`.

### Step 4, set the stopping rule and hold it

Fix the end condition before launch: a fixed sample size or a fixed number of whole weeks, decided in
Step 3. Do not stop early because the result looks good. If early stopping is a real requirement, use a
method built for it, such as a sequential test with an alpha spending function, and set its boundaries
in advance. Peeking without such a method and stopping on a good number is how a 5 percent test becomes
a 20 percent test.

### Step 5, run clean and watch for cycles

Run at least one full week so every weekday appears in both arms, because behaviour differs sharply by
day. Watch for a novelty effect in the first days, where regular users react to any change and the
effect fades. If the product has strong seasonality, avoid running across a holiday or a launch that
hits one arm differently. Keep assignment stable: a user who saw treatment sees treatment for the whole
test.

### Step 6, read the result honestly

At the planned end, compare the primary metric with a confidence interval, not a point estimate. If the
interval crosses zero, the result is null and you cannot claim an effect. Check every guardrail. If you
tested several variants or several metrics, correct for the multiple comparisons: a simple rule of
thumb is Bonferroni, which divides the 5 percent threshold by the number of comparisons, so five
variants each need to clear 1 percent. State the effect size in the unit of the decision, then decide
per Step 1. The named ways an experiment lies, each with its tell and fix, are in
`references/pitfalls.md`.

### Step 7, write up what it decided

Record the hypothesis, the design, the numbers, the result with its interval, and the decision taken.
A null result gets written up with the same care as a win, because its value is stopping the rebuild.
Note anything that would change the read: a novelty effect still fading, a guardrail near its limit, a
segment that behaved differently.

## Self-audit

- The hypothesis names a mechanism and could be wrong in a stated way.
- One primary metric and the guardrails were fixed in writing before launch.
- Sample size per arm and run length were computed from the baseline and the minimum detectable effect
  before starting.
- The stopping rule was fixed in advance and no early stop was taken outside a sequential method.
- Exactly one thing changed between the arms.
- The test ran at least one full week and novelty and seasonality were considered.
- The result is reported with a confidence interval, and multiple comparisons were corrected.
- A null result, if that is the outcome, is stated as an answer with the effect size it ruled out.

## Honest limits

This skill designs and reads controlled online experiments. It does not analyse observational data you
already have, where you cannot assign groups: that belongs to `data-analysis`. The deep statistics of a
tricky significance calculation, an unusual distribution, or a power analysis for a non-proportion
metric belong to `numbers-check`. The engineering of the flag system and the events pipeline belongs to
the product's own tooling and to `observability-setup`.

The sample size formula here is a rule of thumb for a two arm proportion test at 80 percent power and 5
percent significance. For ratio metrics, revenue per user, or unequal arms, compute power properly
rather than trusting the shortcut. When traffic will never reach the required sample in a reasonable
window, an experiment is the wrong tool, and a decision made on judgement stated as judgement beats a
test too underpowered to detect anything.

## Off switch

If the user says "stop", "just execute", or "just ship it", stand down and stop pushing the full
protocol. Nothing further is pushed for the session unless the user asks for the protocol. A skill
that keeps demanding a power calculation after being told to move gets uninstalled.

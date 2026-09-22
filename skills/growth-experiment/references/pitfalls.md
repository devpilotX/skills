# Ways an experiment lies

The failure modes that turn a test into a false conclusion, each with the tell and the fix.

## Peeking and early stopping

The trap. You watch the running test and stop the moment it crosses significance. Because you get a new
chance to cross the line at every check, the real false positive rate climbs far above 5 percent.
Checking daily for two weeks can push it past 20 percent.

The tell: the test ended when the number looked good rather than at a planned sample size.

The fix: fix the end point in advance and hold it. If you need to stop early, use a sequential method
with an alpha spending function set before launch, which budgets the false positive rate across the
peeks.

## Multiple comparisons

The trap. You test five variants, or one variant against ten metrics, and report the one that reached
significance. At the 5 percent threshold, testing twenty independent things yields about one false
positive by chance alone.

The tell: many things were tested and one is reported.

The fix: name the one primary metric before launch. For genuine multiple tests, apply a correction.
Bonferroni divides the threshold by the number of comparisons, so five variants each need to clear 1
percent. It is conservative and simple, which is the right trade for a growth decision.

## Novelty and primacy effects

The trap. Regular users react to any visible change, up or down, simply because it is new. The early
effect fades over one to two weeks. Reading the first days as the steady state ships a mirage.

The tell: a strong effect in the first days that shrinks as the test runs.

The fix: run long enough for the novelty to decay, and look at the effect among users who joined during
the test separately from existing users, since new users have no old version to react to.

## Weekday and seasonality cycles

The trap. Behaviour differs by day of week and by season. A test that runs Monday to Friday misses the
weekend pattern. A test across a holiday sees distorted traffic.

The tell: the run length is not a whole number of weeks, or it spans a known event.

The fix: run whole weeks. Avoid holidays and launches that hit one arm differently. If seasonality is
strong, block on it or extend the run to average over it.

## Assignment and tracking bugs

Sample ratio mismatch. If a 50/50 split arrives as 52/48, the randomisation or logging is broken and
the whole result is suspect. Check the split against the intended ratio first, before reading any
outcome. A large deviation from the expected ratio means stop and fix the plumbing.

Leakage between arms. A user who sees both variants, through a shared device or a reassignment on
login, contaminates both. Assignment must be stable per user for the whole test.

Dilution. Counting users who never reached the changed surface waters down a real effect toward zero.
Analyse the population that was actually exposed, defined the same way in both arms.

## Reading failures

Null read as failure. An interval that crosses zero means no detected effect, which is a real answer
that stops the next team rebuilding the same thing. Write it up as a finding, with the effect size it
ruled out.

Underpowered null. A null from a test that never had the sample to detect a meaningful effect says
nothing. Before believing a null, confirm the test could have detected the effect you cared about.

Ignored guardrails. A win on the primary metric that quietly worsened retention, latency, or support
load is a loss. Read every guardrail before declaring a win.

Segment mining after the fact. "It did not work overall, but it worked for mobile users in Canada" is
the multiple comparison trap again. A post hoc segment is a hypothesis for the next test, not a result
from this one.

## When the experiment was the wrong tool

Some decisions do not fit an experiment: a change to a tiny population, a one way door that cannot be
reverted, a brand or pricing move whose effect takes quarters to appear, or a market too small to reach
significance in any reasonable time. For these, gather what evidence you can, decide on judgement, and
state clearly that it was judgement and not a measured result. A confident number from an underpowered
test is worse than an honest guess.

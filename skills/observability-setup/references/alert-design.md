# Alert design

The main file's rule is that every alert names an action. This is how to write one that does, how to
tell a symptom alert from a cause alert, and how to set a threshold from data instead of from a round
number.

## The parts of an alert that gets acted on

An alert missing any of these becomes noise the first time it fires without a clear next move.

| Part | What it holds | Failure when omitted |
| --- | --- | --- |
| Name | What is wrong in user terms | Reader cannot triage from the title |
| Condition | Metric, comparison, threshold, duration | Fires on a single spike, or never |
| Severity | Page or ticket, nothing else | Everything pages, so nothing does |
| Owner | The team or rota that responds | Alert fires into a void |
| Runbook | Link to the steps to take | Responder starts from zero at 3am |
| Action | The first thing to do | The alert is information, not a call to act |

## Symptom alerts versus cause alerts

Alert on what a user feels. A user feels errors and slowness. A user does not feel high CPU, a full
disk that has not yet caused a failure, or a garbage collection pause that stayed under the latency
budget.

Symptom alerts, which page:

- error rate above the budget for a sustained window
- latency at the high percentile above the objective
- a business event rate dropping to zero when it should be steady
- a queue consumer that has stopped consuming

Cause alerts, which ticket at most, because they may be harmless and often self correct:

- CPU or memory above a threshold
- disk usage climbing
- connection pool near its limit
- a dependency returning elevated but non fatal warnings

The trap is alerting on causes because they are easy to measure. A cause alert that fires while users
are unaffected trains the team to ignore it, and the ignore habit carries over to the symptom alert
that mattered.

## Setting a threshold from data

Never open with a round number. Ten percent error rate and five hundred milliseconds are guesses
dressed as decisions.

1. Pull a week of the metric, including at least one busy period and one quiet period.
2. Read the normal high percentile. That is the floor of normal, not the average.
3. Set the alert threshold above the observed normal peak, far enough that routine variation does not
   trip it, close enough that a real regression does.
4. Add a duration so a single scrape does not fire it. A condition true for five minutes is a
   problem; a condition true for one scrape is jitter.
5. Watch it for a fortnight and move it if it fires without cause or misses a real event.

## Absence and rate of change

Two conditions a static threshold never catches.

Absence: a consumer that stops consuming, a cron that did not run, a heartbeat that went quiet. These
produce no error, so the signal is silence. Alert when the event count over a window is zero and should
not be.

Rate of change: a slow leak that never crosses a static line until it is too late. Memory that climbs
one percent an hour crosses no fixed threshold for two days. Alert on the slope, not the level.

## A worked alert

Checkout latency, expressed the way it should be stored:

    name: Checkout pay latency above objective
    condition: p99 of duration_ms on route /orders/:id/pay > 800 for 10m
    severity: page
    owner: payments-rota
    runbook: link to the checkout latency runbook
    action: check the payments-api dependency latency first, then the database
            connection pool saturation, then roll back the last checkout deploy

The threshold of 800 came from a week of data where the normal p99 sat near 300 and peaked near 550
under load. The action names the first three things to look at, in the order that has resolved this
alert before, so the responder does not start from a blank page.

## Monthly review

Every alert that fired in the month gets one question: did it require an action? If it fired and the
answer was no, the threshold is wrong or the alert should not exist. Fix or delete it. An alert that
cries wolf is worse than a missing alert, because it erodes trust in the ones that are real.

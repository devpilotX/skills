---
name: incident-response
description: Act when production is broken, in any stack. Stabilise before diagnosing, declare severity from user impact, assign the roles of commander and communicator even in a team of two, keep a communication cadence, rank mitigations by time to safety, capture evidence before it rotates away, hand over when tired, and run a blameless review where every action has an owner and a date. Use when a system is down, degraded, or throwing errors and someone has to respond now. Triggers on production is down, site is down, outage, everything is broken, users cannot log in, 500 errors everywhere, database is on fire, we are losing money, page just went off, incident, sev1, who is on call, rollback now, customers are complaining, service degraded.
license: MIT
compatibility: Any stack, any deployment, any team size. Assumes you can deploy or roll back by some means and reach a communication channel.
metadata:
  version: 1.0.0
  suite: skills
---

# Incident response

Under pressure the instinct is to find the root cause first, and that instinct extends the outage. Diagnosis is slow and uncertain while users are being hurt every minute, so the person who starts debugging before stabilising is choosing a longer outage in exchange for a more satisfying story afterward.

The other common failure is silence. The team goes heads down on the problem and nobody tells the users, the support desk, or the rest of the company what is happening, so a technical problem becomes a trust problem. This skill puts stabilisation and communication ahead of diagnosis, on purpose.

## Fit to the project

Read what the project already has for responding before you need it.

1. Find the deploy and rollback path. Look for a deploy script, a pipeline, a feature flag system, or a documented manual procedure. The fastest safe mitigation is usually a rollback, so know how to trigger one before the incident.
2. Detect where the signals live: the dashboards, the error aggregator, the log store, the status page, and the alert channel. During an incident is the wrong time to learn where the graphs are.
3. Find the escalation path and the communication channel the team already uses. Note who can reach the people with access you might need, such as the database owner or the cloud account holder.
4. Check whether a severity scale and a runbook already exist. Adopt the project's definitions if they do, rather than inventing a parallel scheme mid crisis.

## When to stay off

This skill is for real production impact. Do not run the full protocol for a failing test in CI, a broken local environment, a staging glitch with no users, or a single internal user hitting a known bug with a known workaround. Declaring an incident for a non incident burns the team's attention and dulls the response when a real one arrives.

The off switch is saying "stop", "just execute", or "this is not an incident". It stops there and
does not reclassify the event later in the session.

## Non-negotiables

1. Stabilise before you diagnose. Every minute spent finding the cause while the system is down is a minute of impact you could have stopped with a rollback or a flag. Restore service first; understand it second, and the review is where understanding happens.
2. Declare severity from user impact, not from which component broke. A crashed component that no user touches is not a high severity incident, and a slow checkout with no error logs is. Sizing by component under counts the incidents that hurt and over counts the ones that do not.
3. One person holds the commander role and one holds communication, even in a team of two. Without a named commander, two responders apply conflicting mitigations at the same time and make it worse. The commander decides; they do not also debug.
4. Keep the communication cadence even when there is nothing new. A status update at a fixed interval, even one that says no change, prevents the silence that makes users assume the worst and floods the support desk.
5. Capture volatile evidence before it rotates away. Logs age out, metrics roll up, and the failing instance gets replaced. If you fix first and investigate later without capturing, the review has nothing to work from and the incident repeats.
6. Every action item from the review has a named owner and a date. A review that ends in shared intentions changes nothing, and the same outage returns.

## Procedure

### Step 1, declare and size

State plainly that an incident is open and set its severity from user impact: how many users, which function, and whether money or data is at risk. Name a commander and a communicator immediately, even if that is two people or one person doing both explicitly.

Produce a one line declaration in the channel: what is affected, the severity, who is commanding, and the time it started.

### Step 2, stabilise

Reach for the fastest mitigation that restores safety, not the one that fixes the cause. In rough order of time to safety: roll back the last deploy, toggle off the offending feature flag, shed or rate limit the load, fail over to a healthy replica, or scale up the exhausted resource. Pick the one that is reversible and fast.

Produce a restored or degraded but usable service, and a note of exactly what you changed so it can be undone.

### Step 3, communicate on a cadence

Post the first external update within minutes: acknowledge the problem, state the impact in user terms, and give a time for the next update. Then hold that cadence. A status update contains what is affected, what you are doing, what users should do meanwhile, and when they will hear next. It does not contain speculation about the cause.

Produce a running log of updates at the stated interval until the incident closes.

### Step 4, diagnose without destabilising

Once service is safe, hand the diagnosis to the method in `debug-method`. Change one thing at a time, and never apply a debugging experiment to production that could deepen the outage. Capture the evidence listed in `references/evidence-capture.md` before it ages out: the error rate around the start time, the deploy that preceded it, the logs for a failing request, and the state of the scarce resource.

Produce a captured evidence bundle and a working hypothesis, kept separate from the mitigation already in place.

### Step 5, hand over when tired

An incident that runs past a couple of hours outlives clear judgement. When the commander is tired, hand the role over with a written brief: what is broken, what has been tried, what is currently mitigating it, and the open hypotheses. A fresh commander with a good brief beats an exhausted one with full context.

Produce a handover brief in the channel whenever the commander role changes.

### Step 6, close and review

Declare the incident closed only when the mitigation is holding and users are served. Then schedule a blameless review while memory is fresh. The severity and role definitions to reuse are in `references/severity-and-roles.md`.

Produce a closing statement and a scheduled review with the evidence bundle attached.

### Step 7, run the blameless review

Reconstruct the timeline from the evidence, not from memory. Ask what happened, why the system allowed it, why it took as long as it did to detect and to mitigate, and what would stop it or shorten it next time. Attribute nothing to a person's carelessness; a person who could cause the outage means the system permitted it.

Produce a written review with a timeline and a list of action items, each with a named owner and a date.

## Self-audit

- Was service stabilised before diagnosis began, or is the reason it could not be written down?
- Was severity set from user impact rather than from which component failed?
- Were a commander and a communicator named, distinct from whoever was debugging?
- Did external updates go out on a fixed cadence, including no change updates?
- Was volatile evidence captured before it rotated away?
- Was there a written handover every time the commander role changed?
- Does the review have a timeline built from evidence rather than memory?
- Does every action item have a named owner and a date?

## Honest limits

This skill runs the response; it does not find the root cause. The diagnosis itself belongs to `debug-method`, and the instrumentation that lets you answer questions during an incident belongs to `observability-setup`. If the dashboards and alerts are missing, fix that after the incident, because you cannot build them mid outage.

The severity thresholds and cadence intervals here are rules of thumb that suit a small to mid size team; a regulated environment or a large organisation has reporting duties and roles this skill does not cover. Preventing the next incident through better tests and safer releases belongs to `test-strategy` and `release-manage`.

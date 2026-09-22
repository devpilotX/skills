# Evidence capture

Most incident evidence is perishable. Logs age out of hot storage, high resolution metrics roll up into averages, and the failing instance gets recycled by the very autoscaler that is trying to heal the system. If you fix first and investigate later without capturing, the blameless review has nothing to reconstruct and the incident comes back.

Capture happens in parallel with stabilisation, not after it. Assign it to a responder while the commander runs the mitigation.

## Capture before you mitigate, if you can

Some evidence is destroyed by the fix itself. A rollback replaces the running code, and restarting a stuck process clears its memory and open connections. When a mitigation will erase state, grab that state first if it costs only seconds: a snapshot of the process, the current connection count, the contents of the stuck queue. If grabbing it would extend the outage, mitigate and accept the loss; safety wins over evidence.

## The bundle to collect

Aim for a bundle that lets someone who was asleep reconstruct the incident:

The error rate and latency for the affected service across a window that starts before the incident and runs to the present. Screenshot or export it, because the live dashboard will look different by the time of the review.

The change that preceded the start. The most common cause of a sudden failure is a recent deploy, a config change, a flag flip, or a dependency upgrade. Record the exact version or commit and its timestamp, and compare it to the incident start time.

The logs for a handful of failing requests, pulled by correlation identifier if the system has one. A few complete failing requests are worth more than a million lines of aggregate noise.

The state of whatever was scarce: connection pool usage, queue depth, memory, disk, CPU, rate limit counters. Saturation of a shared resource is behind a large share of incidents and it is the first thing that recovers once you mitigate, so it is easy to lose.

The external dependency status: was a provider you rely on also having an incident at the same time? Their status page at the incident time is evidence you cannot recover later.

## Timestamps in one timezone

Record everything in one timezone, and say which. An incident spanning several tools and several people produces timestamps in local time, in UTC, and in whatever the logs default to, and reconciling them afterward wastes an hour. Pick UTC or the team's standard and convert as you capture.

## Where to put it

Drop the bundle somewhere durable and linked from the incident channel: an attachment, a shared drive, a ticket. Evidence that lives only in one responder's terminal scrollback is gone when they close the window.

## What not to capture

Do not screenshot or paste anything containing secrets, full personal records, tokens, or payment details. If a failing request log contains a card number, redact it before it goes into the bundle. The review is read by more people than the incident, so treat the bundle as widely visible.

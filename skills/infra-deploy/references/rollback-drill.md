# Rollback drill

A rollback plan nobody has run is a hope with a runbook attached. The only way to know a rollback works
is to perform one on purpose, before an incident forces it. This file is the rehearsal: run it in
pre-production first, then in production during a quiet window, and write down how long it took.

## Why rehearse it

The first time you roll back should not be at three in the morning with users affected. Rollbacks fail in
ways that only surface under a real attempt: a migration that cannot run backwards, a config the old
version no longer understands, an artefact that was garbage collected, a cache full of the new format.
Finding these during a drill costs an hour. Finding them during an incident costs the outage plus the
rollback that will not complete.

## What a rollback must undo, and what it cannot

A rollback returns the running code to a previous known good version. It does not undo everything.

State is the boundary. Data written by the new version stays written. A rollback of code cannot recover a
row deleted by the new version, so destructive migrations and data changes need their own plan, separate
from the code rollback. This is why migrations decouple from the deploy: the schema must serve both the
old and the new code at once, so rolling the code back does not hit a schema it cannot read.

Anything the new version sent outward, an email, a webhook, a payment, is gone too. A rollback is not a
time machine for side effects.

## The drill steps

Confirm the previous artefact still exists and is retrievable by its tag or digest. If your registry
garbage collects old images, the rollback target may already be gone; fix that before anything else.

Take a fresh backup of state and verify it restores, because the point of the drill includes proving the
backup is real.

Deploy the current version to pre-production, then trigger the rollback to the previous version using the
exact mechanism production uses, not a shortcut.

Start a timer when you begin the rollback and stop it when the previous version is serving healthy
traffic. That number is the recovery time you can promise.

Watch the readiness checks flip and confirm traffic moves to the old version with no gap. A rollback that
leaves a window with nothing serving is not done.

Confirm the old version runs against the current schema. If it errors on a column the new version added,
your migration was not backward safe and the deploy strategy needs the expand and contract pattern.

Check the caches and queues. A message in the new format sitting in a queue the old version cannot parse
will fail after the rollback; drain or version those payloads.

## Failure modes to check during the drill

The rollback target artefact is missing from the registry.

The database migration has no safe reverse, so the old code meets a schema it cannot read.

A configuration value the new version added is now absent, and the old version had a default that
differs.

An in flight queue message is in a format the old version does not understand.

A cache holds new format entries the old version misreads; decide whether to flush on rollback.

A client bundle was already served to users and calls an endpoint the rolled back server removed.

## Recording the result

Write the measured rollback time where the team will find it during an incident, in the runbook, not in a
chat message.

Note which failure modes you checked and which you could not, so the gaps are visible rather than assumed
handled.

State the state boundary explicitly: what the rollback recovers and what it does not, so nobody expects
deleted data to return.

Re-run the drill after any change to the deploy mechanism, the migration strategy, or the artefact
retention policy, because each of those can quietly break the path you proved once.

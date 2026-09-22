# Severity and roles

The point of a severity scale is to decide how hard to respond without arguing about it during the incident. The point of named roles is to stop two people applying conflicting fixes at once. Both are set from user impact, never from which box is red.

## A severity scale by user impact

These levels are a rule of thumb. Adopt the project's own scale if it has one.

Sev1 means a core function is unusable for most users, or money or data is actively at risk. The whole team drops other work. Someone communicates externally within minutes.

Sev2 means a significant function is degraded or broken for a meaningful share of users, with a workaround or partial availability. It gets an owner and active work, but not everyone.

Sev3 means a minor or non urgent problem: a small subset of users, a cosmetic fault, or a fault with an easy workaround. It gets a ticket and a normal schedule.

The test for the boundary is not the component. A crashed background worker that no user notices is a Sev3 even though a process died. A checkout that is slow enough to lose sales is a Sev1 even though nothing is throwing errors.

## Roles

The commander owns the response. They decide which mitigation to apply, they hold the timeline, and they call when to escalate, hand over, and close. The commander does not debug. The moment the commander is also head down in logs, nobody is watching the whole picture.

The communicator owns everyone outside the response: the status page, the support desk, the affected customers, and the rest of the company. They translate technical state into user terms and hold the cadence. This frees the commander from context switching between fixing and explaining.

The responders do the hands on work: the rollback, the query, the log search. They report findings to the commander and change one thing at a time.

In a team of two, one person is commander plus communicator and the other is the responder, and you say so out loud. The roles still exist; they are just held by fewer people. The failure to avoid is two people silently both being responders with no one commanding.

## Escalation

Escalate when the mitigation is not holding, when the incident crosses a severity boundary upward, or when it needs access or authority the current responders do not have. Escalation is not a failure; a late escalation is. Know before the incident who holds the database credentials, the cloud account, the DNS, and the payment provider relationship, because those are the people you will need and cannot reach quickly if you start looking mid crisis.

## The status update template

A useful external update has four parts and no speculation:

```
What is affected: checkout is failing for about half of users.
What we are doing: we have rolled back the last release and are monitoring.
What to do meanwhile: please retry in a few minutes; carts are saved.
Next update: within 30 minutes, or sooner if this changes.
```

State impact in what the user cannot do, not in which service is down. Users do not know or care what the inventory service is; they know they cannot buy.

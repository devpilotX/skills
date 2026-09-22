# Rollout shapes

The main file lists the shapes and says to pick by what a failure costs and how fast it shows. This is
each shape set against its cost, what it needs to work, when it is the wrong choice, and how to abort
from it. Use it as a decision aid, not a ranking; the right shape depends on the blast radius you can
tolerate.

## The shapes at a glance

| Shape | Blast radius on failure | Needs | Speed to abort |
| --- | --- | --- | --- |
| All at once | Everyone | Nothing extra | A rollback or a flag |
| Canary | The canary slice | Per version metrics | Route traffic back |
| Staged by cohort | The current cohort | Cohort routing, wait per stage | Hold and roll the last cohort back |
| Blue green | Everyone, but switchable | Two full environments | Switch traffic to the old environment |
| Dark launch | Nobody, results hidden | A way to run without exposing output | Stop running the shadow path |

## All at once

Every user gets the new version at the deploy. Simple, no extra machinery, and the blast radius is the
whole population.

Right choice when the change is low risk, the system is small, and a rollback or flag flip is fast.
Wrong choice for anything where a failure affects money, data, or a large audience, because there is no
smaller group to fail on first.

Abort by rolling back or flipping the flag. There is no partial state to unwind, which is the one thing
this shape has going for it under pressure.

## Canary

A small share of traffic goes to the new version while the rest stays on the old one. Limits exposure
to the size of the canary.

Right choice when you have per version metrics, because the whole point is to compare the canary
against the baseline. Wrong choice without those metrics: the main file is blunt that a canary without
separate metrics is just a slower deploy, since you cannot tell the two versions apart.

Set the canary share small enough that a failure is tolerable and large enough that the metrics have
signal. Watch error rate and the tail latency of the canary specifically, not the blended number.

Abort by routing the canary traffic back to the old version. Fast, because the old version never
stopped serving.

## Staged by cohort

Ship to internal users, then one percent, then ten, then everyone, with a wait at each stage and the
abort condition checked before moving on.

Right choice when different cohorts can be routed separately and a problem takes time to surface. Wrong
choice when the wait is set too short: the main file warns that for anything data related the wait is
hours rather than minutes, because the failure mode is a slow data problem, not an immediate error.

The wait per stage is the whole safety mechanism. If you move to the next cohort before the current one
has had time to reveal a problem, you have a slow all at once rollout with extra steps.

Abort by holding the rollout at the current stage and rolling the last cohort back. Cohorts already on
the new version stay unless they are affected.

## Blue green

Two full environments run in parallel. Traffic switches from the old to the new in one move, and back
just as fast.

Right choice when a fast switch back is worth the cost of running two environments. Wrong choice when
the two environments share state, particularly a database, because the shared state does not switch
with the traffic and can leave the old environment unable to serve after a switch back.

The shared state problem is the one that catches teams. Plan how the database is handled before
choosing this shape, or the fast switch back is an illusion.

Abort by switching traffic back to the old environment, subject to the shared state being compatible.

## Dark launch

The new path runs on real traffic but its results are not shown to anyone. The only way to test
performance at real volume before users depend on the path.

Right choice when you need production scale evidence that the new path holds up. Wrong choice as a
substitute for a real rollout, because nobody is actually using the results yet.

Abort by stopping the shadow path. Nothing user facing changes, because nothing user facing was ever
connected.

## Choosing

Ask two questions. What does a failure cost, and how quickly would it be visible? A cheap, immediately
visible failure tolerates all at once. An expensive failure that surfaces slowly wants a staged rollout
with long waits and per version metrics. A failure you cannot afford to expose at all wants a dark
launch first, then a staged rollout of the proven path.

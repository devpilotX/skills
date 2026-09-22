---
name: agent-orchestrate
description: Split work across several agents or sessions without losing the fact that mattered or paying more to coordinate than the work would have cost alone. Use when a task is large enough to divide, when delegating to sub-agents or parallel sessions, when a review-and-revise loop needs a stopping rule, or when a context budget is running out and work must be handed on. Decides when delegation pays, writes briefs that return usable results, sets loop and retry limits so cycles terminate, and reconciles partial or contradictory results. Triggers on split this work, delegate to sub-agents, run these in parallel, coordinate multiple agents, break this into tasks, my context is full, hand off part of this, orchestrate the work, fan out these tasks, review loop wont stop, agents disagree, too much to do in one session, parallelize this.
license: MIT
compatibility: Any project, any language, any model provider or agent framework. No specific orchestration tool required.
metadata:
  version: 1.0.0
  suite: skills
---

# Agent orchestrate

Delegation looks free and is not. A parent agent splits a task, writes four vague briefs, waits, and gets back four results it cannot use because none of them answered the question that was actually asked. Then a summary of a summary drops the one number the whole task depended on, and the parent reports a confident answer built on a fact nobody checked. This skill decides when splitting work pays, and structures it so the results come back usable.

## Fit to the project

Read what the task and the environment allow before fanning out.

1. Check whether the work actually divides. If every subtask needs the output of the one before it, there is nothing to parallelise, and delegation only adds coordination cost. Look for independent pieces before splitting.
2. Detect what the orchestration environment supports: whether sub-agents can run at all, whether they run in parallel or only in sequence, and what a child can return. A plan that assumes parallel execution on a serial runner stalls.
3. Read the context budget you have. Delegation trades your budget for coordination overhead, and past a point the overhead costs more than doing the work in one place. Estimate before committing.

## Non-negotiables

1. Delegate only when the subtask is separable and its result is verifiable by the parent. Delegating work you cannot check means trusting a result you cannot see was produced, which is how a wrong answer gets laundered into a confident one.
2. Every brief states the goal, the inputs, the exact shape of the expected result, and the done condition. A brief that omits the result shape gets back prose the parent has to re-do, so the delegation saved nothing.
3. Set a loop limit and a retry limit before starting any review-and-revise cycle. Without a hard stop, a reviewer and an author trade edits until the budget is gone. Two or three revision rounds is a common ceiling; name the number up front.
4. The parent verifies claims rather than trusting them. A child reporting success is a claim, not a fact. Check the artifact the child produced, not its summary of the artifact, before building on it.
5. Never summarise a summary without keeping a path back to the source. Each compression layer drops detail, and the detail that gets dropped is the one no layer thought was important. Carry the load-bearing facts forward verbatim.

## Procedure

### Step 1, decide whether to delegate at all

Estimate the cost of doing the work directly against the cost of writing a brief, waiting, and verifying the result. Delegation pays when the subtask is large, separable, and its result is cheap to check. It costs more than it saves when the task is small, when it needs constant back-and-forth, or when verifying the result is as much work as producing it. Write down the decision and the reason.

### Step 2, split by dependency, not by wish

Map which subtasks need the output of which others. Independent subtasks can run in parallel. Dependent subtasks run in sequence, and the dependency order is fixed by the data flow, not by preference. A subtask that reads another's output cannot start until that output exists, so putting them in parallel just produces a wrong answer faster.

### Step 3, write a brief that returns something usable

For each subtask, write the goal in one sentence, the inputs the child receives, the exact result shape expected, and the condition that means done. State what the child must not do when it would otherwise guess. A brief the parent could not act on if it came back is a brief that will come back unusable. The five parts and a worked example are in `references/brief-template.md`.

### Step 4, bound every loop

Before any review cycle, set the maximum rounds and the retry limit on a failing child. Decide what happens when the limit is hit: accept the best result so far, escalate to a human, or fall back to doing it directly. A cycle without a declared stopping rule does not terminate on its own.

### Step 5, verify before you build

When results come back, check each against its done condition by inspecting the artifact, not the child's description of it. A child that says the tests pass has made a claim; run the tests or read their output. Treat an unverifiable success the same as a failure.

### Step 6, reconcile partial and contradictory results

When children return conflicting answers, do not average them and do not pick the most confident. Find which one is checkable against the code or the data and use that. When results are partial, name the gap explicitly rather than papering over it. Carry the load-bearing facts forward in full so the next layer does not lose them. The named failures this step guards against are catalogued in `references/failure-modes.md`.

## Self-audit

- Was the decision to delegate written down with its cost reasoning, rather than assumed?
- Does every brief state the goal, inputs, result shape, and done condition?
- Was the split made by data dependency, so nothing parallel actually depended on another parallel task?
- Does every loop have a declared round limit and retry limit with a defined outcome at the limit?
- Did the parent verify each result against its artifact rather than the child's summary?
- When results conflicted, was the winner chosen by checkability rather than confidence?
- Were the load-bearing facts carried forward verbatim rather than compressed through a second summary?

## Honest limits

This skill decides how to divide and verify work; it does not persist the results across sessions, which is what `memory-keeper` owns. Writing the individual brief as a prompt that a model follows reliably is the job of `prompt-forge`. The cost estimates here are judgement calls, not measured figures, and they depend on the environment's per-call overhead, which varies by framework and provider.

The off switch: say "stop" or "just execute" and this skill stands down, so the work runs in one place without splitting or coordination. It will not keep proposing a fan-out after you decline.

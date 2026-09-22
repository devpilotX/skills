# Read protocol and compaction

How to rebuild context at session start cheaply, when to write, and how to compact a file that outgrew its budget. The numbers here are rules of thumb, not measurements; pick different ones if the project has a reason and write them down.

## Rebuilding context at session start

The goal is to spend the fewest tokens that let you act correctly. Reading every file in full on every session wastes budget and buries the one line that mattered.

1. Read `state.md` in full. It is short by design and tells you what the last session was doing.
2. Read `facts.md` in full. It is the ground the rest sits on.
3. Scan `decisions.md` upwards from the bottom of the file, where the newest block sits, and stop once the decisions stop being relevant to the current task. You rarely need the whole history at once.
4. Read `questions.md` in full so you do not re-answer something already parked.
5. Read the last 20 to 40 lines of `log.md`. Go further back only when the recent tail references something you do not recognise.

Stop when you can state, in one paragraph, what the work is and what the next step is. If you cannot, read more; if you can, start working.

## When to write

Write at these moments, because they are the ones whose context is expensive to reconstruct later:

At a decision. The choice, the reason, and what you rejected. The reason is the part that is impossible to recover months later.

Before a risky or hard-to-reverse step. Write the current state and the intended next step first, so an interrupted or failed step leaves a recoverable trail.

At a handoff. Before another agent, tool, or person takes over, write `state.md` so it reads without you present.

At session end. Update `state.md` to the new present and log what happened, even when the session was short.

Do not write on every small action. A log of trivia is as hard to read as no log, and it burns the budget faster.

## Handling a conflict between memory and code

Memory drifts because the code keeps moving after the note was written. When a fact or a decision disagrees with what the code now does, the code is correct and the memory is stale. Append a dated log entry describing the drift, then edit the fact or add a reversing decision. Never act on the stale memory because it sounds confident.

## Compaction rules of thumb

A file over budget gets shorter without losing its conclusions.

Keep every decision and its reason. These are the expensive part and they do not compact.

Keep facts that are still true. Drop facts that a newer fact already replaced.

In the log, collapse a run of routine entries into one dated summary line that keeps the outcome. A week of small refactors becomes one line naming the week and the net result.

Prefer summarising to deleting. A deleted detail is gone; a summarised detail keeps the conclusion a later reader needs.

After compacting, the file should read as a coherent shorter history, not as a file with holes. Record the compaction in the log with the date range you summarised.

## Handoff checklist

Before handing off, confirm `state.md` answers four questions without you: what is done, what is in progress, what the next concrete step is, and what is half-finished and must not be assumed complete. A handoff that fails any of these will cost the next agent a round trip to a human.

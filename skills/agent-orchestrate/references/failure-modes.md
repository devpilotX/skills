# Orchestration failure modes

Named failures that recur when work is split across agents or sessions, and what stops each one. These come from watching delegation go wrong, so treat them as patterns to watch for rather than measured frequencies.

## The lost fact

A child produces a detailed result. The parent summarises it. A grandparent summarises that. By the top, the one number the task depended on is gone, because no layer judged it important enough to keep. The answer that arrives is confident and wrong.

What stops it: carry load-bearing facts forward verbatim. A figure, an identifier, a specific error message, or a file path travels unchanged through every layer. Summarise the narrative around it, never the fact itself. When in doubt about whether a detail is load-bearing, keep it.

## The unverifiable success

A child reports that it finished and the tests pass. The parent believes it and builds on top. The tests never ran, or ran on the wrong target. The failure surfaces two layers later, far from its cause.

What stops it: the parent checks the artifact, not the report. Read the test output, open the file the child claims to have written, run the command the child claims succeeded. A success you cannot inspect is treated as a failure.

## The runaway loop

A reviewer finds issues, the author fixes them, the reviewer finds new issues in the fixes, and the cycle burns the entire budget without converging. Each round feels productive and the whole never terminates.

What stops it: a declared round limit set before the loop starts, commonly two or three, and a rule for what happens at the limit. On the last round the reviewer may only confirm the existing issues are resolved, not open new ones. When the limit is hit without convergence, escalate or accept the best result rather than continuing.

## The false parallel

Two subtasks run at once, but the second needed the first one's output. The second runs on stale or missing input and produces a result that looks complete and is built on nothing.

What stops it: map the data dependencies before splitting. A subtask that reads another's output is downstream of it and runs after it, whatever the schedule would prefer. Parallel is for genuinely independent work only.

## The contradiction average

Two children return different answers to the same question. The parent splits the difference or picks the more confident one. Both moves produce an answer that neither child would endorse and that matches no reality.

What stops it: resolve conflicts by checkability, not by confidence or averaging. Find which answer can be tested against the code or the data, test it, and use the one that holds. When neither can be checked, report the conflict rather than inventing a resolution.

## The delegation that cost more

A task was small enough to do directly, but got split anyway. Writing the briefs, waiting, and verifying the results took longer than the work would have. The coordination overhead swallowed the gain.

What stops it: estimate the coordination cost before delegating. Small, tightly coupled, or hard-to-verify tasks stay in one place. Delegation earns its overhead only on work that is large, separable, and cheap to check.

## The context handoff that lost the thread

A session runs out of context and hands off to a fresh one, but the handoff note assumed knowledge that lived only in the old session. The new session cannot reconstruct it and asks a human or guesses.

What stops it: write the handoff so it reads without the original session present. This overlaps with `memory-keeper`, which owns durable state across sessions; use it to persist what a handoff needs.

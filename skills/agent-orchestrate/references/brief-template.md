# Writing a brief that returns something usable

A brief is the contract between the parent and the child. When it is vague, the child fills the gap with a guess, and the parent gets back something it has to redo. This is the shape of a brief that comes back usable, with a worked example.

## The five parts

Goal. One sentence naming the outcome, not the activity. "Return the list of endpoints that lack auth checks" beats "look at the auth code".

Inputs. Everything the child needs, stated in full. A child cannot see the parent's context, so an input referenced but not supplied is an input the child will invent.

Result shape. The exact form the answer must take: a list, a table with named columns, a patch, a yes-or-no with evidence. This is the part most often left out and the part that decides whether the result is usable.

Done condition. The check that means the subtask is finished and correct. The child runs it before returning, and the parent runs it again on receipt.

Guardrails. What the child must not do, and what it should return instead of guessing. "If the config format is unclear, return the ambiguity; do not pick one" prevents a confident wrong answer.

## Worked example

A weak brief:

```
Look into why the build is slow and fix it.
```

The child does not know which build, what "slow" means, what it may change, or what to return. It will guess all four.

The same brief made usable:

```
Goal: identify the three slowest steps in the CI build defined in the pipeline
config at the path I give you.

Inputs: the pipeline config file contents (attached), and the timing log from
the last run (attached).

Result shape: a table of step name, measured seconds, and one sentence on why
it is slow. No code changes in this task.

Done condition: every row cites a line in the timing log. The three steps sum
to more than half the total build time or you say they do not.

Guardrails: if the timing log does not break down by step, say so and return
what it does show. Do not estimate timings that are not in the log.
```

The result of the second brief is something the parent can act on without a second round.

## Briefs for a review loop

A review brief adds two things: the criteria the reviewer checks against, and the round number. "Round 2 of at most 3" tells the reviewer a stop is coming and stops it from opening new issues on the last round that cannot be addressed. Give the reviewer the same done condition the author had, so they are measuring the same target.

## What a brief cannot fix

A brief cannot make an unseparable task separable. If the child needs to see the parent's full working context to do the job, the task was not ready to delegate, and the brief will be as long as the work. That is the signal to do it in the parent instead.

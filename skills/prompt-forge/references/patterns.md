# Patterns by job type

Reusable shapes. Each one exists because the job has a failure mode that a general prompt does not
address.

## Extraction and structured output

Failure mode: fields invented when the source does not contain them.

Give the exact schema, field by field, with types. Then give the rule for absence, which is the part
that matters: emit an explicit null and never infer a value. Require a quote or a location for every
extracted field so the result can be checked against the source. Ask for a list of fields that were
requested and not found.

For a batch, ask for one record per input with a stable identifier, so a missing record is visible.

## Code generation

Failure mode: code that looks right, uses an API that does not exist, and matches no convention in
the surrounding project.

State the language and version, the framework and version, and the runtime. Paste the interfaces it
must fit, not a description of them. Name the error handling and logging convention used in the
project. Say whether tests are wanted and in which framework. Say what may not be added, since new
dependencies are the usual unwanted surprise.

Ask for the code to be accompanied by the assumptions made about anything not shown.

## Critique

Failure mode: agreement, or manufactured nitpicking, depending on how the request was framed.

Do not ask whether the work is good. Ask what breaks, under which input, with what consequence.
Require a verdict. Require that a clean result be reported as clean rather than padded. Forbid style
commentary unless it causes a defect. For a stronger version of this, use the `reality-check` or
`code-review` skill, which carry the full anti-flattery contract.

## Long research

Failure mode: a fluent synthesis of whatever appeared first, with unverifiable attributions.

Require a citation per claim, with links that resolve. Require the date of each source, since currency
matters more than authority on most technical questions. Require contradictions between sources to be
reported rather than averaged into a smooth answer. Require an explicit list of questions the search
could not answer. Forbid a conclusion that no cited source supports.

See the `deep-research` skill for the full method.

## Prose work

Failure mode: generic register, which is the accent of the median answer.

Give a sample of the target voice, since a sample beats any adjective. Give the audience and what they
already know, which sets the level. Give the length as a number. Say what to leave out. Forbid the
patterns you do not want by name.

See the `human-prose` skill for the enforcement pass.

## Analysis on data

Failure mode: confident arithmetic that is wrong, and conclusions the data cannot support.

Require the calculation to be shown, step by step, with units. Require the result to be sanity checked
against an independent estimate. Require sample size and what the data cannot tell you. Forbid a causal
claim from correlational data. Where a script can compute it, ask for the script rather than the
answer, because a script is checkable and arithmetic in prose is not.

See the `numbers-check` skill.

## Decision support

Failure mode: a balanced list of considerations with no recommendation, which pushes the work back to
the asker.

Require a single recommendation with the reasoning. Require the strongest argument against it. Require
the conditions under which the recommendation flips. Require what evidence would be decisive and how
to get it this week. Forbid concluding that it depends.

## Agent and system prompts

Failure mode: instructions that contradict each other, so behaviour becomes unpredictable.

Order the rules by precedence and say that the order is the precedence. Separate the things that are
never permitted from the things that are defaults. Give a small number of hard rules rather than a long
list of preferences, since a rule that is sometimes ignored teaches that all rules are optional. Define
the stop condition, meaning when the task is finished. Define the escalation path, meaning what to do
when the task cannot be finished.

Test a system prompt by writing the three inputs most likely to break it, then checking what happens.

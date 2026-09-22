# Document skeletons

Each skeleton lists what belongs in a section and the mistake most often made there.

## README

```
# Name

One sentence: what it is and who it is for.

## Install
[The command. Prerequisites only if they are not obvious.]

## Use
[The smallest complete working example. Runnable as written.]

## Configuration
[Options as a table: name, default, effect.]

## Limits
[What it does not do. Saves the reader discovering it later.]

## Licence
```

The usual mistake is putting background, motivation, or architecture above the example. A reader arrives
wanting to know whether this solves their problem, and the example answers that faster than any
description. Badges and a logo do not belong above the first sentence.

## Specification

```
# Title

## Problem
[What is broken or missing now, with evidence. Not the solution.]

## Goal
[The outcome, stated so that success is checkable.]

## Out of scope
[Explicit exclusions.]

## Constraints
[Technical, legal, budget, timeline, and anything already decided.]

## Design
[The approach. Interfaces and data shapes concretely, not described.]

## Acceptance criteria
[Numbered, each independently verifiable.]

## Risks
[What could go wrong, and the trigger for each.]

## Open questions
[Named, with who decides and by when.]
```

The out of scope section is the one that prevents argument, and the one most often omitted. Acceptance
criteria that cannot be checked by someone who did not write them are not criteria.

## Decision record

```
# Decision: [the choice, stated as a decision not a question]

Status: proposed / accepted / superseded by [link]
Date: [ISO date]
Deciders: [names]

## Context
[The forces at play. What makes this a real decision.]

## Decision
[What was chosen, in one or two sentences.]

## Options considered
[Each option with its main advantage and the reason it lost. Include the option of doing nothing.]

## Consequences
[What becomes easier, what becomes harder, what is now locked in.]

## Reversal
[What would make this the wrong decision, and how expensive reversal would be.]
```

Keep these immutable. When the decision changes, write a new record and mark the old one superseded. An
edited decision record loses the history that made it worth writing.

The reversal section is what makes the record useful a year later.

## Runbook

```
# Runbook: [symptom as the reader would see it]

Severity: [what is broken for whom]
Owner: [team or person]

## Confirm the symptom
1. [command]
   Expected: [output]
   If different: [where to go instead]

## Mitigate
[Numbered steps. Stop the bleeding before diagnosing.]

## Diagnose
[Numbered steps with commands and what each result means.]

## Resolve
[Numbered steps.]

## Verify
[How to confirm it is actually fixed, not just quiet.]

## Escalate
[Who to wake, at what point, and how to reach them.]
```

Written for someone tired, under pressure, who did not build the system. Exact commands, copy and
pasteable, with expected output after each. Mitigation comes before diagnosis, because stopping harm
beats understanding it. No background prose anywhere.

## Release notes

```
# [version] - [date]

## Breaking
[Each change, what breaks, and the exact migration step.]

## Added
[User visible capability, described by what the user can now do.]

## Fixed
[The symptom that is gone, not the internal cause.]

## Known issues
[With workarounds.]
```

Group by what it means to the user, never by commit or by component. "Fixed a race in the session cache"
tells a user nothing, whereas "you no longer get logged out when two tabs refresh at once" tells them
whether to upgrade.

Breaking changes go first, with the migration step inline, because that is the only section some readers
need.

## Report and one pager

```
# Title

## Recommendation
[What to do, in one or two sentences. First, always.]

## Why
[The two or three reasons that actually drive it.]

## What it costs
[Money, time, and what gets given up.]

## What could go wrong
[The real risks, with likelihood.]

## Evidence
[Data and sources. Everything checkable lives here.]

## If you disagree
[The strongest argument against, and what evidence would change the recommendation.]
```

One page means one page. The evidence section can be long because nobody reads it in the meeting, but the
first three sections have to fit on a screen.

The final section is what earns trust with a sceptical reader, and it is the section people are most
tempted to leave out.

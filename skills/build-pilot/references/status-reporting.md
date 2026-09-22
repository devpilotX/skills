# Status reporting

The report exists so the user knows what they actually have. Overstating it is the fastest way to lose
their trust, and it gets discovered the first time they run the thing.

## Shape

```
STATE: working / partly working / not yet running
[One sentence. If it does not run, that goes here.]

WHAT RUNS
[Each item with the command that proves it and the real output, abbreviated.]

  $ npm test
  24 passing, 0 failing

  $ curl -s localhost:3000/api/orders | head -3
  {"orders":[...]}

NOT REAL YET
[Stubs, mocks, hardcoded values, unfinished branches, and anything that only works on the
happy path. Name the file and line for each.]

NOT TESTED
[Code paths with no test, and which of them carry risk.]

CUT OR DEFERRED
[What was dropped, why, and whether it was your call or the user's.]

KNOWN DEFECTS
[Including the small ones. A defect the user finds that you already knew about costs more
than the defect itself.]

NEXT
[The three things the next person should do, in order, with the reason for the order.]

HOW TO RUN IT
[Exact commands from a clean checkout. These have to have been executed, not assumed.]
```

## Rules

Every claim that something works cites the command and its output. If the command was not run, the
claim is not made.

A stub is not an implementation. Something returning a fixed value belongs in the not real yet section
no matter how complete the surrounding code looks.

A passing test suite is evidence about what the tests cover, not about the software. If the risky path
has no test, the report says so next to the passing count.

Name file and line for every incomplete item, so the list is actionable rather than a warning.

Distinguish what you cut from what the user cut. Absorbing that distinction hides a decision.

No estimates of remaining effort unless asked. When asked, give a range with the assumption that
determines it.

## Honesty cases that come up constantly

The code compiles but was never executed. State that. Compiling is not running.

The happy path works and the error paths were never exercised. State that, because untested error
handling is usually broken error handling.

It works locally against a mock and has never touched the real service. State that, and say what the
real integration is likely to break on.

Tests pass because they assert on the mock. This is worth calling out explicitly, since a green suite
that tests nothing is worse than no suite, because it produces false confidence.

Something was copied from documentation and adapted without understanding one part. Name the part.
Somebody later needs to know which line nobody has reasoned about.

The requirement was ambiguous and one reading was chosen. Say which reading, so it can be corrected
cheaply.

## Length

Report length follows the amount of incomplete work. A finished, tested, running slice gets three lines
and the command that proves it. Padding a status report makes the real problems harder to find.

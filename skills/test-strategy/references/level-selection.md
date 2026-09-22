# Level selection

A decision aid for choosing which kind of test fits a piece of code. Read down the table, pick the row that
matches what you are testing, and write the test at that level rather than defaulting to the level you find
easiest.

## The decision table

| What you are testing | Level | Why this level | What to avoid |
| --- | --- | --- | --- |
| A pure calculation with branches | unit | fast, exhaustive on edge cases | do not stand up a database for arithmetic |
| Input validation and parsing | unit | many inputs, one function | do not test through the HTTP layer |
| A state machine or transition rule | unit | each transition is one case | do not assert on private fields |
| A handler with its database | integration | the seam is where defects hide | do not mock the database and call it tested |
| A repository against its engine | integration | constraints and types differ from fakes | do not use an in memory substitute for a real engine |
| A queue consumer | integration | delivery and ordering are the risk | do not assert only that handle was called |
| A full signup or checkout journey | end to end | proves the parts connect | do not write fifty of these |
| An interface between two teams | contract | breaks the provider's build, not production | do not hand roll a shared fixture that drifts |
| A round trip or an invariant | property | finds inputs nobody would write | do not pin a single example and stop |

## How to read the table

The level is chosen by where the risk lives, not by what is convenient. A calculation with ten branches
wants ten unit tests, because standing up a database to check arithmetic is slow and proves nothing extra.
A handler that reads and writes a database wants an integration test against the real engine, because the
defect that reaches production is usually a constraint, a transaction boundary, or a type coercion that a
fake does not reproduce.

## The shape of the pyramid, and when to break it

Most codebases want many unit tests, fewer integration tests, and a small number of end to end journeys.
The end to end tests are slow and brittle, so keep the count low and the value high: the journeys that lose
money if they break.

Break the shape when the risk is concentrated at a seam. A thin service that mostly wires other services
together has little unit logic worth testing and most of its risk at the integration boundaries. Test where
the failure costs something, and let the shape follow the risk rather than forcing the risk into a shape.

## Choosing test doubles at each level

At the unit level, pass values in and read values out. If a unit needs a double, that is a hint the logic
is tangled with a dependency and might want a seam.

At the integration level, use the real thing wherever it is practical, which now includes the database and
the queue. Mock only at a boundary you do not own, such as a third party HTTP service, and build the
fixture from a recorded real response so it matches what the service actually returns.

At the end to end level, use as much of the real system as the environment allows. A double at this level
usually defeats the point, which is proving the real parts connect.

## Cost and speed budget

Unit tests should run in milliseconds each, so the whole set runs on every save. Integration tests run in
tens to hundreds of milliseconds and run on every change or every push. End to end tests run in seconds
each and run on a merge or a schedule. When a level drifts past its budget, people stop running it, and a
test nobody runs protects nothing.

## A worked selection

A function computes shipping cost from weight, destination zone, and a promotion flag, then a handler
persists the chosen rate to an orders table. Split it: unit tests cover the cost function across zero
weight, the zone boundaries, and the promotion on and off, with no database. One integration test covers
the handler writing the computed rate against the real database, checking the row and the currency column.
No end to end test here, because the shipping calculation is not a user journey on its own.

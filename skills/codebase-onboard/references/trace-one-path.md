# Tracing one path end to end

Reading files in isolation builds a map with no roads. Following one real request or one real job from entry to exit shows you which files connect, in what order, and where the surprises hide. Do this once early and the rest of the codebase falls into place around the path you walked.

## Pick the right path

Choose a path that carries weight: the login flow, the checkout, the main report, the job that moves the most data. Avoid a health check or a static page, because they touch almost nothing and teach almost nothing. The path should cross at least one boundary and hit at least one data store.

## Follow it, do not read around it

Start at the entry point you confirmed from the routing code. From there, at each function, answer one question: what does this call next? Do not wander into sibling functions that this path does not use. The discipline of following only the live path is what keeps the trace short enough to hold in your head.

When the next hop is not obvious, make the running system tell you. Add a log line that prints the function name and a marker, or set a breakpoint, and send one real request through. The stack trace at a breakpoint is the exact path, with none of the guesswork.

## Record the boundaries

Write the trace as an ordered list of hops. For each hop, note three things in prose: the function, whether it crosses a boundary such as a network call or a database query, and any state it reads or writes. A boundary is where latency, failure, and security live, so mark every one.

A worked example of the shape, for a checkout request:

```
1. POST /checkout            router registration in routes file
2. checkout_handler          validates the cart, reads session
3. pricing.total             pure calculation, no side effects
4. inventory.reserve         database write, can fail on stock
5. payment.charge            external call to payment provider, can time out
6. order.create              database write, returns order id
7. checkout_handler          serializes the response
```

That list tells you where to be careful. Steps 4 and 5 can fail independently, so a change near them needs to think about what happens when the reserve succeeds and the charge fails. You learned that from the trace, not from any single file.

## What the trace reveals

The trace exposes the real architecture. If step 3 turns out to call the database, the code is not as layered as the directory names claimed. If two entry points share steps 3 through 6, you found a genuine shared module. If a single request makes five separate calls to the same service, you found a performance problem before anyone reported it.

## When the path forks

Real paths branch. Follow the main branch first and note the forks without chasing them. A conditional that handles a rare case can wait; the common path is what teaches you the system. Come back for the branches only when a change actually touches them.

## Turn the trace into a test

If the path has no test that covers it end to end, the trace you just wrote is the outline of one. An end to end test that exercises the path you walked protects the next reader from the regression you were worried about. Writing that test belongs to `test-strategy`, but the trace is the specification it starts from.

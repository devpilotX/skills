# The eleven gates

Each gate lists what to look for and the questions that surface real defects rather than generic
advice. Skip nothing, but record a gate as not applicable when it genuinely is.

## Gate 1, correctness and error handling

Every external call, meaning network, disk, database, subprocess, and clock, can fail. Find the ones
with no handling.

Empty catch blocks, and catches that log and continue as though nothing happened.

Errors swallowed into a generic message that loses the cause.

Promise rejections and goroutine or thread panics with no handler at the top level.

Retries with no backoff, no jitter, and no cap, which turn a brief outage into a self inflicted denial
of service.

Operations that are not idempotent but get retried anyway. Payment capture and email sending are the
classic pair.

Partial failure in multi step work. If step three of five fails, what is the state of the first two?

Timezone and locale handling around dates, and any arithmetic on floating point money.

Off by one and boundary handling on pagination, slicing, and limits.

Questions that find real bugs: what happens on the second click of the submit button, what happens if
this request arrives twice, and what happens if the response is empty rather than absent.

## Gate 2, tests

Coverage percentage is close to meaningless on its own. Look for whether the tests would catch a
regression in the code that matters.

Does a test exist for each money path, auth path, and destructive operation?

Are failure paths tested, or only success paths? Untested error handling is usually broken error
handling.

Are there tests that assert on the shape of external responses, including the error shapes?

Do tests run in CI on every change, or only locally when someone remembers?

Are tests deterministic? Look for sleeps, real network calls, real clocks, and shared mutable
fixtures.

Is there at least one test that exercises the full path a user takes?

A useful check: pick the most dangerous function in the codebase, then find its test. If there is
none, that is the finding.

## Gate 3, secrets and configuration

Search history as well as the working tree, because a removed secret is still in the log.

```
git log -p --all -S "PRIVATE KEY" ; git log -p --all -S "api_key"
grep -rInE "(secret|token|password|api[_-]?key)\s*[:=]" --include="*" .
```

Hardcoded credentials, keys, and connection strings in source, config, test fixtures, or CI files.

Secrets in client side code or in anything bundled for the browser, including environment variables
inlined at build time.

`.env` files committed, or absent from `.gitignore`.

Default or example credentials left active.

No separation between development, staging, and production configuration.

No rotation path. If a key leaks today, what is the procedure, and is it written down?

If a live secret is found, say so in the first line of the report, because the fix includes rotation
and not only deletion.

## Gate 4, authentication and authorisation

Authorisation checked at the boundary but not on the object. The common defect is a handler that
confirms someone is logged in and then loads a record by an identifier from the request without
checking ownership.

Identifiers that are sequential and therefore enumerable.

Roles checked in the client only.

Session handling: expiry, invalidation on logout, invalidation on password change, and rotation on
privilege change.

Password storage using a current password hash with a sensible cost, not a general purpose digest.

Multi factor and account recovery flows, which are a frequent bypass.

Token scope and lifetime, and whether refresh tokens can be replayed.

Administrative endpoints reachable from the public internet.

Rate limiting on login, password reset, and anything that sends mail or costs money.

The test to run mentally: as user A, can I read or change user B's data by changing one value in the
request?

## Gate 5, input handling and injection

Database access built by string concatenation anywhere, including inside an ORM escape hatch.

Shell invocation built from user input.

Deserialisation of untrusted input into objects.

Rendering user content into HTML without escaping, and any use of the framework's explicit
bypass for raw HTML.

File upload handling: type validation by content rather than extension, size limits, storage outside
the web root, and filename sanitisation for traversal.

Server side request forgery on any feature that fetches a URL supplied by a user.

Redirect targets taken from request parameters.

Cross site request forgery protection on state changing requests, and whether the cookie policy
actually supports it.

Validation on the server for everything validated in the client, since client validation is a user
experience feature and not a control.

## Gate 6, data, migrations, and backups

Backups: do they exist, are they automated, and has a restore ever been tested? An untested backup is
a hope.

Migration reversibility, and what happens to a migration that fails halfway.

Migrations that lock a large table, and whether that was measured against production row counts
rather than a development dataset.

Data that cannot be reconstructed if lost, and whether it has stronger protection than the rest.

Personal data inventory: what is collected, where it lives, who can read it, how long it is kept, and
whether deletion actually deletes. Retention with no policy is a liability that grows.

Encryption at rest for anything sensitive, and in transit everywhere.

Foreign key and uniqueness constraints in the schema, rather than only in application code, since
application code has bugs and the database does not forget.

Soft delete semantics, and whether deleted rows still appear in exports and reports.

## Gate 7, failure and recovery

Single points of failure. What is the one process, host, or third party that takes the product down?

Health checks that actually check dependencies, rather than returning success unconditionally.

Behaviour when a dependency is slow rather than down, which is the harder and more common case.
Timeouts on every outbound call, with values chosen rather than defaulted.

Circuit breaking or shedding under overload, or at least a bounded queue.

Graceful shutdown: in flight requests finished, connections drained, work requeued.

Deploy rollback. Can the previous version be restored in minutes, and has that been done once on
purpose?

Data corruption recovery, which is distinct from outage recovery.

## Gate 8, performance and cost

Measure before claiming. Any performance number in the report is either measured with a named command
or labelled as an estimate.

Queries inside loops, which is the single most common scaling defect.

Missing indexes on columns used in filters, joins, and ordering. Read the query plan rather than
guessing.

Unbounded queries with no limit, and endpoints that return everything.

Payload sizes, image handling, and whether the client downloads more than it displays.

Caching: what is cached, how it is invalidated, and what happens on a cold cache. An invalidation
strategy of hoping is common.

Work done in a request that belongs in a background job, especially sending mail and generating files.

Cost per user or per request at the current price list, and which line grows fastest. For anything
calling a paid model API, compute cost at the usage of the heaviest ten percent of users, not the
average, because that is where the bill comes from.

Anything that scales with total data rather than with the page being viewed.

## Gate 9, observability

Can the team tell that it is broken before a user tells them? If not, that is the finding, and it
usually outranks the individual defects.

Structured logs with a request identifier that crosses service boundaries.

Errors reaching an aggregator, rather than only a log file nobody opens.

Metrics for the handful of things that indicate health: error rate, latency at a high percentile,
queue depth, and the main business event.

Alerts that page a human, with thresholds someone chose, and a documented owner.

Logs checked for personal data, tokens, and card numbers, which are routinely leaked there.

Log retention and volume, since both cost and compliance sit in that decision.

Audit trail for administrative and destructive actions, with actor, target, and time.

## Gate 10, accessibility and client quality

Keyboard only operation of every interactive path, including modals and menus.

Focus management: visible focus, focus trapping in dialogs, and focus restored on close.

Form labels properly associated, and errors announced rather than only coloured.

Contrast ratios against the current [WCAG guidance](https://www.w3.org/WAI/standards-guidelines/wcag/),
checked rather than eyeballed.

Images with alternative text that carries the same information, and decorative images marked as such.

Content that depends on hover or on colour alone.

Motion and animation honouring a reduced motion preference.

Behaviour at small viewport sizes and at 200 percent zoom.

Loading and empty and error states for every view that fetches data, since these are the states users
see when something goes wrong and the states that most often do not exist.

## Gate 11, dependencies, licences, and operations

Known advisories in the dependency tree, retrieved rather than assumed, and separated into runtime and
development since the risk differs.

Unmaintained packages, single maintainer packages, and anything pinned to a version with a published
advisory.

Lockfile committed, and builds reproducible.

Licence compatibility for every dependency against how the product ships. A copyleft dependency inside
a distributed proprietary binary is a legal problem, not a style preference.

Supply chain basics: dependency installation scripts, pinned CI actions, and who can push to the
default branch.

Operational items that block a real launch: a way for users to report problems, a documented
on call or at least an owner, a rollback runbook, terms and privacy text if personal data is
collected, cookie and tracking consent where required, and an accessibility statement where required.

Documentation sufficient for a second person to deploy the project without asking the author, which is
the practical test of whether the project can survive a holiday.

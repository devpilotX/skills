# Recurring tradeoffs

Analyses for the decisions that come up most. Each ends with the threshold that changes the answer.

## Deployment shape

A single deployable application with one database is the correct default, and remains correct much
longer than most teams believe. One repository, one deploy, one place to look when it breaks, real
transactions, and a call stack you can read.

Separate deployable services buy independent deployment, independent scaling, and a hard boundary that
survives staff turnover. They cost distributed tracing, network failure handling, eventual consistency,
schema coordination, and a platform to run them on. The cost is mostly operational and it is continuous.

Modules inside one deployable is the underused middle. Enforce boundaries in the code, keep one deploy,
and split later along seams that already exist. This keeps the option open cheaply.

What actually forces a split: a component with genuinely different scaling behaviour such as video
transcoding, a compliance boundary requiring separation, a team large enough that deploy contention is
measurable, or a part needing a different runtime.

Threshold: below roughly fifteen engineers, deploy contention is rarely the real constraint, so a split
usually costs more than it returns. Above that, measure how often deploys block each other before
deciding.

## Service communication

Synchronous request and response is easy to reason about, easy to debug, and couples availability. If A
calls B and B is down, A is down, unless A handles it, which it usually does not.

Asynchronous messaging decouples availability and absorbs load spikes. It costs ordering questions,
duplicate delivery, a dead letter path somebody has to watch, and debugging across logs rather than in
one stack trace.

Choose synchronous when the caller needs the answer to continue, and asynchronous when the work can
finish later. That is the whole rule. Adopting messaging for work the user is waiting on adds latency and
complexity without decoupling anything the user experiences.

Every asynchronous consumer must be idempotent, because delivery will repeat. Design the idempotency key
before writing the consumer.

## Datastore selection

A relational database is the default and covers most workloads well past the point people assume. It
gives constraints, transactions, joins, and a query planner that has had decades of work. Modern ones
handle JSON documents, full text search, queueing and geospatial data adequately, which removes several
reasons teams historically added a second store.

A document store suits genuinely schema-variable data where you never need to query across documents.
The usual failure is discovering later that you do.

A key value store suits caching, sessions, rate limiting, and ephemeral state.

A search index suits real text search with ranking. Treat it as a derived store that can be rebuilt, and
never as the source of truth.

A time series store suits metrics and telemetry at volume, where writes dominate and old data ages out.

A graph store suits traversals several hops deep as the primary access pattern, which is a narrower case
than it appears. Two hops in SQL is a join.

Every additional store adds a consistency problem, a backup requirement, an upgrade path, and an
operational burden. The bar for the second store is high.

Threshold: add a specialised store when a specific query pattern is measurably too slow in the primary
store after indexing has been done properly, not before.

## Caching

Order of attempts: fix the query and add the index first, then cache.

Cache invalidation is the hard part and it needs deciding before the cache is added. Time based expiry is
simple and serves stale data for a known window. Event based invalidation is correct and easy to get
wrong. Never invalidate on write into a cache written by another process.

Cache the expensive and stable. Never cache something whose staleness is visible to a user in a way that
matters, such as a balance or a permission.

Ask what happens on a cold cache. If the system cannot survive one, the cache is load bearing
infrastructure and needs the same care as the database.

## Tenancy

Shared schema with a tenant column is simplest and scales to many tenants. The risk is a missing filter
in one query leaking data across tenants, so enforce it at a layer that cannot be forgotten rather than
in each query.

Schema per tenant eases per tenant restore and export, and makes migrations slow past a few hundred
tenants.

Database per tenant gives the strongest isolation and the highest operational cost, and is usually driven
by a contract rather than by engineering.

Threshold: start shared unless a regulatory requirement or a signed contract says otherwise, and design
the tenant filter so that omitting it fails rather than returns everything.

## Where state lives

Stateless application processes are worth the discipline, because they make scaling, restarting and
deploying straightforward.

Session state belongs in a shared store or a signed token, never in process memory, or the second
instance breaks logins in a way that is hard to reproduce.

Background jobs belong in a durable queue, not in a timer inside a web process, or the work disappears on
deploy.

Uploaded files belong in object storage, not the local disk, unless there is exactly one machine forever.

Scheduled work needs a lock, or it runs once per instance.

## Serverless against long running processes

Serverless suits spiky, short, stateless work and shifts operational burden to the provider. It costs
cold starts, execution time limits, a harder local development story, connection pool pressure on the
database, and pricing that becomes unfavourable under steady high load.

Long running processes suit steady load, long connections, websockets, and anything needing a warm cache.

Threshold: at steady high utilisation, a reserved instance is usually cheaper than per invocation
pricing. Model the cost at expected load with `business-model` rather than assuming either direction.

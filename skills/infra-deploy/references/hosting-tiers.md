# Hosting tiers compared

Pick the simplest tier the requirements allow. The pain in infrastructure comes from running a platform
bigger than the workload needs, so the burden of proof sits on the more complex option. Every row below
trades operational cost for control, and the right choice is the one whose limits you will not hit soon.

## The tiers

### Managed platform hosting

A service takes a repository, builds it, and runs it. You push, it deploys. Lowest operational cost and
the fastest to start.

Costs you: per unit price at scale, limited control over the runtime, and trouble with long running
processes or unusual runtimes. Background work and websockets are sometimes constrained.

Right when: the app is a standard web service, the team is small, and predictable traffic does not need
hand tuned infrastructure. This is the correct answer for most applications for a long time.

Limits appear: when a process must run for minutes, when the runtime is exotic, or when per request cost
overtakes a rented machine.

### Single virtual machine with containers

One rented machine runs your containers behind a reverse proxy. Cheap, predictable, and something a
single person can understand end to end.

Costs you: patching the operating system, and a plan for when the machine dies, because it will. No
automatic failover unless you build it.

Right when: cost predictability matters, traffic is modest, and the team can operate a server.

Limits appear: when you need more than one machine and start reinventing load balancing and rollout by
hand.

### Managed container hosting

Runs your containers without you running a scheduler. A middle ground between a platform and Kubernetes.

Costs you: more configuration than a platform, less than a cluster. You still think about networking and
scaling policies.

Right when: you have outgrown a single machine but do not have the multi service orchestration that
justifies a cluster.

Limits appear: when orchestration across many services and complex networking becomes the daily work.

### Kubernetes

A cluster orchestrates many services with autoscaling and self healing. Powerful and a second product to
run.

Costs you: continuous attention, a steep operating skill set, and a control plane to keep healthy. For a
single application it is overhead with no return.

Right when: genuine multi service orchestration, autoscaling needs, or an existing platform team already
operating one.

Limits appear: not from capability, but from the staff time it consumes when adopted too early.

### Serverless functions

Short, stateless work runs on demand with no server to manage. Scales to zero.

Costs you: cold starts on infrequent calls, execution time limits, and pressure on database connection
pools when many instances start at once.

Right when: spiky, short, stateless work such as webhooks, scheduled jobs, and light API endpoints.

Limits appear: with long tasks, latency sensitive paths that cannot tolerate a cold start, or heavy
per invocation database use.

## Decision matrix

| Requirement | Platform | Single VM | Managed containers | Kubernetes | Serverless |
| --- | --- | --- | --- | --- | --- |
| Fastest to first deploy | Yes | No | Partly | No | Yes |
| Lowest operational burden | Yes | No | Partly | No | Yes |
| Cheapest at steady load | No | Yes | Partly | No | No |
| Long running processes | Partly | Yes | Yes | Yes | No |
| Many services orchestrated | No | No | Partly | Yes | No |
| Scales to zero | No | No | No | Partly | Yes |
| One person can operate it | Yes | Yes | Partly | No | Yes |

## How to record the choice

State the requirement that drove the decision, not the preference. "Chose a managed platform because the
app is one web service with steady traffic and the team is two people" is a reason. "Chose Kubernetes
because it is standard" is not.

Attach the monthly cost estimate with its source page and the date, and the assumed usage the estimate
rests on. Name the single line item that grows fastest with traffic, because that is the one that becomes
the bill. Note what would make you move up a tier, so the next person knows the trigger rather than
guessing.

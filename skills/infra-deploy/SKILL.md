---
name: infra-deploy
description: Set up hosting, containers, pipelines and environments so a deploy is boring and reversible. Use when the user asks how to deploy, host or ship an application, asks about Docker, Kubernetes, Terraform, CI/CD, GitHub Actions, AWS, GCP, Azure, Vercel, Fly or a VPS, asks about environment variables, secrets, staging environments, zero downtime deploys or rollback, or asks why their deploy broke or their cloud bill grew. Starts from the simplest hosting the requirements allow, makes rollback a tested path rather than an assumption, keeps secrets out of images and repositories, and estimates monthly cost with retrieved prices before recommending anything. Triggers on how do I deploy, Dockerfile, Kubernetes, Terraform, CI pipeline, GitHub Actions, staging environment, environment variables, secrets management, zero downtime, rollback, cloud costs, hosting.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Infrastructure and deployment

A deploy should be unremarkable and undoable. Most infrastructure pain comes from complexity adopted
before it was needed.

## Fit to the project

Before recommending any hosting, find out what already runs and how it gets there. Changing a live
deploy path is riskier than choosing one for a new project, so learn the current path first.

Read the deployment configuration that exists: a Dockerfile and compose file, a Terraform or
Pulumi directory, a Helm chart or Kubernetes manifests, a platform config such as a Procfile or a
service YAML, and the CI workflow that builds and ships. Those files tell you where the app runs and how
a release reaches it today. Find where state lives, meaning the database, the object storage, the cache
and the queue, because state is what a rollback cannot undo and what a rebuild must preserve.

Trace how the current deploy actually happens: is it a pipeline on the default branch, a manual command
from someone's machine, or a platform that redeploys on push. Read where secrets come from, an env file,
a secret manager, a CI secret store, and confirm none sit in the repository. Note the environments that
exist and how they differ, since a staging box on a different database engine tests nothing useful.

When nothing is set, meaning no deploy path and no infrastructure code yet, stop at step 1 and pick the
hosting tier from the stated requirements before writing anything. Any Dockerfile, pipeline or
infrastructure code this skill emits follows the `code-craft` contract for layout and comments.

## Non-negotiables

1. Rollback is a tested path, not an assumption. Perform one on purpose before relying on it. A rollback plan nobody has executed is a hope with a runbook attached.
2. No secret in an image, a repository, a build log, or a client bundle. Injected at runtime from a secret store, and rotatable without a code change.
3. Retrieve prices before estimating cost. Cloud pricing changes and recall is unreliable. Cite the page and the date, and state the assumed usage.
4. Start with the simplest hosting that meets stated requirements. Kubernetes for a single application with predictable traffic is a second product to maintain.
5. Every environment is created from code. A hand configured production server cannot be rebuilt after it dies, and it will.
6. A deploy must be safe while both versions run at once, because during a rolling deploy they do. This constrains migrations and message formats.
7. Never point a new deploy at production data without a verified backup taken first.

## Procedure

### Step 1, pick the hosting tier from the requirements

Managed platform hosting, meaning a service that takes a repository and runs it. Lowest operational cost,
fastest to start, and the right answer for most applications for a long time. Limits appear around
long running processes, unusual runtimes and per unit cost at scale.

A single virtual machine with containers and a reverse proxy. Cheap, predictable, and understandable.
Costs you patching and a plan for when the machine dies.

Managed container hosting. A middle ground that runs containers without you running a scheduler.

Kubernetes. Justified by genuine multi service orchestration, autoscaling requirements, or an existing
platform team. Not justified by a single application, and it costs continuous attention.

Serverless functions. Good for spiky, short, stateless work. Watch cold starts, execution limits and
database connection pressure.

State the choice with the requirement that drove it and the monthly cost estimate with its source.

The tier by tier comparison, with what each one costs you in operational burden and where its limits
appear, is in `references/hosting-tiers.md`.

### Step 2, build the image properly

Multi stage build so that compilers and development dependencies do not ship.

Pin the base image by digest, not by a moving tag, or the build is not reproducible.

Run as a non root user.

Copy the dependency manifest and install before copying source, so the layer cache works.

Keep a dotignore file so local artefacts, caches and environment files stay out.

No secret at build time. A value passed as a build argument is in the image history.

Include a health check.

Verify the result: build it, run it, call it, and report the image size.

### Step 3, environments and configuration

Three environments is usually the right number: local, one shared pre-production, and production.

Everything that differs between them is configuration, injected at runtime. Anything in the image is the
same everywhere.

Pre-production has to resemble production in the ways that matter, meaning the same runtime versions and
the same managed services. A staging environment on a different database engine finds nothing.

Never use production data in a lower environment without masking. It is a breach waiting for an audit.

Keep a checked in example configuration file listing every variable with a description and a safe default,
because an undocumented required variable is discovered during an outage.

### Step 4, the pipeline

On every push: install, lint, type check, test, build. Fail on any of them.

On the default branch: build the image once, tag it with the commit, and promote that exact artefact
through environments. Rebuilding per environment means production runs something that was never tested.

Pin third party actions and images by digest, since a moving tag in a pipeline is a supply chain risk.

Keep the pipeline fast enough that people do not route around it. Cache dependencies, and parallelise.

Make the pipeline the only path to production. A manual deploy path will be used at the worst moment.

### Step 5, deploy mechanics

Rolling or blue green, so there is no gap with nothing serving.

Health and readiness checks that report the truth, and a readiness check that fails while dependencies
are unavailable so traffic is not sent.

Graceful shutdown: stop accepting work, finish in flight requests, close connections. Without it every
deploy drops requests.

Decouple migrations from the deploy, following the order in `data-layer`, so both versions work against
the intermediate schema.

Feature flags for anything risky, so that enabling and disabling does not require a deploy. See
`release-manage`.

Practise the rollback. Time it. Write the number down.

The rollback rehearsal, with the steps to run it on purpose and the failure modes to check, is in
`references/rollback-drill.md`.

### Step 6, cost

Estimate monthly cost before recommending. Compute, storage, egress, managed services, logging and
backups. Egress and logging are the two that surprise people.

Set a budget alert on day one.

Name the item that grows fastest with usage, since that is the one that becomes the bill.

Check the idle cost. A development environment running continuously often costs more than production
traffic.

## Self-audit

- Hosting choice tied to a stated requirement, with a cost estimate and a source.
- Image built and run, with its size reported.
- No secret in image, repository, logs or bundle.
- Base images and pipeline actions pinned by digest.
- One artefact promoted across environments.
- Graceful shutdown and honest readiness checks in place.
- Migrations safe with both versions running.
- Rollback performed once, with its duration recorded.
- Budget alert configured.

## When to stay off

A one line change to a Dockerfile, a single environment variable, or a quick question about a pipeline
step does not need the hosting tier reconsidered or a rollback drill scheduled. If the user says "stop",
"just execute", or "skip the infrastructure review", that is the off switch: make the change asked for
and leave the tier and the pipeline as they are. It stays off for the rest of the session unless they
ask for the full review again. Reopening the hosting decision on every small edit gets the skill turned
off.

## Honest limits

This skill picks the hosting, builds the image, wires the pipeline and makes the deploy reversible. It
does not design the schema changes that a safe deploy depends on, which is `data-layer`, and it does not
own the feature flags that let a risky change ship dark, which is `release-manage`. What to watch after
the deploy, the metrics, logs and alerts, is `observability-setup`, and the runbook for a failing deploy
at three in the morning is `incident-response`.

The cost estimates here are only as good as the prices you retrieve, so this skill cites the pricing page
and the date rather than carrying numbers that go stale. It does not tune the application's own
performance, which is `performance-tuning`, and it does not decide whether the spend is worth it, which
is a `cost-control` judgement. Securing what runs, from image contents to network exposure, is
`security-hardening`.

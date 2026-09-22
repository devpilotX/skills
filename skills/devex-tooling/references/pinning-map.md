# Pinning map by ecosystem

Reproducible means the same inputs build the same output tomorrow. That takes three pins: the runtime
version, the dependency lockfile, and the base image digest. This table gives the file that carries
each pin per ecosystem. Commit every one of them.

## Runtime and manager pins

| Ecosystem | Runtime version file | Lockfile | Manager pin |
| --- | --- | --- | --- |
| Node.js | `.nvmrc` or `engines` in `package.json` | `package-lock.json`, `pnpm-lock.yaml`, or `yarn.lock` | `packageManager` field in `package.json` |
| Python | `.python-version` or `requires-python` | `poetry.lock`, `Pipfile.lock`, or `uv.lock` | pin the tool in the lock or in a constraints file |
| Ruby | `.ruby-version` | `Gemfile.lock` | `bundler` version recorded in the lock |
| Go | `go` directive in `go.mod` | `go.sum` | toolchain line in `go.mod` |
| Rust | `rust-toolchain.toml` | `Cargo.lock` | channel pinned in the toolchain file |
| Java | `.tool-versions` or a wrapper | Gradle or Maven lock | wrapper script, `gradlew` or `mvnw` |
| PHP | `platform.php` in `composer.json` | `composer.lock` | Composer version in CI |
| Multi language | `.tool-versions` for asdf or mise | per language as above | one manager per language |

One lockfile per project. Two lockfiles from two package managers resolve differently and produce
failures that appear only in continuous integration, where the other manager runs.

## Container base image pinning

Pin the base image by digest, not by tag. A tag such as `node:20` moves under you; a digest does not.

```
# floating, do not do this
FROM node:20

# pinned, reproducible
FROM node:20-slim@sha256:<the digest printed by docker inspect>
```

Record where the digest came from in a comment so the next person can update it deliberately. Update
the digest on the same schedule as dependencies rather than letting it drift.

## What each pin protects against

The runtime pin stops the classic split where one machine has a newer language version and reproduces
a bug the others cannot. It also lets the pipeline install the exact version rather than the latest.

The lockfile pins the whole transitive tree, not just the direct dependencies. Deleting it and running
install again is the single most common way a build becomes irreproducible, because the resolver picks
newer compatible versions that were never tested.

The image digest pins the operating system layer, the system libraries, and the preinstalled tools.
Without it, a rebuild months later can pull a base image with a different libc or a removed package.

## Verifying the pins hold

Run the setup from a fresh clone in a clean directory, on a machine that has never built the project,
and confirm it produces a working checkout with the recorded versions. A pin that has never been tested
from scratch is a pin nobody has confirmed.

In the pipeline, cache by lockfile hash so a rebuild with an unchanged lockfile reuses the resolved
tree, and invalidate the cache the moment the hash changes. That gives both speed and the guarantee
that a lockfile change is actually rebuilt.

## Common mistakes

Committing a lockfile but installing with a flag that ignores it. The flag defeats the pin silently.

Declaring a runtime version in the README as prose rather than in a file the tooling reads. Prose does
not get enforced, so it drifts.

Pinning the direct dependencies to exact versions but leaving the lockfile out of version control. The
transitive tree is where most surprises live, and only the lockfile pins it.

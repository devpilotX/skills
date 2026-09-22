# Feedback loop budgets

The feedback loop is the time from an action to the result that tells you whether it worked. When a
stage runs long, people route around it: they skip the hook, they push without running tests, they
stop running the type checker locally. These targets are what teams tolerate before that happens.
Measure your own numbers and replace these; a target is a starting line, not a measurement.

## Target times per stage

| Stage | Target | Route-around risk above target |
| --- | --- | --- |
| Save to formatted | under 1 second | Formatting on save gets turned off |
| Save to type error shown | under 3 seconds | The editor integration gets ignored |
| Save to relevant unit test result | under 10 seconds | Tests stop being run during development |
| Pre-commit hook | under 5 seconds | People learn the bypass flag and use it always |
| Full local test suite | under 2 minutes | The suite is run only in the pipeline |
| Clean install from lockfile | under 2 minutes | Fresh setup gets avoided, environments drift |
| Commit to green pipeline | under 10 minutes | Merges happen on red, review stalls |
| Incremental rebuild | under 5 seconds | Developers batch changes and lose the fast loop |

## How to measure each one

Save to result: use the editor's own timing or a stopwatch on a representative file, not the smallest
file in the repository. The number that matters is the one for a file people actually edit.

Test suite: run it three times after a warm cache and take the median, because the first run pays for
cache population that later runs do not.

Install: delete the dependency directory and the local cache, then time a full install from the
lockfile. Timing an install that reused a warm cache measures the cache, not the cost a newcomer pays.

Pipeline: read the duration the pipeline reports for the last ten runs on the default branch and take
the slowest, because the slow run is the one that blocks a merge.

## What to do when a stage is over budget

Formatting slow: scope the formatter to changed files on save and run the full pass only in the
pipeline. A formatter that reformats the whole tree on every save is misconfigured.

Type check slow: enable incremental mode and a build cache. Check that the checker is not reprocessing
generated files or vendored code that should be excluded.

Tests slow: split the suite so a change runs only the tests that touch it, with the full suite on push.
Look for real network calls, real clocks, and sleeps, which are the usual cause of a slow suite.

Install slow: cache dependencies in the pipeline by lockfile hash, and check whether a heavy dependency
pulls a large transitive tree that a lighter one would avoid.

Pipeline slow: cache by lockfile hash, run independent jobs in parallel, and build only what changed in
a monorepo. A pipeline that reinstalls everything on every run is the common cause.

Rebuild slow: use a tool that does incremental work properly and caches by input hash. Without caching,
a large project rebuilds far more than the change required.

## The rule that ties them together

Fix the loop before adding any further check. A check that pushes a stage over its budget trains people
to skip that stage, and a skipped check catches nothing. Speed is what keeps the guard rails in use, so
it comes before coverage every time the two trade off.

## Recording the numbers

Write the measured times into the repository, in the setup doc or a short `docs/tooling.md`, next to
the date they were taken. A number with no date rots quietly as the project grows, and the next person
cannot tell whether it still holds. Re-measure when a stage starts to feel slow rather than waiting for
someone to complain.

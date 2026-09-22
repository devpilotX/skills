# Branching, bisecting, and recovery

## Sizing a branch strategy

Copy the strategy to the team, not from a company whose constraints you do not share.

For most teams, trunk based development fits: short lived branches off a single main line, merged
within a day or two behind a passing test suite, with the main line always releasable. Short branches
mean small diffs and little merge pain, because integration happens continuously rather than in a big
bang at the end.

A heavier model with long lived develop and release branches earns its complexity only when you
genuinely support several released versions at once, or ship on a slow fixed cadence with formal
release stabilisation. Applied to a small team shipping continuously, that model adds merge overhead
and ceremony without a matching benefit.

Whichever you pick, protect the main line: require review and a green build before merge, and restrict
who can push directly. The rule that no shared history gets rewritten applies to every branch others
share, not only main.

## Finding a regression by bisecting

When a behaviour broke and the offending commit is unknown, bisect instead of reading commits one by
one. Bisect does a binary search over the history, so it tests about log2 of the range rather than the
whole range: a thousand commits become about ten tests.

```
git bisect start
git bisect bad                 # the current broken commit
git bisect good <known-good>   # a commit you know worked
```

Git checks out the midpoint. Test it, then mark it:

```
git bisect good                # this commit is fine, search newer
git bisect bad                 # this commit is broken, search older
```

Repeat until it names the first bad commit, then end the session:

```
git bisect reset
```

Where the test can be scripted, automate the whole search so you do not judge each step by hand:

```
git bisect run ./reproduce-test
```

The script exits zero when the commit is good and non zero when it is bad. This turns a long hunt into
a single command.

## Recovery recipes

The reflog is the safety net. It records where your branch pointers have been, so a commit that looks
lost after a reset or a bad rebase is usually still there and reachable by its hash.

```
git reflog
```

Find the hash of the state you want back, then recover according to the case.

Lost commit after a hard reset or a bad rebase. Point the branch back at the good state:

```
git reset --hard <hash-from-reflog>
```

Use this only on a branch whose history is yours alone, because it discards the commits after that
hash.

Committed on the wrong branch. Move the work to the right branch by cherry picking the commits onto
it, then remove them from the wrong branch:

```
git switch correct-branch
git cherry-pick <hash>
```

A bad merge that is already shared. Do not rewrite it, because others have it. Revert it instead, which
records a new commit that undoes the merge and keeps history honest:

```
git revert -m 1 <merge-hash>
```

A bad merge that is not yet shared. You may reset back to before it, since no one else has it.

An amend you regret. The pre amend commit is in the reflog; recover it by hash the same way.

The theme across every case: prefer a move that adds a commit or repoints a private branch over one
that discards shared work. Revert is safe on shared history; reset and force push are not.

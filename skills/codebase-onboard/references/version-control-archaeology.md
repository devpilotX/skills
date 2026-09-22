# Version control archaeology

The commit history is the only record of how the code was actually built, in what order, and by whom. It answers questions the code cannot: which files move together, which nobody dares touch, and who to ask when a comment lies.

## Files that change together

Two files that appear in the same commit again and again share a coupling the type system does not show. Change one and you probably need to change the other. To find the pairs, list the files per commit and count the repeats.

```
git log --pretty=format:%H --name-only | awk 'NF==1{c=$0;next}{print c" "$0}'
```

Group the output by commit and look for files that recur as a set. A route handler that always changes with a specific serializer, or a migration that always changes with a model, is telling you where the real modules are, regardless of the directory layout.

The rule of thumb: if two files changed together in more than half of the commits that touched either one, treat them as one unit when you plan a change.

## High churn files

Count how many commits touched each file. The busiest files are where the work concentrates and where bugs cluster, because change is where bugs come from.

```
git log --pretty=format: --name-only | sort | uniq -c | sort -rn | head -30
```

A file at the top of this list is either the heart of the system or a dumping ground. Read it early. A file with a hundred commits and no tests is the highest risk edit you can make.

## Files nobody touches

The opposite signal matters too. A file untouched for years is either stable and correct, or so frightening that people route around it. The commit messages on its last few changes usually say which.

```
git log -1 --format="%ai %an %s" -- path/to/file
```

If the last commit reads like a careful fix with a ticket reference, the file is probably stable. If it reads like "revert" or "hotfix, do not touch", route around it the way everyone else does until you understand why.

## Who to ask

For any file, the recent authors are the people who still remember it.

```
git log --format=%an -- path/to/file | sort | uniq -c | sort -rn | head -5
```

The top name is your fastest path to an answer that reading cannot give. If that person has left, their commits and the tickets they reference are the next best thing.

## Reading a suspicious change

When a line looks wrong, find the commit that introduced it before you rewrite it. The message and the surrounding diff often reveal a constraint that is not obvious from the code alone.

```
git log -1 -S"the exact suspicious string" -- path/to/file
git blame -L 40,60 path/to/file
```

A line that looks like a mistake is sometimes a fix for a bug you have not met yet. The history is how you tell a defect from a workaround.

## What history cannot tell you

A squashed or shallow history erases these signals. If the log shows one commit called "initial import", you have no archaeology to do and you fall back to reading and running. A repository that was migrated between version control systems often loses author and date fidelity, so treat old timestamps in a migrated repo with suspicion.

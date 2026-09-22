# Commit messages that say why

The diff shows what changed. The message exists to record what the diff cannot: why the change was
needed, what constraint forced it, and what it affects. That context is gone in six months, and the
person reading blame on a line cannot recover it from the code.

## Shape

A short subject line in the imperative mood, describing the change as an instruction: "Fix off by one
in pagination", not "Fixed" and not "Fixes". Keep it under about fifty characters so it reads in a log
and a pull request list.

A blank line, then a body that explains the why. What problem this solves, what alternative was
rejected and for what reason, what the reader should watch out for. Wrap the body so it reads in a
terminal, around seventy two characters.

A reference to the ticket or issue, so the fuller history is one click away.

## A message that helps versus one that does not

A message that does not help: "update code", "fix bug", "changes", "wip". These say nothing the diff
does not already show, and they make the log useless for finding anything later.

A message that helps names the reason. Instead of "change timeout to 30s", write that the downstream
service p99 latency crosses the old limit under load, so the timeout was raised to stop spurious
failures, with the ticket referenced. The next person changing that value learns why it is thirty and
not three.

## Why granularity and the message work together

A commit that does one thing can be described in one honest subject line. When you find yourself
writing "and" in the subject, that is the signal the commit bundled two ideas and should be split. The
message discipline and the commit granularity enforce each other: you cannot write a clean one line
subject for a commit that did five unrelated things.

## Conventional prefixes

Some teams prefix subjects with a type such as fix, feat, or refactor, sometimes to drive automated
release notes. Follow the project's convention if it has one. If it does not, do not impose a scheme
the team has not adopted; a clear plain subject beats a prefix nobody agreed to.

## Rewriting your own messages before they are shared

While the commits are still only on your machine, cleaning up messages and squashing noise is fair
game and improves the record. An interactive rebase lets you reword, reorder, squash, and split before
you push. Once the commits are shared, that freedom is gone, because rewriting them changes history
others have. Do the cleanup before the first push, not after.

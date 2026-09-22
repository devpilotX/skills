---
name: git-discipline
description: Treat version control as a record another person reads and a machine bisects, not a save button. Use when writing commits, when a diff is too large to review, when choosing a branch strategy, when a commit message says only what changed, when hunting a regression, when recovering from a bad merge or a lost commit or work on the wrong branch, or when tempted to force push a shared branch. Keeps one commit to one reversible idea, writes messages that say why, sizes the branch strategy to the team, keeps diffs reviewable, finds regressions by bisecting, recovers lost work through the reflog, and never rewrites history others have. Triggers on write a commit message, squash these commits, split this commit, branch strategy, git flow, trunk based, my diff is huge, find the commit that broke this, git bisect, recover a lost commit, undo a bad merge, wrong branch, git reflog, rebase or merge, force push.
license: MIT
compatibility: Any project using Git, in any language, solo or in a team, with any hosting provider or none. The commands shown are standard Git.
metadata:
  version: 1.0.0
  suite: skills
---

# Git discipline

Git gets treated as a save button: one commit at the end of the day named "fixes", a branch strategy
copied from a company a hundred times the size, and a diff so large the reviewer approves it without
reading it. Then a regression appears, the history is a wall of mixed changes, and nobody can find
which commit introduced it or revert it without pulling in unrelated work. The record was written for
nobody, so it helps nobody.

This skill keeps the history readable by the next person and usable by the tools that read it: one
commit that is one reversible idea, a message that says why, and history that others can rely on
because it does not get rewritten under them.

## Fit to the project

Read the project's existing habits before imposing a workflow.

1. Read the recent log. See how commits are sized, whether messages explain why or only what, and
   whether there is a subject and body convention already in use. Match a working local convention
   over this document.
2. Check for a stated contribution guide, a commit message template, or a pull request template. If
   one exists, it wins, and this skill fills the gaps it leaves.
3. Look at the branch names and the merge pattern in the log: is history linear from rebasing or does
   it show merge commits, and is there a long lived release branch or a single main line. Keep the
   pattern the team already reads.
4. Confirm who else shares the branches you are on. The rule against rewriting history depends
   entirely on whether anyone else has the commits you are about to change.

## Non-negotiables

1. Never rewrite history that another person already has. A force push, a rebase, or an amend on a
   shared branch changes commits others have based work on, which loses their commits or forces a
   painful recovery on everyone who pulled. Rewrite only commits that never left your machine.
2. One commit is one reversible idea. A commit that mixes a bug fix, a rename, and a new feature
   cannot be reverted without dragging in the other two, and it cannot be understood at a glance. If
   the subject line needs the word "and", the commit is doing too much.
3. The commit message says why, not only what. The diff already shows what changed. The message
   records the reason, the constraint, or the ticket, because that context is gone in six months and
   the diff cannot recover it.
4. Do not use a destructive command that discards work until you have a way back. A hard reset, a
   force push, or a branch delete can lose commits, and the safety net is the reflog plus not having
   rewritten shared history. Confirm the recovery path exists before running the command.
5. Keep a diff small enough to actually review. A change of thousands of lines gets rubber stamped, so
   the defects in it ship. Split the work into reviewable pieces rather than asking for a review no
   one can honestly give.

## Procedure

### Step 1, size each commit to one idea

Stage by intent, not by "everything that changed". Group the hunks that belong to a single idea and
commit them together, then the next idea separately. Use patch mode staging to split a file's changes
across commits when they belong to different ideas. The result is a series where each commit could be
reverted alone and the log reads as a sequence of decisions.

### Step 2, write the message that survives six months

Write a short subject in the imperative describing the change, then a body that explains why it was
needed and what it affects. Reference the ticket or issue. The test is whether someone running blame
on this line in a year learns why the line is the way it is from your message alone. The message
patterns and examples are in `references/commit-messages.md`.

### Step 3, size the branch strategy to the team

Do not copy a heavyweight branching model from a large organisation onto a small team. For most teams,
short lived branches off a single main line, merged quickly behind tests, keep integration pain low. A
long lived release branch earns its cost only when you genuinely support multiple released versions at
once. The strategies and when each fits are in `references/branching-and-recovery.md`.

### Step 4, keep the diff reviewable

Before opening a review, read your own diff as the reviewer will. Separate a noisy mechanical change,
such as a formatting pass or a rename, into its own commit or its own pull request so it does not bury
the real change. If the diff is too large to review in one honest sitting, split it. A reviewable diff
is a rule of thumb of a few hundred changed lines, less when the logic is dense.

### Step 5, find a regression by bisecting

When something broke and you do not know which commit did it, bisect rather than reading every commit.
Tell the tool one known good commit and one known bad commit, and let it check out the midpoint each
round so you test a logarithmic number of commits instead of all of them. Automate the check with a
script that exits zero for good and non zero for bad where the test can be scripted. The exact
commands are in `references/branching-and-recovery.md`.

### Step 6, recover from a mistake safely

For a bad merge, a lost commit, work committed on the wrong branch, or an amend you regret, the reflog
records where the branch pointers were, so a commit that seems lost is usually still reachable. Recover
by pointing a branch back at the right commit or cherry picking the work onto the right branch, using
non destructive moves first. The recovery recipes for each case are in
`references/branching-and-recovery.md`. Do not reach for a hard reset or a force push as the first
move, because those can turn a recoverable mistake into a lost one.

## Self-audit

- Could each commit be reverted on its own without dragging in an unrelated change?
- Does each subject line describe one idea, with no "and" joining two changes?
- Does each message say why the change was made, not only what changed?
- Is the branch strategy sized to this team rather than copied from a much larger one?
- Is the diff small enough that a reviewer can read all of it honestly?
- Before any destructive command, was the recovery path confirmed, and was shared history left
  unrewritten?
- When hunting a regression, was bisect used rather than reading every commit by hand?
- Has no commit that another person already pulled been rewritten?

## Honest limits

This skill governs how you use version control. It does not review the code inside the commits, which
is owned by `code-review`, nor does it decide how a release is cut and tagged, which is owned by
`release-manage`.

The diff size and cadence figures here are rules of thumb, not measurements, and a team with a
different review culture will set different ones. This skill assumes Git; another version control
system has its own recovery model and its own history rules, and those specifics are out of scope.

## Off switch

If the user says "stop", "just execute", or "skip the git review", stand down and do only the version
control action asked for. The off switch holds for the rest of the session unless the skill is invoked
again. A skill that keeps reshaping commits after being declined gets uninstalled.

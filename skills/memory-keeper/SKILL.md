---
name: memory-keeper
description: Keep durable project memory in plain text so a session that closes days ago can be resumed without a human retelling the context. Use when work spans more than one session, when an agent hands off to another agent or tool, before a risky step that might need to be undone, or at the end of any session worth resuming. Writes project facts, dated decisions with reasoning, current task state, open questions, and an append-only log, keeps files under a size budget by summarising old detail, reads them in a fixed order at startup, and corrects memory when the code disagrees. Triggers on remember this for next time, save the context, where did we leave off, pick up where we stopped, resume the project, hand this off, write it down before we lose it, keep a project log, record this decision, dont lose this context, session memory, project notes, what did we decide last week.
license: MIT
compatibility: Any project in any language. The optional CLI needs Python 3.8 or newer and uses only the standard library.
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Memory keeper

A session ends and the reasoning behind it goes with it. Days later the next session reopens the repository, cannot tell which choices were deliberate and which were accidents, and either asks the human to retell everything or quietly repeats a mistake that was already solved and reverted. This skill writes a small set of plain-text files into the repository so the reasoning survives the session that produced it.

## Fit to the project

Read what the project already keeps before adding a second place to look.

1. Check for an existing memory or notes location: a `docs/` folder, an `ADR` or `decisions` directory, a `CHANGELOG`, a wiki, or a `NOTES` file. If dated decisions already live somewhere, write there instead of starting a rival store.
2. Read the ignore rules. The memory directory is committed, so confirm its path is not swept up by a broad ignore pattern, and confirm nothing secret is committed near it.
3. Detect the version control in use so the memory directory lands in a tracked path and travels with the code, not in a local scratch folder that dies with the machine.
4. Where the project keeps nothing, create the directory described in `references/file-format.md` and say in your report that you started it.

## Non-negotiables

1. Never write a secret, token, key, password, connection string, or customer record into memory. These files are committed and readable by everyone with the repository. A leaked credential in git history costs a rotation and an audit, and the history keeps the leak after the file is edited.
2. The code is the source of truth, not the memory. When a memory file disagrees with what the code now does, the code wins. Correct the memory with a new dated note that says what changed; do not trust a stale fact over the running system.
3. Never rewrite a past log entry or a past decision in place. History that gets edited cannot be trusted later. A reversal is a new dated entry that names the one it overturns, so the change is visible.
4. Keep each file under its line budget. A memory file that grows without bound stops being read, which defeats the point. When a file passes budget, summarise the oldest detail into a shorter form and keep the summary; do not delete the detail silently.
5. Write at the moments that matter: at a decision, before a risky or hard-to-reverse step, at a handoff to another agent, and at session end. Memory written only when convenient loses exactly the context that was expensive to acquire.

## Procedure

### Step 1, read before writing

At session start, read the memory files in the fixed order in `references/file-format.md`: current state first because it is cheapest and most immediate, then facts, then decisions, then open questions, then the tail of the log. Stop once you have enough to act. The order exists so context rebuilds without reading every file in full.

Produce a one paragraph summary of where the work stands, and note any file the briefing flagged as over budget.

### Step 2, reconcile memory against the code

Before acting on any remembered fact, confirm it against the code or the running system when the cost of being wrong is high. If a decision says the cache is write-through and the code now shows write-back, the code wins. Append a dated correction to the log and fix the fact. Never let a confident but stale memory drive a change.

### Step 3, write at the moment, not at the end

When a decision gets made, record it with its date, the choice, the reason, and the alternatives rejected. When a risky step is about to run, write the current state and the intended next step first, so an interrupted session can recover. Keep the log append-only and dated.

### Step 4, compact when a file passes budget

Run the budget check. For any file over its limit, replace a run of old low-value detail with a short dated summary that keeps the conclusion and drops the play-by-play. Facts that are still true stay. Decisions are never compacted away; only their surrounding narrative is. Record in the log that you compacted and which range you summarised.

### Step 5, hand off cleanly

Before passing work to another agent or tool, write the current state so it reads without you present: what is done, what is in progress, the next concrete step, and any half-finished change that must not be assumed complete. A handoff that depends on memory held only in the current session context is a handoff that loses the context on the next turn.

### Step 6, use the CLI or write the files by hand

The files are plain Markdown, so any tool or a human can write them by following `references/file-format.md`. When Python is available, the shipped CLI does the mechanical parts:

```
python3 scripts/memory.py init
python3 scripts/memory.py brief
python3 scripts/memory.py log "switched the cache to write-through after stale reads"
python3 scripts/memory.py decision "use SQLite for local runs" --why "no server in CI" --instead-of "a Postgres container"
python3 scripts/memory.py budget
```

The `brief` command prints the session-start briefing in the fixed read order and flags files over budget. Code the CLI emits or that you write around it follows the `code-craft` contract, so it arrives organised and commented rather than as one block. The read protocol and the compaction rules of thumb are in `references/read-protocol.md`.

## Self-audit

- Does every memory file avoid secrets, tokens, keys, and customer data?
- Is the memory directory in a committed, tracked path rather than a local scratch folder?
- Were decisions recorded with a date, a reason, and the alternatives rejected?
- Where memory disagreed with the code, did the code win and the memory get a dated correction?
- Is every file within its line budget, or was an over-budget file compacted with a summary that kept the conclusion?
- Were past entries left intact, with changes made as new dated entries rather than edits in place?
- Does the current state file read well enough for a different agent to resume without asking?

## Honest limits

This skill keeps notes; it does not manage code history. Branching, tags, and release notes belong to `release-manage`, and the reasoning format for architecture choices overlaps with what `arch-decide` produces, so defer to an existing ADR store when one exists. The CLI cannot detect a secret in the text it is handed, so the caller carries that rule. Memory is only as accurate as the last write, and the reconciliation step against the code exists because it will drift.

The off switch: say "stop" or "skip the memory" and this skill stands down for the rest of the session unless you invoke it again. It will not keep writing notes after you decline.

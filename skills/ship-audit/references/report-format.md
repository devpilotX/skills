# Report format

Verdict first. A reader who stops after four lines should still know what to do.

## Severity

Critical. Data loss, data exposure, unauthorised access, money moving incorrectly, or total outage.
Blocks release with no discussion.

High. A likely path to a broken experience for many users, or a defect that gets much more expensive
after launch, such as a schema decision or an absent audit trail.

Medium. Real defect with a workaround or limited blast radius.

Low. Worth fixing, safe to schedule.

Observation. Unconfirmed, or a judgement call the author may reasonably decline. Kept separate so the
confirmed list stays trustworthy.

Severity follows consequence, never effort. A one character fix preventing a data leak is critical. A
month of refactoring for elegance is low.

## Structure

```
VERDICT: SHIP / SHIP WITH FIXES / DO NOT SHIP / NOT ENOUGH ACCESS
[One or two sentences. If DO NOT SHIP, the reason is in this line.]

SCOPE
Reviewed: [paths, commit or branch]
Commands run: [each command and its result]
Not reviewed: [what was out of reach and why it matters]
Assumed bar: [internal tool / public product / handles money / handles personal data]

BLOCKERS
1. [CRITICAL] path/to/file.ts:142 - [what is wrong]
   Trigger: [exact sequence that causes it]
   Consequence: [what is lost]
   Fix: [the specific change]

HIGH
[same shape]

MEDIUM AND LOW
[same shape, may be condensed to one line each]

GATES
Correctness: pass, checked [what]
Tests: finding, see 3
Secrets: pass, scanned working tree and history
[... all eleven, each pass / finding / not applicable / not reviewed]

OBSERVATIONS
[Unconfirmed items, clearly marked]

IF YOU FIX ONLY THREE THINGS
[The three with the best consequence to effort ratio, in order]
```

## Rules

Findings are numbered so they can be referenced in a follow up.

Line numbers are real. Cite a symbol name instead if the file is likely to move.

Trigger and consequence are separate fields on purpose. A finding with no trigger is an assumption,
and a finding with no consequence is a preference.

The gates table is what makes the report honest. It shows coverage, including the parts skipped, so
the reader can judge how much the verdict is worth.

The three item section at the end is the part most readers act on. Choose by consequence, not by ease.

Do not include a closing summary. The verdict is already at the top.

## Length

Report length tracks the number of real problems. A clean project gets a short report. Padding a
report to look thorough is the same failure as flattery, and it trains the reader to ignore the next
one.

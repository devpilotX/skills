# Verdict guide

The verdict is the first thing the author reads and often the only thing a busy author reads. It has to
be one of four values, and the value has to follow a rule the author can predict, so that a review feels
consistent from one change to the next.

## The four verdicts

APPROVE means the change is correct on the paths that matter, safe to merge as written, and needs nothing
from the author. Preferences may still appear below, clearly marked as optional. Use this when you ran the
checks and found nothing that would break in production.

APPROVE WITH FIXES means the change is sound but carries findings the author should resolve before merge,
none of which change the design. A missing null guard, an untested failure path, an off by one on a
boundary. The author can fix these without a second review round.

REQUEST CHANGES means at least one finding blocks merge: a correctness defect on a real path, a security
hole, an irreversible data operation with no safeguard, or a contract change that breaks a caller. The
first line names the single most important blocking reason.

NEEDS MORE CONTEXT means the change cannot be judged yet. The intent is unclear, a referenced file was not
provided, or the diff hides the caller that decides whether a finding is real. Say exactly what you need
to finish the review.

## Choosing between them

Start at APPROVE and demote only for a reason you can name.

Any blocking finding forces REQUEST CHANGES, however small the diff. One object level authorisation gap in
a hundred line change still lets a user read another user's record.

A non-blocking finding demotes APPROVE to APPROVE WITH FIXES. It does not reach REQUEST CHANGES, because
the author does not need a second round to land a null guard.

Missing intent or missing context beats everything and forces NEEDS MORE CONTEXT. Reviewing without the
goal produces findings that argue with a decision the author never made.

## Ranking findings inside the report

Order by consequence, not by the order you found them or by how easy they were to spot.

A data loss defect outranks a logic defect. A logic defect on a common path outranks one on a rare path. A
security finding outranks a clarity finding every time. Two findings of equal consequence order by how
many users the failure reaches.

Put the reasoning for the ranking in one clause per finding, so the author can disagree with the order
rather than guess at it.

## Wording that keeps a review usable

Write the trigger as a concrete input, not as a category. "When items is empty" beats "in edge cases".
"When two requests arrive before the first commits" beats "under concurrency".

Write the consequence in terms of who is hurt. "The second user sees the first user's balance" beats "this
is a race condition".

Write the fix as the smallest change that closes the finding, and stop there. A fix that also tidies the
surrounding code turns a two line review into a rewrite the author did not ask for.

Never pad the report to look thorough. A three line review of a clean change carries more trust than
twenty lines of manufactured style comments, and trust is the only thing that keeps reviews read.

## A worked verdict

A change adds a discount code to checkout. The success path is correct and tested. The code reads the
discount record, then writes the order total, with no lock between the read and the write, and no test for
two requests at once.

Verdict: REQUEST CHANGES. First line: concurrent checkout can apply a discount twice because the read and
write are not atomic. Blocking finding names the exact sequence, the consequence in money, and a fix that
takes the row lock or moves the arithmetic into a single statement. The rest of the review is short,
because the rest of the change is clean and saying so is honest.

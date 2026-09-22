# Ranking findings by reachability

A vulnerability list sorted by theoretical severity sends the fix effort to the wrong place. What matters
is what an attacker actually reaches: a medium-severity flaw on an unauthenticated public endpoint
outranks a critical one that needs three prior compromises. This file gives the ranking method, the
prerequisites vocabulary, and worked orderings so findings arrive in the order they should be fixed.

## What reachability means

For each finding, state what an attacker must already have before the finding is usable. That prerequisite
chain is the reachability. The fewer and easier the prerequisites, the higher the finding ranks,
regardless of the raw severity score.

Prerequisite ladder, from easiest to hardest for an attacker:

  Nothing. The endpoint is public and unauthenticated.
  A free account. Anyone can register and reach it.
  A specific low-privilege role. The attacker needs a normal user account.
  A valid identifier they can guess or enumerate.
  A stolen session or token.
  Network position, such as being inside the internal network already.
  A prior compromise of another component.
  Physical access to a device.

A finding that needs "nothing" and yields data theft is at the top of the report. A finding that needs "a
prior compromise" and yields the same data sits far lower, because reaching it means the attacker already
won somewhere else.

## The ranking table

Order by the pair (prerequisite height, impact), with prerequisite height dominating.

  Rank 1: no prerequisite, high impact. Example: an unauthenticated endpoint returning any user's record
  by changing an identifier. Fix first.
  Rank 2: no prerequisite, medium impact. Example: user enumeration on the login form that speeds a later
  credential attack.
  Rank 3: free account, high impact. Example: a registered user reaching an admin function because the
  role check is only in the interface.
  Rank 4: low-privilege role, high impact. Example: object-level authorisation missing, so user A reads
  user B's records with a guessed identifier.
  Rank 5: guessable identifier, medium impact. Example: sequential invoice numbers exposing totals.
  Rank 6: stolen token, high impact. Example: a token with no expiry that stays valid after logout.
  Rank 7: internal network position, high impact. Example: a database port open only inside the network
  with a weak account.
  Rank 8: prior compromise required. Example: a deserialisation flaw reachable only from an already
  compromised internal service.

## Worked ordering

A scan returns five findings. Sorted by raw severity a scanner might list them critical, critical, high,
medium, low. Re-sort by reachability:

  A "high" stored cross-site scripting in a public comment field, reachable with nothing: goes to the top.
  A "critical" remote code execution in an internal admin tool reachable only from inside the network and
  behind authentication: drops well down, because the attacker needs a foothold and an admin session
  first.
  A "critical" SQL injection in a public search parameter, reachable with nothing: near the top, above the
  admin-tool RCE.
  A "medium" missing object-level authorisation reachable by any registered user: mid-table, above the
  internal RCE.
  A "low" verbose error message leaking a stack trace, reachable with nothing: stays low on impact but is
  cheap to fix, so note it as quick remediation.

The reordered report is: public SQL injection, public stored cross-site scripting, missing object-level
authorisation, internal admin RCE, verbose error leak. That order matches what an attacker would try
first, which is the order the owner should fix.

## Writing each finding

For every finding, record four things so the reader can weigh it without rerunning the test:

  What an attacker needs, stated as the prerequisite from the ladder above.
  What they get if it works, in concrete terms, such as "reads any user's address and order history".
  How you confirmed it, such as the exact identifier swap you performed on your own system.
  The fix, addressing the class rather than the one instance, since one missing check usually means the
  pattern is wrong in more than one place.

## The trap to avoid

Do not let a high severity number float a finding to the top when its prerequisites are steep. The
attacker does not read the severity score; they take the cheapest path in. Reachability is the honest
sort order, and it is the one that gets the dangerous things fixed first.

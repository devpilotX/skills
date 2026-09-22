# Gates

A gate is a deliberate stop where the user holds information the process needs. Three of them are
mandatory, and each has a defined question and a defined failure if skipped.

## Gate 1, after the restatement

Question for the user: is this what you actually want built?

Present the restatement, the assumptions, and the out of scope list. Ask for correction on those three
things only, not for approval of a design that does not exist yet.

What goes wrong if skipped: the whole build solves the wrong problem, and nobody finds out until
delivery. This is the single most common way software work gets wasted, and the gate costs one message.

Proceed without an answer only when the request is unambiguous and small. Say that you are proceeding
on the stated reading.

## Gate 2, after the options

Question for the user: which approach, given these costs?

Present the options with the recommendation and the argument against it. Keep it to three options at
most, because more than that pushes the decision back onto the asker.

What goes wrong if skipped: a one way decision gets made by whoever typed fastest. Data models, vendor
choices, auth models and public interfaces are expensive to reverse, and the user often knows a
constraint that rules an option out.

Never pass this gate unanswered on a one way door. For a reversible choice, pick the simplest option,
say why, and note that it can be changed later.

## Gate 3, after the plan

Question for the user: is this the right order, and is the first slice the right first slice?

Slice order decides what exists if the work stops early, which happens often. Confirming it is cheap
insurance.

What goes wrong if skipped: the build spends its first days on the part that was easy to start rather
than the part that was most likely to be wrong.

## Gates during the build

Two situations require an unscheduled stop.

A discovery that invalidates the decision. Something researched in stage 2 turns out wrong, or a
limitation appears that the design did not account for. Stop, say what changed, and return to stage 3
with the new fact. Do not patch around a broken premise.

A scope change. Either the user adds something, or the work reveals a requirement nobody saw. Name what
it costs, what it displaces, and let the user choose. Quietly absorbing scope produces a late project
with no visible cause.

## How to hold a gate without being obstructive

Ask for the minimum. One question with a recommended default beats five open questions.

Give a default and say you will use it. "I will use Postgres unless you have a reason not to" moves
faster than asking which database and waiting.

Keep working on anything the gate does not block. If the data model is undecided but the build tooling
is not, set up the tooling.

Never re-ask a question the user already answered. Record decisions as they arrive and treat them as
settled unless new evidence arrives.

Never use a gate to avoid committing. The recommendation is still required at every gate.

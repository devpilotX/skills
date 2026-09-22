# A reconciliation, from mismatch to found error

Reconciliation is the control that catches almost everything, and the difference between the bank and the
ledger is not noise to absorb but a number that points at its own cause. This file works one month end
from a failed reconciliation to the located errors, so the diagnostic patterns in the main file have a
concrete shape. All amounts are illustrative.

## The starting position

  Bank statement closing balance: 41250.00
  Ledger closing balance for the same account: 40977.00
  Difference: 273.00

The ledger is short by 273.00. A difference is a signpost, so before scanning every line, test it against
the patterns that explain most reconciliation gaps.

## Test the difference against known shapes

Divisible by nine? 273 / 9 = 30.333, so no. A difference that divides evenly by nine usually means a
transposed digit, such as 91 entered as 19.

Exactly twice a plausible entry? Half of 273 is 136.50. If an entry of 136.50 exists with the wrong sign,
posting a payment as a receipt or the reverse, it moves the balance by twice its value. Scan for 136.50.
None found, so this is not a single sign error of that size.

A round number that looks like a missing fee or transfer? 273.00 is not obviously round, so it is likely
a combination rather than one clean cause. That is common, and the way through is to reconcile line by
line. Tick each item that appears on both sides until only the unmatched items remain.

## Line by line matching

Tick every transaction that appears identically on the bank statement and in the ledger. What is left
after ticking is the set of items that live on only one side. In this month the unmatched items are:

  On the bank statement but not in the ledger:
    Bank charge, monthly account fee: 18.00
    Card processing fee settlement: 205.00

  In the ledger but not on the bank statement:
    Customer payment recorded, not yet cleared: 500.00

  A payment processor settlement recorded gross in the ledger, net at the bank:
    Ledger shows a 1200.00 sale; the bank received 1150.00 after a 50.00 fee.

## Resolve each unmatched item

The two bank fees, 18.00 and 205.00, were never entered in the ledger. Bank and processor fees are among
the most commonly missed entries. Post them as expenses. This raises the ledger by 223.00 of the missing
223 toward the gap.

The 500.00 customer payment in the ledger has not yet cleared the bank. This is a timing difference, not
an error. It stays as a reconciling item and clears next period, so it does not need a ledger change.

The gross versus net settlement is the classic processor trap. The ledger recorded the 1200.00 sale but
never recorded the 50.00 fee the processor deducted before settling. Post the 50.00 as a processing
expense. This accounts for the final 50.00 of the difference.

## Confirm the reconciliation

  Missing bank fees posted: 18.00 + 205.00 = 223.00
  Missing processor fee posted: 50.00
  Total ledger correction: 273.00
  Uncleared customer payment held as a timing item: 500.00

After posting the 273.00 of missed fees, the adjusted ledger balance agrees with the bank statement once
the 500.00 in-transit receipt is set aside as a legitimate timing difference. The gap is explained in
full, and nothing was plugged.

## What to record

Note each correcting entry with its reason, so next month the same fees are expected and entered as they
occur rather than found again at reconciliation. Add the processor to the list of accounts that need their
own reconciliation against the settlement report, since the gross-to-net gap there is a recurring source
of missing fee entries. The exercise succeeds when this month agrees and when the same errors do not
recur.

## When the difference will not resolve

If line-by-line matching leaves a difference that none of the patterns explain, do not force it into a
suspense account and move on as though it were solved. Record the unexplained amount in a suspense
account, list it as an open question with the exact figure and the period, and put it on the handover list
for the accountant. An unexplained difference sitting visibly in suspense is honest; one absorbed into a
convenient category is a future problem.

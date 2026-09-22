# Rights requests, retention, vendors, and evidence

The parts of compliance that fail in practice are the ones that have to run repeatedly: serving a
request, deleting on schedule, and proving a control works. Written policy is not enough for any of
them.

## Retention and deletion that runs

A retention period written in a policy but enforced by nothing is a promise the system breaks every day.
For each data item, set a period tied to its purpose, then build the mechanism that acts on it.

Run a scheduled job that finds data past its retention period and deletes or anonymises it. Anonymising
means removing the link to a person so thoroughly that it cannot be reversed, not merely hiding a
column, because data that can be re-identified is still personal data.

Decide how deletion reaches backups. A live deletion that leaves the record in a nightly backup means a
restore brings the deleted data back. Options are to exclude certain data from backups, to age backups
out on a defined cycle so deleted data disappears within a bounded window, or to re-apply deletions
after a restore. Pick one and document it, because "we deleted it" is false if a backup still holds it.

Test the deletion path against a sample record end to end: create it, let the retention trigger, and
confirm it is gone from the live store, the logs, the analytics, and within the backup window. An
untested deletion path usually misses one of those places.

## Serving access, deletion, and portability requests

Build one repeatable workflow, because these requests arrive without warning and often carry a deadline.

Verify the requester is who they claim, so you do not disclose one person's data to another. Locate the
subject's data everywhere the inventory says it lives, including logs, backups, and third parties, not
only the main database. For an access request, return what is held in a readable form. For a
portability request, return it in a structured, machine-readable form the subject can move elsewhere.
For a deletion request, delete or anonymise across every location and confirm each, then record what was
done and when.

Track the deadline from the day the request arrives, and retrieve the applicable deadline from the
governing regulation rather than assuming one, because it differs by framework. A request you serve
partially, missing the copies in backups or at a vendor, is not served.

## Vendors and sub-processors

Every third party that processes data on your behalf is a processor, and its own vendors are
sub-processors. For each, record what data it receives, what it does with it, where it processes it, and
what agreement governs it. A vendor handling personal data with no data-processing agreement is a gap to
flag, not to reason around, because the responsibility for their handling flows back to you.

When a vendor uses its own sub-processors, that chain matters: your data can end up somewhere you never
sent it directly. Ask each vendor for its sub-processor list and its processing locations, and treat an
unclear answer as a finding.

## Cross-border transfer

Data moving between jurisdictions can trigger extra requirements, because a receiving country's
protections may differ from the sending one's. Map where each data flow physically processes and stores
data, including a vendor's hosting region and its sub-processors' regions. Where a flow crosses a border
that a governing framework restricts, note it and route the question of which transfer mechanism is
valid to a qualified professional, since that validity is a legal judgement and the recognised
mechanisms change.

## Evidence, not intention

An auditor treats a control you cannot evidence as a control you do not have. For each control you
claim, keep something inspectable.

Access restriction: a current list of who and what can reach the data, plus a log of when access was
granted and revoked. "Access is limited" without the list is an assertion.

Encryption: the configuration showing it is on, for data at rest and in transit, rather than a statement
that it is.

Retention: the job definition and its run log showing it executed and what it removed.

Requests served: the record of each request, what was done, and the date, so a pattern of timely service
is visible.

Change control: the history showing the inventory and the controls were updated when the system changed.

Keep this evidence collected and current rather than assembled in a panic before a review. A control
that worked but left no evidence cannot be proven to have worked, and to a reviewer that is the same as
having failed.

## The handoff to a professional

Where an answer requires deciding whether something is lawful, valid, or certifiable, write the question
rather than the answer. State the situation, the data and amounts involved, what you already checked,
and the specific decision needed. A precise question is the useful output, because it saves the lawyer
or auditor the time they would otherwise bill to reconstruct the context.

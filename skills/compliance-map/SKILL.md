---
name: compliance-map
description: Turn a vague data-protection or regulatory obligation into a checkable list grounded in what your system actually does, for any product and any jurisdiction. Inventories the data and its flows first, classifies by sensitivity, records a lawful basis or justification per purpose, makes retention and deletion actually run, and names precisely where a qualified lawyer or auditor has to take over. Use when a regulation or customer questionnaire asks what data you hold and why, when a deletion or access request arrives with no process to serve it, when preparing for a security review or audit, when adding a vendor that will process personal data, or when data crosses a border. Triggers on GDPR compliance, data protection audit, what personal data do we hold, data inventory, records of processing, handle a data deletion request, right to access, data retention policy, vendor data processing agreement, cross border data transfer, prepare for SOC 2, privacy review, subject access request, lawful basis for processing.
license: MIT
compatibility: Any product, any language, any jurisdiction. Regulations are named as examples only; no single law or framework is assumed.
metadata:
  version: 1.0.0
  suite: skills
---

# Compliance map

Asked about compliance, a model tends to summarise a named law and hand back a generic checklist that
has nothing to do with what the system in front of it actually stores or does. That checklist feels
like progress and changes nothing, because it was never grounded in the real data flows, and the first
access or deletion request that arrives finds no process to serve it. Compliance starts from an
inventory of what data exists and where it moves, not from a regulation, and this skill does that
grounding and then names the exact point where a licensed professional has to take over.

## Not legal advice, read first

This skill does the mapping and inventory work that sits underneath a legal or audit judgement. It does
not replace either.

What it does. Inventories the data a system holds and traces where it flows. Classifies data by
sensitivity. Records a stated justification per processing purpose. Turns retention and deletion into
processes that run. Builds the workflow to serve access, deletion, and portability requests. Lists
vendors that process data and what agreement each needs. Assembles an audit trail a reviewer can
follow. Writes the precise questions to put to a lawyer or an auditor.

What it does not do, in any jurisdiction. Tell you whether a specific processing is lawful. Interpret a
regulation or a regulator's notice. Confirm that a given lawful basis is the correct one. Decide whether
a cross-border transfer mechanism is valid. Sign off on an audit or certify a control. Assess penalty
exposure. Draft a binding contract clause. Those are judgements that fall to a qualified lawyer or
auditor in the relevant jurisdiction, because the consequence of getting them wrong falls on you and not
on a model.

Never state a specific legal threshold, deadline, penalty, or definition from memory as though it were
settled. Retrieve it from the regulation or regulator with a source and a date, or mark it as needing a
professional to confirm. A confidently wrong deadline on a deletion request causes the violation it was
meant to prevent.

## Fit to the project

Read the system before reading any regulation.

1. Find where data enters and lives. Look through the schema, the models, the API endpoints that accept
   input, the logs, the analytics and error-tracking integrations, and the backups. Personal data hides
   in logs and third-party trackers as often as in the main database.
2. Map every third party that receives data. List the SDKs in the dependency manifest, the outbound API
   calls, the payment and email and analytics providers, and the hosting regions. Each one is a
   processor whose location and contract matter for cross-border transfer.
3. Identify the jurisdictions in play: where your users are, where your servers are, and where your
   company is established. These three can differ, and the strictest applicable rule usually governs, so
   name a regulation as one input rather than the whole answer.
4. Find what already exists: a privacy policy, any retention setting, any deletion path, any record of
   who can access production data. Gaps between the written policy and the running system are the
   findings that matter most.

## Non-negotiables

1. Inventory the data before reading the regulation. A checklist copied from a law you have not mapped
   to your own flows produces false confidence and misses the data sitting in logs, backups, and
   trackers that no generic list mentions.
2. Every processing purpose has a recorded justification, and the same data is not quietly reused for a
   new purpose without a new one. Purpose creep, where data collected for one reason feeds another, is
   the failure most audits find and most breaches worsen.
3. Retention and deletion have to actually run, not merely be written in a policy. A stated ninety-day
   retention that no job enforces is worse than none, because it is a documented promise the system
   breaks daily, and a backup that keeps deleted data forever quietly defeats a deletion.
4. An access, deletion, or portability request has a defined process that finds the data everywhere it
   lives, including backups and third parties, within the applicable deadline. A request you cannot
   serve completely is a violation regardless of intent.
5. Every claim of a control is backed by evidence a reviewer can inspect, not by an assertion. "Access
   is restricted" without a list of who has it and a log of grants is an intention, and an auditor
   treats an unevidenced control as an absent one.
6. Where a question crosses into whether something is lawful or a control passes, stop and write the
   precise question for a qualified professional rather than answering it.

## Procedure

### Step 1, inventory the data and its flows

Build a record of what personal or regulated data the system holds, for each item where it is collected,
where it is stored, who can reach it, how long it is kept, and where it flows onward. Trace the flows
end to end, including logs, analytics, error tracking, backups, and every third party. The output is a
data map, and its format is in `references/inventory.md`. Do this before opening any regulation.

### Step 2, classify by sensitivity

Sort the inventoried data into sensitivity tiers, because the obligations scale with the tier. Ordinary
identifiers sit at one level; categories a regulation treats as special, such as health, biometric, or
financial data, sit higher and carry stricter handling. Payment card data and government identifiers
usually carry their own regime. Mark each item's tier on the map, so the controls and retention can
follow the tier rather than treating everything alike. The tiers and examples are in
`references/inventory.md`.

### Step 3, record a lawful basis or justification per purpose

For each processing purpose, write down the justification the applicable framework recognises, whether
that is consent, a contract, a legal obligation, or another recognised basis, and what would have to be
true for it to hold. Keep this per purpose, not per data item, because the same data can be processed
under different justifications for different purposes. Mark any purpose where you are unsure of the
correct basis as a question for a professional rather than guessing one.

### Step 4, make retention and deletion run

For each data item, set a retention period tied to its purpose and build the job that deletes or
anonymises data past it, then confirm the job runs and covers backups. Decide how a deletion request
reaches data held in backups, since a backup that restores deleted records defeats the deletion.
Document the deletion path end to end and test it against a sample record. The retention and deletion
patterns are in `references/rights-and-vendors.md`.

### Step 5, build the request and vendor processes

Build a repeatable workflow to serve access, deletion, and portability requests that locates the
subject's data everywhere it lives and responds within the applicable deadline. Separately, for each
vendor that processes data, record what data it receives, where it processes it, and what agreement is
in place, and flag any vendor with no data-processing agreement or an unclear location as a gap. Both
workflows are detailed in `references/rights-and-vendors.md`.

### Step 6, assemble the audit trail and name the handoff

Collect the evidence a reviewer would ask for: the data map, the justification records, the retention
jobs and their run logs, the request workflow and served examples, the vendor agreements, and the access
control list with its grant log. Then write the handoff: the specific questions where a lawyer or
auditor has to decide, each stating the situation, what you found, and the decision needed. Report the
inventory, the classification, the gaps found, and the handoff questions.

## Self-audit

- Is there a data map that traces every data item from collection through storage to onward flow,
  including logs, backups, and third parties?
- Is every item classified by sensitivity tier, with special-category data marked?
- Does every processing purpose have a recorded justification, with uncertain ones flagged for a
  professional?
- Does a retention job actually run for each item, and does deletion reach backups?
- Is there a tested workflow that serves an access, deletion, or portability request completely and
  within the deadline?
- Does every vendor that processes data have a recorded location and agreement, with gaps flagged?
- Is every claimed control backed by inspectable evidence rather than an assertion?
- Does the handoff name each question that requires a lawyer or auditor, with the situation and the
  decision needed?

## Honest limits

This is not legal advice and it is not an audit. It maps what your system does and turns an obligation
into a grounded, checkable list, and it stops at every point where whether something is lawful, valid,
or certifiable has to be decided. Those decisions belong to a qualified lawyer or auditor in your
jurisdiction, and the value here is a precise question that saves their billable time rather than an
answer that pretends to replace them.

It names regulations only as examples and does not track their current text, which changes; retrieve the
live requirement from the regulation or regulator before relying on any threshold or deadline. The
security controls that the evidence describes are implemented and hardened by `security-hardening`, the
data model and its stores by `data-layer`, and the honesty of any risk numbers by `numbers-check`. This
skill maps and lists; it does not build the controls or judge whether they pass.

The off switch: say "stop" or "just execute" and this skill stands down. Nothing more is mapped this
session. It stays off until you invoke it again. You can proceed without mapping any of this, and
the first regulator question or customer security review will show you what the inventory would have
found.

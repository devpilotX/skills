# Data inventory and sensitivity classification

The inventory is the artifact everything else depends on. A regulation cannot be applied to a system
whose data flows nobody has written down.

## What a data map records

For each item of personal or regulated data, record these fields. Keep it in whatever format the team
will maintain, a table or a structured file, so long as every field is present.

The data item, named specifically. "Email address" and "device identifier", not "user data".

Where it is collected: which form, endpoint, SDK, or import brings it in.

Where it is stored: which database, which table or collection, which log stream, which analytics tool,
and which backups.

Who can reach it: which roles, which services, and which third parties.

The purpose it is processed for, stated as a specific use rather than a general one.

How long it is kept, and by what mechanism it is deleted or anonymised at the end.

Where it flows onward: every third party that receives it and the region that party processes it in.

The sensitivity tier, from the classification below.

## Where personal data hides

The main database is the obvious place. The gaps that inventories miss:

Application logs and request logs, which often capture full request bodies, headers, IP addresses, and
identifiers that were never meant to be retained.

Error and crash tracking, which can capture stack traces containing user input and session data.

Analytics and product-metrics tools, which receive identifiers and behaviour by design and process them
in a region you did not choose.

Backups and snapshots, which keep copies of everything long after the live record changed or was
deleted.

Third-party SDKs embedded in a client, which can send data directly from the user's device to a vendor
without touching your servers, so it never appears in your database yet is still your responsibility.

Support tickets, email, and spreadsheets, where personal data accumulates outside any system with a
retention control.

## Sensitivity tiers

Classify each item so the handling scales with the risk rather than treating a marketing preference like
a medical record.

Ordinary personal data: a name, an email, an account identifier, general profile fields. Standard
handling and retention apply.

Sensitive or special-category data: information many frameworks single out for stricter treatment, such
as health, biometric, genetic, racial or ethnic origin, religious belief, sexual orientation, trade
union membership, and precise location. This tier usually needs a stronger justification and tighter
access, and some of it you may be better off not collecting at all.

Regulated financial and identity data: payment card data, bank details, and government-issued
identifiers. These commonly carry their own dedicated regime with specific storage and handling rules,
so keep them out of general stores and note the regime that applies.

Children's data: data about minors, which many jurisdictions protect more strictly regardless of the
tier it would otherwise fall in. If your product can be used by children, flag it, because the rules
change.

Mark the tier on every item in the map. The tier drives the retention period, the access restriction,
and whether a processing purpose needs a stronger justification, so a map without tiers cannot drive
any of those decisions.

## Keeping the map current

An inventory made once and never updated becomes wrong the first time someone adds a field or an
integration. Tie an inventory update to the change process for the schema and the dependency manifest,
so a new data field or a new vendor cannot ship without appearing on the map. A stale map is worse than
none, because it is trusted while being wrong.

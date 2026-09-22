---
name: email-deliver
description: Get application email into the inbox instead of spam or the void, on any stack and any sending provider. Sets up authentication that receivers actually check, separates transactional from marketing identities, warms a new domain slowly, keeps the list clean, and treats bounces and complaints and unsubscribes as hard rules rather than nice-to-haves. Use when mail lands in spam, when a new domain sends nothing that arrives, when signup or receipt or reset messages go missing, when a provider warns about complaint rate, or when reputation drops and delivery falls with it. Triggers on my emails go to spam, email not being delivered, set up SPF DKIM DMARC, password reset email never arrives, gmail rejects my mail, high bounce rate, spam complaints, warm up sending domain, verify sending domain, why is my email in junk, transactional email setup, improve deliverability, DMARC failing, sender reputation dropped.
license: MIT
compatibility: Any language, any application, any sending provider or self-hosted mail transfer agent. The optional record checks use dig or nslookup, both standard on common systems.
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Email deliver

A model asked to add email usually wires up a send call, points it at a from address on a fresh domain,
and reports success because the API returned 200. The message then lands in spam or nowhere, the bounce
and complaint feedback is dropped on the floor, and nobody notices until a customer says the password
reset never came. Delivery is a property of authentication, reputation, and list quality, and none of
those is visible in a 200 response.

## Fit to the project

Read what already exists before adding a single record or line of code.

1. Find how mail is sent today. Look for a provider SDK or SMTP client in the dependency manifest, an
   existing from address in configuration or environment variables, and any template directory. Match
   the sending path already in place instead of introducing a second one.
2. Detect the sending domain and whether it is the same domain as the website. Query the current SPF,
   DKIM, and DMARC records for that domain so you know the starting point rather than guessing. The
   commands are in `references/diagnostics.md`.
3. Separate the kinds of mail the project sends. Password resets and receipts are transactional and
   have to arrive within seconds. Newsletters and product announcements are marketing and can wait.
   These belong on different subdomains, and mixing them is a common cause of transactional mail
   getting caught in a marketing reputation problem.
4. Note where bounces, complaints, and unsubscribes are handled today. If the answer is nowhere, that
   is the first gap to close, because a provider will throttle or suspend an account that keeps sending
   to addresses that reject or complain.

Adopt the provider the project already pays for rather than switching. Any reputable sending provider
can reach the inbox with correct setup, and the setup is what this skill is about.

## Non-negotiables

1. Never send to an address the user did not knowingly give you for this purpose. Bought lists,
   scraped addresses, and addresses collected for one purpose and reused for another produce complaints
   and spam-trap hits that can blacklist the sending domain for months.
2. Every message has to pass DKIM and SPF with the signing and envelope domains aligned to the visible
   from domain. Passing without alignment does not satisfy DMARC, and a receiver enforcing a reject
   policy will drop the mail. Alignment is the point, not mere presence of a record.
3. Handle bounces and complaints on receipt. Suppress any address that hard bounces once, and any
   address that files a complaint, permanently. Continuing to send to a known bad address is what turns
   a warning into a suspension.
4. Every marketing message carries a working one-click unsubscribe that takes effect without a login,
   and the suppression happens before the next send. A broken or slow unsubscribe generates complaints,
   and complaints cost more reputation than the unsubscribe ever would.
5. Warm a new sending domain by volume over days, not all at once. A cold domain that sends fifty
   thousand messages on day one looks exactly like a compromised account to a receiver, and the mail
   gets filtered as a block.
6. Generated sending and webhook code follows the `code-craft` contract: the send path, the retry
   logic, and the bounce and complaint handlers live in separate functions with names that say what
   they do, and every failure carries which message and which recipient it concerned.

## Procedure

### Step 1, set up authentication and prove alignment

Publish three record types for the sending domain and confirm each one resolves. SPF is a TXT record
listing the hosts allowed to send for the domain, checked against the envelope sender. DKIM is a
public key in DNS whose matching private key signs each message, so a receiver can confirm the body
and headers were not altered. DMARC is a TXT record at `_dmarc.` that tells receivers what to do when
SPF or DKIM fail, and it is the record that ties the other two to the visible from address through
alignment.

Start DMARC at `p=none` with a reporting address so you collect aggregate reports without affecting
delivery, read the reports until every legitimate source passes aligned, then move to `p=quarantine`
and finally `p=reject`. Moving straight to reject before reading reports will silently drop mail from
a forgotten sending source. The record syntax and a reading guide are in `references/records.md`.

### Step 2, split sending identities

Send transactional mail from one subdomain and marketing mail from another, each with its own DKIM
key and its own reputation. A subdomain such as one reserved for receipts keeps a marketing complaint
spike from delaying a password reset. Document which subdomain each message type uses so a later change
does not merge them by accident.

### Step 3, warm the domain and keep the list clean

For a new domain, raise volume gradually over one to two weeks, starting in the low hundreds per day
and roughly doubling when complaint and bounce rates stay low. Send to the most engaged recipients
first, because opens and low complaints early build the reputation that carries the later volume. Treat
these numbers as a rule of thumb and slow down if any rate climbs.

Collect addresses with confirmed opt-in where the recipient clicks a link to verify. Validate syntax
and the domain's mail records at capture time to catch typos. Remove any address that has not engaged
over a long window from marketing sends, because sending to dead addresses drags the whole domain's
reputation down.

### Step 4, wire up feedback and suppression

Configure the provider to deliver bounce, complaint, and delivery events to a webhook, verify the
signature on every event, and record the outcome per recipient. On a hard bounce or a complaint, add
the address to a suppression list the send path checks before every send. On a soft bounce, retry a
few times over hours and suppress if it keeps failing. A worked handler is in
`references/diagnostics.md`.

### Step 5, watch reputation and diagnose drops

Track bounce rate, complaint rate, and any reputation dashboard the provider exposes. A rule of thumb
many providers publish is to keep the complaint rate under roughly one in a thousand and hard bounces
low; a sudden climb usually means a bad import, a compromised form, or a spam trap in the list. When
delivery drops, narrow down where the message stops: does the provider accept it, does the receiver
accept it at SMTP, does it pass DMARC at the receiver, and does it land in inbox or spam. The
narrowing checklist is in `references/diagnostics.md`.

### Step 6, check content and links

Keep a real text part alongside the HTML, avoid link shorteners and mismatched display URLs, and host
images and links on domains that share the sending domain's reputation rather than on a domain a
filter distrusts. Avoid a single giant image with no text, which is a classic spam pattern. Report the
records published, the subdomains chosen, the suppression rules, and the monitoring in place.

## Self-audit

- Does SPF, DKIM, and DMARC resolve for the sending domain, and does a test message pass all three with
  aligned domains?
- Is DMARC advanced past `p=none` only after reports confirm every legitimate source passes aligned?
- Do transactional and marketing messages send from separate subdomains with separate keys?
- Is there a suppression list that the send path checks before every send, populated from hard bounces
  and complaints?
- Does every marketing message carry a working one-click unsubscribe that suppresses before the next
  send?
- Are bounce and complaint webhook events signature-verified before they are trusted?
- For a new domain, was volume raised gradually rather than sent in one large batch?
- Does the report name the records, subdomains, suppression rules, and monitoring, with no address sent
  to that was not knowingly collected?

## Honest limits

This skill gets mail authenticated and keeps a sending reputation clean. It does not write the marketing
copy or design the template, and it cannot force a specific receiver to deliver a message, because inbox
placement is the receiver's decision and no sender controls it outright. It does not cover the legal
side of consent and marketing permission across jurisdictions; that boundary belongs to `compliance-map`.
The application code that calls the send path and handles the webhook is owned by `backend-build`, and
the readability of that code is owned by `code-craft`.

The volume and rate figures here are rules of thumb drawn from what sending providers publish, not fixed
limits, and a specific provider's stated thresholds override them. When a provider documents a different
number, use theirs.

Say "stop" or "just execute" and the skill stands down for the session. That is the off switch. It
stays off until you invoke it again. Sending mail without any of this is a choice you can make, and
you will find out about it when the deliverability drops.

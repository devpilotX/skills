# Diagnosing where mail stops, and handling feedback

Delivery is a chain, and a message can die at any link. Narrow down which link before changing
anything, because the fix for a provider rejection is nothing like the fix for a spam-folder placement.

## Checking the records that already exist

Query the live records before you publish new ones, so you know the starting point. On a system with
dig:

```
dig +short TXT example.com
dig +short TXT selector1._domainkey.example.com
dig +short TXT _dmarc.example.com
```

Where dig is unavailable, nslookup does the same:

```
nslookup -type=TXT example.com
nslookup -type=TXT _dmarc.example.com
```

Read the SPF record for a `-all` or `~all` ending and count the includes against the ten-lookup limit.
Read the DMARC record for the current policy value. If any record is missing, that is the first thing
to fix.

## The narrowing checklist

Follow the message from send to inbox and find the last link that succeeded.

1. Did the provider accept the message for sending? Check the send API response and the provider's own
   activity log. A rejection here is an authentication or account problem, not a receiver problem.
2. Did the receiving server accept it at SMTP? The provider log records the remote response. A 5xx
   rejection carries a reason: a reputation block, a bad address, a policy refusal. A 4xx is a
   temporary defer that the provider will retry.
3. Did it pass DMARC at the receiver? The DMARC aggregate reports show pass or fail per source. A fail
   here points at alignment, not at content.
4. Did it land in inbox or spam? This is the only link the logs cannot tell you. Use seed addresses on
   the major mailbox providers you care about and check placement directly, because a message can be
   accepted, pass DMARC, and still be filed in spam on content or reputation grounds.

Fix the earliest failing link first. Fixing content when the real problem is a failing DMARC alignment
wastes a day.

## What a sudden reputation drop usually means

A gradual decline usually tracks list decay: engagement falling as addresses go stale. A sudden drop
almost always has a specific cause worth hunting immediately:

A bad import, where a batch of old or purchased addresses went out and hit spam traps or generated
complaints. A compromised signup form or account, where a spammer is using your sending path. A content
change that tripped filters, such as a new link domain with no reputation. A single large recipient
domain that started rejecting, which shows as a cliff on one destination rather than across all of
them.

Isolate by segment. Break the numbers down by recipient domain, by message type, and by send batch, and
the drop usually localises to one of them, which names the cause.

## Handling bounces and complaints

Configure the provider to post delivery events to a webhook, and treat every event as untrusted until
its signature is verified. A handler in pseudocode, to be written in the project's language against the
`code-craft` contract:

```
on webhook_event(request):
    if not verify_provider_signature(request):
        reject 403
    event = parse(request.body)
    switch event.type:
        case hard_bounce:
            suppress(event.recipient, reason="hard_bounce", permanent=true)
        case complaint:
            suppress(event.recipient, reason="complaint", permanent=true)
            unsubscribe_from_marketing(event.recipient)
        case soft_bounce:
            record_soft_bounce(event.recipient)
            if soft_bounce_count(event.recipient) > 5:
                suppress(event.recipient, reason="repeated_soft_bounce", permanent=false)
        case delivered:
            record_delivery(event.recipient)
    return 200
```

The send path reads the suppression list before every send and skips any suppressed address. A hard
bounce means the address does not exist or refused permanently, so it never gets another message. A
complaint means the recipient marked the mail as spam, which is the most damaging signal a mailbox
provider records, so that address is suppressed and pulled from marketing at once.

## Unsubscribe as a hard requirement

Every marketing message carries an unsubscribe that works without a login and takes effect before the
next send. Support the one-click header that mailbox providers read, so a recipient can unsubscribe
from the mailbox interface without opening the message. A slow or broken unsubscribe converts people
who would have quietly left into people who file a complaint, and a complaint costs far more reputation
than an unsubscribe.

## A minimal set of alerts

Alert when the complaint rate over a rolling window crosses the provider's stated threshold, when the
hard bounce rate on a send batch spikes, and when a DMARC report shows a new sending source you did not
expect, because an unexpected source is either a forgotten integration or a spoofer.

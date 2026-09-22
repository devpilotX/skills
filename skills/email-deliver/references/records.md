# Authentication records and what each one proves

Three record types decide whether a receiver trusts your mail. Presence is not the goal; alignment is.

## SPF

SPF is a TXT record on the sending domain that lists the hosts and networks allowed to send mail using
that domain in the envelope sender, the address the receiving server sees during the SMTP exchange
rather than the address a human reads. A receiver checks the connecting server against this list.

A minimal record looks like this, where the include pulls in the provider's own list of sending hosts:

```
v=spf1 include:_spf.example-provider.net -all
```

The ending matters. `-all` means reject anything not listed, `~all` means treat it as soft fail. Use
`-all` once you are certain every legitimate sender is covered, because a soft fail leaves room a
spoofer can exploit. SPF has a hard limit of ten DNS lookups; chaining too many includes causes a
permanent error that fails the check, so keep the record flat and remove includes for services you no
longer use.

SPF alone proves only that an allowed host sent the mail. It says nothing about whether the body was
altered, and it breaks when mail is forwarded, because the forwarding server is not in your record.
That is why SPF is not enough on its own.

## DKIM

DKIM signs each message with a private key held by the sending system, and publishes the matching
public key in DNS at a selector you choose. A receiver fetches the public key and confirms the signed
headers and body arrived unchanged. The published record looks like this, with the selector as the
label:

```
selector1._domainkey.example.com  TXT  "v=DKIM1; k=rsa; p=MIGfMA0..."
```

Rotate keys periodically and publish a new selector before retiring the old one so no message is signed
with a key that has already been removed. DKIM survives forwarding, because the signature travels with
the message. It proves the message was signed by someone holding the key for the signing domain, which
is why the signing domain has to be yours and not the provider's shared domain if you want alignment.

## DMARC

DMARC is a TXT record at `_dmarc.example.com` that does two things: it tells receivers what to do when a
message fails authentication, and it asks them to send reports. The record ties SPF and DKIM to the
visible from address through alignment. A message passes DMARC when either SPF or DKIM passes and the
domain that passed matches the from domain.

```
_dmarc.example.com  TXT  "v=DMARC1; p=none; rua=mailto:reports@example.com; adkim=r; aspf=r"
```

The policy value `p` is the lever. `none` means take no action but send reports. `quarantine` means
treat a failing message as suspicious, usually spam. `reject` means refuse it. The alignment mode
`adkim` and `aspf` can be relaxed (`r`), where a subdomain counts as matching the parent, or
strict (`s`), where the domains have to be identical.

## Why alignment beats presence

A message can have a passing SPF and a passing DKIM and still fail DMARC. This happens when the domain
that passed is the provider's shared domain rather than your from domain. The receiver sees
authentication that does not belong to the sender the human is looking at, treats it as unaligned, and
applies your DMARC policy. Under `p=reject` the mail is dropped. Setting up a custom signing domain and
a custom envelope domain with the provider is what makes the passing result align, and alignment is the
only version that satisfies a strict receiver.

## Rolling out DMARC without dropping mail

Start at `p=none` and point `rua` at a mailbox or a report parser. Aggregate reports arrive as XML,
usually daily, one per receiver, listing how many messages each sending source sent and whether they
passed aligned SPF and DKIM. Read them until every legitimate source, including any third party that
sends on your behalf such as a support desk or an invoicing tool, passes aligned. Only then move to
`p=quarantine`, watch for a week, then `p=reject`. Skipping the report-reading phase is how a forgotten
sender gets its mail silently rejected the day you enforce.

---
name: security-hardening
description: Find and fix the security defects that actually get exploited, on systems the user owns. Use when the user asks for a security review, asks how to secure or harden their application, asks about authentication, authorisation, password storage, sessions, tokens, encryption, injection, cross site scripting, CSRF, file uploads, dependency vulnerabilities or supply chain risk, or asks whether their setup is safe. Also use before any launch that handles personal data, money or credentials. Works from a threat model rather than a generic list, ranks findings by what an attacker actually reaches, retrieves current advisories instead of recalling them, and treats broken object level authorisation as the first thing to check because it is the most common serious defect in web software. Triggers on security review, harden my app, is this secure, OWASP, SQL injection, XSS, CSRF, password hashing, JWT, session security, file upload security, dependency vulnerabilities, secrets leaked, penetration test my own app.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Security hardening

Defensive work on systems the user owns or is authorised to test. A generic checklist finds generic
problems, so start from what an attacker would actually try against this specific system.

## Scope

This skill covers the user's own systems, their own code, and systems they have written authorisation to
test. It does not help with access to systems the user does not control. If ownership is unclear, ask
before proceeding.

## Fit to the project

Read what the system is and how it is exposed before testing anything, in this order.

1. The stack and its versions: the language, the framework, the datastore, and the authentication library
   or service. The framework decides where the raw HTML bypass lives, how parameterised queries are
   written, and which session and token defaults are in play, so the review adapts to it rather than
   assuming one.
2. The entry points that actually reach the internet: public and authenticated endpoints, admin
   interfaces, webhooks, file uploads, and any debug or metrics endpoint left routed. Map who can call
   each and what it can reach before ranking anything.
3. The dependency manifest and lockfile, so the audit tool that fits the ecosystem is the one that runs,
   and so runtime dependencies are separated from development ones where the risk differs.
4. Where secrets and personal data live today: the config, the environment, the logs, and the datastore.
   A leak in a log is reached more easily than a flaw behind three controls, so knowing where the data
   sits shapes the reachability ranking.

When nothing is documented, because you are handed a running system with no notes, enumerate the routes
from the code and the deployment config first, treat everything reachable as in scope until shown
otherwise, and say which parts you could not confirm are covered.

## Non-negotiables

1. Check object level authorisation first. Changing an identifier in a request to read someone else's record is the most common serious defect in web applications, and it is usually present because the route check looked sufficient.
2. Retrieve advisories, never recall them. Use the dependency tooling and check the current [CVE data](https://nvd.nist.gov/vuln) or the ecosystem advisory database, with dates. A remembered vulnerability list is out of date.
3. Never invent a vulnerability identifier, a severity score or a compliance requirement. Cite it or mark it unverified.
4. Rank by reachability. A theoretical issue behind three controls ranks below a simple one on an exposed endpoint. Say what an attacker needs before each finding is usable.
5. If a live secret is found, that goes in the first line, and the fix includes rotation rather than only deletion. Removing a key from code leaves it in history and in whoever already copied it.
6. Fix the class, not only the instance. One unescaped output usually means the escaping approach is wrong somewhere.
7. No security theatre. Password composition rules, forced rotation and security questions make things worse. Say so rather than adding them.

## Procedure

### Step 1, threat model briefly

Ten minutes of this beats a long checklist. The method is in `references/threat-model.md`.

Name what is worth stealing, who would want it, how they reach it, and what stops them today. Then test
the things that stop them.

### Step 2, map the attack surface

Every entry point: public endpoints, authenticated endpoints, administrative interfaces, webhooks,
file uploads, background consumers reading external data, scheduled jobs, and any debug or metrics
endpoint that was left reachable.

For each, record who can call it, what it trusts, and what it can reach.

Find the forgotten ones. Old API versions still routed, a staging environment on a public address with
production data, a database port open to the world, an object storage bucket set to public, a metrics
endpoint exposing internals.

### Step 3, authorisation and authentication

For every endpoint touching user owned data, confirm ownership is checked on the object, not just the
session. Test it: as user A, request user B's resource by identifier.

Check that role checks exist on the server and are not only enforced in the interface.

Passwords stored with a current password hashing function at a sensible cost. Never a general purpose
digest, with or without a salt.

Sessions invalidated on logout, on password change, and on permission change. Rotated on privilege
change.

Tokens: signature, expiry, audience and issuer all validated, algorithm pinned so it cannot be swapped,
and lifetimes short with a refresh path. Never trust a claim the client can set.

Account recovery and multi factor enrolment paths tested, since these are the usual bypass rather than
the login form.

Rate limits on login, password reset, token refresh, and anything sending mail or costing money.

### Step 4, input and output handling

Parameterised queries everywhere, including inside any raw query escape hatch in the ORM.

No shell invocation built from user input. Where a subprocess is required, pass arguments as a list and
never through a shell.

Output escaped for the context it lands in: HTML body, attribute, JavaScript, URL and CSS each differ.
Find every use of the framework's raw HTML bypass and justify each one.

No deserialisation of untrusted data into objects.

File uploads: validate by content rather than extension, cap the size, store outside the web root or in
object storage, generate the stored filename yourself, and never trust the client supplied name or type.

Any feature fetching a URL supplied by a user is a server side request forgery risk. Allow only expected
hosts and block internal address ranges, including the cloud metadata endpoint.

Redirect targets validated against an allowed list.

Cross site request forgery protection on state changing requests, with a cookie policy that supports it.

### Step 5, data protection

Transport security everywhere, with modern settings, and no mixed content.

Encryption at rest for anything sensitive, with a key management story that permits rotation.

Least privilege on database accounts, cloud roles and API tokens. An application account that can drop
tables is an unnecessary risk.

Personal data inventory: what is collected, where it lives, who can read it, how long it is kept, and
whether deletion works. Retention with no policy grows into a liability.

Check logs, error reports and analytics payloads for personal data and secrets, which is where leaks most
often happen.

### Step 6, dependencies and supply chain

Run the ecosystem audit tool and report the real output.

```
npm audit --omit=dev ; pip-audit ; cargo audit ; govulncheck ./... ; bundle audit
```

Separate runtime from development findings, since the risk differs.

Lockfile committed and builds reproducible.

Review install scripts on new dependencies, which run with your permissions.

Pin CI actions and base images by digest, since a moving tag is a code execution path into your pipeline.

Restrict who can push to the default branch and who can publish releases.

### Step 7, verify and report

Actually try the attacks on your own system: the identifier swap, the missing authorisation, the
unescaped field, the oversized upload, the expired token.

Report using the `ship-audit` structure, ordered by reachability, each finding with what an attacker needs,
what they get, and the fix.

## Self-audit

- Object level authorisation tested by actually swapping an identifier.
- Every advisory cited with a source and a date, none recalled.
- Live secrets, if any, reported first with rotation in the fix.
- Findings ordered by reachability, each with the attacker's prerequisites.
- Fixes address the class, not only the instance.
- Audit tooling run with real output included.
- Logs and error reports checked for leakage.
- No security theatre recommended.
- Anything not reviewed is disclosed.

## When to stay off

If the user says "just execute" or "stop", check the single thing asked, such as one endpoint's
authorisation, and skip the threat model, the full surface map, and the ranked report. The off switch
stays off for the rest of the session unless the user reopens it. A review that keeps expanding its own
scope after being told to stop is not welcome.

## Honest limits

This skill finds and fixes defects on systems the user owns or is authorised to test. It does not perform
unauthorised testing, it does not certify compliance against a named standard, and it does not replace a
formal audit or a professional penetration test on a system where one is legally required. Where a
finding needs a fix written, the patch follows the `code-craft` contract so it arrives readable and
commented rather than as one dense block, and the correctness of that fix belongs to `test-strategy`. The
final ranked write-up uses the `ship-audit` structure.

Its findings are only current at the moment of the scan, because advisories change daily, so every one is
retrieved and dated rather than recalled, and a review is a snapshot rather than a guarantee. The
step-by-step threat model method is in `references/threat-model.md`, and a reachability ranking table with
worked examples of ordering findings is in `references/reachability.md`.

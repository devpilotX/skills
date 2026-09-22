---
name: auth-implement
description: Build sign-in and permission checks without the holes that get exploited first. Use when adding login, sessions or tokens, when storing passwords, when adding a second factor, when wiring social or delegated sign-in, when checking who may read or write a record, or when building password reset and account recovery. Picks server sessions or tokens by what the client is, stores credentials where each client can defend them, hashes passwords with a named algorithm family and a cost factor, rate limits without becoming a denial of service, checks object level access on every read and write, and treats recovery as the most attacked path. Triggers on add login, implement authentication, build sign in, session vs JWT, where to store the token, hash passwords, add MFA, add two factor, social login, OAuth login, OIDC, password reset, forgot password, account recovery, check permissions, who can access this, refresh tokens, log out everywhere.
license: MIT
compatibility: Any language, framework, and client type. The example flows are protocol level and map to any auth library. No single vendor is required.
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Auth implement

Login code usually runs on the first try and fails the first attacker. The route check looks
sufficient while it only verifies a session exists, never that the session owns the record it is
reading. A token is validated for its signature and nothing else. Passwords land in a general purpose
digest. Each of these is the default path a model reaches for, and each is a known way in.

This skill builds the parts that stop those attacks. It produces code, so follow the `code-craft`
contract for how that code is organised and commented.

## Fit to the project

Read what the project already decided before adding a second scheme next to it.

1. Find the existing auth: a session middleware, a token library, an identity provider config, or a
   framework's built in user model. One working scheme beats two half schemes, so extend what is
   there unless it is broken.
2. Identify every client type that signs in: a server rendered site, a single page app in a browser,
   a native mobile app, a command line tool, a service calling another service. The client decides
   session versus token and where a credential can live, so name them before choosing.
3. Read the data model for ownership. Find the column or relationship that ties a record to the user
   who may see it. If there is none, object level authorisation cannot be enforced and that is the
   first thing to fix.
4. Check for an identity provider already in use. If the organisation has single sign-on, adding a
   local password store is usually the wrong direction. Delegate instead.

## Non-negotiables

1. Check object level authorisation on every read and every write. Verify the logged in user owns or
   may access the specific record, not merely that a session exists. Changing an identifier in a
   request to fetch another user's record is the most common serious defect in web software, and it
   is present because the route check looked enough.
2. Store passwords with a memory hard or deliberately slow hashing function built for passwords:
   Argon2id, scrypt, or bcrypt, with a cost factor tuned so one hash takes a noticeable fraction of a
   second on your hardware. A general purpose digest such as SHA-256, salted or not, is crackable at
   billions of guesses per second and counts as storing them in the clear.
3. Invalidate sessions everywhere on password change and on any credential reset. A stolen session
   that survives the victim changing their password defeats the reason they changed it.
4. Validate every part of a delegated token, not just the signature. Check the issuer, the audience,
   the expiry, and pin the signing algorithm so it cannot be swapped to none or to a symmetric key you
   did not intend. A token accepted on signature alone lets an attacker present one minted for a
   different application.
5. Rate limit login, password reset, token refresh, and second factor entry per account and per
   source, and make the limit fail closed for the attacker without locking the real user out
   permanently. A hard permanent lockout on failed attempts is a denial of service anyone can trigger
   with a victim's email address.
6. Never trust a claim the client can set. A role, a price, a user id, or an entitlement that arrives
   in a request, a cookie, or an editable token is attacker input until the server rechecks it.

## Procedure

### Step 1, pick session or token by the client

Decide by what the client can defend, not by fashion.

For a browser talking to your own server, prefer a server side session with an opaque cookie marked
HttpOnly, Secure, and SameSite. The browser cannot read an HttpOnly cookie from script, so a cross
site scripting bug cannot steal it directly. This is the safest default for a first party web app.

For a native mobile app or a command line tool, a token is normal because there is no cookie jar.
Store it in the platform secret store: the keychain on one mobile platform, the keystore on the other,
the OS credential manager on a desktop. Never in plain application storage.

For one service calling another, use short lived tokens issued by an identity provider or a signed
client credential, never a long lived static secret checked into anything.

Details of where each client may keep a credential and why are in
`references/credential-storage.md`.

### Step 2, store passwords correctly or delegate

If the project holds passwords, hash with Argon2id where the library exists, scrypt or bcrypt
otherwise. Set the cost so a single verification takes a meaningful fraction of a second on production
hardware, and record the parameters so you can raise them later. Verify on login and, when the stored
cost is below current policy, rehash transparently.

Check new and reset passwords against a known breached password set rather than imposing composition
rules. Length with a breach check beats mandatory symbols, which push people toward predictable
substitutions.

If an identity provider is available, delegate sign-in and skip the password store entirely. The token
validation you then owe is in Step 4.

### Step 3, enforce authorisation on the object

Write the check as: this user may perform this action on this specific object. Put it in one place the
request cannot bypass, and call it on reads as well as writes. A list endpoint filters by owner in the
query rather than fetching all rows and hiding some in the response.

Enforce role checks on the server. A hidden button in the interface is not a control. Test the check
by requesting another user's record by its identifier while signed in as someone with no right to it,
and confirm the server refuses.

Map the privilege escalation paths: an endpoint that lets a user grant themselves a role, a mass
assignment that lets a request set an is_admin field, an admin API reachable without an admin check.
The escalation catalogue is in `references/authorization-patterns.md`.

### Step 4, validate delegated sign-in fully

For OpenID Connect or OAuth 2.0, use the authorization code flow with PKCE for public clients. On the
token, verify the signature against the provider's published keys, then verify the issuer matches the
provider you configured, the audience matches your client, the token has not expired, and the nonce
matches the one you sent. Pin the expected signing algorithm.

Never accept an ID token or access token whose algorithm header you did not expect, and never accept
one where the algorithm is none. Treat the userinfo you receive as identity only after these checks
pass.

### Step 5, add a second factor ranked by real protection

Offer factors in order of the protection they actually give. A hardware security key or platform
passkey using WebAuthn resists phishing because the credential is bound to the origin. A time based
one time code from an authenticator app is next. A code sent by SMS is the weakest common option
because of SIM swap and interception, so treat it as a fallback rather than the default. The ranking
and the enrolment attacks are in `references/authorization-patterns.md`.

Protect the enrolment and recovery of the second factor as carefully as the login, because that is
where the bypass usually is.

### Step 6, build recovery as the most attacked path

Account recovery is where attackers go when the login is solid, so build it last and hardest. Send a
reset link with a single use, short lived, high entropy token tied to the account, and invalidate it
on use and on a new request. Do not reveal whether an email address has an account. Rate limit reset
requests per account and per source. On a successful reset, invalidate all existing sessions and
require the second factor if one is enrolled.

Avoid security questions. Their answers are frequently public, so they lower the bar rather than
raising it.

## Self-audit

- Does every read and write check that the user owns or may access the specific object, verified by
  actually swapping an identifier in a request?
- Are passwords stored with Argon2id, scrypt, or bcrypt at a tuned cost, and never a general purpose
  digest?
- Does a password change or reset invalidate every existing session for that account?
- Are delegated tokens checked for issuer, audience, expiry, and a pinned algorithm, not signature
  alone?
- Do login, reset, refresh, and second factor entry have rate limits that do not permanently lock a
  real user out?
- Is the credential stored in the right place for each client type: HttpOnly cookie for a first party
  browser app, platform secret store for native clients?
- Is every role, price, and identifier from the request rechecked on the server rather than trusted?
- Does account recovery avoid revealing whether an email has an account, and invalidate sessions on
  reset?

## Honest limits

This skill builds authentication and authorisation. It does not perform a full security review of the
surrounding system: input handling, output escaping, dependency advisories, and transport security
belong to `security-hardening`, which also owns the threat model that decides which of these matters
most here.

The cost factors and the factor ranking are current rules of thumb, not fixed constants. Retune the
hashing cost as hardware improves, and confirm library defaults against the library's own current
guidance rather than these numbers alone. This skill does not choose or operate an identity provider;
selecting one is an architecture decision that `arch-decide` covers.

## Off switch

If the user says "stop", "just execute", or "skip the auth review", stand down and make only the
change asked for. The off switch stays in effect for the rest of the session unless the user invokes
the skill again. A skill that keeps forcing checks after being declined gets the whole collection
uninstalled.

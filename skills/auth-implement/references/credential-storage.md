# Credential storage by client type

Where a credential can live is decided by what the client can defend, not by convenience. The same
token is safe in one place and stolen from another.

## First party browser app

Prefer an opaque server side session identifier in a cookie. The cookie carries three flags. HttpOnly
keeps script from reading it, so a cross site scripting bug cannot exfiltrate it in one line. Secure
keeps it off plaintext connections. SameSite (Lax or Strict) limits when the browser attaches it to
cross origin requests, which blunts cross site request forgery.

Do not put a token in localStorage or sessionStorage. Both are readable by any script on the page, so
one injected script reads the token and the HttpOnly protection you could have had is gone. This is
the single most common browser storage mistake.

If the app is a single page app talking to an API on another origin, either put the API behind the
same site with a cookie, or accept that a token in memory (a JavaScript variable, never persisted)
is the tradeoff, cleared on reload and refreshed from an HttpOnly refresh cookie.

## Native mobile app

There is no cookie jar, so a token is normal. Store it in the platform secret store rather than in
application preferences or a file. On one mobile platform that is the keychain; on the other it is the
keystore backed store. These are encrypted at rest and gated by the device unlock.

Bind the refresh token to the device where the platform supports it, so a copied token off one device
does not work on another.

## Command line tool

Use the operating system credential manager where one exists. Where none does, a file with permissions
locked to the user is the fallback, and the file holds a short lived token rather than a password.
Never print a token to standard output where it lands in shell history or a log.

## Service to service

No human, no browser, no interactive login. Use short lived tokens issued by an identity provider
through the client credentials flow, or a signed assertion using a private key the calling service
holds. A long lived static shared secret checked into configuration is the pattern to avoid, because
it never rotates and it leaks through logs and images.

## Token lifetime as a control

A short access token lifetime limits the damage of a stolen token to the window before it expires. A
common shape is an access token measured in minutes and a refresh token measured in days, with the
refresh token stored more carefully than the access token because it is the higher value item.

Revocation matters because expiry alone is not enough on a logout or a compromise. For opaque server
side sessions, revocation is deleting the server record. For self contained tokens, keep a short
denylist of revoked token identifiers until they expire, or keep lifetimes short enough that the
window is acceptable.

## What never goes in a client

The password itself after login. The server side signing key. Another user's token. A long lived
credential that grants more than the client needs. When in doubt, give the client the least it can
function with and the shortest lifetime it can tolerate.

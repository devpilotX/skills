# Authorization patterns and escalation paths

Authentication proves who someone is. Authorisation decides what they may do. Most breaches of user
data are authorisation failures, not authentication failures, so this is where the attention goes.

## The check that has to exist

For every action, the question is whether this user may perform this action on this specific object.
Answer all three parts. A check that confirms the user is logged in answers only the first part and
lets any logged in user read any record by guessing its identifier.

Enforce the check in one place the request path cannot skip. A middleware, a policy layer, or a guard
that every handler goes through beats a check copied into each handler, because the copy that gets
forgotten is the hole.

## Reads matter as much as writes

Write checks are usually present because losing data feels dangerous. Read checks are skipped because
reading feels harmless. It is not. Reading another user's record is a data breach. Check ownership on
list endpoints by filtering in the query, on detail endpoints by verifying ownership after fetch, and
on any embedded object in a response.

## Broken object level access, tested

The test is direct. Sign in as user A. Take a record that belongs to user B and note its identifier.
Request it as user A by that identifier, through every route that touches it: the detail view, the
edit form, the delete, the export, the API. A correct system refuses every one. A system that refuses
the edit but returns the detail has a read hole.

Sequential or guessable identifiers make this trivial for an attacker. Opaque identifiers raise the
effort but are not a substitute for the check, because identifiers leak through referrers, logs, and
shared links.

## Privilege escalation paths to close

Mass assignment. A create or update endpoint that binds the whole request body to a model lets an
attacker set a field you never put on the form, such as a role or an is_admin flag. Bind only the
fields the action is meant to change.

Self service role change. An endpoint that lets a user set their own role or group is escalation by
design unless it is gated by an existing higher privilege.

Missing check on the admin surface. An admin API or page that relies on the admin link being hidden
rather than on a server side role check. Hidden is not protected.

Horizontal to vertical. A user who can edit their own profile can sometimes edit an admin's profile
through the same endpoint if ownership is not checked, which turns equal access into higher access.

Trusting a token claim. A role or entitlement carried in a client readable or editable token, trusted
without a server side recheck against the current state.

## Second factor ranked by real protection

A hardware security key or a platform passkey using WebAuthn resists phishing, because the credential
is bound to the origin and the browser will not release it to a lookalike domain. This is the
strongest common factor.

A time based one time password from an authenticator app is next. It is not phishing resistant, since
a user can be tricked into typing the code into a fake site in real time, but it defeats password
reuse and credential stuffing.

A push approval prompt is roughly as strong as the one time code and adds a fatigue risk: repeated
prompts can wear a user into approving one. Add number matching where the platform supports it.

A code sent by SMS is the weakest common factor because of SIM swap and network interception. Use it
as a fallback, not the default, and never as the only factor for a high value account.

## Enrolment and recovery are the bypass

An attacker who cannot beat the second factor attacks its enrolment and its recovery. Require the
current factor to enrol a new one. On recovery of a lost factor, require identity proof at least as
strong as the factor being replaced, and invalidate active sessions. A recovery flow that emails a
bypass code with no other check makes the second factor decorative.

# Threat modelling in ten minutes

A short model beats a long checklist, because it tells you which checklist items matter here.

## Four questions

What is worth taking? List the assets concretely. Customer records, payment credentials, session tokens,
source code, the ability to send mail from your domain, compute for mining, and the reputation cost of
defacement. Be specific, because "our data" does not guide any decision.

Who would take it, and why? The realistic set for most products is opportunistic automated scanning,
credential stuffing against your login, a customer trying to see another customer's data, a disgruntled
insider, and a targeted attacker only if what you hold is valuable enough. Design for the first three
first, because they are constant.

How would they reach it? Walk the path from the internet to the asset. Every hop is a control that either
exists or does not.

What stops them today? For each path, name the control. Where the answer is "nobody would think to try
that", there is no control.

## Trust boundaries

Draw the lines where data crosses from less trusted to more trusted. Each line needs validation.

Browser to server. Everything from the client is attacker controlled, including headers, cookies, hidden
fields and anything the interface disabled.

Server to database. The query is trusted, so injection here converts a boundary failure into total access.

Your service to a third party. Their response is not trusted either, and a compromised or wrong upstream
can feed you bad data.

Third party into your service, meaning webhooks. Verify the signature, or anyone can post to that
endpoint.

Job queue into a consumer. Messages may be replayed or crafted if the queue is reachable.

Build pipeline into production. A dependency or action is code execution with your deploy permissions.

Between tenants in a shared system. This boundary exists in code only, which is why it fails most often.

## Per feature questions

Run these against whatever is being built, since they catch specific defects rather than general ones.

Who is allowed to do this, and where is that checked? If the answer is the interface, it is not checked.

What happens if this is called twice at once, or a hundred times in a second?

What does this trust from the request that it should verify instead? Identifiers, prices, quantities,
roles, email addresses and flags are the usual ones.

What does this expose in the response that the caller should not see? Internal identifiers, other users'
data in an embedded object, stack traces, and field level detail the caller is not entitled to.

What gets logged here, and should it be?

If this fails halfway, what state is left behind?

Can a user reach another user's resource by changing one value?

## Ranking findings

Reachability first. Anonymous and remote outranks authenticated. Authenticated outranks requiring
administrative access. Requiring physical access or an existing compromise ranks last.

Then impact. Total data exposure, money movement and remote code execution sit above single record
exposure, which sits above information disclosure.

Then how easy it is. A single altered request outranks something needing a race window or a specific
timing.

Ranking by how interesting a finding is, rather than by reachability, produces reports that get ignored.

## Controls that earn their cost

Object level authorisation checks, enforced somewhere that cannot be forgotten.

Parameterised queries as the only way to reach the database.

Output escaping by default, with bypasses individually justified.

Short lived scoped tokens.

Rate limits on authentication and anything expensive.

A current password hashing function with a sensible cost.

Dependency audits in the pipeline, blocking on high severity.

Least privilege on every credential the application holds.

Logging that shows who did what, without recording secrets.

## Controls that do not

Password composition rules, which push people toward predictable substitutions. Length and a breach check
work better.

Forced periodic rotation with no evidence of compromise, which produces incremented passwords.

Security questions, whose answers are frequently public.

Hiding an endpoint rather than protecting it.

Client side validation treated as a control.

Custom cryptography.

An allowed list of user agents or the absence of a public link, treated as access control.

Secret detection in the pipeline with nobody acting on the results.

# Adding a package and license obligations

Adding a dependency is a decision with a security cost, a maintenance cost, and sometimes a legal
obligation. Run these checks before the package touches the manifest, not after.

## Check the name

Typosquatting is a real and cheap attack: publish a package one character off a popular name and wait
for a fat finger or a model that hallucinated the name. Before adding, confirm the exact spelling
against the package the documentation or the ecosystem points to, not against memory. Watch for a
transposed letter, a hyphen where the real one has a plain separator, a singular where the real one is
plural, and a lookalike namespace or scope.

Be extra careful with a name a language model suggested, because models sometimes invent
plausible package names that do not exist or that a squatter has since registered to catch exactly
that mistake.

## Check that it is maintained

An unmaintained package is a liability the day an advisory lands with no one to patch it. Look for a
release within a reasonable window rather than years ago, an issue tracker where maintainers respond,
and more than a single maintainer where the ecosystem exposes that. A single maintainer is not
disqualifying, but it is a single point of failure worth noting for anything load bearing.

Download count is weak evidence on its own, because a squatter can inflate it and a good niche package
can be low. Use it alongside the other signals, not instead of them.

## Check that it is needed

The cheapest dependency is the one you did not add. For a few lines of well understood logic, writing
it is often safer than pulling a package and its transitive tree. Weigh the size of the tree the
package drags in against the size of the problem it solves. A large dependency for one small helper is
a bad trade.

## Review install scripts

Many ecosystems let a package run a script on install. That script runs arbitrary code with your
permissions immediately, before you have run a line of the package's actual code. For a new or unknown
package, inspect whether it declares install hooks, and where the ecosystem allows it, install with
scripts disabled first and review before enabling. Never let an unreviewed package's install hook run
on a machine holding credentials or in a release pipeline.

## License obligations that bite at distribution

A license question is easy to ignore until you distribute, then it is expensive. The obligations that
matter depend on whether you ship the software to others or run it as a hosted service.

Permissive licenses such as MIT, BSD, and Apache 2.0 generally allow use with attribution and few
other conditions. Apache 2.0 additionally includes a patent grant and a notice requirement.

Copyleft licenses such as the GPL family can require that software you distribute which incorporates
the dependency be released under the same license, meaning your own source. The strong copyleft
licenses reach further than the weak ones such as LGPL or MPL, which are usually limited to the
licensed component itself.

A network copyleft license such as AGPL can trigger the source obligation even when you only offer the
software as a network service rather than distributing a binary, which catches teams who assumed a
hosted service was exempt.

A dependency with no license at all is not free to use; absent a license, default copyright applies
and you have no grant. Treat an unlicensed package as unusable until clarified.

None of this is legal advice. Flag a real obligation and, for anything load bearing at distribution,
route the question to a lawyer rather than guessing.

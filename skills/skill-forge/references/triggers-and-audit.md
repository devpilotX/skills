# Trigger phrases and the audit that fits them

The description decides whether a skill ever activates, and the self-audit decides whether it delivered. Both fail in the same way: written in the author's vocabulary instead of the reader's. This is how to write them in the right register.

## Why triggers are written last

Written first, a trigger list describes the skill you hoped to build. Written last, it describes the one you built. The order matters because the skill's real job usually narrows during the writing, and a description fixed early keeps advertising the wider job the file no longer does.

## The register that activates

A skill activates when the phrases in its description match what a user actually types. Users type symptoms and requests, not the technical name of the cause.

Someone whose page is slow types "site is slow" or "why is this taking so long", not "latency percentile regression". Someone whose skill scores nine types "my skill wont pass" or "stuck at nine", not "criterion coverage gap". Collect the phrases by imagining the person with the problem at the moment they reach for help, before they know the cause. That moment is when the skill has to fire.

Write at least ten phrases, comma separated, after the words "Triggers on". Include the blunt complaint, the direct request, and the technical term for the reader who does know it, so the skill activates across the range of how people ask. The scorer counts the phrases and the count is a floor, not a target; a real spread of phrasings matters more than the number.

## Common trigger mistakes

All ten phrases in one register, usually the engineer's, so the skill misses everyone who describes the symptom instead of the cause.

Phrases that are near-synonyms of each other rather than different ways in. Ten words for the same request cover less ground than five requests and five symptoms.

The word "Use when" missing, or fewer than ten phrases after "Triggers on". The scorer fails both, so check the exact wording.

A description under 200 or over 1024 characters, or spread across more than one line. The specification requires one line in that range, and the scorer measures it.

## Writing the self-audit

Each audit item is a question answerable yes or no by looking at the output. The test is whether two people checking the same output would give the same answer. "Is the code clean" fails, because clean is a matter of taste. "Is every function within its length budget" passes, because the budget is a number and the lengths are countable.

Write the audit from the non-negotiables. Each non-negotiable is a rule; each audit item asks whether the rule held. That pairing keeps the audit honest, because it checks the things the skill said mattered rather than a fresh list of nice properties.

At least six items, each a yes-or-no check. An audit of vague affirmations is worse than none, because it reads as coverage while checking nothing.

## Reusing an existing skill's shape

The fastest way to a passing structure is to open a skill that already scores ten, keep its headings and their order, and replace the content. The headings are spelled exactly the way the scorer expects, so copying them removes a class of failure before it happens. Pick one that emits code and one that does not, so you have both shapes to hand.

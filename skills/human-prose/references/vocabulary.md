<!-- lint-exempt: vocab,vocab-density,copula-avoidance,significance-padding,participle-tail -->
# Vocabulary

This file has to quote the words it tells you to avoid, so it declares linter exemptions on the line
above. Every lint report prints the exemptions a file claims, so nothing hides.

Frequency studies of text published after 2022 found a set of words rising sharply against their own
earlier baseline. The useful part is not that the words are bad. The useful part is that they cluster:
one is coincidence, six in a page is a fingerprint, because these words co-occur in model output far
more often than in writing by a person who chose each one.

## Read this literally

A word being overused by a model does not implicate its synonyms. `delve` is a marker; `dig`, `probe`
and `examine` are not. Swapping a flagged word for a longer synonym changes nothing, because the
problem was never the word. The problem is that the sentence made an evaluative claim instead of
stating a fact, and the word was the easiest way to do that.

Context decides. `underscore` is a marker in its figurative sense and an ordinary noun when it means the
character or incidental music. `landscape` is a marker when it means a field of activity and ordinary
when it means terrain. `tapestry` is a marker as a metaphor and ordinary as woven cloth. Do not flag a
literal use.

## Tier one, never in the evaluative sense

delve, showcase, underscore (as a verb), tapestry, testament, landscape (abstract), realm, interplay,
intricate, pivotal, crucial, vital, meticulous, garner, foster, bolster, boast, myriad, plethora,
seamless, holistic, multifaceted, nuanced (as praise), profound, vibrant, groundbreaking,
revolutionary, cutting-edge, transformative, unparalleled, indelible, enduring, resonate, leverage (as
a verb), utilize, navigate (figurative), unpack, shed light on, deep dive, at its core, at the heart
of, nestled, in today's world, in an era of, plays a key role, it is important to note, worth noting,
valuable insights.

## Tier two, at most rarely and only when precise

highlight, emphasize, enhance, robust, comprehensive, significant, key (as an adjective), notable,
renowned, diverse, rich, complex, dynamic, framework, ecosystem (non-biological), cornerstone,
hallmark, turning point, Additionally, Moreover, Furthermore, Notably, Ultimately, reflects.

Budget: zero tier one, and under three tier two per thousand words.

## Replacements that actually work

Each row replaces an evaluative verb with the fact it was standing in for. The point is the right
column, not a synonym.

| Instead of | Write the fact |
|---|---|
| played a pivotal role in | did the specific thing, with a date |
| underscores the importance of | the number, the consequence, or nothing |
| a testament to their dedication | the hours, the cost, or the years |
| delve into the intricacies of | explain the part that is actually hard |
| seamless integration | it connects over one API call, or it does not |
| robust and scalable | the load it held and where it broke |
| leverage our expertise | what you did before, for whom |
| navigate the complex landscape of | the two rules that conflict |
| a myriad of options | the four options, named |
| foster collaboration | who talked to whom, and when |
| serves as a reminder that | delete the sentence |

## The words drift by model generation

Overuse is not stable over time, which matters when you are dating a piece of text rather than only
cleaning it. Treat these groupings as rough, not as cutoffs.

Text from roughly 2023 to mid 2024 clusters around Additionally, boasts, bolstered, crucial, delve,
emphasizing, enduring, garner, intricate, interplay, key, landscape, meticulous, pivotal, underscore,
tapestry, testament, valuable, vibrant.

Text from roughly mid 2024 to mid 2025 drops delve sharply and clusters around align with, bolstered,
crucial, emphasizing, enhance, enduring, fostering, highlighting, pivotal, showcasing, underscore,
vibrant.

Text from roughly mid 2025 onwards narrows further, to emphasizing, enhance, highlighting and
showcasing, with more weight carried by claims about how notable or well covered a subject is than by
single words.

So a page thick with `delve` and `tapestry` reads as older output, and a page with no tier one words but
a participial tail on every paragraph reads as newer. Neither is proof of anything on its own.

## Model specific habits

Output from Grok skews toward words that sound empirical without doing empirical work: causal,
empirical, correlate, holdouts. It has kept overusing underscore after other models moved on.

Fiction prompts collapse toward a small set of defaults: the name Elara, whispering woods, the smell of
ozone, a distant dog barking, a mix of X and Y, and a character releasing a breath they did not know
they were holding.

## What the shipped detector covers

`scripts/ai_tells.py` checks a deliberately conservative subset of the lists above. Words like `key`
and `enduring` are left out because they are too common in ordinary writing to flag without producing
more noise than signal, which would teach a reader to ignore the report. The detector is a smoke alarm
for the unambiguous cases. This file is the reference for the judgement calls it cannot make.

Derived from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
CC BY-SA 4.0. Observations were reorganised and rewritten as generative rules; the wording here is
original.

<!-- lint-exempt: vocab,vocab-density,chatter,placeholder,artifact,significance-padding,section-summary,negative-parallelism,copula-avoidance,cutoff-disclaimer,x-and-y-heading,vague-attribution -->
# House style

This file enumerates the patterns it bans, so it declares per-rule exemptions from the linter on the
line above. Only files whose job is to document the patterns carry exemptions, and the lint report
prints every one of them so that nothing hides.

Every file in this repository follows these rules, and `tools/validate_skills.py` enforces the
mechanical ones on every commit. The point is that content produced by or with these skills should
not carry the stylistic residue that marks machine-written text.

The rules come from [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
an advice page from WikiProject AI Cleanup, plus the linguistic studies it cites. That page is
released under CC BY-SA 4.0. Observations from it were paraphrased and condensed here rather than
copied.

Read the caveat first, because it matters more than the rules: humans are bad at telling machine
text from human text, and automated detectors have error rates high enough that Wikipedia tells
editors not to rely on them. One 2025 study found untrained human judgement performed at about the
level of chance. So these rules do not make text "undetectable" and this repository does not claim
they do. They make text read better, which is a different and more achievable goal.

## Punctuation

No em dashes (U+2014). Use a comma, a colon, parentheses, or a second sentence. Em dashes are the
most widely known tell, and models overuse them in places where most writers would reach for
something else.

No en dashes (U+2013) as sentence punctuation. They are fine inside numeric ranges such as 1939-1945
if you write them as plain hyphens, which is what this repo does.

Straight quotes and straight apostrophes only. ASCII `'` and `"`. Curly quotes are the default output
of several chatbots and of word processors with smart quotes turned on.

No emoji anywhere, including headings and bullet lists.

No horizontal rules between sections. A line of three hyphens is Markdown for a thematic break and
appears in machine output far more often than in hand written documents. Section headings already
separate sections.

## Headings

Sentence case. "House style", not "House Style". Title case in headings is one of the more reliable
signals, because most people do not bother to capitalise every word.

Do not write a heading whose only content is more headings. Every section says something.

Do not put the document title in the body if the filename or context already carries it.

Avoid the "X and Y" heading shape when one noun would do. "Awards and recognition" is close to a
signature.

## Vocabulary

The following words are either banned in this repo or capped at rare use. Two frequency analyses
motivate the list: an excess vocabulary study of biomedical abstracts
([Kobak et al., Science Advances 2025](https://doi.org/10.1126/sciadv.adt3813)) and work on why
certain terms became overrepresented after alignment training
([Juzek and Ward, arXiv 2412.11385](https://arxiv.org/abs/2412.11385)).

delve, underscore (figurative), tapestry (figurative), testament, showcase, pivotal, crucial,
landscape (figurative), realm, robust, seamless, boasts (meaning has), vibrant, intricate,
meticulous, foster, garner, bolster, align with, enhance, leverage (as a verb), utilize, holistic,
myriad, plethora, navigate (figurative), unlock (figurative), embark, harness, profound,
groundbreaking, renowned, nestled, ever-evolving, valuable insights, key takeaways.

Also avoid "Additionally" as a sentence opener, and "It is important to note that" in any form.

Prefer the plain word. Wrote, not authored. Used, not utilized. Moved, not relocated. Tried, not
attempted. Died, not passed away. Has, not features or offers or boasts.

## Sentence construction

Use plain copulas. "The script is a validator" beats "The script serves as a validator". One
analysis of academic writing measured a drop of over ten percent in the frequency of is and are in
2023, with no comparable movement before that
([Geng and Trotta, arXiv 2404.08627](https://arxiv.org/abs/2404.08627)), because models reach for
serves as, stands as, represents, functions as, and marks instead. A broader comparison of
grammatical and rhetorical style between human and model text reports the same direction
([Reinhart et al., PNAS 2025](https://doi.org/10.1073/pnas.2422455122)).

State relationships directly. "Jane ran engineering at ExampleCorp from 2019" beats "Jane was
associated with engineering leadership at ExampleCorp".

Avoid negative parallelism as a reflex. "Not just X, but Y", "It is not X, it is Y", and "Y rather
than X" are all fine once in a long document and become a signature when repeated.

Avoid the rule of three when only two things are true. Three adjectives or three parallel clauses,
used as a rhythm rather than because there are three items, is a strong tell.

Vary sentence length deliberately. Some short. Some long enough to carry a qualification that the
short ones cannot.

Repeat a word when it is the right word. Synonym rotation to avoid repetition reads as machine
output, and Wikipedia has a whole essay on why elegant variation hurts clarity.

## Content patterns

No significance padding. Do not tell the reader that something reflects a broader trend, marks a
turning point, or leaves a lasting mark, unless a cited source says so.

No closing summary that restates what the document just said. Stop when the content stops.

No "Challenges" section that opens with "Despite its strengths" and closes with vague optimism.

No promotional register. This applies to README files in particular, where the pull toward press
release language is strongest.

No vague attribution. "Experts argue" and "industry reports suggest" without a citation are weasel
wording. Name the source or drop the claim.

No participle tails. Ending a sentence with a dangling "-ing" clause that adds commentary rather
than fact, as in "reducing costs and improving outcomes", is a habit worth breaking.

## Formatting

Keep bold rare. Bolding an inline header on every bullet of a list is a recognisable machine
pattern. Where a list needs labels, plain text labels are enough.

Prefer prose to a bulleted list when the items are sentences that relate to each other.

Do not build a small table for two facts that a sentence carries better.

No placeholder text left behind. No "[insert name here]", no "2025-xx-xx" dates, no "add if
available" comments.

No text addressed to the operator. No "Would you like me to expand this?", no "I hope this helps",
no assurances that the document complies with the guidelines it was written against.

## Citations

Every external claim gets a real link that resolves. Check it. Fabricated or broken citations are
the single most damaging failure in this category, and invalid DOIs and ISBNs are a known
fingerprint.

Cite the specific page or section for anything book length.

Do not leave tracking parameters such as `utm_source=chatgpt.com` on a URL. They identify the tool
that fetched the page and they are noise.

## What the checks enforce

`tools/validate_skills.py` fails the build on em dashes, curly quotes, emoji, thematic breaks,
title case headings, banned vocabulary over threshold, tracking parameters, known chatbot markup
artifacts such as `oaicite` and `turn0search`, trailing whitespace, missing final newline, broken
internal references, and any frontmatter that violates the skill specification.

`tools/score_skills.py` scores every skill against the ten criteria in RUBRIC.md and fails below ten.
Its tenth criterion runs this style detector over every Markdown file in the skill, so a style finding
costs a rubric point as well as failing the validator.

`skills/code-craft/scripts/structure_scan.py` applies the same discipline to code: file length,
function length, nesting depth and parameter count, measured against the budgets in
`skills/code-craft/references/budgets.md`.

A file that has to enumerate the banned patterns declares per rule exemptions in an HTML comment near
the top, and every lint report prints them. Two files in this repository carry one: this style guide,
and the comment policy in `code-craft`, which has to quote the leftover work markers it tells you to
delete. Nothing else opts out of anything.

## Honest limits

A style guide cannot make generated text human. It removes the residue, not the origin. If you are
in a setting where authorship must be disclosed, such as academic submission, journalism, or
Wikipedia itself, disclose it. Wikipedia treats undisclosed machine generated content as a policy
problem regardless of how clean the prose is, and passing a style check is not permission to skip
that.

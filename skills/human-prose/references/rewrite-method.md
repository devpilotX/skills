<!-- lint-exempt: vocab,copula-avoidance -->
# Rewrite method

How to work on text you did not write.

## Diagnose before editing

Run the detector first and read the report, then read the text yourself. The two findings lists
rarely match, and the gap is informative.

Decide which of three problems you have, because they need different work.

Surface residue. The content is fine and the prose carries the accent. Mechanical fixes handle it,
and this is the fast case.

Hollow content. The sentences are grammatical and say nothing. No amount of word swapping helps,
because the fix is adding facts the text does not contain. Say so rather than polishing emptiness.

Wrong claims. The text asserts things that are false or unsourced. Fix the facts first. Cleaning the
style of a wrong document makes it more persuasive and more harmful.

## Preserving voice

If the user has other writing, read two or three samples before touching anything. Note the things
they do that a generic editor would flatten.

Do they use contractions? Long sentences or short? First person? Lists or prose? Jokes? Regional
spelling? Profanity? Sentence fragments for emphasis?

Then make the edited text match those habits, including the ones that are technically sloppy. A
consistent quirk is stronger evidence of a human author than clean prose is.

When no sample exists, ask for one, or ask two questions about audience and register. Do not invent a
voice and do not default to the neutral one, which is the accent being removed.

## Mechanical pass, in order

Work through these in sequence. Later steps depend on earlier ones.

1. Strip high severity artifacts. Leaked markup, tracking parameters, placeholders, operator chatter, cutoff disclaimers. No judgement needed, they all go.
2. Verify every citation. Open each link. Check that DOIs resolve to the right paper and that ISBNs pass their checksum. Delete or replace anything that fails, and never leave a plausible looking broken reference in place.
3. Fix punctuation. Em dashes out, curly quotes to straight, emoji out, horizontal rules out.
4. Fix headings. Sentence case. Merge headings that contain nothing but other headings. Rename "X and Y" headings where one noun works.
5. Replace copula avoidance with is and has.
6. Cut significance padding and participle tails. These usually delete cleanly with no replacement needed, which tells you they carried no information.
7. Fix attribution. Name the source or cut the claim.
8. Reduce overrepresented vocabulary. Replace with the plain word, not with another fancy word.
9. Vary sentence length. Read for rhythm and break the pattern where every sentence has the same shape.
10. Add specificity. The last and most important step, covered below.

## Adding specificity

This is what separates a rewrite from a paraphrase, and it is the step that cannot be automated.

For each vague sentence, ask what fact would make this checkable. Then either get the fact from the
user or mark it for them to fill.

"Significant cost savings" becomes "cut the monthly bill from 4,100 to 2,600".

"Extensive experience in the field" becomes "eleven years, six of them at a competitor".

"Users love the new design" becomes "support tickets about the old navigation dropped by half".

"A range of features" becomes the two features people actually use.

When the user cannot supply the fact, cut the sentence. A shorter honest document beats a longer vague
one, and vagueness is the accent you are trying to remove.

## Marking what you could not fix

Do not silently paper over gaps. Hand back a short list of the places where a fact is needed, phrased
as questions the author can answer in a sentence each. Three good questions get better results than a
polished draft built on guesses.

## Checking the result

Run the detector at `--strict`. Then apply three reads that the script cannot do.

The swap read. Would any sentence be equally true of a competitor, a different city, a different
product? If yes, it says nothing.

The aloud read. Where you run out of breath, split it. Where it sounds like marketing, cut the
adjective.

The stranger read. Would someone who knows this subject learn anything? If not, the problem was never
the style.

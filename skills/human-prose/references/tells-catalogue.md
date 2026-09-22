<!-- lint-exempt: vocab,vocab-density,chatter,placeholder,artifact,significance-padding,vague-attribution,section-summary,negative-parallelism,copula-avoidance,cutoff-disclaimer,x-and-y-heading,title-case-heading,bold-label-list,participle-tail,rule-of-three,em-dash,curly-quote -->
# Catalogue of tells

This file enumerates the patterns it describes, so it declares broad linter exemptions. Every
exemption appears in the lint report.

The catalogue condenses [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing),
an advice page maintained by WikiProject AI Cleanup and licensed CC BY-SA 4.0, together with the
research it cites. Observations were paraphrased and reorganised rather than copied. Follow the link
for the original, which has example diffs from real articles.

Read the limits in `../SKILL.md` first. None of these patterns proves machine authorship on its own.
They cluster, and the cluster is the signal.

## Why the patterns exist

A model predicts the most likely continuation, so output drifts toward the centre of its training
distribution. The practical effect is a trade of specificity for generality. A precise fact such as
"held the patent on the first automatic coupler" becomes a vague elevation such as "a transformative
figure in industrial history". The subject gets less specific and more praised at the same time.

That single mechanism explains most of what follows.

## Content level

Significance inflation. Statements that an ordinary detail reflects a broader trend, marks a turning
point, or leaves a lasting legacy. Watch for stands as, serves as, is a testament to, plays a vital
role, underscores its importance, setting the stage for, indelible mark, deeply rooted.

Notability assertion. Text that argues the subject deserves attention by listing the kinds of outlets
that covered it, rather than saying what those outlets reported. Phrases such as independent
coverage, regional media outlets, trade publications, featured in, maintains an active social media
presence. More common in output from 2025 onward.

Superficial analysis bolted onto a fact. Usually a present participle clause at the end of a
sentence, adding an interpretation nobody sourced. Ending with ", highlighting the growing demand for
sustainable materials" is the shape.

Promotional register that leaks in even when neutrality was requested. Words such as boasts, vibrant,
rich, nestled, in the heart of, renowned, diverse array, commitment to. Travel guide voice and press
release voice are both common failure modes.

Vague attribution. Experts argue, observers have noted, industry reports suggest, critics contend,
several sources, often with one citation or none. Also presenting one source's view as widely held.

Formulaic challenge and outlook sections. A "Challenges" heading opening with "Despite its strengths"
and closing on vague optimism, often paired with "Future prospects". The rigid shape is the tell, not
the mention of difficulty.

Ecosystem padding in biology writing. Over-connecting a species to its wider environment and
belabouring conservation status and research efforts even when none exist.

## Language and grammar

Overrepresented vocabulary. Frequency studies of text written after 2022 found sharp rises in a
specific set of words. See the excess vocabulary analysis of biomedical abstracts
([Kobak et al., Science Advances 2025](https://doi.org/10.1126/sciadv.adt3813)) and work on how
alignment training drove the overuse
([Juzek and Ward, arXiv 2412.11385](https://arxiv.org/abs/2412.11385)).

The set moves over time, which matters if you are dating text rather than just cleaning it. Delve
peaked in 2023 and early 2024 and then fell away. The 2023 cluster included boasts, bolstered,
crucial, delve, intricate, interplay, meticulous, pivotal, tapestry, testament, vibrant, and
Additionally as a sentence opener. The mid 2024 cluster leaned on align with, enhance, foster,
highlighting, showcasing, underscore. Later output favours emphasising, enhance, highlighting,
showcasing, plus the notability assertions above. Grok output over-favours superficially scientific
words such as empirical and causal.

One or two of these words means nothing. Density is the signal, which is why the detector reports a
per thousand word rate as well as individual hits.

Copula avoidance. Models reach for serves as, stands as, functions as, represents a, marks a,
operates as, and refers to, where a writer would use is. They also prefer features, offers, and
boasts over has. An analysis of academic writing measured a drop of over ten percent in the frequency
of is and are in 2023 with no comparable earlier movement
([Geng and Trotta, arXiv 2404.08627](https://arxiv.org/abs/2404.08627)). A broader style comparison
found the same direction ([Reinhart et al., PNAS 2025](https://doi.org/10.1073/pnas.2422455122)).

Vague connection language. Writing that someone was associated with or connected to a role, instead
of saying they held it. "Was connected with science education at the university" where the fact is
"taught physics there from 2011".

Negative parallelism. Not only X but also Y. It is not X, it is Y. Y rather than X. The construction
implies the reader was about to reach a wrong conclusion. Humans use it, models use it as a reflex,
and the reversed form is especially common in Grok output.

Three item rhythm. Adjective, adjective, adjective, or three parallel clauses used for cadence rather
than because three things exist. Strongest signal when it appears somewhere nobody would bother with
style, such as a commit message or an edit summary.

Synonym rotation. Older models carried a repetition penalty, which produces elegant variation:
the same idea renamed every time it recurs. Human writers repeat the right word.

## Formatting

Title case headings. Capitalising every significant word in a heading. One of the more reliable
signals, because most writers do not bother.

A title line repeated at the top of a document that already has a title.

Headings that contain only more headings, with no content of their own.

The "X and Y" heading shape where one noun would do. "Awards and recognition" is close to a
signature.

Heavy bold, especially an inline bolded label at the start of every list item, followed by a colon.
The habit comes from readmes, slide decks, and listicles.

Em dashes used where a comma, colon, or parenthesis would be normal, usually with spaces around them
against most typographic conventions. Newer models were tuned to suppress this, and a 2026 comparison
found only one major assistant using them more than professional writers, so treat this as
corroboration rather than proof.

Curly quotes and curly apostrophes, sometimes mixed inconsistently with straight ones in the same
document. Word processors and macOS also produce these, so it is weak on its own.

Emoji used as decoration on headings or bullets.

Horizontal rules between every section, which is a Markdown habit.

Small tables holding two facts that a sentence would carry better.

Skipped heading levels, such as starting at level three, or overuse of level one headings. Usually a
symptom of Markdown being converted to another markup.

## Markup and leaked internals

These are the strongest signals, because they are machine output that nobody meant to publish. The
detector treats all of them as high severity.

ChatGPT: `contentReference`, `oaicite`, `oai_citation`, `turn0search0` and similar tokens,
`turn0image0`, and JSON fragments containing `attributableIndex`.

Gemini: `[cite: 1]` style markers, and `[span_1](start_span)` pairs.

Grok: `grok_card` tags, `grok_render_citation_card_json`.

DeepSeek: lenticular bracket citations with a dagger, such as the pattern around a numeric id.

Perplexity: `[attached_file:1]`, `[web:1]`, and source URLs pointing at an upload bucket containing
`ppl-ai-file-upload`.

Tracking parameters appended to source URLs: `utm_source=chatgpt.com`, `utm_source=openai`,
`utm_source=copilot.com`, `referrer=grok.com`. These identify the tool that fetched the page. Strip
them. Note that they show the citation was gathered with a tool, which is not the same as the prose
being generated.

Markdown syntax where another markup language was required, especially a fenced block labelled
wikitext, or `##` headings inside a wiki page.

## Text meant for the operator

Content that was correspondence, not copy. I hope this helps. Would you like me to expand this.
Certainly. Of course. You are absolutely right. Let me know if you need anything else.

Knowledge cutoff and missing source disclaimers. As of my last knowledge update. While specific
details are limited. Not widely documented. Based on available information. When the subject is a
person, this often becomes a claim that they keep a low profile or keep personal details private,
which is usually invented.

Unfilled placeholders. Bracketed prompts such as insert name here, dates written as 2025-xx-xx,
comments saying to add something if available, and template scaffolding left in place.

Procedural self-justification. Text or commit messages that reassure the reader the work complies
with the relevant guidelines, itemise which standards were followed, or describe what was deliberately
preserved and avoided. Human commit messages say what changed.

## Citation failures

Broken external links in a newly written document, especially several at once, with no archived copy
anywhere.

Invalid ISBN checksums and unresolvable DOIs.

DOIs that resolve to an unrelated paper. A plausible looking reference pointing at something else
entirely is a common fabrication pattern.

Book citations with no page number, or with a page number that does not contain the claim.

Named references defined but never used inline, or used but never defined.

This category does the most damage, because a confident false citation is worse than no citation.
Verify before publishing.

## What is not a tell

Do not use these as evidence, because they point weakly or in the wrong direction.

Correct grammar. Many people write well.

Formal or academic vocabulary in general. The signal is a specific word set, not register.

Prose that strikes you as bland or robotic. Machine output skews positive and verbose rather than
flat, and readers unfamiliar with it often guess wrong.

Mixed casual and formal register, which is normal for technical writers, younger writers, and
multi-author documents.

Transition words on their own. Only a few are genuinely overused, and essay writing has always used
them.

Missing citations. Hundreds of thousands of Wikipedia articles predating these tools lack them, and
current models cite constantly, just not always accurately.

Bizarre or broken markup, which more often comes from editor bugs and browser extensions than from a
model.

Good formatting, including correct complex templates.

## Signs of human writing

Worth adding deliberately when the goal is prose that reads as written by a person.

Plain copulas. There is a, it has a.

Plain verbs. Wrote rather than authored. Used rather than utilised. Died rather than passed away.

Definite claims, including superlatives, where a source supports them. Machine output hedges.

Occasional hedging and intensifiers such as very, perhaps, and tends to, which models trim.

Slightly wordy constructions that a copy editor would tighten, such as in order to, as a result of,
and the fact that.

Anything text predating 30 November 2022, which rules out these tools entirely.

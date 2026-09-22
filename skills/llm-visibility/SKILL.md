---
name: llm-visibility
description: Get a site retrieved and cited by AI answer engines and chat assistants rather than only ranked in classic blue links. Shape content so a passage can be lifted and attributed, put the direct answer first, make the entity and author clear, add supporting structured data, publish an llms.txt style summary, decide which AI crawlers to allow or block against the traffic tradeoff, and measure citation share across assistants. Use when a brand appears in search but never in AI answers, when deciding whether to block AI crawlers, or when planning content for answer engines. Triggers on show up in chatgpt answers, get cited by ai, generative engine optimization, llms.txt file, should I block gptbot, ai crawler policy, perplexity citations, google ai overviews, answer engine optimization, my brand not in ai answers, structure content for llms, get quoted by ai assistants.
license: MIT
compatibility: Any website on any stack. The crawler policy applies to any server that can serve robots.txt and response headers.
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# LLM visibility

Asked to get a site into AI answers, a model tends to recycle classic SEO advice, add some keywords, and call it done. Answer engines do not work like the ten blue links: they retrieve passages, synthesise an answer, and cite a few sources, so a page that ranks well can still never get quoted. This skill shapes content and access so a specific passage can be extracted and attributed, and it names the tradeoff of blocking the crawlers that feed those answers.

When the work produces markup, JSON-LD, or an llms.txt file, follow the `code-craft` contract so the output is organised and commented rather than dumped as a block.

## Fit to the project

Read what the site already exposes before adding anything.

1. Check the current AI crawler policy. Read robots.txt for user agents such as the ones used by AI assistants for training and for live retrieval, and note whether any are already allowed or disallowed. Blocking a retrieval crawler removes the site from that assistant's live answers, which is a business decision, not a default.
2. Look at how answers already appear. Ask the major assistants a few questions the site should be the answer to, and record whether the site is cited, a competitor is cited, or the answer is wrong. That citation baseline is what later work moves.
3. Read three key pages for extractability. Is there a direct answer near the top, or does the point arrive after five paragraphs of preamble? Are claims stated as self contained sentences a model can lift, or do they depend on the previous paragraph to make sense?
4. Find the entity and author signals already present: an about page, author bylines with credentials, an Organization or Person block in structured data. Answer engines weight clear authorship and a recognisable entity when deciding whom to cite.

## Non-negotiables

1. Do not block an AI retrieval crawler without stating the tradeoff. Blocking it protects content from being used but also removes the site from that assistant's live citations and any referral traffic that comes with them. The user decides with the tradeoff in front of them.
2. Every claim written for extraction has to be true and supportable. Answer engines and their users check, and being cited for a wrong statement is worse than not being cited. Do not invent statistics or authorities to look quotable.
3. Keep the on-page facts and any llms.txt summary in agreement with the visible page. A summary that overstates or contradicts the page reads as manipulation and gets discounted.
4. Do not fabricate an author, credentials, or an organisation to game entity signals. False authorship is detectable and destroys the trust that gets a source cited again.
5. Treat retrieval crawler access and training crawler access as separate decisions. Blocking training use while allowing live retrieval is a valid position, and conflating the two removes the site from answers you may have wanted to appear in.

## Procedure

### Step 1, baseline the current citation share

Ask each assistant the questions the site should own, and record who gets cited for each. Note the exact phrasing of any answer that mentions the site or a competitor. This is the before state; citation share, not ranking, is the metric this skill moves. Keep the questions so you can re-ask them after changes.

### Step 2, put the direct answer first

For each target page, state the answer to its core question in the first paragraph, in one or two self contained sentences that make sense lifted out of context. Retrieval systems favour a clear, early, quotable passage over an answer buried under preamble. Keep the supporting detail below it for the reader who wants more.

### Step 3, make passages liftable and attributable

Break content into sections with descriptive headings that match how people ask the question. Write claims as complete sentences that do not rely on the previous one, so a single extracted passage stays accurate. Attach names, dates, and specific figures to claims where they exist, because a concrete attributable statement gets quoted over a vague one.

### Step 4, strengthen entity and author clarity

Give the content a clear author with real credentials and a byline, and describe the publishing organisation on an about page. Add Person and Organization structured data so the entity is machine readable, and keep names consistent across the site and any external profiles. The extraction and entity rules are detailed in `references/extractable-content.md`.

### Step 5, publish supporting structured data and a summary

Add JSON-LD for the content types the pages genuinely are, the same discipline as on-page SEO. Consider an llms.txt style summary file at the site root: a plain, honest map of what the site covers and where the authoritative pages are, written for a machine reading agent. Treat llms.txt as an emerging convention with no guaranteed support, not a ranking mechanism.

### Step 6, set the crawler policy deliberately

Decide, per crawler, whether to allow training use and whether to allow live retrieval, and write the robots.txt and any header rules to match that decision. Document why each choice was made. The tradeoff and the known crawler categories are laid out in `references/ai-crawler-policy.md`. Present the traffic cost of any block to the user before applying it.

### Step 7, measure citation share over time

Re-ask the baseline questions on a schedule, because answers drift as models update. Track how often the site is cited, for which questions, and whether the cited passage is accurate. Watch server logs for referral traffic from assistant domains where it exists. Judge the work by change in citation share, not by any single answer on any single day.

## What good output produces

A short list of target questions the site should be the source for, with the current cited source for each and the gap to close.

Pages whose first paragraph answers the question in liftable sentences, with headings that mirror real questions and claims that carry attribution.

A documented crawler policy that states, per crawler, the allow or block decision and the traffic tradeoff the user accepted.

## Self-audit

- Does each target page answer its core question in the first paragraph in self contained sentences?
- Is every extractable claim true and supported, with no invented figure or authority?
- Do the on-page facts and any llms.txt summary agree with each other?
- Is the author real, credentialed, and consistent with the entity structured data?
- Was the traffic tradeoff of any crawler block stated to the user before it was applied?
- Are retrieval access and training access treated as separate, documented decisions?
- Is there a citation baseline and a plan to re-measure it over time?

## Honest limits

This skill improves the chance of being retrieved and cited; it cannot guarantee any assistant cites the site, because retrieval and synthesis are opaque and change with each model update. It does not create authority that does not exist, and a site with no credible content will not be cited however well structured.

Classic crawlability, indexation, titles, and page experience for blue link ranking belong to `seo-optimize`. Getting new pages discovered and indexed quickly belongs to `index-fast`. Writing the prose so it does not read as machine generated belongs to `human-prose`. The llms.txt convention has no guaranteed adoption, so treat it as a low cost bet rather than a proven channel.

If the user says "stop", "just execute", or "skip the visibility audit", that is the off switch. Do
only what was asked and stand down. The session continues without it unless the user reopens the
question.

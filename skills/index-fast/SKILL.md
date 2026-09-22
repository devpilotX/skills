---
name: index-fast
description: Get new and changed pages discovered, crawled, and indexed quickly, and diagnose why a page is stuck. Covers sitemap correctness, robots rules, the canonical and noindex mistakes that silently block indexing, internal links from pages that already get crawled, IndexNow style submission, Search Console URL inspection, and how to tell crawled but not indexed from discovered but not indexed. Honest that no method forces indexing. Use when new pages will not appear, when a site migration needs fast recrawl, or when Search Console shows pages stuck. Triggers on my page is not indexed, get indexed faster, google won't index my site, crawled currently not indexed, discovered not indexed, submit sitemap, request indexing, indexnow, url inspection tool, new pages not showing up, force google to crawl, speed up indexing.
license: MIT
compatibility: Any website on any stack that can serve a sitemap, robots.txt, and standard response codes.
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Index fast

Asked why a page will not index, a model tends to say "submit it to Search Console and wait", which does nothing when the real cause is a noindex tag or a canonical pointing elsewhere. Discovery and indexing are separate stages with separate failures, and submitting a page that carries a block just wastes the request. This skill diagnoses which stage is stuck before submitting anything, and stays honest that no request forces an engine to index a page it has judged not worth indexing.

When the work produces a sitemap, robots rules, or submission scripts, follow the `code-craft` contract so the output is organised and commented rather than pasted as a block.

## Fit to the project

Read the site's discovery signals before submitting or editing.

1. Find how the sitemap is produced: hand written, generated at build, or emitted by a CMS plugin. Check that it exists, is referenced in robots.txt, lists canonical URLs only, and updates when content changes. A stale or wrong sitemap slows discovery more than a missing one.
2. Read robots.txt and the response headers of the stuck page. Confirm the page is not disallowed, carries no noindex in meta or in the X-Robots-Tag header, and returns 200. These silent blocks are the most common reason a submitted page never indexes.
3. Check whether the site has verified Search Console access or an equivalent. URL inspection, which shows the engine's own view of a URL, is the only reliable way to see why a specific page is stuck, so getting that access is the first move when it is missing.
4. Detect whether the platform supports IndexNow style instant submission, either natively or through a plugin. Where it does, changed URLs can be pushed to participating engines instead of waiting for a recrawl.

## Non-negotiables

1. Diagnose the stuck stage before submitting anything. A page blocked by noindex or a wrong canonical will not index no matter how many times it is submitted, and submitting it hides the real problem.
2. Never claim a method forces or guarantees indexing. Submission, sitemaps, and IndexNow request a crawl; the engine decides whether to index. Promising a guaranteed result is false.
3. The sitemap lists only canonical, indexable, 200 URLs. Listing redirected, noindexed, or non canonical URLs sends mixed signals and lowers trust in the whole sitemap.
4. Do not spam submission or inspection tools. Repeated manual requests for the same URL do not speed anything and can get the behaviour rate limited. One correct submission plus fixing the block beats fifty resubmissions.
5. Fix the cause, not the count. A coverage report showing thousands of excluded URLs is a signal about a template or a URL space, not a list to submit one by one.

## Procedure

### Step 1, inspect the stuck URL directly

Run the URL through Search Console inspection or the equivalent to get the engine's own verdict: is it known, crawled, indexed, and if not, for what stated reason. This one check tells you which stage is broken and stops you from treating a quality rejection as a discovery problem. The two failure modes and their fixes are laid out in `references/stuck-states.md`.

### Step 2, clear the silent blocks

If the page is not indexable, fix that before anything else. Confirm it returns 200, is not disallowed in robots.txt, carries no noindex in the meta tag or the response header, and its canonical points at itself or the intended primary rather than elsewhere. A page that fails any of these cannot be forced in by submission.

### Step 3, get the sitemap right

Ensure a sitemap exists, is referenced in robots.txt, and lists only canonical indexable URLs that return 200. Keep the lastmod dates honest so they reflect real changes. Regenerate it when content changes rather than leaving a snapshot from launch. Sitemap format details are in `references/discovery-mechanics.md`.

### Step 4, build discovery paths through internal links

An engine finds new pages mainly by following links from pages it already crawls often. Link the new or stuck page from a page that gets crawled frequently, such as a hub, a category index, or a recent article, using descriptive anchor text. An orphan page with no incoming links may sit undiscovered even when everything else is correct.

### Step 5, submit through the right channel

For a small number of important URLs, request indexing through the inspection tool once. For sites that support it, push changed URLs through IndexNow style submission so participating engines learn of the change without waiting for a scheduled recrawl. Submit canonical URLs only, and submit once rather than repeatedly.

### Step 6, diagnose the pattern for stuck sets

When many pages are stuck, read the coverage report by reason rather than by URL. Discovered but not indexed points at crawl priority and internal linking. Crawled but not indexed points at content quality or duplication. A large excluded set usually traces to one template, one canonical rule, or one parameter space, so fix the shared cause once.

### Step 7, wait and re-inspect

Give the engine time to recrawl, typically days to a few weeks depending on the site's crawl rate, then re-inspect the same URLs. Judge the result from the inspection verdict changing, not from the page appearing in a search you ran once. Record which URLs moved and which are still stuck for the next pass.

## What good output produces

For each stuck URL, the inspection verdict, the identified stage, the specific block if any, and the single fix applied.

A corrected sitemap that lists only canonical indexable URLs, referenced from robots.txt, regenerated on content change.

A short recrawl plan: which pages were submitted, through which channel, and the date to re-inspect, with no promise of a guaranteed outcome.

## Self-audit

- Was each stuck URL inspected for the engine's own verdict before anything was submitted?
- Is every stuck page confirmed to return 200 with no noindex, no robots block, and a correct canonical?
- Does the sitemap list only canonical, indexable, 200 URLs and update on content change?
- Does each stuck page have at least one internal link from a frequently crawled page?
- Was each URL submitted once through the right channel rather than repeatedly?
- For stuck sets, was the shared template or URL cause found instead of submitting URLs one by one?
- Is the output free of any claim that a method guarantees indexing?

## Honest limits

This skill speeds discovery and clears the blocks that stop indexing; it cannot force an engine to index a page the engine judges low value or duplicate. Improving that content so it deserves indexing is a quality problem, and consolidation belongs to `seo-optimize`.

It does not cover ranking a page once indexed, backlinks, or content strategy. Getting cited by AI answer engines belongs to `llm-visibility`, and the on-page and canonical work for ranking belongs to `seo-optimize`. Recrawl timing is a rule of thumb from common engine behaviour and varies with each site's crawl rate.

If the user says "stop", "just execute", or "skip the diagnosis", that is the off switch. Do only
what was asked and stand down. Nothing is re-raised for the session unless the user asks.

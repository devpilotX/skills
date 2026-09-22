---
name: seo-optimize
description: Improve how a website earns organic search traffic through technical and on-page work: crawlability, indexation, titles and descriptions, heading order, internal links, structured data, canonical tags, pagination and faceted URLs, page experience metrics, and international targeting. Diagnose with real crawl and search data before changing anything, and never promise a specific ranking. Use when a site loses organic traffic, when pages will not rank, or when a launch needs a technical review. Triggers on why did my traffic drop, pages not ranking, fix my SEO, technical SEO audit, improve search visibility, rewrite title tags, meta descriptions, fix duplicate content, add structured data, canonical tags, core web vitals, hreflang setup, site not showing in google, on-page optimization.
license: MIT
compatibility: Any website on any stack, static or server rendered. The optional checks use only a crawler or browser you already have.
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Search optimize

A request to improve SEO usually gets title tags edited and keywords added, because that is the most probable answer rather than the useful one. The traffic drop was a canonical tag pointing every product page at the homepage, and no amount of copywriting fixes that. This skill forces a diagnosis from crawl data and Search Console before a single tag changes, so the work targets the cause instead of the symptom.

When the change produces HTML, JSON-LD, or template markup, follow the `code-craft` contract so the output arrives organised and commented rather than pasted as one block.

## Fit to the project

Read the site before touching it. The stack decides where every fix lands.

1. Find how pages are generated: a static site generator, a server framework, a headless CMS, or a single page app that renders client side. Client rendered pages need the SEO signals present in the initial HTML or in server side rendering, not injected after load, so detect this first.
2. Locate the existing signals. Read robots.txt at the site root, find the sitemap it references, and view source on three representative pages to see current title, meta description, canonical tag, heading order, and any JSON-LD. Note whether titles are unique or templated identically.
3. Get real data before opinions. Open the site's Search Console or equivalent and record the queries, impressions, and average position for the pages in question. If no Search Console property exists, that is the first thing to set up, because guessing at rankings without it wastes every later step.
4. Where the project has settled a URL scheme, a canonical policy, or a metadata template, adopt it and extend it. A second inconsistent convention confuses crawlers more than the original gap.

## Non-negotiables

1. Diagnose with real data before changing anything. Pull crawl output and Search Console figures first. Editing tags on a hunch can move a page that was ranking and lose traffic you cannot get back quickly.
2. Never promise a ranking or a traffic number. Search engines rank on signals you do not control and change without notice. A promised position that does not arrive destroys trust and is not something any honest audit can offer.
3. One canonical destination per piece of content. If two URLs serve the same content and both are canonical, or a canonical points somewhere unintended, the engine picks one on its own and can drop the page you wanted indexed.
4. Do not add noindex, disallow, or a canonical to a template without checking every page that template renders. A single template rule can deindex thousands of pages silently, and the drop shows up weeks later.
5. Titles and descriptions describe the page honestly. Keyword stuffing and misleading titles get rewritten by the engine or suppressed, and the click that arrives on a false promise bounces and teaches the engine the result was bad.

## Procedure

### Step 1, establish the baseline

Record where the site stands before any edit. Capture indexed page count from Search Console coverage, the queries and positions for the target pages, and a crawl of the site with any crawler that reports status codes, titles, canonicals, and redirect chains. Save this as the before state so you can prove a change helped or revert it if it hurt.

### Step 2, fix crawlability and indexation first

Confirm the pages you want found return 200, are not blocked in robots.txt, carry no accidental noindex, and have a canonical pointing at themselves or the intended primary. Check that a crawler starting from the homepage can reach them through links within a few hops. Repair redirect chains longer than one hop and remove links to 404 pages. Work the checks in the order given in `references/crawl-diagnosis.md`. Nothing else matters until the important pages can be crawled and indexed, which is why `index-fast` is the neighbouring skill for stubborn discovery problems.

### Step 3, get the on-page signals right

Write a unique title under about 60 characters and a description under about 155 characters for each important page, each describing that page rather than the site. Use one h1 per page that matches the page intent, and keep headings in order without skipping levels for visual size. These are rules of thumb on length; the engine truncates in pixels, not characters, so treat the numbers as guides. The length figures, heading rules, and hreflang setup are detailed in `references/on-page-and-schema.md`.

### Step 4, strengthen internal linking and structure

Link to important pages from other pages that already get crawled and carry authority, using descriptive anchor text rather than "click here". Flatten deep pages closer to the homepage. Group related content so a crawler and a reader can both see the site's shape. Internal links are the lever you fully control, unlike backlinks.

### Step 5, add structured data that matches the page

Add JSON-LD only for types the page genuinely represents, such as an article, a product with a real price, or a set of FAQs actually on the page. Validate it against the schema and against the engine's rich result test. Marking up content that is not visible on the page, or a review score you invented, risks a manual action.

### Step 6, handle canonicalisation, pagination, and faceted URLs

Pick one canonical form for each URL: one of http or https, one of www or bare domain, one trailing slash policy, lowercase paths, and consistent parameter order. Redirect the rest to it. For paginated lists, let each page self canonicalise and stay indexable rather than pointing every page at page one. For faceted or filtered URLs that multiply into near duplicates, decide deliberately which combinations should be crawlable and block or noindex the rest so crawl budget is not spent on infinite variants.

### Step 7, measure page experience and revalidate

Measure the loading, interactivity, and layout stability metrics on real pages using a field data source where available and a lab tool otherwise. Treat page experience as one ranking input among many, not the deciding one. After changes, recrawl, resubmit affected sitemaps, and watch Search Console for two to four weeks before judging the result, because indexing and ranking updates lag.

## What a good audit produces

A prioritised list where each item names the page or template affected, the evidence from crawl or Search Console, the change, and the expected effect. Crawlability and indexation fixes rank above copywriting, because a page that cannot be indexed cannot rank at any quality of title.

A before and after snapshot of indexed page count, target query positions, and the affected metrics, so the effect is visible and reversible.

A note of every template level change and the count of pages it touched, checked before it shipped.

## Self-audit

- Did every recommendation cite crawl output or Search Console data rather than a guess?
- Is there no promise of a specific ranking or traffic figure anywhere in the output?
- Does every important page return 200, avoid noindex and robots blocks, and carry a correct canonical?
- Is every title and description unique to its page and within the length rule of thumb?
- Was every template level change checked against the pages it renders before shipping?
- Does all structured data reflect content actually on the page and validate against the schema?
- Is there a before snapshot that lets the change be measured or reverted?
- Are pagination and faceted URLs handled so crawl budget is not spent on duplicates?

## Honest limits

This skill covers technical and on-page work you control on your own site. It does not build backlinks, run outreach, or manage paid search, and it cannot make content rank that does not deserve to. Off-page authority and content quality decide most competitive rankings and sit outside this file.

It does not get new or changed pages discovered and indexed quickly; that diagnosis of crawled versus discovered but not indexed belongs to `index-fast`. Getting cited by AI answer engines rather than ranked in blue links belongs to `llm-visibility`. The numbers on title and description length are rules of thumb from common engine behaviour, not guarantees, and search engines change ranking factors without notice.

If the user says "stop", "just execute", or "skip the audit", that is the off switch. Make only the
change asked for and stand down. Nothing is re-raised for the rest of the session unless they ask.

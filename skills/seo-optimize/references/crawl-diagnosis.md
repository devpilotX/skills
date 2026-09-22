# Crawl and indexation diagnosis

Use this when organic traffic drops or pages will not appear in search. Work top down: a page has to be crawlable before it can be indexed, and indexed before it can rank. Fixing a title on a page the engine cannot index changes nothing.

## The order to check

1. Does the URL return 200? A page returning 404, 410, 500, or a soft 404 that returns 200 with empty content will not stay indexed. Check the real status with a request, not the browser, because a service worker can hide the true code.
2. Is it blocked in robots.txt? A Disallow rule stops crawling. A blocked page can still appear as a bare URL with no snippet, which looks like an indexing bug but is a robots rule.
3. Does it carry a noindex? Check both the meta robots tag in the HTML head and the X-Robots-Tag HTTP header. A noindex in either place removes the page from the index even when everything else is correct.
4. Where does the canonical point? A canonical to a different URL tells the engine to index that other URL instead. A canonical to a redirected or 404 URL confuses the choice. Self referencing canonical is the safe default for a primary page.
5. Can a crawler reach it from the homepage? A page with no internal links pointing at it, an orphan, may never be discovered even when it is perfect. Links are how crawlers travel.

## Reading the coverage report

Search Console groups URLs by state. Two states get confused constantly.

Discovered but not indexed means the engine knows the URL exists but has not crawled it yet, often a crawl budget or priority signal. More internal links from crawled pages and a cleaner sitemap help.

Crawled but not indexed means the engine fetched the page and chose not to index it, usually a quality or duplication signal. Thin content, near duplicate of another page, or a soft 404 are the common causes. Adding links does not fix this one; improving or consolidating the content does.

Excluded by noindex, blocked by robots, alternate page with canonical, and redirect are self explanatory once you know to read the reason rather than the count.

## Common silent killers

A staging noindex or a Disallow: / left in robots.txt after a launch. This deindexes the whole site and is the first thing to rule out after a sudden total drop.

A canonical template that points every page of a type at one URL, so only one of thousands gets indexed.

A migration that changed URLs without 301 redirects, so the old indexed URLs 404 and the new ones start from zero.

A parameter or faceted URL space that generates near infinite low value URLs and spends the crawl budget before the real pages get visited.

Mixed signals: a page in the sitemap that also carries noindex, or a canonical that disagrees with the redirect target. The engine has to guess, and its guess is often not yours.

## What to record

For each affected URL: status code, robots verdict, meta and header robots value, canonical target, whether an internal link path from the homepage exists, and the Search Console state with its stated reason. That table tells you which layer is broken before you spend effort on the wrong one.

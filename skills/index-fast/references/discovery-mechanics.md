# Discovery mechanics: sitemaps, robots, and submission

How engines find pages, and the configuration that either helps or silently blocks them.

## Sitemaps

A sitemap is a list of URLs the site wants crawled. It speeds discovery of pages that are weakly linked, but it does not force indexing.

Rules that keep a sitemap trusted:

List only canonical URLs. A sitemap URL that then canonicalises to a different URL sends a mixed signal.

List only indexable, 200 URLs. Do not list redirected, noindexed, or 404 URLs. Each bad entry lowers the engine's trust in the file.

Keep lastmod honest. A lastmod that updates on every crawl regardless of real change teaches the engine to ignore it. Set it to the real content change time.

Split large sitemaps. A single file has limits on URL count and size; past them, use a sitemap index that points at several sitemaps. Keep each file under the published limits.

Reference the sitemap in robots.txt with a Sitemap line, and submit it once in Search Console. Resubmitting an unchanged sitemap does nothing.

## Robots.txt

Robots.txt controls crawling, not indexing. A Disallow stops the crawl; it does not remove an already indexed URL, and a disallowed URL can still appear as a bare link with no snippet.

The trap: to remove a page from the index with noindex, the engine has to be able to crawl the page to see the noindex. If the page is also disallowed in robots.txt, the engine never reads the noindex and the page can linger in the index. Do not combine a robots Disallow with a noindex intent on the same URL.

Keep robots.txt minimal and readable. A stray Disallow: / from a staging config is the classic sitewide indexing killer, so check it first after a sudden total drop.

## Internal links as the primary discovery path

Engines find most pages by following links from pages they crawl often. The homepage, category hubs, and recent content get crawled frequently, so a link from one of those is the fastest organic discovery route. A page with no incoming internal link, an orphan, depends entirely on the sitemap and may wait a long time.

## IndexNow style submission

Some engines accept a direct ping that a URL has been added or changed, so they can crawl it without waiting for a scheduled visit. Where the platform supports it, this shortens the discovery delay for changed pages.

What it does: tells participating engines a URL changed, prompting a crawl.

What it does not do: guarantee indexing. The crawl still ends in the engine's own decision. Submit canonical URLs only, and submit on real change rather than on a loop.

## Recrawl timing

How fast an engine returns depends on the site's crawl rate, which grows with the site's authority and update frequency. A new low authority site may wait weeks; an established news site is crawled within minutes. Treat any timing figure as a rule of thumb and measure the site's own rate from server logs and inspection history rather than assuming a fixed number.

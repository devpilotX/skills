# Stuck states: crawled versus discovered but not indexed

The two most confused indexing states have opposite fixes. Read the exact state from URL inspection or the coverage report before acting, because treating one as the other wastes the effort.

## Discovered but not indexed

The engine knows the URL exists, usually from the sitemap or a link, but has not crawled it, or crawled it and deprioritised it. This is a crawl priority signal.

What it usually means: the site has more URLs than the engine wants to crawl right now, the URL is weakly linked, or the sitemap is noisy with low value URLs that dilute the important ones.

What helps: link the page from pages that already get crawled often so it inherits some priority. Trim the sitemap to canonical, valuable URLs only. Improve the site's overall crawl efficiency by removing dead ends and infinite parameter spaces. Submitting the URL once can nudge it, but the underlying priority is the real lever.

What does not help: resubmitting the same URL repeatedly, or editing the page content, since the engine has not judged the content yet.

## Crawled but not indexed

The engine fetched the page and decided not to index it. This is a quality or duplication signal, not a discovery one.

What it usually means: the content is thin, near duplicate of another page, a soft 404, or otherwise judged not worth a slot in the index. The page was seen and passed over.

What helps: improve or consolidate the content so the page is substantially different and useful. If it duplicates another page, decide which is canonical and point the other at it or merge them. Remove soft 404s that return 200 with empty or error content.

What does not help: adding internal links or resubmitting, since the engine already saw the page and made its call on the content.

## How to read the verdict

URL inspection reports the current state and, for a stuck page, the reason. Match the reason to the fix rather than reaching for submission by reflex.

If the state is a block reason such as excluded by noindex, blocked by robots.txt, or alternate page with canonical, the fix is to clear that specific block, covered in the main skill. Those are not quality or priority problems; they are configuration mistakes.

## A quick decision path

Is the page blocked by noindex, robots, or a canonical elsewhere? Clear the block first.

Is it discovered but not crawled? Work on internal links and sitemap quality.

Is it crawled but not indexed? Work on content quality and duplication.

Is it indexed but you expected better placement? That is ranking, which this skill does not cover; hand off to seo-optimize.

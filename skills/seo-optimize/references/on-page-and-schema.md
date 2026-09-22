# On-page signals and structured data

Length figures here are rules of thumb from how major engines commonly truncate and weight content. They are not guarantees, and engines rewrite titles when they judge their own version more useful.

## Titles

One title per page, unique across the site, describing that page. A rule of thumb is under about 60 characters or roughly 600 pixels, because engines truncate on pixel width, not character count. Put the most specific term first. A templated title that reads the same on every page wastes the strongest on-page signal.

Avoid stuffing the same keyword several times. The engine reads it as manipulation and may replace the title with text pulled from the page.

## Meta descriptions

The description does not rank the page directly. It affects the click, because it often becomes the snippet. Write under about 155 characters, describe what the page delivers, and give a reason to click. A missing description lets the engine assemble one from the page, which is acceptable but less controlled.

## Headings

One h1 that states the page subject. Subheadings in order, h2 then h3, without skipping a level to get a font size. Screen readers and crawlers both use heading order to understand structure, so a visual choice made with heading tags breaks both.

## Internal links and anchor text

Anchor text tells the engine what the linked page is about. "Pricing plans" beats "click here". Link important pages from pages that already get crawled and carry authority. Keep important pages within a few clicks of the homepage. Fix links that point at redirects or 404s, because each one wastes a hop and a signal.

## Structured data with JSON-LD

Add JSON-LD in a script tag for types the page genuinely is. Common useful types:

Article for a news or blog post, with headline, author, and date published.
Product for a commerce page, with a real name and a price that matches the visible price.
FAQPage only when the questions and answers appear on the page for the user to read.
BreadcrumbList to describe the page's position in the site hierarchy.
Organization or Person on an about or profile page to state who publishes the content.

Rules that keep it safe:

Mark up only content visible to the user on that page. Hidden markup or invented review scores can trigger a manual action that removes rich results across the site.

Validate every block against the schema and against the engine's rich result test before shipping. A syntax error in one block can void the whole page's structured data.

Keep prices, availability, and dates in the markup in sync with what the page displays. Stale structured data that contradicts the page gets ignored or penalised.

## International targeting

For a site in several languages or regions, hreflang annotations tell the engine which version to show which user. Every version links to every other version including itself, the return links have to be mutual, and the language and region codes have to be valid. A one directional or mistyped hreflang set is ignored, so partial setup buys nothing.

## Page experience

Loading, interactivity, and layout stability are inputs to ranking, weighted less than relevance. Measure them on real pages with field data where you have it, because lab scores on a fast machine hide problems real users hit on slower networks and devices. Fix the worst real pages first rather than chasing a perfect lab score.

# Extractable content and entity clarity

Answer engines retrieve passages and attribute them. This file covers how to write so a passage survives being lifted out, and how to make the publisher and author legible to a machine.

## Writing a liftable passage

A passage is liftable when it stays accurate with no surrounding context. Test each key claim by copying one sentence on its own and asking whether it still means what you intended.

Put the answer to the page's core question in the first paragraph. A reader and a retrieval system both benefit, and the retrieval system will not scroll past preamble to find the point.

Write claims as complete sentences. "It supports up to 40 concurrent connections" fails alone because "it" is undefined. "The connection pool supports up to 40 concurrent connections" survives extraction.

Attach specifics. A named figure, a date, a version, or a source inside the sentence gives the engine something concrete to quote and to attribute. Vague claims lose to concrete ones when the engine picks what to cite.

Use headings that mirror how people ask. A heading reading "How much does it cost?" matches a query better than "Pricing structure", and the passage under a matching heading is easier to select as the answer.

## Structure that helps retrieval

Short sections, each answering one question, beat one long undivided page. The engine can select the relevant section instead of the whole document.

A question and answer block, where the answer directly follows the question in plain text, gives a clean unit to extract. Keep the answer self contained.

A summary sentence at the top of a long section states the takeaway before the detail, so a system that reads only the opening still gets the point.

## Entity and author signals

Answer engines prefer sources they can identify. Make the publisher and author explicit.

Give articles a real author byline with relevant credentials, not a generic "admin" or "team". Link the byline to an author page that states who they are and why they are qualified on the topic.

Describe the organisation on an about page: what it does, since when, and how to contact it. A recognisable, consistent entity is easier to cite with confidence.

Add Person and Organization structured data so the entity is machine readable, and keep the names, spelling, and details identical across the site and any external profiles. Inconsistent names split the entity signal.

## The llms.txt convention

Some sites publish a plain text file at the root that maps the site for machine reading agents: what the site covers, where the authoritative pages are, and short honest descriptions. It is an emerging convention with no guaranteed support from any assistant, so treat it as a low cost addition rather than a channel you can rely on.

Keep it honest and in sync with the site. A summary that oversells or contradicts the pages it points to is worse than none, because it reads as manipulation.

## What not to do

Do not invent statistics, quotes, or authorities to look more quotable. Being cited for a false claim is a worse outcome than not being cited.

Do not fabricate an author or credentials. False authorship is detectable and, once caught, the source loses the trust that got it cited.

Do not stuff the page with question headings that the content does not actually answer. An engine that lifts a heading with no real answer under it will not do it twice.

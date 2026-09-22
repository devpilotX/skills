# Structure by the reader's questions

A topic outline lists what the writer knows. A reader outline answers what the reader asks, in the order the questions arrive. The second holds attention; the first loses it around the third heading.

## The question sequence

For most pieces the named reader moves through a predictable sequence. Not every piece needs every question, and the job from the skill's Step 1 decides which to cut.

What is this, in one sentence I can repeat to a colleague. Answer immediately, in the opening, not after three paragraphs of background.

Why should I care right now. The reason today, tied to the reader's actual situation. A piece that cannot answer this has no opening hook worth keeping.

Does it actually work. Proof the reader can check: the number, the demo, the before and after, the named case. Claims without proof get skimmed past.

How do I do it, or how does it work. The mechanism or the steps, only as deep as this reader needs. A beginner needs the path; an expert needs the one non-obvious detail.

What could go wrong. The limits, the cost, the case where this is the wrong choice. Naming the downside is what makes the upside believable.

What next. The single action or decision the piece was written to produce, matching the job from Step 1.

## Worked reorder

A draft on a caching library opened with the history of caching, then the API, then benchmarks, then a use case. Reordered by reader questions for a backend engineer hitting latency: the latency problem and its cost first (why care now), then the benchmark showing the fix works (does it work), then the three-line integration (how), then the case where the cache serves stale data (what could go wrong), then the install command (what next). The history was cut, because that reader never asked it.

## The swap test

Read each sentence and ask whether it would still be true if you swapped in a competitor's product or a different subject. "Our platform is designed for scale" survives the swap, so it says nothing and gets cut or replaced. "Handles 40,000 writes per second on a single node before sharding" fails the swap, so it is doing work. Run this on every sentence in the cut pass. A draft where most sentences survive the swap has no substance yet, and the fix is more specifics, not more editing.

## Openings that enter the subject

The opening has one job: get the reader into the subject before they decide to leave. Ways that work, matched to the piece:

Start inside a concrete moment. "The pager went off at 3 a.m. because a cache we trusted had gone stale." The reader is in the story before they chose to be.

Start with the surprising number. "We deleted 40 percent of our tests last month and coverage of real bugs went up."

Start with the reader's own question stated plainly. "You want to know whether this is worth rewriting a working service for. Here is the honest answer."

State the claim someone could disagree with. "Most retry logic makes outages worse, and here is the code that proves it."

Openings that stall and get cut: defining a term the reader already knows, describing the state of the industry, asking a rhetorical question the reader did not ask, or promising that the piece will explore a topic. Explore nothing. Say the thing.

## Endings that keep the promise

The ending delivers the job from Step 1 and stops. It does not restate the sections, does not summarize what the reader just read, and does not open a new topic. If the job was a decision, the ending gives the decision rule. If the job was an action, the ending gives the next step in one line. Then it ends, because a piece that keeps going after its work is done teaches the reader to stop early next time.

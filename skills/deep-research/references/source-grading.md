# Source grading

Three axes, graded separately, because a source can be strong on one and useless on another.

## Independence

Does the source benefit from the answer?

Independent. No stake in the outcome. An academic group with no funding tie, a standards body, a
regulator, a journalist with no commercial relationship.

Interested. Benefits from one answer. Vendors, their customer case studies, sponsored research,
consultants selling the remedy, and anyone whose employer sells the thing.

Hostile. Benefits from the opposite answer. Competitors, and campaigners against the subject. Useful
for finding the strongest objection, and not for the overall verdict.

Unknown. Funding or affiliation not disclosed. Treat as interested until shown otherwise, and say that
is what you did.

An interested source is not worthless. It is authoritative on its own claims, plans, and prices, and
weak on comparative performance. Use it for the first and not the second.

## Currency

How fast does this fact change?

Volatile, measured in weeks. Prices, quotas, model capabilities, package versions, availability,
staffing, anything in active development. A source older than a few months needs rechecking, and a
source older than a year is probably wrong.

Slow, measured in years. Regulation, industry structure, standards, market share.

Stable. Mathematics, physical constants, settled history, established biology.

Record the date every time. On a volatile question, an old authoritative source loses to a current
mediocre one, and this is the mistake that most often produces a confidently wrong research output.

## Primacy

How many hands has the evidence passed through?

Primary. The original evidence. The paper, the filing, the specification, the source code, the pricing
page, the raw dataset, the court document.

Secondary. Someone reporting on primary evidence. Quality journalism, review articles, textbooks.
Useful for context and for finding the primary source.

Tertiary. Aggregation of secondary material. Encyclopedias, listicles, most content marketing, most
model output including this suite's own. Acceptable as a map, never as the citation.

Circular. Sources citing each other back to one unverified origin. Common on statistics that get
repeated for years. If three sources give the same oddly specific number, find where it started, and
be prepared to find that nobody knows.

Always try to reach the primary source. When you cannot, say which secondary source you relied on and
that the primary was not reachable.

## Specific traps

Statistics with no methodology. A market size with no stated method is marketing. Report it as a claim
by that publisher rather than as a fact.

Surveys with undisclosed sampling. Who was asked, how many, and how they were selected decides whether
the number means anything.

Benchmarks published by an interested party, especially where the configuration is unstated. Assume it
was tuned to favour the publisher.

Preprints, which have not been reviewed. Usable, and label them.

Retracted papers, which keep getting cited for years. Check.

Screenshots and secondhand quotes, which are frequently altered or missing context. Find the original.

Documentation describing intended behaviour rather than actual behaviour. Bug trackers and changelogs
are often more honest than the documentation.

Content optimised for search, which increasingly includes generated articles with fabricated
specifics. Prefer sources with a named author and a date.

Dead links revived from an archive, which may not reflect the current state. Note that the live version
differs if it does.

## Recording the grade

One line per source, as in this shape:

```
https://example.org/spec-v3  (2026-03-11)  independent / volatile / primary
  Standards body. No commercial stake. Current revision, supersedes the 2024 text.

https://vendor.example/benchmarks  (2025-08-02)  interested / volatile / primary
  Vendor's own benchmark, configuration not stated. Used only for its feature claims.
```

The one line note is the part a reader uses, because it says what the source may be trusted for. Write
it as a limit rather than as praise.

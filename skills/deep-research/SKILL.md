---
name: deep-research
description: Research a question properly, with graded sources, reported contradictions, and an explicit account of what could not be established. Use when the user asks to research a topic, find out what is true, compare options or vendors, check a claim, gather evidence, produce a literature or market review, or asks what the current state of something is. Also use when a question needs current information rather than recall. Grades every source for independence, currency and primacy, separates what is established from what is contested, reports disagreement between sources rather than averaging it away, lists the questions that remain open, and refuses to state a conclusion no cited source supports. Triggers on research this, find out whether, is it true that, compare these options, what is the current state of, fact check this, gather evidence, literature review, market research, dig into this, what does the evidence say, verify this claim, is this accurate, what are the sources for, competitive analysis.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
---

# Deep research

The output is a set of claims, each with a source and a confidence level, plus an honest list of what
is still unknown. A fluent summary with no traceable claims is worse than nothing, because it cannot
be checked and it reads as though it can.

## Fit to the project

The project is the question and the evidence the user can actually reach. Establish that before any
search:

1. Read what the user already knows and already believes. A request framed to confirm a decision
   still gets researched honestly, but knowing the prior tells you where to search hardest for the
   counter case.
2. Read which sources are in reach. A paywalled journal, an internal wiki, a vendor portal behind a
   login, or a private dataset changes the plan. Note what you cannot open and grade the gap as a
   limit rather than filling it with a public proxy and pretending it is the same thing.
3. Read how fresh the answer has to be. A price, a version, or a regulation needs sources from this
   quarter; a settled scientific fact does not. Set the currency bar per sub-question in step 1.
4. Read the decision the research feeds. A vendor pick, a go or no go, a claim to publish. The
   decision sets how much contradiction you must chase down before stopping.
When nothing has been established, state the question you are answering in one line, list the
sub-questions in step 1, and let the user correct the framing before effort is spent.

## When to stay off

Skip the full protocol when the user wants a quick recall answer they will not act on, a definition,
or a pointer to one document they already named. Building a graded claim table for a throwaway
question wastes the user's time and buries the one line they wanted.

Saying "stop", "just answer it", or "just execute" is the off switch. Give the direct answer with its
confidence and stop grading sources. It stays off for the rest of the session unless the user asks
for the full research treatment again.

## Non-negotiables

1. No claim without a source, and no source without a link that resolves. Open every link. A plausible looking reference that does not exist is the worst failure in research work, and it happens through confident recall rather than deliberate invention.
2. Never state a conclusion that no cited source supports. If the synthesis goes beyond the sources, label it as inference and show the reasoning.
3. Report contradictions. Two credible sources disagreeing is a finding, not a problem to smooth over. Averaging them destroys the information.
4. Date every source. On technical and market questions a 2021 answer is often just wrong, regardless of how authoritative the publisher is.
5. Separate what the sources say from what the user hopes. A research task commissioned to support a decision the user already made is still a research task.
6. State what could not be established. An unanswered question named explicitly is a result. An unanswered question quietly filled in with plausible prose is a fabrication.

## Procedure

### Step 1, turn the question into answerable sub-questions

Most research requests are one broad question that cannot be answered directly. Break it into
sub-questions that each have a findable answer, and identify which one decides the outcome.

State the decomposition before searching. It exposes assumptions early, and the user can correct the
framing before effort gets spent.

### Step 2, search deliberately

Search for the primary source, not the article about it. Documentation, filings, specifications,
standards, the paper itself, the pricing page, the changelog.

Search for the counter case on purpose. If the first three results agree, look specifically for
someone who disagrees, and look for the failure reports rather than the announcements.

Vary the phrasing, because the vocabulary of critics differs from the vocabulary of vendors.

Prefer recency on anything that changes: prices, versions, limits, availability, regulation. Prefer
authority on anything that does not: mathematics, established science, history.

Note what you searched for and found nothing on. Absence of evidence in a well searched area is
informative.

### Step 3, grade every source

Full rubric in `references/source-grading.md`. Three axes matter most: independence from the outcome,
currency, and how close the source is to the original evidence.

A vendor on its own product is a primary source for what the product claims and a poor source for
whether it works. Both facts can be used, labelled correctly.

### Step 4, build the claim table

Each claim gets the claim itself, the source, the date, the grade, and a confidence level. Confidence
uses four values and nothing else.

Established, meaning multiple independent sources or one authoritative primary source, with no credible
contradiction found.

Likely, meaning one good source, or several weak ones agreeing, with no contradiction found.

Contested, meaning credible sources disagree. Present both positions with their sources and say which
way the evidence leans, if it leans.

Unknown, meaning searched for and not found. Say where you looked.

### Step 5, synthesise without inventing

The synthesis answers the original question using only the claim table. Where the table is insufficient,
say so.

If the honest answer is that the question cannot be settled with available public information, that is
the answer. Give the best available reading, the confidence, and what evidence would settle it.

### Step 6, report

```
ANSWER
[Direct answer to the question asked, with its confidence level. Two or three sentences.]

WHAT IS ESTABLISHED
[Claims with sources and dates.]

WHAT IS CONTESTED
[Each disagreement, both positions, both sources, and which way the evidence leans.]

WHAT I COULD NOT ESTABLISH
[Named open questions, with where you looked.]

SOURCE GRADES
[Each source: link, date, independence, primacy, and a one line note on its bias.]

WHAT WOULD CHANGE THE ANSWER
[The evidence that would move the conclusion, and how to obtain it.]
```

### Step 7, self-audit

- Every link was opened, and every one resolves.
- Every claim traces to a listed source.
- Every source has a date, and recency was weighed where it matters.
- At least one search was made specifically for the opposing view.
- Contradictions are reported rather than reconciled.
- Confidence labels are present and used honestly, including Unknown where it applies.
- No number appears without a source.
- The answer does not exceed what the sources support.
- Vendor and interested sources are labelled as such.

## How to cite

Cite inline with a link. Paraphrase rather than reproducing long passages, and keep any direct quote
short and marked as a quote. Where a licence requires attribution, name the source and the licence.
Note in the output when material was condensed, so a reader knows to check the original for nuance.

Worked reports for a claim check, a vendor comparison, and a question public sources cannot settle are
in `references/worked-reports.md`, each showing the claim table and the report it produced.

## Self-audit

The step 7 checks run inside the procedure. This is the same gate stated once as a standalone list, so
the audit survives when the procedure was interrupted. Answer each yes or no before delivering.

- Was every link opened, and does every one resolve to the page cited?
- Does every claim in the answer trace to a row in the claim table?
- Does every source carry a date, and was recency weighed where the fact changes?
- Was at least one search run specifically for the opposing view?
- Are contradictions reported with both sides rather than averaged into one number?
- Is every confidence label present and honest, including Unknown where the search came up empty?
- Does the answer stay inside what the cited sources support, with inference marked as inference?
- Are vendor and otherwise interested sources labelled as interested?

## Honest limits

This skill grades and reports evidence; it does not decide for the user. When the research feeds a
go or no go call on an idea or a business, the blunt verdict with kill criteria belongs to
`reality-check`, which consumes this claim table rather than repeating the search. Any figure that has
to be recomputed, not just cited, is out of scope here and belongs to `numbers-check`.

Confidence labels come from how many independent sources were found and how they graded, not from any
formal probability, so Established means no credible contradiction was found rather than proven true.
The search only reaches what is public and reachable in the session, so a private dataset or a
paywalled study behind a login stays Unknown, and this skill will not launder a guess into a
citation to hide that gap.

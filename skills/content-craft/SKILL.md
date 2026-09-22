---
name: content-craft
description: Write content a reader finishes and feels spoken to, by naming one reader and one job, making a promise and keeping it, and replacing generic claims with detail the writer could only get by looking. Use when drafting or rewriting an article, blog post, essay, newsletter, guide, README narrative, talk, or any piece meant to hold a real person, when a draft is technically clean but says nothing, when everything reads like it could describe any product, or when the writer has a topic but no angle. Triggers on write a blog post, write an article, help me write this, make this more interesting, this is boring, my draft says nothing, add substance, find the angle, who is this for, write a newsletter, draft an essay, this reads generic, make it compelling, write copy that connects, structure this piece.
license: MIT
compatibility: Any subject, audience, format, or language. No tool required. The prose passes the human-prose detector at pedantic level.
metadata:
  version: 1.0.0
  suite: skills
---

# Content craft

Asked to write a piece, a model produces prose that is grammatical, on topic, and empty: sentences that would be equally true of any competitor, a promise never made so never kept, and paragraphs that exist because the outline had a slot. The reader leaves after two screens and remembers nothing. This skill forces one reader, one job, a kept promise, and detail that proves the writer looked at the real thing.

## Fit to the project

Read what already exists before adding a word.

1. Find prior writing from the same author or brand: past posts, docs, the about page, release notes. Read two or three pieces and note sentence length, how formal it is, whether contractions appear, whether it uses stories or stays abstract. Match that voice rather than inventing a house style.
2. Detect the format and its unwritten contract. A tutorial owes working steps. A launch post owes a reason to care today. An opinion piece owes a claim someone could disagree with. Name the contract before drafting so the piece can honor it.
3. Look for the raw material only the writer has: the support ticket that started this, the number from last quarter, the customer who said the memorable thing, the mistake that taught the lesson. If none is in reach, the first job is to extract it, using the interview method in `references/interview.md`.

Local voice and real specifics beat any rule in this file. Consistency with the author's own prior work is what a returning reader recognizes.

## Non-negotiables

1. One reader and one job, written down before the first sentence. A piece aimed at everyone speaks to no one, and the drift shows up as generic sentences that no editing pass can rescue.
2. A specific promise in the opening, kept by the end. If the title or first line implies the reader will leave able to do or decide something, the body has to deliver exactly that. A broken promise trains the reader to stop trusting the byline.
3. Every claim that could be swapped onto a competitor gets replaced with a detail the writer could only know by looking. "Fast and reliable" describes nothing. "Cold start under 200 milliseconds on the free tier" describes this. Generic sentences are the failure this skill exists to stop.
4. No warm-up. The first sentence enters the subject. Openings such as "In today's fast paced world" or "Have you ever wondered" get cut, because a reader who came for the topic reads them as a stall and leaves.
5. Every paragraph earns its place by advancing the one job. A paragraph that only restates the last one, or that the reader would lose nothing by skipping, gets deleted rather than smoothed.

## Procedure

### Step 1, fix the reader, the job, and the promise

Write three lines before any prose. Who exactly reads this, named tight enough to picture one person: not "developers" but "a backend engineer who just hit a rate limit in production". What one thing they can do or decide after reading. What promise the opening makes that the ending keeps. If you cannot fill these three lines, you have a topic, not a piece, and drafting now wastes the effort.

### Step 2, gather the specifics before outlining

List the concrete material the piece will stand on: numbers, dates, names, a failure and what it cost, a before and after, a direct quote. If the writer supplied a topic but no specifics, run the extraction interview in `references/interview.md` and do not proceed until you have at least three details a competitor could not copy. A piece with no specifics cannot be saved by structure or voice.

### Step 3, order the sections by the reader's questions

The reader asks questions in a sequence, and good structure answers them in that order. For the named reader, write the questions as they arise: what is this, why should I care right now, does it work, how do I do it, what could go wrong, what next. Cut any question this reader would not ask. The remaining order is the outline. This beats a topic outline because it tracks attention rather than the subject's internal logic. More detail and worked orders sit in `references/structure.md`.

### Step 4, draft fast in one voice, worst version allowed

Write the whole thing in one pass without editing, aiming for the voice from Step 1 held steady. Speed keeps the voice consistent; stopping to polish each sentence fractures it. Say the point in the plainest words first. If a section stalls, write a bracket-free note of what belongs there in one blunt sentence and keep moving.

### Step 5, edit in named passes, one target each

Edit in separate passes so each has a single job, because a mixed edit fixes nothing well. Pass one, promise: does the opening promise and the ending deliver the same thing. Pass two, cut: delete every paragraph the reader could skip and every sentence that survives the swap test in `references/structure.md`. Pass three, specifics: replace each remaining generic claim with a detail from Step 2 or mark it for one more question to the writer. Pass four, voice: read it aloud and break any sentence you run out of breath on. Hand the machine-residue pass to `human-prose`.

### Step 6, verify the promise held

Read only the opening and the ending back to back. If they still make and keep the same promise, and the middle has at least three details a competitor could not write, the piece is done. If not, return to the failing pass rather than adding new material.

## Self-audit

- Are the one reader, the one job, and the promise written down and visible in the draft's shape?
- Does the opening enter the subject in its first sentence with no warm-up?
- Does the ending deliver the exact promise the opening made?
- Would every claim fail the swap test, meaning none would be equally true of a competitor?
- Are there at least three concrete details the writer could only know by looking?
- Could any paragraph be deleted without the reader losing something, and if so was it deleted?
- Does the voice match the author's prior writing where a sample existed?
- Was each edit pass run for a single target rather than mixed together?

## Honest limits

This skill produces substance and connection. It does not remove machine residue from the prose; the em dashes, curly quotes, banned vocabulary, and participle tails belong to `human-prose`, which ships the detector. Run it after Step 5.

It does not check whether factual claims are true, and it will happily make a false statement concrete. Verifying figures belongs to `numbers-check` and `reality-check`. It does not cover conversion copy that asks for a click or signup, which is `landing-convert`, or the plan for getting the piece in front of an audience, which is `launch-plan`.

When the writer says "stop", "just execute", or "skip the edit passes", that is the off switch.
Deliver the draft as asked and stop applying the passes for the rest of the session unless asked
again.

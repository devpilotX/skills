---
name: landing-convert
description: Build a landing page that asks for exactly one action, matched to the traffic that arrives, answering objections in the order a real buyer hits them, with proof a stranger can check. Use when writing or fixing a landing page, sales page, signup page, pricing section, or hero, when a page has many links and no clear action, when traffic arrives but nobody converts, when the headline does not match the ad that sent the click, or when a form asks for more than the visitor will give. Triggers on write a landing page, fix my landing page, improve conversion, page does not convert, write the hero section, write a call to action, reduce form fields, pricing page, message match, why is nobody signing up, landing page copy, sales page, above the fold, headline for my ad.
license: MIT
compatibility: Any product, framework, or language. Copy and structure are stack independent. Generated markup follows the code-craft contract.
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Landing convert

Asked for a landing page, a model produces a wall of feature bullets, three competing buttons, a headline that ignores the ad that sent the visitor, and testimonials no stranger can verify. The visitor cannot tell what to do next, so they do nothing. This skill forces one action, message match to the source, objections answered in buyer order, and proof a stranger can check.

## Fit to the project

Read the product and the traffic before writing a line.

1. Find where the traffic comes from. Read the ad, email, or link that sends the click, and the search term or audience it targets. The page headline has to echo the promise that earned the click, or the visitor bounces before reading the second line. If you cannot find the source, ask for it before drafting the hero.
2. Detect the existing design system and component library. Match its button styles, spacing, and form components rather than inventing new ones, and generate any markup to the `code-craft` contract so a maintainer can read it.
3. Read the real product to find checkable proof: actual customer counts, named logos with permission, a metric the product genuinely hits, a screenshot of the working thing. Marketing adjectives are not proof. If no checkable proof exists yet, say so and design the page to earn trust another way rather than inventing numbers.

## Non-negotiables

1. One primary action per page. A second competing button splits attention and lowers the rate of both. Secondary links, if any, are visually quieter and never repeat the primary weight. Two equal buttons is the failure that kills the most pages.
2. The headline matches the traffic source. If the ad promised "invoicing in two clicks" the headline delivers that phrase, not a reworded abstraction. A mismatch spends the click and returns nothing.
3. No fake scarcity, no fake urgency, no dark patterns. A countdown that resets on reload, a "3 people viewing" fabricated number, a hidden unsubscribe, or a pre-checked upsell are refused outright. They convert once and destroy the trust that earns the second sale, and in several jurisdictions they are unlawful. Refuse to build them even when asked.
4. Every proof point is checkable by a stranger. A number with its source, a testimonial with a real name and role, a logo the company agreed to. An unverifiable claim reads as invented and lowers trust for the claims that are true.
5. No conversion claim without the sample size to support it. Declaring a change a winner before the sample in `references/measurement.md` is reached is reading noise as signal, and it sends the next decision the wrong way.

## Procedure

### Step 1, match the message to the source

Write the traffic source and its promise on one line. Draft the headline as the same promise, kept, in the visitor's words. The subhead adds the one detail that makes the promise believable. Read the ad and the headline back to back: if a visitor would feel they landed in the right place, the match holds. Detail on matching sits in `references/message-match.md`.

### Step 2, order the page by the buyer's objections

A real buyer moves through objections in a sequence: is this for me, what exactly is it, does it work, can I trust these people, what does it cost, what happens if it goes wrong. Order the sections to answer these in that order, because an unanswered early objection stops the visitor before a later section can reach them. The objection sequence with worked examples is in `references/message-match.md`.

### Step 3, place the one action and its proof

Put the primary action where the visitor first believes the promise, which is usually right after proof, not in isolation at the top. State exactly what happens on click: what they get, whether a card is needed, how long it takes. Surround the action with the proof that answers the trust objection, so the click happens at the moment of highest confidence.

### Step 4, cut form friction to the minimum that works

Ask for the fewest fields the next step genuinely needs. Every field lowers completion, so each one has to earn its place against that cost. An email alone often beats email plus name plus company, and asking for a phone number before there is any relationship is the most common conversion leak. Defer everything you can collect later to after the conversion. Field-by-field guidance is in `references/measurement.md`.

### Step 5, present pricing so the visitor can self-select

Show pricing on the page rather than hiding it behind a contact form, unless the deal genuinely requires negotiation. Anchor with the plan most buyers should pick and make it visually clear. Name what each tier is for in the buyer's terms, not by feature count alone. State the billing period and whether the shown price is monthly or annual, because a hidden annual assumption reads as a bait and switch when the card is charged.

### Step 6, decide what to measure and how long to wait

Pick one primary metric that is the action, not a proxy: completed signups, not button clicks. Before changing anything, record the current rate. When testing a change, compute the sample size needed to detect a real difference and wait for it before believing the result. The formula, a worked example, and the trap of stopping early are in `references/measurement.md`.

## Self-audit

- Does the page ask for exactly one primary action, with any secondary link visibly quieter?
- Does the headline repeat the promise of the traffic source in the visitor's words?
- Is every proof point checkable by a stranger, with a source, a real name, or a permitted logo?
- Is there zero fake scarcity, zero fabricated counts, and zero pre-checked upsell?
- Does the form ask only for fields the next step genuinely needs?
- Is the price and its billing period visible without a form, unless the deal truly needs negotiation?
- Is the primary metric the completed action rather than a click or a view?
- Is a required sample size written down before any change is called a winner?

## Honest limits

This skill shapes the page and its copy. It does not remove machine residue from the writing; run `human-prose` on the finished copy. It does not write long-form articles or the substance behind them, which is `content-craft`. Generated markup follows the `code-craft` contract but this skill does not own component architecture or accessibility depth, which are `frontend-build`.

It does not run the experiment or the analytics, and the sample-size guidance in `references/measurement.md` is a rule of thumb for a first read, not a substitute for a statistician on a high-stakes test. It does not plan the traffic or the campaign that sends visitors, which is `launch-plan`.

When the user says "stop", "just execute", or "skip the conversion checks", that is the off switch.
Build the page as asked and stop applying the checks for the rest of the session unless asked again.
The refusal of dark patterns in non-negotiable 3 is the one rule that stays even then.

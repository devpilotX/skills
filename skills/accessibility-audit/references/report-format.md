# Reporting findings

A finding is only useful if someone can fix it and later confirm it is fixed. Colour-coded scores and pass or fail badges fail both tests. Each finding names the barrier and the people it excludes.

## What automated tools catch and miss

Catch, reliably:

- Missing alt attributes and empty accessible names.
- Contrast below the ratio, for solid colours over solid backgrounds.
- Missing form labels where the association is programmatic.
- Missing document language, duplicate ids, some ARIA misuse.

Miss, and these are the ones that lock people out:

- Keyboard traps and broken tab order.
- Whether an accessible name is meaningful, not just present.
- Reading order that differs from visual order.
- Whether a status update is announced.
- Whether focus is managed on dialog open and close.
- Whether an error is actually associated with its field.

This is why a clean automated scan is a floor and not a pass. State that limit in the report.

## Finding template

Write each finding with these parts:

```
Criterion: 1.4.3 Contrast (minimum), Level AA
Surface: checkout form
Element: the "promo code" field label
Barrier: label text is grey #8a9099 on white, measured 2.9:1, below the 4.5:1 minimum.
Excludes: readers with low vision or colour vision deficiency cannot read the label.
Fix: change label colour to a token that clears 4.5:1 on white, for example #4a4f57.
Severity: serious.
```

The two parts models usually skip are the barrier and who it excludes. Without them a fixer guesses and a reviewer cannot confirm the fix.

## Severity, grouped so the worst is read first

- Blocker: a group cannot use a core function at all. A keyboard trap, an unlabelled submit button, a modal that cannot be closed by keyboard.
- Serious: a group can proceed but with significant difficulty. Poor contrast on body text, a form error not announced.
- Minor: an issue that affects some users in some cases. A redundant link, a heading level skipped in a low-traffic area.

List blockers first. A report sorted by page rather than by severity buries the issues that matter under the ones that do not.

## Report structure

1. Scope: the surfaces tested, the conformance target (for example WCAG 2.2 AA), and the assistive technology and browser pairs used.
2. Method: automated scan plus manual keyboard walk plus screen reader testing. State that manual testing was done so the report can support a conformance claim.
3. Findings, grouped by severity, each in the template above.
4. Appendix: raw automated tool output, kept separate from the conclusion.

## What to write when it passes

Do not write "accessible". Write what was tested and what was found:

```
Tested to WCAG 2.2 AA across the login, dashboard and settings surfaces,
by automated scan, full keyboard walk, and screen reader testing on two
screen reader and browser pairs. No blocker or serious findings. Three
minor findings listed below.
```

That sentence can back a claim. "This is accessible" cannot, because it names no target, no method and no coverage.

---
name: accessibility-audit
description: Check accessibility conformance rather than assert it, by walking the keyboard path, verifying visible focus, accessible names and roles, contrast including non-text, forms and error recovery, motion, headings and landmarks, and live regions against named WCAG success criteria. Use when someone claims an interface is accessible without checking, when an audit or VPAT is needed, when a keyboard or screen reader user reports a barrier, when a legal or procurement requirement cites WCAG, or before shipping a UI. Triggers on accessibility audit, is this accessible, WCAG compliance, screen reader testing, keyboard navigation broken, check contrast, a11y review, fix focus states, accessible forms, ADA compliance, VPAT, run an accessibility check, my site fails accessibility.
license: MIT
compatibility: Any web UI and, with platform equivalents, native apps. Automated checks assume a DOM; manual checks apply to any platform with a screen reader.
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Accessibility audit

A model asked whether an interface is accessible runs one automated scanner, sees zero errors, and reports that the interface passes. Automated tools catch at most a third to a half of WCAG issues, and the ones they miss are the ones that lock people out: a keyboard trap, an unlabelled icon button, a focus order that jumps around the page, an error shown only in red. This skill checks conformance against named success criteria and manual paths, and reports each finding as a barrier with the people it excludes, not a colour-coded score.

## Fit to the project

Read the interface and its target before testing.

1. Find the conformance target. Most legal and procurement requirements cite WCAG 2.1 or 2.2 Level AA. If no target is stated, test to 2.2 AA and say so. The criterion numbers below are stable public facts from the WCAG specification.
2. Detect the platform and its assistive technology. A web app pairs with a browser screen reader; a native app uses the platform screen reader. Pick the tools that match before writing steps.
3. List the interactive surfaces to cover: every form, dialog, menu, custom control, and any content that updates without a page load. Coverage is per surface, not per page.
4. Note any component library in use, since a known library often documents its own accessibility support and gaps worth verifying rather than assuming.

Any code you write to fix findings follows the `code-craft` contract: semantic elements first, one responsibility per file, no decorative markup.

## Non-negotiables

1. Every finding names the success criterion, the barrier, and who it excludes. A finding that says "improve accessibility" cannot be fixed or verified; one that says "1.4.3 fails at 3.1:1, low vision readers cannot read the label" can.
2. Never claim conformance from an automated scan alone. Scanners miss keyboard traps, focus order, meaningful names and reading order, so a clean scan reported as a pass is a false statement that exposes the project.
3. The full keyboard path is walked by hand, with no mouse, on every interactive surface. A control reachable only by mouse fails WCAG 2.1.1 and excludes every keyboard and switch user.
4. Focus is visible at every step and never lost. A removed focus outline fails 2.4.7 and a focus that lands nowhere after a dialog closes strands keyboard and screen reader users.
5. Contrast is measured, not judged by eye: 4.5:1 for normal text and 3:1 for large text under 1.4.3, and 3:1 for interactive component boundaries and meaningful graphics under 1.4.11.

## Procedure

### Step 1, run automated checks and record their limit

Run an automated checker across each surface and record what it reports. Then write the sentence that keeps the report honest: automated tools cover roughly a third to a half of criteria, so a clean scan is a floor, not a pass. Keep the tool output as an appendix, not as the conclusion.

### Step 2, walk the keyboard path end to end

Put the mouse away. Work from the criterion list in `references/wcag-checklist.md`. Tab through every surface and confirm you can reach and operate every control, that Enter and Space activate as expected, that Escape closes dialogs and menus, and that arrow keys work where a composite widget expects them (2.1.1). Confirm you can always tab back out, with no keyboard trap (2.1.2). Record the tab order and flag any place it does not match the visual order (2.4.3).

### Step 3, verify focus and names

Confirm a visible focus indicator at every step, clearing 3:1 against its background (2.4.7, 1.4.11). Then check every control has an accessible name that matches its visible label (4.1.2, 2.5.3): an icon button needs a name, a form field needs an associated label, a link needs text that means something out of context (2.4.4). Verify roles and states are correct for custom widgets, so a toggle reports pressed and a tab reports selected (4.1.2).

### Step 4, check forms and error recovery

For each form, confirm every field has a programmatic label (1.3.1, 3.3.2), that errors are identified in text and not by colour alone (1.4.1, 3.3.1), that the error is associated with its field and announced (3.3.1), and that the user can correct and resubmit without losing entered data (3.3.4 where it applies). Confirm required fields and formats are stated before submission, not only after failure.

### Step 5, check structure, motion and live regions

Verify one main landmark and a logical heading outline with no skipped levels (1.3.1, 2.4.6, 2.4.1 for a skip link). Confirm content and function do not depend on orientation (1.3.4) and reflow at 400 percent zoom without horizontal scroll (1.4.10). Confirm motion respects prefers-reduced-motion and that anything moving longer than five seconds can be paused (2.2.2, 2.3.3). Confirm dynamic updates use a live region so a screen reader announces them (4.1.3).

### Step 6, test with a screen reader by hand

Turn on the platform screen reader and work through each surface with the display where a sighted screen reader user would have it. Confirm the reading order matches the visual order (1.3.2), that names and roles are announced, that state changes are spoken, and that a status message reaches the user without moving focus. This step catches what no scanner reaches.

### Step 7, report each finding as a barrier

For each issue write the criterion number and level, the surface and element, what the barrier is, who it excludes, and the fix, using the template in `references/report-format.md`. Group by severity: blockers that lock a group out first, then serious, then minor. State the conformance target tested and that manual and screen reader testing were done, so the report can back a claim rather than assert one.

## Self-audit

- Does every finding name a WCAG success criterion, the barrier, and who it excludes?
- Was the full keyboard path walked by hand on every interactive surface?
- Is a visible focus indicator confirmed at every step and never lost after a dialog closes?
- Was contrast measured with a tool against 4.5:1, 3:1 and 1.4.11, not judged by eye?
- Does every form field have a label and every error appear in text, not colour alone?
- Was at least one full surface tested with a real screen reader?
- Does the report state the conformance target and that testing went beyond an automated scan?

## Honest limits

This checks conformance and reports barriers; it does not certify legal compliance or produce a signed VPAT, which a qualified accessibility professional owns. It does not design the fixes' visual values, which come from `ui-design`, nor build the components, which is `frontend-build` and `code-craft`. Testing with two screen readers does not prove every assistive technology works, since behaviour varies across screen reader and browser pairs.

Automated coverage figures here are a widely cited rule of thumb, not a measured property of a specific tool, so treat a clean scan as a floor and never as a pass.

## Off switch

Saying "stop", "just execute", or "skip the accessibility pass" is the off switch. Nothing further
is raised for the session unless you ask again.

---
name: ui-design
description: Make interface design decisions without a designer by producing concrete values instead of adjectives: a fixed spacing scale, a type scale with real sizes and line heights, colour chosen for contrast ratios first, and hierarchy built from size, weight and position. Use when you build a UI with no design file, when a screen looks unfinished or arbitrary, when spacing and font sizes were picked by eye, when interactive states are missing, or when someone asks to make a page look deliberate. Triggers on make this look better, design this page, pick fonts and colours, spacing looks off, choose a colour palette, this UI looks amateur, style this component, what font size, add hover and focus states, make it look professional, design without a designer, clean up the layout.
license: MIT
compatibility: Any UI stack, web or native, any framework or none. The values are unitless ratios and pixel figures you can map to rem, dp, pt or points.
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# UI design

A model asked to style a screen reaches for adjectives it cannot measure. It picks 13px here and 15px there, pads one card 12px and the next 20px, and chooses a blue that looks fine on the design machine and fails contrast for a fifth of readers. The result looks arbitrary because it is arbitrary, and no amount of shadow hides that the underlying numbers were never chosen. This skill replaces taste you do not have with values you can defend.

## Fit to the project

Read what the project already decided before inventing a scale.

1. Find the token or theme source: a Tailwind config, a CSS custom property block, a theme object, a variables file, or platform resource files. If a spacing or type scale exists, adopt it exactly and stop inventing.
2. Read two or three finished screens and record the real values in use: the font sizes, the gaps between elements, the corner radius, the two or three colours that carry the brand. Match them rather than introducing a parallel set.
3. Detect the platform density expectation. Web pointer targets differ from touch targets, and native platforms publish minimum sizes. Note which one applies before setting hit areas.
4. Where the project has settled nothing, take the scales in `references/scales.md` and say in your report which values you applied.

Generated markup is code, so it follows the `code-craft` contract: split by responsibility, named for what it is, no decorative dividers.

## Non-negotiables

1. Every spacing value comes from one scale, and every gap is a step on it. An arbitrary mix of 12, 15, 18 and 22 reads as unfinished because the eye detects the lack of a system even when it cannot name it.
2. Body text is at least 16px on the web with a line height between 1.4 and 1.6. Smaller loses readers with average eyesight, and a line height near 1.0 makes paragraphs collide.
3. Text contrast meets WCAG 1.4.3 before anything else about the colour is considered: 4.5:1 for normal text, 3:1 for text at 24px or 18.66px bold and above. A colour picked for looks that fails this excludes low vision readers and must be rejected.
4. Every interactive element defines rest, hover, focus, active and disabled, and focus is a visible ring, not a colour swap. A control with only a rest state gives no feedback and a keyboard user cannot see where they are.
5. Touch targets are at least 44 by 44px, pointer targets at least 24 by 24px per WCAG 2.5.8. A 20px icon button is missed by thumbs and fails the criterion.

## Procedure

### Step 1, set the spacing scale

Pick one base unit, 4px or 8px, and derive every space from it: 4, 8, 12, 16, 24, 32, 48, 64. Use 8px as the base for most screens and 4px only where dense data demands finer steps. Assign roles: 4 to 8 for space inside a control, 16 to 24 between related elements, 32 to 64 between sections. From now on a gap is a scale step or it is wrong.

### Step 2, set the type scale

Choose a base body size, 16px on the web, and build sizes on a ratio near 1.25: 16, 20, 25, 31, 39, or round to 16, 20, 24, 32, 40 for cleaner figures. Set line height by role: 1.5 for body, 1.25 for headings, 1.4 for captions. Limit weights to two or three, such as 400 for body, 600 for emphasis, 700 for headings. A page with five font sizes chosen by eye looks noisier than one with four sizes from a ratio.

### Step 3, choose colour by contrast first

Start from the two or three functional colours: a text colour, a background, and one accent. Test each text on background pair against the ratios in rule 3 before judging the hue. Build a neutral ramp of five to seven greys for borders, backgrounds and muted text, and check that muted text still clears 4.5:1. Reserve the accent for one job, usually the primary action, so it keeps meaning. Non-text contrast for borders and icons meets WCAG 1.4.11 at 3:1.

### Step 4, build hierarchy from size, weight and position

Rank the content on each screen: what a reader sees first, second, third. Express that rank with size and weight, not colour alone, since colour hierarchy vanishes for colour blind readers. Put the most important element where the eye lands first, top left in left to right layouts. One primary action per view, styled as the accent; everything else is secondary or a plain link.

### Step 5, define every interactive state

For each control write all five states from rule 4, using the state list and worked button in `references/states.md`. Hover shifts background or elevation by a small step. Focus draws a 2px ring with a 2px offset that clears 3:1 against its neighbour. Active presses in. Disabled drops opacity to around 40 percent and removes the pointer. States are code, so keep them in one place per component per the `code-craft` contract.

### Step 6, set density, alignment and optical spacing

Choose a target size from the platform detected in Fit to the project. Align elements to a shared edge so labels, inputs and buttons share a left or baseline. Correct optical spacing where math lies: a circle or triangle needs slightly more padding than a square to look equally inset, and text next to an icon often needs 1 to 2px less than the scale gap to look balanced.

### Step 7, restrain motion

Use motion to explain a change, not to decorate. Keep transitions between 150 and 300ms, with 200ms as a default; anything over 400ms feels slow. Ease out for entrances, ease in for exits. Respect reduced motion by cutting non-essential animation to an instant crossfade. One or two moving things at once, never a screen that all animates.

## Self-audit

- Does every spacing value map to a single named scale step?
- Is body text at least 16px with line height between 1.4 and 1.6?
- Does every text and background pair meet 4.5:1, or 3:1 for large text?
- Does each interactive element define rest, hover, focus, active and disabled?
- Is focus shown as a visible ring rather than only a colour change?
- Are touch targets at least 44px and pointer targets at least 24px?
- Is there exactly one primary action styled as the accent per view?
- Are transition durations between 150 and 300ms with reduced motion handled?

## Honest limits

This produces a defensible baseline, not a brand identity; logo, illustration and voice belong to a human designer or brand owner. It does not verify conformance end to end, only sets values that can pass; `accessibility-audit` owns proving a built interface meets WCAG. It does not manage tokens and component contracts at scale, which is the job of `design-system`, and the framework wiring and data states sit with `frontend-build`.

The scales here are rules of thumb drawn from common practice, not measured findings, so a project with different constraints should pick different numbers and record them.

## Off switch

Saying "stop", "just execute", or "skip the design pass" is the off switch. It stays off for the rest of the session unless you ask again. A skill that keeps restyling after being told to stop gets uninstalled.

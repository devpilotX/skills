# WCAG checklist by manual check

Criterion numbers are from the WCAG specification and are stable public facts. Levels are marked A or AA. This is a working checklist for a Level AA audit, ordered by the manual check that finds each issue.

## Keyboard

- 2.1.1 Keyboard (A): every function works from the keyboard.
- 2.1.2 No keyboard trap (A): focus can always move away from a component.
- 2.1.4 Character key shortcuts (A): single-key shortcuts can be turned off or remapped.
- 2.4.3 Focus order (A): tab order follows a meaningful sequence.
- 2.4.7 Focus visible (AA): a visible focus indicator on every focusable element.
- 2.4.11 Focus not obscured, minimum (AA, 2.2): the focused element is not fully hidden by other content.

## Names, roles, values

- 1.1.1 Non-text content (A): images and icons have text alternatives.
- 2.4.4 Link purpose in context (A): link text means something.
- 2.5.3 Label in name (A): the accessible name includes the visible label text.
- 4.1.2 Name, role, value (A): custom controls expose correct role, name and state.

## Contrast and use of colour

- 1.4.1 Use of colour (A): colour is not the only way information is conveyed.
- 1.4.3 Contrast, minimum (AA): 4.5:1 for normal text, 3:1 for large text (24px, or 18.66px bold).
- 1.4.11 Non-text contrast (AA): 3:1 for interactive component boundaries and meaningful graphics.

## Forms

- 1.3.1 Info and relationships (A): labels are programmatically associated with fields.
- 3.3.1 Error identification (A): errors are described in text.
- 3.3.2 Labels or instructions (A): fields have labels and format hints before submission.
- 3.3.3 Error suggestion (AA): a correction is suggested where known.
- 3.3.4 Error prevention (AA): for legal, financial or data changes, submissions are reversible, checked or confirmed.

## Structure and reflow

- 1.3.2 Meaningful sequence (A): reading order matches visual order.
- 2.4.1 Bypass blocks (A): a skip link or landmark to jump repeated content.
- 2.4.6 Headings and labels (AA): headings and labels describe topic or purpose.
- 1.4.10 Reflow (AA): content reflows at 320 CSS pixels wide without horizontal scroll, which maps to 400 percent zoom.
- 1.3.4 Orientation (AA): content is not locked to one orientation.
- 1.4.4 Resize text (AA): text scales to 200 percent without loss of content.

## Motion and time

- 2.2.1 Timing adjustable (A): time limits can be extended or turned off.
- 2.2.2 Pause, stop, hide (A): moving content over five seconds can be paused.
- 2.3.1 Three flashes (A): nothing flashes more than three times per second.
- 2.3.3 Animation from interactions (AAA, worth checking): respect prefers-reduced-motion.

## Dynamic updates

- 4.1.3 Status messages (AA): status messages are announced without moving focus, via a live region.

## Contrast quick reference

- Normal text: 4.5:1.
- Large text (24px, or 18.66px bold): 3:1.
- Interactive boundaries, focus rings, meaningful icons: 3:1.
- Decorative graphics and disabled controls: no minimum.

Measure with a contrast tool. Do not judge by eye, and do not trust a token name that says "muted" to be safe on a coloured background.

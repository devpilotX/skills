# Default scales

Use these when the project has settled nothing. They are rules of thumb from common practice, not measured findings. Record which ones you applied.

## Spacing scale

Base unit 8px. Steps: 4, 8, 12, 16, 24, 32, 48, 64, 96.

Roles for each step:

- 4px: gap between an icon and its label, tight inset in dense tables.
- 8px: padding inside a small control, gap between a label and its input.
- 12px: padding inside a button, gap between list rows.
- 16px: default padding inside a card, gap between related fields.
- 24px: gap between groups of fields, padding inside a large card.
- 32px: gap between distinct blocks on a page.
- 48px: gap between page sections.
- 64px and 96px: top and bottom of a page, hero spacing.

If a screen is data dense, drop to a 4px base and use 4, 8, 12, 16, 20, 24. Do not mix two bases on one screen.

## Type scale

Base body 16px, ratio near 1.25 rounded for clean figures.

- 12px: fine print, captions, table metadata. Line height 1.4.
- 14px: secondary text, helper text. Line height 1.5.
- 16px: body. Line height 1.5.
- 20px: lead paragraph, small heading. Line height 1.4.
- 24px: section heading. Line height 1.3.
- 32px: page heading. Line height 1.25.
- 40px: display heading. Line height 1.2.

Weights: 400 for body, 600 for emphasis and small headings, 700 for large headings. Three weights cover almost every screen.

Line length for reading sits between 45 and 75 characters per line. Constrain body text width to roughly 60 characters where the layout allows.

## Neutral ramp

Seven greys give borders, backgrounds and muted text without inventing new values per screen. Sample values for a light theme:

- Grey 0: #ffffff, page background.
- Grey 1: #f4f5f7, subtle surface.
- Grey 2: #e4e6eb, hairline border.
- Grey 3: #c7cbd1, strong border.
- Grey 4: #8a9099, disabled text, must not be used for body text on white since it clears large text only.
- Grey 5: #4a4f57, muted body text, clears 4.5:1 on white.
- Grey 6: #1f2329, primary text.

Check any pair you rely on with a contrast tool rather than trusting these labels on a coloured background.

## Radius and elevation

Corner radius: 0 for full bleed, 4px for inputs and buttons, 8px for cards, 12px for modals. Pick one radius per element type and keep it.

Elevation by shadow, three levels only. Resting cards flat or level 1, raised menus level 2, modals level 3. Each level is one small step in blur and vertical offset, for example 0 1px 2px, 0 4px 8px, 0 12px 24px, all with low opacity black. More than three levels reads as noise.

## Motion durations

- 100ms: state change on a small control, such as a hover background.
- 200ms: default transition, panel open, tab switch.
- 300ms: larger movement, a drawer sliding in.
- Over 400ms: avoid for interface feedback; it reads as lag.

Ease out for entrances, ease in for exits, ease in out for movement that both enters and settles. Under a reduced motion preference, replace slides and scales with an instant or 80ms crossfade.

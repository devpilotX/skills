# Token layers and naming

This file holds the layering model and a naming grammar to apply when a project has none.

## Three layers

Layer one, raw values. Descriptive names tied to the value, changed rarely. These are the palette and the scale.

```
blue-500: #1d4ed8
grey-900: #1f2329
space-4: 16px
radius-2: 8px
```

Layer two, semantic tokens. Named by role, pointing at layer one. Components read these. Theming repoints these and nothing else.

```
color-action: blue-500
color-text-primary: grey-900
space-inset-card: space-4
radius-card: radius-2
```

Layer three, component tokens. Optional, scoped to one component, pointing at layer two.

```
button-bg: color-action
button-padding-x: space-inset-card
```

The rule that makes this work: a component never reads layer one. If a button uses `blue-500` directly, a rebrand or a dark theme cannot reach it, and you are back to hunting hardcoded values.

## Why role names survive a rename

A token named for its appearance encodes an assumption that will break.

- `blue-500` breaks when the brand colour becomes green. Every consumer now reads a token whose name lies.
- `margin-16` breaks when the spacing changes to 12px, so either the name lies or you rename across the codebase.
- `header-blue` breaks when the same colour is needed in a footer, so the name no longer describes where it is used.

A role name does not encode any of that. `color-action` stays true when the hue changes, `space-inset-card` stays true when the value changes, and `color-text-primary` stays true wherever text appears.

## Naming grammar

Order the parts consistently: category, role, variant, state.

- Category: color, space, size, radius, shadow, font, duration, z.
- Role: what it is for. text, background, border, action, surface, inset, stack.
- Variant: a distinction within the role. primary, secondary, subtle, sm, md, lg.
- State: only when the token itself is stateful. hover, focus, active, disabled.

Examples that follow the grammar:

```
color-text-primary
color-text-muted
color-background-surface
color-border-focus
color-action
color-action-hover
space-inset-sm
space-stack-md
radius-card
font-size-body
duration-fast
```

Avoid: value in the name (`color-1d4ed8`, `margin-16`), place in the name (`sidebar-bg`, `header-blue`), and abbreviations that need a legend (`clr-txt-pri`). Write the grammar into the token file header so the next contributor extends it the same way.

## Dark mode as a layer two swap

If components read only layer two, a theme is a second set of layer two definitions pointing at the same or different layer one values.

```
light:
  color-text-primary: grey-900
  color-background-surface: grey-0
dark:
  color-text-primary: grey-50
  color-background-surface: grey-900
```

No component changes. This is the payoff for keeping raw and semantic layers apart, and the reason a component reading a raw hex forces a rewrite when dark mode arrives.

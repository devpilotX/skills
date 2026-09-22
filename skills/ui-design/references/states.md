# Interactive states and worked example

Most generated interfaces ship a rest state and nothing else. This file lists the states each control owes a user and shows one worked button.

## States every interactive element owes

- Rest: the default look.
- Hover: pointer is over the element. Shift background or elevation by one small step. Not available on touch, so never hide meaning behind it.
- Focus: the element has keyboard focus. Draw a visible ring, 2px wide with a 2px offset, clearing 3:1 contrast against the adjacent colour per WCAG 1.4.11. Never remove focus outlines without replacing them.
- Active: the element is being pressed. Press it in with a darker background or a 1px downward shift.
- Disabled: the element cannot be used. Drop opacity to around 40 percent, remove the pointer cursor, and remove it from the tab order only if a reason to keep it announced does not apply.

Extra states some controls need:

- Selected or checked, for toggles, tabs and list items.
- Loading, for a button that triggers an async action; show a spinner and block a second press.
- Error and valid, for form fields, shown with an icon or text and not colour alone.
- Read only, distinct from disabled, where the value shows but cannot change.

## Worked example, a primary button

Values reference the default scales file. Colours are placeholders; test them against the real theme.

```css
.button-primary {
  font-size: 16px;
  line-height: 1.5;
  font-weight: 600;
  padding: 12px 24px;
  min-height: 44px;
  border-radius: 4px;
  color: #ffffff;
  background: #1d4ed8;
  border: 1px solid transparent;
  cursor: pointer;
  transition: background 200ms ease-out;
}

.button-primary:hover {
  background: #1a45bd;
}

.button-primary:focus-visible {
  outline: 2px solid #1d4ed8;
  outline-offset: 2px;
}

.button-primary:active {
  background: #163ba0;
}

.button-primary:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

@media (prefers-reduced-motion: reduce) {
  .button-primary {
    transition-duration: 80ms;
  }
}
```

Check the text on background pair: white on #1d4ed8 clears 4.5:1 for normal text. Check the focus ring against the surrounding page colour, not against the button, since the ring sits outside the button.

## Optical spacing corrections

Geometry and perception disagree in a few places worth correcting by hand:

- A circular or triangular icon looks smaller than a square of the same bounding box. Give it 1 to 2px more visual size or padding to match.
- Text set next to an icon usually needs 1 to 2px less than the scale gap, because the icon has visual whitespace built in.
- Optical alignment of a play triangle inside a round button shifts the triangle right by 1 to 2px, because its visual centre is left of its geometric centre.
- Capital letters and numerals sit above the baseline with different overshoot than round letters. Align to the baseline, not the bounding box, when placing text next to shapes.

These are small, and they are the difference between a layout that looks measured and one that looks almost right.

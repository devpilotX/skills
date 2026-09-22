# View states and keyboard audit

The main file requires five states on every data view and a keyboard path verified by tabbing. This file
turns those into concrete checks: what each state has to render for common view types, and the keyboard
audit to run before claiming an interface works.

## The five states, per view type

Every view that fetches data has to answer all five. The success state is the one that usually gets built
alone, and the other four are where users land first.

### List or table

Loading: a skeleton or a spinner that reserves the final layout so the page does not jump when data lands.
Empty: a message that says nothing matched and, where it helps, an action to clear a filter or add the first
item. An empty list is not an error.
Error: a message the user can act on, plus a retry control. Never a blank screen or a raw error string.
Partial: when some rows load and one fails, show what arrived and mark the gap, rather than dropping the whole
list.
Success: the rows, with pagination or virtualisation if the list can grow long.

### Detail page

Loading: a skeleton matching the real layout, not a centered spinner that shifts everything on load.
Empty: for a record that does not exist, a not found state distinct from an error, because the fix differs.
Error: distinguish a failed fetch, which offers retry, from a forbidden record, which offers a way back.
Partial: when the main record loads but a secondary panel fails, render the record and show the panel in its
own error state.
Success: the record.

### Form

Loading: disable submission while initial data loads so the user cannot submit an empty form.
Empty: for a create form, sensible defaults and a clear primary action.
Error: field level errors linked to their input and a form level error for a failed submit, both announced to
assistive technology, not only coloured.
Partial: on a validation failure, keep every value the user typed. Losing input on error is a defect users
remember.
Success: a confirmation, and either a redirect or a cleared form, decided deliberately.

### Dashboard

Loading: each widget shows its own loading state so one slow query does not blank the page.
Empty: a widget with no data says so in place rather than rendering an empty chart.
Error: one widget failing shows its own error and leaves the rest of the dashboard usable.
Partial: this is the normal state of a dashboard, since widgets load independently. Design for it, do not
treat it as an edge case.
Success: all widgets populated.

## Keyboard audit

Run this with the mouse untouched, before claiming the interface works.

1. Tab from the top. Focus moves in reading order and never jumps somewhere surprising.
2. Every interactive element receives focus and shows a visible focus ring. A control you cannot reach by tab
   is not operable.
3. Buttons and links activate with Enter, and buttons also with Space. A div with a click handler will not,
   which is why semantic elements come first.
4. A menu or dropdown opens with the keyboard, moves through options with the arrow keys, and closes with
   Escape.
5. A dialog traps focus while open, returns focus to the trigger on close, and closes with Escape.
6. On route change, focus moves to the new content or a heading, so a screen reader announces the new page
   instead of leaving focus on the old link.
7. Focus order still makes sense at 200 percent zoom and on a small viewport, where layout reflows.

Any step that fails is a bug to fix during the build, because retrofitting it changes markup structure and
costs several times more later.

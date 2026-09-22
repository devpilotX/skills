# Frontend checklist

## Forms

Validate on blur for each field, and on submit for the whole form. Validating on every keystroke tells
people their email is invalid while they are typing it.

Show the error next to the field, linked to it programmatically so a screen reader announces it. Colour
alone is not an error message.

Disable the submit control while the request is in flight, and say what is happening. A form with no
submission feedback gets submitted three times.

Make submission idempotent on the server. The client will send it twice regardless of what the button
does.

Preserve what the user typed when submission fails. Clearing a form on error is the fastest way to lose
a user.

Warn before navigating away from unsaved changes, and do not warn when nothing changed.

Use correct input types and autocomplete attributes, so browsers and password managers work. This is a
small change with a large effect on completion rates.

Never disable paste on a password or code field.

Handle the case where the server rejects something the client considered valid, because the server is
the authority and its message has to be displayable.

For multi step forms, keep state where a refresh does not destroy it.

## Loading and error states

Show a skeleton matching the eventual layout, so content arriving does not shift the page.

Distinguish empty from loading from error. All three commonly render as a blank area.

Empty states say what it is, why it is empty, and what to do about it. An empty table with no message
looks broken.

Errors say what failed and what the user can do. A retry control belongs on anything transient.

Partial failure needs its own handling. When one of four panels fails, three should still work.

Time out a request rather than showing a spinner forever.

Handle the stale case, where data loaded and is now out of date, which needs a refresh affordance rather
than an error.

## Lists and tables

Paginate or virtualise anything unbounded. A list that works with fifty rows will be tried with fifty
thousand.

Put sort, filter and page in the URL so the view can be shared and survives a refresh.

Keep row actions reachable by keyboard.

Provide a loading state that does not collapse the layout.

Say how many results there are, and what the filter excluded.

## Responsive behaviour

Design the narrow viewport first, since it forces priority decisions that the wide layout hides.

Test at 200 percent zoom, which is a common accessibility requirement and breaks fixed heights.

Touch targets large enough to hit, with spacing between them.

Nothing important behind hover, because touch devices have no hover.

Test with long strings and with a language that expands.

## Client performance

Measure with the profiler and a throttled network before changing anything, and report the numbers.

Ship less JavaScript before optimising the JavaScript you ship.

Split by route, and lazily load anything below the fold or behind an interaction.

Serve images at display size in a modern format, with width and height set to reserve space.

Reserve space for anything that loads late, including fonts and advertisements, to avoid layout shift.

Fetch at the route level rather than deep in the tree, to avoid request waterfalls.

Debounce input driven requests, and cancel superseded ones.

Apply memoisation to a measured re-render problem, not as a habit.

## Dependencies

Check the installed size, not the published size, and state it in kilobytes.

Check whether the platform already does it. Date formatting, unique identifiers, deep cloning, fetching
and form state all have native or near native options now.

Check maintenance status and how many transitive dependencies arrive with it.

Prefer one utility you understand over a framework you adopt for one function.

## Before calling it done

Keyboard only pass through every path, including modals and menus.

Small viewport pass.

Throttled network pass.

Failing API pass, and an API returning the wrong shape.

Empty data pass.

Console clean of errors and warnings.

No secret or internal endpoint visible in the shipped bundle.

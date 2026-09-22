# Components and versioning

This file covers what earns a component, variants versus overrides, and how to ship a breaking change without breaking consumers.

## What earns a component

The rule of three: build a component when the same structure and behaviour repeats in three or more places. Below that, a copied block is cheaper than an API you must maintain for a single caller.

Signals that something has earned a component:

- The same markup appears in three files with only content differences.
- A team keeps re-deriving the same states, such as loading and error, for the same shape.
- A visual detail must stay consistent across surfaces, such as the primary button.

Signals it has not:

- One screen uses it once and no other screen is planned to.
- The variations between instances are so large that the shared part is a div.
- Wrapping it would need more props than the markup it replaces.

## Variants versus overrides

Prefer a small set of named variants over a pile of booleans. Four boolean props (`primary`, `large`, `disabled`, `loading`) allow sixteen combinations, most untested and some contradictory. A single `variant` prop with named values (`primary`, `secondary`, `ghost`) and a `size` prop keeps the surface small and the combinations meaningful.

Design the API around real needs, not today's screen. Ask what a caller must decide (the intent, the size, whether it is loading) and expose those. Do not expose internal layout details as props, since those become a contract you cannot change later.

Allow a one-off override through a documented escape hatch, such as a `className` or `style` prop, so an unusual case does not force a new variant into the shared API. State in the docs that the escape hatch is for exceptions and that a pattern used three times should become a variant.

## Documentation that gets read

For each public component, document in a file next to the code:

- What it is for, in one or two sentences.
- Its props, each with a type and a default.
- Its states, including loading, error and disabled where they apply.
- One copyable usage example.

Documentation in a separate wiki drifts out of date because it updates on a different schedule than the code. Documentation beside the component gets edited in the same commit that changes the component.

## Versioning and breaking changes

Use semantic versioning:

- Patch (1.0.x): a fix that changes nothing about the API.
- Minor (1.x.0): additive. A new component, a new optional prop, a new variant value.
- Major (x.0.0): anything that can break a consumer. A removed or renamed prop, a changed default, removed markup, a changed token name.

Ship a breaking change in three moves:

1. In a minor release, add the new API alongside the old and mark the old deprecated with a warning that names the replacement.
2. Give consumers at least one release cycle to migrate.
3. In the next major release, remove the old API and publish a migration note.

A migration note names the old API, the new API, and the mechanical change. Where the change is search and replace, include the pattern so a consumer can run it. Example:

```
Renamed prop `color` to `variant` on Button.
Old: <Button color="primary">
New: <Button variant="primary">
Codemod: replace `color=` with `variant=` on Button elements.
```

## Adoption without a big-bang rewrite

Do not rewrite every screen at once; that stalls and gets reverted. Instead:

1. Introduce the tokens and one reference surface built the new way.
2. Make new work use the system by default.
3. Migrate existing surfaces by replacing raw values with semantic tokens first, then swapping copied markup for components.
4. Track progress by counting remaining hardcoded colour and spacing values over time. The count going to zero is the adoption metric.

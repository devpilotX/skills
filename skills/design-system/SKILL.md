---
name: design-system
description: Build tokens and components with the discipline that keeps them usable: naming that survives a rename, token layers from raw value to semantic role, a rule for what earns a component, and a versioning plan for breaking changes. Use when a codebase has drifted into copies of the same button, when colours and spacing are hardcoded everywhere, when you plan a shared component library, when tokens need naming, or when a team asks whether a design system is worth it yet. Triggers on build a design system, create design tokens, shared component library, name our tokens, stop duplicating components, theme our app, versioning the component library, migrate to tokens, is a design system worth it, semantic colour tokens, component API design, breaking change in the library.
license: MIT
compatibility: Any stack that renders UI, web or native, any framework. Tokens map to CSS variables, a theme object, platform resources or a JSON source.
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Design system

A model asked for a design system builds a component for every element on the current screen, names tokens after the colours they hold today, and ships no versioning story. Six months later `blue-500` is green because the brand changed, `Card` has fourteen boolean props, and half the app still uses copied markup because migration was never planned. The failure is not the tokens or the components; it is the missing discipline around naming, layering and change. This skill supplies that discipline and, first, tells you when not to build one at all.

## Fit to the project

Read the codebase before proposing a single token.

1. Count the real duplication. Search for repeated colour hex values, repeated spacing numbers, and copied component markup. A design system is justified by duplication that exists, not by duplication you imagine.
2. Find the existing theme mechanism: CSS custom properties, a theme object, Tailwind config, platform resource files. Build on it rather than introducing a second system beside it.
3. Detect the consumer count. One app with one team needs far less than a token pipeline; several apps sharing a brand need the full layering. Size the system to the number of consumers.
4. Where nothing exists and duplication is real, use the layer and naming rules below and record your choices in the report.

Everything here emits code, so generated tokens and components follow the `code-craft` contract: one responsibility per file, names that say what the value is, no decorative dividers.

## Non-negotiables

1. Name tokens by role, never by appearance. `color-text-primary` survives a rebrand; `blue-900` becomes a lie the day the brand changes and every consumer inherits the lie.
2. Keep raw values and semantic tokens in separate layers. A component that reads a raw hex instead of a semantic token cannot be themed, and dark mode becomes a rewrite.
3. A component earns its place only when the same structure and behaviour repeats in three or more places. A one-off wrapped as a component adds an API to maintain for a single caller and slows every future change.
4. Breaking changes ship behind a version bump with a migration note, never as a silent edit. A renamed prop or a changed default that lands without warning breaks consumers at their next install and destroys trust in the library.
5. Every public component documents its props, its states and one usage example. An undocumented component gets copied instead of imported, which recreates the duplication the system was meant to remove.

## Procedure

### Step 1, decide whether to build one at all

If the project is one app, one team, and duplication fits on a screen, a single stylesheet or one theme file is the correct answer and a design system is premature. Write that conclusion and stop. Build a system only when duplication is real and more than one surface or team consumes the same UI. Record the trigger that justified it.

### Step 2, define the token layers

Use three layers, detailed with a naming grammar in `references/token-layers.md`. Layer one is raw values with descriptive names: `blue-500`, `space-4`, `size-16`. Layer two is semantic tokens that point at layer one by role: `color-action`, `color-text-primary`, `space-inset-card`. Layer three is optional component tokens for a specific component: `button-padding-x`. Components read layer two or three, never layer one. Theming happens by repointing layer two, so dark mode changes one file.

### Step 3, name so the name survives a rename

Name by what the token is for, not what it looks like or where it sits today. Use a consistent order: category, role, variant, state, such as `color-text-primary`, `color-border-focus`, `space-inset-sm`. Avoid names that encode a value (`margin-16`) or a place (`header-blue`), because both break the moment the value or the place changes. Write the naming grammar down so the next contributor extends it the same way.

### Step 4, decide what earns a component and what stays an override

Apply the rule of three from non-negotiable 3; the full reasoning, variant guidance and versioning moves are in `references/components-and-versioning.md`. When something repeats enough to be a component, design its API around variants and props that map to real needs, not to today's screen. Prefer a small set of named variants over a pile of booleans; four booleans allow sixteen states, most of which are untested. Allow a one-off override through a documented escape hatch, such as a class or style prop, so a single unusual case does not force a new variant.

### Step 5, document so it gets read

For each public component write what it is for, its props with types and defaults, its states, and one copyable example. Keep the doc next to the component so it updates with the code. Put the token catalogue in one place a consumer can scan. Documentation that lives in a separate wiki drifts; documentation next to the code survives edits.

### Step 6, version and plan the breaking change

Adopt semantic versioning: patch for fixes, minor for additive changes, major for anything that breaks a consumer. For a breaking change, ship a deprecation warning one minor version ahead where possible, then remove in the major with a migration note that names the old and new API. A codemod or a search and replace recipe in the note turns a day of consumer work into minutes.

### Step 7, plan adoption and migration

Do not rewrite every screen at once. Introduce the system, migrate one high traffic surface as the reference, and let new work use it by default. Track adoption by counting remaining hardcoded values over time. Migrate by replacing raw values with semantic tokens first, then swapping copied markup for components, so themeability lands before the larger refactor.

## Self-audit

- Is every token named by role rather than by its current appearance?
- Are raw values and semantic tokens in separate layers, with components reading only semantic or component tokens?
- Was each component justified by the same structure repeating in three or more places?
- Does every public component document its props, states and one example?
- Does the change plan use semantic versioning with a migration note for breaking changes?
- Is there a documented escape hatch for one-off overrides?
- Does the report state whether a design system was justified or premature, and why?

## Honest limits

This owns tokens, component contracts and the change discipline around them; it does not choose the visual values themselves. The spacing scale, type scale and contrast ratios come from `ui-design`, and proving a built component meets WCAG belongs to `accessibility-audit`. Framework wiring, state placement and data states sit with `frontend-build`, and the internal code quality of each component follows `code-craft`.

The rule of three and the layer count are rules of thumb from common practice, not measured findings. A project with more consumers or a stricter brand may need more layers; one with fewer needs fewer.

## Off switch

Saying "stop", "just execute", or "no system, just a stylesheet" is the off switch. That holds for
the session unless you reopen it.

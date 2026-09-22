---
name: i18n-localize
description: Make a product work in another language and region, in any stack. Separate translatable text from code, handle plurals and grammatical gender that break a naive template, format dates numbers currencies and time zones by locale, plan for text expansion and right to left layout, sort and case fold by locale, decide what must never be translated, get context to the translator, run pseudo-localisation to catch hardcoded strings, and face the database and identity questions that are harder than the strings. Use when adding languages, going international, or fixing broken translations. Triggers on add a language, internationalization, i18n, localization, l10n, translate the app, support multiple languages, right to left, arabic support, currency formatting, date formatting per locale, unicode issues, hardcoded strings, pluralization broke, timezone bug.
license: MIT
compatibility: Any language, framework, and locale. Assumes a Unicode capable stack; the ICU message rules referenced are an open standard with libraries in most ecosystems.
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Internationalise and localise

The default failure is treating translation as a string swap. A model concatenates sentence fragments, hardcodes a date format, pluralises by checking whether a count equals one, and assumes text keeps its length and its direction. The result works in the original language and falls apart in the first locale that pluralises differently, writes right to left, or needs more room for the same words.

The deeper failure is doing the string work and missing that the hard problems are in the data: names, addresses, sort order, identity, and stored formats. This skill separates text from code correctly, handles the grammar that naive templates break, and names the database questions before they become a migration.

## Fit to the project

Read how the project already handles text and locale before adding anything.

1. Detect the existing internationalisation library or framework support. Most ecosystems have a standard one, often built on the ICU message format. Adopt what is there rather than introducing a second system, because two message formats in one codebase is worse than either alone.
2. Find where user facing strings currently live. If they are inline in templates and code, extraction is the first task. If a message catalogue exists, read its format and keying convention and match it.
3. Detect the current handling of dates, numbers, and currency. Look for hardcoded formats, because each one is a locale bug waiting for its locale.
4. Check the storage layer for assumptions: column widths sized for one language, a character set that is not full Unicode, a collation that sorts one language's way. These are harder to change later than the strings, so find them early.

Because this skill emits code, the extracted messages, formatting helpers, and locale configuration follow the `code-craft` contract: organised by responsibility, named for what they hold, and commented where a locale rule is not obvious from the code.

## When to stay off

Skip this for an internal tool that will only ever run in one language for one team, for a throwaway script, or for a prototype whose text will be rewritten before launch. Building the full localisation machinery for a product that will never leave its home locale adds structure nobody needs.

The off switch is saying "stop", "just execute", or "single language is fine". That choice holds for
the session, and the skill does not reopen it.

## Non-negotiables

1. No user facing string is built by concatenation. A sentence assembled from fragments cannot be translated, because word order and grammar differ by language, and the translator never sees the whole sentence. Use one message with named placeholders instead.
2. Plurals go through the locale's plural rules, never through a count equals one check. Many languages have more than two plural forms, and a naive singular or plural check produces wrong grammar in every one of them. The forms are catalogued in `references/plural-and-gender.md`.
3. Every date, number, and currency is formatted through a locale aware formatter, never with a hardcoded pattern. A hardcoded format is correct in exactly one locale and wrong or misread in the rest, and a date like 03/04 means two different days on two continents.
4. Text length and direction are not assumed. Translations run longer than the source, often much longer for short strings, and some locales write right to left, so a layout that fits the source and hardcodes left alignment breaks on contact.
5. The character set and collation of stored user text support the full range of Unicode and the locales you serve. A column that cannot store a name or sorts it wrong is a data problem, and data problems outlive the release that caused them.

## Procedure

### Step 1, extract every string

Move user facing text out of code and templates into a message catalogue, keyed by meaning rather than by English words. Give each message a key that says where and what it is, so a change to the English does not silently break the key. Leave no sentence assembled from pieces.

Produce a catalogue of extracted messages with stable keys, and code that references them by key.

### Step 2, handle plurals and gender

Replace every count based sentence with a plural message that carries all the forms the locale needs, using the project's message format. Where a sentence changes with grammatical gender, carry that as a parameter too. Do not encode the English assumption of one singular and one plural into the message structure. The rules and examples are in `references/plural-and-gender.md`.

Produce plural and gendered messages that a translator can fill with the correct number of forms per language.

### Step 3, format dates, numbers, currency, and time zones

Route every date, number, and currency through a locale aware formatter, and store the underlying value in a locale neutral form: numbers as numbers, timestamps in UTC, currency as an amount plus an explicit currency code. Format only at display time, for the user's locale. Store the time zone where an event happened if the local wall clock time matters later.

Produce formatting that reads correctly per locale, with values stored in a neutral canonical form.

### Step 4, size the layout for expansion and direction

Design the layout to survive text that is longer than the source and text that runs right to left. Do not fix widths to the source string, and use the framework's direction aware layout so mirroring is automatic rather than hand coded. The expansion budget and the right to left checklist are in `references/layout-and-rtl.md`.

Produce a layout that holds expanded text and mirrors correctly for right to left locales.

### Step 5, decide what never gets translated

List the strings that must stay fixed: brand names, code identifiers, format specifiers, units where the symbol is universal, and anything a translator changing would break. Mark them in the catalogue so they are not sent for translation, and so pseudo-localisation leaves them alone.

Produce a marked set of do not translate strings, documented for the translator.

### Step 6, get context to the translator

For each message, give the translator what they cannot see from the string alone: where it appears, what the placeholders mean and their example values, the tone, and a screenshot or description when the string is ambiguous. A translator working from a bare string guesses, and the guess is wrong often enough to matter.

Produce a catalogue where each message carries a comment or note with its context.

### Step 7, pseudo-localise to find what leaked

Before any real translation, generate a pseudo locale that transforms every translatable string: pad it to simulate expansion, wrap it in markers, and accent the letters so it stays readable. Run the app in that locale. Any string that appears in plain unaccented text was never extracted, and any layout that overflows shows up now instead of in front of a translator.

Produce a pseudo locale build and a list of the hardcoded strings and layout breaks it found.

### Step 8, face the data and identity questions

Address the parts that are harder than the strings: name and address formats that differ by country, locale aware sorting and case folding for search and display, storage collation, and identity fields like honorifics that do not map across cultures. The catalogue of these is in `references/data-and-identity.md`.

Produce a plan for the stored data: character set, collation, name and address handling, and the migrations needed.

## Self-audit

- Is every user facing string extracted to a catalogue, with none built by concatenation?
- Do plural messages carry all the forms the target locales need, not just singular and plural?
- Is every date, number, and currency formatted by locale, with values stored in a neutral form?
- Does the layout hold expanded text and mirror for right to left locales?
- Are the do not translate strings marked so they are never sent for translation?
- Does each message carry context for the translator?
- Was a pseudo locale run, and were the leaked strings and layout breaks fixed?
- Is there a plan for storage character set, collation, and name and address formats?

## Honest limits

This skill prepares a product for other locales; it does not produce the translations. The actual translation is human work, and machine translation without review ships errors that read as carelessness to a native speaker. Writing the surrounding code to the readability contract is owned by `code-craft`, and the query and schema changes for storing international data belong to `data-layer`.

The plural and formatting rules here follow the ICU standard, which is a rule of thumb for coverage rather than a guarantee for every language on earth; a locale with unusual grammar may need a linguist. Legal duties around data residency, tax on prices, and consent by region are jurisdiction specific and are not covered here; treat them as questions for a professional in that jurisdiction.

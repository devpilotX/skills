# Data and identity

The strings are the visible part of localisation and the easy part. The hard part is the stored data: names, addresses, sorting, and identity. These outlive any single release, because changing a schema or a collation after data is in it is a migration, not an edit.

## Names

The assumption that a name has a first part and a last part is wrong in much of the world. Some cultures write the family name first. Some people have one name. Some have several family names. Middle names, patronymics, and honorifics vary by region. A form with two fixed fields labelled first and last name excludes real people and stores others wrong.

The safer design is a single full name field for display, plus optional structured fields only where a genuine need exists, such as matching a legal document. Store what the user enters, display it as entered, and do not reformat a name into an order the user did not choose.

## Addresses

Address structure varies by country: the order of the lines, whether a postal code exists and its format, whether a state or region is required, and how the city relates to the region. A form hardcoded to one country's shape cannot capture another's address correctly.

Drive the address form from the selected country: show the fields that country uses, in that country's order, with that country's validation. Store the country explicitly so the address can be formatted correctly on output. Do not validate a postal code against one country's pattern for every country.

## Sorting and case folding

Alphabetical order is per language. The same set of characters sorts differently in different locales, letters with accents sort in language specific positions, and some languages treat a digraph as a single letter. Sorting user visible lists with a byte comparison produces an order that looks random to the reader.

Use a locale aware collator for any list a user reads. For sorting inside the database, set a collation that matches the locale, and be aware that one collation cannot be simultaneously correct for every language, so a multilingual list may need collation chosen per query.

Case folding is also locale specific. The classic trap is Turkish, where the uppercase of a dotless i is not the same as the English uppercase I, so a case insensitive comparison done with the wrong locale gives the wrong answer. Use Unicode aware, locale aware case operations for comparison, and prefer case folding over naive lowercasing for case insensitive matches.

## Storage character set and normalisation

Store text in a character set that covers all of Unicode, so no name or message is silently truncated or corrupted. Beyond the character set, the same visible string can have more than one byte representation because of Unicode normalisation forms, so an accented letter can be one code point or a base letter plus a combining mark. Normalise to a single form on input, or equal looking names will fail to match and duplicates will slip in.

## Identity fields that do not map

Some identity concepts do not transfer. Honorifics and titles differ by culture and are often gendered in ways that do not apply everywhere. Gender itself is not a two value field in every context, and a form that forces a binary choice excludes people and collects wrong data. Where a field exists only because one locale expects it, make it optional and locale specific rather than global and required.

## Plan the migration early

Every item above is cheaper to decide before data accumulates. A column too narrow for a name, a collation that sorts one language, or a character set short of full Unicode all become migrations once real user data depends on them. Find these in the schema during planning, because the schema questions are the ones that get harder with time. The migration itself is owned by `data-layer`.

# Breaking changes

The main file lists what counts as breaking and warns it is routinely misjudged. This is the full
lookup: the change, why it breaks a consumer, and the version bump it forces under semantic versioning.
The rule behind every row is that a change is breaking if a consumer who did nothing wrong now has to do
work.

## The lookup

| Change | Why it breaks a consumer | Bump |
| --- | --- | --- |
| Remove a public function, field, or endpoint | Calls to it now fail | Major |
| Rename anything public | The old name no longer resolves | Major |
| Change a parameter or field type | Existing values no longer fit | Major |
| Make an optional field required | Callers who omitted it now fail | Major |
| Narrow accepted input | Input that used to pass is now rejected | Major |
| Change a default value | Callers relying on the old default get new behaviour | Major |
| Change the meaning of an error code | Handlers keyed on the code misbehave | Major |
| Change observable behaviour with the same signature | Consumers depending on the old behaviour break silently | Major |
| Add an optional field or parameter | Old callers keep working | Minor |
| Add a new endpoint or function | Nothing existing changes | Minor |
| Widen accepted input | Everything that passed still passes | Minor |
| Fix a defect with no behaviour change consumers relied on | Nothing consumers should have depended on changes | Patch |

## The ones that get misjudged

Making an optional field required feels like a small tightening. It is a major change, because every
caller who left the field out now gets an error they did not have before.

Changing a default is invisible in the signature and breaks the callers who never set the value because
the old default suited them. The signature looks identical, so it slips through review.

Changing observable behaviour with an unchanged signature is the hardest to catch. If consumers depend
on the order of results, the timezone of a timestamp, the rounding of a number, or the exact text of an
error, changing any of those breaks them even though the function looks the same. This is why the
changelog matters more than the diff.

Narrowing accepted input, for example rejecting a format you used to tolerate, breaks the callers who
were sending that format. Widening input is safe; narrowing is not.

## When the thing is not imported

For an application nobody imports, the main file says a date or a build number is fine and arguing
about semantics is wasted effort. The bump column above only applies to things other people depend on:
a library, an API, a shared schema, a published event format. For an internal service behind your own
routing layer, the equivalent question is whether a consumer inside your organisation has to change,
and the inventory of who calls it comes from the dependants list.

## Turning a breaking change into a non breaking one

Often the break is avoidable with a two step move that keeps both versions valid at once.

1. Add the new thing alongside the old one. A new field, a new endpoint, a new parameter with a
   default that reproduces the old behaviour.
2. Deprecate the old thing with a date and a migration path, following the deprecation step in the main
   file.
3. Move consumers over during the deprecation window, using the usage telemetry to see who is left.
4. Remove the old thing on the stated date. Only this final step is the major bump, and by the time it
   happens nobody is using the old path.

This is the same expand then contract shape that keeps a data migration compatible with both code
versions, and it is why the release and the migration plans have to line up.

## What to write in the changelog

Every major bump gets a breaking changes section at the top of the entry, with the migration step
inline. Do not make a consumer read the code to find out what changed. State the old behaviour, the new
behaviour, and the exact edit the consumer makes to move across. A breaking change with no migration
note is, in the words of the main file, an outage scheduled for your customers.

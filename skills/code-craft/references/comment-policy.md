<!-- lint-exempt: placeholder -->
# Comment policy

This file quotes the leftover work markers it tells you to delete, so it declares one linter exemption
on the line above. The lint report prints every exemption, so nothing hides.

A comment is code that the compiler cannot check and the test suite cannot exercise. It goes stale
silently. That cost is worth paying for information the code cannot carry, and worth paying for nothing
else.

## The test a comment has to pass

Delete the comment and reread the code. If a competent reader loses something real, keep it. If they
lose nothing, the comment was restating syntax.

Then ask the second question: would this comment still be true after a plausible edit? A comment naming
a line number, a variable that may get renamed, or a value that lives somewhere else is already wrong.

## Comments worth writing

A constraint from outside the code. The remote API rejects more than fifty identifiers per call, so the
batch size is fifty. Nothing in the file says that and nobody can derive it.

The reason for a choice that looks wrong. The lookup runs before the permission check because the
permission depends on the record's owner. Without this, the next reader helpfully reorders it and opens
a hole.

A bug this guards against, with the identifier. The upstream driver returns an empty string instead of
null on a timeout, so the check covers both.

A unit, a range, or an invariant that the type cannot express. Values arrive in hundredths of a cent.
The list stays sorted by expiry so the first expired entry ends the scan.

A deliberate omission. No retry here because the caller owns the retry policy, and two layers of
retries multiply.

A pointer to the authority. The rounding follows the rule in the tax specification, section and all,
rather than the obvious approach.

## Comments to delete on sight

A restatement of the line beneath it. Incrementing the counter above `counter += 1` tells a reader
nothing they did not have.

A heading that names an obvious block. Loop through the items, then a loop through the items. If the
block needs a label, it needs a function name.

Decorative banners and dividers drawn from repeated characters. They never match each other after the
second edit, and a heading in an editor's outline view does the same job for free.

Commented-out code. Version control holds it. A commented block gets copied forward for years and
nobody dares delete it because nobody knows if it matters.

A leftover marker naming work you did not do. Writing `TODO` or `FIXME` into generated code hands the
user an obligation they did not ask for and cannot judge. Either do the work, or say the gap in your
report where the user can act on it.

Change history in a comment. Version control owns who changed what and when, and the comment copy is
wrong within a month.

Attribution of the code to a tool or a model. It dates the file, it tells the reader nothing about the
behaviour, and it is the first thing a reviewer strips.

A commented apology or hedge about the code's quality. Fix it or describe the limit precisely.

## Docstrings

Write one wherever the project's convention expects one, in the form the project already uses. Where
the project has no convention, follow the language's standard: docstrings in Python, doc comments in
Go and Rust and Java, JSDoc or TypeScript doc comments for JavaScript.

Cover what the function does in one line, what its arguments mean when the names are not enough, what
it gives back, what it raises or returns on failure, and any side effect a caller would not expect.

Skip the paragraph that restates the signature. A docstring reading "getUser: gets a user" is noise
with extra steps.

Document the contract, not the implementation. A caller needs to know that identifiers are matched case
insensitively. They do not need to know that the matching uses a dictionary.

## Density

Most well named code needs very few comments. A file where one line in four is a comment usually has a
naming problem wearing a disguise. A file with no comments at all is fine if nothing outside the code
constrains it, and suspicious in code that talks to a payment processor, a tax rule, or hardware.

Comment the surprising parts. Leave the ordinary parts alone.

## Language and tone

Write full sentences in the project's language. Present tense, describing what the code does now.

Say what is true rather than what was intended. A comment reading "this should handle unicode" is a
report that nobody checked.

No address to a reader or an operator. A comment is a note to the next maintainer about the code, not a
message about the task.

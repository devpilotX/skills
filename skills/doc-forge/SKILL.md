---
name: doc-forge
description: Produce documents that survive contact with a reader, in Markdown and as print ready HTML or PDF. Use when the user asks to write or generate a document, a README, a specification, a report, a proposal, a runbook, a one pager, release notes, an architecture decision record, or documentation, or asks to convert Markdown to PDF or HTML, or asks to clean up and structure an existing document. Chooses the document type from what the reader needs to do after reading, front loads the decision or answer, keeps structure flat, and converts with scripts/md2doc.py which needs no third party packages and embeds print styling so any browser can produce the PDF. Applies the human-prose rules so the output does not read as machine generated. Triggers on write a README, write a spec, make a PDF, convert markdown to pdf, write documentation, write a report, one pager, runbook, release notes, format this document.
license: MIT
metadata:
  version: 1.0.0
  suite: skills
  emits_code: true
---

# Doc forge

A document exists so a reader can do something. Decide what that something is, then write the shortest
thing that lets them do it.

## Fit to the project

Match the documents the project already keeps before writing a new one, because a reader expects the
next document to look like the last.

1. Look for a `docs/` directory, an existing `README.md`, a `CHANGELOG.md`, and any `adr/` or
   `decisions/` folder. Copy their heading depth, their section names, and whether they keep a table
   of contents. A repository that already numbers its decision records expects the next one numbered
   the same way.
2. Detect the toolchain that renders the docs: a `mkdocs.yml`, a Docusaurus or Sphinx config, a
   `_config.yml` for a static site. When one exists, write Markdown that renders under it and do not
   introduce a syntax it cannot parse, since `scripts/md2doc.py` is a fallback for when no such
   pipeline is present.
3. Read the changelog format in use, Keep a Changelog style or bare commit list, and follow it so
   release notes slot in rather than starting a second convention.
4. When nothing has been established, no docs folder and no site config, default to a single Markdown
   file per document, convert with `scripts/md2doc.py`, and tell the user which document type you
   picked and why.

## Procedure

### Step 1, pick the type from the reader's next action

The type follows from what happens after reading, and getting this wrong is the main reason documents go
unread.

The reader needs to install and use software. Write a README. Opening line says what the thing is and who
it is for, then installation, then the smallest working example, then configuration, then where to go for
more. Nothing else above the example.

The reader needs to build something. Write a specification. State the problem, the constraints, the
interfaces, the acceptance criteria, and what is explicitly out of scope. The out of scope section
prevents more argument than any other part.

The reader needs to decide. Write a one pager or a decision record. Recommendation first, options
considered, the reasoning, the cost, the risk, and what would reverse the decision.

The reader needs to fix a live problem at three in the morning. Write a runbook. Numbered steps, exact
commands, expected output after each step, and what to do when it differs. No prose, no background. A
runbook with explanation in it is a runbook nobody can follow under pressure.

The reader needs to know what changed. Write release notes. Grouped by what it means to the user, not by
commit. Breaking changes first, with the migration step.

The reader needs to understand a subject. Write an explainer. One idea per section, concrete example per
idea, and the common misunderstanding named directly.

If the reader's next action cannot be named, the document does not have a purpose yet. Ask.

## Non-negotiables

1. Answer or recommendation first. A document that makes the reader work for the conclusion loses most readers before it arrives.
2. No filler sections. No introduction that restates the title, no conclusion that restates the body, no "overview" that says the document has sections.
3. Every command is runnable as written, and every code sample is complete enough to execute. Placeholders are marked clearly with what to substitute.
4. No invented facts, figures, versions, or citations. Anything unverified gets marked as needing confirmation.
5. Apply the `human-prose` rules. Sentence case headings, no em dashes, straight quotes, plain copulas, no significance padding. Run the detector before delivering.
6. Length is decided by content. Padding a document to look substantial makes it less likely to be read.

### Step 2, apply the structure rules

Flat beats deep. Three heading levels at most. A fourth level means the document should be split.

One idea per section, and the heading says what the idea is. A heading that only contains other headings
gets merged.

Front load every section too, not just the document. The first sentence of a section carries its point.

Prose for reasoning, lists for enumeration, tables for comparison across a shared set of attributes. A
table with one column of real content should be prose. A list of sentences that relate to each other
should be a paragraph.

Code blocks get a language tag so they highlight correctly.

Link rather than repeat. Duplicated content goes stale in one place and then contradicts itself.

A table of contents earns its place above roughly eight sections, and not below that.

### Step 3, convert to HTML or PDF

`scripts/md2doc.py` converts Markdown to self contained HTML with embedded print styling, A4 page rules,
and page break handling that avoids splitting headings from their content.

```
python3 scripts/md2doc.py report.md                      # writes report.html
python3 scripts/md2doc.py report.md -o out.html --toc    # with a contents block
python3 scripts/md2doc.py report.md --pdf                # also tries to make a PDF
python3 scripts/md2doc.py a.md b.md -o manual.html --toc # concatenate in order
```

It needs no third party packages, which is the point: it works in a clean environment. YAML frontmatter
is read for the title and removed from the body.

For PDF it tries weasyprint, then wkhtmltopdf, then a headless Chromium, then pandoc, and reports which
one it used. When none is installed it says so and exits with status 3, and the HTML is still print ready,
so opening it and printing to PDF from a browser gives the same result. Do not claim a PDF was produced
when the exit status was 3.

Supported Markdown covers headings, paragraphs, fenced and indented code, ordered and unordered lists
with one nesting level, blockquotes, pipe tables, horizontal rules, inline code, bold, italic,
strikethrough, links, bare URLs, and images. Anything outside that list needs checking in the output, or
use pandoc directly.

### Step 4, run the detector and any embedded code through its contract

Run the human-prose detector at `--strict` on the finished Markdown before you convert it, so no machine
residue reaches the reader. Fix findings rather than converting around them.

A document that ships code the reader is meant to run, an install snippet, a configuration file, a worked
example longer than a couple of lines, is code the reader will paste, so pass it through the `code-craft`
contract: split by responsibility, name values for what they hold, and comment why rather than what. A
broken command in a runbook fails at the worst moment, so verify every block that claims to be runnable.

## Reusable shapes

`references/templates.md` has skeletons for a README, a specification, a decision record, a runbook, and
release notes, each annotated with what goes in every section and what commonly gets put there wrongly.

`references/format-support.md` lists exactly what `scripts/md2doc.py` renders, the PDF engine order it
tries, the exit codes it returns, and the Markdown features that need checking in the output.

## Self-audit

- The reader's next action is named, and the type matches it.
- The conclusion or recommendation is in the first few lines.
- No introduction or conclusion that only restates.
- Every command was run, or is marked as unverified.
- Three heading levels at most, sentence case throughout.
- The human-prose detector runs clean at `--strict`.
- Links resolve.
- Removing any section would lose information. If not, remove it.

## When to stay off

Skip the type ceremony for a two line note, an inline answer, a code comment, or a scratch file the
user called a draft. Forcing a chat reply into README structure wastes the reader's time and buries a
one sentence answer under headings.

Saying "stop", "just execute", or "skip the docs" is the off switch. It stays off for the rest of
the session unless the user asks again. A skill that keeps reformatting a note nobody wanted
formatted gets uninstalled.

## Honest limits

This skill decides document shape and converts Markdown to print ready HTML or PDF. It does not verify
that the facts inside are true, which belongs to `reality-check`, and the wording pass it runs is the
`human-prose` detector rather than a full rewrite, so hand long form prose to `human-prose` when the
voice matters more than the structure.

`scripts/md2doc.py` supports the Markdown subset listed in `references/format-support.md` and nothing
past it, and it makes a PDF only when a rendering engine is already installed, exiting with status 3
and a print ready HTML file when none is. Do not report a PDF that status 3 never produced.

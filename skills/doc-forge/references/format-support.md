# What md2doc.py renders

This is the contract for `scripts/md2doc.py`. It converts a Markdown subset to a single self contained
HTML file with embedded print styling, and optionally to PDF when a rendering engine is present. Read
this before promising a feature the converter does not have.

## Markdown features that render

| Feature | Syntax | Notes |
| --- | --- | --- |
| Headings | `#` through `######` | Six levels parse, but keep documents to three. |
| Paragraphs | blank line separated | Soft line breaks join into one paragraph. |
| Fenced code | triple backtick | Language tag after the fence sets highlighting. |
| Indented code | four spaces | Rendered as a code block without a language. |
| Unordered list | `-` or `*` | One nesting level. Deeper nesting is flattened. |
| Ordered list | `1.` | One nesting level. Numbering restarts per block. |
| Blockquote | `>` | Single level. Nested quotes are not parsed. |
| Pipe table | `| a | b |` | Header row plus a separator row required. |
| Horizontal rule | three hyphens | Renders as a thematic break line. |
| Inline code | single backtick | No language, monospace only. |
| Bold | double asterisk | |
| Italic | single asterisk or `_x_` | |
| Strikethrough | double tilde | |
| Links | `[text](url)` | Title attribute is ignored. |
| Bare URLs | `https://...` | Linkified automatically. |
| Images | `![alt](src)` | Local paths must resolve at convert time. |

## Features that do not render

Anything outside the table above passes through as literal text or is dropped. The common ones that
catch people:

- Nested lists past one level. The second level is flattened into the first.
- Footnotes, definition lists, and task list checkboxes. Not parsed.
- Raw HTML blocks. Passed through unescaped, so they can break the page styling.
- Math notation. No MathML or LaTeX rendering.
- Reference style links and images. Only inline links resolve.
- Frontmatter beyond title. YAML is read for the title and stripped from the body; other keys are
  ignored.

When a document needs any of these, convert with pandoc directly and check the output rather than
claiming md2doc handled it.

## PDF engine order

`--pdf` tries these in order and reports which one produced the file:

1. weasyprint, if importable as a Python package.
2. wkhtmltopdf, if on the path.
3. A headless Chromium or Chrome, if found.
4. pandoc, if on the path.

The first one that succeeds wins. The chosen engine is named in the output so a reader can reproduce it.

## Exit codes

| Code | Meaning | What to do |
| --- | --- | --- |
| 0 | HTML written, and PDF written if requested | Report both paths. |
| 2 | Bad arguments or an input file that does not exist | Fix the command. |
| 3 | HTML written, but no PDF engine was installed | Open the HTML and print to PDF from a browser. |

Status 3 is not a failure of the document. The HTML is print ready with A4 page rules and page break
handling, so a browser print gives the same result as an installed engine. Never report a PDF as
produced when the exit status was 3.

## Print styling built in

The embedded stylesheet sets A4 page size with sane margins, avoids splitting a heading from the
content under it, keeps table headers with at least one row, and prevents a code block from breaking
mid line where the engine allows it. Concatenating several inputs with `-o` and `--toc` produces one
document with a contents block, in the order the files were given on the command line.

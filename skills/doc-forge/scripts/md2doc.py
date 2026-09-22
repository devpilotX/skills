#!/usr/bin/env python3
"""Convert Markdown to print ready HTML, and to PDF when a converter is available.

No third party packages are required for the HTML output, which is self contained
with embedded CSS and page rules, so any browser can print it to PDF. When one of
pandoc, weasyprint, wkhtmltopdf or a headless Chromium is installed, --pdf uses it.

Supported Markdown: ATX headings, paragraphs, fenced and indented code, ordered and
unordered lists with one level of nesting, blockquotes, pipe tables, horizontal
rules, inline code, bold, italic, strikethrough, links, and images. YAML
frontmatter is read for the title and then removed from the body.

Usage:
  python3 md2doc.py input.md                    # writes input.html
  python3 md2doc.py input.md -o out.html --toc  # adds a table of contents
  python3 md2doc.py input.md --pdf              # also tries to produce a PDF
  python3 md2doc.py a.md b.md -o combined.html  # concatenates in order
"""

from __future__ import annotations

import argparse
import html
import os
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

CSS = """
:root { --ink: #1a1a1a; --muted: #565656; --rule: #d6d6d6; --bg: #ffffff; }
* { box-sizing: border-box; }
body {
  font-family: Georgia, "Times New Roman", serif;
  font-size: 11.5pt; line-height: 1.55; color: var(--ink); background: var(--bg);
  margin: 0 auto; padding: 2.2rem 1.4rem; max-width: 46rem;
  text-rendering: optimizeLegibility;
}
h1, h2, h3, h4 {
  font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
  line-height: 1.25; margin: 1.8em 0 0.6em; page-break-after: avoid;
}
h1 { font-size: 1.9em; margin-top: 0; }
h2 { font-size: 1.38em; border-bottom: 1px solid var(--rule); padding-bottom: 0.22em; }
h3 { font-size: 1.12em; }
h4 { font-size: 1em; color: var(--muted); }
p, ul, ol, blockquote, table, pre { margin: 0 0 0.9em; }
ul, ol { padding-left: 1.5em; }
li { margin: 0.2em 0; }
li > ul, li > ol { margin: 0.25em 0 0.35em; }
a { color: #0b4fa8; text-decoration: underline; }
code {
  font-family: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
  font-size: 0.88em; background: #f2f2f2; padding: 0.1em 0.32em; border-radius: 3px;
}
pre {
  background: #f7f7f7; border: 1px solid #e3e3e3; border-radius: 4px;
  padding: 0.8em 0.95em; overflow-x: auto; page-break-inside: avoid;
}
pre code { background: none; padding: 0; font-size: 0.84em; }
blockquote {
  margin-left: 0; padding: 0.15em 0 0.15em 1em;
  border-left: 3px solid var(--rule); color: var(--muted);
}
table { border-collapse: collapse; width: 100%; font-size: 0.95em; page-break-inside: avoid; }
th, td { border: 1px solid var(--rule); padding: 0.45em 0.6em; text-align: left; vertical-align: top; }
th { background: #f4f4f4; font-weight: 600; }
hr { border: 0; border-top: 1px solid var(--rule); margin: 1.6em 0; }
img { max-width: 100%; }
.toc { background: #fafafa; border: 1px solid var(--rule); border-radius: 4px; padding: 0.9em 1.2em; }
.toc-title {
  font-family: -apple-system, "Segoe UI", Helvetica, Arial, sans-serif;
  font-weight: 600; margin-bottom: 0.4em;
}
.toc ul { list-style: none; padding-left: 0; margin: 0; }
.toc ul ul { padding-left: 1.1em; }
@page { size: A4; margin: 19mm 17mm; }
@media print {
  body { padding: 0; max-width: none; font-size: 10.5pt; }
  a { color: var(--ink); }
  a[href^="http"]::after { content: " (" attr(href) ")"; font-size: 0.78em; color: var(--muted); }
  h1, h2 { page-break-after: avoid; }
  .no-print { display: none; }
}
"""

INLINE_CODE = re.compile(r"`([^`]+)`")
IMAGE = re.compile(r"!\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
LINK = re.compile(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
BOLD = re.compile(r"\*\*([^*]+)\*\*")
ITALIC = re.compile(r"(?<![*\w])\*([^*\n]+)\*(?!\*)")
STRIKE = re.compile(r"~~([^~]+)~~")
# A bare URL, stopping before trailing sentence punctuation so that a full stop at
# the end of a sentence does not become part of the link target.
AUTOLINK = re.compile(r"(?<![\"(\[=])\bhttps?://[^\s<>\")\]]*[^\s<>\")\].,;:!?]")


def slugify(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-{2,}", "-", s) or "section"


def inline(text: str) -> str:
    """Convert inline markup, protecting code spans from further processing."""
    spans: list[str] = []

    def stash(m: re.Match) -> str:
        spans.append(html.escape(m.group(1), quote=False))
        return "\x00%d\x00" % (len(spans) - 1)

    text = INLINE_CODE.sub(stash, text)
    text = html.escape(text, quote=False)

    text = IMAGE.sub(lambda m: '<img src="%s" alt="%s">'
                     % (html.escape(m.group(2), quote=True), m.group(1)), text)
    text = LINK.sub(lambda m: '<a href="%s">%s</a>'
                    % (html.escape(m.group(2), quote=True), m.group(1)), text)
    text = AUTOLINK.sub(lambda m: '<a href="%s">%s</a>' % (m.group(0), m.group(0)), text)
    text = BOLD.sub(r"<strong>\1</strong>", text)
    text = ITALIC.sub(r"<em>\1</em>", text)
    text = STRIKE.sub(r"<del>\1</del>", text)

    for i, code in enumerate(spans):
        text = text.replace("\x00%d\x00" % i, "<code>%s</code>" % code)
    return text


def split_frontmatter(text: str) -> tuple[dict, str]:
    meta: dict = {}
    if not text.startswith("---\n"):
        return meta, text
    end = text.find("\n---", 4)
    if end == -1:
        return meta, text
    block = text[4:end]
    for line in block.splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip().strip("'\"")
    rest = text[end + 4:]
    return meta, rest.lstrip("\n")


def table_rows(lines: list[str], start: int) -> tuple[str, int]:
    """Render a pipe table starting at start. Returns html and the next index."""
    def cells(row: str) -> list[str]:
        row = row.strip()
        if row.startswith("|"):
            row = row[1:]
        if row.endswith("|"):
            row = row[:-1]
        return [c.strip() for c in row.split("|")]

    header = cells(lines[start])
    i = start + 2
    body: list[list[str]] = []
    while i < len(lines) and "|" in lines[i] and lines[i].strip():
        body.append(cells(lines[i]))
        i += 1
    out = ["<table>", "<thead><tr>"]
    out += ["<th>%s</th>" % inline(c) for c in header]
    out.append("</tr></thead>")
    if body:
        out.append("<tbody>")
        for row in body:
            out.append("<tr>" + "".join("<td>%s</td>" % inline(c) for c in row) + "</tr>")
        out.append("</tbody>")
    out.append("</table>")
    return "\n".join(out), i


def emit_fenced_code(lines: list[str], i: int, out: list[str]) -> int:
    """Render a fenced code block starting at i, returning the index past it."""
    fence = lines[i].strip()[:3]
    lang = lines[i].strip()[3:].strip()
    i += 1
    buf: list[str] = []
    while i < len(lines) and not lines[i].strip().startswith(fence):
        buf.append(lines[i])
        i += 1
    i += 1
    cls = ' class="language-%s"' % html.escape(lang, quote=True) if lang else ""
    out.append("<pre><code%s>%s</code></pre>"
               % (cls, html.escape("\n".join(buf), quote=False)))
    return i


def emit_heading(match: re.Match, out: list[str],
                 headings: list[tuple[int, str, str]]) -> None:
    """Append an ATX heading, giving it a slug unique among prior headings."""
    level = len(match.group(1))
    body = match.group(2)
    slug = slugify(body)
    base, n = slug, 2
    existing = {h[2] for h in headings}
    while slug in existing:
        slug = "%s-%d" % (base, n)
        n += 1
    headings.append((level, body, slug))
    out.append('<h%d id="%s">%s</h%d>' % (level, slug, inline(body), level))


def emit_blockquote(lines: list[str], i: int, out: list[str]) -> int:
    """Render a blockquote by joining its lines, returning the index past it."""
    quote: list[str] = []
    while i < len(lines) and lines[i].strip().startswith(">"):
        quote.append(lines[i].strip().lstrip(">").strip())
        i += 1
    out.append("<blockquote><p>%s</p></blockquote>" % inline(" ".join(quote)))
    return i


def emit_list_item(match: re.Match, out: list[str], list_stack: list[str]) -> None:
    """Append one list item, opening or closing list tags to match its depth."""
    indent = len(match.group(1).replace("\t", "    "))
    depth = 1 if indent < 2 else 2
    kind = "ol" if re.match(r"\d", match.group(2)) else "ul"
    while len(list_stack) > depth:
        out.append("</%s>" % list_stack.pop())
    if len(list_stack) < depth:
        out.append("<%s>" % kind)
        list_stack.append(kind)
    elif list_stack and list_stack[-1] != kind:
        out.append("</%s>" % list_stack.pop())
        out.append("<%s>" % kind)
        list_stack.append(kind)
    out.append("<li>%s</li>" % inline(match.group(3)))


TABLE_DIVIDER = re.compile(r"\|?\s*:?-{2,}:?\s*(\|\s*:?-{2,}:?\s*)*\|?")
LIST_ITEM = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
HR = re.compile(r"(-{3,}|\*{3,}|_{3,})")
ATX = re.compile(r"(#{1,6})\s+(.*\S)\s*$")


@dataclass
class Doc:
    """Mutable accumulator threaded through block rendering."""
    out: list[str]
    para: list[str]
    list_stack: list[str]

    def flush_para(self) -> None:
        """Close the open paragraph, if any, escaping and joining its lines."""
        if self.para:
            self.out.append("<p>%s</p>" % inline(" ".join(self.para).strip()))
            self.para.clear()

    def close_lists(self, to_depth: int = 0) -> None:
        """Close open list tags down to the given nesting depth."""
        while len(self.list_stack) > to_depth:
            self.out.append("</%s>" % self.list_stack.pop())

    def break_block(self) -> None:
        """End any open paragraph and list before a new block starts."""
        self.flush_para()
        self.close_lists()


def is_table_start(lines: list[str], i: int, stripped: str) -> bool:
    """True when line i begins a pipe table, judged by its divider row."""
    return ("|" in stripped and i + 1 < len(lines)
            and bool(TABLE_DIVIDER.fullmatch(lines[i + 1].strip())))


def consume_block(doc: Doc, lines: list[str], i: int,
                  headings: list[tuple[int, str, str]]) -> int:
    """Render the block at line i into doc, returning the next line index."""
    line = lines[i]
    stripped = line.strip()
    if stripped.startswith("```") or stripped.startswith("~~~"):
        doc.break_block()
        return emit_fenced_code(lines, i, doc.out)
    if not stripped:
        doc.break_block()
        return i + 1
    heading = ATX.match(stripped)
    if heading:
        doc.break_block()
        emit_heading(heading, doc.out, headings)
        return i + 1
    if HR.fullmatch(stripped):
        doc.break_block()
        doc.out.append("<hr>")
        return i + 1
    if stripped.startswith(">"):
        doc.break_block()
        return emit_blockquote(lines, i, doc.out)
    if is_table_start(lines, i, stripped):
        doc.break_block()
        block, nxt = table_rows(lines, i)
        doc.out.append(block)
        return nxt
    item = LIST_ITEM.match(line)
    if item:
        doc.flush_para()
        emit_list_item(item, doc.out, doc.list_stack)
        return i + 1
    doc.para.append(stripped)
    return i + 1


def convert(md: str, headings: list[tuple[int, str, str]]) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    doc = Doc(out=[], para=[], list_stack=[])
    i = 0
    while i < len(lines):
        i = consume_block(doc, lines, i, headings)
    doc.flush_para()
    doc.close_lists()
    return "\n".join(doc.out)


def build_toc(headings: list[tuple[int, str, str]]) -> str:
    entries = [h for h in headings if 2 <= h[0] <= 3]
    if len(entries) < 3:
        return ""
    out = ['<nav class="toc"><div class="toc-title">Contents</div><ul>']
    depth = 2
    for level, text, slug in entries:
        while level > depth:
            out.append("<ul>")
            depth += 1
        while level < depth:
            out.append("</ul>")
            depth -= 1
        out.append('<li><a href="#%s">%s</a></li>' % (slug, inline(text)))
    while depth > 2:
        out.append("</ul>")
        depth -= 1
    out.append("</ul></nav>")
    return "\n".join(out)


def to_pdf(html_path: Path, pdf_path: Path, source_md: Path | None) -> str | None:
    """Try the available converters in order. Returns the tool used, or None."""
    if shutil.which("weasyprint"):
        r = subprocess.run(["weasyprint", str(html_path), str(pdf_path)],
                           capture_output=True, text=True)
        if r.returncode == 0:
            return "weasyprint"
    if shutil.which("wkhtmltopdf"):
        r = subprocess.run(["wkhtmltopdf", "--enable-local-file-access",
                            str(html_path), str(pdf_path)],
                           capture_output=True, text=True)
        if r.returncode == 0:
            return "wkhtmltopdf"
    for browser in ("chromium", "chromium-browser", "google-chrome"):
        if shutil.which(browser):
            r = subprocess.run([browser, "--headless", "--disable-gpu", "--no-sandbox",
                                "--print-to-pdf=%s" % pdf_path, html_path.as_uri()],
                               capture_output=True, text=True)
            if r.returncode == 0 and pdf_path.exists():
                return browser
    if shutil.which("pandoc") and source_md:
        r = subprocess.run(["pandoc", str(source_md), "-o", str(pdf_path)],
                           capture_output=True, text=True)
        if r.returncode == 0:
            return "pandoc"
    return None


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="md2doc.py",
                                 description="Markdown to print ready HTML and PDF.")
    ap.add_argument("inputs", nargs="+", help="markdown files, concatenated in order")
    ap.add_argument("-o", "--output", help="output html path")
    ap.add_argument("-t", "--title", help="document title, defaults to frontmatter or first heading")
    ap.add_argument("--toc", action="store_true", help="insert a table of contents")
    ap.add_argument("--pdf", action="store_true", help="also try to produce a PDF")
    args = ap.parse_args(argv)

    bodies: list[str] = []
    headings: list[tuple[int, str, str]] = []
    title = args.title
    first_source: Path | None = None

    for raw in args.inputs:
        path = Path(raw)
        if not path.is_file():
            print("no such file: %s" % raw, file=sys.stderr)
            return 2
        if first_source is None:
            first_source = path
        meta, text = split_frontmatter(path.read_text(encoding="utf-8"))
        if not title:
            title = meta.get("title") or meta.get("name")
        bodies.append(convert(text, headings))

    if not title and headings:
        title = headings[0][1]
    title = title or "Document"

    toc = build_toc(headings) if args.toc else ""
    document = (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        "<meta charset=\"utf-8\">\n"
        "<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
        "<title>%s</title>\n<style>%s</style>\n</head>\n<body>\n%s%s\n</body>\n</html>\n"
        % (html.escape(title, quote=False), CSS, (toc + "\n") if toc else "",
           "\n".join(bodies))
    )

    out_path = Path(args.output) if args.output else Path(args.inputs[0]).with_suffix(".html")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(document, encoding="utf-8")
    print("wrote %s (%d bytes, %d headings)" % (out_path, len(document), len(headings)))

    if args.pdf:
        pdf_path = out_path.with_suffix(".pdf")
        tool = to_pdf(out_path, pdf_path, first_source)
        if tool:
            print("wrote %s using %s" % (pdf_path, tool))
        else:
            print(
                "no PDF converter found. The HTML is print ready, so either open it "
                "and print to PDF from the browser, or install one of: weasyprint "
                "(pip install weasyprint), wkhtmltopdf, chromium, pandoc.",
                file=sys.stderr)
            return 3
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

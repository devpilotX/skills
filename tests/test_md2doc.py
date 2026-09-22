#!/usr/bin/env python3
"""Tests for the Markdown converter in the doc-forge skill.

Checks the conversion of every supported construct, and checks escaping, which is
the part that causes real damage when it is wrong.

Run with: python3 tests/test_md2doc.py
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "doc-forge" / "scripts" / "md2doc.py"
FIXTURE = ROOT / "tests" / "fixtures" / "doc_sample.md"

spec = importlib.util.spec_from_file_location("md2doc", SCRIPT)
assert spec and spec.loader, "cannot load converter at %s" % SCRIPT
md2doc = importlib.util.module_from_spec(spec)
sys.modules["md2doc"] = md2doc
spec.loader.exec_module(md2doc)

failures: list[str] = []


def check(condition: bool, message: str) -> None:
    if condition:
        print("  pass  %s" % message)
    else:
        print("  FAIL  %s" % message)
        failures.append(message)


with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp) / "out.html"
    rc = md2doc.main([str(FIXTURE), "-o", str(out), "--toc"])
    check(rc == 0, "converter exits cleanly")
    doc = out.read_text(encoding="utf-8")

print("\nstructure")
check("<title>Converter test</title>" in doc, "title comes from frontmatter")
check("version: 1" not in doc, "frontmatter is stripped from the body")
check('class="toc"' in doc and 'href="#lists"' in doc, "table of contents links to slugs")
check('<h2 id="lists">' in doc, "headings carry stable identifiers")
check("@media print" in doc and "@page" in doc, "print rules are embedded")
check("<style>" in doc, "stylesheet is inlined, so the file is self contained")

print("\ninline markup")
check("<strong>bold</strong>" in doc, "bold")
check("<em>italic</em>" in doc, "italic")
check("<del>strike</del>" in doc, "strikethrough")
check("<code>inline code</code>" in doc, "inline code")
check('<a href="https://example.com">link</a>' in doc, "explicit link")
check('<a href="https://example.org/page">' in doc, "bare URL becomes a link")
check("</a>." in doc, "trailing full stop stays outside the link")

print("\nblocks")
check(doc.count("<ul>") >= 2, "nested unordered list")
check("<ol>" in doc and "step one" in doc, "ordered list")
check("<th>Field</th>" in doc, "table header")
check("<td>primary key</td>" in doc, "table body cell")
check("<code>null</code>" in doc, "inline markup inside a table cell")
check("<blockquote>" in doc and "Continued on the next line." in doc, "blockquote joins lines")
check("<pre><code" in doc, "fenced code block")

print("\nescaping, the part that matters")
check("x &lt; 3 and x &gt; 1" in doc, "angle brackets inside code are escaped")
check("<script>alert" not in doc, "raw script tag does not survive")
check("&lt;script&gt;alert(1)&lt;/script&gt;" in doc, "raw HTML is shown as text")
check("6 &amp; 7" in doc, "ampersand is escaped")

print("\nunit level behaviour")
check(md2doc.slugify("Hello, World!") == "hello-world", "slugify strips punctuation")
check(md2doc.slugify("") == "section", "slugify has a fallback")
meta, body = md2doc.split_frontmatter("---\ntitle: T\n---\nBody\n")
check(meta.get("title") == "T" and body.strip() == "Body", "frontmatter parsing")
meta2, body2 = md2doc.split_frontmatter("No frontmatter here\n")
check(meta2 == {} and body2.startswith("No frontmatter"), "missing frontmatter is fine")
check("<code>a &lt; b</code>" in md2doc.inline("`a < b`"), "code span escaped on its own")
check(md2doc.inline("**a** and *b*") == "<strong>a</strong> and <em>b</em>", "inline combination")

print("\n%d check(s) failed" % len(failures))
sys.exit(1 if failures else 0)

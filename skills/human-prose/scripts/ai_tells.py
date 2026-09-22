#!/usr/bin/env python3
"""Detect stylistic markers commonly found in machine generated prose.

Reads files given as arguments, or stdin when no arguments are given, and reports
matches grouped by severity with line numbers.

Severity levels:
  high    Artifacts that almost never appear in hand written text, such as leaked
          chatbot citation markup or unfilled placeholders.
  medium  Strong stylistic markers, such as em dashes, curly quotes, emoji,
          title case headings, and overrepresented vocabulary above threshold.
  low     Soft patterns that are fine once and become a signature when repeated,
          such as negative parallelism and three item rhythm.

Exit codes:
  0  nothing above the failing threshold
  1  findings at or above the failing threshold
  2  usage error

The default failing threshold is high. Pass --strict to fail on medium as well,
or --pedantic to fail on anything.

Sources for the pattern list are documented in ../references/tells-catalogue.md.
No third party packages are required.
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

EXEMPT_MARKER = "lint-vocab-exempt"
EXEMPT_RE = re.compile(r"lint-exempt:\s*([a-z0-9,\-\s]+?)\s*-->")

# Files that document these patterns have to quote them. Exemptions are declared
# per file, per rule, in an HTML comment near the top, and every report prints
# which rules a file opted out of so that nothing hides.
ALL_RULES = {
    "artifact", "placeholder", "em-dash", "en-dash", "curly-quote", "emoji",
    "thematic-break", "title-case-heading", "x-and-y-heading", "bold-label-list",
    "vocab", "vocab-density", "copula-avoidance", "significance-padding",
    "vague-attribution", "chatter", "cutoff-disclaimer", "section-summary",
    "negative-parallelism", "participle-tail", "rule-of-three", "trailing-space",
    "final-newline",
}


def parse_exemptions(lines: list[str]) -> set[str]:
    # The window is generous enough to sit just below YAML frontmatter.
    head = "\n".join(lines[:20])
    rules: set[str] = set()
    if EXEMPT_MARKER in head:
        rules |= {"vocab", "vocab-density"}
    for m in EXEMPT_RE.finditer(head):
        for token in m.group(1).split(","):
            token = token.strip()
            if token in ALL_RULES:
                rules.add(token)
            elif token == "all":
                rules |= set(ALL_RULES)
    return rules

# Vocabulary with measured overrepresentation in post-2022 model output.
# Frequency studies are cited in the catalogue reference file.
VOCAB = [
    "delve", "delving", "underscore", "underscores", "underscoring", "tapestry",
    "testament", "showcase", "showcases", "showcasing", "pivotal", "crucial",
    "realm", "robust", "seamless", "seamlessly", "boasts", "vibrant",
    "intricate", "intricacies", "meticulous", "meticulously", "foster",
    "fostering", "garner", "garnered", "bolster", "bolstered", "enhance",
    "enhances", "enhancing", "utilize", "utilizes", "utilizing", "holistic",
    "myriad", "plethora", "profound", "groundbreaking", "renowned", "nestled",
    "multifaceted", "paradigm", "synergy", "cultivate", "cultivating",
    "embark", "harness", "harnessing", "unparalleled", "noteworthy",
]

VOCAB_PHRASES = [
    "align with", "aligns with", "aligned with", "valuable insights",
    "key takeaways", "ever-evolving", "ever evolving", "rich history",
    "deeply rooted", "indelible mark", "stands as a", "serves as a",
    "plays a vital role", "plays a key role", "plays a significant role",
    "a testament to", "in the realm of", "at the forefront of",
    "the world of", "when it comes to", "it is worth noting",
    "it is important to note", "it's important to note",
    "it is crucial to note", "important to remember",
]

# Constructions that replace a plain copula.
COPULA_AVOIDANCE = [
    r"\bserves? as\b", r"\bstands? as\b", r"\bfunctions? as\b",
    r"\brepresents? a\b", r"\bmarks? a\b", r"\boperates? as\b",
    r"\brefers to\b",
]

SIGNIFICANCE_PADDING = [
    r"\breflect(s|ing)? (a )?broader\b",
    r"\bunderscor\w+ (its|the) (importance|significance)\b",
    r"\bhighlight(s|ing)? (its|the) (importance|significance)\b",
    r"\bcontribut(es|ing) to the broader\b",
    r"\bsetting the stage for\b",
    r"\bkey turning point\b",
    r"\bcement(s|ed|ing)? (its|his|her|their) (place|legacy|status)\b",
    r"\blasting (impact|legacy|impression)\b",
    r"\benduring legacy\b",
    r"\bsymboliz\w+ (its|the)\b",
]

VAGUE_ATTRIBUTION = [
    r"\bexperts (argue|say|believe|agree|note)\b",
    r"\bobservers have (cited|noted)\b",
    r"\bindustry reports (suggest|indicate|show)\b",
    r"\bcritics (argue|say|contend)\b",
    r"\bscholars (argue|note|agree)\b",
    r"\bit is widely (believed|held|regarded)\b",
    r"\bmany (believe|argue|consider)\b",
    r"\bsome (would )?(argue|say)\b",
    r"\bstudies (show|suggest|indicate)\b(?![^.]{0,80}https?://)",
]

COLLABORATIVE_CHATTER = [
    r"\bI hope this helps\b",
    r"\bwould you like me to\b",
    r"\blet me know if\b",
    r"\bis there anything else\b",
    r"\bhere('s| is) (a|an|the) (breakdown|overview|summary) (of|for) \b",
    r"\bas an AI (language )?model\b",
    r"\bcertainly!\b",
    r"\bof course!\b",
    r"\byou('re| are) absolutely right\b",
    r"\bgreat question\b",
    r"\bfeel free to\b",
]

CUTOFF_DISCLAIMERS = [
    r"\bas of my (last )?(knowledge|training) (update|cutoff)\b",
    r"\bup to my last (training|knowledge)\b",
    r"\bwhile specific details are (limited|scarce)\b",
    r"\bnot widely (available|documented|disclosed)\b",
    r"\bbased on (the )?available information\b",
    r"\bin the (provided|available) sources\b",
    r"\bmaintains a low profile\b",
    r"\bkeeps personal details private\b",
]

SECTION_SUMMARY = [
    r"^\s*#{1,6}\s*(conclusion|in conclusion|summary|final thoughts|closing thoughts)\s*$",
    r"^\s*(in conclusion|in summary|to summarize|to sum up|overall,)\b",
    r"^\s*#{1,6}\s*(challenges and legacy|future outlook|future prospects)\s*$",
    r"\bdespite (its|these) [a-z ]{0,30}(challenges|limitations)\b",
]

# Leaked internal markup from specific tools. These are near proof of origin.
ARTIFACTS = [
    (r"contentReference", "ChatGPT reference markup"),
    (r"oaicite|oai_citation", "ChatGPT citation markup"),
    (r"turn\d+(search|image|news|file)\d+", "ChatGPT search or image token"),
    (r'\{"attribution":\{"attributableIndex"', "ChatGPT attribution JSON"),
    (r"\[cite:\s*\d+", "Gemini citation marker"),
    (r"\[span_\d+\]\((start|end)_span\)", "Gemini span marker"),
    (r"grok_card|grok_render_citation_card_json", "Grok citation card"),
    (r"【\d+\u2020", "DeepSeek lenticular citation"),
    (r"\[attached_file:\d+\]|\[web:\d+\]", "Perplexity file or web marker"),
    (r"ppl-ai-file-upload", "Perplexity upload bucket URL"),
    (r':::writing\{variant=', "document wrapper markup"),
    (r"utm_source=(chatgpt\.com|openai|copilot\.com)", "chatbot tracking parameter"),
    (r"referrer=grok\.com", "Grok tracking parameter"),
    (r"```wikitext", "wikitext wrapped in a markdown fence"),
]

PLACEHOLDERS = [
    (r"\[(insert|add|your)[^\]]{0,40}\]", "unfilled bracket placeholder"),
    (r"\b20\d\d-(xx|XX)-(xx|XX)\b", "placeholder date"),
    (r"<!--\s*(add|insert)[^>]{0,60}(if available|here)\s*-->", "placeholder comment"),
    (r"\[(Entertainer|Company|Product|Name)'?s? Name\]", "template placeholder"),
    (r"\bTODO\b(?!\()", "leftover TODO"),
    (r"\bLorem ipsum\b", "filler text"),
]

# A present participle clause tacked onto the end of a sentence to add commentary
# rather than fact. Restricted to the verbs that actually show up this way, because
# a general two-participle rule flags ordinary noun lists such as zoning, bonding.
PARTICIPLE_TAIL = (
    r",\s+(highlighting|underscoring|emphasi[sz]ing|reflecting|symboli[sz]ing|"
    r"contributing|ensuring|showcasing|cultivating|fostering|encompassing|"
    r"enhancing|demonstrating|solidifying|cementing|reinforcing|signal+ing|"
    r"illustrating|paving|ushering|marking)\b"
)

# "X and Y" headings are only a signal when one side is an evaluative noun, as in
# "Awards and recognition". Ordinary technical pairings such as "Concurrency and
# ordering" are normal and must not be flagged.
PUFFERY_NOUNS = {
    "awards", "recognition", "legacy", "impact", "significance", "importance",
    "achievements", "contributions", "influence", "reception", "accolades",
    "honours", "honors", "challenges", "prospects", "outlook", "trends",
    "highlights", "milestones", "innovations",
}

ADJ_SUFFIXES = (
    "ive", "ous", "ful", "ent", "ant", "able", "ible", "ic", "al", "ary",
    "ate", "less",
)

NEGATIVE_PARALLELISM = [
    r"\bnot only\b[^.]{0,80}\bbut (also|it)\b",
    r"\bit(?:'s| is) not (just|merely|only)\b[^.]{0,60},? it(?:'s| is)\b",
    r"\bnot (just|merely|simply)\b[^.]{0,60},? but\b",
    # The contrast is often carried by a dash, colon or comma instead of "but".
    r"\b(is|are|was|were|it's)\s+not (just|merely|simply|only)\b[^.]{0,60}[\u2014\u2013:,]",
    r"\brather than (simply|merely|just)\b",
    r"\bno [a-z]+, no [a-z]+, just\b",
]

ACRONYM_OK = {
    "AI", "API", "CI", "CD", "CLI", "CSS", "HTML", "HTTP", "HTTPS", "ID", "IO",
    "JSON", "LLM", "MD", "MIT", "MVP", "PDF", "PR", "SDK", "SEO", "SQL", "SSR",
    "TLS", "UI", "URL", "UX", "YAML", "GDPR", "SLA", "SLO", "KPI", "ROI", "CAC",
    "LTV", "GTM", "OKR", "QA", "RFC", "TDD", "WCAG", "XSS", "CSRF", "DNS",
}

SMALL_WORDS = {
    "a", "an", "and", "as", "at", "but", "by", "for", "from", "if", "in", "into",
    "nor", "of", "off", "on", "onto", "or", "over", "per", "so", "the", "to",
    "up", "via", "with", "yet", "is", "are", "was", "were", "be", "been", "not",
    "that", "than", "then", "when", "where", "how", "why", "what", "it", "its",
}


@dataclass
class Finding:
    path: str
    line: int
    severity: str
    rule: str
    detail: str


def is_emoji(ch: str) -> bool:
    if ch in "\u200d\ufe0f":
        return False
    code = ord(ch)
    ranges = (
        (0x1F300, 0x1FAFF), (0x1F000, 0x1F2FF), (0x2600, 0x27BF),
        (0x2B00, 0x2BFF), (0xFE0F, 0xFE0F), (0x1F1E6, 0x1F1FF),
    )
    if any(lo <= code <= hi for lo, hi in ranges):
        return True
    return unicodedata.category(ch) == "So" and code > 0x2100


def strip_code_and_fences(lines: list[str]) -> list[bool]:
    """Return a mask marking lines that sit inside a fenced code block."""
    inside = False
    mask = []
    for line in lines:
        if line.lstrip().startswith("```"):
            mask.append(True)
            inside = not inside
            continue
        mask.append(inside)
    return mask


def looks_title_case(heading: str) -> bool:
    words = [w for w in re.findall(r"[A-Za-z][A-Za-z'\-]*", heading)]
    if len(words) < 3:
        return False
    significant = [w for w in words[1:] if w.lower() not in SMALL_WORDS]
    if len(significant) < 2:
        return False
    capped = 0
    for w in significant:
        if w.upper() in ACRONYM_OK or w.isupper():
            continue
        if w[0].isupper():
            capped += 1
    checkable = [w for w in significant if not (w.upper() in ACRONYM_OK or w.isupper())]
    if not checkable:
        return False
    return capped == len(checkable)


Add = Callable[[int, str, str, str], None]

# Each family below reports at most one finding of its kind per line and shares
# the single-line, single-pass contract, so the order of families here is the
# reported order and must not change.
PATTERN_FAMILIES = [
    (COPULA_AVOIDANCE, "low", "copula-avoidance", "replaces a plain is or has: %s"),
    (SIGNIFICANCE_PADDING, "medium", "significance-padding",
     "unsourced claim about importance or legacy"),
    (VAGUE_ATTRIBUTION, "medium", "vague-attribution",
     "opinion attributed to an unnamed authority"),
    (COLLABORATIVE_CHATTER, "high", "chatter",
     "text addressed to the operator rather than the reader"),
    (CUTOFF_DISCLAIMERS, "high", "cutoff-disclaimer",
     "knowledge cutoff or missing source disclaimer"),
    (SECTION_SUMMARY, "medium", "section-summary",
     "restating conclusion or a formulaic challenges section"),
    (NEGATIVE_PARALLELISM, "low", "negative-parallelism", "not X but Y construction"),
]


def scan_artifacts(add: Add, i: int, line: str) -> None:
    """Report leaked tool markup and unfilled placeholders on one line.

    Runs before the code-fence skip because these are proof of origin even
    inside a fence.
    """
    for pat, label in ARTIFACTS:
        if re.search(pat, line, re.I):
            add(i, "high", "artifact", label)
    for pat, label in PLACEHOLDERS:
        if re.search(pat, line, re.I):
            add(i, "high", "placeholder", label)


def scan_typography(add: Add, i: int, line: str) -> None:
    """Report punctuation and typography markers on one line."""
    if "\u2014" in line:
        add(i, "medium", "em-dash", "em dash, use a comma, colon, parentheses or a new sentence")
    if re.search(r"\w\s*\u2013\s*\w", line) and not re.search(r"\d\s*\u2013\s*\d", line):
        add(i, "medium", "en-dash", "en dash used as sentence punctuation")
    for ch in "\u2018\u2019\u201c\u201d":
        if ch in line:
            add(i, "medium", "curly-quote", "curly quotation mark or apostrophe, use ASCII")
            break
    bad_emoji = [c for c in line if is_emoji(c)]
    if bad_emoji:
        add(i, "medium", "emoji", "emoji used in text: " + " ".join(sorted(set(bad_emoji))))
    if re.fullmatch(r"\s*(-{3,}|\*{3,}|_{3,})\s*", line):
        add(i, "medium", "thematic-break", "horizontal rule between sections")


def scan_headings(add: Add, i: int, line: str) -> None:
    """Report title case headings and puffery noun pairings on one line."""
    heading = re.match(r"\s*(#{1,6})\s+(.*\S)\s*$", line)
    if not heading:
        return
    body = heading.group(2)
    if looks_title_case(body):
        add(i, "medium", "title-case-heading", "title case heading: " + body[:60])
    two_noun = re.fullmatch(r"([A-Za-z]+) and ([A-Za-z]+)", body.strip())
    if two_noun and {two_noun.group(1).lower(), two_noun.group(2).lower()} & PUFFERY_NOUNS:
        add(i, "low", "x-and-y-heading",
            "heading pairs a puffery noun with another: " + body)


def scan_line_shapes(add: Add, i: int, line: str) -> None:
    """Report list-item and sentence-opening shapes on one line."""
    if re.match(r"\s*[-*+]\s+\*\*[^*]{2,40}\*\*\s*:", line):
        add(i, "low", "bold-label-list", "bold inline header on a list item")
    if re.match(r"\s*Additionally,", line):
        add(i, "medium", "vocab", "sentence opening with Additionally")


def scan_pattern_families(add: Add, i: int, line: str) -> None:
    """Report the first match from each regex-list family on one line.

    The detail for copula-avoidance carries the matched pattern; the rest use a
    fixed message, which is why the message field doubles as a format string.
    """
    for patterns, sev, rule, detail in PATTERN_FAMILIES:
        for pat in patterns:
            if re.search(pat, line, re.I):
                add(i, sev, rule, detail % pat if "%s" in detail else detail)
                break


def scan_sentence_constructions(add: Add, i: int, raw: str, line: str) -> None:
    """Report participle tails, three adjective rhythm and trailing space."""
    tail = re.search(PARTICIPLE_TAIL, line, re.I)
    if tail:
        add(i, "low", "participle-tail",
            "comment clause tacked on with '" + tail.group(1) + "'")
    for triple in re.findall(r"\b([a-z]+),\s+([a-z]+),\s+and\s+([a-z]+)\b", line):
        if all(len(w) > 4 and w.endswith(ADJ_SUFFIXES) for w in triple):
            add(i, "low", "rule-of-three", "three adjective rhythm: " + ", ".join(triple))
            break
    if raw != raw.rstrip():
        add(i, "low", "trailing-space", "trailing whitespace")


def accumulate_vocab(line: str, i: int, hits: dict[str, list[int]]) -> int:
    """Record overrepresented terms and phrases, returning the line word count."""
    lowered = line.lower()
    for w in VOCAB:
        for _ in re.finditer(r"\b" + re.escape(w) + r"\b", lowered):
            hits.setdefault(w, []).append(i)
    for p in VOCAB_PHRASES:
        if p in lowered:
            hits.setdefault(p, []).append(i)
    return len(re.findall(r"[a-z']+", lowered))


def report_vocab(add: Add, hits: dict[str, list[int]], word_total: int) -> None:
    """Emit per-term vocab findings and the aggregate density finding."""
    total = sum(len(v) for v in hits.values())
    density = (total / word_total * 1000) if word_total else 0.0
    for word, hit_lines in sorted(hits.items()):
        sev = "medium" if len(hit_lines) > 1 else "low"
        add(hit_lines[0], sev, "vocab",
            "overrepresented term '%s' x%d (lines %s)"
            % (word, len(hit_lines), ",".join(str(n) for n in hit_lines[:8])))
    if density > 4.0:
        add(1, "medium", "vocab-density",
            "overrepresented vocabulary density %.1f per 1000 words, budget 4.0" % density)


def scan(path: str, text: str) -> list[Finding]:
    out: list[Finding] = []
    lines = text.splitlines()
    exemptions = parse_exemptions(lines)
    exempt_vocab = "vocab" in exemptions
    in_code = strip_code_and_fences(lines)
    in_frontmatter = False
    vocab_hits: dict[str, list[int]] = {}
    word_total = 0

    def add(n: int, sev: str, rule: str, detail: str) -> None:
        if rule in exemptions:
            return
        out.append(Finding(path, n, sev, rule, detail))

    for i, raw in enumerate(lines, start=1):
        line = raw
        if i == 1 and line.strip() == "---":
            in_frontmatter = True
            continue
        if in_frontmatter:
            if line.strip() == "---":
                in_frontmatter = False
            continue
        scan_artifacts(add, i, line)
        if in_code[i - 1]:
            continue
        scan_typography(add, i, line)
        scan_headings(add, i, line)
        scan_line_shapes(add, i, line)
        scan_pattern_families(add, i, line)
        scan_sentence_constructions(add, i, raw, line)
        if not exempt_vocab:
            word_total += accumulate_vocab(line, i, vocab_hits)

    if vocab_hits:
        report_vocab(add, vocab_hits, word_total)

    if lines and not text.endswith("\n"):
        add(len(lines), "low", "final-newline", "file does not end with a newline")

    return out


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(
        prog="ai_tells.py",
        description="Report stylistic markers of machine generated prose.")
    ap.add_argument("paths", nargs="*", help="files to scan, or stdin if omitted")
    ap.add_argument("--strict", action="store_true", help="fail on medium findings too")
    ap.add_argument("--pedantic", action="store_true", help="fail on any finding")
    ap.add_argument("--quiet", action="store_true", help="print only the summary")
    args = ap.parse_args(argv)

    targets: list[tuple[str, str]] = []
    if args.paths:
        for p in args.paths:
            fp = Path(p)
            if not fp.is_file():
                print("skip (not a file): %s" % p, file=sys.stderr)
                continue
            try:
                targets.append((p, fp.read_text(encoding="utf-8")))
            except UnicodeDecodeError:
                print("skip (not utf-8 text): %s" % p, file=sys.stderr)
    else:
        targets.append(("<stdin>", sys.stdin.read()))

    if not targets:
        print("nothing to scan", file=sys.stderr)
        return 2

    findings: list[Finding] = []
    exempt_report: list[tuple[str, set[str]]] = []
    for path, text in targets:
        ex = parse_exemptions(text.splitlines())
        if ex:
            exempt_report.append((path, ex))
        findings.extend(scan(path, text))

    order = {"high": 0, "medium": 1, "low": 2}
    findings.sort(key=lambda f: (order[f.severity], f.path, f.line))

    counts = {"high": 0, "medium": 0, "low": 0}
    for f in findings:
        counts[f.severity] += 1
        if not args.quiet:
            print("%-6s %s:%d  [%s] %s" % (f.severity, f.path, f.line, f.rule, f.detail))

    if exempt_report and not args.quiet:
        print("\ndeclared exemptions (files that document these patterns):")
        for path, ex in exempt_report:
            print("  %s: %s" % (path, ",".join(sorted(ex))))

    print("\nscanned %d file(s): %d high, %d medium, %d low"
          % (len(targets), counts["high"], counts["medium"], counts["low"]))

    if args.pedantic:
        return 1 if findings else 0
    if args.strict:
        return 1 if (counts["high"] or counts["medium"]) else 0
    return 1 if counts["high"] else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))

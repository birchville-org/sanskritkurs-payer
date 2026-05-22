#!/usr/bin/env python3
"""
add_grammar_boxes.py

For deficit lessons: finds yellow-table content in the HTML source and
wraps the corresponding MD paragraph(s) in ::: grammar-box containers.

Usage:
    python3 scripts/add_grammar_boxes.py <lesson_num>   # single lesson
    python3 scripts/add_grammar_boxes.py all            # lessons with deficit
"""

import sys, os, re, html as html_mod
from html.parser import HTMLParser

BASE   = "/Volumes/SanDisk1TB/proj/Payer"
QA_DIR = os.path.join(BASE, "docs/public/qa")
MD_DIR = os.path.join(BASE, "docs/lektionen")

# ── HTML parser: extract text content of each bgcolor=#FFFFCC table ──────────

class GrammarBoxExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.boxes = []          # list of text strings, one per yellow table
        self._depth = 0          # nesting depth inside a yellow table
        self._buf   = []         # text buffer for current box
        self._in_box = False

    def handle_starttag(self, tag, attrs):
        attrs_d = dict(attrs)
        bg = attrs_d.get("bgcolor", "").upper().replace("#","")
        if tag == "table" and bg in ("FFFFCC", "FFFFCC".lower().upper()):
            if not self._in_box:
                self._in_box = True
                self._depth  = 1
                self._buf    = []
            else:
                self._depth += 1
        elif self._in_box and tag == "table":
            self._depth += 1
        # bold marker
        if self._in_box and tag in ("b", "strong"):
            self._buf.append("\x02BOLD_ON\x02")

    def handle_endtag(self, tag):
        if self._in_box and tag == "table":
            self._depth -= 1
            if self._depth == 0:
                self._in_box = False
                text = " ".join(self._buf).strip()
                text = re.sub(r'\s+', ' ', text)
                # remove bold markers for matching purposes
                text = text.replace("\x02BOLD_ON\x02", "")
                if text:
                    self.boxes.append(text)

    def handle_data(self, data):
        if self._in_box:
            stripped = data.strip()
            if stripped:
                self._buf.append(stripped)


def extract_html_boxes(html_path):
    with open(html_path, encoding="utf-8", errors="replace") as f:
        html_src = f.read()
    # decode HTML entities
    html_src = html_mod.unescape(html_src)
    parser = GrammarBoxExtractor()
    parser.feed(html_src)
    return parser.boxes


# ── Normalise text for fuzzy matching ────────────────────────────────────────

def normalise(text):
    """Strip bold markers, collapse whitespace, lowercase."""
    text = re.sub(r'\*+', '', text)          # strip markdown bold
    text = re.sub(r'\[\[br\]\]', ' ', text)  # expand [[br]]
    text = re.sub(r'::+\s*\S+', '', text)    # strip container markers
    text = re.sub(r'[#\-\*\_]', '', text)    # strip markdown syntax
    text = re.sub(r'\s+', ' ', text).strip().lower()
    return text


def first_words(text, n=8):
    """Return first n words of normalised text."""
    return ' '.join(normalise(text).split()[:n])


# ── Check if a MD block is already inside a grammar-box ──────────────────────

def already_wrapped(md_content, match_start):
    """Return True if match_start is inside a grammar-box (stack-based parser)."""
    before = md_content[:match_start]
    # Stack of (colon_count, container_type) tuples
    stack = []
    for line in before.split('\n'):
        stripped = line.strip()
        m_open = re.match(r'^(:::+)\s+(\S+)', stripped)
        m_close = re.match(r'^(:::+)\s*$', stripped)
        if m_open:
            stack.append((len(m_open.group(1)), m_open.group(2)))
        elif m_close:
            colon_count = len(m_close.group(1))
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == colon_count:
                    stack.pop(i)
                    break
    return any(ctype == 'grammar-box' for _, ctype in stack)


# ── Find the MD paragraph that corresponds to an HTML box text ───────────────

def find_md_match(md_content, box_text):
    """
    Find the start/end of the MD block that best matches the HTML box text.
    Returns (start, end) char offsets into md_content, or None.
    """
    key = first_words(box_text, 6)
    if not key:
        return None

    # Build a regex from the key words (allow any whitespace/markdown between words)
    words = key.split()
    # escape each word
    escaped = [re.escape(w) for w in words]
    # allow [\s\S]{0,40} between words to account for bold markers etc.
    pattern = r'[\s\S]{0,30}'.join(escaped)

    m = re.search(pattern, md_content, re.I)
    if not m:
        return None

    # Find paragraph boundaries around the match
    pos = m.start()

    # Walk back to start of paragraph block (blank line or section header)
    block_start = pos
    while block_start > 0 and md_content[block_start-1] != '\n':
        block_start -= 1
    # Walk further back: include any adjacent list items / lines in same block
    while block_start > 0:
        prev_line_end = block_start - 1
        prev_line_start = md_content.rfind('\n', 0, prev_line_end)
        prev_line = md_content[prev_line_start+1:prev_line_end+1].strip()
        if prev_line == '' or prev_line.startswith('#') or prev_line.startswith(':::'):
            break
        block_start = prev_line_start + 1

    # Walk forward: include list items, additional paragraphs that are part of box
    # Strategy: include up to the next blank line followed by a non-list, non-bold line
    block_end = m.end()
    # extend to end of current line
    nl = md_content.find('\n', block_end)
    block_end = nl + 1 if nl >= 0 else len(md_content)

    # Extend through continuation lines (list items, non-blank)
    while block_end < len(md_content):
        next_nl = md_content.find('\n', block_end)
        if next_nl < 0:
            block_end = len(md_content)
            break
        line = md_content[block_end:next_nl].strip()
        if line == '':
            # blank line – stop here (don't include it)
            break
        if line.startswith('#'):
            break
        block_end = next_nl + 1

    return block_start, block_end


# ── Wrap a text block in grammar-box ─────────────────────────────────────────

def make_bold_lines(block_text):
    """Make non-empty, non-container, non-list-continuation lines bold."""
    result = []
    for line in block_text.split('\n'):
        stripped = line.strip()
        if not stripped:
            result.append(line)
        elif stripped.startswith(':::') or stripped.startswith('#'):
            result.append(line)
        elif stripped.startswith('*') or stripped.startswith('-'):
            # list item – make content bold if not already
            if '**' not in line:
                line = re.sub(r'^(\s*[\*\-]\s*)(.*)', lambda m: m.group(1) + '**' + m.group(2) + '**', line)
            result.append(line)
        else:
            if '**' not in line:
                line = '**' + stripped + '**'
            result.append(line)
    return '\n'.join(result)


def wrap_block(block_text):
    """
    Decide whether to use ::: or :::: grammar-box and wrap the block.
    Use :::: if the block contains a ::: indent / ::: media block.
    """
    has_nested = bool(re.search(r'^:::', block_text, re.M))
    outer = '::::' if has_nested else ':::'
    bolded = make_bold_lines(block_text.rstrip())
    return f"{outer} grammar-box\n{bolded}\n{outer}\n"


# ── Main processing for one lesson ───────────────────────────────────────────

def process_lesson(n):
    html_path = os.path.join(QA_DIR, f"lektion{n}.html")
    md_path   = os.path.join(MD_DIR,  f"lektion{n:02d}.md")

    if not os.path.exists(html_path):
        print(f"L{n}: HTML not found, skipping.")
        return
    if not os.path.exists(md_path):
        print(f"L{n}: MD not found, skipping.")
        return

    html_boxes = extract_html_boxes(html_path)
    with open(md_path, encoding="utf-8") as f:
        md_content = f.read()

    # Count existing grammar-boxes
    existing = len(re.findall(r'^:::+\s*grammar-box', md_content, re.M))
    print(f"\nL{n}: {len(html_boxes)} HTML boxes, {existing} MD boxes already present.")

    changes = 0
    # Process boxes in reverse order of occurrence so offsets don't shift
    matches = []
    for box_text in html_boxes:
        result = find_md_match(md_content, box_text)
        if result is None:
            print(f"  [SKIP] No MD match for: {box_text[:60]!r}")
            continue
        start, end = result
        if already_wrapped(md_content, start):
            continue  # already in a grammar-box
        matches.append((start, end, box_text))

    # Deduplicate overlapping matches (keep first match for each region)
    seen_regions = []
    unique_matches = []
    for (s, e, t) in sorted(matches):
        overlaps = any(s < es and e > ss for ss, es in seen_regions)
        if not overlaps:
            seen_regions.append((s, e))
            unique_matches.append((s, e, t))

    # Apply in reverse order
    for start, end, box_text in sorted(unique_matches, key=lambda x: x[0], reverse=True):
        block_text = md_content[start:end]
        wrapped    = wrap_block(block_text)
        md_content = md_content[:start] + wrapped + md_content[end:]
        changes += 1

    with open(md_path, 'w', encoding="utf-8") as f:
        f.write(md_content)

    new_count = len(re.findall(r'^:::+\s*grammar-box', md_content, re.M))
    print(f"  Applied {changes} wrappers. MD now has {new_count} grammar-boxes.")


# ── Entry point ───────────────────────────────────────────────────────────────

DEFICIT_LESSONS = [52, 54, 56, 57, 61]

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: add_grammar_boxes.py <lesson_num|all>")
        sys.exit(1)

    arg = sys.argv[1]
    if arg == "all":
        lessons = DEFICIT_LESSONS
    else:
        lessons = [int(arg)]

    for n in lessons:
        process_lesson(n)
    print("\nDone.")

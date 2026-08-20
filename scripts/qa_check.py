import os
import re
import sys
import html as html_mod

BASE   = "/Volumes/SanDisk1TB/proj/Payer"
QA_DIR = os.path.join(BASE, "docs/public/qa")


# ── Signalrot check ───────────────────────────────────────────────────────────

def _red_texts_from_html(html_path):
    """Return list of normalised red-text strings from <font color="#FF0000">."""
    with open(html_path, encoding="utf-8", errors="replace") as f:
        src = html_mod.unescape(f.read())
    raw_list = re.findall(
        r'<font[^>]*color="#?FF0000[^>]*>([\s\S]*?)</font>', src, re.I
    )
    results = []
    for raw in raw_list:
        text = re.sub(r'<[^>]+>', '', raw).strip()
        text = re.sub(r'\s+', ' ', text)
        if text:
            results.append(text)
    return results


def check_signalrot(md_filepath, content):
    """
    Cross-reference <font color="#FF0000"> entries in the QA HTML against
    ***text*** markers in the MD.  Returns list of error strings.
    Only runs when a matching QA HTML file exists.
    """
    errors = []
    m = re.search(r'lektion(\d+)\.md$', md_filepath)
    if not m:
        return errors
    n = int(m.group(1))
    html_path = os.path.join(QA_DIR, f"lektion{n}.html")
    if not os.path.exists(html_path):
        return errors

    red_texts = _red_texts_from_html(html_path)
    if not red_texts:
        return errors

    # Metrik symbol equivalences: QA HTML uses modifier letters, MD uses Unicode symbols
    METRIK_EQUIV = {
        '˘': '◡', 'ˉ': '—',
    }

    missing = []
    for text in red_texts:
        # Also try with backslash-escaped leading dash (suffix notation: \-xyz)
        escaped_text = re.sub(r'^-', r'\\-', text)
        # Also try with metrik symbol equivalences (˘→◡, ˉ→—, with spaces between)
        equiv_text = ' '.join(METRIK_EQUIV.get(c, c) for c in text)
        # Accept any asterisk wrapping: *text* or sig[text]
        pattern = r'(?:\*+' + re.escape(text) + r'\*+|sig\[' + re.escape(text) + r'\])'
        pattern_esc = r'(?:\*+' + re.escape(escaped_text) + r'\*+|sig\[' + re.escape(escaped_text) + r'\])'
        pattern_equiv = r'(?:\*+' + re.escape(equiv_text) + r'\*+|sig\[' + re.escape(equiv_text) + r'\])'
        # Also accept text that appears as part of a Markdown heading (## ... text ...)
        pattern_heading = r'^#{1,6}\s+.*' + re.escape(text)
        if (not re.search(pattern, content)
                and not re.search(pattern_esc, content)
                and not re.search(pattern_equiv, content)
                and not re.search(pattern_heading, content, re.MULTILINE)):
            missing.append(text)

    total = len(red_texts)
    found = total - len(missing)
    if missing:
        errors.append(
            f"Signalrot: {found}/{total} present — missing: "
            + ", ".join(repr(t) for t in missing)
        )
    return errors


# ── Grammar-box scope check ──────────────────────────────────────────────────

def _yellow_table_word_counts(html_path):
    """Return list of word counts for each yellow bgcolor table in the HTML."""
    with open(html_path, encoding='utf-8', errors='replace') as f:
        src = html_mod.unescape(f.read())
    tables = re.findall(
        r'<table[^>]*bgcolor="[#]?[Ff]{4}[Cc]{2}"[^>]*>([\s\S]*?)</table>',
        src, re.I
    )
    counts = []
    for t in tables:
        text = re.sub(r'<[^>]+>', ' ', t)
        text = re.sub(r'\s+', ' ', text).strip()
        counts.append(len(text.split()) if text else 0)
    return counts


def _grammarbox_word_counts(content):
    """Return list of word counts for each grammar-box in the MD."""
    lines = content.split('\n')
    counts = []
    in_box = False
    box_lines = []
    depth = 0
    for line in lines:
        if re.match(r'^:{3,}\s*grammar-box', line):
            in_box = True; depth = 1; box_lines = []
        elif in_box:
            if re.match(r'^:{3,}\s*[^\s:]', line):
                depth += 1; box_lines.append(line)
            elif re.match(r'^:{3,}\s*$', line):
                depth -= 1
                if depth == 0:
                    in_box = False
                    text = '\n'.join(box_lines)
                    text = re.sub(r'\|+', ' ', text)
                    text = re.sub(r'\[\[br\]\]', ' ', text)
                    text = re.sub(r'[*_`#>:]', '', text)
                    text = re.sub(r'\s+', ' ', text).strip()
                    counts.append(len(text.split()) if text else 0)
                else:
                    box_lines.append(line)
            else:
                box_lines.append(line)
    return counts


def check_grammarbox_scope(md_filepath, content):
    """
    Detect potentially truncated grammar-boxes.

    Check 1 (structural): grammar-box immediately followed by a bullet list —
    the classic pattern where closing ::: cuts off the rule's enumeration.

    Check 2 (HTML-based, only when table count == box count): if the MD
    grammar-box word count is < 55 % of the corresponding HTML yellow table,
    flag it as truncated.
    """
    errors = []

    # Check 1: orphaned bullet list after grammar-box
    lines = content.split('\n')
    i = 0
    box_num = 0
    in_box = False
    depth = 0
    while i < len(lines):
        line = lines[i]
        if re.match(r'^:{3,}\s*grammar-box', line):
            in_box = True; depth = 1
        elif in_box:
            if re.match(r'^:{3,}\s*\S+', line):
                depth += 1
            elif re.match(r'^:{3,}\s*$', line):
                depth -= 1
                if depth == 0:
                    in_box = False
                    box_num += 1
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j < len(lines) and lines[j].startswith('- '):
                        errors.append(
                            f"Grammar-box {box_num} possibly truncated: "
                            f"immediately followed by bullet list (line {j + 1})"
                        )
        i += 1

    # Check 2: HTML word-count comparison (only when table count == box count)
    m = re.search(r'lektion(\d+)\.md$', md_filepath)
    if m:
        n = int(m.group(1))
        html_path = os.path.join(QA_DIR, f"lektion{n}.html")
        if os.path.exists(html_path):
            html_counts = _yellow_table_word_counts(html_path)
            md_counts = _grammarbox_word_counts(content)
            if html_counts and len(html_counts) == len(md_counts):
                for idx, (hw, mw) in enumerate(zip(html_counts, md_counts)):
                    if hw >= 20 and mw / hw < 0.55:
                        errors.append(
                            f"Grammar-box {idx + 1} possibly truncated: "
                            f"{mw} words vs {hw} in HTML ({mw / hw:.0%})"
                        )

    return errors


# ── Container nesting and syntax check ───────────────────────────────────────

def check_container_nesting(content):
    errors = []
    # matches 3 to 6 colons optionally followed by a word
    container_re = re.compile(r'^(?P<colons>:{3,6})\s*(?P<name>[a-zA-Z0-9_-]+)?')
    stack = []
    
    valid_containers = {
        'indent', 'grammar-box', 'media', 'deleteme-box', 'literatur-box', 'literatur', 'note-box',
        'no-header', 'tip', 'warning', 'important', 'center', 'metrik-schema'
    }
    
    for idx, line in enumerate(content.split('\n')):
        line_stripped = line.strip()
        m = container_re.match(line_stripped)
        if m:
            colons = m.group('colons')
            name = m.group('name')
            colons_count = len(colons)
            line_num = idx + 1
            
            if name:
                name_lower = name.lower()
                
                if name_lower not in valid_containers:
                    errors.append(f"Line {line_num}: Unknown container name '{name_lower}'")
                
                if stack:
                    parent_name, parent_colons, parent_line = stack[-1]
                    
                    # Depth hierarchy check: outer must have strictly more colons than inner
                    if parent_colons <= colons_count:
                        errors.append(
                            f"Line {line_num}: Nested container '{name_lower}' ({colons_count} colons) "
                            f"inside '{parent_name}' ({parent_colons} colons) in line {parent_line}. "
                            f"Outer container must have more colons than inner."
                        )
                    
                    # Media should never be nested inside anything
                    if name_lower == 'media':
                        errors.append(
                            f"Line {line_num}: Media block '{name_lower}' is nested inside '{parent_name}' (line {parent_line}). "
                            f"Media blocks must be placed at the root level."
                        )
                
                stack.append((name_lower, colons_count, line_num))
            else:
                # Closing tag
                found_idx = -1
                for i in range(len(stack) - 1, -1, -1):
                    if stack[i][1] == colons_count:
                        found_idx = i
                        break
                if found_idx != -1:
                    stack = stack[:found_idx]
                else:
                    errors.append(f"Line {line_num}: Redundant closing container tag '{colons}' (no matching open tag)")
                    
    for name, colons_count, line_num in stack:
        errors.append(f"Line {line_num}: Unclosed container '{name}' (depth {colons_count})")
        
    return errors


# ── existing checks ───────────────────────────────────────────────────────────

def check_markdown_file(filepath):
    errors = []
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        lines = content.split('\n')

    # 1. Check YAML Frontmatter
    if not content.startswith('---\n'):
        errors.append("Missing YAML Frontmatter start ('---')")
    else:
        parts = content.split('---\n')
        if len(parts) < 3:
             errors.append("Missing YAML Frontmatter end ('---')")

    # 2. Check for exactly one H1
    h1_count = len(re.findall(r'^# ', content, re.MULTILINE))
    if h1_count == 0:
        errors.append("Missing H1 heading (# ...)")
    elif h1_count > 1:
        errors.append(f"Multiple H1 headings found ({h1_count})")

    # 3. Cyrillic injection check
    cyrillic_chars = re.findall(r'[Ѐ-ӿ]', content)
    is_bg = "/bg/" in filepath
    if cyrillic_chars and not is_bg:
         errors.append(f"Found {len(cyrillic_chars)} Cyrillic characters in non-Bulgarian file.")

    # 4. Container nesting and syntax check
    errors.extend(check_container_nesting(content))

    # 5. Signalrot + grammar-box scope (only for German DE lessons with QA HTML)
    is_de_lesson = (
        "/lektionen/" in filepath
        and "/bg/" not in filepath and "/en/" not in filepath
        and "/es/" not in filepath and "/it/" not in filepath
        and "/ru/" not in filepath and "/uk/" not in filepath
    )
    if is_de_lesson:
        errors.extend(check_signalrot(filepath, content))
        errors.extend(check_grammarbox_scope(filepath, content))

    return errors


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 qa_check.py <file_or_dir>")
        sys.exit(1)

    target = sys.argv[1]
    if os.path.isfile(target):
        files = [target]
    else:
        files = [
            os.path.join(dp, f)
            for dp, dn, filenames in os.walk(target)
            for f in filenames
            if f.endswith(".md") and (
                re.match(r'lektion\d+\.md$', f) or
                re.match(r'uebung\d+\.md$', f)
            )
        ]

    total_errors = 0
    for f in sorted(files):
        file_errors = check_markdown_file(f)
        if file_errors:
            print(f"❌ {f}:")
            for err in file_errors:
                print(f"  - {err}")
            total_errors += len(file_errors)
        else:
            print(f"✅ {f}: OK")

    if total_errors:
        print(f"\nTotal errors found: {total_errors}")
        sys.exit(1)
    else:
        print("\nAll checks passed!")
        sys.exit(0)

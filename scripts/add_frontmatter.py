#!/usr/bin/env python3
"""
add_frontmatter.py — Backfills missing title/subtitle/category/status into DE lesson files.

For DE files in docs/lektionen/ that are missing `title`, derives:
  title    → "Lektion N"  (from lesson_id frontmatter or # heading)
  subtitle → first bullet in deleteme-box, or first ## N.N. section heading
  category → "Grammatik" (added only if absent)
  status   → stable       (added only if absent)

All existing frontmatter lines (lesson_id, last_reconstructed, next, …) are preserved verbatim.

Usage:
  python3 scripts/add_frontmatter.py           # dry-run (prints only)
  python3 scripts/add_frontmatter.py --write   # actually modify files
"""

import os
import re
import sys

LEKTIONEN_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs', 'lektionen')


def split_frontmatter(content):
    """Return (fm_lines, fm_keys, body) or (None, {}, content) if no frontmatter."""
    if not content.startswith('---\n'):
        return None, {}, content
    end = content.find('\n---', 3)
    if end == -1:
        return None, {}, content
    fm_block = content[4:end]          # text between opening and closing ---
    body = content[end + 4:]           # everything after closing ---
    fm_lines = fm_block.splitlines()
    fm_keys = {}
    for line in fm_lines:
        m = re.match(r'^(\w+):\s*(.*)', line)
        if m:
            fm_keys[m.group(1)] = m.group(2).strip('"').strip("'")
    return fm_lines, fm_keys, body


def _is_image_bullet(text):
    """True if a deleteme-box bullet is an image citation rather than a topic."""
    return (
        'Bildquelle' in text or
        re.match(r'^\*\*lekt\d+', text) or
        re.match(r'^\*\*(Abb\.|Image)', text)
    )


def extract_subtitle(body):
    """Derive a subtitle from the deleteme-box first content bullet or first ## heading."""
    # 1. Try all deleteme-box blocks; prefer ones with topic bullets over image citations
    for dm in re.finditer(r':::+ deleteme-box(.*?):::+', body, re.DOTALL):
        bullets = re.findall(r'^- (.+)', dm.group(1), re.MULTILINE)
        content_bullets = [b.strip() for b in bullets if not _is_image_bullet(b.strip())]
        if content_bullets:
            subtitle = content_bullets[0]
            return subtitle[0].upper() + subtitle[1:] if subtitle else subtitle
    # 2. Fallback: first ## N.N. section heading
    m = re.search(r'^## \d+\.\d+\.\s+(.+)', body, re.MULTILINE)
    if m:
        return m.group(1).strip()
    return ''


def build_new_content(fm_lines, fm_keys, body, lesson_id, subtitle):
    """Prepend title/subtitle; append category/status if absent; keep everything else."""
    new_lines = []
    new_lines.append(f'title: Lektion {lesson_id}')
    if subtitle:
        escaped = subtitle.replace('"', '\\"')
        new_lines.append(f'subtitle: "{escaped}"')
    # Preserve all original frontmatter lines
    new_lines.extend(fm_lines)
    # Add category/status only if not already present
    if 'category' not in fm_keys:
        new_lines.append('category: "Grammatik"')
    if 'status' not in fm_keys:
        new_lines.append('status: stable')
    return '---\n' + '\n'.join(new_lines) + '\n---' + body


def process_file(filepath, write=False):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    fm_lines, fm_keys, body = split_frontmatter(content)
    if fm_lines is None:
        return None  # no frontmatter at all

    if 'title' in fm_keys:
        return None  # already complete

    lesson_id = fm_keys.get('lesson_id', '')
    if not lesson_id:
        m = re.search(r'^# Lektion (\d+)', body, re.MULTILINE)
        lesson_id = m.group(1) if m else '?'

    subtitle = extract_subtitle(body)
    new_content = build_new_content(fm_lines, fm_keys, body, lesson_id, subtitle)

    if write:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

    return (lesson_id, subtitle)


def main():
    args = sys.argv[1:]
    write = '--write' in args
    start, end = 1, 9999
    if '--range' in args:
        i = args.index('--range')
        start, end = int(args[i + 1]), int(args[i + 2])
    mode = 'WRITE' if write else 'DRY-RUN'
    print(f'add_frontmatter.py — {mode}  (lessons {start}–{end})\n')

    updated = []
    for fname in sorted(os.listdir(LEKTIONEN_DIR)):
        if not re.match(r'^lektion\d+\.md$', fname):
            continue
        m = re.match(r'^lektion(\d+)\.md$', fname)
        num = int(m.group(1))
        if num < start or num > end:
            continue
        path = os.path.join(LEKTIONEN_DIR, fname)
        result = process_file(path, write=write)
        if result is not None:
            lesson_id, subtitle = result
            status = 'UPDATED' if write else 'WOULD UPDATE'
            print(f'  [{status}] {fname}')
            print(f'           title:    Lektion {lesson_id}')
            if subtitle:
                print(f'           subtitle: "{subtitle}"')
            else:
                print(f'           subtitle: (none derived — check manually)')
            updated.append(fname)

    print(f'\nTotal: {len(updated)} file(s) {"updated" if write else "would be updated"}.')
    if not write:
        print('\nRerun with --write to apply changes.')


if __name__ == '__main__':
    main()

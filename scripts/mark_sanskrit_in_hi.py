#!/usr/bin/env python3
"""
Mark Sanskrit Devanagari in existing Hindi lesson files with ⟪⟫ markers.

For each docs/hi/lektionen/lektion*.md, reads the corresponding German source
(docs/lektionen/lektion*.md) to extract Sanskrit Devanagari runs.
Those runs are then wrapped with ⟪⟫ in the Hindi file so scholarly_fixes
can render them red, while unmarked Hindi Devanagari stays black.

Idempotent: strips existing ⟪⟫ markers before re-applying.
"""

import os
import re
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DE_DIR = os.path.join(BASE_DIR, 'docs', 'lektionen')
HI_DIR = os.path.join(BASE_DIR, 'docs', 'hi', 'lektionen')

_DEVA_RE = re.compile(r'[ऀ-ॿ]+')
_MARKED_RE = re.compile(r'⟪([ऀ-ॿ]+)⟫')


def mark_sanskrit(hi_content, sanskrit_runs):
    # Strip existing markers for idempotency
    hi_content = _MARKED_RE.sub(r'\1', hi_content)

    def replace_fn(m):
        run = m.group(0)
        return f'⟪{run}⟫' if run in sanskrit_runs else run

    return _DEVA_RE.sub(replace_fn, hi_content)


def process_file(filename):
    de_path = os.path.join(DE_DIR, filename)
    hi_path = os.path.join(HI_DIR, filename)

    if not os.path.exists(de_path):
        print(f'  skip {filename} (no DE source)')
        return
    if not os.path.exists(hi_path):
        print(f'  skip {filename} (no HI file)')
        return

    de_content = open(de_path, encoding='utf-8').read()
    hi_content = open(hi_path, encoding='utf-8').read()

    sanskrit_runs = set(_DEVA_RE.findall(de_content))
    if not sanskrit_runs:
        print(f'  skip {filename} (no Devanagari in DE source)')
        return

    new_hi = mark_sanskrit(hi_content, sanskrit_runs)

    if new_hi == hi_content:
        print(f'  unchanged {filename}')
        return

    open(hi_path, 'w', encoding='utf-8').write(new_hi)
    marked = len(_MARKED_RE.findall(new_hi))
    print(f'  marked {filename}: {marked} Sanskrit run(s)')


def main():
    if not os.path.isdir(HI_DIR):
        print(f'ERROR: HI directory not found: {HI_DIR}')
        sys.exit(1)

    files = sorted(f for f in os.listdir(HI_DIR) if f.endswith('.md'))
    print(f'Processing {len(files)} Hindi lesson file(s)...')
    for filename in files:
        process_file(filename)
    print('Done.')


if __name__ == '__main__':
    main()

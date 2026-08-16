#!/usr/bin/env python3
"""
QA German Remnants Auditor for Payer Sanskritkurs.
Audits Markdown files in target languages for German remnants using translation_qa.py (Strictly Read-Only).
"""
import os
import sys
import argparse
import glob
from pathlib import Path

ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from translation_qa import is_file_fallback, get_translation_queue, check_has_de_phrases, clean_markdown_for_lid

def main():
    parser = argparse.ArgumentParser(description="Find German remnants in translated Markdown files (read-only QA audit).")
    parser.add_argument('-l', '--lang', required=True, help="Target language code (e.g. en, tr)")
    args = parser.parse_args()

    target_dir = ROOT / "docs" / args.lang / "lektionen"
    if not target_dir.exists():
        print(f"Error: Directory {target_dir} does not exist.")
        return

    md_files = sorted(target_dir.glob("*.md"))
    flagged_count = 0
    for filepath in md_files:
        is_fb, reason = is_file_fallback(filepath, args.lang)
        if is_fb:
            flagged_count += 1
            print(f"    [FALLBACK/REMNANT in {filepath.name}]: {reason}")

    print(f"\n[QA] Checked {len(md_files)} files in [{args.lang}]. Detected remnants/fallbacks in {flagged_count} files (Read-Only).")
    sys.exit(0)

if __name__ == '__main__':
    main()


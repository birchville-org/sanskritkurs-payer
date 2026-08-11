#!/usr/bin/env python3
"""
Structural Diff Validator for Sanskritkurs Payer.
Compares a translated file against its German master file across 5 structural invariants:
1. Sanskrit / Devanāgarī Tags (⟪...⟫ and sig[...])
2. Markdown Table Dimensions (number of tables, rows, columns)
3. Media / Images (![](...) and ::: media blocks)
4. Custom Containers (::: grammar-box, ::: indent, ::: deleteme-box)
5. Headings (#, ##, ###)

Usage:
  python3 scripts/qa_structure_diff.py --lang ru [--file lektion01.md]
  python3 scripts/qa_structure_diff.py --master docs/lektionen/lektion01.md --target docs/ru/lektionen/lektion01.md
"""

import sys
import os
import re
import argparse

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MASTER_DIR = os.path.join(BASE_DIR, "docs", "lektionen")

def extract_structure(content: str) -> dict:
    """Extract structural metrics from markdown content."""
    lines = content.split('\n')
    
    # 1. Sanskrit Tags
    deva_tags = re.findall(r'⟪[^⟫]+⟫', content)
    sig_tags = re.findall(r'sig\[[^\]]+\]', content)
    
    # 2. Tables
    tables = []
    current_table_rows = 0
    current_table_cols = 0
    in_table = False
    
    for line in lines:
        stripped = line.strip()
        if stripped.startswith('|') and stripped.endswith('|'):
            if not in_table:
                in_table = True
                current_table_rows = 0
                cols = len([c for c in stripped.split('|') if c.strip() or c == '']) - 1
                current_table_cols = cols
            current_table_rows += 1
        else:
            if in_table:
                tables.append({'rows': current_table_rows, 'cols': current_table_cols})
                in_table = False
                current_table_rows = 0
                current_table_cols = 0
    if in_table:
        tables.append({'rows': current_table_rows, 'cols': current_table_cols})

    # 3. Media & Images
    images = re.findall(r'!\[.*?\]\(.*?\)', content)
    media_blocks = len(re.findall(r':::\s*media', content))
    captions = len(re.findall(r'\(Bildquelle:|\(Bildquelle|\(Bild-Quelle|\(Source:|Bildquelle:', content, re.IGNORECASE))

    # 4. Containers
    grammar_boxes = len(re.findall(r':::\s*grammar-box', content))
    indents = len(re.findall(r':::\s*indent', content))
    deleteme_boxes = len(re.findall(r':::\s*deleteme-box', content))

    # 5. Headings
    headings = []
    for line in lines:
        m = re.match(r'^(#{1,6})\s+(.*)', line.strip())
        if m:
            headings.append({'level': len(m.group(1)), 'text': m.group(2).strip()})

    return {
        'deva_tags_count': len(deva_tags),
        'sig_tags_count': len(sig_tags),
        'tables': tables,
        'table_count': len(tables),
        'images_count': len(images),
        'media_blocks_count': media_blocks,
        'captions_count': captions,
        'grammar_boxes': grammar_boxes,
        'indents': indents,
        'deleteme_boxes': deleteme_boxes,
        'headings_count': len(headings),
        'headings': headings
    }

def compare_structures(master_path: str, target_path: str) -> list:
    """Compare structure of master vs target file. Returns list of mismatch descriptions."""
    if not os.path.exists(master_path):
        return [f"Master file not found: {master_path}"]
    if not os.path.exists(target_path):
        return [f"Target file not found: {target_path}"]

    with open(master_path, 'r', encoding='utf-8') as f:
        master_content = f.read()
    with open(target_path, 'r', encoding='utf-8') as f:
        target_content = f.read()

    m_struct = extract_structure(master_content)
    t_struct = extract_structure(target_content)

    mismatches = []

    # Invariant 1: Sanskrit Tags
    m_tags = m_struct['deva_tags_count'] + m_struct['sig_tags_count']
    t_tags = t_struct['deva_tags_count'] + t_struct['sig_tags_count']
    if m_tags != t_tags:
        mismatches.append(f"Sanskrit Tag Count Mismatch: Master={m_tags}, Target={t_tags}")

    # Invariant 2: Tables
    if m_struct['table_count'] != t_struct['table_count']:
        mismatches.append(f"Table Count Mismatch: Master={m_struct['table_count']}, Target={t_struct['table_count']}")
    else:
        for idx, (m_tab, t_tab) in enumerate(zip(m_struct['tables'], t_struct['tables'])):
            if m_tab['rows'] != t_tab['rows']:
                mismatches.append(f"Table {idx+1} Row Count Mismatch: Master={m_tab['rows']}, Target={t_tab['rows']}")

    # Invariant 3: Images & Media
    if m_struct['images_count'] != t_struct['images_count']:
        mismatches.append(f"Image Count Mismatch: Master={m_struct['images_count']}, Target={t_struct['images_count']}")
    if m_struct['media_blocks_count'] != t_struct['media_blocks_count']:
        mismatches.append(f"Media Block Count Mismatch: Master={m_struct['media_blocks_count']}, Target={t_struct['media_blocks_count']}")

    # Invariant 4: Custom Containers
    if m_struct['grammar_boxes'] != t_struct['grammar_boxes']:
        mismatches.append(f"Grammar Box Count Mismatch: Master={m_struct['grammar_boxes']}, Target={t_struct['grammar_boxes']}")
    if m_struct['indents'] != t_struct['indents']:
        mismatches.append(f"Indent Container Count Mismatch: Master={m_struct['indents']}, Target={t_struct['indents']}")

    # Invariant 5: Headings
    if m_struct['headings_count'] != t_struct['headings_count']:
        mismatches.append(f"Heading Count Mismatch: Master={m_struct['headings_count']}, Target={t_struct['headings_count']}")

    return mismatches

def main():
    parser = argparse.ArgumentParser(description="Structural Diff Validator")
    parser.add_argument("--lang", help="Language code (e.g. ru)")
    parser.add_argument("--file", help="Specific filename in lektionen/ (e.g. lektion01.md)")
    parser.add_argument("--master", help="Explicit path to master file")
    parser.add_argument("--target", help="Explicit path to target file")

    args = parser.parse_args()

    if args.master and args.target:
        mismatches = compare_structures(args.master, args.target)
        if mismatches:
            print(f"❌ Structural Mismatches found between {os.path.basename(args.master)} and {os.path.basename(args.target)}:")
            for m in mismatches:
                print(f"  - {m}")
            sys.exit(1)
        else:
            print(f"✓ Structural Integrity Verified: {os.path.basename(args.target)} matches {os.path.basename(args.master)} perfectly!")
            sys.exit(0)

    if not args.lang:
        print("Error: Specify --lang CODE or both --master and --target")
        sys.exit(1)

    target_dir = os.path.join(BASE_DIR, "docs", args.lang, "lektionen")
    if not os.path.exists(target_dir):
        print(f"Error: Target directory does not exist: {target_dir}")
        sys.exit(1)

    files_to_check = [args.file] if args.file else sorted(os.listdir(MASTER_DIR))
    total_checked = 0
    failed_files = 0

    for fname in files_to_check:
        if not fname.endswith('.md'):
            continue
        m_path = os.path.join(MASTER_DIR, fname)
        t_path = os.path.join(target_dir, fname)

        if not os.path.exists(t_path):
            continue

        mismatches = compare_structures(m_path, t_path)
        total_checked += 1
        if mismatches:
            failed_files += 1
            print(f"❌ {fname} (lang: {args.lang}):")
            for m in mismatches:
                print(f"    - {m}")

    if failed_files > 0:
        print(f"\nSummary: {failed_files}/{total_checked} files failed structural validation for lang '{args.lang}'.")
        sys.exit(1)
    else:
        print(f"\n✓ All {total_checked} files for lang '{args.lang}' passed structural validation with 100% parity!")
        sys.exit(0)

if __name__ == "__main__":
    main()

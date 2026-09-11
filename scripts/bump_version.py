#!/usr/bin/env python3
"""
Synchronizes the release version from package.json across:
  - docs/index.md and all docs/*/index.md
  - docs/settings.md and all docs/*/settings.md
  - docs/release-notes.md

Usage:
  python3 scripts/sync_release_version.py [--check]
"""

import sys
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def get_target_version():
    pkg_path = ROOT / 'package.json'
    pkg_data = json.loads(pkg_path.read_text(encoding='utf-8'))
    return pkg_data['version']

def sync_index_file(path: Path, target_version: str, check_only: bool = False) -> bool:
    content = path.read_text(encoding='utf-8')
    ver_tag = f"v{target_version}"
    
    # Check if existing version matches
    m = re.search(r'v[0-9]+\.[0-9]+(?:\.[0-9]+)?', content)
    if m:
        if m.group(0) == ver_tag:
            return True
        if check_only:
            return False
        # Replace the version
        new_content = re.sub(r'v[0-9]+\.[0-9]+(?:\.[0-9]+)?', ver_tag, content, count=1)
        path.write_text(new_content, encoding='utf-8')
        return True
    else:
        # File is missing the version line (e.g. docs/vi/index.md)
        if check_only:
            return False
        # Insert before the last ::: of note-box
        if ':::' in content:
            parts = content.rsplit(':::', 1)
            line = f"**Phiên bản hiện tại**: {ver_tag}\n" if '/vi/' in str(path) else f"**Aktuelle Version**: {ver_tag}\n"
            new_content = parts[0].rstrip() + '\n' + line + ':::' + parts[1]
            path.write_text(new_content, encoding='utf-8')
            return True
        return False

def sync_settings_file(path: Path, target_version: str, check_only: bool = False) -> bool:
    content = path.read_text(encoding='utf-8')
    ver_tag = f"v{target_version}"
    
    # Check if existing version matches
    m = re.findall(r'v[0-9]+\.[0-9]+(?:\.[0-9]+)?', content)
    if m:
        if all(v == ver_tag for v in m):
            return True
        if check_only:
            return False
        new_content = re.sub(r'v[0-9]+\.[0-9]+(?:\.[0-9]+)?', ver_tag, content)
        path.write_text(new_content, encoding='utf-8')
        return True
    else:
        # Missing note-box (e.g. docs/af/settings.md)
        if check_only:
            return False
        box = f"""
::: note-box  Informationen & Version
**Huidige weergawe**: `{ver_tag}`
**Vrystellingsnotas & Changelog**: [Wat is nuut in {ver_tag}?](/af/release-notes)
**Bronkode & Bewaarplek**: [GitHub Repository](https://github.com/birchville-org/sanskritkurs-payer)
:::
""" if '/af/' in str(path) else f"""
::: note-box  Informationen & Version
- **Aktuelle Version**: `{ver_tag}`
- **Release Notes & Changelog**: [Was ist neu in {ver_tag}?](/release-notes)
- **Quellcode & Repository**: [GitHub Repository](https://github.com/birchville-org/sanskritkurs-payer)
:::
"""
        new_content = content.rstrip() + '\n' + box.strip() + '\n'
        path.write_text(new_content, encoding='utf-8')
        return True

def main():
    check_only = '--check' in sys.argv
    version = get_target_version()
    print(f"{'Checking' if check_only else 'Synchronizing'} release version v{version}...")
    
    errors = []
    
    # Process index files (excluding .vitepress build artifacts)
    index_files = [f for f in sorted(ROOT.glob('docs/**/index.md')) if '.vitepress' not in f.parts]
    for f in index_files:
        ok = sync_index_file(f, version, check_only=check_only)
        if not ok:
            errors.append(f"{f.relative_to(ROOT)} has outdated or missing version (expected v{version})")
            
    # Process settings files (excluding .vitepress build artifacts)
    settings_files = [f for f in sorted(ROOT.glob('docs/**/settings.md')) if '.vitepress' not in f.parts]
    for f in settings_files:
        ok = sync_settings_file(f, version, check_only=check_only)
        if not ok:
            errors.append(f"{f.relative_to(ROOT)} has outdated or missing version (expected v{version})")
            
    if errors:
        print(f"❌ {len(errors)} version discrepancies found:")
        for err in errors:
            print(f"  - {err}")
        sys.exit(1)
        
    if not check_only:
        try:
            sys.path.insert(0, str(ROOT / 'scripts'))
            from translation_qa import get_file_hash, get_stored_hashes, save_stored_hashes
            stored = get_stored_hashes()
            src_idx = ROOT / 'docs' / 'index.md'
            src_set = ROOT / 'docs' / 'settings.md'
            if src_idx.exists() and src_set.exists():
                src_idx_h = get_file_hash(src_idx)
                src_set_h = get_file_hash(src_set)
                for lang in stored.keys():
                    stored[lang]['index.md'] = src_idx_h
                    stored[lang]['settings.md'] = src_set_h
                save_stored_hashes(stored)
        except Exception as e:
            print(f"  ⚠ Warning: could not update master_hashes.json: {e}")

    print(f"✓ All {len(index_files)} index.md and {len(settings_files)} settings.md files are synchronized to v{version}.")

if __name__ == '__main__':
    main()

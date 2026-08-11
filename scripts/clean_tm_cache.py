#!/usr/bin/env python3
"""
Scans all Translation Memory JSON caches in docs/.payer/tm/ and purges:
1. Any entry containing 'ERROR:'
2. Any non-German TM entry where '# Lektion' or '## Lektion' was stored instead of the localized heading.
"""

import os
import glob
import json
import re

TM_DIR = "/Volumes/SanDisk1TB/proj/Payer/docs/.payer/tm"

def clean_tm_caches():
    if not os.path.exists(TM_DIR):
        print("TM directory not found.")
        return

    tm_files = glob.glob(os.path.join(TM_DIR, "*.json"))
    total_purged = 0

    for filepath in sorted(tm_files):
        lang = os.path.basename(filepath).replace(".json", "")
        with open(filepath, 'r', encoding='utf-8') as f:
            try:
                tm_data = json.load(f)
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
                continue

        purged_keys = []
        for key, val in list(tm_data.items()):
            if not isinstance(val, str):
                continue
            # Purge ERROR strings
            if "ERROR:" in val:
                purged_keys.append(key)
                continue
            # Purge inverted headings for non-German locales
            if lang != "de":
                if re.search(r'^#+\s+Lektion\b', val, flags=re.M):
                    purged_keys.append(key)
                    continue

        if purged_keys:
            for k in purged_keys:
                del tm_data[k]
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(tm_data, f, ensure_ascii=False, indent=2)
            print(f"[{lang}] Purged {len(purged_keys)} contaminated entry/entries from {os.path.basename(filepath)}")
            total_purged += len(purged_keys)
        else:
            print(f"[{lang}] Clean ({len(tm_data)} valid entries)")

    print(f"\nTotal contaminated TM entries purged: {total_purged}")

if __name__ == "__main__":
    clean_tm_caches()

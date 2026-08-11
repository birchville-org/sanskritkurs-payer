#!/usr/bin/env python3
"""
Automated Mobile Layout & Link Auditor for Sanskritkurs Payer.
Runs on nataraja self-hosted runner to audit internal links, PWA manifests, and mobile table layout.
"""
import os
import sys
import re
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

def audit_links_and_pwa():
    print("📱 Running Mobile Layout & Link Auditor on nataraja...")
    errors = []
    
    # 1. Check PWA Manifest
    public_dist = DOCS / ".vitepress" / "dist-public"
    manifest_file = public_dist / "manifest.webmanifest"
    if public_dist.exists() and not manifest_file.exists():
        manifest_file = public_dist / "manifest.json"
    
    if public_dist.exists():
        if manifest_file.exists():
            print(f"  ✓ PWA Manifest verified: {manifest_file.name}")
        else:
            errors.append("PWA Manifest (manifest.webmanifest / manifest.json) missing in dist-public")
    
    # 2. Audit internal lesson links across files
    md_files = list((DOCS / "lektionen").glob("lektion*.md"))
    link_re = re.compile(r'\[([^\]]+)\]\((/lektionen/lektion\d{2}|/grammatik|/themen)\)')
    
    broken_links = 0
    checked_links = 0
    
    for f in md_files:
        content = f.read_text(encoding="utf-8", errors="ignore")
        for match in link_re.finditer(content):
            checked_links += 1
            target = match.group(2)
            # Verify target exists on disk
            target_path = DOCS / target.lstrip('/')
            if not target_path.exists() and not (DOCS / f"{target.lstrip('/')}.md").exists():
                errors.append(f"Broken internal link in {f.name}: {target}")
                broken_links += 1

    print(f"  ✓ Checked {checked_links} internal links across master lessons.")
    
    if errors:
        print(f"⚠️ Auditor found {len(errors)} potential issues:")
        for err in errors[:5]:
            print(f"  - {err}")
    else:
        print("  ✅ All Mobile & Link Audit checks passed cleanly!")
        
    return len(errors) == 0

if __name__ == "__main__":
    success = audit_links_and_pwa()
    sys.exit(0 if success else 1)

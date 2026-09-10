#!/usr/bin/env python3
"""
Autonomous Plausibility & Spot-Check Audit Tool.
Samples representative lesson and exercise files for a given language
and performs deep syntactic and semantic sanity checks.
"""

import sys
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import translation_qa as qa
from translation.config import LANGUAGES, LANG_NAMES

SAMPLE_FILES = [
    "lektionen/lektion08.md",
    "lektionen/lektion40.md",
    "lektionen/lektion56.md",
    "lektionen/uebung04.md",
    "lektionen/uebung18.md",
    "lektionen/uebung55.md"
]

def spot_check_file(filepath: Path, code: str) -> list:
    """Audit a single file for common failure patterns. Returns list of error strings."""
    if not filepath.exists():
        return [f"File does not exist: {filepath.name}"]

    txt = filepath.read_text(encoding="utf-8", errors="ignore")
    errors = []

    # 1. Check QA fallback status directly
    is_fb, reason = qa.is_file_fallback(filepath, code)
    if is_fb:
        errors.append(f"QA Fallback: {reason}")

    # 2. Check frontmatter category
    m_cat = re.search(r'^category:\s*["\']?(.*?)["\']?\s*$', txt, re.MULTILINE)
    if m_cat:
        cat_val = m_cat.group(1).strip()
        if cat_val == "Übung" and code != "de":
            errors.append("Untranslated frontmatter: category is 'Übung'")

    # 3. Check untranslated German headers
    if code != "de":
        if re.search(r'^#\s+Übung\s+\d+', txt, re.MULTILINE):
            errors.append("Untranslated heading: '# Übung N'")
        if re.search(r'^#\s+Lektion\s+\d+', txt, re.MULTILINE) and code not in ["nl", "af", "no", "da", "sv"]:
            errors.append("Untranslated heading: '# Lektion N'")

    # 4. Check untranslated image captions
    if code != "de":
        if re.search(r'\bAbb\.:', txt):
            errors.append("German image prefix 'Abb.:' detected")
        if re.search(r'\(Bildquelle:', txt):
            errors.append("German source prefix '(Bildquelle:' detected")

    return errors

def audit_language(code: str) -> dict:
    """Run spot checks across sample files for language."""
    qa.verify_qa_integrity()
    lang_dir = ROOT / "docs" / code
    results = {}
    for rel_path in SAMPLE_FILES:
        target_f = lang_dir / rel_path
        errs = spot_check_file(target_f, code)
        results[rel_path] = errs
    return results

def main():
    args = sys.argv[1:]
    target_langs = args if args else ["no", "pl", "cs", "am"]

    print("==================================================")
    print("🔍 AUTONOMOUS SPOT-CHECK AUDIT")
    print("==================================================")
    qa.verify_qa_integrity()
    print("✓ QA Integrity Gate: Operational (Lingua active)")
    print("--------------------------------------------------")

    for code in target_langs:
        lang_name = LANG_NAMES.get(code, code)
        print(f"\n[{code.upper()}] {lang_name}:")
        results = audit_language(code)
        has_issues = False
        for fpath, errs in results.items():
            fname = Path(fpath).name
            if errs:
                has_issues = True
                print(f"  ❌ {fname:20s}: {', '.join(errs)}")
            else:
                print(f"  ✓  {fname:20s}: Clean")
        if not has_issues:
            print(f"  🎉 All {len(SAMPLE_FILES)} spot-checked files completely clean.")

if __name__ == "__main__":
    main()

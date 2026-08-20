#!/usr/bin/env python3
import os
import argparse
import sys
from pathlib import Path

# Add current dir to path to allow imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from translation_qa import (
    get_translation_queue, 
    check_has_de_phrases, 
    clean_markdown_for_lid,
    COMMON_DE_WORDS,
    get_lingua_detector,
    is_sanskrit_iast,
    STRICT_DE_GRAMMAR_KEYWORDS,
    GERMAN_KEYWORDS,
    LATIN_GRAMMAR_TERMS,
    DE_FALLBACK_ALLOWED
)
import re

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"

def isolate_hard_chunks(lang):
    queue = get_translation_queue(lang)
    if not queue:
        print(f"No pending/fallback files found for {lang}.")
        return

    print(f"Analyzing {len(queue)} files in queue for language {lang}...")
    found_issues = 0

    for filename, reason in queue:
        if "Contains" not in reason and "TODO" not in reason and "Exact" not in reason:
            continue
            
        file_path = DOCS / lang / filename
        if not file_path.exists():
            file_path = DOCS / lang / "lektionen" / filename
        if not file_path.exists():
            continue

        txt = file_path.read_text(encoding="utf-8", errors="ignore")
        clean_txt = clean_markdown_for_lid(txt)
        
        strict_keywords = STRICT_DE_GRAMMAR_KEYWORDS
        gen_keywords = GERMAN_KEYWORDS
        if lang != "de":
            latin_terms = LATIN_GRAMMAR_TERMS
            strict_keywords = [kw for kw in strict_keywords if kw not in latin_terms]
            gen_keywords = [kw for kw in gen_keywords if kw not in latin_terms]

        raw_paras = [p.strip() for p in clean_txt.split("\n\n") if len(p.strip()) >= 40]
        detector = get_lingua_detector(lang)
        
        for idx, raw_p in enumerate(raw_paras):
            issue_found = None
            
            # 1. Keyword check
            for kw in strict_keywords:
                if re.search(r'\b' + re.escape(kw) + r'\b', raw_p, re.IGNORECASE):
                    issue_found = f"Strict German keyword: '{kw}'"
                    break
                    
            if not issue_found and lang not in DE_FALLBACK_ALLOWED:
                for kw in gen_keywords:
                    if re.search(r'\b' + re.escape(kw) + r'\b', raw_p, re.IGNORECASE):
                        issue_found = f"German keyword: '{kw}'"
                        break
                        
            # 2. Lingua check
            if not issue_found and detector:
                p = re.sub(r'^[#|\s:-]+', '', raw_p, flags=re.M)
                p = re.sub(r':br', ' ', p).strip()
                if len(p) >= 40 and not is_sanskrit_iast(p) and not raw_p.startswith("```") and not raw_p.startswith("---") and not raw_p.startswith("#"):
                    skip_script = False
                    if lang in ['ru', 'uk', 'bg'] and any('\u0400' <= c <= '\u04FF' for c in p): skip_script = True
                    elif lang in ['ar', 'fa'] and any('\u0600' <= c <= '\u06FF' for c in p): skip_script = True
                    elif lang == 'he' and any('\u0590' <= c <= '\u05FF' for c in p): skip_script = True
                    elif lang in ['el', 'grc'] and any('\u0370' <= c <= '\u03FF' for c in p): skip_script = True
                    elif lang == 'th' and any('\u0E00' <= c <= '\u0E7F' for c in p): skip_script = True
                    elif lang == 'ta' and any('\u0B80' <= c <= '\u0BFF' for c in p): skip_script = True
                    elif lang == 'pa' and any('\u0A00' <= c <= '\u0A7F' for c in p): skip_script = True
                    elif lang in ['zh', 'zh-CN'] and any('\u4E00' <= c <= '\u9FFF' for c in p): skip_script = True
                    elif lang == 'am' and any('\u1200' <= c <= '\u137F' for c in p): skip_script = True
                    
                    if not skip_script:
                        words = set(re.findall(r'\b[a-zäöüß]+\b', p.lower()))
                        de_hits = words.intersection(COMMON_DE_WORDS)
                        if len(de_hits) >= 2:
                            try:
                                from lingua import Language
                                lang_detected = detector.detect_language_of(p)
                                if lang_detected == Language.GERMAN and lang not in DE_FALLBACK_ALLOWED:
                                    if not any(cit in p for cit in ["Dümmler", "Berlin", "Kielhorn", "Solomons", "Monier-Williams", "Stenzler", "Image source:", "Fig.:"]):
                                        issue_found = f"Lingua detected German (Stop words: {de_hits})"
                                elif lang_detected == Language.ENGLISH and lang in DE_FALLBACK_ALLOWED and lang != "en":
                                    issue_found = f"Lingua detected English"
                            except Exception:
                                pass
                                
            if issue_found:
                found_issues += 1
                print(f"\n[{filename}] - Issue: {issue_found}")
                print("-" * 50)
                print(raw_p)
                print("-" * 50)
                
    print(f"\nTotal problematic chunks found: {found_issues}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Isolate hard chunks that fail QA")
    parser.add_argument("--lang", type=str, required=True, help="Target language code (e.g. zh-CN)")
    args = parser.parse_args()
    isolate_hard_chunks(args.lang)

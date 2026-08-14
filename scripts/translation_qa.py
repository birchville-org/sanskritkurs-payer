#!/usr/bin/env python3
"""
Shared Translation QA and Fallback Detection Module for Payer Sanskritkurs.
Single Source of Truth for fallback checking, German remnant detection, and language status reporting.
"""

import os
import re
import difflib
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
TOTAL_MASTER = 136

from translation.terms import (
    DE_FALLBACK_ALLOWED, EXCLUDE_META, GERMAN_KEYWORDS, STRICT_DE_GRAMMAR_KEYWORDS
)

# Lazy Lingua Detector Initialization
_LINGUA_DETECTOR = None

def get_lingua_detector():
    global _LINGUA_DETECTOR
    if _LINGUA_DETECTOR is None:
        try:
            from lingua import Language, LanguageDetectorBuilder
            _LINGUA_DETECTOR = LanguageDetectorBuilder.from_all_languages().with_low_accuracy_mode().build()
        except Exception:
            _LINGUA_DETECTOR = False
    return _LINGUA_DETECTOR if _LINGUA_DETECTOR else None

def is_excluded_file(file_path):
    """Check if a file should be excluded from lesson counts (meta files, test files)."""
    name = Path(file_path).name
    if name in EXCLUDE_META or "qa_viewer" in name or "deleteme" in str(file_path):
        return True
    if name.startswith("test") or name.endswith("-test.md"):
        return True
    return False

def clean_markdown_for_lid(txt):
    """Clean markdown formatting, frontmatter, and metadata before language detection."""
    # Strip YAML frontmatter & deleteme-box metadata blocks
    txt_no_yaml = re.sub(r'^---.*?---\n', '', txt, flags=re.DOTALL)
    txt_no_meta = re.sub(r':::\s*deleteme-box\b.*', '', txt_no_yaml, flags=re.DOTALL)
    clean_txt = re.sub(r'[\u0900-\u097F]+', '', txt_no_meta)  # Remove Devanagari
    clean_txt = re.sub(r'⟪.*?⟫', '', clean_txt)              # Remove Sanskrit brackets
    clean_txt = re.sub(r'!\[.*?\]\(.*?\)', '', clean_txt)     # Remove images
    clean_txt = re.sub(r'\[.*?\]\(.*?\)', '', clean_txt)      # Remove links
    clean_txt = re.sub(r':::[^\n]+', '', clean_txt)           # Remove container tags
    return clean_txt



def check_has_de_phrases(txt, code, fast=False):
    """Check if text contains unallowed German (or English) phrases/remnants."""
    if code == "de":
        return False

    clean_txt = clean_markdown_for_lid(txt)

    # 1. Strict German grammar & table keyword detection
    strict_keywords = STRICT_DE_GRAMMAR_KEYWORDS
    gen_keywords = GERMAN_KEYWORDS
    if code == "en":
        # International Latin terms used in English grammar are valid, not German remnants
        latin_terms = {"Nominativ", "Akkusativ", "Genetiv", "Instrumentalis", "Vokativ", "Ablativ", "Passiv", "Infinitiv"}
        strict_keywords = [kw for kw in strict_keywords if kw not in latin_terms]
        gen_keywords = [kw for kw in gen_keywords if kw not in latin_terms]

    if sum(1 for kw in strict_keywords if kw in clean_txt) >= 1:
        return True

    # 2. General German keyword detection (for non-DE fallback languages)
    if code not in DE_FALLBACK_ALLOWED and code != "en":
        if sum(1 for kw in gen_keywords if kw in clean_txt) >= 1:
            return True

    if fast:
        return False

    # 3. Lingua Statistical Language Detection
    detector = get_lingua_detector()
    if detector:
        from lingua import Language
        raw_paras = [p.strip() for p in clean_txt.split("\n\n") if len(p.strip()) > 20]
        unallowed_paras = 0
        for raw_p in raw_paras:
            if raw_p.startswith("```") or raw_p.startswith("---"):
                continue
            p = re.sub(r'^[#|\s:-]+', '', raw_p, flags=re.M)
            p = re.sub(r':br', ' ', p).strip()
            if len(p) < 20:
                continue
            if code == "en" and len(p) < 45:
                continue
            try:
                lang_detected = detector.detect_language_of(p)
                if lang_detected == Language.GERMAN and code not in DE_FALLBACK_ALLOWED:
                    # Ignore German publisher/city names, image captions, and proper names in English citations
                    if code == "en" and any(cit in p for cit in ["Dümmler", "Berlin", "Kielhorn", "Solomons", "Monier-Williams", "Stenzler", "Image source:", "Fig.:", "Udaipur", "Naran"]):
                        continue
                    unallowed_paras += 1
                    if unallowed_paras >= 1:
                        return True
                elif lang_detected == Language.ENGLISH and code in DE_FALLBACK_ALLOWED and code != "en":
                    unallowed_paras += 1
                    if unallowed_paras >= 1:
                        return True
            except Exception:
                pass

    return False

def is_file_fallback(filepath, code):
    """
    Authoritative check whether a file is considered a fallback or incomplete.
    Returns: (is_fallback: bool, reason: str)
    """
    if code == "de":
        return False, ""

    filepath = Path(filepath)
    if not filepath.exists():
        return True, "File does not exist"

    txt = filepath.read_text(encoding="utf-8", errors="ignore")

    # 1. Tag Check
    if "TODO: Fallback translation" in txt:
        return True, "Contains TODO: Fallback translation tag"

    # 2. German Master Exact Copy Check (compare cleaned text to ignore identical Sanskrit/IAST/markup)
    de_file = DOCS / "lektionen" / filepath.name
    if not de_file.exists():
        de_file = DOCS / filepath.name

    if de_file.exists():
        de_txt = de_file.read_text(encoding="utf-8", errors="ignore")
        c_de = clean_markdown_for_lid(de_txt)
        c_txt = clean_markdown_for_lid(txt)
        if len(c_de.strip()) > 30:
            ratio = difflib.SequenceMatcher(None, c_de, c_txt).ratio()
            if ratio > 0.80:
                return True, f"Exact/near-exact copy of German master file ({int(ratio*100)}% match)"

    # 3. German Phrase & Lingua LID Check
    if check_has_de_phrases(txt, code):
        return True, "Contains unallowed German/English phrases or remnants"

    return False, ""

def tag_file_for_retranslation(filepath, code):
    """
    Scans a file for German remnant blocks and appends '<!-- TODO: Fallback translation -->' 
    to blocks containing German remnants, so lan_translate.py will re-translate them.
    Returns: True if file was modified, False otherwise.
    """
    if code == "de" or code in DE_FALLBACK_ALLOWED:
        return False

    filepath = Path(filepath)
    if not filepath.exists():
        return False

    txt = filepath.read_text(encoding="utf-8", errors="ignore")
    blocks = txt.split("\n\n")
    modified = False
    new_blocks = []

    detector = get_lingua_detector()

    for block in blocks:
        if "<!-- TODO: Fallback translation -->" in block:
            new_blocks.append(block)
            continue

        clean_b = clean_markdown_for_lid(block)
        has_kw = any(kw in clean_b for kw in GERMAN_KEYWORDS)
        has_lingua_de = False

        if not has_kw and detector and len(clean_b.split()) >= 3:
            try:
                from lingua import Language
                if detector.detect_language_of(clean_b) == Language.GERMAN:
                    has_lingua_de = True
            except Exception:
                pass

        if has_kw or has_lingua_de:
            block = block.strip() + " <!-- TODO: Fallback translation -->"
            modified = True

        new_blocks.append(block)

    if modified:
        filepath.write_text("\n\n".join(new_blocks), encoding="utf-8")

    return modified

def get_language_status(code):
    """
    Calculate full status metrics for a language code.
    Returns dict with keys: code, total_files, sauber, fallbacks, pct, unfinished_files
    """
    if code == "de":
        return {"code": "de", "total_files": TOTAL_MASTER, "sauber": TOTAL_MASTER, "fallbacks": 0, "pct": 100.0, "unfinished_files": []}

    lang_dir = DOCS / code
    if not lang_dir.exists():
        return {"code": code, "total_files": 0, "sauber": 0, "fallbacks": TOTAL_MASTER, "pct": 0.0, "unfinished_files": []}

    all_md = list(lang_dir.glob("**/*.md"))
    files = [f for f in all_md if not is_excluded_file(f)]

    fallbacks = 0
    unfinished_files = []

    for f in files:
        is_fb, reason = is_file_fallback(f, code)
        if is_fb:
            fallbacks += 1
            unfinished_files.append((f.name, reason))

    sauber = max(0, TOTAL_MASTER - fallbacks)
    pct = round((sauber / TOTAL_MASTER) * 100.0, 1)

    return {
        "code": code,
        "total_files": len(files),
        "sauber": sauber,
        "fallbacks": fallbacks,
        "pct": pct,
        "unfinished_files": unfinished_files
    }

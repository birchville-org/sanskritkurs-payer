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
from translation.config import TOTAL_MASTER

from translation.terms import (
    DE_FALLBACK_ALLOWED, EXCLUDE_META, GERMAN_KEYWORDS, STRICT_DE_GRAMMAR_KEYWORDS, LATIN_GRAMMAR_TERMS, LATIN_TOLERANT_LANGS
)

_PAIR_DETECTORS = {}

LINGUA_LANG_MAP = {
    'en': 'ENGLISH', 'fr': 'FRENCH', 'es': 'SPANISH', 'it': 'ITALIAN',
    'pt': 'PORTUGUESE', 'nl': 'DUTCH', 'ro': 'ROMANIAN', 'hu': 'HUNGARIAN',
    'fi': 'FINNISH', 'tr': 'TURKISH', 'bg': 'BULGARIAN', 'ru': 'RUSSIAN',
    'uk': 'UKRAINIAN', 'el': 'GREEK', 'hi': 'HINDI', 'pa': 'PUNJABI',
    'ta': 'TAMIL', 'th': 'THAI', 'vi': 'VIETNAMESE', 'id': 'INDONESIAN',
    'ar': 'ARABIC', 'fa': 'PERSIAN', 'he': 'HEBREW', 'zh': 'CHINESE',
    'zh-CN': 'CHINESE', 'la': 'LATIN', 'af': 'AFRIKAANS', 'lt': 'LITHUANIAN',
    'sh': 'SERBIAN', 'sq': 'ALBANIAN', 'zu': 'ZULU',
    'no': 'BOKMAL', 'da': 'DANISH', 'sv': 'SWEDISH', 'is': 'ICELANDIC',
    'pl': 'POLISH', 'cs': 'CZECH', 'sk': 'SLOVAK', 'sl': 'SLOVENE',
    'ka': 'GEORGIAN', 'hy': 'ARMENIAN', 'te': 'TELUGU', 'et': 'ESTONIAN'
}

def get_lingua_detector(target_lang=None):
    global _PAIR_DETECTORS
    if target_lang in _PAIR_DETECTORS:
        return _PAIR_DETECTORS[target_lang]
    try:
        from lingua import Language, LanguageDetectorBuilder
        tgt_attr = LINGUA_LANG_MAP.get(target_lang)
        if target_lang == 'sh':
            det = LanguageDetectorBuilder.from_languages(Language.GERMAN, Language.CROATIAN, Language.SERBIAN, Language.ENGLISH).build()
        elif tgt_attr and hasattr(Language, tgt_attr) and getattr(Language, tgt_attr) != Language.GERMAN:
            langs = [Language.GERMAN, getattr(Language, tgt_attr)]
            if target_lang not in DE_FALLBACK_ALLOWED and target_lang != 'en':
                langs.append(Language.ENGLISH)
            det = LanguageDetectorBuilder.from_languages(*langs).build()
        else:
            det = LanguageDetectorBuilder.from_all_languages().build()
        _PAIR_DETECTORS[target_lang] = det
        return det
    except Exception as e:
        import sys
        sys.stderr.write(f"[CRITICAL QA ERROR] Lingua detector failed to initialize: {e}\n")
        return None

def is_excluded_file(file_path):
    """Check if a file should be excluded from lesson counts (meta files, test files)."""
    name = Path(file_path).name
    if name in EXCLUDE_META or "qa_viewer" in name or "deleteme" in str(file_path):
        return True
    if name.startswith("test") or name.endswith("-test.md"):
        return True
    return False

COMMON_DE_WORDS = {
    "der", "die", "das", "und", "oder", "nicht", "ist", "sind", "wird", "werden",
    "wurde", "wurden", "mit", "von", "auf", "für", "bei", "nach", "über", "durch",
    "aus", "im", "dem", "den", "des", "eine", "einer", "eines", "einem", "einen",
    "wenn", "aber", "als", "auch", "wie", "sie", "er", "wir", "ihr", "alle", "dies",
    "ohne", "unter", "vor", "zwischen"
}

def clean_markdown_for_lid(txt):
    """Clean markdown formatting, frontmatter, and metadata before language detection."""
    # Extract prose YAML frontmatter string values to scan them
    yaml_match = re.match(r'^---\n(.*?)\n---\n', txt, flags=re.DOTALL)
    yaml_vals = []
    if yaml_match:
        yaml_content = yaml_match.group(1)
        for line in yaml_content.splitlines():
            m = re.search(r'^([a-zA-Z0-9_-]+):\s*["\']?(.*?)["\']?\s*$', line)
            if m:
                key, val = m.group(1).lower(), m.group(2).strip()
                if key in ('category', 'uebung_id', 'lesson_id', 'status', 'last_reconstructed', 'next', 'prev'):
                    continue
                if val and not val.isdigit() and not re.match(r'^\d{4}-\d{2}-\d{2}$', val) and val.lower() not in ('true', 'false', 'stable'):
                    yaml_vals.append(val)
                
    # Strip YAML frontmatter & deleteme-box metadata blocks
    txt_no_yaml = re.sub(r'^---.*?---\n', '', txt, flags=re.DOTALL)
    if yaml_vals:
        txt_no_yaml = "\n\n".join(yaml_vals) + "\n\n" + txt_no_yaml
        
    txt_no_meta = re.sub(r':::\s*deleteme-box\b.*', '', txt_no_yaml, flags=re.DOTALL)
    clean_txt = re.sub(r'^>+\s*', '', txt_no_meta, flags=re.MULTILINE)
    clean_txt = re.sub(r'[\u0900-\u097F]+', '', clean_txt)     # Remove Devanagari
    clean_txt = re.sub(r'⟪.*?⟫', '', clean_txt)              # Remove Sanskrit brackets
    clean_txt = re.sub(r'!\[.*?\]\(.*?\)', '', clean_txt)     # Remove images
    clean_txt = re.sub(r'\[.*?\]\(.*?\)', '', clean_txt)      # Remove links
    clean_txt = re.sub(r':::[^\n]+', '', clean_txt)           # Remove container tags
    return clean_txt

def is_sanskrit_iast(text):
    """Check if text contains IAST characters or verse delimiters |"""
    iast_chars = set("āīūṛṝḷḹṅñṇṭḍśṣṃḥĀĪŪṚṜḶḸṄÑṆṬḌŚṢṂḤ")
    iast_count = sum(1 for c in text if c in iast_chars)
    if '|' in text or '||' in text:
        return True
    if len(text) > 0 and (iast_count / len(text)) > 0.04:
        return True
    return False

def check_has_de_phrases(txt, code, fast=False):
    """Check if text contains unallowed German (or English) phrases/remnants."""
    if code == "de":
        return False

    # Check for untranslated German top headings like '# Übung N'
    if re.search(r'^#\s+Übung\s+\d+', txt, re.MULTILINE):
        return True

    clean_txt = clean_markdown_for_lid(txt)

    # 1. Strict German grammar & table keyword detection
    strict_keywords = STRICT_DE_GRAMMAR_KEYWORDS
    gen_keywords = GERMAN_KEYWORDS
    if code != "de" and code in LATIN_TOLERANT_LANGS:
        latin_terms = LATIN_GRAMMAR_TERMS
        strict_keywords = [kw for kw in strict_keywords if kw not in latin_terms]
        gen_keywords = [kw for kw in gen_keywords if kw not in latin_terms]

    # Keyword check using word-boundary matching
    for kw in strict_keywords:
        if re.search(r'(?<!\w)' + re.escape(kw) + r'(?!\w)', clean_txt, re.IGNORECASE):
            return True

    # 2. General German keyword detection (for non-DE fallback languages)
    if code not in DE_FALLBACK_ALLOWED:
        for kw in gen_keywords:
            if re.search(r'(?<!\w)' + re.escape(kw) + r'(?!\w)', clean_txt, re.IGNORECASE):
                return True

    if fast:
        return False

    # 2.5 YAML Frontmatter Subtitle & Description Check
    detector = get_lingua_detector(code)
    if detector and code not in DE_FALLBACK_ALLOWED:
        from lingua import Language
        yaml_m = re.match(r'^---\n(.*?)\n---\n', txt, flags=re.DOTALL)
        if yaml_m:
            for y_line in yaml_m.group(1).splitlines():
                km = re.search(r'^(subtitle|description):\s*["\']?(.*?)["\']?\s*$', y_line, re.IGNORECASE)
                if km:
                    y_val = km.group(2).strip()
                    y_clean = re.sub(r'[\u0900-\u097F]+', '', y_val)
                    y_clean = re.sub(r'⟪.*?⟫', '', y_clean).strip()
                    if len(y_clean) >= 20 and not is_sanskrit_iast(y_clean):
                        try:
                            if detector.detect_language_of(y_clean) == Language.GERMAN:
                                return True
                        except Exception:
                            pass

    # 3. Lingua Statistical Language Detection (High accuracy pairwise, min length >= 40, no headings, no Sanskrit)
    if detector:
        from lingua import Language
        raw_paras = [p.strip() for p in clean_txt.split("\n\n") if len(p.strip()) >= 40]
        for raw_p in raw_paras:
            if raw_p.startswith("```") or raw_p.startswith("---") or raw_p.startswith("#"):
                continue
            p = re.sub(r'^[#|\s:-]+', '', raw_p, flags=re.M)
            p = re.sub(r':br', ' ', p).strip()
            if len(p) < 40:
                continue
            if is_sanskrit_iast(p):
                continue
            # Skip paragraphs that contain target non-Latin scripts
            if code in ['ru', 'uk', 'bg'] and any('\u0400' <= c <= '\u04FF' for c in p):
                continue
            if code in ['ar', 'fa'] and any('\u0600' <= c <= '\u06FF' for c in p):
                continue
            if code == 'he' and any('\u0590' <= c <= '\u05FF' for c in p):
                continue
            if code in ['el', 'grc'] and any('\u0370' <= c <= '\u03FF' for c in p):
                continue
            if code == 'th' and any('\u0E00' <= c <= '\u0E7F' for c in p):
                continue
            if code == 'ta' and any('\u0B80' <= c <= '\u0BFF' for c in p):
                continue
            if code == 'pa' and any('\u0A00' <= c <= '\u0A7F' for c in p):
                continue
            if code in ['zh', 'zh-CN'] and any('\u4E00' <= c <= '\u9FFF' for c in p):
                continue
            if code in ['am', 'gez'] and any('\u1200' <= c <= '\u137F' for c in p):
                continue
            if code == 'si' and any('\u0D80' <= c <= '\u0DFF' for c in p):
                continue
            if code == 'ka' and any('\u10A0' <= c <= '\u10FF' for c in p):
                continue
            if code == 'hy' and any('\u0530' <= c <= '\u058F' for c in p):
                continue
            if code == 'te' and any('\u0C00' <= c <= '\u0C7F' for c in p):
                continue

            # Require at least 1 distinct German common stop word
            words = set(re.findall(r'\b[a-zäöüß]+\b', p.lower()))
            de_hits = words.intersection(COMMON_DE_WORDS)
            if len(de_hits) >= 1:
                try:
                    lang_detected = detector.detect_language_of(p)
                    if lang_detected == Language.GERMAN and code not in DE_FALLBACK_ALLOWED:
                        if any(cit in p for cit in ["Dümmler", "Berlin", "Kielhorn", "Solomons", "Monier-Williams", "Stenzler", "Image source:", "Fig.:", "Lüders", "Alsdorf", "Weber, Max", "Tübingen", "Tüpfli", "Bussmann", "Payer, Alois", "Hoffmann, Karl"]):
                            continue
                        return True
                    elif lang_detected == Language.ENGLISH and code in DE_FALLBACK_ALLOWED and code not in ["en", "rm"]:
                        return True
                except Exception:
                    pass

    return False

def verify_qa_integrity():
    """
    Self-verifying smoke test / plausibility gate.
    Asserts that the detector is active and catches synthetic German text.
    Fails closed if the detector is broken or silently disabled.
    """
    test_de_text = "Dies ist ein deutscher Beispielsatz zum Einritzen in Palmblätter, der zweifelsfrei erkannt werden muss."
    for test_lang in ['en', 'no', 'pl', 'zh']:
        if not check_has_de_phrases(test_de_text, test_lang):
            raise RuntimeError(
                f"[CRITICAL QA INTEGRITY FAILURE] German remnant detector is NOT operational for '{test_lang}'! "
                f"Lingua language detector must be installed and functioning."
            )
    return True

# Auto-execute integrity self-check on import (fail-closed security)
verify_qa_integrity()

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

    # 2. German Master Exact Copy Check
    de_file = DOCS / "lektionen" / filepath.name
    if not de_file.exists():
        de_file = DOCS / filepath.name

    if de_file.exists():
        de_txt = de_file.read_text(encoding="utf-8", errors="ignore")
        txt_body = re.sub(r'^---\n.*?\n---\n', '', txt, flags=re.DOTALL).strip()
        de_body = re.sub(r'^---\n.*?\n---\n', '', de_txt, flags=re.DOTALL).strip()
        if txt_body == de_body and len(txt_body) > 0:
            return True, "Exact copy of German master file"

    # 3. German Phrase & Lingua LID Check
    if check_has_de_phrases(txt, code):
        return True, "Contains unallowed German/English phrases or remnants"

    # 4. Unresolved Translation Placeholders Check
    if re.search(r'(?:⟨|&lang;)?(?:DEVA|IAST_L|STRUCT)_[0-9\u0966-\u096F\u0660-\u0669N]+(?:⟩|&rang;)?', txt):
        return True, "Contains unresolved translation placeholders"

    return False, ""

def get_translation_queue_files(code):
    """Canonical list of (src, tgt) file pairs (136 master files) for a language."""
    if code == "de":
        return []
    lang_dir = DOCS / code
    pairs = []
    # 1. Main pages
    for p in ['index.md', 'grammatik.md', 'themen.md', 'impressum.md', 'settings.md']:
        pairs.append((DOCS / p, lang_dir / p))
    # 2. Lessons 01-61
    for i in range(1, 62):
        pairs.append((DOCS / f'lektionen/lektion{i:02d}.md', lang_dir / f'lektionen/lektion{i:02d}.md'))
    # 3. Scripts 01-11
    for i in range(1, 12):
        pairs.append((DOCS / f'lektionen/schrift{i:02d}.md', lang_dir / f'lektionen/schrift{i:02d}.md'))
    # 4. Exercises 01-61
    for i in range(1, 62):
        pairs.append((DOCS / f'lektionen/uebung{i:02d}.md', lang_dir / f'lektionen/uebung{i:02d}.md'))
    # 5. Wortlisten
    for p in ['lektionen/wortliste.md', 'lektionen/inhaltsverzeichnis.md']:
        pairs.append((DOCS / p, lang_dir / p))
    return pairs

def get_translation_queue(code):
    """
    Canonical Single Source of Truth for translation queue.
    A file is in queue if:
      1. Missing target file
      2. Target is older than source (mtime < src_mtime)
      3. is_file_fallback(tgt, code) returns True
    """
    if code == "de":
        return []
    pairs = get_translation_queue_files(code)
    todo = []
    
    hashes = get_stored_hashes()
    lang_hashes = hashes.get(code, {})
    
    for src, tgt in pairs:
        if not src.exists():
            continue
        if not tgt.exists():
            todo.append((tgt.name, "Fehlt (neu)"))
            continue
        if tgt.stat().st_mtime < src.stat().st_mtime:
            current_src_hash = get_file_hash(src)
            stored_src_hash = lang_hashes.get(tgt.name)
            if stored_src_hash and current_src_hash == stored_src_hash:
                pass # Source content hasn't changed despite newer mtime
            else:
                todo.append((tgt.name, "Veraltet"))
                continue
        is_fb, reason = is_file_fallback(tgt, code)
        if is_fb:
            todo.append((tgt.name, reason))
    return todo

def tag_file_for_retranslation(filepath, code):
    """
    Deprecated: QA tools are strictly read-only.
    Returns: False (no file modifications).
    """
    return False

def get_language_status(code):
    """
    Calculate full status metrics for a language code using canonical get_translation_queue.
    Returns dict with keys: code, total_files, sauber, fallbacks, pct, unfinished_files
    """
    if code == "de":
        return {"code": "de", "total_files": TOTAL_MASTER, "sauber": TOTAL_MASTER, "fallbacks": 0, "pct": 100.0, "unfinished_files": []}

    queue = get_translation_queue(code)
    fallbacks = len(queue)
    sauber = max(0, TOTAL_MASTER - fallbacks)
    pct = round((sauber / TOTAL_MASTER) * 100.0, 1)

    return {
        "code": code,
        "total_files": TOTAL_MASTER,
        "sauber": sauber,
        "fallbacks": fallbacks,
        "pct": pct,
        "unfinished_files": queue
    }


def is_language_completed(lang):
    """
    Returns True if the language is 100% complete (0 items in translation queue).
    """
    if lang == "de":
        return True
    return len(get_translation_queue(lang)) == 0

import hashlib
import json

def get_file_hash(filepath):
    hasher = hashlib.md5()
    with open(filepath, 'rb') as f:
        buf = f.read()
        hasher.update(buf)
    return hasher.hexdigest()

def get_stored_hashes():
    hash_file = ROOT / "docs" / ".payer" / "master_hashes.json"
    if not hash_file.exists():
        return {}
    try:
        with open(hash_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def save_stored_hashes(data):
    hash_file = ROOT / "docs" / ".payer" / "master_hashes.json"
    hash_file.parent.mkdir(parents=True, exist_ok=True)
    with open(hash_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

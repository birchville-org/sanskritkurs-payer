#!/usr/bin/env python3
"""
gen_wortliste.py

Generates wortliste.md for each language by extracting vocabulary sections
from already-translated lektion files. No LLM needed.

Usage:
  python3 scripts/gen_wortliste.py              # all languages
  python3 scripts/gen_wortliste.py en fr        # specific languages
  python3 scripts/gen_wortliste.py --dry-run    # preview only
"""

import re
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"

LANG_CONFIG = {
    "": {
        "section_keywords": ["Wortliste"],
        "lektion_heading": "Lektion",
        "title": "Wortliste (Gesamtübersicht)",
        "subtitle": "*Alle neuen Wörter aus dem Kurs in der Reihenfolge ihrer Einführung, mit thematischen Erläuterungen.*",
        "frontmatter": "---\noutline: 2\n---\n",
    },
    "en": {
        "section_keywords": ["Word List", "Word list", "Vocabulary"],
        "lektion_heading": "Lesson",
        "title": "Word List (Complete Overview)",
        "subtitle": "*All new words from the course in the order of their introduction, with thematic explanations.*",
        "frontmatter": "---\noutline: 2\n---\n",
    },
    "fr": {
        "section_keywords": ["Liste de mots", "Liste des mots", "Vocabulaire"],
        "lektion_heading": "Leçon",
        "title": "Liste de mots (vue d'ensemble complète)",
        "subtitle": "*Tous les nouveaux mots du cours dans l'ordre de leur introduction, avec des explications thématiques.*",
        "frontmatter": "---\noutline: 2\n---\n",
    },
    "it": {
        "section_keywords": ["Elenco di parole", "Elenco delle parole", "Elenco lessicale", "Vocabolario", "Lista di parole"],
        "lektion_heading": "Lezione",
        "title": "Elenco di parole (panoramica completa)",
        "subtitle": "*Tutte le nuove parole del corso nell'ordine della loro introduzione, con spiegazioni tematiche.*",
        "frontmatter": "---\noutline: 2\n---\n",
    },
    "es": {
        "section_keywords": ["Lista de palabras", "Vocabulario", "Lista de palabras"],
        "lektion_heading": "Lección",
        "title": "Lista de palabras (vista general completa)",
        "subtitle": "*Todas las palabras nuevas del curso en el orden de su introducción, con explicaciones temáticas.*",
        "frontmatter": "---\noutline: 2\n---\n",
    },
    "ru": {
        "section_keywords": ["Список слов", "Словарь"],
        "lektion_heading": "Урок",
        "title": "Список слов (полный обзор)",
        "subtitle": "*Все новые слова курса в порядке их введения, с тематическими пояснениями.*",
        "frontmatter": "---\noutline: 2\n---\n",
    },
    "uk": {
        "section_keywords": ["Список слів", "Словник"],
        "lektion_heading": "Урок",
        "title": "Список слів (повний огляд)",
        "subtitle": "*Усі нові слова курсу в порядку їх введення з тематичними поясненнями.*",
        "frontmatter": "---\noutline: 2\n---\n",
    },
    "bg": {
        "section_keywords": ["Речник", "Списък с думи"],
        "lektion_heading": "Урок",
        "title": "Речник (пълен преглед)",
        "subtitle": "*Всички нови думи от курса в реда на въвеждането им, с тематични обяснения.*",
        "frontmatter": "---\noutline: 2\n---\n",
    },
    "hi": {
        "section_keywords": ["शब्दावली", "शब्द सूची"],
        "lektion_heading": "पाठ",
        "title": "शब्दावली (संपूर्ण सारांश)",
        "subtitle": "*पाठ्यक्रम के सभी नए शब्द उनके परिचय के क्रम में, विषयगत व्याख्याओं के साथ।*",
        "frontmatter": "---\noutline: 2\n---\n",
    },
    "ta": {
        "section_keywords": ["சொற்பட்டியல்", "சொல் பட்டியல்", "Wortliste"],
        "lektion_heading": "பாடம்",
        "title": "சொற்பட்டியல் (முழுமையான கண்ணோட்டம்)",
        "subtitle": "*பாடநெறியின் அனைத்து புதிய சொற்களும் அவை அறிமுகப்படுத்தப்பட்ட வரிசையில், கருப்பொருள் விளக்கங்களுடன்.*",
        "frontmatter": "---\noutline: 2\n---\n",
    },
    "pa": {
        "section_keywords": ["ਸ਼ਬਦ ਸੂਚੀ", "ਸ਼ਬਦਾਵਲੀ", "Wortliste"],
        "lektion_heading": "ਪਾਠ",
        "title": "ਸ਼ਬਦ ਸੂਚੀ (ਸੰਪੂਰਨ ਸੰਖੇਪ)",
        "subtitle": "*ਕੋਰਸ ਦੇ ਸਾਰੇ ਨਵੇਂ ਸ਼ਬਦ ਉਹਨਾਂ ਦੀ ਜਾਣਕਾਰੀ ਦੇ ਕ੍ਰਮ ਵਿੱਚ, ਵਿਸ਼ੇਸ਼ ਵਿਆਖਿਆਵਾਂ ਸਮੇਤ।*",
        "frontmatter": "---\noutline: 2\n---\n",
    },
}

ACTIVE_LANGS = ["en", "fr", "it", "es", "ru", "uk", "bg", "hi", "ta", "pa"]


def extract_wortliste_sections(lektion_path: Path, keywords: list[str]) -> list[str]:
    """
    Extract all Wortliste sections from a lektion file.
    Returns list of content strings (without the section heading).
    """
    text = lektion_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    # Build regex matching any keyword variant (with optional number suffix)
    kw_pattern = "|".join(re.escape(k) for k in keywords)
    section_re = re.compile(
        r"^## \d+\.\d+\.\s+(?:" + kw_pattern + r")(?:\s+\d+)?\s*$",
        re.IGNORECASE,
    )
    next_section_re = re.compile(r"^## ")

    sections = []
    i = 0
    while i < len(lines):
        if section_re.match(lines[i].strip()):
            # Collect until next ## heading
            content_lines = []
            i += 1
            while i < len(lines) and not next_section_re.match(lines[i]):
                content_lines.append(lines[i])
                i += 1
            # Strip leading/trailing blank lines
            while content_lines and not content_lines[0].strip():
                content_lines.pop(0)
            while content_lines and not content_lines[-1].strip():
                content_lines.pop()
            if content_lines:
                sections.append("".join(content_lines))
        else:
            i += 1

    return sections


def get_lektion_num(path: Path) -> int:
    m = re.search(r"lektion(\d+)", path.name)
    return int(m.group(1)) if m else 0


def generate_wortliste(lang: str, dry_run: bool = False) -> bool:
    cfg = LANG_CONFIG.get(lang)
    if not cfg:
        print(f"[{lang}] Keine Konfiguration gefunden.")
        return False

    ldir = DOCS_DIR / lang / "lektionen" if lang else DOCS_DIR / "lektionen"
    if not ldir.is_dir():
        print(f"[{lang or 'de'}] Verzeichnis nicht gefunden: {ldir}")
        return False

    lektionen = sorted(ldir.glob("lektion*.md"), key=get_lektion_num)
    if not lektionen:
        print(f"[{lang or 'de'}] Keine Lektionen gefunden.")
        return False

    sections_found = 0
    body_parts = []

    for lek_path in lektionen:
        num = get_lektion_num(lek_path)
        sections = extract_wortliste_sections(lek_path, cfg["section_keywords"])
        if not sections:
            continue
        sections_found += 1
        body_parts.append(f"## {cfg['lektion_heading']} {num}\n\n")
        body_parts.append("\n\n".join(sections))
        body_parts.append("\n\n")

    if not sections_found:
        print(f"[{lang or 'de'}] Keine Wortliste-Sektionen gefunden (Keywords: {cfg['section_keywords']}).")
        return False

    content = (
        cfg["frontmatter"]
        + "\n"
        + f"# {cfg['title']}\n\n"
        + cfg["subtitle"]
        + "\n\n\n"
        + "".join(body_parts).rstrip()
        + "\n"
    )

    out_path = ldir / "wortliste.md"
    label = lang or "de"

    if dry_run:
        print(f"[{label}] DRY-RUN: würde {out_path} schreiben ({sections_found} Lektionen, {len(content)} Zeichen)")
    else:
        out_path.write_text(content, encoding="utf-8")
        print(f"[{label}] ✅ {out_path.relative_to(DOCS_DIR)} ({sections_found} Lektionen, {len(content)} Zeichen)")

    return True


def main() -> None:
    args = sys.argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]

    if dry_run:
        print("DRY RUN — keine Dateien werden geschrieben\n")

    langs = args if args else ACTIVE_LANGS

    for lang in langs:
        generate_wortliste(lang, dry_run=dry_run)


if __name__ == "__main__":
    main()

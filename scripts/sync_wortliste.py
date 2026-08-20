#!/usr/bin/env python3
"""
sync_wortliste.py — Sync wortliste sections from individual lektion files
to the global docs/lektionen/wortliste.md (or a language-specific variant).

For German (default): extracts "## N.X. Wortliste" sections from docs/lektionen/.
For other languages (--lang LANG): extracts the same section NUMBER from the
translated lektionen and builds/updates docs/LANG/lektionen/wortliste.md.
The wortliste heading and "Lektion" label are taken from the translated file,
so no AI translation is needed.

Usage:
  python3 scripts/sync_wortliste.py all             # DE, all lektionen
  python3 scripts/sync_wortliste.py 52              # DE, lektion 52 only
  python3 scripts/sync_wortliste.py --lang ta all   # TA, all lektionen
  python3 scripts/sync_wortliste.py --lang pa all   # PA, all lektionen
  python3 scripts/sync_wortliste.py --lang es 6 12  # ES, specific lektionen
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
DE_DIR = ROOT / "docs" / "lektionen"
DE_WORTLISTE = DE_DIR / "wortliste.md"

# Localised labels for the wortliste page header
LANG_LABELS = {
    "de": {
        "title": "Wortliste (Gesamtübersicht)",
        "subtitle": "Alle neuen Wörter aus dem Kurs in der Reihenfolge ihrer Einführung, mit thematischen Erläuterungen.",
        "lektion_prefix": "Lektion",
    },
    "es": {
        "title": "Lista de palabras (visión general)",
        "subtitle": "Todas las palabras nuevas del curso en el orden de su introducción, con explicaciones temáticas.",
        "lektion_prefix": "Lección",
    },
    "it": {
        "title": "Lista delle parole (panoramica)",
        "subtitle": "Tutte le nuove parole del corso nell'ordine della loro introduzione, con spiegazioni tematiche.",
        "lektion_prefix": "Lezione",
    },
    "ta": {
        "title": "சொற்பட்டியல் (ஒட்டுமொத்த கண்ணோட்டம்)",
        "subtitle": "பாடத்தில் புதிதாக அறிமுகப்படுத்தப்பட்ட அனைத்து சொற்களும், கருப்பொருள் விளக்கங்களுடன்.",
        "lektion_prefix": "பாடம்",
    },
    "pa": {
        "title": "ਸ਼ਬਦ-ਸੂਚੀ (ਸੰਖੇਪ ਜਾਣਕਾਰੀ)",
        "subtitle": "ਕੋਰਸ ਵਿੱਚ ਉਹਨਾਂ ਦੀ ਜਾਣ-ਪਛਾਣ ਦੇ ਕ੍ਰਮ ਵਿੱਚ ਸਾਰੇ ਨਵੇਂ ਸ਼ਬਦ, ਵਿਸ਼ੇ ਸੰਬੰਧੀ ਵਿਆਖਿਆਵਾਂ ਦੇ ਨਾਲ।",
        "lektion_prefix": "ਪਾਠ",
    },
    "en": {
        "title": "Word List (complete overview)",
        "subtitle": "All new words from the course in the order of their introduction, with thematic explanations.",
        "lektion_prefix": "Lesson",
    },
    "fr": {
        "title": "Liste des mots (vue d'ensemble)",
        "subtitle": "Tous les nouveaux mots du cours dans l'ordre de leur introduction, avec des explications thématiques.",
        "lektion_prefix": "Leçon",
    },
    "hi": {
        "title": "शब्द-सूची (संपूर्ण सिंहावलोकन)",
        "subtitle": "पाठ्यक्रम के सभी नए शब्द उनके परिचय के क्रम में, विषयगत स्पष्टीकरणों के साथ।",
        "lektion_prefix": "पाठ",
    },
    "bg": {
        "title": "Речник (пълен преглед)",
        "subtitle": "Всички нови думи от курса в реда на въвеждането им, с тематични обяснения.",
        "lektion_prefix": "Урок",
    },
    "ru": {
        "title": "Список слов (полный обзор)",
        "subtitle": "Все новые слова курса в порядке их введения, с тематическими пояснениями.",
        "lektion_prefix": "Лекция",
    },
    "uk": {
        "title": "Список слів (повний огляд)",
        "subtitle": "Усі нові слова курсу в порядку їх введення, з тематичними поясненнями.",
        "lektion_prefix": "Лекція",
    },
    "la": {
        "title": "Index verborum (conspectus totus)",
        "subtitle": "Omnia verba nova cursus ordine quo introducta sunt, cum explicationibus thematicis.",
        "lektion_prefix": "Lectio",
    },
    "rm": {
        "title": "Glista da pleds (survista completta)",
        "subtitle": "Tut ils pleds novs dal curs en l'urden da lur introducziun, cun explicaziuns tematicas.",
        "lektion_prefix": "Lecziun",
    },
    "ro": {
        "title": "Lista de cuvinte (prezentare generală)",
        "subtitle": "Toate cuvintele noi din curs în ordinea introducerii lor, cu explicații tematice.",
        "lektion_prefix": "Lecție",
    },
}


def find_wortliste_section_number(de_path: Path) -> str | None:
    """Return the section number of the Wortliste section in the German file,
    e.g. '2.5' for '## 2.5. Wortliste'. Returns None if no wortliste."""
    text = de_path.read_text(encoding="utf-8")
    m = re.search(r'^## (\d+(?:\.\d+)*)\. Wortliste[ \t]*\n', text, re.MULTILINE)
    return m.group(1) if m else None


def extract_section_by_number(path: Path, section_num: str) -> tuple[str, str] | None:
    """Extract section heading line and body from a file by section number.
    Returns (heading_line, body) or None if not found."""
    text = path.read_text(encoding="utf-8")
    m = re.search(rf'^## {re.escape(section_num)}\. .+\n', text, re.MULTILINE)
    if not m:
        return None
    heading = m.group(0).rstrip()
    start = m.end()
    next_m = re.search(r'^## ', text[start:], re.MULTILINE)
    end = start + next_m.start() if next_m else len(text)
    body = text[start:end].rstrip()
    return heading, body


def build_wortliste_md(lang: str, lektion_nums: list[int]) -> str:
    """Build a complete wortliste.md content for the given language."""
    labels = LANG_LABELS.get(lang, LANG_LABELS["de"])
    lang_dir = ROOT / "docs" / lang / "lektionen"
    lines = [
        "---",
        "outline: 2",
        "---",
        "",
        "::: deleteme-box",
        "**Zitierweise & Rechte**",
        "",
        ":::",
        "",
        f"# {labels['title']}",
        "",
        f"*{labels['subtitle']}*",
        "",
        "",
    ]
    for n in lektion_nums:
        de_path = DE_DIR / f"lektion{n:02d}.md"
        if not de_path.exists():
            continue
        sec_num = find_wortliste_section_number(de_path)
        if not sec_num:
            continue  # Lektion has no wortliste (e.g. lektion01)
        lang_path = lang_dir / f"lektion{n:02d}.md"
        if not lang_path.exists():
            print(f"  L{n:02d}: {lang} file not found, skipping")
            continue
        result = extract_section_by_number(lang_path, sec_num)
        if not result:
            print(f"  L{n:02d}: section {sec_num} not found in {lang} file, skipping")
            continue
        _, body = result
        lines.append(f"## {labels['lektion_prefix']} {n}")
        lines.append("")
        if body:
            lines.append(body)
        lines.append("")
        lines.append("")
        print(f"  L{n:02d}: ok")
    return "\n".join(lines)


def sync_wortliste_de(lektion_nums: list[int]) -> None:
    """Original German sync: update existing wortliste.md in-place."""
    wortliste_text = DE_WORTLISTE.read_text(encoding="utf-8")
    changed = 0
    for n in lektion_nums:
        path = DE_DIR / f"lektion{n:02d}.md"
        if not path.exists():
            print(f"  L{n:02d}: file not found, skipping")
            continue
        result = find_wortliste_section_number(path)
        if not result:
            print(f"  L{n:02d}: no wortliste section, skipping")
            continue
        text = path.read_text(encoding="utf-8")
        m = re.search(rf'^## {re.escape(result)}\. Wortliste[ \t]*\n', text, re.MULTILINE)
        start = m.end()
        next_m = re.search(r'^## ', text[start:], re.MULTILINE)
        end = start + next_m.start() if next_m else len(text)
        new_content = text[start:end].rstrip()

        m2 = re.search(rf'^## Lektion {n}\s*\n', wortliste_text, re.MULTILINE)
        if not m2:
            print(f"  L{n:02d}: '## Lektion {n}' not found in wortliste.md, skipping")
            continue
        body_start = m2.end()
        next_m2 = re.search(r'^(?:## |::: deleteme-box|::: literatur)', wortliste_text[body_start:], re.MULTILINE)
        body_end = body_start + next_m2.start() if next_m2 else len(wortliste_text)
        old_body = wortliste_text[body_start:body_end]
        new_body = "\n" + new_content + "\n\n"
        if old_body == new_body:
            print(f"  L{n:02d}: up to date")
        else:
            wortliste_text = wortliste_text[:body_start] + new_body + wortliste_text[body_end:]
            print(f"  L{n:02d}: updated")
            changed += 1
    DE_WORTLISTE.write_text(wortliste_text, encoding="utf-8")
    print(f"\nDone. {changed} section(s) updated.")


def main() -> None:
    args = sys.argv[1:]
    lang = "de"

    # Parse --lang flag
    if "--lang" in args:
        idx = args.index("--lang")
        if idx + 1 >= len(args):
            print("Error: --lang requires a language code (e.g. --lang ta)")
            sys.exit(1)
        lang = args[idx + 1]
        args = args[:idx] + args[idx + 2:]

    if not args:
        print("Usage: python3 scripts/sync_wortliste.py [--lang LANG] <all|lesson_num [...]>")
        print("Examples:")
        print("  python3 scripts/sync_wortliste.py all")
        print("  python3 scripts/sync_wortliste.py --lang ta all")
        print("  python3 scripts/sync_wortliste.py --lang pa all")
        sys.exit(1)

    nums = list(range(1, 62)) if args[0] == "all" else [int(a) for a in args if a.isdigit()]

    if lang == "de":
        sync_wortliste_de(nums)
    else:
        if lang not in LANG_LABELS:
            print(f"Warning: no labels defined for lang '{lang}', using German fallback")
        out_path = ROOT / "docs" / lang / "lektionen" / "wortliste.md"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        print(f"Building {out_path} from {len(nums)} lektionen...")
        content = build_wortliste_md(lang, nums)
        out_path.write_text(content, encoding="utf-8")
        print(f"\nWritten: {out_path}")


if __name__ == "__main__":
    main()

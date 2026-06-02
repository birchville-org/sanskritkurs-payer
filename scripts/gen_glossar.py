#!/usr/bin/env python3
"""
gen_glossar.py — Alphabetisches Glossar aus den Wortlisten-Abschnitten generieren.

Liest die bereits übersetzten Lektionsdateien einer Sprache, extrahiert die
Wortlisten-Abschnitte und erstellt ein nach Schriftzeichen sortiertes Glossar.
Kein KI-Aufruf nötig — rein aus dem vorhandenen Material zusammengestellt.

Usage:
  python3 scripts/gen_glossar.py             # Deutsch (root)
  python3 scripts/gen_glossar.py --lang es   # Spanisch
  python3 scripts/gen_glossar.py --lang ta   # Tamil
  python3 scripts/gen_glossar.py --lang all  # Alle konfigurierten Sprachen
"""

import re, sys, unicodedata
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent

# ── Devanāgarī → IAST Konvertierung ─────────────────────────────────────────
try:
    from indic_transliteration import sanscript as _san
    def deva_to_iast(text: str) -> str:
        """Extrahiere führende Devanāgarī-Sequenz und konvertiere zu IAST."""
        # Nur den ersten zusammenhängenden Devanāgarī-Block nehmen
        m = re.match(r'^([ऀ-ॿ]+)', text.strip())
        if not m:
            return ""
        deva_clean = m.group(1)
        try:
            return _san.transliterate(deva_clean, _san.DEVANAGARI, _san.IAST)
        except Exception:
            return ""
except ImportError:
    def deva_to_iast(text: str) -> str:
        return ""

# ── Sprachkonfiguration ──────────────────────────────────────────────────────
LANG_CONFIG = {
    "de": {
        "dir": "docs/lektionen",
        "glossar_path": "docs/lektionen/glossar.md",
        "title": "Glossar Sanskrit–Deutsch",
        "subtitle": "Zusammengestellt aus den Wortlisten des Sanskrit-Kurses von Alois Payer.  \n© Simone Dünneisen (FS 2011), Lektionen 1–46. Ergänzt um Lektionen 47–61.",
        "col_sanskrit": "Sanskrit", "col_iast": "IAST", "col_genus": "Genus",
        "col_meaning": "Deutsch", "col_lektion": "Lektion",
        "link_prefix": "/lektionen/lektion",
    },
    "en": {
        "dir": "docs/en/lektionen",
        "glossar_path": "docs/en/lektionen/glossar.md",
        "title": "Glossary Sanskrit–English",
        "subtitle": "Compiled from the word lists of Alois Payer's Sanskrit course.",
        "col_sanskrit": "Sanskrit", "col_iast": "IAST", "col_genus": "Genus",
        "col_meaning": "English", "col_lektion": "Lesson",
        "link_prefix": "/en/lektionen/lektion",
    },
    "it": {
        "dir": "docs/it/lektionen",
        "glossar_path": "docs/it/lektionen/glossar.md",
        "title": "Glossario Sanscrito–Italiano",
        "subtitle": "Compilato dalle liste di parole del corso di sanscrito di Alois Payer.",
        "col_sanskrit": "Sanscrito", "col_iast": "IAST", "col_genus": "Genere",
        "col_meaning": "Italiano", "col_lektion": "Lezione",
        "link_prefix": "/it/lektionen/lektion",
    },
    "es": {
        "dir": "docs/es/lektionen",
        "glossar_path": "docs/es/lektionen/glossar.md",
        "title": "Glosario Sánscrito–Español",
        "subtitle": "Compilado a partir de las listas de palabras del curso de sánscrito de Alois Payer.",
        "col_sanskrit": "Sánscrito", "col_iast": "IAST", "col_genus": "Género",
        "col_meaning": "Español", "col_lektion": "Lección",
        "link_prefix": "/es/lektionen/lektion",
    },
    "fr": {
        "dir": "docs/fr/lektionen",
        "glossar_path": "docs/fr/lektionen/glossar.md",
        "title": "Glossaire Sanskrit–Français",
        "subtitle": "Compilé à partir des listes de mots du cours de sanskrit d'Alois Payer.",
        "col_sanskrit": "Sanskrit", "col_iast": "IAST", "col_genus": "Genre",
        "col_meaning": "Français", "col_lektion": "Leçon",
        "link_prefix": "/fr/lektionen/lektion",
    },
    "hi": {
        "dir": "docs/hi/lektionen",
        "glossar_path": "docs/hi/lektionen/glossar.md",
        "title": "शब्दकोश संस्कृत–हिंदी",
        "subtitle": "आलोइस पायर के संस्कृत पाठ्यक्रम की शब्द-सूचियों से संकलित।",
        "col_sanskrit": "संस्कृत", "col_iast": "IAST", "col_genus": "लिंग",
        "col_meaning": "हिंदी", "col_lektion": "पाठ",
        "link_prefix": "/hi/lektionen/lektion",
    },
    "bg": {
        "dir": "docs/bg/lektionen",
        "glossar_path": "docs/bg/lektionen/glossar.md",
        "title": "Речник Санскрит–Български",
        "subtitle": "Съставено от речниковите списъци на курса по санскрит на Алоис Пайер.",
        "col_sanskrit": "Санскрит", "col_iast": "IAST", "col_genus": "Род",
        "col_meaning": "Български", "col_lektion": "Урок",
        "link_prefix": "/bg/lektionen/lektion",
    },
    "ru": {
        "dir": "docs/ru/lektionen",
        "glossar_path": "docs/ru/lektionen/glossar.md",
        "title": "Глоссарий Санскрит–Русский",
        "subtitle": "Составлено по спискам слов курса санскрита Алоиса Пайера.",
        "col_sanskrit": "Санскрит", "col_iast": "IAST", "col_genus": "Род",
        "col_meaning": "Русский", "col_lektion": "Лекция",
        "link_prefix": "/ru/lektionen/lektion",
    },
    "uk": {
        "dir": "docs/uk/lektionen",
        "glossar_path": "docs/uk/lektionen/glossar.md",
        "title": "Глосарій Санскрит–Українська",
        "subtitle": "Складено зі списків слів курсу санскриту Алоїса Пайєра.",
        "col_sanskrit": "Санскрит", "col_iast": "IAST", "col_genus": "Рід",
        "col_meaning": "Українська", "col_lektion": "Лекція",
        "link_prefix": "/uk/lektionen/lektion",
    },
    "ta": {
        "dir": "docs/ta/lektionen",
        "glossar_path": "docs/ta/lektionen/glossar.md",
        "title": "சொற்களஞ்சியம் சமஸ்கிருதம்–தமிழ்",
        "subtitle": "ஆலோயிஸ் பயர் அவர்களின் சமஸ்கிருத பாடத்திட்டத்தின் சொற்பட்டியல்களிலிருந்து தொகுக்கப்பட்டது.",
        "col_sanskrit": "சமஸ்கிருதம்", "col_iast": "IAST", "col_genus": "பால்",
        "col_meaning": "தமிழ்", "col_lektion": "பாடம்",
        "link_prefix": "/ta/lektionen/lektion",
    },
    "pa": {
        "dir": "docs/pa/lektionen",
        "glossar_path": "docs/pa/lektionen/glossar.md",
        "title": "ਸ਼ਬਦਕੋਸ਼ ਸੰਸਕ੍ਰਿਤ–ਪੰਜਾਬੀ",
        "subtitle": "ਅਲੋਇਸ ਪਾਏਰ ਦੇ ਸੰਸਕ੍ਰਿਤ ਕੋਰਸ ਦੀਆਂ ਸ਼ਬਦ-ਸੂਚੀਆਂ ਤੋਂ ਸੰਕਲਿਤ।",
        "col_sanskrit": "ਸੰਸਕ੍ਰਿਤ", "col_iast": "IAST", "col_genus": "ਲਿੰਗ",
        "col_meaning": "ਪੰਜਾਬੀ", "col_lektion": "ਪਾਠ",
        "link_prefix": "/pa/lektionen/lektion",
    },
}

DEV = r'[ऀ-ॿ]'


def get_wortliste_anchor(lang_dir: Path, lektion_num: int) -> str:
    """VitePress-Anker des Wortliste-Abschnitts ermitteln."""
    path = lang_dir / f"lektion{lektion_num:02d}.md"
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    # Suche nach irgendwelchem Wortliste-ähnlichem Abschnitt (mehrsprachig)
    m = re.search(
        r"^## (\d+(?:\.\d+)*)\.\s+\S+",
        text,
        re.MULTILINE,
    )
    # Finde den letzten ## Abschnitt vor der Übung
    headings = re.findall(r"^## (\d+(?:\.\d+)*)\..*$", text, re.MULTILINE)
    if len(headings) >= 2:
        # Vorletzter Abschnitt = typischerweise Wortliste
        sec = headings[-2].replace(".", "-")
        return f"#_{sec}-" + re.sub(r"^## \d+(?:\.\d+)*\.\s+", "", [h for h in text.split("\n") if h.startswith(f"## {headings[-2]}.")][0]).strip().lower().replace(" ", "-").replace("/", "-")[:30] if sec[0].isdigit() else f"#{sec}-wortliste"
    return ""


def _make_anchor(lektion_num: int, lang_dir: Path) -> str:
    """Vereinfachter Anker: Sektionsnummer des vorletzten ## Abschnitts."""
    path = lang_dir / f"lektion{lektion_num:02d}.md"
    if not path.exists():
        return ""
    text = path.read_text(encoding="utf-8")
    headings = re.findall(r"^## (\d+(?:\.\d+)*)\..*$", text, re.MULTILINE)
    if len(headings) >= 2:
        sec = headings[-2].replace(".", "-")
        prefix = "_" if sec[0].isdigit() else ""
        # Heading text für anchor
        for line in text.split("\n"):
            m = re.match(rf"^## {re.escape(headings[-2])}\.\s+(.+)", line)
            if m:
                slug = m.group(1).lower().strip()
                slug = re.sub(r"[^a-z0-9-￿\s-]", "", slug)
                slug = re.sub(r"\s+", "-", slug)[:40]
                return f"#{prefix}{sec}-{slug}"
    return ""


def parse_entries(lang_dir: Path, de_dir: Path) -> list:
    """Extrahiert Wortliste-Einträge aus allen Lektionsdateien."""
    entries = []
    seen = set()

    for n in range(1, 62):
        lang_path = lang_dir / f"lektion{n:02d}.md"
        de_path = de_dir / f"lektion{n:02d}.md"
        if not lang_path.exists():
            continue

        # Wortliste-Abschnitt ermitteln (via deutsche Quelldatei für zuverlässige Sektionsnummer)
        wl_sec = None
        if de_path.exists():
            de_text = de_path.read_text(encoding="utf-8")
            m = re.search(r"^## (\d+(?:\.\d+)*)\. Wortliste", de_text, re.MULTILINE)
            if m:
                wl_sec = m.group(1)

        if not wl_sec:
            continue

        lang_text = lang_path.read_text(encoding="utf-8")
        # Wortliste-Abschnitt in der Zielsprache finden
        sec_m = re.search(rf"^## {re.escape(wl_sec)}\.\s+.+\n", lang_text, re.MULTILINE)
        if not sec_m:
            continue

        start = sec_m.end()
        next_m = re.search(r"^## ", lang_text[start:], re.MULTILINE)
        section_text = lang_text[start: start + next_m.start() if next_m else len(lang_text)]

        # Anker berechnen
        heading_line = sec_m.group(0).strip()
        heading_slug = re.sub(r"^## \d+(?:\.\d+)*\.\s+", "", heading_line).lower()
        heading_slug = re.sub(r"[^a-z0-9-￿\s-]", "", heading_slug)
        heading_slug = re.sub(r"\s+", "-", heading_slug.strip())[:40]
        sec_anchor = wl_sec.replace(".", "-")
        anchor = f"#_{sec_anchor}-{heading_slug}" if wl_sec[0].isdigit() else f"#{sec_anchor}-{heading_slug}"

        # Einträge parsen — Format A: **iast** genus -- देव : Bedeutung
        for line in section_text.split("\n"):
            ma = re.match(
                r"^[-\s]*\*\*([^*]+)\*\*\s*([^ऀ-ॿ:=\n]*?)\s*(?:--|=)?\s*([ऀ-ॿ]+(?:\s[ऀ-ॿ]+)*)\s*[=:]\s*(.+)",
                line,
            )
            if ma:
                iast = ma.group(1).strip()
                genus = ma.group(2).strip().rstrip(".,")
                deva = ma.group(3).strip()
                bed = ma.group(4).strip().rstrip(".")
                if re.search(DEV, deva) and len(deva) >= 2:
                    key = (deva, n)
                    if key not in seen:
                        seen.add(key)
                        # IAST aus dem Eintrag übernehmen oder algorithmisch erzeugen
                        iast_final = iast if iast else deva_to_iast(deva)
                        entries.append({
                            "iast": iast_final, "deva": deva, "genus": genus,
                            "bedeutung": bed, "lektion": n, "anchor": anchor,
                        })
                continue
            # Format B: देव genus : Bedeutung
            mb = re.match(
                r"^[-\s]*([ऀ-ॿ][ऀ-ॿ\s]*?)\s*(m\b|f\b|n\b|mfn\b|3\b|Adv\b|Adj\b|PP\b)[.,]?\s*:?\s*(.{3,})",
                line,
            )
            if mb:
                deva = mb.group(1).strip()
                genus = mb.group(2).strip()
                bed = mb.group(3).strip().rstrip(".")
                if re.search(DEV, deva) and len(deva) >= 2:
                    key = (deva, n)
                    if key not in seen:
                        seen.add(key)
                        entries.append({
                            "iast": deva_to_iast(deva), "deva": deva, "genus": genus,
                            "bedeutung": bed, "lektion": n, "anchor": anchor,
                        })
    return entries


def first_char(deva: str) -> str:
    for ch in deva:
        cp = ord(ch)
        if 0x0900 <= cp <= 0x0939:
            return ch
    return deva[0]


def generate(lang: str) -> None:
    cfg = LANG_CONFIG[lang]
    lang_dir = ROOT / cfg["dir"]
    de_dir = ROOT / "docs/lektionen"
    out_path = ROOT / cfg["glossar_path"]

    if not lang_dir.exists():
        print(f"  {lang}: Verzeichnis {lang_dir} nicht vorhanden — übersprungen")
        return

    entries = parse_entries(lang_dir, de_dir)
    if not entries:
        print(f"  {lang}: Keine Einträge gefunden — übersprungen")
        return

    entries.sort(key=lambda e: unicodedata.normalize("NFC", e["deva"]))
    groups: dict = defaultdict(list)
    for e in entries:
        groups[first_char(e["deva"])].append(e)

    c = cfg
    lines = [
        "---", "outline: 2", "---", "",
        "::: deleteme-box", "**Quelle & Urheberrecht**", "", ":::", "",
        f"# {c['title']}", "",
        f"*{c['subtitle']}*", "", "---", "",
    ]

    for group_char, group_entries in sorted(groups.items(), key=lambda x: unicodedata.normalize("NFC", x[0])):
        lines.append(f"## {group_char}")
        lines.append("")
        lines.append(f"| {c['col_sanskrit']} | {c['col_iast']} | {c['col_genus']} | {c['col_meaning']} | {c['col_lektion']} |")
        lines.append("|---|---|---|---|---|")
        for e in group_entries:
            iast = e["iast"] or "—"
            genus = e["genus"] or "—"
            bed = e["bedeutung"].replace("|", "/").replace("\n", " ")[:120]
            lekt_link = f"[{e['lektion']}]({c['link_prefix']}{e['lektion']:02d}{e['anchor']})"
            lines.append(f"| {e['deva']} | {iast} | {genus} | {bed} | {lekt_link} |")
        lines.append("")

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text("\n".join(lines), encoding="utf-8")
    lektionen = sorted(set(e["lektion"] for e in entries))
    print(f"  {lang}: {len(entries)} Einträge, {len(groups)} Gruppen, L{lektionen[0]}–L{lektionen[-1]} → {out_path}")


def main() -> None:
    args = sys.argv[1:]
    lang = "de"
    if "--lang" in args:
        idx = args.index("--lang")
        if idx + 1 < len(args):
            lang = args[idx + 1]

    if lang == "all":
        print("Generiere Glossar für alle Sprachen...")
        for l in LANG_CONFIG:
            generate(l)
    elif lang in LANG_CONFIG:
        generate(lang)
    else:
        print(f"Unbekannte Sprache: '{lang}'. Verfügbar: {', '.join(LANG_CONFIG)}")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
pre_push_check.py — Qualitätsprüfung vor git push

Zwei Scope-Modi:
  --scope=diff  (Standard) Nur Dateien die seit origin/main geändert wurden
  --scope=all   Alle Markdown-Dateien im Projekt

Checks:
  GLOBAL  (immer):    YAML-Frontmatter, Build-Gate
  SCOPED  (auf diff): Zero-HTML, Platzhalter, Fremdzeichen in falschen Sprachen,
                       Bildunterschriften-Format, Lizenzen-Vollständigkeit

Gibt Exit-Code 0 bei Erfolg, 1 bei Fehlern zurück.

Usage:
  python3 scripts/pre_push_check.py              # scope=diff, kein build
  python3 scripts/pre_push_check.py --build      # inkl. npm run docs:build
  python3 scripts/pre_push_check.py --scope=all  # alle Files
  python3 scripts/pre_push_check.py --fix        # reparierbare Fehler automatisch fixen
"""

import os, re, sys, subprocess, unicodedata
from pathlib import Path

ROOT = Path(__file__).parent.parent

# ── Konfiguration ─────────────────────────────────────────────────────────────

# Sprachen mit lateinischer Schrift → Kyrillisch wäre Fehler
LATIN_LANGS  = {'en', 'it', 'es', 'fr', 'la', 'rm', 'ro', 'de'}
# Sprachen mit kyrillischer Schrift
CYRILLIC_LANGS = {'bg', 'ru', 'uk'}
# Sprachen mit Indic-Schrift
INDIC_LANGS  = {'hi', 'ta', 'pa'}

# Sprach-Präfix → erwartete Schriftsysteme
LANG_SCRIPTS = {
    **{l: 'latin'    for l in LATIN_LANGS},
    **{l: 'cyrillic' for l in CYRILLIC_LANGS},
    **{l: 'indic'    for l in INDIC_LANGS},
}

# Platzhalter die auf fehlgeschlagene Übersetzung hinweisen
PLACEHOLDER_PATTERNS = [
    r'DEVA_\d+',          # Devanāgarī-Platzhalter aus lan_translate.py
    r'\bTODO\b',
    r'\bPLACEHOLDER\b',
    r'⟨DEVA_\d+⟩',
]

# HTML-Tags die in Markdown nicht erlaubt sind (Zero-HTML Policy)
HTML_TAG_RE = re.compile(
    r'<(?!(?:br\s*/?>|!--|/!--|img\s|/img|a\s|/a|strong|/strong|span|/span|'
    r'code|/code|em|/em|mark|/mark|sub|/sub|sup|/sup|s>|/s>|del|/del))[a-zA-Z/][^>]*>',
    re.IGNORECASE
)

# ── Hilfsfunktionen ────────────────────────────────────────────────────────────

def get_diff_files():
    """Gibt Liste der seit origin/main geänderten .md-Dateien zurück."""
    try:
        result = subprocess.run(
            ['git', 'diff', '--name-only', '--diff-filter=ACM', 'origin/main..HEAD'],
            capture_output=True, text=True, cwd=ROOT
        )
        files = [ROOT / f for f in result.stdout.strip().split('\n') if f.endswith('.md')]
        return [f for f in files if f.exists()]
    except Exception as e:
        print(f"  ⚠ git diff fehlgeschlagen: {e}")
        return []

def get_all_md_files():
    """Alle .md-Dateien in docs/ ausser docs/lektionen/ (DE ist immutable)."""
    files = []
    for lang_dir in (ROOT / 'docs').iterdir():
        if not lang_dir.is_dir() or lang_dir.name in ('.vitepress', 'public', 'qa', 'lektionen'):
            continue
        for f in lang_dir.rglob('*.md'):
            files.append(f)
    return files

def lang_from_path(path: Path) -> str:
    """Extrahiert Sprachkürzel aus Pfad: docs/ta/lektionen/... → 'ta'"""
    try:
        rel = path.relative_to(ROOT / 'docs')
        parts = rel.parts
        if parts[0] == 'lektionen':
            return 'de'
        return parts[0] if len(parts) > 1 else 'de'
    except ValueError:
        return 'de'

def check_config_files_in_diff():
    """Warnt wenn Config-Dateien im Diff sind → manuelle Review empfohlen."""
    result = subprocess.run(
        ['git', 'diff', '--name-only', 'origin/main..HEAD'],
        capture_output=True, text=True, cwd=ROOT
    )
    config_files = [f for f in result.stdout.strip().split('\n')
                    if any(f.endswith(ext) for ext in ['.mjs', '.css', '.vue', '.ts'])
                    and '.vitepress' in f]
    return config_files

# ── Checks ────────────────────────────────────────────────────────────────────

def check_yaml_frontmatter(files):
    """Prüft ob YAML-Frontmatter korrekt geparst werden kann."""
    errors = []
    for path in files:
        content = path.read_text(encoding='utf-8', errors='replace')
        if not content.startswith('---'):
            continue
        end = content.find('\n---\n', 4)
        if end == -1:
            errors.append((path, 'Frontmatter nicht geschlossen'))
            continue
        fm = content[4:end]
        # Prüfe auf bekannte YAML-Probleme
        for i, line in enumerate(fm.split('\n'), 1):
            # Unquotete Strings die mit " beginnen
            m = re.match(r'^(\w+):\s+"([^"]+)"\s+\S', line)
            if m:
                errors.append((path, f'Zeile {i}: YAML-Wert könnte Parser brechen: {line.strip()[:60]}'))
    return errors

def check_zero_html(files):
    """Prüft auf rohes HTML (Zero-HTML-Policy)."""
    errors = []
    for path in files:
        if 'lektionen' not in str(path):
            continue
        content = path.read_text(encoding='utf-8', errors='replace')
        matches = HTML_TAG_RE.findall(content)
        # Ignoriere HTML in deleteme-box (unsichtbar)
        # Ignoriere &lt; / &gt; Entitäten
        real = [m for m in matches if '&' not in m]
        if real:
            errors.append((path, f'{len(real)} HTML-Tag(s): {real[:3]}'))
    return errors

def check_placeholders(files):
    """Findet nicht-ersetzte Übersetzungs-Platzhalter."""
    errors = []
    combined = re.compile('|'.join(PLACEHOLDER_PATTERNS))
    for path in files:
        content = path.read_text(encoding='utf-8', errors='replace')
        # Ignoriere Code-Spans (`...`) und Code-Blöcke um False Positives zu vermeiden
        stripped = re.sub(r'`[^`]+`', '', content)
        stripped = re.sub(r'```.*?```', '', stripped, flags=re.DOTALL)
        matches = combined.findall(stripped)
        if matches:
            errors.append((path, f'Platzhalter: {list(set(matches))[:5]}'))
    return errors

def check_escaped_vue_components(files):
    """Findet fälschlicherweise HTML-escapte Vue-Komponenten wie &lt;PayerTopicIndex /&gt;."""
    errors = []
    vue_re = re.compile(r'&lt;Payer[A-Za-z]+')
    for path in files:
        content = path.read_text(encoding='utf-8', errors='replace')
        if vue_re.search(content):
            errors.append((path, 'Vue-Komponente HTML-escapt (z.B. &lt;PayerTopicIndex /&gt;)'))
    return errors

def check_foreign_chars(files):
    """Findet Zeichen falscher Schriftsysteme (z.B. Chinesisch in Tamil)."""
    CJK_RE = re.compile(r'[一-鿿㐀-䶿]')
    errors = []
    for path in files:
        lang = lang_from_path(path)
        expected = LANG_SCRIPTS.get(lang, 'latin')
        content = path.read_text(encoding='utf-8', errors='replace')

        # CJK in Nicht-CJK-Sprachen (ausser wenn es legitime Eigennamen sind)
        cjk = CJK_RE.findall(content)
        if cjk and not lang.startswith('zh'):
            # lektion50 und licenses.md haben legitimerweise CJK (Everest, Lisu)
            if 'lektion50' not in str(path) and 'licenses' not in path.name:
                errors.append((path, f'CJK-Zeichen: {"".join(set(cjk))[:10]}'))

        # Kyrillisch in Latin-Sprachen
        if expected == 'latin':
            cyrillic = [c for c in content if 'CYRILLIC' in unicodedata.name(c, '')]
            if cyrillic:
                errors.append((path, f'Kyrillisch in {lang}: {"".join(set(cyrillic))[:10]}'))
    return errors

def check_image_captions(files):
    """Prüft Bildunterschriften-Format: Abb.: Text [[br]] Bildquelle: [Details](...)"""
    errors = []
    # Erlaubte Formate
    good_caption = re.compile(
        r'^Abb\.: .+(\[\[br\]\]|\n).*Bildquelle:',
        re.MULTILINE
    )
    bad_font = re.compile(r'<font[^>]*>', re.IGNORECASE)
    for path in files:
        if 'lektionen' not in str(path):
            continue
        content = path.read_text(encoding='utf-8', errors='replace')
        # Legacy <font> Tags bei Bildunterschriften
        if bad_font.search(content):
            errors.append((path, 'Legacy <font>-Tag in Bildunterschrift'))
    return errors

def check_html_arrow_entities(files, fix=False):
    """Findet -&gt; (HTML-Entity als Pfeil) das → sein sollte, und &gt; als Blockquote-Marker."""
    errors = []
    arrow_re  = re.compile(r'-&gt;')
    bq_re     = re.compile(r'^&gt;', re.MULTILINE)
    # Auch &lt;- (Linkspfeil)
    larrow_re = re.compile(r'&lt;-')
    for path in files:
        content = path.read_text(encoding='utf-8', errors='replace')
        # Code-Spans und Code-Blöcke ausschliessen
        stripped = re.sub(r'```.*?```', '', content, flags=re.DOTALL)
        stripped = re.sub(r'`[^`\n]+`', '', stripped)
        hits = []
        if arrow_re.search(stripped):
            hits.append('-&gt; (sollte → sein)')
        if bq_re.search(stripped):
            hits.append('&gt; am Zeilenbeginn (sollte > sein)')
        if larrow_re.search(stripped):
            hits.append('&lt;- (sollte ← sein)')
        if hits:
            if fix:
                fixed = content
                fixed = arrow_re.sub('→', fixed)
                fixed = bq_re.sub('>', fixed)
                fixed = larrow_re.sub('←', fixed)
                path.write_text(fixed, encoding='utf-8')
                errors.append((path, f'Automatisch repariert: {hits}'))
            else:
                errors.append((path, f'HTML-Entity als Pfeil: {hits}'))
    return errors

def check_licenses(files):
    """Prüft ob alle lektXXYY-Bild-IDs in licenses.md vorhanden sind."""
    errors = []
    licenses_de = (ROOT / 'docs/licenses.md')
    if not licenses_de.exists():
        return [('licenses.md', 'Datei nicht gefunden')]

    licenses_content = licenses_de.read_text(encoding='utf-8', errors='replace')
    id_re = re.compile(r'lekt\d{4}')
    defined_ids = set(id_re.findall(licenses_content))

    for path in files:
        if 'lektionen' not in str(path) or lang_from_path(path) != 'de':
            continue  # Nur DE-Quelldateien prüfen
        content = path.read_text(encoding='utf-8', errors='replace')
        used_ids = set(id_re.findall(content))
        missing = used_ids - defined_ids
        if missing:
            errors.append((path, f'IDs fehlen in licenses.md: {sorted(missing)}'))
    return errors

def check_release_version():
    """Prüft ob die Version aus package.json auf der Startseite (docs/index.md) eingetragen ist."""
    import json
    pkg_path = ROOT / 'package.json'
    idx_path = ROOT / 'docs/index.md'
    if not pkg_path.exists() or not idx_path.exists():
        return None
    try:
        pkg_data = json.loads(pkg_path.read_text('utf-8'))
        version = pkg_data.get('version', '')
        if not version: return None
        
        parts = version.split('.')
        if len(parts) >= 2:
            short_v = f"{parts[0]}.{parts[1]}"
            idx_content = idx_path.read_text('utf-8')
            if f"Version {short_v}" not in idx_content and f"v{short_v}" not in idx_content:
                return f"Version {short_v} fehlt in docs/index.md (Release Notes nicht nachgetragen!)"
    except Exception as e:
        return f"Fehler beim Version-Check: {e}"
    return None

# ── Hauptprogramm ──────────────────────────────────────────────────────────────

def main():
    args = sys.argv[1:]
    scope = 'diff'
    run_build = False
    fix_mode = False

    for a in args:
        if a == '--scope=all':   scope = 'all'
        if a == '--scope=diff':  scope = 'diff'
        if a == '--build':       run_build = True
        if a == '--fix':         fix_mode = True

    print(f"\n{'='*60}")
    print(f"  Pre-Push Check  |  scope={scope}  |  build={'ja' if run_build else 'nein'}")
    print(f"{'='*60}\n")

    total_errors = 0

    # ── 1. Config-Dateien Warnung ────────────────────────────────────────────
    config_files = check_config_files_in_diff()
    if config_files:
        print(f"⚠  Config-Dateien im Diff ({len(config_files)}):")
        for f in config_files:
            print(f"   {f}")
        print("   → Manuelle Sichtprüfung aller Sprachversionen empfohlen\n")

    # ── 2. Dateien ermitteln ─────────────────────────────────────────────────
    if scope == 'diff':
        files = get_diff_files()
        print(f"📋 Scope: {len(files)} geänderte .md-Dateien seit origin/main")
    else:
        files = get_all_md_files()
        print(f"📋 Scope: alle {len(files)} .md-Dateien")

    if not files:
        print("   (keine .md-Dateien im Scope)\n")

    # ── 3. YAML-Frontmatter (alle Files im Scope) ────────────────────────────
    print("\n[1/6] YAML-Frontmatter...")
    errs = check_yaml_frontmatter(files)
    if errs:
        for path, msg in errs:
            print(f"  ❌ {path.relative_to(ROOT)}: {msg}")
        total_errors += len(errs)
    else:
        print(f"  ✓ {len(files)} Dateien geprüft — OK")

    # ── 4. Zero-HTML ─────────────────────────────────────────────────────────
    print("\n[2/6] Zero-HTML (kein rohes HTML in .md)...")
    errs = check_zero_html(files)
    if errs:
        for path, msg in errs:
            print(f"  ❌ {path.relative_to(ROOT)}: {msg}")
        total_errors += len(errs)
    else:
        print(f"  ✓ OK")

    # ── 4b. Escapte Vue-Komponenten ──────────────────────────────────────────
    print("\n[2b] Escapte Vue-Komponenten (&lt;Payer...&gt;)...")
    errs = check_escaped_vue_components(files)
    if errs:
        for path, msg in errs:
            print(f"  ❌ {path.relative_to(ROOT)}: {msg}")
        total_errors += len(errs)
    else:
        print(f"  ✓ OK")

    # ── 4c. HTML-Entities als Pfeile ────────────────────────────────────────
    print("\n[2c] HTML-Entities als Pfeile (-&gt; statt →)...")
    errs = check_html_arrow_entities(files, fix=fix_mode)
    if errs:
        for path, msg in errs:
            icon = '✓' if fix_mode else '❌'
            print(f"  {icon} {path.relative_to(ROOT)}: {msg}")
        if not fix_mode:
            total_errors += len(errs)
    else:
        print(f"  ✓ OK")

    # ── 5. Platzhalter ───────────────────────────────────────────────────────
    print("\n[3/6] Übersetzungs-Platzhalter (DEVA_, TODO, ...)...")
    errs = check_placeholders(files)
    if errs:
        for path, msg in errs:
            print(f"  ❌ {path.relative_to(ROOT)}: {msg}")
        total_errors += len(errs)
    else:
        print(f"  ✓ OK")

    # ── 6. Fremdzeichen ──────────────────────────────────────────────────────
    print("\n[4/6] Fremdzeichen (CJK, Kyrillisch in falschen Sprachen)...")
    errs = check_foreign_chars(files)
    if errs:
        for path, msg in errs:
            print(f"  ❌ {path.relative_to(ROOT)}: {msg}")
        total_errors += len(errs)
    else:
        print(f"  ✓ OK")

    # ── 7. Bildunterschriften ────────────────────────────────────────────────
    print("\n[5/6] Bildunterschriften-Format...")
    errs = check_image_captions(files)
    if errs:
        for path, msg in errs:
            print(f"  ⚠ {path.relative_to(ROOT)}: {msg}")
        # Nur Warning, kein hard error
    else:
        print(f"  ✓ OK")

    # ── 7b. Fehlende licenses.md ────────────────────────────────────────────
    print("\n[5b] Fehlende licenses.md pro Sprache...")
    LANGS = ['en','it','es','fr','hi','bg','ru','uk','ta','pa','la','rm','ro']
    missing_lic = [l for l in LANGS if not (ROOT / 'docs' / l / 'licenses.md').exists()]
    if missing_lic:
        print(f"  ❌ licenses.md fehlt für: {missing_lic}")
        total_errors += len(missing_lic)
    else:
        print(f"  ✓ OK — alle {len(LANGS)} Sprachen haben licenses.md")

    # ── 5c. qa_viewer Dropdown-Vollständigkeit ──────────────────────────────
    print("\n[5c] qa_viewer.html — Dropdown enthält alle Sprachen...")
    qa_viewer = ROOT / 'docs/public/qa_viewer.html'
    if not qa_viewer.exists():
        print("  ⚠ qa_viewer.html nicht gefunden — übersprungen")
    else:
        qa_content = qa_viewer.read_text(encoding='utf-8')
        SKIP_DIRS = {'.vitepress', 'public', 'qa', 'lektionen', 'de', '.zennotes', 'archive', 'quick', 'trash', 'zh-CN', 'zh-TW', 'th'}
        lang_dirs = {d.name for d in (ROOT / 'docs').iterdir()
                     if d.is_dir() and d.name not in SKIP_DIRS}
        # Prüfe ob jede Sprache als option value in QA-Viewer vorhanden ist
        missing_dropdown = []
        for lang in sorted(lang_dirs):
            pattern = f'value="{lang}/lektionen/'
            if pattern not in qa_content:
                missing_dropdown.append(lang)
        if missing_dropdown:
            print(f"  ❌ Sprache(n) fehlen im qa_viewer-Dropdown: {missing_dropdown}")
            print(f"     → Beide <select>-Elemente in docs/public/qa_viewer.html ergänzen")
            total_errors += len(missing_dropdown)
        else:
            print(f"  ✓ OK — alle {len(lang_dirs)} Sprachen im Dropdown")

    # ── 8. Lizenzen (nur bei --scope=all oder wenn DE-Dateien im Diff) ───────
    de_files = [f for f in files if lang_from_path(f) == 'de']
    if de_files or scope == 'all':
        print("\n[6/6] Lizenzen-Vollständigkeit (licenses.md)...")
        errs = check_licenses(files if scope == 'all' else de_files)
        if errs:
            for path, msg in errs:
                print(f"  ⚠ {path if isinstance(path, str) else path.relative_to(ROOT)}: {msg}")
        else:
            print(f"  ✓ OK")
    else:
        print("\n[6/6] Lizenzen — übersprungen (keine DE-Dateien im Diff)")

    # ── 9. Build-Gate ────────────────────────────────────────────────────────
    if run_build:
        print("\n[Build] npm run docs:build...")
        result = subprocess.run(
            ['npm', 'run', 'docs:build'],
            capture_output=True, text=True, cwd=ROOT
        )
        if result.returncode != 0:
            print(f"  ❌ Build FEHLGESCHLAGEN:")
            print(result.stderr[-1000:])
            total_errors += 1
        else:
            print(f"  ✓ Build OK")

    # ── 10. Release-Version in index.md ──────────────────────────────────────
    print("\n[7/7] Release-Version in docs/index.md prüfen...")
    ver_err = check_release_version()
    if ver_err:
        print(f"  ❌ {ver_err}")
        total_errors += 1
    else:
        print(f"  ✓ OK")

    # ── Zusammenfassung ──────────────────────────────────────────────────────
    print(f"\n{'='*60}")
    if total_errors == 0:
        print(f"  ✅ Alle Checks bestanden — bereit zum Push")
    else:
        print(f"  ❌ {total_errors} Fehler gefunden — Push blockiert")
        print(f"     Tipp: python3 scripts/pre_push_check.py --fix  (wo möglich)")
    print(f"{'='*60}\n")

    sys.exit(0 if total_errors == 0 else 1)


if __name__ == '__main__':
    main()

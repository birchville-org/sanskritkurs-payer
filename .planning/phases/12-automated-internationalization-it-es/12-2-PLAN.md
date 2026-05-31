---
phase: 12-automated-internationalization-it-es
plan: 2
type: execute
wave: 2
depends_on:
  - 12-1
files_modified:
  - docs/es/wortliste.md
  - docs/ta/wortliste.md
  - docs/pa/wortliste.md
  - docs/es/licenses.md
  - docs/ta/licenses.md
  - docs/pa/licenses.md
autonomous: true
requirements:
  - I18N-06
  - I18N-09
  - I18N-10
  - I18N-11

must_haves:
  truths:
    - "docs/es/wortliste.md existiert mit spanischen Wortlisten-Einträgen"
    - "docs/ta/wortliste.md existiert mit tamilischen Wortlisten-Einträgen"
    - "docs/pa/wortliste.md existiert mit Punjabi-Wortlisten-Einträgen"
    - "docs/es/licenses.md existiert mit spanischen Überschriften und Phrasen"
    - "docs/ta/licenses.md existiert mit tamilischen Überschriften und Phrasen"
    - "docs/pa/licenses.md existiert mit Punjabi-Überschriften und Phrasen"
  artifacts:
    - path: "docs/es/wortliste.md"
      provides: "Spanische Gesamtwortliste"
    - path: "docs/ta/wortliste.md"
      provides: "Tamilische Gesamtwortliste"
    - path: "docs/pa/wortliste.md"
      provides: "Punjabi-Gesamtwortliste"
    - path: "docs/es/licenses.md"
      provides: "Spanische Lizenz-Seite"
    - path: "docs/ta/licenses.md"
      provides: "Tamilische Lizenz-Seite"
    - path: "docs/pa/licenses.md"
      provides: "Punjabi Lizenz-Seite"
  key_links:
    - from: "scripts/gen_wortliste.py"
      to: "docs/{lang}/wortliste.md"
      via: "Extraktion aus lektionen/*.md Wortlisten-Sektionen"
      pattern: "section_keywords.*Lista de palabras"
    - from: "scripts/lan_translate.py generate_licenses()"
      to: "docs/{lang}/licenses.md"
      via: "Phrasen-Substitution ohne LLM"
      pattern: "LICENSES_LABELS.*title"
---

<objective>
Wortlisten und Lizenz-Seiten für ES, TA und PA generieren.

Purpose: gen_wortliste.py extrahiert Vokabular-Sektionen aus den übersetzten Lektionen ohne LLM. generate_licenses() kopiert die deutsche licenses.md mit Phrasen-Substitution. Beide Generatoren benötigen vollständige Lektionen-Dateien (Wave 1).

Output: docs/es/wortliste.md, docs/ta/wortliste.md, docs/pa/wortliste.md und je eine licenses.md.
</objective>

<execution_context>
@/Volumes/SanDisk1TB/proj/Payer/.claude/get-shit-done/workflows/execute-plan.md
@/Volumes/SanDisk1TB/proj/Payer/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@/Volumes/SanDisk1TB/proj/Payer/CLAUDE.md
@/Volumes/SanDisk1TB/proj/Payer/.planning/phases/12-automated-internationalization-it-es/12-CONTEXT.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Wortlisten für ES, TA und PA generieren</name>
  <files>docs/es/wortliste.md, docs/ta/wortliste.md, docs/pa/wortliste.md</files>

  <read_first>
    /Volumes/SanDisk1TB/proj/Payer/scripts/gen_wortliste.py — komplett (60 Zeilen: Usage, LANG_CONFIG, ACTIVE_LANGS)
  </read_first>

  <action>
Führe gen_wortliste.py für die drei Zielsprachen aus:

cd /Volumes/SanDisk1TB/proj/Payer && python3 scripts/gen_wortliste.py es ta pa

Das Skript:
- Liest alle docs/es/lektionen/lektion*.md durch und extrahiert Abschnitte, die den LANG_CONFIG["es"]["section_keywords"] entsprechen ("Lista de palabras", "Vocabulario").
- Schreibt das Ergebnis als docs/es/wortliste.md mit dem Frontmatter aus LANG_CONFIG["es"]["frontmatter"].
- Wiederholt dies für ta und pa mit den jeweiligen Konfigurationen.

Falls die Ausgabe leer oder sehr kurz ist (< 100 Zeilen): Das Skript hat keine Wortlisten-Sektionen gefunden. In diesem Fall:
1. Prüfe stichprobenartig docs/ta/lektionen/lektion01.md auf den tatsächlichen Abschnitts-Namen (grep -n "Wort\|Word\|பதம்\|ਸ਼ਬਦ" docs/ta/lektionen/lektion01.md | head -10).
2. Notiere den gefundenen Abschnitts-Namen für den SUMMARY.
3. Falls der Keyword-Match komplett versagt: Führe stattdessen gen_wortliste.py ohne Sprachfilter aus (python3 scripts/gen_wortliste.py) und prüfe, ob die DE-Wortliste korrekt erzeugt wird — das bestätigt, dass das Skript funktioniert.
  </action>

  <verify>
    <automated>
test -f /Volumes/SanDisk1TB/proj/Payer/docs/es/wortliste.md && test -f /Volumes/SanDisk1TB/proj/Payer/docs/ta/wortliste.md && test -f /Volumes/SanDisk1TB/proj/Payer/docs/pa/wortliste.md && wc -l /Volumes/SanDisk1TB/proj/Payer/docs/es/wortliste.md /Volumes/SanDisk1TB/proj/Payer/docs/ta/wortliste.md /Volumes/SanDisk1TB/proj/Payer/docs/pa/wortliste.md
    </automated>
  </verify>

  <acceptance_criteria>
- docs/es/wortliste.md, docs/ta/wortliste.md und docs/pa/wortliste.md existieren
- Jede Datei hat mindestens 10 Zeilen (Frontmatter + Titel + mindestens ein Eintrag)
- Kein Python-Traceback in der Ausgabe
  </acceptance_criteria>

  <done>Drei wortliste.md-Dateien vorhanden mit zumindest Frontmatter und Titel.</done>
</task>

<task type="auto">
  <name>Task 2: licenses.md für ES, TA und PA generieren</name>
  <files>docs/es/licenses.md, docs/ta/licenses.md, docs/pa/licenses.md</files>

  <read_first>
    /Volumes/SanDisk1TB/proj/Payer/scripts/lan_translate.py — Zeilen 861-888 (generate_licenses-Funktion), Zeilen 31-86 (LICENSES_LABELS für es/ta/pa), Zeilen 941-951 (translate_main_pages)
  </read_first>

  <action>
generate_licenses() wird durch translate_main_pages() aufgerufen. Der einfachste Weg ist, --pages zu verwenden, was Hauptseiten UND licenses.md schreibt. Da index.md/grammatik.md/impressum.md/themen.md bereits aus Wave 1 vorhanden sind, überspringt das Skript sie (mtime-Check). Nur licenses.md wird neu geschrieben, wenn die DE-Quelle neuer ist.

Führe aus:
cd /Volumes/SanDisk1TB/proj/Payer && python3 scripts/lan_translate.py --lang es --pages
cd /Volumes/SanDisk1TB/proj/Payer && python3 scripts/lan_translate.py --lang ta --pages
cd /Volumes/SanDisk1TB/proj/Payer && python3 scripts/lan_translate.py --lang pa --pages

Falls eine der licenses.md-Dateien fehlt trotz "up to date"-Meldung (weil out_path neuer als src_path):
cd /Volumes/SanDisk1TB/proj/Payer && python3 -c "
from scripts.lan_translate import generate_licenses
import os, sys
os.chdir('/Volumes/SanDisk1TB/proj/Payer')
sys.path.insert(0, 'scripts')
for lang in ['es', 'ta', 'pa']:
    from lan_translate import generate_licenses
    generate_licenses(lang)
"

Alternativ: touch docs/licenses.md, dann --pages erneut ausführen (aktualisiert mtime der Quelle).

Verifiziere nach Abschluss:
- Erste Zeile von docs/es/licenses.md enthält "Auditoría de licencias de imágenes" (aus LICENSES_LABELS["es"]["title"])
- Erste Zeile von docs/ta/licenses.md enthält "படப் உரிம தணிக்கை" (aus LICENSES_LABELS["ta"]["title"])
- Erste Zeile von docs/pa/licenses.md enthält "ਚਿੱਤਰ ਲਾਇਸੈਂਸ ਆਡਿਟ" (aus LICENSES_LABELS["pa"]["title"])
  </action>

  <verify>
    <automated>
grep -l "Auditoría" /Volumes/SanDisk1TB/proj/Payer/docs/es/licenses.md && grep -l "படப்" /Volumes/SanDisk1TB/proj/Payer/docs/ta/licenses.md && grep -l "ਚਿੱਤਰ" /Volumes/SanDisk1TB/proj/Payer/docs/pa/licenses.md
    </automated>
  </verify>

  <acceptance_criteria>
- docs/es/licenses.md enthält den String "Auditoría de licencias de imágenes"
- docs/ta/licenses.md enthält den String "படப் உரிம தணிக்கை"
- docs/pa/licenses.md enthält den String "ਚਿੱਤਰ ਲਾਇਸੈਂਸ ਆਡਿਟ"
- Alle drei Dateien sind nicht leer (> 5 Zeilen)
  </acceptance_criteria>

  <done>Drei licenses.md-Dateien mit sprachspezifischen Überschriften vorhanden.</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Beschreibung |
|----------|-------------|
| docs/licenses.md → gen_wortliste/generate_licenses | Quell-Markdown wird kopiert und substituiert |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-12-03 | Information Disclosure | licenses.md Phrasen-Substitution | accept | Nur feste Phrasen aus LICENSES_PHRASES Dict, kein dynamisches Parsen |
| T-12-04 | Tampering | gen_wortliste.py Regex-Extraktion | accept | Liest nur bereits übersetzte Markdown-Dateien; kein Netzwerkzugriff |
| T-12-SC | Tampering | npm/pip installs | accept | Keine neuen Installationen in diesem Plan |
</threat_model>

<verification>
Nach Task 1: 3 wortliste.md-Dateien mit Inhalt.
Nach Task 2: 3 licenses.md-Dateien mit sprachspezifischen Titeln.
Gesamt: 6 neue Dateien in docs/es/, docs/ta/, docs/pa/.
</verification>

<success_criteria>
- docs/es/wortliste.md, docs/ta/wortliste.md, docs/pa/wortliste.md — vorhanden, nicht leer
- docs/es/licenses.md — enthält "Auditoría de licencias de imágenes"
- docs/ta/licenses.md — enthält "படப் உரிம தணிக்கை"
- docs/pa/licenses.md — enthält "ਚਿੱਤਰ ਲਾਇਸੈਂਸ ਆਡਿਟ"
</success_criteria>

<output>
Erstelle `.planning/phases/12-automated-internationalization-it-es/12-2-SUMMARY.md` nach Abschluss.
</output>

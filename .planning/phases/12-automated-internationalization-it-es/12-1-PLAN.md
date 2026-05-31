---
phase: 12-automated-internationalization-it-es
plan: 1
type: execute
wave: 1
depends_on: []
files_modified:
  - docs/es/lektionen/
  - docs/ta/lektionen/
  - docs/pa/lektionen/
  - docs/ta/index.md
  - docs/ta/grammatik.md
  - docs/ta/impressum.md
  - docs/ta/themen.md
  - docs/pa/index.md
  - docs/pa/grammatik.md
  - docs/pa/impressum.md
  - docs/pa/themen.md
autonomous: true
requirements:
  - I18N-09
  - I18N-10

must_haves:
  truths:
    - "docs/es/lektionen/ enthält 11 schrift-Dateien (schrift01.md–schrift11.md)"
    - "docs/es/lektionen/ enthält 61 uebung-Dateien (uebung01.md–uebung61.md)"
    - "docs/ta/lektionen/ enthält 61 lektion-Dateien, 11 schrift-Dateien und 61 uebung-Dateien"
    - "docs/pa/lektionen/ enthält 61 lektion-Dateien, 11 schrift-Dateien und 61 uebung-Dateien"
    - "docs/ta/ enthält index.md, grammatik.md, impressum.md, themen.md"
    - "docs/pa/ enthält index.md, grammatik.md, impressum.md, themen.md"
  artifacts:
    - path: "docs/es/lektionen/schrift01.md"
      provides: "Spanische Schrift-Seite 01"
    - path: "docs/es/lektionen/uebung01.md"
      provides: "Spanische Übungs-Seite 01"
    - path: "docs/ta/lektionen/lektion01.md"
      provides: "Tamilische Lektion 01"
    - path: "docs/pa/lektionen/lektion01.md"
      provides: "Punjabi Lektion 01"
  key_links:
    - from: "scripts/lan_translate.py"
      to: "docs/{lang}/lektionen/"
      via: "translate_file() mit mtime-Check"
      pattern: "os\\.path\\.exists.*lektion"
---

<objective>
Übersetzungsabschluss für ES, TA und PA sicherstellen.

Purpose: Die Hintergrund-Jobs (PIDs 77177/77178) übersetzen laufend. Dieser Plan prüft, ob alle Dateien vollständig erzeugt wurden, und startet fehlende Übersetzungen nach. Erst wenn alle Dateien vorhanden sind, können Wave-2-Pläne beginnen.

Output: Vollständige Dateibestände in docs/es/lektionen/ (schrift + uebung), docs/ta/ (lektionen + Hauptseiten) und docs/pa/ (lektionen + Hauptseiten).
</objective>

<execution_context>
@/Volumes/SanDisk1TB/proj/Payer/.claude/get-shit-done/workflows/execute-plan.md
@/Volumes/SanDisk1TB/proj/Payer/.claude/get-shit-done/templates/summary.md
</execution_context>

<context>
@/Volumes/SanDisk1TB/proj/Payer/CLAUDE.md
@/Volumes/SanDisk1TB/proj/Payer/.planning/ROADMAP.md
@/Volumes/SanDisk1TB/proj/Payer/.planning/phases/12-automated-internationalization-it-es/12-CONTEXT.md
</context>

<tasks>

<task type="auto">
  <name>Task 1: Übersetzungsstand prüfen und fehlende Dateien ermitteln</name>
  <files>docs/es/lektionen/, docs/ta/lektionen/, docs/pa/lektionen/</files>

  <read_first>
    /Volumes/SanDisk1TB/proj/Payer/scripts/lan_translate.py — Zeilen 1-30 (LANGUAGES, LESSONS, MAIN_PAGES), Zeilen 891-980 (parse_lang_args, main)
    /Volumes/SanDisk1TB/proj/Payer/CLAUDE.md — Hard Rules
  </read_first>

  <action>
Führe folgende Shell-Befehle aus, um den Ist-Stand zu ermitteln:

1. ES schrift-Dateien zählen:
   ls /Volumes/SanDisk1TB/proj/Payer/docs/es/lektionen/ | grep -c "^schrift"

   Erwartet: 11. Bei weniger als 11: Notiere welche fehlen (schrift01.md–schrift11.md).

2. ES uebung-Dateien zählen:
   ls /Volumes/SanDisk1TB/proj/Payer/docs/es/lektionen/ | grep -c "^uebung"

   Erwartet: 61. Bei weniger als 61: Notiere fehlende Nummern.

3. TA lektion-Dateien zählen:
   ls /Volumes/SanDisk1TB/proj/Payer/docs/ta/lektionen/ | grep -c "^lektion"

   Erwartet: 61.

4. TA schrift-Dateien zählen:
   ls /Volumes/SanDisk1TB/proj/Payer/docs/ta/lektionen/ | grep -c "^schrift"

   Erwartet: 11.

5. TA uebung-Dateien zählen:
   ls /Volumes/SanDisk1TB/proj/Payer/docs/ta/lektionen/ | grep -c "^uebung"

   Erwartet: 61.

6. PA lektion-Dateien zählen:
   ls /Volumes/SanDisk1TB/proj/Payer/docs/pa/lektionen/ | grep -c "^lektion"

   Erwartet: 61.

7. PA schrift-Dateien zählen:
   ls /Volumes/SanDisk1TB/proj/Payer/docs/pa/lektionen/ | grep -c "^schrift"

   Erwartet: 11.

8. PA uebung-Dateien zählen:
   ls /Volumes/SanDisk1TB/proj/Payer/docs/pa/lektionen/ | grep -c "^uebung"

   Erwartet: 61.

9. Hauptseiten TA prüfen:
   ls /Volumes/SanDisk1TB/proj/Payer/docs/ta/ | grep -E "^(index|grammatik|impressum|themen)\.md"

   Erwartet: 4 Dateien.

10. Hauptseiten PA prüfen:
    ls /Volumes/SanDisk1TB/proj/Payer/docs/pa/ | grep -E "^(index|grammatik|impressum|themen)\.md"

    Erwartet: 4 Dateien.

Dokumentiere das Ergebnis für Task 2.
  </action>

  <verify>
    <automated>
ls /Volumes/SanDisk1TB/proj/Payer/docs/es/lektionen/ | grep -c "^schrift" && ls /Volumes/SanDisk1TB/proj/Payer/docs/es/lektionen/ | grep -c "^uebung" && ls /Volumes/SanDisk1TB/proj/Payer/docs/ta/lektionen/ | grep -c "^lektion" && ls /Volumes/SanDisk1TB/proj/Payer/docs/pa/lektionen/ | grep -c "^lektion"
    </automated>
  </verify>

  <acceptance_criteria>
- Ausgabe zeigt exakte Zählungen für alle 8 Dateigruppen
- Fehlende Dateien sind namentlich aufgelistet (falls vorhanden)
- Kein Fehler beim ls-Befehl (Verzeichnisse existieren)
  </acceptance_criteria>

  <done>Ist-Stand aller Übersetzungsdateien dokumentiert, fehlende Nummern identifiziert.</done>
</task>

<task type="auto">
  <name>Task 2: Fehlende Übersetzungen nachstarten</name>
  <files>docs/es/lektionen/, docs/ta/lektionen/, docs/pa/lektionen/, docs/ta/index.md, docs/ta/grammatik.md, docs/ta/impressum.md, docs/ta/themen.md, docs/pa/index.md, docs/pa/grammatik.md, docs/pa/impressum.md, docs/pa/themen.md</files>

  <read_first>
    /Volumes/SanDisk1TB/proj/Payer/scripts/lan_translate.py — Zeilen 959-980 (main, Usage-Beispiele)
  </read_first>

  <action>
Starte basierend auf den Ergebnissen aus Task 1 gezielte Nachhol-Jobs. Das Skript überspringt bereits vorhandene Dateien automatisch (mtime-Check), daher können die Befehle auch bei vollständigem Stand bedenkenlos ausgeführt werden.

Führe die folgenden Befehle sequenziell aus (warte jeweils auf Abschluss):

1. Für ES schrift + uebung (wenn schrift < 11 oder uebung < 61):
   cd /Volumes/SanDisk1TB/proj/Payer && python3 scripts/lan_translate.py --lang es all

   Das Skript übersetzt alle fehlenden Dateien (schrift, uebung, lektion) für ES und überspringt vorhandene.

2. Für TA alle Dateien (wenn lektion < 61 oder schrift < 11 oder uebung < 61):
   cd /Volumes/SanDisk1TB/proj/Payer && python3 scripts/lan_translate.py --lang ta all

3. Für PA alle Dateien (wenn lektion < 61 oder schrift < 11 oder uebung < 61):
   cd /Volumes/SanDisk1TB/proj/Payer && python3 scripts/lan_translate.py --lang pa all

4. Für TA + PA Hauptseiten (wenn index.md/grammatik.md/impressum.md/themen.md fehlen):
   cd /Volumes/SanDisk1TB/proj/Payer && python3 scripts/lan_translate.py --lang ta --pages
   cd /Volumes/SanDisk1TB/proj/Payer && python3 scripts/lan_translate.py --lang pa --pages

Hinweis: Die Jobs verbinden sich mit nyx.local:8000. Falls der Server nicht erreichbar ist, beendet das Skript mit einem Netzwerkfehler — in diesem Fall den Nutzer informieren und auf Server-Verfügbarkeit prüfen lassen.

Nach Abschluss aller Jobs: Wiederhole die Zählungen aus Task 1, um Vollständigkeit zu bestätigen.
  </action>

  <verify>
    <automated>
ls /Volumes/SanDisk1TB/proj/Payer/docs/es/lektionen/ | grep "^schrift" | wc -l | tr -d ' ' | grep -x "11" && ls /Volumes/SanDisk1TB/proj/Payer/docs/es/lektionen/ | grep "^uebung" | wc -l | tr -d ' ' | grep -x "61" && ls /Volumes/SanDisk1TB/proj/Payer/docs/ta/lektionen/ | grep "^lektion" | wc -l | tr -d ' ' | grep -x "61" && ls /Volumes/SanDisk1TB/proj/Payer/docs/pa/lektionen/ | grep "^lektion" | wc -l | tr -d ' ' | grep -x "61"
    </automated>
  </verify>

  <acceptance_criteria>
- docs/es/lektionen/ enthält genau 11 schrift*.md Dateien
- docs/es/lektionen/ enthält genau 61 uebung*.md Dateien
- docs/ta/lektionen/ enthält genau 61 lektion*.md Dateien
- docs/ta/lektionen/ enthält genau 11 schrift*.md Dateien
- docs/ta/lektionen/ enthält genau 61 uebung*.md Dateien
- docs/pa/lektionen/ enthält genau 61 lektion*.md Dateien
- docs/pa/lektionen/ enthält genau 11 schrift*.md Dateien
- docs/pa/lektionen/ enthält genau 61 uebung*.md Dateien
- docs/ta/ enthält index.md, grammatik.md, impressum.md, themen.md
- docs/pa/ enthält index.md, grammatik.md, impressum.md, themen.md
  </acceptance_criteria>

  <done>Alle Übersetzungsdateien für ES, TA und PA sind vollständig vorhanden.</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Beschreibung |
|----------|-------------|
| nyx.local:8000 → Python-Skript | LLM-Output wird direkt in Markdown-Dateien geschrieben |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-12-01 | Tampering | LLM-Output in Markdown | accept | Skript schreibt UTF-8 plain text; kein Code-Execution-Pfad |
| T-12-02 | Denial of Service | nyx.local:8000 | accept | Lokaler Server, kein externer Angriffspunkt; Retry-Logik im Skript |
| T-12-SC | Tampering | pip/npm installs | accept | Keine neuen Package-Installationen in diesem Plan |
</threat_model>

<verification>
Nach Task 2: Alle drei Sprachen vollständig übersetzt.
Zählung: ES schrift=11, ES uebung=61, TA lektion=61, TA schrift=11, TA uebung=61, PA lektion=61, PA schrift=11, PA uebung=61.
Hauptseiten TA und PA: je 4 Dateien vorhanden.
</verification>

<success_criteria>
- docs/es/lektionen/: 61 lektion + 11 schrift + 61 uebung = 133 Dateien
- docs/ta/lektionen/: 61 lektion + 11 schrift + 61 uebung = 133 Dateien
- docs/pa/lektionen/: 61 lektion + 11 schrift + 61 uebung = 133 Dateien
- docs/ta/: index.md, grammatik.md, impressum.md, themen.md vorhanden
- docs/pa/: index.md, grammatik.md, impressum.md, themen.md vorhanden
</success_criteria>

<output>
Erstelle `.planning/phases/12-automated-internationalization-it-es/12-1-SUMMARY.md` nach Abschluss.
</output>

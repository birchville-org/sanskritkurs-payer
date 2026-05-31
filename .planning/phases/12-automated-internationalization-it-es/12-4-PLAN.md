---
phase: 12-automated-internationalization-it-es
plan: 4
type: execute
wave: 3
depends_on:
  - 12-2
  - 12-3
files_modified:
  - .planning/phases/12-automated-internationalization-it-es/12-4-SUMMARY.md
autonomous: false
requirements:
  - I18N-06
  - I18N-09
  - I18N-10
  - I18N-11

must_haves:
  truths:
    - "npm run docs:build läuft ohne Fehler durch"
    - "Build-Ausgabe enthält Seiten für es/, ta/ und pa/"
    - "Alle Phase-12-Anforderungen (ES 133 Dateien, TA 133 Dateien, PA 133 Dateien) erfüllt"
    - "Git-Commit mit allen neuen Übersetzungsdateien erstellt"
  artifacts:
    - path: "docs/.vitepress/dist/"
      provides: "Produktions-Build mit 11 Sprachen"
    - path: ".planning/phases/12-automated-internationalization-it-es/12-4-SUMMARY.md"
      provides: "Abschlussdokumentation Phase 12"
  key_links:
    - from: "npm run docs:build"
      to: "docs/.vitepress/dist/"
      via: "VitePress SSG"
      pattern: "docs:build"
---

<objective>
Build-Verifikation und Git-Commit für Phase 12.

Purpose: Finaler Build-Gate-Test gemäß CLAUDE.md Hard Rule. Erst wenn `npm run docs:build` erfolgreich durchläuft, gilt Phase 12 als abgeschlossen. Anschließend werden alle neuen Dateien committed.

Output: Grüner Build, Git-Commit mit vollständigem ES/TA/PA-Inhaltsbestand.
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
  <name>Task 1: Build-Gate — npm run docs:build</name>
  <files>docs/.vitepress/dist/</files>

  <read_first>
    /Volumes/SanDisk1TB/proj/Payer/CLAUDE.md — Build Gate Hard Rule
    /Volumes/SanDisk1TB/proj/Payer/package.json — Build-Skript und NODE_OPTIONS
  </read_first>

  <action>
Führe den VitePress-Build aus:

cd /Volumes/SanDisk1TB/proj/Payer && npm run docs:build

Der Build nutzt NODE_OPTIONS=--max-old-space-size=8192 (in package.json konfiguriert) um den erhöhten Speicherbedarf der drei neuen Sprachen (je ~135 Seiten = ~400 Seiten mehr) abzufangen.

Erwartete Laufzeit: 5-15 Minuten bei 11 Sprachen × ~135 Seiten.

Bei Build-Fehler: Lies die genaue Fehlermeldung. Häufige Ursachen und Korrekturen:

1. "Cannot find module" oder "file not found" → Eine Datei wird in config.mjs referenziert, existiert aber nicht. Prüfe docs/.vitepress/config.mjs auf Sidebar-Einträge für ta/pa und vergleiche mit tatsächlichen Dateipfaden.

2. "YAML frontmatter parse error" → Eine übersetzte Datei hat defektes Frontmatter. Suche:
   grep -rn "^---" docs/ta/ docs/pa/ | grep -v "^Binary" | head -20

3. "Out of memory" → NODE_OPTIONS wurde nicht gesetzt. Prüfe: node --max-old-space-size=8192 node_modules/.bin/vitepress build docs

4. VitePress "broken links" → Ein interaktiver Link zeigt auf eine nicht vorhandene Seite. Ausgabe des Build-Logs nach "dead link" durchsuchen.

Nach erfolgreichem Build: Prüfe die Ausgabe:
ls /Volumes/SanDisk1TB/proj/Payer/docs/.vitepress/dist/es/ 2>/dev/null | wc -l
ls /Volumes/SanDisk1TB/proj/Payer/docs/.vitepress/dist/ta/ 2>/dev/null | wc -l
ls /Volumes/SanDisk1TB/proj/Payer/docs/.vitepress/dist/pa/ 2>/dev/null | wc -l

Jedes Verzeichnis sollte mehr als 0 Einträge haben.
  </action>

  <verify>
    <automated>
cd /Volumes/SanDisk1TB/proj/Payer && npm run docs:build 2>&1 | tail -5
    </automated>
  </verify>

  <acceptance_criteria>
- npm run docs:build beendet sich mit Exit-Code 0
- Build-Ausgabe enthält keine "Error:" Zeile
- docs/.vitepress/dist/es/, docs/.vitepress/dist/ta/ und docs/.vitepress/dist/pa/ existieren nach dem Build
  </acceptance_criteria>

  <done>Build erfolgreich abgeschlossen ohne Fehler.</done>
</task>

<task type="checkpoint:human-verify" gate="blocking">
  <what-built>
VitePress-Build mit 11 Sprachen wurde ausgeführt. ES, TA und PA sind vollständig übersetzt (je 133 Lektionen/Schrift/Übungs-Dateien), Wortlisten und Lizenz-Seiten sind generiert.
  </what-built>
  <how-to-verify>
1. Starte den Dev-Server: cd /Volumes/SanDisk1TB/proj/Payer && npm run docs:dev

2. Öffne http://localhost:5173 im Browser.

3. Prüfe den Sprach-Wähler: Zeigt er 11 Sprachen an? (DE, EN, IT, BG, RU, UK, HI, FR, ES, TA, PA)

4. Wechsle zu Spanisch (ES) und öffne Lektion 1 — erscheint spanischer Text?

5. Wechsle zu Tamil (TA) und öffne Lektion 1 — erscheint tamilischer Text?

6. Wechsle zu Punjabi (PA) und öffne Lektion 1 — erscheint Gurmukhi-Text?

7. Prüfe in einer Sprache: Schrift- und Übungsseiten über die Sidebar erreichbar?
  </how-to-verify>
  <resume-signal>Tippe "approved" wenn alle 7 Punkte bestätigt, oder beschreibe gefundene Probleme.</resume-signal>
</task>

<task type="auto">
  <name>Task 3: Git-Commit aller neuen Übersetzungsdateien</name>
  <files>.planning/phases/12-automated-internationalization-it-es/12-4-SUMMARY.md</files>

  <read_first>
    /Volumes/SanDisk1TB/proj/Payer/CLAUDE.md — Build Gate (muss vor Commit bestanden sein)
  </read_first>

  <action>
Commit nur nach grünem Build (Task 1) und menschlicher Verifikation (Task 2).

Füge alle neuen Übersetzungsdateien zum Staging-Bereich hinzu:

git -C /Volumes/SanDisk1TB/proj/Payer add docs/es/lektionen/schrift*.md docs/es/lektionen/uebung*.md docs/es/wortliste.md docs/es/licenses.md
git -C /Volumes/SanDisk1TB/proj/Payer add docs/ta/
git -C /Volumes/SanDisk1TB/proj/Payer add docs/pa/

Prüfe den Staging-Status:
git -C /Volumes/SanDisk1TB/proj/Payer status --short | head -20

Erstelle den Commit:
git -C /Volumes/SanDisk1TB/proj/Payer commit -m "feat(i18n): complete ES/TA/PA translations for Phase 12

- ES: add schrift01-11, uebung01-61, wortliste, licenses
- TA: add all 61 lektionen, 11 schrift, 61 uebung, main pages, wortliste, licenses
- PA: add all 61 lektionen, 11 schrift, 61 uebung, main pages, wortliste, licenses
- Build: npm run docs:build passes with 11 active locales

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

Verifiziere den Commit:
git -C /Volumes/SanDisk1TB/proj/Payer log --oneline -3
  </action>

  <verify>
    <automated>
git -C /Volumes/SanDisk1TB/proj/Payer log --oneline -1 | grep -i "i18n\|ES\|TA\|PA\|phase 12"
    </automated>
  </verify>

  <acceptance_criteria>
- git log zeigt den neuen Commit mit "i18n" oder Sprach-Kürzel im Titel
- git status zeigt "nothing to commit" oder nur nicht-gestagete Dateien aus anderen Arbeitsbereichen
- Commit-Message enthält alle drei Sprachen (ES, TA, PA)
  </acceptance_criteria>

  <done>Git-Commit mit allen Phase-12-Übersetzungsdateien erstellt.</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Beschreibung |
|----------|-------------|
| npm run docs:build | Verarbeitet ~1500 Markdown-Dateien, läuft lokal |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-12-07 | Denial of Service | VitePress Build (11 Sprachen × 135 Seiten) | mitigate | NODE_OPTIONS=--max-old-space-size=8192 in package.json gesetzt (D-01) |
| T-12-08 | Tampering | git add docs/ | mitigate | Nur docs/es/, docs/ta/, docs/pa/ werden gestaged; docs/lektionen/ explizit ausgelassen |
| T-12-SC | Tampering | npm/pip installs | accept | Keine neuen Installationen |
</threat_model>

<verification>
Nach Task 1: npm run docs:build Exit-Code 0.
Nach Task 2 (Checkpoint): Menschliche Bestätigung der 11-Sprachen-Navigation.
Nach Task 3: Git-Commit vorhanden.
</verification>

<success_criteria>
- npm run docs:build erfolgreich (Exit-Code 0, kein "Error:" in Ausgabe)
- Sprach-Wähler zeigt 11 Sprachen (DE, EN, IT, BG, RU, UK, HI, FR, ES, TA, PA)
- Git-Commit mit ES/TA/PA-Dateien in der Historie
- Phase 12 vollständig: ES 133 Seiten, TA 133 Seiten, PA 133 Seiten + je wortliste + licenses
</success_criteria>

<output>
Erstelle `.planning/phases/12-automated-internationalization-it-es/12-4-SUMMARY.md` nach Abschluss.
</output>

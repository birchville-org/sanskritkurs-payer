---
phase: 12-automated-internationalization-it-es
plan: 3
type: execute
wave: 2
depends_on:
  - 12-1
files_modified:
  - docs/es/lektionen/
  - docs/ta/lektionen/
  - docs/pa/lektionen/
  - docs/ta/index.md
  - docs/ta/grammatik.md
  - docs/pa/index.md
  - docs/pa/grammatik.md
autonomous: true
requirements:
  - I18N-06
  - I18N-09
  - I18N-10

must_haves:
  truths:
    - "Kein rohes HTML in docs/es/, docs/ta/ oder docs/pa/ (ausgenommen docs/lektionen/ DE-Referenz)"
    - "Kein nicht-übersetzter TODO-Marker oder DEVA_-Platzhalter in ES/TA/PA-Dateien"
    - "Keine deutschen Passagen (außer unübersetzbaren Sanskrit-Termen) in TA und PA"
    - "sync_layouts.py meldet keine Layout-Abweichungen für ES/TA/PA"
  artifacts:
    - path: "docs/es/lektionen/lektion01.md"
      provides: "Bereinigte spanische Lektion 01 (kein HTML)"
    - path: "docs/ta/lektionen/lektion01.md"
      provides: "Bereinigte tamilische Lektion 01 (kein HTML)"
    - path: "docs/pa/lektionen/lektion01.md"
      provides: "Bereinigte Punjabi Lektion 01 (kein HTML)"
  key_links:
    - from: "scripts/purge_html.py"
      to: "docs/es/ docs/ta/ docs/pa/"
      via: "Regex-basierte HTML-Entfernung"
      pattern: "purge_html.*content"
    - from: "scripts/sync_layouts.py"
      to: "docs/{lang}/lektionen/"
      via: "Layout-Synchronisation von DE-Referenz"
      pattern: "sync_layouts.*lang"
---

<objective>
Qualitätsprüfung der übersetzten ES-, TA- und PA-Dateien.

Purpose: Maschinell übersetzte Dateien können rohes HTML, nicht-ersetzte Platzhalter oder unübersetzte deutsche Passagen enthalten. Dieser Plan bereinigt und prüft alle drei Sprachen, bevor der Build-Schritt (Wave 3) gestartet wird.

Output: Bereinigte Dateien ohne HTML-Reste, ohne TODO-Marker und ohne Layout-Abweichungen.
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
  <name>Task 1: HTML-Bereinigung und Platzhalter-Suche</name>
  <files>docs/es/lektionen/, docs/ta/lektionen/, docs/pa/lektionen/, docs/ta/index.md, docs/ta/grammatik.md, docs/pa/index.md, docs/pa/grammatik.md</files>

  <read_first>
    /Volumes/SanDisk1TB/proj/Payer/scripts/purge_html.py — komplett (Zeilen 1-50: purge_html-Funktion, Zielpfad-Konfiguration)
    /Volumes/SanDisk1TB/proj/Payer/CLAUDE.md — Hard Rules (Zero-HTML, German is immutable, Devanāgarī always red)
  </read_first>

  <action>
Schritt 1 — Platzhalter und Fehler suchen:

Suche nach nicht-übersetzten Platzhaltern in ES/TA/PA:
grep -rn "TODO\|DEVA_\|\[TRANSLATE\]\|\[FEHLER\]" /Volumes/SanDisk1TB/proj/Payer/docs/es/ /Volumes/SanDisk1TB/proj/Payer/docs/ta/ /Volumes/SanDisk1TB/proj/Payer/docs/pa/ 2>/dev/null | grep -v "SUMMARY\|\.planning" | head -30

Suche nach rohem HTML (häufigste Überreste):
grep -rn "<div\|<span\|<table\|<br>\|<p>\|<strong>" /Volumes/SanDisk1TB/proj/Payer/docs/es/lektionen/ /Volumes/SanDisk1TB/proj/Payer/docs/ta/lektionen/ /Volumes/SanDisk1TB/proj/Payer/docs/pa/lektionen/ 2>/dev/null | head -30

Dokumentiere alle Treffer für den SUMMARY.

Schritt 2 — purge_html.py anpassen und ausführen:

purge_html.py arbeitet standardmäßig auf docs/lektionen/ (DE). Die DE-Dateien dürfen NICHT angefasst werden (Hard Rule: German is immutable). Führe das Skript mit angepasstem Verzeichnis aus:

Für ES:
cd /Volumes/SanDisk1TB/proj/Payer && python3 -c "
import sys
sys.argv = ['purge_html.py']
import scripts.purge_html as ph
# purge_html.py liest 'directory' als globale Variable
import importlib.util, os
spec = importlib.util.spec_from_file_location('purge_html', 'scripts/purge_html.py')
mod = importlib.util.load_module_from_spec(spec)
# NICHT direkt ausführen, da directory hardcoded ist.
# Stattdessen: grep nach HTML-Resten und manuell korrigieren
"

Da purge_html.py das Verzeichnis hardcoded hat ('docs/lektionen'), sind folgende Alternativen zu verwenden:

Option A — Direkte sed-Bereinigung der häufigsten HTML-Reste:
find /Volumes/SanDisk1TB/proj/Payer/docs/es /Volumes/SanDisk1TB/proj/Payer/docs/ta /Volumes/SanDisk1TB/proj/Payer/docs/pa -name "*.md" -not -path "*/lektionen/DE/*" | xargs grep -l "<div\|<span\|<br>\|<p>" 2>/dev/null | while read f; do
  echo "HTML gefunden in: $f"
done

Option B — Falls HTML-Reste gefunden werden: Datei-für-Datei mit dem Edit-Tool bereinigen (maximal 5-10 Dateien zu erwarten bei maschineller Übersetzung).

Wichtig: Devanāgarī-Zeichen und IAST in den Dateien NICHT verändern. Nur HTML-Tags entfernen.

Schritt 3 — Stichproben-QA (3 Dateien pro Sprache):
Öffne folgende Dateien und prüfe visuell auf:
- Keine offenen HTML-Tags
- Keine deutschen Fließtext-Passagen (Sanskrit-Termini wie "Sandhi", "Devanāgarī" sind OK)
- VitePress-Container-Syntax (:::) korrekt geschlossen

Stichproben:
head -50 /Volumes/SanDisk1TB/proj/Payer/docs/es/lektionen/lektion01.md
head -50 /Volumes/SanDisk1TB/proj/Payer/docs/ta/lektionen/lektion01.md
head -50 /Volumes/SanDisk1TB/proj/Payer/docs/pa/lektionen/lektion01.md
  </action>

  <verify>
    <automated>
grep -rn "<div\|<span\|<table\|<br>\|<p>" /Volumes/SanDisk1TB/proj/Payer/docs/es/lektionen/ /Volumes/SanDisk1TB/proj/Payer/docs/ta/lektionen/ /Volumes/SanDisk1TB/proj/Payer/docs/pa/lektionen/ 2>/dev/null | wc -l
    </automated>
  </verify>

  <acceptance_criteria>
- grep-Zählung von rohem HTML in ES/TA/PA lektionen: 0 (oder dokumentierte Ausnahmen, die kein Build-Fehler verursachen)
- Kein TODO-Platzhalter in keiner der drei Sprachen
- Stichproben-QA (lektion01 je Sprache) zeigt übersetzte Inhalte, keine deutschen Passagen im Fließtext
- Devanāgarī und IAST unverändert vorhanden
  </acceptance_criteria>

  <done>ES, TA und PA Lektionen-Dateien sind HTML-frei und ohne Übersetzungs-Platzhalter.</done>
</task>

<task type="auto">
  <name>Task 2: Layout-Synchronisation prüfen (sync_layouts.py)</name>
  <files>docs/es/lektionen/, docs/ta/lektionen/, docs/pa/lektionen/</files>

  <read_first>
    /Volumes/SanDisk1TB/proj/Payer/scripts/sync_layouts.py — Zeilen 1-40 (Usage, was wird synchronisiert)
  </read_first>

  <action>
sync_layouts.py synchronisiert strukturelle Layout-Elemente von DE nach anderen Sprachen (z.B. Tabellen-Struktur, Container-Verschachtelung). Es ÜBERSETZT NICHT — es korrigiert nur strukturelle Abweichungen.

Führe für jede Sprache eine Prüfung aus:

cd /Volumes/SanDisk1TB/proj/Payer && python3 scripts/sync_layouts.py es
cd /Volumes/SanDisk1TB/proj/Payer && python3 scripts/sync_layouts.py ta
cd /Volumes/SanDisk1TB/proj/Payer && python3 scripts/sync_layouts.py pa

Falls das Skript keine Sprache als Argument akzeptiert, sondern eine Lektion-Nummer erwartet, verwende:
cd /Volumes/SanDisk1TB/proj/Payer && python3 scripts/sync_layouts.py all

Notiere die Ausgabe:
- Wie viele Dateien wurden angepasst?
- Wurden Fehler oder Warnungen gemeldet?

Falls sync_layouts.py Dateien ändert: Das ist korrekt und erwünscht. Die Änderungen verbessern die strukturelle Konsistenz.

Falls sync_layouts.py mit einem Fehler abbricht: Fehler im SUMMARY dokumentieren und mit Task-Ergebnis "teilweise abgeschlossen" markieren.

Abschluss-Check: Prüfe, dass die DE-Referenzdateien (docs/lektionen/) unverändert sind:
git diff --stat /Volumes/SanDisk1TB/proj/Payer/docs/lektionen/ | head -10

Erwartet: keine Änderungen in docs/lektionen/.
  </action>

  <verify>
    <automated>
git -C /Volumes/SanDisk1TB/proj/Payer diff --name-only docs/lektionen/ | wc -l | tr -d ' ' | grep -x "0"
    </automated>
  </verify>

  <acceptance_criteria>
- sync_layouts.py läuft ohne Python-Traceback durch
- docs/lektionen/ (DE-Referenz) zeigt 0 git-Änderungen nach dem Lauf
- Ausgabe von sync_layouts.py für ES/TA/PA im SUMMARY dokumentiert (Anzahl angepasster Dateien)
  </acceptance_criteria>

  <done>Layout-Synchronisation abgeschlossen; DE-Referenz unverändert; Ergebnisse dokumentiert.</done>
</task>

</tasks>

<threat_model>
## Trust Boundaries

| Boundary | Beschreibung |
|----------|-------------|
| DE docs/lektionen/ | Darf von keinem Skript verändert werden (Hard Rule) |

## STRIDE Threat Register

| Threat ID | Category | Component | Disposition | Mitigation Plan |
|-----------|----------|-----------|-------------|-----------------|
| T-12-05 | Tampering | sync_layouts.py → DE-Dateien | mitigate | git diff nach Lauf prüfen; DE-Dateien in acceptance_criteria explizit verifiziert |
| T-12-06 | Tampering | purge_html.py Regex | accept | Bereinigt nur HTML-Tags, kein Textinhalt |
| T-12-SC | Tampering | npm/pip installs | accept | Keine neuen Installationen |
</threat_model>

<verification>
Nach Task 1: 0 rohe HTML-Tags in ES/TA/PA Lektionen.
Nach Task 2: sync_layouts.py erfolgreich, docs/lektionen/ unverändert.
</verification>

<success_criteria>
- grep nach HTML-Tags in ES/TA/PA lektionen/ gibt 0 zurück
- sync_layouts.py läuft ohne Fehler für alle drei Sprachen
- git diff docs/lektionen/ zeigt keine Änderungen
</success_criteria>

<output>
Erstelle `.planning/phases/12-automated-internationalization-it-es/12-3-SUMMARY.md` nach Abschluss.
</output>

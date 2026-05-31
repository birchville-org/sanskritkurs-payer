---
phase: 15-vitepress-aware-markdown-editor
plan: 03
subsystem: ui
tags: [css, editor-preview, grammar-box, vitepress-parity, qa-viewer]

requires:
  - "15-02 (Editor-Tab): div#editor-preview mit editor-preview Klasse muss existieren"
provides:
  - "Inline <style id='editor-preview-styles'>-Block in qa_viewer.html"
  - "Alle Container-CSS-Regeln gescoped auf .editor-preview"
  - "Visuelle 1:1-Parität mit VitePress-Build fuer grammar-box, grammar-box2, deleteme-box, no-header, tables"
affects:
  - "qa_viewer.html Editor-Tab: Vorschau zeigt korrekt gestylte Container"

tech-stack:
  added: []
  patterns:
    - "CSS-Scope-Präfix .editor-preview auf allen Container-Regeln (Pitfall 3 aus RESEARCH.md)"
    - "Dark-Mode-Overrides via .dark .editor-preview (kompatibel mit bestehender toggleTheme()-Logik)"

key-files:
  created: []
  modified:
    - "docs/public/qa_viewer.html"

key-decisions:
  - "Kein !important-Overuse: nur fuer deleteme-box und no-header thead, analog zu custom.css-Vorlage"
  - "Bestehende .editor-preview Basis-Regel (aus Plan 02, display:none/padding/bg) bleibt erhalten; neuer Block erweitert sie mit Container-spezifischem Styling"
  - "color: #b22222 fuer .sanskrit-dev (nicht #ff0000 aus CLAUDE.md-Text) — massgeblich ist custom.css (#b22222 ist der tatsaechliche Wert)"

requirements-completed: [EDIT-01, EDIT-02]

duration: 8min
completed: 2026-05-31
---

# Phase 15 Plan 03: Editor-Preview CSS Summary

**Vollstaendiger Container-CSS-Block als `<style id="editor-preview-styles">` in qa_viewer.html eingefuegt — alle 12 Container-Typen auf .editor-preview gescoped, visuelle Parität mit VitePress-Build**

## Performance

- **Duration:** ~8 min
- **Started:** 2026-05-31T18:18:00Z
- **Completed:** 2026-05-31T18:26:00Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments

- `<style id="editor-preview-styles">` nach dem bestehenden `<style>`-Block in `<head>` eingefuegt
- Alle Regeln mit `.editor-preview`-Praefix gescoped (kein CSS-Leak in qa_viewer-UI)
- grammar-box: gelber Hintergrund #fefce8, goldener Rand #eab308 + Dark-Mode-Override #241500
- grammar-box2: oranger Hintergrund #ffedd5, tief-oranger Rand #ea580c + Dark-Mode-Override #361e04
- deleteme-box: `display: none !important` (unsichtbar)
- no-header table thead: `display: none !important`
- sanskrit-dev: `color: #b22222` (CLAUDE.md Hard Rule: Devanagari immer rot)
- Tabellen: `border-collapse: collapse`, `border: 1px solid #94a3b8`, `padding: 0.6rem 0.8rem`
- Dark-Mode-Zeilenstreifung, compact/laut-table-Helfer, blockquote-Resets in grammar-box(2)
- npm run docs:build besteht ohne Fehler

## Task Commits

1. **Task 1: Editor-Preview CSS-Block in qa_viewer.html einfuegen** - `ccba1a0` (feat)

## Files Created/Modified

- `docs/public/qa_viewer.html` - Neuer `<style id="editor-preview-styles">`-Block mit 65 CSS-Zeilen

## Decisions Made

- **color: #b22222 statt #ff0000:** CLAUDE.md nennt #ff0000 als Farbe in der Beschreibung, aber custom.css (die massgebliche CSS-Quelle) verwendet #b22222 (Scholastic Red). Der Plan-Spec legt #b22222 explizit fest. custom.css-Wert gewinnt.
- **Bestehende .editor-preview-Basisregel nicht ersetzen:** Plan 02 hat bereits display:none/width/height/overflow/padding/background fuer .editor-preview definiert. Der neue Block ergaenzt Container-Regeln; die Basis-Layout-Eigenschaften im bestehenden style-Block bleiben erhalten (kein Duplikat-Conflict, da CSS-Kaskade gilt).
- **Kein !important-Overuse:** Nur deleteme-box und no-header thead benoetigen !important (analog zu custom.css). Alle anderen Regeln wirken durch Spezifitaet.

## Deviations from Plan

**1. [Rule 3 - Blocking] Worktree-Branch musste auf aktuelle main gerebaset werden**
- **Found during:** Task 1 Vorbereitung
- **Issue:** Der Worktree-Branch wurde vor den Phase-15-Commits erstellt und enthielt qa_viewer.html noch ohne Editor-Elemente aus Plan 02.
- **Fix:** `git rebase b7929ad` auf den letzten merge-Commit von Plan 02 durchgefuehrt. Danach enthielt die Datei alle Editor-Elemente korrekt.
- **Files modified:** keine (nur git-History-Update)
- **Commit:** Kein separater Commit (git-Metadaten-Operation)

## Known Stubs

Keine — CSS-Block ist vollstaendig und alle Container-Typen sind abgedeckt.

## Threat Flags

Keine neuen Trust Boundaries. T-15-05 (CSS-Scope-Verletzung) wurde mitigiert: alle CSS-Regeln haben `.editor-preview`-Praefix. Manuell verifiziert via Node-Check.

## Self-Check: PASSED

- [x] `<style id="editor-preview-styles">` in qa_viewer.html vorhanden
- [x] `.editor-preview .grammar-box` mit #fefce8/#eab308 vorhanden
- [x] `.editor-preview .deleteme-box { display: none !important }` vorhanden
- [x] `.editor-preview .no-header table thead { display: none !important }` vorhanden
- [x] `.editor-preview .sanskrit-dev { color: #b22222 }` vorhanden
- [x] `.dark .editor-preview .grammar-box` und `.grammar-box2` Dark-Mode-Overrides vorhanden
- [x] Tabellen: `border: 1px solid #94a3b8` und `padding: 0.6rem 0.8rem` vorhanden
- [x] Commit ccba1a0 vorhanden
- [x] npm run docs:build erfolgreich

---
*Phase: 15-vitepress-aware-markdown-editor*
*Completed: 2026-05-31*

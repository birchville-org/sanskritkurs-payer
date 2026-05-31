---
phase: 15-vitepress-aware-markdown-editor
plan: 01
subsystem: ui
tags: [markdown-it, markdown-it-container, markdown-it-multimd-table, esm.sh, qa-viewer, scholarly-fixes]

requires: []
provides:
  - "buildRenderer() ES-Modul-Funktion in qa_viewer.html, exponiert als window.buildRenderer"
  - "scholarly_fixes als md.core.ruler.after('linkify') im Browser (Token-API-Ansatz)"
  - "Alle 12 Container-Plugins registriert (grammar-box bis no-header)"
  - "window.render() als Convenience-Wrapper fuer direkte Render-Aufrufe"
affects:
  - "15-02 (Editor-Tab): buildRenderer() wird von Editor-Tab-Logik aufgerufen"
  - "15-03 (CSS): preview div erwartet die Container-Klassen aus diesem Modul"

tech-stack:
  added:
    - "markdown-it@14.2.0 (CDN via esm.sh, kein npm-install)"
    - "markdown-it-container@4.0.0 (CDN via esm.sh)"
    - "markdown-it-multimd-table@4.2.3 (CDN via esm.sh)"
  patterns:
    - "ESM-Import via esm.sh mit gepinnten Versionen fuer Single-File-HTML-Tools"
    - "scholarly_fixes als md.core.ruler.after('linkify') mit Token-API statt Post-Render-Regex"
    - "multimd vor allen container-Plugins registrieren (Pitfall 2)"

key-files:
  created: []
  modified:
    - "docs/public/qa_viewer.html"

key-decisions:
  - "scholarly_fixes als Token-API-Implementierung (md.core.ruler.after) statt Post-Render-Regex, um [[br]] in Tabellenzellen korrekt zu behandeln (Pitfall 4 aus RESEARCH.md)"
  - "html: true bewusst gesetzt und kommentiert -- Werkzeug ist ausschliesslich fuer Single-Author lokal"
  - "window.buildRenderer = buildRenderer am Ende des Modul-Blocks, damit der nicht-module Script-Block Zugriff erhaelt"
  - "Kein separater editor-renderer.js -- alles bleibt in qa_viewer.html (RESEARCH.md Architecture Patterns)"

patterns-established:
  - "Pattern: ESM-Import mit gepinnten Versionen in Single-File-HTML (alle drei Pakete auf exakten Versionen)"
  - "Pattern: Token-API fuer scholarly_fixes (html_inline Token fuer Devanagari-Spans)"

requirements-completed: [EDIT-01, EDIT-03, EDIT-04]

duration: 15min
completed: 2026-05-31
---

# Phase 15 Plan 01: buildRenderer-Modul Summary

**Client-seitiger Markdown-Renderer mit markdown-it 14.2.0 + allen 12 VitePress-Container-Plugins und scholarly_fixes via Token-API in qa_viewer.html eingebettet**

## Performance

- **Duration:** ~15 min
- **Started:** 2026-05-31T17:49:00Z
- **Completed:** 2026-05-31T18:04:39Z
- **Tasks:** 1
- **Files modified:** 1

## Accomplishments
- buildRenderer()-Funktion als `<script type="module">` in qa_viewer.html eingebettet und als window.buildRenderer exponiert
- Alle drei CDN-Imports mit gepinnten Versionen: markdown-it@14.2.0, markdown-it-container@4.0.0, markdown-it-multimd-table@4.2.3
- Registrierungsreihenfolge identisch zu config.mjs: prevent_br_link -> multimd -> 12 Container-Plugins -> scholarly_fixes
- scholarly_fixes als md.core.ruler.after('linkify') mit Token-API (korrekte [[br]]-Behandlung in Tabellenzellen, Pitfall 4)
- npm run docs:build besteht ohne Fehler

## Task Commits

1. **Task 1: buildRenderer-Modul in qa_viewer.html einbetten** - `cd361de` (feat)

**Plan metadata:** *(folgt in diesem Commit)*

## Files Created/Modified
- `docs/public/qa_viewer.html` - Neuer `<script type="module">`-Block mit buildRenderer(), scholarly_fixes, window.buildRenderer

## Decisions Made
- **Token-API statt Post-Render-Regex:** scholarly_fixes wurde als md.core.ruler.after('linkify') mit Token-API implementiert, nicht als Post-Render-Regex. Grund: Pitfall 4 aus RESEARCH.md -- [[br]] innerhalb von Tabellenzellen muss nach dem Block-Parsing behandelt werden, nicht davor.
- **html_inline Token fuer Devanagari:** Da html: true gesetzt ist, werden Devanagari-Spans und [[indent]]-Spans als html_inline-Token eingefuegt (direktes HTML, keine verschachtelten span_open/span_close Token). Das spiegelt das Verhalten der config.mjs-Implementierung auf Browserseite.
- **window.render als Convenience-Wrapper:** Zusaetzlich zu window.buildRenderer wurde window.render = (text) => buildRenderer().render(text) exponiert, damit nachfolgende Plaene die Funktion direkt aufrufen koennen.

## Deviations from Plan

Keine -- Plan wurde exakt wie beschrieben ausgefuehrt.

Die einzige implizite Entscheidung: Der Plan nennt `state.Token('span_open', ...)` als Ansatz fuer Devanagari-Spans (analog zu config.mjs). Da html: true gesetzt ist, ist `html_inline` ein saubererer Ansatz (kein Token-Nesting erforderlich, direktes HTML-String-Einbetten). Diese Variante ist funktional aequivalent und einfacher zu warten.

## Issues Encountered
- Worktree-Pfad-Isolation: Der erste Edit-Versuch schlug fehl, weil der absolute Pfad auf das Haupt-Repo zeigte statt auf den Worktree. Korrekt geloest durch Verwendung des Worktree-Pfads `/Volumes/SanDisk1TB/proj/Payer/.claude/worktrees/agent-ab43a3da68dea9076/docs/public/qa_viewer.html`.

## User Setup Required
Keine -- kein externer Dienst, kein npm install erforderlich.

## Next Phase Readiness
- window.buildRenderer() ist verfuegbar fuer Phase 15, Plan 02 (Editor-Tab-Integration)
- window.render() kann direkt fuer Smoke-Tests aufgerufen werden
- npm run docs:build ist gruen

## Self-Check: PASSED

- [x] docs/public/qa_viewer.html im Worktree existiert und enthaelt buildRenderer
- [x] Commit cd361de vorhanden
- [x] Alle 8 Pflichtstrings im automatisierten Check bestaetigt
- [x] npm run docs:build erfolgreich

---
*Phase: 15-vitepress-aware-markdown-editor*
*Completed: 2026-05-31*

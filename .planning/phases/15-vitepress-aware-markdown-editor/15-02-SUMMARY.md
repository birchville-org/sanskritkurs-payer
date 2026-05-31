---
phase: 15-vitepress-aware-markdown-editor
plan: 02
subsystem: ui
tags: [editor-tab, markdown-preview, debounce, qa-viewer, tab-switching]

requires:
  - "15-01 (buildRenderer): window.buildRenderer() muss verfuegbar sein"
provides:
  - "Editor-Tab als dritter Button in #view-controls (btn-editor)"
  - "textarea#editor-input mit editor-input Klasse (left-pane)"
  - "div#editor-preview mit editor-preview Klasse (right-pane)"
  - "setViewMode('editor') schaltet alle vier bestehenden Elemente aus und zeigt editor-input + editor-preview"
  - "renderPreview() ruft window.buildRenderer() lazy und setzt editorPreview.innerHTML"
  - "loadEditorContent() laedt Markdown der aktuellen Lektion per fetch() in die Textarea"
  - "Debounce 300ms auf editorInput via clearTimeout/setTimeout(renderPreview, 300)"
affects:
  - "15-03 (CSS): editor-preview erwartet VitePress-Container-Klassen fuer korrektes Styling"

tech-stack:
  added: []
  patterns:
    - "Lazy-Initialisierung von window.md via window.buildRenderer() beim ersten Editor-Aufruf"
    - "Debounce-Pattern via clearTimeout/setTimeout fuer Input-Events"
    - "fetch() zum Laden von Markdown-Quelldateien vom VitePress Dev-Server"

key-files:
  created: []
  modified:
    - "docs/public/qa_viewer.html"

key-decisions:
  - "window.md lazy initialisiert (nicht beim Seitenload) — buildRenderer() steht als ESM-Modul erst nach type=module-Block bereit; lazy-init vermeidet Race Condition"
  - "Kein Save-Button eingefuegt — CLAUDE.md Hard Rule: docs/lektionen/ sind unveraenderlich"
  - "editor-preview erhielt eigene CSS-Klasse (nicht raw-viewer), da Proportional-Font und Overflow-Styling benoetigt werden"
  - "DOMContentLoaded-Fallback fuer Event-Listener-Registrierung — Script laeuft im klassischen Script-Block, DOM bereits vorhanden; direktes Register sicherer"

requirements-completed: [EDIT-02, EDIT-05]

duration: 10min
completed: 2026-05-31
---

# Phase 15 Plan 02: Editor-Tab Summary

**Editor-Tab mit textarea-Input, Debounce-Rendering (300 ms) und Lesson-Preload per fetch() in qa_viewer.html eingebettet — dritter Button in #view-controls, vollstaendige Tab-Switching-Logik, lazy buildRenderer()-Initialisierung**

## Performance

- **Duration:** ~10 min
- **Started:** 2026-05-31T18:10:00Z
- **Completed:** 2026-05-31T18:20:00Z
- **Tasks:** 2
- **Files modified:** 1

## Accomplishments

- Dritter Button "Editor" im #view-controls btn-group eingefuegt (onclick="setViewMode('editor')")
- textarea#editor-input mit Klasse editor-input in #left-pane (display:none, eigene CSS-Klasse)
- div#editor-preview mit Klasse editor-preview in #right-pane (display:none, eigene CSS-Klasse)
- CSS-Regeln fuer .editor-input und .editor-preview im style-Block ergaenzt (Source Serif 4, CSS-Variablen)
- setViewMode() erweitert: editor-Modus blendet leftFrame, rightFrame, leftRaw, rightRaw aus
- renderPreview(): lazy window.md via window.buildRenderer(), innerHTML-Zuweisung an editorPreview
- loadEditorContent(): fetch() auf Markdown-URL der aktuellen Lektion, befuellt Textarea, ruft renderPreview()
- Debounce 300ms via clearTimeout/setTimeout auf editorInput
- npm run docs:build besteht ohne Fehler

## Task Commits

1. **Task 1: Editor-Button und HTML-Elemente** - `2951f7c` (feat)
2. **Task 2: Editor-Tab JavaScript-Logik** - `3ae1f86` (feat)

## Files Created/Modified

- `docs/public/qa_viewer.html` - Editor-Button, HTML-Elemente, CSS-Regeln, JS-Logik

## Decisions Made

- **Lazy window.md Init:** buildRenderer() ist in einem type=module-Block exponiert. Der nicht-module Script-Block laeuft synchron; window.buildRenderer koennte noch null sein wenn setViewMode('editor') sofort beim Seitenload aufgerufen wuerde. Lazy-Init in renderPreview() loest das Problem ohne komplexes Event-Ordering.
- **Kein Save-Button:** CLAUDE.md Hard Rule - docs/lektionen/ sind unveraenderlich. loadEditorContent() liest nur.
- **editor-preview als eigene CSS-Klasse:** raw-viewer hat monospace-Font und ist fuer Code gedacht. editor-preview braucht Proportional-Font und Overflow-Auto fuer gerendertes HTML.

## Deviations from Plan

**1. [Rule 2 - Missing] .editor-preview CSS-Regel ergaenzt**
- **Found during:** Task 1
- **Issue:** Der Plan spezifiziert CSS nur fuer .editor-input, nicht fuer .editor-preview. Ohne Styling wuerde der Preview-Div keinen sichtbaren Hintergrund und kein Padding haben.
- **Fix:** .editor-preview CSS-Regel mit display:none, width/height 100%, padding, background/color via CSS-Variablen ergaenzt.
- **Files modified:** docs/public/qa_viewer.html
- **Commit:** 2951f7c

**2. [Rule 2 - Missing] Fallback-Event-Listener-Registrierung**
- **Found during:** Task 2
- **Issue:** Der Plan sieht vor, den Input-EventListener "einmalig beim Script-Load" zu registrieren. Im klassischen Script-Block ist das DOM bereits vorhanden; direktes Registrieren mit _debounceRegistered-Flag verhindert Doppelanmeldung.
- **Fix:** IIFE mit _debounceRegistered-Guard fuer direkte Registrierung beim Script-Load.
- **Files modified:** docs/public/qa_viewer.html
- **Commit:** 3ae1f86

## Known Stubs

Keine - Editor-Tab ist funktional vollstaendig. Das Rendering haengt von window.buildRenderer() aus Plan 15-01 ab, das korrekt implementiert ist.

## Threat Flags

Keine neuen Trust Boundaries jenseits des Threat Models in PLAN.md (T-15-03: innerHTML-Zuweisung, T-15-04: fetch() same-origin).

## Self-Check: PASSED

- [x] docs/public/qa_viewer.html im Worktree enthaelt btn-editor, editor-input, editor-preview, renderPreview, loadEditorContent, editorDebounce, buildRenderer, setTimeout(renderPreview, 300)
- [x] Commit 2951f7c vorhanden
- [x] Commit 3ae1f86 vorhanden
- [x] npm run docs:build erfolgreich
- [x] Kein Save-Button, kein Schreiben auf docs/lektionen/

---
*Phase: 15-vitepress-aware-markdown-editor*
*Completed: 2026-05-31*

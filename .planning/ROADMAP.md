# Project Roadmap - Milestone v1.3

## Milestones

- ✅ **v1.0 Initial MVP** — Phasen 1-4 (shipped 2026-04-14)
- ✅ **v1.1 Interaktion & Flexibilität** — Phasen 5-9 (shipped 2026-04-19)
- ✅ **v1.2 Search, Index & I18n Expansion** — Phasen 10-14 (shipped 2026-05-27)
  - ⚠ Known gaps: BG (23/61), UK (31/61), RU Übungen (0/61) — handled out-of-band via lan_translate.py
- [ ] **v1.3 Polyglot & Polish** — Phasen 15-17

## Phasen

<details open>
<summary>📋 v1.2 Search, Index & I18n Expansion (Phasen 10-13)</summary>

### Phase 10: Search Optimization & Core Infrastructure
Fokus auf linguistischer Präzision und technischer Skalierbarkeit.
- [x] **Plan 10.1**: Implementierung von IAST-Folding und sprachspezifischer Suche.
- [x] **Plan 10.2**: Modularisierung der VitePress-Konfiguration (Locale-Splitting).
- **Erfolgskriterien**:
    - Suche nach "Sanskrit" findet "Saṃskṛta".
    - Konfiguration ist in separate Dateien pro Sprache aufgeteilt.

### Phase 11: Thematic Indexing & Navigation
Vertikale Erschließung der Inhalte durch Querverweise.
- [x] **Plan 11.1**: Aufbau des automatisierten Daten-Loaders für Frontmatter-Tags.
- [x] **Plan 11.2**: Erstellung der Themen-Register-Seite und der "Related Lessons" Komponente.
- **Erfolgskriterien**:
    - Eine zentrale Seite listet alle Lektionen nach Themen (z.B. Sandhi) auf.
    - Am Ende jeder Lektion erscheinen passende Themen-Vorschläge.

### Phase 12: I18n Expansion V1.3 — ES-Vervollständigung, Tamil (TA), Punjabi (PA)
Horizontale Erweiterung um drei neue Sprachen: ES vervollständigt (Übungen/Schriften), TA und PA neu.
**Plans:** 4 plans

- [x] **Plan 12.0**: GUI-Aktivierung — config.mjs, pa.mjs Locale, Verzeichnisstrukturen (2026-05-31).
- [ ] 12-1-PLAN.md — Übersetzungsabschluss: Vollständigkeitsprüfung und Nachhol-Jobs für ES/TA/PA
- [ ] 12-2-PLAN.md — Wortlisten und licenses.md für ES, TA, PA generieren
- [ ] 12-3-PLAN.md — QA: HTML-Bereinigung, Platzhalter-Suche, Layout-Synchronisation
- [ ] 12-4-PLAN.md — Build-Gate (npm run docs:build) und Git-Commit

- **Erfolgskriterien**:
    - ES: alle 61 Lektionen + 11 Schriften + 61 Übungen + wortliste verfügbar.
    - TA und PA: alle 61 Lektionen + 11 Schriften + 61 Übungen + wortliste verfügbar.
    - Homepage bietet 11 Sprachen zur Auswahl (DE, EN, IT, BG, RU, UK, HI, FR, ES, TA, PA).
    - Build: `npm run docs:build` erfolgreich.

### Phase 13: QA Infrastructure Restoration
High-fidelity restoration and standardization of the Sanskrit QA viewer.
- [x] **Plan 13.1**: Completed.
- **Erfolgskriterien**:
    - Viewer resolve routing 404s.
    - Strict visual parity with "Scholarly Synthesis" design.

### Phase 14: Lektion 27 Fidelity & Review
High-fidelity manual reconstruction and validation of Sanskrit Lesson 27.
- [x] **Plan 14.1**: Surgical correction of paradigm tables (27.7.12) and missing Devanāgarī.
- [x] **Plan 14.2**: Standardization of wordlist images and captions in 27.5.
- [x] **Plan 14.3**: Verification against original HTML and license auditing.
- **Erfolgskriterien**:
    - 1:1 structural parity with original L27 HTML.
    - Zero-HTML in all sections.
    - Paradigm tables correctly formatted with all script entries.

</details>

<details open>
<summary>📋 v1.3 Editor First (Phasen 15-17)</summary>

### Phase 15: VitePress-aware Markdown Editor ⭐ PRIORITY
Der Kern von v1.3: ein Split-Pane-Editor mit Live-Vorschau, der VitePress-Containersyntax korrekt rendert.
**Plans:** 4/4 plans complete

- [x] 15-01-PLAN.md — buildRenderer-Modul: markdown-it + alle 12 Container + scholarly_fixes in qa_viewer.html
- [x] 15-02-PLAN.md — Editor-Tab UI: Button, Textarea, Preview-Div, setViewMode, Debounce, Lesson-Preload
- [x] 15-03-PLAN.md — Container-CSS: alle Stile gescoped auf .editor-preview, Dark-Mode-Overrides
- [x] 15-04-PLAN.md — Integration & Build-Gate: [[br]]-Tabellen-Verifikation, visuelle QA, npm run docs:build

- **Erfolgskriterien**:
    - Editor rendert alle VitePress-Container 1:1 wie der Produktions-Build.
    - Änderungen sind sofort in der Vorschau sichtbar.
    - `[[br]]` und MultiMD-Tabellen werden korrekt dargestellt.

### Phase 16: I18n Completion — ES, LA, RM, TA (sekundär)
Horizontale Erweiterung um die verbleibenden vier Sprachen.
- [ ] **Plan 16.1**: Setup der Verzeichnisstrukturen für `/es/`, `/la/`, `/rm/`, `/ta/`.
- [ ] **Plan 16.2**: Massenübersetzung via AI (lan_translate.py → nyx.local:8000).
- [ ] **Plan 16.3**: Integration der neuen Locales in die VitePress-Config.
- [ ] **Plan 16.4**: Quality-Sync & Visual Remediation (Layout-Synchronisation via sync_layouts.py).
- **Erfolgskriterien**:
    - Alle 61 Lektionen sind in ES, LA, RM, TA verfügbar.
    - Die Homepage bietet 11 Sprachen zur Auswahl an.

### Phase 17: Scholarly Polish — Captions, Metadata & Comparison (sekundär)
Standardisierung der Metadaten und Legacy-Vergleichswerkzeug.
- [ ] **Plan 17.1**: Standardisierung aller Bildunterschriften (999.14) — minimalistisches Format.
- [ ] **Plan 17.2**: Audit und Vervollständigung der licenses.md.
- [ ] **Plan 17.3**: Historical Comparison Mode (999.12) — Side-by-Side Legacy-HTML vs Modern-Markdown.
- **Erfolgskriterien**:
    - Alle Bildunterschriften folgen dem L16-Ref Standard.
    - Vergleichsmodus über QA-Viewer erreichbar.

</details>

## Backlog

### Phase 999.10: Follow-up — Phase 10 incomplete plans (BACKLOG)

**Goal:** Resolve plans that ran without producing summaries during Phase 10 execution
**Source phase:** 10
**Deferred at:** 2026-04-26 during /gsd-next advancement
**Plans:**
- [x] 10-1: Infrastructure Cleanup (ran, no SUMMARY.md)
- [x] 10-2: Search Optimization (ran, no SUMMARY.md)
- [x] 10-3: Verification (ran, no SUMMARY.md)

### Phase 999.11: Follow-up — Phase 11 incomplete plans (BACKLOG)

**Goal:** Resolve plans that ran without producing summaries during Phase 11 execution
**Source phase:** 11
**Deferred at:** 2026-04-26 during /gsd-next advancement
**Plans:**
- [x] 11-1: Data Infrastructure (ran, no SUMMARY.md)
- [x] 11-2: Index Page (ran, no SUMMARY.md)
- [x] 11-3: UI Components (ran, no SUMMARY.md)
- [x] 11-4: Integration (ran, no SUMMARY.md)

### Phase 999.12: Historical Comparison Mode (Legacy vs Modern) (BACKLOG)

**Goal:** Integrate a toggleable side-by-side view for comparing legacy HTML sources with modern Markdown lessons.
**Requirements:** TBD
**Plans:** 0 plans

Plans:
- [ ] TBD (promote with /gsd-review-backlog when ready)
- [ ] **Global Logo Cleanup**: Remove `sanskritkurslogo.jpg` from all lesson Markdown files.

### Phase 999.13: VitePress-aware Markdown Editor (BACKLOG)

**Goal:** Build a QA-Viewer-style split-pane editor: left pane edits Markdown, right pane renders live preview with full VitePress-specific syntax support.
**Implementation Options:**
- **Option A (Web-based, preferred):** Standalone `/editor.html` page (like `qa_viewer.html`) with `<textarea>` or CodeMirror on the left; right pane uses client-side `markdown-it` + same plugins as `config.mjs` (`markdown-it-container`, `markdown-it-multimd-table`) for 1:1 preview parity. `[[br]]` substitution and CSS containers replicated client-side.
- **Option B (VS Code):** A dedicated extension that injects our `config.mjs` logic into the native Markdown preview.
**Notes from discussion:**
- Simple textarea + marked.js gives basic preview but misses VitePress-specific syntax.
- Accurate preview requires bundling the same markdown-it plugins used in `config.mjs` — feasible via CDN or small build step.
- Separate search per pane also discussed as a QA-viewer enhancement (see Phase 999.15).
**Requirements:** TBD
**Plans:** 0 plans

Plans:
- [ ] TBD (promote with /gsd-review-backlog when ready)

### Phase 999.14: Standardisierung aller Bildunterschriften (BACKLOG)

**Goal:** Umwandlung aller Bildunterschriften in das neue minimalistische Format (Kurze Caption + Link auf zentrale Lizenzseite) unter Berücksichtigung der korrekten Markdown-Syntax (Leerzeile nach Bild).
**Requirements:** TBD
**Plans:** 0 plans

Plans:
- [ ] TBD (promote with /gsd-review-backlog when ready)

## Progress

| Phase | Milestone | Plans | Status | Completed |
|-------|-----------|-------|--------|-----------|
| 1-4 | v1.0 | 4/4 | Complete | 2026-04-14 |
| 5-9 | v1.1 | 5/5 | Complete | 2026-04-19 |
| 10 | v1.2 | 2/2 | Complete | 2026-04-26 |
| 11 | v1.2 | 2/2 | Complete | 2026-04-26 |
| 12 | v1.2 | 4/4 | Complete | 2026-04-26 |
| 13 | v1.2 | 1/1 | Complete | 2026-05-08 |
| 14 | v1.2 | 3/3 | Complete | 2026-05-16 |
| 15 | v1.3 | 4/4 | Complete    | 2026-05-31 |
| 16 | v1.3 | 0/4 | Pending | — |
| 17 | v1.3 | 0/3 | Pending | — |

### Phase ${NEXT}: ${DESCRIPTION} (BACKLOG)

**Goal:** Develop or extend a Neovim plugin (Lua) to support the 'Winning Formula' for complex Sanskrit paradigms, including auto-alignment for || (colspan) and ^^ (rowspan) markers.
**Requirements:** TBD
**Plans:** 0 plans

Plans:
- [ ] Research existing table plugins (e.g., table-next.nvim) for extension points.
- [ ] Implement grid-aware alignment logic in Lua.
- [ ] (promote with /gsd-review-backlog when ready)

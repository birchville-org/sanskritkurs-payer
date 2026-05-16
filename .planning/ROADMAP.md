# Project Roadmap - Milestone v1.2

## Milestones

- ✅ **v1.0 Initial MVP** — Phasen 1-4 (shipped 2026-04-14)
- ✅ **v1.1 Interaktion & Flexibilität** — Phasen 5-9 (shipped 2026-04-19)
- [ ] **v1.2 Search, Index & I18n Expansion** — Phasen 10-12 (REPAIR REQUIRED)

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

### Phase 12: Multilingual Expansion (V1.2 Final)
Horizontale Erweiterung um IT, ES, BG sowie neu UK und RU.
- [x] **Plan 12.1**: Setup der Verzeichnisstrukturen für `/it/` und `/es/`.
- [x] **Plan 12.2**: Durchführung der Massenübersetzung via AI (UK & RU hinzugefügt).
- [x] **Plan 12.3**: Integration der neuen Locales in die VitePress-Config.
- [x] **Plan 12.4**: Quality-Sync & Visual Remediation (DE Struktur & Icons vereinheitlicht).
- **Erfolgskriterien**:
    - Alle 61 Lektionen sind in EN, IT, ES, BG, UK, RU verfügbar.
    - Die Homepage bietet alle 7 Sprachen zur Auswahl an.

### Phase 13: QA Infrastructure Restoration
High-fidelity restoration and standardization of the Sanskrit QA viewer.
- [x] **Plan 13.1**: Completed.
- **Erfolgskriterien**:
    - Viewer resolve routing 404s.
    - Strict visual parity with "Scholarly Synthesis" design.

### Phase 14: Lektion 27 Fidelity & Review
High-fidelity manual reconstruction and validation of Sanskrit Lesson 27.
- [ ] **Plan 14.1**: Surgical correction of paradigm tables (27.7.12) and missing Devanāgarī.
- [ ] **Plan 14.2**: Standardization of wordlist images and captions in 27.5.
- [ ] **Plan 14.3**: Verification against original HTML and license auditing.
- **Erfolgskriterien**:
    - 1:1 structural parity with original L27 HTML.
    - Zero-HTML in all sections.
    - Paradigm tables correctly formatted with all script entries.

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

**Goal:** Build or configure a Markdown editor that supports project-specific extensions like `::: grammar-box`, `^^` rowspans, and `{.sanskrit-dev}` for seamless content creation.
**Implementation Options:**
- **Option A (Web-based):** An integrated `/editor` page in VitePress using Monaco Editor + project-specific `markdown-it` plugins for 1:1 parity.
- **Option B (VS Code):** A dedicated extension that injects our `config.mjs` logic into the native Markdown preview.
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
| 14 | v1.2 | 0/3 | Planned | - |

### Phase ${NEXT}: ${DESCRIPTION} (BACKLOG)

**Goal:** Develop or extend a Neovim plugin (Lua) to support the 'Winning Formula' for complex Sanskrit paradigms, including auto-alignment for || (colspan) and ^^ (rowspan) markers.
**Requirements:** TBD
**Plans:** 0 plans

Plans:
- [ ] Research existing table plugins (e.g., table-next.nvim) for extension points.
- [ ] Implement grid-aware alignment logic in Lua.
- [ ] (promote with /gsd-review-backlog when ready)

# Phase 11: Thematic Indexing & Specialized Navigation - Plan

## Phase Goal
Implementierung eines automatisierten Themen-Registers und einer „Related Lessons“-Navigation basierend auf dem Scan von Überschriften.

## Requirements
- **INDEX-01**: Automatisches Themen-Register.
- **INDEX-02**: Related Lessons Komponente.
- **INDEX-03**: Scholarly Design (Premium Cards).

## Tasks

### Wave 1: Data Infrastructure
<task read_first="docs/.vitepress/config.mjs" acceptance_criteria="File docs/.vitepress/theme/data/topics.data.mjs exists. It extracts headings from German lessons correctly.">
<action>
Themen-Daten-Loader implementieren:
1. Verzeichnis `docs/.vitepress/theme/data/` erstellen.
2. `topics.data.mjs` erstellen:
   - Nutzt `createContentLoader` für `docs/lektionen/*.md`.
   - Extrahiert Überschriften als Schlagworte.
   - Filtert generische Begriffe (z.B. "Übung", "Lektion") aus.
   - Exportiert ein Mapping von Themen zu Lektionsnummern.
</action>
</task>

### Wave 2: Index Page
<task read_first="docs/grammatik.md" acceptance_criteria="File docs/themen.md exists (or grammatik.md is updated). It displays an automated, grouped list of topics.">
<action>
Themen-Register Seite erstellen:
1. Eine neue Seite `docs/themen.md` erstellen (oder die bestehende `grammatik.md` um eine automatisierte Sektion ergänzen).
2. Nutzt die Daten aus `topics.data.mjs`, um alle Schlagworte alphabetisch aufzulisten.
3. Jedes Schlagwort linkt auf die entsprechenden Lektionen.
</action>
</task>

### Wave 3: UI Components
<task read_first="docs/.vitepress/theme/components/PayerDocFooter.vue" acceptance_criteria="File docs/.vitepress/theme/components/PayerRelatedLessons.vue exists. It follows the AGENTS.md design system.">
<action>
RelatedLessons Komponente bauen:
1. `PayerRelatedLessons.vue` erstellen.
2. Design: Parchment-Background, Newsreader-Serif, Card-Layout.
3. Logik: Erkennt die aktuelle Lektion, sucht via `topics.data.mjs` nach Lektionen mit gleichen Überschriften/Themen.
4. Zeigt bis zu 3 Vorschläge als Karten an.
</action>
</task>

### Wave 4: Integration
<task read_first="docs/.vitepress/theme/index.mjs" acceptance_criteria="RelatedLessons component is visible at the bottom of lesson pages.">
<action>
Komponente in das Theme integrieren:
1. Registrierung der Komponente in `theme/index.mjs`.
2. Einbindung in das Layout (z.B. via `doc-footer-before` Slot oder direkt im `Layout.vue`).
</action>
</task>

## Verification Criteria
- [ ] Themen-Register zeigt automatisch generierte Schlagworte.
- [ ] Unter einer Lektion erscheinen passende Karten zu verwandten Themen.
- [ ] Das Design entspricht dem Scholarly-Look (AGENTS.md).
- [ ] Build läuft fehlerfrei durch.

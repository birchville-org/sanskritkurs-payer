# Phase 10: Search Optimization & Core Infrastructure - Plan

## Phase Goal
Vorbereitung der technischen Basis für Milestone v1.2 durch Modularisierung der Konfiguration und Optimierung der Suche für Sanskrit-Inhalte.

## Requirements
- **SRCH-01**: IAST Folding in MiniSearch.
- **SRCH-02**: Lokalisierung der Suche.

## Tasks

### Wave 1: Infrastructure Cleanup
<task read_first="docs/.vitepress/config.mjs" acceptance_criteria="File docs/.vitepress/locales/de.mjs exists. File docs/.vitepress/locales/en.mjs exists. docs/.vitepress/config.mjs is significantly smaller and imports locales.">
<action>
Modularisierung der VitePress-Konfiguration:
1. Verzeichnis `docs/.vitepress/locales/` erstellen.
2. `root` (DE) Konfiguration in `de.mjs` auslagern.
3. `en` Konfiguration in `en.mjs` auslagern.
4. `config.mjs` anpassen, um diese Dateien zu importieren.
5. `getSidebarItems` Logik so anpassen, dass sie weiterhin für alle Locales funktioniert (ggf. als Export in `config.mjs` behalten).
</action>
</task>

### Wave 2: Search Optimization
<task read_first="docs/.vitepress/config.mjs" acceptance_criteria="config.mjs contains search.options.miniSearch.options.processTerm hook. The hook implements diacritic folding.">
<action>
Sanskrit-optimierte Suche implementieren:
1. Implementierung der `normalizeSanskrit` Hilfsfunktion (wie in 10-RESEARCH.md beschrieben) in `config.mjs`.
2. Erweiterung der `themeConfig.search.options.miniSearch` Konfiguration.
3. Den `processTerm` Hook setzen, der `normalizeSanskrit` auf alle Begriffe (indiziert und gesucht) anwendet.
4. Sicherstellen, dass Devanāgarī-Zeichen durch die Normalisierung nicht beschädigt werden.
</action>
</task>

### Wave 3: Verification
<task read_first="docs/.vitepress/config.mjs" acceptance_criteria="Local dev server builds and runs. Search for 'Sanskrit' finds pages with 'Saṃskṛta'. Search for 'Lektion' finds German and English pages correctly.">
<action>
Verifizierung der Suche und Build-Stabilität:
1. `npm run docs:dev` starten.
2. Diverse Suchen durchführen:
   - "Sanskrit" -> findet "Saṃskṛta"
   - "Samkrta" -> findet "Saṃskṛta"
   - "Lektion" -> findet deutsche Lektionen
   - "Lesson" -> findet englische Lessons
3. Einen vollständigen Build mit `npm run docs:build` testen, um sicherzustellen, dass die modulare Config keine Probleme verursacht.
</action>
</task>

## Verification Criteria
- [ ] Build läuft ohne Fehler durch.
- [ ] Suche findet IAST-Begriffe ohne Diakritika.
- [ ] Sidebar-Navigation funktioniert in DE und EN weiterhin einwandfrei.
- [ ] Konfiguration ist modular in `locales/` aufgeteilt.

## must_haves
- [ ] Funktionierendes IAST-Folding.
- [ ] Modulare Konfigurations-Struktur.

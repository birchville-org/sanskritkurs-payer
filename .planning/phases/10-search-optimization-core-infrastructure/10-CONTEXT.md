# Phase 10: Search Optimization & Core Infrastructure - Context

**Gathered:** 2026-04-22
**Status:** Decided

<domain>
## Phase Boundary
Diese Phase legt das technische Fundament für Milestone v1.2. Sie optimiert die linguistische Suche (IAST/Devanāgarī) und modularisiert die Konfiguration für die anstehende Erweiterung auf IT und ES.

### Goals
- Implementierung eines aggressiven IAST-Folding (Diakritika-Normalisierung).
- Optimierung der Suche für native Devanāgarī-Zeichen.
- Modularisierung der VitePress-Konfiguration durch locale-spezifische Dateien.
</domain>

<decisions>
## Implementation Decisions

### 1. Search Strategy (Folding)
- **IAST Folding**: Aggressive Normalisierung auf Basis-ASCII (ś, ṣ, s → s; ā, a → a; ṛ, r → r; ṅ, ñ, ṇ, n → n etc.). Ziel ist maximale Auffindbarkeit für Nutzer mit Standard-Tastaturen.
- **Devanāgarī Search**: Native Zeichen sollen ebenfalls normalisiert/indiziert werden, um die Suche über verschiedene Skripte hinweg zu unterstützen.
- **Provider**: Nutzung des integrierten MiniSearch-Providers mit Custom `processTerm` Hook.

### 2. Infrastructure (Modularization)
- **Locale-Splitting**: Die `themeConfig` für jede Sprache wird in separate Dateien in `.vitepress/locales/` (z.B. `en.mjs`, `it.mjs`) ausgelagert.
- **Shared Logic**: Die `getSidebarItems` Logik bleibt zentral, wird aber so angepasst, dass sie die modularen Configs bedient.

### 3. Constraints
- **German Reference**: Die deutschen Seiten (`/lektionen/`, `/uebungen/`) sind die unveränderliche Referenz. Sie dürfen durch diese Phase (z.B. durch neue Metadaten-Felder, falls nötig) nicht in ihrem sichtbaren Inhalt verändert werden.
</decisions>

<canonical_refs>
## Canonical References

### VitePress & Search
- [docs/.vitepress/config.mjs](file:///Volumes/SanDisk1TB/proj/Payer/docs/.vitepress/config.mjs)
- [MiniSearch Documentation](https://lucaong.github.io/minisearch/modules/_minisearch_.html)

### Prior Context
- [.planning/phases/6/06-CONTEXT.md](file:///Volumes/SanDisk1TB/proj/Payer/.planning/phases/6/06-CONTEXT.md) (Locale Architecture)
</canonical_refs>

---
*Phase: 10-search-optimization-core-infrastructure*
*Context gathered: 2026-04-22*

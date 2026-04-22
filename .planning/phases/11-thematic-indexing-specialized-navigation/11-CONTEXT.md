# Phase 11: Thematic Indexing & Specialized Navigation - Context

**Gathered:** 2026-04-22
**Status:** Decided

<domain>
## Phase Boundary
Diese Phase implementiert das automatisierte Themen-Register und die „Related Lessons“-Navigation. Ziel ist eine intelligente Verknüpfung der Inhalte ohne manuellen Pflegeaufwand.

### Goals
- Automatisierte Extraktion von Themen aus den Überschriften der Lektionen.
- Erstellung einer dynamischen Index-Seite (Themen-Register).
- Implementierung einer „Related Lessons“-Komponente im Karten-Design.
</domain>

<decisions>
## Implementation Decisions

### 1. Topic Extraction Strategy
- **Source**: Schlagworte werden automatisch aus den Überschriften (`#`, `##`, `###`) der Lektionen extrahiert.
- **Reference Logic**: Da Schlagworte im Hintergrund einheitlich auf **Deutsch** bleiben sollen, nutzt der Indexer die deutschen Original-Dateien (`/docs/lektionen/*.md`) als Basis, um Themen zu identifizieren. Diese Themen werden dann auf die entsprechenden Dateien in anderen Sprachen gemappt.
- **Scope**: Es werden ausschließlich **Lektionen** (`lektion*.md`) indexiert. Übungen und Schrift-Einführungen sind ausgeschlossen.

### 2. UI & Interaction
- **Presentation**: Verwandte Lektionen werden am Ende jeder Seite in einem hochwertigen **Karten-Design (Premium Cards)** im „Scholarly Synthesis“-Stil angezeigt.
- **Index Page**: Die Register-Seite wird dynamisch generiert und gruppiert Lektionen nach den extrahierten Schlagworten.

### 3. Constraints
- **German Reference**: Die Themen-Identifikation basiert primär auf der deutschen Struktur.
- **No Manual Tags**: Es sollen vorerst keine manuellen `tags` im Frontmatter benötigt werden (Inhalts-Scan bevorzugt).
</decisions>

<canonical_refs>
## Canonical References

### VitePress Data Loading
- [VitePress createContentLoader](https://vitepress.dev/guide/data-loading#createcontentloader)

### Styling & Components
- [.planning/AGENTS.md](file:///Volumes/SanDisk1TB/proj/Payer/.planning/AGENTS.md) (Design System)
- [docs/.vitepress/theme/components/](file:///Volumes/SanDisk1TB/proj/Payer/docs/.vitepress/theme/components/) (Existing Components)
</canonical_refs>

---
*Phase: 11-thematic-indexing-specialized-navigation*
*Context gathered: 2026-04-22*

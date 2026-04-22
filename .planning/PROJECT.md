# Sanskritkurs Pipeline

## What This Is

Ein automatisiertes Produktionssystem (Static Site Generator Pipeline), das bestehende und neue Sanskrit-Lektionen in eine moderne Dokumentations-Website umwandelt. Das System kombiniert das Leseverhalten professioneller technischer Dokumentationen (Sidebar, Full-Text-Search, On-this-page-Navigation) mit warmen, lesefreundlichen Serif-Farbschemata.

## Core Value

Perfekte typografische Darstellung von Sanskrit/Devanāgarī eingebettet in eine blitzschnelle, übersichtliche und voll durchsuchbare Struktur, die als einfache Pipeline vollautomatisch neue Kapitel integrieren kann.

## Current Milestone: v1.2 Search, Index & I18n Expansion

**Goal:** Tiefergehende Erschließung der Inhalte durch Indizes und Suche sowie Ausbau der internationalen Präsenz (IT/ES).

**Target features:**
- **Thematische Indizes**: Aufbau eines Querverweis-Systems für grammatikalische Begriffe.
- **Erweiterte Suche**: Optimierung für Devanāgarī und IAST-Transliterationen.
- **Mehrsprachigkeit (IT/ES)**: Integration von Italienisch und Spanisch inklusive automatisierter Übersetzung.
- **Multimedia-Pilot**: *Verschoben auf v1.3+*

## Requirements

### Validated

- ✓ **Konverter & Import** — v1.0
- ✓ **Bild-Übernahme** — v1.0
- ✓ **Lizenz-Audit** — v1.0
- ✓ **Typografie & Unicode** — v1.0
- ✓ **Navigation & Seitenstruktur** — v1.0
- ✓ **Theme & Design** — v1.0
- ✓ **Volltextsuche** — v1.0
- ✓ **Deployment-Mechanismus** — v1.0
- ✓ **Quiz-Komponenten (L10N)** — v1.1
- ✓ **i18n Setup (DE/EN)** — v1.1
- ✓ **Grammar Exercise Translation (1-60)** — v1.1
- ⚠ **Wide-Mode (Layout Toggle)** — Discarded in v1.1 in favor of standard responsive layout.

### Active

- [ ] **Thematische Indizes** (INDEX-01): Aufbau einer Querverweis-Struktur für grammatikalische Begriffe.
- [ ] **Devanāgarī-Suche** (SRCH-01): Optimierung der Suchfunktion für transliterierte und native Zeichen.
- [ ] **Internationalisierung IT/ES** (I18N-02): Setup und Übersetzung für Italienisch und Spanisch.

### Key Decisions & Constraints

- **German Reference**: Die deutschen Seiten (`/lektionen/`, `/uebungen/`) gelten als unantastbare Referenz und dürfen durch automatisierte Prozesse (Übersetzung, Refactoring) nicht verändert werden.
- **SSG-Fokus**: Das System bleibt ein statischer Generator (VitePress).

## Evolution

This document evolves at phase transitions and milestone boundaries.

**After each phase transition** (via `/gsd-transition`):
1. Requirements invalidated? → Move to Out of Scope with reason
2. Requirements validated? → Move to Validated with phase reference
3. New requirements emerged? → Add to Active
4. Decisions to log? → Add to Key Decisions
5. "What This Is" still accurate? → Update if drifted

**After each milestone** (via `/gsd-complete-milestone`):
1. Full review of all sections
2. Core Value check — still the right priority?
3. Audit Out of Scope — reasons still valid?
4. Update Context with current state

---
*Last updated: 2026-04-22 after v1.2 milestone start*

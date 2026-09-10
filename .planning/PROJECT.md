# Sanskritkurs Pipeline

## What This Is

Ein automatisiertes Produktionssystem (Static Site Generator Pipeline), das bestehende und neue Sanskrit-Lektionen in eine moderne Dokumentations-Website umwandelt. Das System kombiniert das Leseverhalten professioneller technischer Dokumentationen (Sidebar, Full-Text-Search, On-this-page-Navigation) mit warmen, lesefreundlichen Serif-Farbschemata.

## Core Value

Perfekte typografische Darstellung von Sanskrit/Devanāgarī eingebettet in eine blitzschnelle, übersichtliche und voll durchsuchbare Struktur, die als einfache Pipeline vollautomatisch neue Kapitel integrieren kann.

## Current Milestone: v2.0 WebGPU KI-Suche (Semantic RAG)

**Goal:** Lokale, offline-fähige semantische Suche und LLM-Antwortgenerierung im Browser via WebGPU und statischer Embedding-Pipeline.

**Target features:**
- **Static Embedding Pipeline** (Phase 24): Vektorisierung aller Lektionen beim VitePress Build.
- **Client-side Semantic Search** (Phase 25): Vektorähnlichkeitssuche per Web Worker im Browser.
- **WebGPU LLM Answer Generation (RAG)** (Phase 26): On-Device Chat & Zitate via Web-LLM (Gemma 2B).
- **Provider-Pattern & Model Management** (Phase 27): Fallback auf API (OpenRouter) & Opt-in Model-Download.

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
- ✓ **Thematische Indizes** (INDEX-01) — v1.2
- ✓ **Devanāgarī-Suche** (SRCH-01) — v1.2
- ✓ **Internationalisierung IT/ES/BG/UK/RU** — v1.2
- ✓ **Markdown Editor** (EDIT-01) — v1.3
- ✓ **Offline-First PWA** — v1.4
- ✓ **QA-Modus-Split** — v1.5
- ✓ **Developer Experience & VSCode Extension** — v1.6
- ✓ **Key Locales (EN, RU) 100% Completion** — v1.7
- ✓ **Polyglot 100% Completion (48 Zielsprachen, 0 Fallbacks)** — v1.8 (v1.8.3)
- ✓ **Autonomous Healer Pipeline & Multi-Arch Container** — v1.8 (v1.8.3)

### Active

- [ ] **Static Embedding Pipeline** (SRCH-02): Vektorisierung aller Markdown-Lektionen während des VitePress-Builds.
- [ ] **Client-side Semantic Search** (SRCH-03): Semantisches Matching im Browser via Web Worker.
- [ ] **WebGPU LLM Answer Generation** (RAG-01): On-Device RAG-Antwortgenerierung mit Gemma 2B IT.
- [ ] **Provider-Pattern & Model Management** (RAG-02): Hybrid-Architektur (WebGPU / OpenRouter API) mit Opt-In Caching.

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

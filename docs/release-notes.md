---
layout: doc
title: Release Notes & Version History
description: Overview of updates, new features, and technical enhancements in Sanskritkurs.
---

# Release Notes & Version History

Overview of releases, new features, and technical optimizations in the Sanskritkurs platform.

## 🚀 Version 1.8.5 (September 2026)

**Focus:** *QA Viewer & Editor Architecture, Navigation Parity across 38 Locales, Staging CI/CD Infrastructure & Nordic Polish*

### ✨ Features & Highlights
- **Interactive QA Viewer & Editor Preview Overhaul**:
  - Fully restored table borders and cell styling in the live preview for multimd tables, headerless tables, and compact tables.
  - Repaired SVG alert icons in editor preview and fixed CSS isolation for `.editor-preview`.
  - Smart `END QA` exit routing: returns directly to the active language homepage or origin lesson instead of hardcoded German root.
  - Robust initial context detection supporting URL parameters (`?lang=...&lesson=...`), document referrer, and local storage state.
- **Universal Navbar Parity & Dynamic Link Synchronization**:
  - Standardized the navbar `QA` label across all 38 locale configurations (`docs/.vitepress/locales/*.mjs`), eliminating mistranslations and ensuring full navbar visibility.
  - Proactive link synchronization in `theme/index.mjs` ensuring all QA links carry the current language and lesson context on mount, route transitions, and user interactions.
- **Nordic Localization & Structural Heading Convergence**:
  - Comprehensive localization and navigation cleanup across Norwegian (`no`), Swedish (`sv`), Icelandic (`is`), and Danish (`da`).
  - Strict enforcement of target-language headings in the translation pipeline and QA gate, purging residual untranslated headings.
- **CI/CD & Staging Server Resilience**:
  - Decoupled staging deployments into persistent containers managed via systemd user services on `nataraja`, guaranteeing zero downtime during builds.
  - Optimized container lifecycle, port collision protection, and nginx clean-URL routing configuration.
- **Parser & Syntax Robustness**:
  - Normalized signal-red syntax (`:sig[...]`) with parser auto-recovery for missing leading colons.
  - Updated container nesting documentation in `docs/public/qa_help.md`.

---

## 🚀 Version 1.8.4 (September 2026)

**Focus:** *100% Quality Convergence across All 48 Target Languages, Stopword Calibrations & Release Sync Automation*

### ✨ Features & Highlights
- **100.0% Complete Sanskrit Translation across All 48 Locales**: Healed, verified, and locked the entire 140-lesson corpus across the final wave of languages (`cs`, `hy`, `da`, `af`, `si`, `am`, `sv`, `sl`, `zu`, `fa`, `gez`, `et`). All 48 target languages now stand at 140/140 clean files (6,720 localized files, 0 fallbacks, 0 pipeline queue).
- **QA & Stopword Calibrations**: Refined the QA false-positive detection filters in `scripts/translation_qa.py` for target-language native words colliding with German stopwords (e.g. Afrikaans pronoun/article `die`, Danish articles `der`/`den`).
- **Autonomous Healing Normalizations**: Extended script validation and structural header/caption normalizations for Amharic (`am`) and Persian (`fa`) in `scripts/autonomous_healer.py`.
- **Automated Locale Version Synchronization**: Integrated `scripts/bump_version.py` into the core verification gate, guaranteeing that version metadata across all 49 index and settings pages stays perfectly synchronized with `package.json`.

---

## 🚀 Version 1.8.3 (September 2026)

**Focus:** *100% Completion Milestone across 48 Target Languages, Addition of Estonian & isiZulu, Autonomous Healing Architecture*

### ✨ Features & Highlights
- **100% Completion Milestone (0 Fallbacks)**: All 48 supported target languages (`en`, `it`, `es`, `fr`, `ru`, `uk`, `rm`, `ar`, `fi`, `ta`, `pa`, `la`, `id`, `th`, `hi`, `el`, `grc`, `ro`, `he`, `hu`, `zh-CN`, `am`, `pt`, `af`, `nl`, `fa`, `lt`, `sh`, `sq`, `bg`, `zh`, `tr`, `vi`, `pl`, `cs`, `sk`, `sl`, `ka`, `hy`, `si`, `te`, `da`, `no`, `sv`, `is`, `gez`, `et`, `zu`) have achieved 100.0% completion without fallbacks (140/140 files clean each, totaling 6,860 clean localized markdown files).
- **Estonian (`et`) Addition**: Integrated, localized, and fully translated with native Estonian grammar conventions (`# Harjutus`, `Pildi allikas:`, `Joonis:`).
- **isiZulu (`zu`) Addition**: Integrated, localized, and fully translated with native isiZulu grammar conventions (`# Isivivinyo`, `Umthombo wesithombe:`, `Umfanekiso:`).
- **Ge'ez (`gez`) & Bulgarian (`bg`) Completion**: Ge'ez (`gez`) healed and verified to 100% with Ethiopic script integrity; Bulgarian (`bg`) fully restored and validated.
- **Autonomous Multi-Worker Healer Pipeline**: Production deployment of `scripts/autonomous_healer.py` with multi-process safe PID isolation, forward/reverse bidirectional queue resolution, and strict Lingua verification gates (`is_file_fallback`).
- **Repository Optimization**: Streamlined project scope by purging non-viable ancient and dialectal corpora (`cop`, `akk`, `arc`, `gsw`), focusing computational and philological resources exclusively on supported living languages.
- **Full QA-Viewer & Navigation Parity**: Interactive QA Viewer (`docs/public/qa_viewer.html`) and VitePress configuration updated to full 49-locale parity with dynamic sidebar and theme generation.

---

## 🚀 Version 1.7.0 (August 2026)

**Focus:** *100% Completion in Key Target Locales, Offline-First PWA & UI Polish*

### ✨ Features & Highlights
- **100% Completion without Fallbacks**: English (`en`) and Russian (`ru`) locales are 100% clean translated (136/136 files, 0 fallbacks) and write-locked.
- **Full UI Localization (SSOT)**: All navigation and control elements (Previous/Next Lesson, Exercises, Table of Contents) are dynamically served across all active locales from a single source of truth.
- **Typography & Quality Assurance**: Upright Devanāgarī typography without italic distortion, unentangled signal-red tags, and sanitized prose across all completed language versions.
- **PWA & Offline-First**: Complete offline capability for all course content across active language versions.
- **Design & Layout**: Refined Hero presentation and feature card layouts without unwanted top divider lines.

---

## 🛠 Version 1.6.1 (July 2026)

**Focus:** *QA-Viewer Parity & Sidebar Integrity*

- **QA-Viewer Synchronization**: `#left-lang` and `#right-lang` in `qa_viewer.html` match `config.mjs` locales exactly.
- **Sidebar Grouping**: Fixed nesting regressions in lesson and chapter overviews.
- **Container Syntax**: Rigorous validation and enforcement of nested `grammar-box` containers.

---

## ⚙️ Version 1.6.0 (July 2026)

**Focus:** *Surgical Fallback Repair & System Stability*

- **Surgical Fallback Logic**: Automatic block-by-block re-translation of incomplete chunks.
- **Integrity Checks**: Automated pre-push build gate to prevent corrupted markdown files from entering the repository.
- **Wordlists & Glossary**: Complete synchronization of all wordlists and terminology definitions across modular libraries.

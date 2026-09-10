---
layout: doc
title: Release Notes & Version History
description: Overview of updates, new features, and technical enhancements in Sanskritkurs.
---

# Release Notes & Version History

Overview of releases, new features, and technical optimizations in the Sanskritkurs platform.

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

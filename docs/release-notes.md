---
layout: doc
title: Release Notes & Version History
description: Overview of updates, new features, and technical enhancements in Sanskritkurs.
---

# Release Notes & Version History

Overview of releases, new features, and technical optimizations in the Sanskritkurs platform.

## 🚀 Version 1.10.0 (Oktober 2026)

**Focus:** *Integration der 18. aktiven Sprache (Telugu / te-IN), vollständiges Telugu-Glossar (778 Einträge), Single Source of Truth für Topics-Data & Bereinigung von Footer- und Language-Settings-Komponenten*

### ✨ Features & Highlights
- **Datenintegrität & Kernfunktionen**:
  - **18. aktive Sprache (Telugu / te-IN)**: Vollständige Übersetzung und Freischaltung des gesamten Sanskritkurses in Telugu (61 Lektionen, 57 Übungsdateien, 11 Schriftlektionen, Inhaltsverzeichnis und Wortliste).
  - **Telugu-Glossar (`docs/te/lektionen/glossar.md`)**: Automatisierte Generierung von 778 Glossareinträgen mit doppelter Schriftführung (IAST und Telugu-Skript via `indic_transliteration`).
  - **Themenübersicht Telugu (`docs/te/themen.md`)**: Vollständige Lokalisierung der grammatischen Indexseite auf Telugu (`వ్యాకరణ పట్టిక`).
  - **VitePress-Locale-Integration**: Vollständige Konfiguration von `docs/.vitepress/locales/te.mjs`, Aufnahme in `ACTIVE_LOCALES` und Anbindung an den QA-Viewer (`qa_viewer.html`).
- **Performance & Rendering**:
  - **Komponenten-Refactoring `PayerDocFooter.vue`**: Ersetzung einer 170-zeiligen `if / else if`-Kaskade durch ein kompaktes, deklaratives `TITLE_TERMS`-Lookup-Objekt mit nativer `.replaceAll()`-Logik. Ergänzung von Telugu (`te`) und Tschechisch (`cs`); Entfernung ausgeschlossener antiker Sprachen (`arc`, `cop`).
  - **Single Source of Truth für Topic-Indizes**: Veraltete, hartcodierte Locales-Listen in `topics.data.js`, `PayerTopicIndex.vue` und `PayerRelatedLessons.vue` durch den direkten Import von `ACTIVE_LOCALES` aus `languages.mjs` ersetzt.
- **Sicherheit & Sandbox**:
  - **Language-Settings-Bereinigung**: Vollständige Lokalisierung für Telugu und Tschechisch in `PayerLanguageSettings.vue`. Entfernung von totem Feedback-Code und ungenutzten Fallbacks.
  - **Link-Konsistenz**: Korrektur interner Dokumentationslinks in `settings.md` auf kanonische Pfade.
- **Plattform- & Backend-Stabilität**:
  - **SSG-Manifest-Generierung**: Saubere Einbindung von `manifest-te.json` mit 142 generierten URLs im VitePress-Postbuild.
  - **Pre-Push-Verifikation**: Erfolgreiche Validierung aller 18 aktiven Sprachversionen gegen strikte QA- und Translation-Memory-Kriterien.

---

## 🚀 Version 1.9.1 (Oktober 2026)

**Focus:** *82% Asset- & Build-Footprint Reduction, 17 Published Core Locales with Contact Dispatch, Open Graph Mail Capsules & Local Storage Sanitization*

### ✨ Features & Highlights
- **Performance & Rendering**:
  - **82.4 % Footprint-Reduktion des SSG-Builds**: Bereinigung des `dist/`-Umfangs von 709 MB auf ca. 125 MB zur Ermöglichung des vollständigen Hostings auf GitHub Pages und CDNs.
  - **QA-Viewer WebP-Migration**: Konvertierung der unkomprimierten Lektionsscans und Devanāgarī-Tafeln von PNG auf hochoptimiertes WebP (von 33 MB auf 6 MB komprimiert).
  - **Vektor-Suchindex-Optimierung**: Kompaktierung der Minisearch-Indizes auf die publizierten Kernsprachen.
- **Datenintegrität & Kernfunktionen**:
  - **Fokussierung auf 17 publizierte Kernsprachen**: Veröffentlichung von Deutsch (DE), Englisch (EN), Französisch (FR), Italienisch (IT), Rumantsch (RM), Spanisch (ES), Neugriechisch (EL), Tschechisch (CS), Hindi (HI), Tamil (TA), Arabisch (AR), Hebräisch (HE), Russisch (RU), Ukrainisch (UK), Indonesisch (ID), Vereinfachtes Chinesisch (zh-CN) und Traditionelles Chinesisch (ZH).
  - **Kontakt-Hinweis im Language-Settings-Modal**: Anzeige des Hinweises „Für weitere Sprachen bitte webmaster@birchville.org kontaktieren“ für unpublizierte Sprachen.
  - **Open Graph & Apple Mail Kapseln**: Kompakte Open Graph Icons und standardisierte Meta-Tags für saubere Vorschauen in Mail-Clients und Messenger-Diensten.
- **Sicherheit & Sandbox**:
  - **LocalStorage-Härtung**: Automatische Bereinigung veralteter oder unpublizierter Sprachauswahlen aus dem lokalen Browser-Speicher (`localStorage`).
  - **XSS-Prävention**: Renderung der Hinweistexte im Sprach-Modal über native Text-Nodes ohne `v-html`.
  - **Strenges URL-Parsing**: Exakte Segment-Erkennung für regionale Sprachcodes (`zh-CN`).
- **Plattform- & Backend-Stabilität**:
  - **Saubere Artefakt-Generierung**: Ausschluss unkompilierter Roh-Markdown-Dateien aus den Ausgabeverzeichnissen in `dist/`.
  - **Tschechische (CS) Navigation**: Lückenlose Sidebar- und Navigationsanbindung für Tschechisch.

---

## 🚀 Version 1.8.14 (Oktober 2026)

**Focus:** *Scholarly Synthesis v2 Box System Migration (6,392 Files), Container Taxonomy Consolidation, markdown-it-extensible 1.4.0 & Native Navbar Restoration*

### ✨ Features & Highlights
- **Scholarly Synthesis v2 Boxensystem (6.392 Dateien)**:
  - Vollständige Migration aller 61 Lektionen, 57 Übungsdateien, 11 Schriftlektionen, Inhaltsverzeichnisse und Wortlisten über Deutsch und alle 46 aktiven Zielsprachen auf das konsolidierte 6-Container-Minimal-Set (`grammar-box`, `warning-box`, `note-box`, `verse-box`, `indent`, `media`) gemäss `docs/METHODIK_BOXENSYSTEM.md`.
  - 100 % Text- und Segmenterhalt über alle 6.392 Dateien (verifiziert durch automatisches Diff-Gate), sodass sämtliche bestehenden Übersetzungen und das Translation Memory unverändert gültig bleiben.
  - Sprachübergreifende Entflechtung von Regelschemata und Beispielen (`::: grammar-box` + `::: indent`) sowie Bereinigung historischer Container- und Blockquote-Artefakte (`scripts/transform_lang_v2.py`).
- **Typografie, Renderer & QA-Viewer (`markdown-it-extensible@1.4.0`)**:
  - Einführung von `::: warning-box` (Scholarly Terracotta `#ea580c`) als Ersatz für das violette `::: important`-Verkehrsschild sowie `::: verse-box` für Ślokas, Mantras und metrische Schemata.
  - Abwärtskompatibles Aliasing für Legacy-Container (`important` -> `warning-box`, `literatur-box` -> `note-box`, `compact` -> `verse-box`) in `docs/.vitepress/config.mjs` und `docs/public/qa_viewer.html`.
  - Aktualisierung der CodeMirror-6-Container-Dekorationen, Snippet-Toolbar und Kurzreferenz (`docs/public/qa_help.md`).
- **Navigation & Portal**:
  - Wiederherstellung der nativen VitePress-Top-Navigation und Entfernung des redundanten Hamburger-Menüs (`BirchvilleNavDrawer`).
  - Ausrichtung des Dokumentationsportals (`site_docs/`) am Birchville Scholarly Synthesis Standard mit Curation Badge und Quick-Access Grid.

---

## 🚀 Version 1.8.13 (Oktober 2026)

**Focus:** *Universal Slide-Over Navigation Drawer, Birchville Scholarly Synthesis Design Tokens, markdown-it-extensible 1.3.2 Security & Nesting Protection*

### ✨ Features & Highlights
- **Universal Slide-Over Navigation Drawer**:
  - Neuer interaktiver Slide-Over Drawer (`BirchvilleNavDrawer.vue`) für nahtlose Navigation auf Desktop- und Mobilgeräten.
  - Vollständiges Fokus-Management (Fokus-Trap-Vermeidung via `:inert`, `visibility: hidden`, `role="dialog"`, `aria-modal="true"` und automatischer Fokus-Rückstellung auf den Menü-Toggle).
  - Schneller Direktzugriff auf Kurs-Inhaltsverzeichnis, Grammatik-Systematik, Wortliste, QA-Viewer und Birchville-Netzwerk-Ressourcen.
- **Birchville „Scholarly Synthesis“ Standard**:
  - Integration der standardisierten Design-Tokens und Frosted-Glass-Header (`backdrop-filter: blur(14px)`).
  - Dezent eingebundenes Birchville-Wappen (`/birchville_logo.png`) im Header und Drawer-Kopf.
  - Theme-adaptive Gestaltung für Light Mode (Warm Ivory & Deep Ink) und Dark Mode (Illuminierte Handschrift bei Kerzenlicht).
- **Sicherheits- & Parser-Härtungen (`markdown-it-extensible@1.3.2`)**:
  - Konsequenter XSS-Schutz durch HTML-Escaping bei benutzerdefinierten Container-Titeln.
  - Attribut- und Tag-Injection-Schutz für alle Block-Container und Inline-Direktiven.
  - Nesting-Stack-Schutz (`nesting.js`): Unbekannte Container schließen übergeordnete Blöcke nicht mehr vorzeitig.
  - Robuste Regex-Prävention gegen Falsch-Positive bei Zeitangaben und URLs.
- **Dokumentation & Portal-Verlinkung**:
  - Aktualisierung der Repository- und Issue-Links auf die GitHub Organization `birchville-org`.
  - Prominente Direktverlinkungen auf Online-Kurs, Portal und Homelab im README.

---

## 🚀 Version 1.8.12 (Oktober 2026)

**Focus:** *CodeMirror 6 Editor-Migration, Footnote & Deflist Rendering, Silent Auto-Repair State Preservation*

### ✨ Features & Highlights
- **QA-Viewer Editor-Upgrade (CodeMirror 6)**:
  - Vollständige Migration von CodeMirror 5 (CDN) auf ein performantes lokales CodeMirror 6 Bundle (`docs/public/qa_editor.js`, esbuild).
  - Native CM6 StateFields und dynamische Dekorationen für Container-Verschachtelungen (`::: grammar-box` etc.).
  - Zeilennummern-Offsetting, Vim-Keymap-Compartment und entkoppelte Editor-Lifecycle-Verwaltung.
- **Wissenschaftliche Fußnoten & Definitionslisten**:
  - Integration von `markdown-it-footnote` und `markdown-it-deflist` im VitePress-Build (`config.mjs`) sowie im clientseitigen QA-Viewer-Renderer (`qa_viewer.html`).
  - Scoped CSS-Styles für `.footnotes`, `.footnote-backref`, `<dt>` und `<dd>` im Light- und Dark-Theme.
- **Silent Auto-Repair State-Preservation**:
  - Nahtloser Erhalt von Cursor-Position (`selection`) und Scroll-Zustand (`scrollDOM`) beim automatischen Bereinigen von Tabellen- und Container-Syntax während des Speicherns.
- **Dokumentation & Stabilität**:
  - Aktualisierung der Schnellsyntax-Referenz in `docs/public/qa_help.md`.

---

## 🚀 Version 1.8.11 (Oktober 2026)

**Focus:** *markdown-it-extensible 1.3.0 Integration & Container Nesting Normalization*

### ✨ Features & Highlights
- **Container Nesting Normalization (`markdown-it-extensible@1.3.0`)**:
  - Automatisches Umschreiben von Container-Hierarchien bei verschachtelten Boxen (`autoNesting`), sodass äussere Boxen strikt mehr Doppelpunkte als innere Boxen besitzen.
  - Verhindert das vorzeitige Schliessen von Eltern-Containern bei gleichartigen Doppelpunkt-Fences.
  - Beseitigung von Child-Margin-Stacking (`margin-top: 0` auf `:first-child`, `margin-bottom: 0` auf `:last-child`) für alle Container-Typen bei titellosen Boxen.
  - Vollständige Unterdrückung leerer Titelklammern (`[]`) und leerer Paragraphen (`p:empty`) innerhalb von Containern.
- **Bereinigung**:
  - Entfernung des veralteten, ungenutzten lokalen Verzeichnisses `packages/vitepress-plugin-scholarly`.

---

## 🚀 Version 1.8.10 (September 2026)

**Focus:** *Documentation Portal & GitHub Pages Deployment (`mkdocs-material` & `mkdocs-static-i18n`), Bilingual System Architecture & Pipeline Guides*

### ✨ Features & Highlights
- **Official Documentation Portal on GitHub Pages**:
  - Deployed bilingual project documentation portal (DE/EN) to [birchville-org.github.io/sanskritkurs-payer](https://birchville-org.github.io/sanskritkurs-payer/) analogous to `AlexandriaSandwich` and `boethlingk`.
  - Configured MkDocs with Material theme (`blue grey` / `teal`), responsive tabs, search, and language switching.
  - Isolated documentation directory in `site_docs/` to prevent interference with the VitePress interactive course.
- **Bilingual Technical Guides**:
  - Comprehensive documentation covering Distributed 3-Node Topology (`nike.local`, `nyx.local`, `nataraja.local`), Mermaid system diagrams, and Concurrency constraints.
  - Detailed specifications of Weg B AI translation pipeline, cryptographic TM caching, and Devanāgarī protection filters.
  - Quantitative benchmark analysis (248.3 GPU hours) and Three-Tier Exclusion Framework.
  - PWA architecture, language-partitioned caching, and Docker/Desktop deployment guides.
- **Automated CI/CD Workflow**:
  - Added `.github/workflows/docs.yml` for automated MkDocs builds and deployment to the `gh-pages` branch upon pushes to `main`.

---

## 🚀 Version 1.8.9 (September 2026)

**Focus:** *Container Parser Hardening (`markdown-it-extensible@1.2.2`), QA Viewer Editor-Preview Parity & Cross-Platform Build Optimizations*

### ✨ Features & Highlights
- **Container Prefix Collision Resolution (`grammar-box2`)**:
  - Eliminated a critical parsing collision in `markdown-it-extensible` where prefix containers (e.g. `grammar-box`) intercepted and falsely consumed more specific containers (e.g. `grammar-box2`).
  - Hardened container matching regex (`^\s*${box}(?:\s+(.*)|(?=\[)(.*))?$`) and enforced longest-first container registration order.
  - Upgraded project dependencies to `markdown-it-extensible@1.2.2` and aligned `qa_viewer.html` and `docs/.vitepress/config.mjs`.
  - Refined editor preview CSS for `.grammar-box2` in `qa_viewer.html` (font-weight normalization, title hiding parity with `custom.css`).
- **Build & Desktop Optimization**:
  - Enhanced Windows cross-platform compatibility for translation lock management (`lock.py`) and git pre-push hooks.
  - Streamlined desktop distribution build with selective VitePress compilation.

---

## 🚀 Version 1.8.8 (September 2026)

**Focus:** *Multi-Locale Glossary IAST Repair & Generator Hardening, Bulgarian Navigation Polish & Sidebar Deduplication*

### ✨ Features & Highlights
- **Universal Sanskrit Glossary IAST Column Repair across All 43 Locales**:
  - Hardened `scripts/gen_glossar.py` to enforce `indic_transliteration` with a fail-fast runtime check, preventing silent degraded executions without transliteration libraries.
  - Eliminated the fallback bug where missing IAST romanizations dumped raw Devanagari text into the IAST table column (`iast = deva_to_iast(deva) or ""`).
  - Batch-regenerated all 43 localized glossaries (`docs/*/lektionen/glossar.md`), fixing over 27,000 table rows: every lemma now renders valid IAST romanization linked to the Cologne Monier-Williams Sanskrit-English Dictionary (`https://www.sanskrit-lexicon.uni-koeln.de/...`).
  - Enhanced configuration handling in `gen_glossar.py` to automatically detect and preserve localized page titles and table column headers across all target languages.
  - Safeguarded the German master source (`docs/lektionen/glossar.md`) from unintended batch overwrites.
- **Bulgarian Navigation & Sidebar Deduplication**:
  - Resolved duplicate menu entries in `docs/.vitepress/locales/bg.mjs` where both the vocabulary list and alphabetical glossary were labeled with the duplicate term for glossary (Rechnik).
  - Renamed the vocabulary list entry to the canonical phrase for word list (Spisuk na dumite), matching the document heading and eliminating sidebar navigation ambiguity.

---

## 🚀 Version 1.8.7 (September 2026)

**Focus:** *English Residue Detection Gate, Language Switcher UX & Dropdown Scrolling, Polytonic Greek Typography & Multi-Locale Convergence*

### ✨ Features & Highlights
- **Universal English Residue QA Gate**:
  - Extended `scripts/translation_qa.py` with Lingua-based statistical language detection and stopword verification for residual English content in all languages where English is not an allowed fallback.
  - Added robust regex patterns targeting unlocalized exercise headers (`Word Forms`, `Verb Forms`, `Translation Exercise`, `Reading Exercise`, `Writing Exercise`) with optional alphabetic section prefixes.
  - Implemented automatic media container stripping (`::: media ... :::`) in LID pre-processing to eliminate false alarms from English attribution/Flickr citations.
- **Language Switcher UX & Dropdown Scrolling**:
  - Added scrolling containment (`max-height: min(75vh, 550px)`, `overflow-y: auto`, `overscroll-behavior: contain`) to the language switcher menu, preventing the main page background from scrolling when browsing long locale lists.
  - Synchronized language switcher options dynamically with active locales configured in Settings (`payer_active_locales`), defaulting to all available languages when unconfigured.
- **Polytonic Greek Typography Enhancement**:
  - Configured high-fidelity font stacks prioritizing `EB Garamond` and `Gentium Plus` for Ancient Greek (`grc`) and Modern Greek (`el-GR`), ensuring authentic rendering of polytonic diacritics and eta characters without browser synthetic bold distortion.
- **Multi-Locale Translation Convergence**:
  - Healed untranslated exercise headings, instructions, and vocabulary glosses across Lithuanian (`lt`), Serbo-Croatian (`sh`), Slovenian (`sl`), Polish (`pl`), and Portuguese (`pt`).
  - Fully translated the offline PWA guide into Hebrew (`docs/he/pwa-guide.md`).
  - Restored broken lesson 51 structures in Lithuanian and cleanly re-assembled `docs/lt/lektionen/wortliste.md`.
- **Translation Prompt Hardening**:
  - Updated LLM system instructions in `scripts/translation/client.py` to mandate complete localization of all subheadings and strictly disallow English fallback translations for non-English targets.

---

## 🚀 Version 1.8.6 (September 2026)

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

# Milestones

## v1.0 Initial MVP (Shipped: 2026-04-14)

**Phases completed:** 4 phases, 4 plans, 102 tasks

**Key accomplishments:**
- **Automated Conversion**: Successfully converted 133 legacy Sanskrit HTML lessons to clean Markdown while preserving full Devanāgarī/Unicode integrity.
- **Modern SSG Stack**: Implemented VitePress with full-text search, persistent hierarchical sidebar numbering, and grammar index.
- **Scholarly Design**: Created a custom Solarized theme with optimized Sanskrit typography (OpenType ligatures) and high-readability scholarly table styling.
- **Asset Integrity**: Completed a full licensing audit and localized storage for 513 unique images.
- **Build Automation**: Established a robust build pipeline with automated link fixing and HTML cleanup scripts.

---

## v1.1 Interaktion & Flexibilität (Shipped: 2026-04-19)

**Phases completed:** 5 phases (5-9), 5 plans, 88 tasks

**Key accomplishments:**
- **Interactive Learning**: Integrated `vitepress-plugin-quiz` with a custom-branded `PayerQuiz.vue` component, supporting localized Single/Multiple Choice questions.
- **Internationalization (i18n)**: Implemented full VitePress `locales` support, including a DE/EN language switcher and a mirrored structure for English content.
- **English Translation**: Completed the bulk translation of grammar exercises 1-60, establishing a fully bilingual grammar reference.
- **Tech Stack Optimization**: Migrated to a multi-stage Docker build with Nginx optimization for cleaner production deployments and faster build/deploy cycles.

---

## v1.2 Search, Index & I18n Expansion (Shipped: 2026-05-27)

**Phases completed:** 5 phases (10-14), 12 plans

**Key accomplishments:**
- **Search Optimization**: IAST folding and language-specific search indexing.
- **Thematic Indexing**: Frontmatter taxonomy parser, thematic register, and related lessons components.
- **I18n Expansion**: Full translation coverage for IT, ES, BG, UK, RU, TA, PA.
- **Lesson 27 Reconstruction**: 1:1 structural parity with original HTML and zero-HTML migration.

---

## v1.3 Polyglot & Polish (Shipped: 2026-06-11)

**Phases completed:** 3 phases (15-17), 11 plans

**Key accomplishments:**
- **VitePress Markdown Editor**: Split-pane live preview with comprehensive custom container rendering.
- **Polyglot Expansion**: Added LA, RM, RO to full locale parity (14 languages total).
- **Scholarly Polish**: Complete licensing audit and standard caption formatting across all image assets.

---

## v1.4 Offline-First PWA (Shipped: 2026-06-15)

**Phases completed:** 4 phases (18-21), 17 plans

**Key accomplishments:**
- **PWA Infrastructure**: Web app manifest, custom install prompts, and app icons.
- **Service Worker Lifecycle**: Cache versioning with CacheFirst, NetworkFirst, and StaleWhileRevalidate strategies.
- **Client-Side Language Selection**: Dynamic localStorage-backed settings page allowing selective offline caching.
- **Lighthouse Verification**: Audited PWA score ≥ 90 and verified offline navigation.

---

## v1.5 QA-Authoring-Split & UAT (Shipped: 2026-06-30)

**Phases completed:** 1 phase (22), 6 plans

**Key accomplishments:**
- **Two Builds & Two Domains**: Isolated `payer.birchville.cc` (public) from `author.payer.birchville.cc` (authoring).
- **Secure Authoring Access**: Authelia reverse-proxy protection for authoring tools.
- **Zero QA Residue**: Stripped editor code, debug utilities, and deleteme containers from public production bundle.

---

## v1.6 Developer Experience / Extension (Shipped: 2026-07-15)

**Phases completed:** 1 phase (23), 2 plans

**Key accomplishments:**
- **VSCode Extension**: Custom syntax highlighting, container snippets, and live markdown-it preview injection.
- **Locales TH & EL**: Full localization and content integration for Thai and Modern Greek.

---

## v1.7 Key Locales 100% Completion & UI Polish (Shipped: 2026-08-22)

**Key accomplishments:**
- **100% Completion without Fallbacks**: English (`en`) and Russian (`ru`) verified 100% clean (136/136 files) with zero fallbacks.
- **UI Localization SSOT**: Dynamic centralized navigation and control elements across all active locales.
- **Typography**: Upright Devanāgarī typography without italic distortion, unentangled signal-red tags.

---

## v1.8 Polyglot 100% Completion (48 Languages) & Autonomous Healing (Shipped: 2026-09-10, Release v1.8.3)

**Key accomplishments:**
- **100% Polyglot Completion (0 Fallbacks)**: All 48 target languages reached 100.0% completion without fallbacks (140/140 clean files per language, totaling 6,860 clean localized markdown files).
- **New Locales**: Integrated, localized, and translated Estonian (`et`) and isiZulu (`zu`).
- **Script Restorations**: Restored Ge'ez (`gez`, Ethiopic script) and Bulgarian (`bg`, Cyrillic script) with zero structural defects.
- **Corpus Optimization**: Purged unsupported ancient and dialectal corpora (`cop`, `akk`, `arc`, `gsw`).
- **Autonomous Multi-Worker Healer Pipeline**: Deployed `scripts/autonomous_healer.py` with multi-process PID isolation, bidirectional queue traversal, and strict Lingua validation gates (`is_file_fallback`).
- **Build Scaling (32 GB Swap / Heap)**: CI and Docker workflows tuned to render 6,979 VitePress SSG pages reliably without heap exhaustion.
- **Multi-Platform Docker Release**: Built and pushed multi-arch container images (`linux/amd64`, `linux/arm64`) to `ghcr.io/birchville-org/sanskritkurs-payer:v1.8.3` and `latest`.

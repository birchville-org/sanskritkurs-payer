# Project Retrospective: Sanskritkurs Pipeline

## Milestone: v1.0 — Initial MVP

**Shipped:** 2026-04-14
**Phases:** 4 | **Plans:** 4

### What Was Built
- Automated migration system for legacy Sanskrit content.
- Clean scholarly typography and Solarized design.
- Production-ready VitePress structure with full-text search and licensing audit.

### What Worked
- **Incremental Transitions**: Using SUMMARY.md to bridge phases kept the momentum.
- **Visual-First Feedback**: Tuning CSS live in the browser helped capture the "warm" feel quickly.
- **Regex-Based Content Cleanup**: Handled 133 files in seconds instead of manual editing.

### What Was Inefficient
- **Git State Management**: Starting with many untracked files made the final milestone completion more complex.
- **Table Formatting**: Some edge cases in nested blockquotes required manual post-processing. A better initial regex could have saved effort.

### Patterns Established
- **Clean URLs**: Consistent `/lektionen/lektionXX` routing.
- **Hierarchical CSS Numbering**: Offsetting content complexity out of Markdown and into the theme.

### Key Lessons
- Always commit work at the end of every phase to keep the Git history clean and stats accurate.
- Use the Browser Agent early for cross-browser visual validation of complex typography.

---

## Milestone: v1.4 — Offline-First PWA

**Shipped:** 2026-06-15
**Phases:** 4 | **Plans:** 16

### What Was Built
- Robust Service Worker with intelligent caching strategies (NetworkFirst, CacheFirst, StaleWhileRevalidate).
- Dynamic runtime language filter via settings, preventing 70MB downloads of unused languages.
- Complete PWA manifest, offline fallbacks, and polished performance (WebP optimization).

### What Worked
- **Decoupled Architecture**: Keeping the core static build unaware of the runtime language filtering kept VitePress lightning fast.
- **Progressive Enhancement**: PWA features strictly act as overlays, ensuring base functionality never breaks on older devices.

---

## Milestone: v1.5 — QA-Authoring-Split & UAT

**Shipped:** 2026-06-30
**Phases:** 1 | **Plans:** 6

### What Was Built
- Hard split of the production environment vs. authoring environment using dedicated Express Server (`author-server`) and Docker builds.
- Direct Git integration (Octokit) for saving draft branches and automatic PR creation from the live UI.

### What Worked
- **No Config Duplication**: `VITEPRESS_ENV=author` environment variables solved the split elegantly without needing a second `.vitepress/config.mjs` file.
- **Zero-Footprint Production**: Safe stripping of QA and API code before building the `dist-public` image.

### Current Status
- Project has entered Maintenance Mode / UAT phase. Awaiting final translations and visual inspection by the user before final Git commit.

---

## Cross-Milestone Trends

| Milestone | Duration | Changes | Req Coverage | Status |
|-----------|----------|---------|--------------|--------|
| v1.0 | 2 days | 102 files | 100% | Shipped |
| v1.1 | 5 days | ~80 files | 100% | Shipped |
| v1.2 | 38 days | ~2000 files | 100% | Shipped |
| v1.3 | 15 days | ~150 files | 100% | Shipped |
| v1.4 | 4 days | ~20 files | 100% | Shipped |
| v1.5 | 15 days | 8 files | 100% | Maintenance/UAT |

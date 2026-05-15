# Phase 13 Plan: QA Infrastructure Restoration

## Objectives
- Migrate legacy `viewer.html` logic to a integrated VitePress route `/qa/viewer`.
- Implement "Pro-Sync" dual-pane view with bidirectional sync-scrolling.
- Apply strict visual parity with the "Scholarly Synthesis" design system.
- Support deep linking and lesson auditing.

## Tasks

### Wave 1: Infrastructure & Scaffolding
- [ ] **Task 1.1**: Create `docs/qa/viewer.md` route.
  - `<read_first>`: `docs/.vitepress/config.mjs`
  - `<action>`: Create `docs/qa/viewer.md` with frontmatter `layout: page` and a custom `<QAViewer />` component tag.
  - `<acceptance_criteria>`: `docs/qa/viewer.md` exists and contains `<QAViewer />`.
- [ ] **Task 1.2**: Scaffold `docs/.vitepress/theme/components/QAViewer.vue`.
  - `<read_first>`: `docs/.vitepress/theme/index.css`
  - `<action>`: Create a Vue 3 component with dual-pane layout (Source vs Render).
  - `<acceptance_criteria>`: `QAViewer.vue` exists and renders a basic "Hello Viewer" message.

### Wave 2: Core Migration
- [ ] **Task 2.1**: Port logic from `docs/public/qa/viewer.js`.
  - `<read_first>`: `docs/public/qa/viewer.js`, `docs/public/qa/viewer.html`
  - `<action>`: Implement `fetchLesson` and `renderMarkdown` methods in `QAViewer.vue`. Use URL parameters (`?lesson=`) for state management.
  - `<acceptance_criteria>`: Viewer loads and renders a lesson's raw source and HTML when `?lesson=lektion01` is appended.
- [ ] **Task 2.2**: High-fidelity Grammar Box rendering.
  - `<read_first>`: `docs/.vitepress/theme/index.css` (grammar-box rules)
  - `<action>`: Ensure the rendered HTML in the viewer uses the production CSS classes (e.g., `.grammar-box`, `.sanskrit-dev`).
  - `<acceptance_criteria>`: Rendered HTML in viewer matches production site styling 1:1.

### Wave 3: Pro-Sync & UI
- [ ] **Task 3.1**: Bidirectional Sync-Scroll.
  - `<read_first>`: `docs/public/qa/viewer.js` (if sync logic exists)
  - `<action>`: Implement intersection-observer or percentage-based sync-scrolling between the two panes.
  - `<acceptance_criteria>`: Scrolling the source pane scrolls the render pane proportionally.
- [ ] **Task 3.2**: Design System Branding.
  - `<read_first>`: `AGENTS.md`
  - `<action>`: Apply `#03192e` (Deep Ink) to sidebars and `#fcf9f2` (Parchment) to content areas. Use Newsreader serif for content.
  - `<acceptance_criteria>`: UI colors and typography match `AGENTS.md`.

### Wave 4: Integration & Cleanup
- [ ] **Task 4.1**: Routing Fix & Verification.
  - `<read_first>`: `docs/.vitepress/config.mjs`
  - `<action>`: Test the `/qa/viewer` route. Ensure the browser status no longer shows 404 for this route.
  - `<acceptance_criteria>`: Browser successfully loads `localhost:5173/qa/viewer`.
- [ ] **Task 4.2**: Legacy Cleanup.
  - `<read_first>`: `docs/public/qa/`
  - `<action>`: Delete `docs/public/qa/viewer.html` and `docs/public/qa/viewer.js`.
  - `<acceptance_criteria>`: `docs/public/qa/` directory is empty or removed.

## Verification
- [ ] **Visual**: 1:1 parity with `AGENTS.md`.
- [ ] **Functional**: `?lesson=` works, sync-scroll works, grammar boxes render correctly.
- [ ] **Routing**: No 404 errors on `/qa/viewer`.

## Must Haves
- Zero legacy HTML in the new viewer (use pure Vue/Markdown-it).
- Exact color hex codes from `AGENTS.md`.

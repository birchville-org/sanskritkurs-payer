# Phase 13 Context: QA Infrastructure Restoration

## Goal
High-fidelity restoration and standardization of the Sanskrit QA viewer to support rigorous content auditing and synchronization with the "Scholarly Synthesis" design system.

## Decisions
- **Navigation Routing**: Migrate the viewer from a static file in `public/` to a dynamic VitePress route at `/qa/viewer.md`. This resolves 404 issues and integrates the tool into the standard site structure.
- **Design System Parity**: Import global VitePress CSS and typography tokens to ensure the viewer matches the "Scholarly Synthesis" mood (Deep Ink, Parchment, Newsreader serif).
- **Audit Features**:
    - **Pro-Sync View**: Dual-pane layout with bidirectional sync-scrolling between raw Markdown source and rendered HTML.
    - **Deep Linking**: Robust URL parameter support for direct navigation to specific lessons (e.g., `?lesson=lektion12`).
    - **Visual Remediation**: Ensure all grammar boxes and Devanāgarī strings are rendered with the same fidelity as the production lessons.

## Specifics
- **Existing Assets**: Utilize the untracked `docs/public/qa/viewer.html` and `.js` as the logic baseline, but refactor into a Vue/VitePress component.
- **Visual Parity**: Strictly follow `AGENTS.md` for whitespace and color luxury.

## Canonical Refs
- [AGENTS.md](file:///Volumes/SanDisk1TB/proj/Payer/AGENTS.md)
- [docs/.vitepress/theme/index.css](file:///Volumes/SanDisk1TB/proj/Payer/docs/.vitepress/theme/index.css)
- [QUALITY_STANDARDS.md](file:///Volumes/SanDisk1TB/proj/Payer/QUALITY_STANDARDS.md)

## Folded Todos
*None.*

## Deferred Ideas
*None.*

# Research: Technical Stack additions for v1.2

## Search & Linguistic Processing
- **MiniSearch (VitePress default)**: Will be extended with a custom `processTerm` hook.
- **Normalization Engine**: JavaScript `String.prototype.normalize('NFD')` + custom regex mappings for IAST-specific characters (e.g., `ṛ` -> `r`, `ṁ` -> `m`).
- **Devanāgarī Support**: MiniSearch handles Unicode, but we may need a transliteration library if we want to search IAST and find Devanāgarī (or vice versa).

## Thematic Indexing
- **VitePress Data Loading**: Using `.data.ts` (Build-Time Data Loading) to aggregate frontmatter from all lessons.
- **Vue 3 Composition API**: Custom components (`GrammarIndex.vue`, `TagCloud.vue`) to render the aggregated data.
- **Frontmatter Schema**: Standardizing `tags`, `category`, and `related` fields across all markdown files.

## Internationalization (i18n)
- **VitePress Locales**: Expanding the `locales` object in `config.mjs`.
- **Modular Config**: Moving locale-specific sidebars/navs to separate files (e.g., `.vitepress/locales/it.mjs`) to keep the main config clean.
- **Translation Pipeline**: Leveraging the existing Python-based batch translator for IT and ES.

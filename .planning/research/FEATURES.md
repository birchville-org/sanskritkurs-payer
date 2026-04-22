# Research: Feature Deep Dive for v1.2

## 1. Thematic Index (Grammar Navigator)
- **Concept**: A centralized page (and potentially a sidebar section) that groups lessons by grammatical category (e.g., "Sandhi", "Verbal Morphology", "Syntax").
- **Implementation**: 
    - Auto-generation based on `tags` in frontmatter.
    - Clickable "Topic Chips" that filter the lesson list.
    - "Related Lessons" section at the bottom of each lesson.

## 2. Sanskrit-Aware Search
- **IAST Folding**: Users searching for "Sanskrit" should find "Saṃskṛta".
- **Devanāgarī Matching**: Support for native script searching without requiring exact Unicode normalization matches (handling different forms of Anusvara, etc.).
- **Multi-locale Search**: Ensuring Italian users don't see German results in their primary search view (VitePress handles this via `themeConfig.search.options.locales`).

## 3. Italian & Spanish Expansion
- **Infrastructure**: New folders `/docs/it/` and `/docs/es/`.
- **Content**: Full mirror of the 61 lessons and exercises.
- **Language Switcher**: Updated header to include IT and ES flags/labels.

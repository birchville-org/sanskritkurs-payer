# Phase 11: Thematic Indexing & Specialized Navigation - Research

## Automated Topic Extraction

### Strategy: Heading Scanning
VitePress `createContentLoader` allows us to load all Markdown files in a directory. We can use a custom `transform` function to extract headings.

**Implementation Sketch:**
```javascript
import { createContentLoader } from 'vitepress'

export default createContentLoader('lektionen/*.md', {
  transform(raw) {
    return raw.map(page => {
      const headings = page.content.match(/^#{1,3}\s+(.+)$/gm) || [];
      return {
        url: page.url,
        title: page.frontmatter.title || headings[0]?.replace(/^#\s+/, ''),
        topics: headings.map(h => h.replace(/^#{1,3}\s+/, '').trim())
      }
    })
  }
})
```

### Cross-Language Mapping
To maintain "Schlagworte im Hintergrund auf Deutsch":
1.  Load German lessons to build a `topicMap`: `{ topic: [lessonNumber] }`.
2.  The `RelatedLessons` component receives the current lesson number.
3.  It looks up other lessons with the same topics in the `topicMap`.
4.  It displays links to these lessons in the *current* locale.

## UI Components: Premium Cards

### Design System (AGENTS.md)
- **Colors**: `#fcf9f2` (Parchment), `#03192e` (Deep Ink).
- **Typography**: Newsreader (Serif) for titles, Inter (Sans) for labels.
- **Style**: No borders, background shifts.

### RelatedLessons.vue
A new Vue component that:
- Reads the global topics data.
- Filters for lessons sharing the same headings as the current page.
- Renders cards with:
  - Small "Topic" label (e.g. "Thema: Sandhi").
  - Large lesson title.
  - Link to the lesson.

## Constraints & Edge Cases
- **Duplicate Headings**: Some headings like "Übung" or "Wortkunde" might be too generic. We may need a exclusion list (e.g. ignore headings with fewer than 4 characters or common generic terms).
- **IAST in Headings**: The extractor must handle diacritics correctly (matching `Sandhi` even if written `Sandhi` or `Sandhi-Regeln`).

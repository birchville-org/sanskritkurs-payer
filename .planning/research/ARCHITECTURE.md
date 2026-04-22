# Research: Architecture for v1.2

## Search Normalization Strategy
The `processTerm` hook in MiniSearch will implement a "Folding" algorithm:
```javascript
function folding(term) {
  return term.toLowerCase()
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '') // Remove standard accents
    .replace(/ṣ/g, 's')
    .replace(/ś/g, 's')
    .replace(/ṛ/g, 'r')
    // ... add all IAST mappings
}
```

## Data Aggregation for Indexing
A new file `docs/.vitepress/data/lessons.data.mts` will export all lesson metadata:
```typescript
import { createContentLoader } from 'vitepress'
export default createContentLoader('**/lektionen/*.md', {
  includeSrc: false,
  transform(raw) {
    return raw.map(p => ({
      title: p.frontmatter.title,
      url: p.url,
      tags: p.frontmatter.tags || []
    }))
  }
})
```

## Localization Scalability
To avoid a massive `config.mjs`, we will use a directory-based config loading:
- `docs/.vitepress/locales/de.mjs`
- `docs/.vitepress/locales/en.mjs`
- `docs/.vitepress/locales/it.mjs` (New)
- `docs/.vitepress/locales/es.mjs` (New)

The main `config.mjs` will import and spread these locale objects into the `defineConfig` call.

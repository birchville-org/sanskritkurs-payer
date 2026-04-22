# Phase 10: Search Optimization & Core Infrastructure - Research

## Search Optimization: IAST & Devanāgarī Folding

### MiniSearch Configuration
VitePress uses MiniSearch. To implement folding, we need to override the `processTerm` option.

**Proposed Normalization Function:**
```javascript
const foldingMap = {
  'ā': 'a', 'ī': 'i', 'ū': 'u', 'ṛ': 'r', 'ṝ': 'r', 'ḷ': 'l', 'ḹ': 'l',
  'ṁ': 'm', 'ṃ': 'm', 'ḥ': 'h', 'ṅ': 'n', 'ñ': 'n', 'ṭ': 't', 'ḍ': 'd',
  'ṇ': 'n', 'ś': 's', 'ṣ': 's'
};

function normalizeSanskrit(term) {
  let normalized = term.toLowerCase().normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  for (const [key, value] of Object.entries(foldingMap)) {
    normalized = normalized.replace(new RegExp(key, 'g'), value);
  }
  return normalized;
}
```

### Devanāgarī Handling
MiniSearch tokenizes Unicode characters. For Devanāgarī folding, we could map similar sounds (e.g., various Anusvara forms) to a common base, but for a start, standardizing on NFC/NFD normalization is a must.

## Core Infrastructure: Modular Configuration

### Current State
`docs/.vitepress/config.mjs` contains all locale definitions, leading to a large file (120+ lines for 2 languages).

### Target State
```text
docs/.vitepress/
├── locales/
│   ├── de.mjs
│   ├── en.mjs
│   ├── it.mjs (for Phase 12)
│   └── es.mjs (for Phase 12)
└── config.mjs (Main entry)
```

**Implementation Detail:**
- `config.mjs` will import `de` and `en` from the `locales/` folder.
- Common shared logic (like `getSidebarItems`) will remain in `config.mjs` or a separate `utils.mjs`.

## Dependencies
- No new npm packages required; built-in JavaScript/VitePress features suffice.

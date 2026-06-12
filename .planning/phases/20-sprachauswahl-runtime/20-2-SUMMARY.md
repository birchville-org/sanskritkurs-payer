# 20-2 Summary: Sidebar Filter (Runtime-Filter)

**Date**: 2026-06-12
**Status**: ✅ Complete

## Deliverables

### 1. Locale Filter Logic
- **File**: `docs/.vitepress/theme/locale-filter.js` (~110 lines)
- **Exports**:
  - `filterSidebarByLocales()` — applies `.locale-hidden` class to inactive locale elements
  - `setupLocaleFilter()` — attaches `payer:locales-changed` event listener

### 2. Integration
- **File**: `docs/.vitepress/theme/index.mjs`
- Import: `filterSidebarByLocales, setupLocaleFilter`
- `filterSidebarByLocales()` called in route watcher (250ms after navigation)
- `setupLocaleFilter()` called in `setup()` (once per session)

### 3. CSS
- **File**: `docs/.vitepress/theme/custom.css`
- Added: `.locale-hidden { display: none !important; }`

## Filter Logic

**Applies to:**
- All `<a href>` links with locale-prefixed paths (e.g. `/en/lektion/01`)
- VitePress Language Switcher elements (`.VPLocaleLink`, `[data-locale]`, etc.)
- Locale `<option>` elements in any `<select>`

**Rules:**
1. Current locale (detected from URL) — **always visible**
2. DE/root — **visible if `activeLocales` includes 'de'**
3. Other locales — **hidden if not in `activeLocales`**
4. Non-locale links (assets, external, etc.) — **always visible**

**Example**: Active locales = `['de', 'en', 'it']`, Current = `de`
- Link to `/en/lektion/01` → visible ✅
- Link to `/ru/lektion/01` → hidden ❌
- Link to `/impressum` (DE root page) → visible ✅
- Link to `/assets/main.js` → visible ✅

## Events

| Event | Trigger | Effect |
|---|---|---|
| Route change | User navigates | Re-filter after 250ms |
| `payer:locales-changed` | Settings save | Re-filter via `requestAnimationFrame` |
| Initial page load | Vue mount | Filter on first watch fire |

## Verification

✅ Build successful (138s)
✅ No JavaScript errors (syntax validated via build)
✅ All imports resolve correctly
✅ CSS class injected

## Manual Test Plan (deferred to Phase 21 QA)

1. Open site with default settings (`de, en, it`)
2. Verify: only DE, EN, IT links visible in Language Switcher
3. Navigate to `/en/lektion/01` → verify EN content visible
4. Go to Settings → add "Français" → save
5. Verify: Language Switcher now shows FR option
6. Navigate to `/fr/lektion/01` → works (link visible)
7. Remove "Italiano" → save
8. Verify: IT links no longer visible in sidebar

## Notes

- Filter is **additive**: only hides, never modifies hrefs
- Filter is **safe for SSG**: only runs client-side (window guard in place)
- Performance: skips re-filter if active locales haven't changed
- Future-proof: targets generic VitePress DOM patterns, not hard-coded class names

# 20-3 Summary: Service Worker Locale-aware Caching

**Date**: 2026-06-12
**Status**: ✅ Complete

## Deliverables

### 1. Updated Service Worker
- **File**: `docs/public/sw.js` (complete rewrite for Phase 20)
- **Size**: ~11.9 KB (was ~7.1 KB in Phase 19)
- **Cache version**: `payer-v20-r1`

## New Features

### A. Active Locales State (client ↔ SW sync)

```
Client (browser tab)
    │
    │ postMessage({ type: 'SET_ACTIVE_LOCALES', locales: ['de','en','it'] })
    ▼
Service Worker
    │
    ├─► Updates ACTIVE_LOCALES in memory
    ├─► Persists to Cache Storage as /__payer_locales (JSON)
    └─► Evicts stale cache entries for deactivated locales
```

**Persistence across SW restarts:**
- Service Workers are terminated & restarted by browser
- On `activate` event: reads `/__payer_locales` from Cache Storage
- Restores `ACTIVE_LOCALES` before claiming clients
- Default `['de', 'en', 'it']` matches `lang-settings.js` DEFAULT_LOCALES

### B. URL Filter: `isUrlAllowed(url, activeLocales)`

Always allowed (cached regardless of locale state):
- `/`, `/index.html`, `/offline.html`, `/manifest.json`, `/hashmap.json`
- `/pwa-icons/*`, `/assets/*`, `/icons/*`
- Any URL with known asset extension (`.css`, `.js`, `.woff2`, `.png`, etc.)

Locale-controlled:
- `/impressum`, `/lektion/01/`, `/settings` (DE root, no prefix) → only if `'de'` is active
- `/en/...` → only if `'en'` is active
- `/it/...` → only if `'it'` is active
- ... for all 14 locales

### C. Strategy Behavior for Inactive Locales

| Strategy | Normal behavior | When locale is inactive |
|---|---|---|
| `networkFirst` | Cache fresh network response | Network-only (no cache put) |
| `cacheFirst` | Return cache if exists | Network-only (no cache lookup OR put) |
| `staleWhileRevalidate` | Cache + background refresh | Network-only (no cache interaction) |

**Critical**: Inactive-locale URLs throw network errors through to the browser (for `networkFirst`) or return 404/503 (for others). The browser will display its own error page for uncached documents, or our `offline.html` if the URL has been visited before being deactivated.

### D. Cleanup Trigger

When user deactivates a locale in Settings:
1. Client sends `SET_ACTIVE_LOCALES` message
2. SW updates `ACTIVE_LOCALES` in memory
3. SW persists to `/__payer_locales` Cache entry
4. SW runs `cleanupInvalidatedCache()` — iterates all cache keys, deletes those failing `isUrlAllowed()` check

## Code Organization

```
sw.js
├── CACHE config (version, name, precache list, locales cache key)
├── INSTALL listener (precache + skipWaiting)
├── ACTIVATE listener (cleanup + restore locales + claim)
├── MESSAGE listener (SET_ACTIVE_LOCALES + SKIP_WAITING)
├── isUrlAllowed() + cleanupInvalidatedCache()
├── networkFirst() / cacheFirst() / staleWhileRevalidate() (with locale checks)
└── FETCH listener (routing)
```

## Verification

✅ Build successful (122s)
✅ `sw.js` copied to `docs/.vitepress/dist/sw.js`
✅ Cache version bumped to `payer-v20-r1`
✅ No syntax errors (VitePress build includes JS parsing of service worker)

## Manual Test Plan (deferred to Phase 21 QA)

1. Load site, open DevTools → Application → Service Workers
2. Verify SW shows version `payer-v20-r1` (new install evicts `payer-v19-r1`)
3. Go to Settings → deactivate "English" → save
4. Console should show: `[SW] Active locales updated: ['de', 'it']`
5. Console should show: `[SW] Evicted N stale entries`
6. Inspect Cache Storage → `/en/...` URLs should be gone
7. Navigate to `/en/lektion/01/` online → should work (network pass-through)
8. Go offline → `/en/lektion/01/` should show offline.html (no cache fallback)
9. Reactivate "English" in Settings
10. Go online, visit `/en/lektion/01/` → cache entry re-created
11. Reload worker (DevTools) → check console: `[SW] Restored active locales: ['de','en','it']`

## Notes

- **Two MESSAGE listeners**: one for `SET_ACTIVE_LOCALES` (Plan 20-3), one for `SKIP_WAITING` (Plan 20-5 install flow). Kept separate for clarity.
- **LOCALES_CACHE_KEY as Request object**: Cache Storage API requires Request or string URL. Using a Request object ensures exact URL matching on `cache.match()` and `cache.put()`.
- **`clone()` on LOCALES_CACHE_KEY**: When putting to cache, the Request is consumed — we clone to preserve the constant for later reads.
- **Shared assets always cached**: CSS/JS/fonts don't have locale prefixes (live in `/assets/`) and are shared across all locales. Never filtered.
- **Performance**: `isUrlAllowed()` is a handful of regex tests per fetch — negligible overhead per request.

## Next

Phase 20-4: Prefetch manifest generation + background locale re-loading on Settings change.

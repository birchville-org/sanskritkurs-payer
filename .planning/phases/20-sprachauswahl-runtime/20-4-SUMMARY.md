# 20-4 Summary: Sprach-Nachladen mit Manifest + Prefetch-API

**Date**: 2026-06-12
**Status**: ✅ Complete

## Deliverables

### 1. Manifest-Generator (Build-Post-Hook)
- **File**: `scripts/gen_locale_manifests.mjs` (~145 Zeilen)
- **Trigger**: `npm run postdocs:build` (automatisch nach Build)
- **Output**: 14× `manifest-{locale}.json` pro Sprache in `dist/`
  - `manifest-de.json` (215 URLs, ~5 KB)
  - `manifest-en.json` (143 URLs, ~3 KB)
  - `manifest-it.json`, `manifest-bg.json`, etc.
  - **Total**: 2077 URLs für 14 Locales

### 2. SW Prefetch-Handler (`docs/public/sw.js`)
- **New message type**: `PREFETCH_LOCALE`
- **Request shape**: `{ type, locale, urls }`
- **Response shape**: `{ type: 'PREFETCH_COMPLETE', locale, cached, failed, total }`
- Updates `ACTIVE_LOCALES` in-memory + persists to `/__payer_locales`
- Sequential fetch (20-5 optimiert zu parallel)

### 3. Settings-Component Erweiterung (`PayerLanguageSettings.vue`)
- **New function**: `prefetchLocale(locale)` — orchestriert Manifest-Fetch + SW-Message
- **Enhanced save()**:
  - Snapshots `oldLocales` vs `newLocales`
  - Identifiziert `addedLocales` und `removedLocales`
  - Für jede neue Sprache: `prefetchLocale()` mit Progress
  - Zeigt per-locale Status als Live-Indikator
- **New UI element**: `.locale-status-list` mit downloading/done/error States

### 4. package.json Integration
```json
"scripts": {
  "postdocs:build": "node scripts/gen_locale_manifests.mjs"
}
```
npm ruft den Hook automatisch nach `npm run docs:build` auf (nur bei Erfolg).

## Architecture: Manifest-Flow

```
Developer: npm run docs:build
     │
     ▼
VitePress builds dist/
     │
     ▼ (post-hook)
gen_locale_manifests.mjs
     │ scans .html files
     │ detects locale by first path segment
     │ groups & writes manifest-{locale}.json
     ▼
dist/manifest-{locale}.json (14 files)

─────────────────────────────────────

User (browser): Settings → aktiviert neue Sprache "Français"
     │
     ▼
Settings.vue.save()
     ├─ detects: addedLocales = ['fr']
     └─ calls prefetchLocale('fr')
           │
           ▼
     fetch('/manifest-fr.json')  → 143 URLs
           │
           ▼
     navigator.serviceWorker.controller.postMessage({
       type: 'PREFETCH_LOCALE',
       locale: 'fr',
       urls: [143 items]
     })
           │
           ▼
     sw.js PREFETCH_LOCALE handler
       ├─ adds 'fr' to ACTIVE_LOCALES
       ├─ persists to /__payer_locales
       └─ sequential fetch() for each URL
             → cache.put() for each successful response
           │
           ▼
     postMessage({ type: 'PREFETCH_COMPLETE', cached: 141, failed: 2, total: 143 })
           │
           ▼
     Settings.vue: UI update → ✓ Französisch: 141/143 Seiten
```

## UI States

Während Prefetch zeigt die Settings-Page:

```
┌─────────────────────────────────────────┐
│ ☑ Français                              │
│                                         │
│ [Speichern / Save] (disabled: Arbeite..│
│                                         │
│ ⏳ Français (fr)      ← downloading     │
│                                         │
│ ⏳ Neue Sprachen werden heruntergeladen │
│    (0/1)...                              │
└─────────────────────────────────────────┘

       ↓ nach Download:

┌─────────────────────────────────────────┐
│ ✅ Saved                                 │
│                                         │
│ ✓ Français (fr)       ← done            │
│                                         │
│ ✓ +1 Sprache(n) hinzugefügt             │
└─────────────────────────────────────────┘
```

Farben:
- ⏳ downloading: `var(--vp-c-warning-1)` (amber)
- ✓ done: `var(--vp-c-success-1)` (green)
- ⚠ error: `var(--vp-c-danger-1)` (red)

## Verification

✅ `npm run docs:build` generiert 14 manifest-Dateien automatisch
✅ Total 2077 URLs across locales
✅ sw.js enthält PREFETCH_LOCALE handler (288 Zeilen total)
✅ Settings-Component mit prefetchLocale() + UI
✅ Build erfolgreich
✅ Locale-detection-Regel konsistent mit SW's `isUrlAllowed()`:
  - Root (kein Prefix) → de
  - `/en/*` → en
  - `/it/*` → it

## Edge Cases

### 1. Manifest nicht gefunden (z.B. dev mode)
- `fetch('/manifest-fr.json')` returnt 404
- `prefetchLocale()` returnt null
- UI zeigt "⚠ Französisch: Download fehlgeschlagen"
- Sprache trotzdem in `activeLocales` (wird beim nächsten Online-Besuch nachgeladen)

### 2. Keine Netzwerk-Verbindung
- `fetch()` in SW wirft Exception
- SW antwortet mit `PREFETCH_COMPLETE` mit fehlenden Entries
- UI zeigt teilweise Erfolge

### 3. SW Controller nicht verfügbar (dev mode, localhost)
- `prefetchLocale()` returnt null sofort
- Settings zeigt Fehler
- Sprache wird trotzdem in localStorage gespeichert
- Nächster Online-Besuch: Pages werden via normale NetworkFirst gecacht (wenn besucht)

### 4. 2-Minuten-Timeout
- Falls SW nicht antwortet (z.B. Browser throttled SW): Timeout bricht ab
- UI zeigt error
- Keine Zombie-Requests

### 5. Doppelte Aktivierung
- Falls locale schon in `oldLocales` → nicht in `addedLocales`
- Kein Prefetch getriggert
- Nur `setActiveLocales()` (no-op wenn gleich)

## Performance

**Sequenzieller Prefetch** (aktuell): ~143 URLs × ~200ms pro URL = ~30 Sekunden pro Sprache
**Parallel (Plan 20-5)**: ~143 URLs / 6 parallel = ~5 Sekunden pro Sprache

→ 20-5 wird Prefetch parallelisieren

## Code Metrics

| Component | File | Lines Change |
|---|---|---|
| Manifest generator | `scripts/gen_locale_manifests.mjs` | +145 (new) |
| SW prefetch handler | `docs/public/sw.js` | +75 lines |
| Settings vue | `PayerLanguageSettings.vue` | +110 lines, +30 CSS |
| package.json | scripts | +1 line |

## Next

Phase 20-5: Progress-Bar für Pre-Caching bei Installation (paralleler Download)

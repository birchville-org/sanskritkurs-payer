# Plan 20-4: Sprachen nachladen

**Phase**: 20 Sprachauswahl (Runtime-Filter)  
**Status**: Pending  
**Dependencies**: 20-3 ✅

## Ziel

Wenn User eine neue Sprache in Settings aktiviert, werden deren Inhalte im Hintergrund online heruntergeladen und im Cache gespeichert. UI-Update (Sidebar, Offline-Indikator) erfolgt automatisch.

## Deliverables

1. Modifikation: `docs/.vitepress/theme/components/PayerLanguageSettings.vue`
2. Modifikation: `docs/public/sw.js` (Prefetch-API)

## Implementation

### 20-4.1: SW Prefetch-Endpoint

Service Worker soll eine Möglichkeit bieten, eine Liste von URLs vorab zu cachen:

```javascript
// In sw.js — Message Handler erweitern
self.addEventListener('message', (event) => {
  if (event.data?.type === 'PREFETCH_LOCALE') {
    const { locale, urls } = event.data
    prefetchLocale(urls).then(count => {
      // Bestätigung an Client
      event.source?.postMessage({
        type: 'PREFETCH_COMPLETE',
        locale,
        cached: count
      })
    })
  }
})

async function prefetchLocale(urls) {
  const cache = await caches.open(CACHE_NAME)
  let cached = 0
  
  for (const url of urls) {
    try {
      const response = await fetch(url)
      if (response.ok) {
        await cache.put(url, response)
        cached++
      }
    } catch (err) {
      console.warn('[SW] Prefetch failed:', url, err.message)
    }
  }
  
  return cached
}
```

### 20-4.2: URL-Liste pro Sprache

Um die relevanten URLs für eine Sprache zu kennen, benötigen wir ein Manifest. VitePress generiert das normalerweise beim Build. Wir können stattdessen eine vereinfachte Strategie nutzen:

**Option A**: Explizite URL-Liste via `sitemap.xml` parsen
```javascript
async function getUrlsForLocale(locale) {
  const response = await fetch('/sitemap.xml')
  const text = await response.text()
  const matches = text.matchAll(/<loc>([^<]+)<\/loc>/g)
  const prefix = locale === 'de' ? '/' : `/${locale}/`
  return Array.from(matches)
    .map(m => m[1])
    .filter(url => new URL(url).pathname.startsWith(prefix))
}
```

**Option B (empfohlen)**: Vereinfachtes `manifest-{locale}.json` pro Sprache generieren
```json
{
  "locale": "en",
  "urls": [
    "/en/",
    "/en/lektion/01",
    "/en/lektion/02",
    ...
  ]
}
```

Build-Script generiert diese Manifests:
```javascript
// scripts/gen-locale-manifests.mjs
import { writeFileSync, mkdirSync } from 'fs'
import { glob } from 'glob'

const DIST = 'docs/.vitepress/dist'
const LOCALES = ['de', 'en', 'it', 'bg', 'ru', 'uk', 'hi', 'fr', 'es', 'ta', 'pa', 'la', 'rm', 'ro']

for (const locale of LOCALES) {
  const prefix = locale === 'de' ? '' : `${locale}/`
  const files = await glob(`${DIST}${prefix}**/*.html`)
  const urls = files
    .map(f => f.replace(DIST, '').replace(/\.html$/, '').replace(/\/index$/, '/'))
    .sort()
  
  mkdirSync(DIST, { recursive: true })
  writeFileSync(
    `${DIST}/manifest-${locale}.json`,
    JSON.stringify({ locale, count: urls.length, urls }, null, 2)
  )
}
```

### 20-4.3: Settings-Component erweitern

```javascript
// In PayerLanguageSettings.vue
const status = ref({})  // { [locale]: 'idle' | 'downloading' | 'done' | 'error' }

async function save() {
  const oldLocales = getActiveLocales()
  const newLocales = selected.value
  setActiveLocales(newLocales)
  
  // Welche sind neu hinzugekommen?
  const added = newLocales.filter(l => !oldLocales.includes(l))
  
  for (const locale of added) {
    status.value[locale] = 'downloading'
    
    try {
      // URL-Liste holen
      const manifestUrl = locale === 'de' ? '/manifest-de.json' : `/manifest-${locale}.json`
      const response = await fetch(manifestUrl)
      const manifest = await response.json()
      
      // Prefetch via SW
      navigator.serviceWorker.controller.postMessage({
        type: 'PREFETCH_LOCALE',
        locale,
        urls: manifest.urls
      })
      
      // Wait for completion (via MessageChannel)
      await new Promise((resolve) => {
        const handler = (event) => {
          if (event.data?.type === 'PREFETCH_COMPLETE' && event.data.locale === locale) {
            navigator.serviceWorker.removeEventListener('message', handler)
            resolve()
          }
        }
        navigator.serviceWorker.addEventListener('message', handler)
      })
      
      status.value[locale] = 'done'
    } catch (err) {
      console.error('Prefetch failed for', locale, err)
      status.value[locale] = 'error'
    }
  }
  
  // Sidebar re-filter
  filterSidebarByLocales()
}
```

### 20-4.4: UI Feedback

```vue
<template>
  <div class="language-settings">
    <!-- ... Checkboxen wie in Plan 20-1 ... -->
    
    <div v-for="locale in selected" :key="locale" class="locale-status">
      <span v-if="status[locale] === 'downloading'">
        ⏳ {{ LOCALE_NAMES[locale] }} wird heruntergeladen...
      </span>
      <span v-else-if="status[locale] === 'done'" class="done">
        ✓ {{ LOCALE_NAMES[locale] }} offline verfügbar
      </span>
      <span v-else-if="status[locale] === 'error'" class="error">
        ⚠ {{ LOCALE_NAMES[locale] }} — Download fehlgeschlagen
      </span>
    </div>
  </div>
</template>
```

## Verification

```bash
npm run docs:build
npm run docs:dev

# 1. Settings: Aktiviere EN (war deaktiviert)
# 2. UI zeigt "⏳ English wird heruntergeladen..."
# 3. DevTools → Network → viele Requests (Lektionen werden geladen)
# 4. UI zeigt "✓ English offline verfügbar"
# 5. DevTools → Cache Storage → /en/ URLs sind enthalten
# 6. Browser offline schalten → /en/lektion/05/ funktioniert
# 7. Settings → Cache leeren → /en/ URLs entfernt
```

## Success Criteria

- ✅ Manifest-Dateien pro Sprache werden beim Build generiert
- ✅ Settings-Page löst Prefetch bei neuer Sprache aus
- ✅ UI zeigt Fortschritt und Erfolg/Misserfolg
- ✅ Neue Sprache ist nach Download offline verfügbar
- ✅ Sidebar wird automatisch aktualisiert
- ✅ Build erfolgreich

## Error Handling

**Keine Netzwerkverbindung beim Aktivieren**:
- User bekommt "⚠ Download fehlgeschlagen" Meldung
- Sprache trotzdem in localStorage gespeichert (wird beim nächsten Online-Besuch nachgeladen)
- UI zeigt Hinweis: "Sprache wird beim nächsten Online-Besuch geladen"

**Teilweise Download** (z.B. 50 von 61 Lektionen):
- SW cacht was er kriegt
- Beim nächsten Online-Besuch: fehlende URLs werden nachgeladen
- User kann trotzdem offline die schon gecachten Lektionen lesen

## Performance

**Erwartete Download-Zeit**:
- EN (61 Lektionen × 30KB HTML + Bilder): ~15-30 Sekunden
- Abhängig von Netzwerkgeschwindigkeit
- Progress-Bar (Plan 20-5) zeigt Fortschritt

**Parallelität**:
- SW prefetcht URLs sequenziell (kein DDoS auf Server)
- Browser-Limit: 6 parallele Requests per Origin
- Rate-Limiting: kein explizites (SW cacht so schnell wie er kann)

## Notes

- Manifest-Generation muss in `npm run docs:build` Workflow integriert werden
  (am Ende des Builds als Post-Hook)
- Manifest-Dateien werden im Root gespeichert (kein Locale-Prefix)
- Cache-Key-Format: `/manifest-{locale}.json`

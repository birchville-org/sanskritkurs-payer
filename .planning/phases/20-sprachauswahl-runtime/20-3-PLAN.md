# Plan 20-3: Service Worker selektives Caching

**Phase**: 20 Sprachauswahl (Runtime-Filter)  
**Status**: Pending  
**Dependencies**: 20-2 ✅

## Ziel

Service Worker cacht nur URLs die zu aktiven Sprachen gehören. Alle anderen URLs werden nicht im Cache gespeichert (obwohl sie angefragt werden).

## Deliverables

Modifikation: `docs/public/sw.js`

## Implementation

### Post-Message Handler für aktive Locales

```javascript
// In sw.js hinzufügen
let ACTIVE_LOCALES = ['de', 'en', 'it']  // Default

self.addEventListener('message', (event) => {
  if (event.data?.type === 'SET_ACTIVE_LOCALES') {
    ACTIVE_LOCALES = event.data.locales
    console.log('[SW] Active locales updated:', ACTIVE_LOCALES)
    
    // Alte Caches für deaktivierte Sprachen aufräumen
    cleanupInvalidatedCache(ACTIVE_LOCALES)
  }
})

async function cleanupInvalidatedCache(activeLocales) {
  const cache = await caches.open(CACHE_NAME)
  const requests = await cache.keys()
  
  for (const request of requests) {
    const url = new URL(request.url)
    if (!isUrlAllowed(url, activeLocales)) {
      await cache.delete(request)
      console.log('[SW] Evicted:', url.pathname)
    }
  }
}
```

### URL-Filter Funktion

```javascript
function isUrlAllowed(url, activeLocales) {
  const pathname = url.pathname
  
  // Immer erlaubt: Root-Assets
  if (pathname === '/' ||
      pathname === '/offline.html' ||
      pathname === '/manifest.json' ||
      pathname.startsWith('/pwa-icons/') ||
      pathname.startsWith('/assets/') ||     // CSS/JS/Fonts (shared)
      pathname.endsWith('.css') ||
      pathname.endsWith('.js') ||
      pathname.endsWith('.woff2') ||
      pathname.endsWith('.woff') ||
      pathname.endsWith('.ttf') ||
      pathname.match(/\.(png|jpg|jpeg|gif|svg|webp|ico)$/)) {
    return true
  }
  
  // Root (DE)
  if (!pathname.match(/^\/[a-z]{2}\//)) {
    return activeLocales.includes('de')
  }
  
  // Locale-spezifische URL
  const match = pathname.match(/^\/([a-z]{2})(\/|$)/)
  if (!match) return true
  
  const locale = match[1]
  return activeLocales.includes(locale)
}
```

### Fetch-Handler anpassen

```javascript
// In Cache-Strategiefunktionen prüfen:
async function networkFirst(request) {
  const url = new URL(request.url)
  
  // Wenn URL zu deaktivierter Sprache gehört: nicht cachen
  if (!isUrlAllowed(url, ACTIVE_LOCALES)) {
    console.log('[SW] Skipping cache for inactive locale:', url.pathname)
    try {
      return await fetch(request)  // Network-only für deaktivierte Sprachen
    } catch {
      return cache.match('/offline.html') || new Response('Offline', { status: 503 })
    }
  }
  
  // ... normale NetworkFirst-Logik wie in Phase 19
}
```

Analog für `cacheFirst()` und `staleWhileRevalidate()`.

### Initialisierung bei SW-Start

```javascript
// Bei activate event: Lese aktive Locales aus Cache (wenn vorhanden)
self.addEventListener('activate', (event) => {
  event.waitUntil(
    // ... bestehende Cleanup-Logik
    caches.open(CACHE_NAME).then(async cache => {
      const settingsResponse = await cache.match('/__payer_locales')
      if (settingsResponse) {
        const data = await settingsResponse.json()
        ACTIVE_LOCALES = data.locales || ACTIVE_LOCALES
      }
    }).then(() => self.clients.claim())
  )
})

// Client sendet Settings bei erstem Besuch:
self.addEventListener('message', (event) => {
  if (event.data?.type === 'SET_ACTIVE_LOCALES') {
    ACTIVE_LOCALES = event.data.locales
    // Persistiere in Cache für SW-Restart
    caches.open(CACHE_NAME).then(cache => {
      cache.put('/__payer_locales', new Response(JSON.stringify({
        locales: ACTIVE_LOCALES,
        updated: Date.now()
      }), { headers: { 'Content-Type': 'application/json' }}))
    })
    cleanupInvalidatedCache(ACTIVE_LOCALES)
  }
})
```

## Scope-Überlegungen

**Caching-Strategie pro URL-Typ**:

| URL | Wenn Sprache aktiv | Wenn Sprache inaktiv |
|-----|-------------------|---------------------|
| `/en/lektion/01/` | NetworkFirst + Cache | Network-only (kein Cache) |
| `/assets/chunks/framework.js` | CacheFirst (shared) | CacheFirst (shared, immer) |
| `/en/images/...` | StaleWhileRevalidate | Network-only (kein Cache) |
| `/offline.html` | Pre-cached immer | Pre-cached immer |

**Warum `/offline.html` bei inaktiver Sprache zeigen?**
User könnte per direktem Link `/en/lektion/99/` offline aufrufen. Da Sprache nicht gecacht ist, sollte die Fallback-Page kommen statt leerem Response.

## Verification

```bash
npm run docs:build
npm run docs:dev

# 1. Settings: Deaktiviere EN, speichere
# 2. DevTools → Application → Cache Storage → payer-cache-v19-r1
# 3. Navigiere zu /en/lektion/01/ (solange online!)
# 4. Refresh → Cache enthält /en/lektion/01/ NICHT
# 5. Settings: Aktiviere EN erneut
# 6. Navigiere zu /en/lektion/01/
# 7. Refresh → Cache enthält /en/lektion/01/ jetzt
# 8. Console: "[SW] Active locales updated: [de,en,it]"
# 9. Console: "[SW] Evicted: ..." beim Deaktivieren
```

## Success Criteria

- ✅ Post-Message Handler empfängt Locale-Updates
- ✅ Persistenz via `/__payer_locales` Cache-Entry
- ✅ Inaktive Sprachen werden nicht gecacht (network-only)
- ✅ Alte Cache-Einträge für deaktivierte Sprachen werden gelöscht
- ✅ Assets (CSS/JS/Fonts) bleiben immer gecacht (shared)
- ✅ offline.html Fallback für deaktivierte URLs funktioniert
- ✅ Build erfolgreich

## Security Notes

- `__payer_locales` ist ein interner Cache-Key (nicht per URL erreichbar)
- Client-seitige Settings können manipuliert werden — aber nur für diesen Client
- Kein Server-Risiko (Cache ist client-lokal)

## Notes

- Cache-Verknappung: Bei 3 aktiven Sprachen wird nur ~70MB gecacht (vs. ~500MB bei allen 14)
- Safari iOS Cache-Limit: 1GB, 7-Tage-Purge — irrelevant bei 70MB
- Post-Message-API ist robust (auch bei SW-Neustart via localStorage-Fallback)

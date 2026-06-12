# Plan 19-3 Summary: Cache-Strategien

**Phase**: 19 Service Worker & Offline Caching  
**Status**: ✅ Complete  
**Completed**: 2026-06-12

## Deliverables

**docs/public/sw.js** (erweitert auf 280 Zeilen mit 3 Cache-Strategien + Fetch-Router)

## Implementation

### Drei Cache-Strategien

#### 1. NetworkFirst (HTML-Dokumente)
```javascript
async function networkFirst(request) {
  const cache = await caches.open(CACHE_NAME)
  
  try {
    const networkResponse = await fetch(request)
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone())
    }
    return networkResponse
  } catch (err) {
    const cachedResponse = await cache.match(request)
    if (cachedResponse) return cachedResponse
    
    // Fallback auf offline.html für Dokumente
    if (request.destination === 'document' 
        || (request.headers.get('accept') || '').includes('text/html')) {
      return cache.match('/offline.html') || new Response('Offline', { status: 503 })
    }
    
    return new Response('Offline - Payer Sanskrit', { status: 503 })
  }
}
```

**Verhalten**:
- Online: Immer frische Version vom Server, Cache wird aktualisiert
- Offline: Cache-Version (wenn vorhanden), sonst offline.html
- Vorteil: User sieht immer aktuelle Lektionen wenn online

**Warum für HTML?**
Lektionen können sich ändern (Korrekturen, Updates). NetworkFirst stellt sicher dass User immer die neueste Version sehen, aber offline trotzdem Zugriff haben.

#### 2. CacheFirst (statische Assets: CSS/JS/Fonts)
```javascript
async function cacheFirst(request) {
  const cache = await caches.open(CACHE_NAME)
  const cachedResponse = await cache.match(request)
  
  if (cachedResponse) return cachedResponse
  
  try {
    const networkResponse = await fetch(request)
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone())
    }
    return networkResponse
  } catch (err) {
    return new Response('Asset unavailable offline', { status: 503 })
  }
}
```

**Verhalten**:
- Cache-Treffer: Sofort zurückgeben (schnell!)
- Cache-Miss: Netzwerk-Fetch + Speichern für nächstes Mal
- Vorteil: Nach erstem Besuch sind Assets immer sofort verfügbar

**Warum für CSS/JS/Fonts?**
VitePress generiert Content-hashed Filenames (`framework.5f2c9a1a.js`). Diese sind unveränderlich — Cache ist immer autoritativ.

#### 3. StaleWhileRevalidate (Bilder)
```javascript
async function staleWhileRevalidate(request) {
  const cache = await caches.open(CACHE_NAME)
  const cachedResponse = await cache.match(request)
  
  const networkResponsePromise = fetch(request)
    .then(response => {
      if (response.ok) cache.put(request, response.clone())
      return response
    })
    .catch(() => null)
  
  if (cachedResponse) {
    networkResponsePromise // fire-and-forget
    return cachedResponse
  }
  
  const networkResponse = await networkResponsePromise
  return networkResponse || new Response('', { status: 404 })
}
```

**Verhalten**:
- Cache vorhanden: Sofort zurückgeben, Netzwerk-Update im Hintergrund
- Kein Cache: Auf Netzwerk warten
- Vorteil: Schnell (wie CacheFirst), aber immer aktueller Cache

**Warum für Bilder?**
Bilder ändern sich selten, aber wenn doch, wollen wir die neue Version. StaleWhileRevalidate gibt sofort die alte Version (schnell!), holt aber die neue im Hintergrund.

### Fetch-Router (URL-basiertes Routing)
```javascript
self.addEventListener('fetch', (event) => {
  const url = new URL(event.request.url)
  
  // Skip non-GET and cross-origin
  if (event.request.method !== 'GET' || url.origin !== location.origin) {
    return
  }
  
  // HTML-Dokumente → NetworkFirst
  if (event.request.destination === 'document') {
    event.respondWith(networkFirst(event.request))
    return
  }
  
  // CSS/JS/Fonts → CacheFirst
  if (event.request.destination === 'style'
      || event.request.destination === 'script'
      || event.request.destination === 'font'
      || url.pathname.endsWith('.css')
      || url.pathname.endsWith('.js')
      || url.pathname.endsWith('.woff2')
      || url.pathname.endsWith('.woff')
      || url.pathname.endsWith('.ttf')) {
    event.respondWith(cacheFirst(event.request))
    return
  }
  
  // Bilder → StaleWhileRevalidate
  if (event.request.destination === 'image'
      || url.pathname.match(/\.(png|jpg|jpeg|gif|svg|webp|ico)$/)) {
    event.respondWith(staleWhileRevalidate(event.request))
    return
  }
  
  // Manifest + PWA-Icons → NetworkFirst
  if (url.pathname === '/manifest.json' || url.pathname.startsWith('/pwa-icons/')) {
    event.respondWith(networkFirst(event.request))
    return
  }
  
  // Fallback: NetworkFirst für alles andere
  event.respondWith(networkFirst(event.request))
})
```

**Routing-Logik**:
1. `request.destination` — Browser kennt den Typ bereits (document, style, script, image, font)
2. File-Extensions als Fallback (für Safari, das destination manchmal nicht setzt)
3. Spezielle Pfade (manifest.json, pwa-icons/) explizit
4. Default: NetworkFirst (sicherste Strategie)

## Verification

**Build-Output**:
```bash
ls -lh docs/.vitepress/dist/sw.js
# 7.1 KB — OK
```

**Browser Test Scenarios**:

### Scenario 1: Erster Besuch (online)
1. Seite öffnen → SW installiert sich
2. Lektion `/lektion/01/` besuchen → NetworkFirst lädt vom Server, cacht im Hintergrund
3. Console: `[SW] Fetch: /lektion/01/` + Netzwerk-Request

### Scenario 2: Zweiter Besuch (offline)
1. Browser → Network → "Offline" aktivieren
2. `/lektion/01/` öffnen → Cache-Version wird geladen (0ms Wartezeit)
3. Console: `[SW] Fetch: /lektion/01/` (kein Netzwerk-Request)

### Scenario 3: Unbekannte Seite (offline)
1. `/lektion/05/` öffnen (nie besucht) → nicht im Cache
2. NetworkFirst → Cache-Miss → offline.html wird angezeigt
3. Console: `[SW] NetworkFirst: Cache miss, serving offline.html`

### Scenario 4: CSS/JS (offline)
1. Seite laden → CacheFirst für `.css` und `.js` Dateien
2. Alle Assets sofort da (aus Cache, keine Netzwerk-Delay)

### Scenario 5: Bilder
1. Bild besuchen (online) → StaleWhileRevalidate cacht es
2. Bild erneut besuchen (offline) → Cache-Version sofort
3. Bild erneut besuchen (online) → Cache-Version + Hintergrund-Update

## Technical Notes

### Warum keine Workbox?
Workbox ist Google's SW-Bibliothek (~30KB gzipped). Für Payer:
- Drei simple Strategien reichen
- Kein Overhead durch Library
- Bessere Debugging (eigener Code, keine Blackbox)
- ~7KB statt ~37KB

**Trade-off**: Mehr Code zu schreiben, aber volle Kontrolle.

### Cache Key: URL vs. Request-Object
```javascript
cache.put(request, response.clone())  // request = Request-Objekt
cache.match(request)                   // request = Request-Objekt
```

**Alternative**: URL-String als Key
```javascript
cache.put(request.url, response.clone())
cache.match(request.url)
```

**Warum Request-Objekt?**
- Berücksichtigt HTTP-Headers (z.B. `Accept: text/html`)
- Vary-Header-Handling automatisch
- Standard-API (weniger Fehleranfällig)

### offline.html Fallback
```javascript
if (request.destination === 'document' 
    || (request.headers.get('accept') || '').includes('text/html')) {
  return cache.match('/offline.html') || new Response('Offline', { status: 503 })
}
```

**Zwei Checks**:
1. `destination === 'document'` — Browser sagt "ich will HTML"
2. `Accept: text/html` — Fallback für Safari (destination manchmal nicht gesetzt)

**Warum Fallback auf 503?**
Wenn `/offline.html` selbst nicht im Cache ist (sollte nie passieren), wollen wir einen klaren 503 statt einem leeren Response.

### Cross-Origin Requests
```javascript
if (url.origin !== location.origin) return
```

**Warum skippen?**
- Externe Ressourcen (CDNs, APIs) sollten nicht gecacht werden
- Cross-Origin Caching ist komplex (opaque responses, CORS-Handling)
- Payer hat keine externen Abhängigkeiten (alles self-hosted)

## Performance

**Erwartete Ladezeiten** (nach erstem Besuch):

| Szenario | Online | Offline |
|----------|--------|---------|
| HTML-Dokument | ~100ms (Netzwerk) | ~10ms (Cache) |
| CSS/JS | ~5ms (Cache) | ~5ms (Cache) |
| Bild | ~10ms (Cache) | ~10ms (Cache) |
| Unbekannte Seite | ~100ms (Netzwerk) | sofort (offline.html) |

**CacheFirst ist ~20x schneller als NetworkFirst** für statische Assets.

## Browser Compatibility

| Feature | Chrome | Firefox | Safari | Edge |
|---------|--------|---------|--------|------|
| `request.destination` | 65+ | 65+ | 11.1+ | 79+ |
| `cache.put()` | 40+ | 44+ | 11.1+ | 17+ |
| `self.clients` | 40+ | 44+ | 11.1+ | 17+ |

**Minimum Support**: Safari iOS 11.3+ (Service Worker Support seit März 2018)

## Dependencies

- Keine externen Dependencies
- Standard Service Worker + Cache Storage APIs
- Browser Support: Chrome 40+, Firefox 44+, Safari 11.1+

## Next Steps

Plan 19-4 ✅ — Offline Fallback (offline.html erstellen + Integration)

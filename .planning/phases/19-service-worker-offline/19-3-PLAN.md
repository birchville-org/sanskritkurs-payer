# Plan 19-3: Cache-Strategien implementieren

**Phase**: 19 Service Worker & Offline Caching  
**Status**: Pending  
**Dependencies**: 19-2 ✅  
**Referenz**: ARCHITECTURE.md Abschnitt 5.2

## Ziel

Intelligente Cache-Strategien für verschiedene Asset-Typen implementieren gemäß Architektur-Dokument.

## Strategie-Übersicht

| Asset-Typ | Strategie | Begründung |
|-----------|-----------|------------|
| **HTML (Dokumente)** | NetworkFirst | Immer aktuell, Fallback auf Cache |
| **CSS/JS/Fonts** | CacheFirst | Unveränderlich (Version in URL), schnell |
| **Bilder** | StaleWhileRevalidate | Sofort laden, im Hintergrund aktualisieren |
| **API/Ajax** | NetworkOnly (oder optional NetworkFirst) | Dynamische Daten |

## Tasks

### 19-3.1: Strategie-Helfer-Funktionen implementieren

**Datei**: `docs/public/sw.js`

Die drei Strategien als wiederverwendbare Funktionen im Service Worker:

#### NetworkFirst (für HTML)

```javascript
async function networkFirst(request) {
  const cache = await caches.open(CACHE_NAME)
  
  try {
    // Versuche Netzwerk
    const networkResponse = await fetch(request)
    
    // Bei Erfolg: Update Cache
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone())
    }
    
    return networkResponse
  } catch (err) {
    // Netzwerk-Fehler: Fallback auf Cache
    console.log('[SW] Network failed, using cache for:', request.url)
    const cachedResponse = await cache.match(request)
    
    if (cachedResponse) {
      return cachedResponse
    }
    
    // Kein Cache-Eintrag: Fallback auf offline.html
    if (request.destination === 'document') {
      return cache.match('/offline.html')
    }
    
    // Kein Fallback verfügbar
    return new Response('Offline - Payer Sanskrit', {
      status: 503,
      statusText: 'Service Unavailable',
      headers: { 'Content-Type': 'text/plain' }
    })
  }
}
```

#### CacheFirst (für statische Assets)

```javascript
async function cacheFirst(request) {
  const cache = await caches.open(CACHE_NAME)
  
  // Erst Cache prüfen
  const cachedResponse = await cache.match(request)
  
  if (cachedResponse) {
    // Cache-Treffer: sofort zurückgeben
    return cachedResponse
  }
  
  // Kein Cache: Netzwerk-Fetch + Speichern
  try {
    const networkResponse = await fetch(request)
    
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone())
    }
    
    return networkResponse
  } catch (err) {
    return new Response('Asset unavailable offline', {
      status: 503,
      statusText: 'Service Unavailable'
    })
  }
}
```

#### StaleWhileRevalidate (für Bilder)

```javascript
async function staleWhileRevalidate(request) {
  const cache = await caches.open(CACHE_NAME)
  
  // Sofort aus Cache (wenn vorhanden)
  const cachedResponse = await cache.match(request)
  
  // Parallel: Cache zurückgeben UND Netzwerk-Fetch starten
  const networkResponsePromise = fetch(request).then((response) => {
    if (response.ok) {
      cache.put(request, response.clone())
    }
    return response
  }).catch(() => null) // Netzwerk-Fehler ignorieren
  
  // Wenn Cache vorhanden: zurückgeben, Netzwerk im Hintergrund
  if (cachedResponse) {
    networkResponsePromise // Fire and forget
    return cachedResponse
  }
  
  // Kein Cache: warte auf Netzwerk
  const networkResponse = await networkResponsePromise
  
  if (networkResponse) {
    return networkResponse
  }
  
  // Fallback: leeres Response
  return new Response('', { status: 404 })
}
```

### 19-3.2: Fetch-Handler mit Routing-Logik

Ersetze den Placeholder `fetch(event.request)` in sw.js (Plan 19-2):

```javascript
self.addEventListener('fetch', (event) => {
  const request = event.request
  const url = new URL(request.url)
  
  // Nur gleich-origin Requests cachen
  if (url.origin !== location.origin) {
    return
  }
  
  // Ignoriere non-GET Requests (z.B. POST bei Formularen)
  if (request.method !== 'GET') {
    return
  }
  
  // Routing-Logik:
  
  // 1. HTML-Dokumente → NetworkFirst
  if (request.destination === 'document') {
    event.respondWith(networkFirst(request))
    return
  }
  
  // 2. CSS/JS/Fonts → CacheFirst
  if (request.destination === 'style'
      || request.destination === 'script'
      || request.destination === 'font'
      || url.pathname.endsWith('.css')
      || url.pathname.endsWith('.js')
      || url.pathname.endsWith('.woff2')) {
    event.respondWith(cacheFirst(request))
    return
  }
  
  // 3. Bilder → StaleWhileRevalidate
  if (request.destination === 'image'
      || url.pathname.match(/\.(png|jpg|jpeg|gif|svg|webp)$/)) {
    event.respondWith(staleWhileRevalidate(request))
    return
  }
  
  // 4. Manifest + Icons → NetworkFirst
  if (url.pathname === '/manifest.json'
      || url.pathname.startsWith('/pwa-icons/')) {
    event.respondWith(networkFirst(request))
    return
  }
  
  // 5. Alles andere → NetworkFirst
  event.respondWith(networkFirst(request))
})
```

## Deliverables

**Datei**: `docs/public/sw.js` (erweitert auf ca. 200 Zeilen)

## Verification

```bash
npm run docs:build
npm run docs:dev

# Testfälle:

# 1. Online-First-Besuch einer Lektion
# Erwartet: HTML aus Netzwerk, CSS/JS aus Cache nach erstem Laden

# 2. DevTools → Network → "Offline" aktivieren
# Erwartet: Lektion lädt noch (NetworkFirst → Cache-Fallback)

# 3. Neue Lektion öffnen (offline)
# Erwartet: offline.html wird angezeigt (nicht besucht → nicht gecacht)

# 4. Bild öffnen (offline, vorher nicht besucht)
# Erwartet: 404 (Bilder auch nicht im Cache)

# 5. Bild öffnen (offline, vorher online besucht)
# Erwartet: Bild aus Cache (StaleWhileRevalidate)
```

## Success Criteria

- ✅ Drei Strategie-Funktionen implementiert
- ✅ Routing-Logik im Fetch-Handler
- ✅ HTML: online = frisch, offline = aus Cache
- ✅ CSS/JS/Fonts: nach erstem Besuch offline verfügbar
- ✅ Bilder: schneller Ladevorgang, Hintergrund-Update
- ✅ Keine Console-Errors

## Edge Cases

### 1. Same-Origin vs. Cross-Origin
- `url.origin !== location.origin` → Request ignorieren
- Verhindert Caching von externen CDNs (z.B. fonts.googleapis.com)
- Begründung: Cross-Origin Caching ist komplex (opaque responses)

### 2. VitePress-Build-Artefakte mit Content-Hash
VitePress generiert Dateien wie `assets/chunks/framework.5f2c9a1a.js`.  
Der Hash ändert sich bei jedem Build → Cache-Strategie muss alte Einträge aufräumen.

**Lösung**: Activate-Handler (Plan 19-2) löscht gesamten alten Cache. Neue URLs werden beim ersten Besuch neu gecacht.

### 3. Query Parameters (z.B. ?v=1.0)
- `cache.match(request)` berücksichtigt per default Query-Params
- Falls Query-Params ignoriert werden sollen: `cache.match(request, { ignoreSearch: true })`

**Entscheidung für Payer**: Standard-Verhalten (Query-Params relevant)

## Performance-Erwartungen

| Szenario | Erwartete Ladezeit |
|----------|-------------------|
| Online, erster Besuch | ~500ms (NetworkFirst) |
| Online, revisited | ~50ms (CacheFirst für Assets) |
| Offline, bekanntes Doc | ~100ms (Cache-Serve) |
| Offline, unbekanntes Doc | sofort offline.html |

## Notes

- Keine Workbox-Abhängigkeit (Pure-Implementierung, ca. 150 Zeilen)
- Strategie-Logik ist einfach debugbar (klare Funktionsgrenzen)
- Bei späterer Erweiterung (z.B. Background-Sync) kann Workbox hinzugefügt werden

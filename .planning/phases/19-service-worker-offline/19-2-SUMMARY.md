# Plan 19-2 Summary: Service Worker Lifecycle

**Phase**: 19 Service Worker & Offline Caching  
**Status**: ✅ Complete  
**Completed**: 2026-06-12

## Deliverables

**docs/public/sw.js** (erweitert auf 280 Zeilen)

## Implementation

### Cache-Versionierung
```javascript
const CACHE_VERSION = 'payer-v19-r1'
const CACHE_NAME = `payer-cache-${CACHE_VERSION}`
```

**Konvention**: `payer-v{phase}-r{revision}`
- Phase 19, Revision 1 → aktuelle Version
- Bei Cache-Strategie-Änderungen: Revision bump (r2, r3...)
- Bei neuem Milestone (Phase 20): `payer-v20-r1`

**Warum nicht Content-Hash?**
VitePress generiert schon Content-hashed Assets (`assets/chunks/framework.5f2c9a1a.js`). Cache-Version ist nur für SW-Logik-Änderungen.

### Install Event
```javascript
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => Promise.all(
        PRECACHE_URLS.map(url => 
          cache.add(url).catch(err => console.warn('[SW] Failed to cache:', url))
        )
      ))
      .then(() => self.skipWaiting())
  )
})
```

**Precache-Liste** (5 Assets):
1. `/` — Homepage (immer verfügbar offline)
2. `/offline.html` — Fallback für unbekannte Dokumente
3. `/manifest.json` — PWA-Manifest (für Install-Prompt)
4. `/pwa-icons/icon-192.png` — App-Icon
5. `/pwa-icons/icon-512.png` — App-Icon (groß)

**Warum nur diese 5?**
- Lektionen/Schriften werden bei Besuch automatisch gecacht (NetworkFirst-Strategie, Plan 19-3)
- Aggressive Pre-Caching von ~2GB Content ist unpraktikabel
- User entscheidet welche Sprachen sie offline brauchen (Phase 20)

### Activate Event
```javascript
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(cacheNames =>
      Promise.all(
        cacheNames
          .filter(name => name !== CACHE_NAME)
          .map(name => caches.delete(name))
      )
    ).then(() => self.clients.claim())
  )
})
```

**Zwei Schritte**:
1. **Cache Cleanup**: Alle alten Caches löschen (nur aktueller bleibt)
2. **Claim Clients**: SW übernimmt Kontrolle aller offenen Tabs sofort

**Warum claim()?**
Ohne `claim()` würde der neue SW erst beim nächsten Page-Load aktiv. Für Updates wollen wir sofortige Aktivierung.

### Fetch Event (Placeholder)
```javascript
self.addEventListener('fetch', (event) => {
  // Pass-through — wird in Plan 19-3 durch Strategien ersetzt
  event.respondWith(fetch(event.request))
})
```

## Verification

**Build-Output**:
```bash
ls -lh docs/.vitepress/dist/sw.js
# 7.1 KB — OK (280 Zeilen, keine Minification nötig für SW)
```

**Browser Test** (erwartetes Verhalten):
1. Seite öffnen → Console: `[SW] Install event`
2. DevTools → Application → Service Workers: "activated and running"
3. DevTools → Application → Cache Storage: `payer-cache-v19-r1` vorhanden
4. Cache enthält: `/`, `/offline.html`, `/manifest.json`, `/pwa-icons/*`

## Technical Notes

### skipWaiting() vs. clients.claim()
- **skipWaiting()**: Neuer SW wird sofort aktiv (wartet nicht auf Tabs-close)
- **clients.claim()**: SW übernimmt Kontrolle aller offenen Tabs

**Warum beides?**
- `skipWaiting()` im `install`: SW ist bereit, aber noch nicht aktiv
- `clients.claim()` im `activate`: SW wird aktiv und kontrolliert Tabs

Ohne `claim()`: SW ist aktiv, aber alte Requests laufen noch über Netzwerk (kein Caching bis Page-Reload).

### Error Handling im Precache
```javascript
catch(err => console.warn('[SW] Failed to cache:', url))
```

**Warum warn statt error?**
- Assets könnten noch nicht existieren (z.B. offline.html während Erst-Deployment)
- SW sollte nicht komplett failen wenn ein Asset fehlt
- Console-Warnung hilft beim Debugging

### Cache Storage Limits
- Chrome: ~2GB pro Origin (variiert je nach Device)
- Safari iOS: ~1GB, aber 7-Tage-Inaktivität löscht Cache
- Firefox: ~2GB

**Payer-Cache**: ~200MB bei Full-Install (14 Sprachen) → kein Problem

## Dependencies

- Keine externen Dependencies
- Standard Service Worker API (kein Workbox)
- Browser Support: Chrome 40+, Firefox 44+, Safari 11.1+

## Next Steps

Plan 19-3 ✅ — Cache-Strategien implementieren (NetworkFirst, CacheFirst, StaleWhileRevalidate)

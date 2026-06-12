# Plan 19-2: Service Worker erstellen (Lebenszyklus)

**Phase**: 19 Service Worker & Offline Caching  
**Status**: Pending  
**Dependencies**: 19-1 ✅

## Ziel

Basis Service Worker erstellen mit korrektem Lebenszyklus: install, activate, fetch.

## Tasks

### 19-2.1: Service Worker Datei erstellen

**Datei**: `docs/public/sw.js`

**Kernstruktur**:
```javascript
// docs/public/sw.js

// Cache Name mit Version
const CACHE_VERSION = 'payer-v19-r1'
const CACHE_NAME = `payer-cache-${CACHE_VERSION}`

// Assets die beim Install gecacht werden (Pre-Cache)
const PRECACHE_URLS = [
  '/',
  '/offline.html',
  '/manifest.json',
  '/pwa-icons/icon-192.png',
  '/pwa-icons/icon-512.png'
]

// Install Event: Pre-Cache kritische Assets
self.addEventListener('install', (event) => {
  console.log('[SW] Install event')
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('[SW] Pre-caching assets')
        // Skip errors (assets might not exist yet)
        const proms = PRECACHE_URLS.map((url) => 
          cache.add(url).catch((err) => {
            console.warn('[SW] Failed to cache:', url, err)
          })
        )
        return Promise.all(proms)
      })
      .then(() => {
        console.log('[SW] Install complete')
        return self.skipWaiting() // Aktiviere SW sofort
      })
  )
})

// Activate Event: Alte Caches aufräumen
self.addEventListener('activate', (event) => {
  console.log('[SW] Activate event')
  
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            console.log('[SW] Deleting old cache:', cacheName)
            return caches.delete(cacheName)
          }
        })
      )
    }).then(() => {
      console.log('[SW] Activate complete')
      return self.clients.claim() // Kontrolliere alle Clients sofort
    })
  )
})

// Fetch Event: Request-Handling (Strategie kommt in 19-3)
self.addEventListener('fetch', (event) => {
  console.log('[SW] Fetch:', event.request.url)
  
  // Placeholder: Network-only für jetzt
  event.respondWith(
    fetch(event.request)
  )
})
```

### 19-2.2: Cache-Versionierung implementieren

**Warum Versionierung**:
- Bei neuem Build ändert sich der Cache-Name
- Alter Cache wird automatisch gelöscht (activate event)
- User bekommt frische Assets nach Update

**Konvention**:
```
payer-v19-r1  → Phase 19, Revision 1
payer-v19-r2  → Phase 19, Revision 2 (nach Bugfix)
payer-v20-r1  → Phase 20 (neue Features)
```

## Deliverables

1. `docs/public/sw.js` (ca. 80 Zeilen)

## Verification

```bash
npm run docs:build
npm run docs:dev

# Im Browser öffnen → DevTools → Application → Service Workers
# Erwartet:
# - "sw.js" geladen
# - Status: "activated and running"
# - Console: "[SW] Install event" + "[SW] Activate event"
```

## Success Criteria

- ✅ sw.js existiert in docs/public/
- ✅ SW wird registriert und aktiviert
- ✅ Cache wird erstellt (DevTools → Cache Storage)
- ✅ Alte Caches werden gelöscht
- ✅ skipWaiting() + clients.claim() funktionieren

## Notes

- Fetch-Event ist noch ein Passthrough (network-only)
- Cache-Strategien kommen in Plan 19-3
- Pre-Cache-Liste ist minimal (wird in 19-4 erweitert für offline.html)

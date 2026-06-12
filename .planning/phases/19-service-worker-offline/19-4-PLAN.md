# Plan 19-4: Offline Fallback Page

**Phase**: 19 Service Worker & Offline Caching  
**Status**: Pending  
**Dependencies**: 19-3 ✅

## Ziel

Benutzerfreundliche Offline-Fallback-Seite erstellen, die angezeigt wird wenn:
1. Ein Dokument noch nicht besucht wurde (nicht im Cache)
2. Der User offline ist
3. NetworkFirst-Strategie Netzwerk-Fehler erhält

## Design-Anforderungen

- **Konsistent mit Design System** (AGENTS.md §7):
  - Farben: `#0a0a0a` (Hintergrund), `#e8e4d8` (Text/Parchment)
  - Fonts: Newsreader (Serif) für Headings, Inter (Sans-Serif) für Body
  - Minimalistisch, keine Dekorationen
- **Inline CSS** (kein externes Stylesheet — muss offline funktionieren)
- **Mehrsprachig**: Zweisprachig (DE/EN) mit klarer Struktur
- **Self-contained**: Keine externen Ressourcen (keine CDN-Fonts, keine Bilder)

## Tasks

### 19-4.1: Offline-HTML-Seite erstellen

**Datei**: `docs/public/offline.html`

```html
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Offline — Sanskritkurs</title>
  <meta name="theme-color" content="#0a0a0a">
  
  <style>
    /* System Fonts (offline-verfügbar) */
    @font-face {
      font-family: 'System Serif';
      src: local('Georgia'), local('Times New Roman');
    }
    
    @font-face {
      font-family: 'System Sans';
      src: local('Helvetica Neue'), local('Arial');
    }
    
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      font-family: 'System Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      background: #0a0a0a;
      color: #e8e4d8;
      line-height: 1.6;
      display: flex;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
      padding: 2rem;
    }
    
    .container {
      max-width: 600px;
      text-align: center;
    }
    
    h1 {
      font-family: 'System Serif', Georgia, serif;
      font-size: clamp(2rem, 5vw, 3rem);
      font-weight: 300;
      margin-bottom: 1rem;
      color: #e8e4d8;
    }
    
    .devanagari {
      font-size: 4rem;
      margin-bottom: 2rem;
      opacity: 0.6;
    }
    
    p {
      font-size: 1.125rem;
      margin-bottom: 1.5rem;
      color: #c4c0b4;
    }
    
    .lang-label {
      display: inline-block;
      font-size: 0.875rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.1em;
      color: #7a7668;
      margin-bottom: 0.5rem;
    }
    
    .divider {
      width: 60px;
      height: 1px;
      background: #3a382f;
      margin: 2rem auto;
    }
    
    .hint {
      font-size: 0.9375rem;
      color: #7a7668;
      margin-top: 3rem;
    }
    
    .hint a {
      color: #c4c0b4;
      text-decoration: underline;
      text-decoration-color: #3a382f;
      text-underline-offset: 3px;
    }
    
    .hint a:hover {
      text-decoration-color: #c4c0b4;
    }
    
    .status-indicator {
      display: inline-block;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #7a7668;
      margin-right: 0.5rem;
      animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
      0%, 100% { opacity: 0.4; }
      50% { opacity: 1; }
    }
  </style>
</head>
<body>
  <div class="container">
    <div class="devanagari">ॐ</div>
    
    <h1>Sie sind offline</h1>
    
    <p>
      <span class="lang-label">Deutsch</span><br>
      Diese Seite ist noch nicht für den Offline-Zugriff verfügbar.<br>
      Bitte verbinden Sie sich mit dem Internet und laden Sie die Seite neu.
    </p>
    
    <div class="divider"></div>
    
    <p>
      <span class="lang-label">English</span><br>
      This page is not yet available offline.<br>
      Please connect to the internet and reload the page.
    </p>
    
    <p class="hint">
      <span class="status-indicator"></span>
      Warte auf Netzwerk… / Waiting for network…
    </p>
    
    <p class="hint">
      <a href="/">Zurück zur Startseite / Back to Home</a>
    </p>
  </div>
  
  <script>
    // Auto-Reload wenn Netzwerk zurück ist
    window.addEventListener('online', () => {
      window.location.reload()
    })
    
    // Optional: Prüfe alle 5 Sekunden ob Netzwerk zurück ist
    setInterval(async () => {
      try {
        const response = await fetch('/', { method: 'HEAD', cache: 'no-cache' })
        if (response.ok) {
          window.location.reload()
        }
      } catch (err) {
        // Noch offline, ignoriere
      }
    }, 5000)
  </script>
</body>
</html>
```

### 19-4.2: offline.html zu Pre-Cache-Liste hinzufügen

**Datei**: `docs/public/sw.js`

Aktualisiere `PRECACHE_URLS` Array:

```javascript
const PRECACHE_URLS = [
  '/',
  '/offline.html',          // ← NEU
  '/manifest.json',
  '/pwa-icons/icon-192.png',
  '/pwa-icons/icon-512.png'
]
```

### 19-4.3: NetworkFirst-Fallback für unbekannte Dokumente

**Datei**: `docs/public/sw.js`

In `networkFirst` Funktion (Plan 19-3), stelle sicher dass `/offline.html` zurückgegeben wird:

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
    console.log('[SW] Network failed, using cache for:', request.url)
    const cachedResponse = await cache.match(request)
    
    if (cachedResponse) {
      return cachedResponse
    }
    
    // Fallback auf offline.html für Dokumente
    if (request.destination === 'document' || request.headers.get('accept')?.includes('text/html')) {
      console.log('[SW] No cache, serving offline.html')
      return cache.match('/offline.html') || new Response('Offline', {
        status: 503,
        statusText: 'Service Unavailable'
      })
    }
    
    // Für andere Assets: 503 Response
    return new Response('Offline - Asset unavailable', {
      status: 503,
      statusText: 'Service Unavailable',
      headers: { 'Content-Type': 'text/plain' }
    })
  }
}
```

## Deliverables

1. `docs/public/offline.html` (ca. 150 Zeilen, ~8 KB)
2. Modifikation: `docs/public/sw.js` (offline.html in PRECACHE_URLS + Fallback-Logik)

## Verification

```bash
npm run docs:build
npm run docs:dev

# Testfälle:

# 1. /offline.html direkt öffnen
# Erwartet: Zweisprachige Fallback-Seite mit Om-Zeichen

# 2. Browser → DevTools → Network → "Offline" aktivieren
# 3. Noch nicht besuchte Lektion öffnen (z.B. /lektion/04/)
# Erwartet: offline.html wird angezeigt

# 4. Netzwerk wiederherstellen
# Erwartet: Seite lädt automatisch neu (JavaScript in offline.html)

# 5. Check Console:
# Erwartet: "[SW] Network failed, using cache..." + "[SW] No cache, serving offline.html"
```

## Success Criteria

- ✅ offline.html existiert und ist standalone (inline CSS/JS)
- ✅ Design System konform (Scholarly Synthesis)
- ✅ offline.html ist in Service Worker Pre-Cache
- ✅ Unbekannte Dokumente zeigen offline.html (offline)
- ✅ Auto-Reload wenn Netzwerk zurück ist
- ✅ Keine externen Ressourcen (offline-fähig)

## Browser Compatibility

| Feature | Chrome | Firefox | Safari |
|---------|--------|---------|--------|
| `@font-face local()` | ✅ | ✅ | ✅ |
| `clamp()` | 79+ | 75+ | 13.1+ |
| `window.addEventListener('online')` | ✅ | ✅ | ✅ |
| `fetch()` im Service Worker | ✅ | ✅ | ✅ (11.3+) |

**Minimum-Support**: Safari iOS 12.2+ (Service Worker Support seit 11.3)

## Notes

- Om-Zeichen (ॐ) ist Unicode, keine externe Font nötig
- System Fonts sind offline verfügbar
- Auto-Reload ist user-friendly (kein manueller Reload nötig)
- 5-Sekunden-Polling ist Backup falls 'online' Event nicht feuert

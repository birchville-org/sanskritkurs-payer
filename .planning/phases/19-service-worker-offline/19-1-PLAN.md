# Plan 19-1: Service Worker registrieren

**Phase**: 19 Service Worker & Offline Caching  
**Status**: Pending  
**Dependencies**: Phase 18 ✅

## Ziel

Service Worker in der VitePress App registrieren, damit er beim ersten Seitenaufruf installiert wird.

## Tasks

### 19-1.1: Service Worker Registration Script erstellen

**Datei**: `docs/.vitepress/theme/sw-register.js`

**Anforderungen**:
- Prüft ob `navigator.serviceWorker` verfügbar ist
- Registriert `/sw.js` beim ersten Seitenaufruf
- Handelt Updates korrekt (neuer SW wartet bis alle Tabs geschlossen sind)
- Nur in Production registrieren (nicht während `npm run docs:dev`)

**Code-Template**:
```javascript
// docs/.vitepress/theme/sw-register.js

export function registerServiceWorker() {
  if (typeof window === 'undefined') return
  if (!('serviceWorker' in navigator)) return
  
  // Nur in Production (nicht localhost oder docs:dev)
  if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
    console.log('[SW] Skipping registration in dev mode')
    return
  }
  
  window.addEventListener('load', async () => {
    try {
      const registration = await navigator.serviceWorker.register('/sw.js', {
        scope: '/'
      })
      
      console.log('[SW] Registered:', registration.scope)
      
      // Handle updates
      registration.addEventListener('updatefound', () => {
        const newWorker = registration.installing
        console.log('[SW] New worker found, installing...')
        
        newWorker.addEventListener('statechange', () => {
          if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
            console.log('[SW] New content available, refresh to update')
            // Optional: Show update notification
          }
        })
      })
    } catch (error) {
      console.error('[SW] Registration failed:', error)
    }
  })
}
```

### 19-1.2: Registration in VitePress Theme einbinden

**Datei**: `docs/.vitepress/theme/index.mjs`

**Änderung**:
- Importiere `registerServiceWorker` aus `./sw-register.js`
- Rufe es in `setup()` oder `onMounted()` auf

**Code**:
```javascript
import { registerServiceWorker } from './sw-register.js'

export default {
  setup() {
    if (typeof window !== 'undefined') {
      registerServiceWorker()
    }
  }
}
```

## Deliverables

1. `docs/.vitepress/theme/sw-register.js` (ca. 30 Zeilen)
2. Modifikation: `docs/.vitepress/theme/index.mjs`

## Verification

```bash
# 1. Build ausführen
npm run docs:build

# 2. Dev-Server starten (simuliert Production)
npm run docs:dev

# 3. Im Browser öffnen (Chrome DevTools → Application → Service Workers)
# Erwartet: "Service Worker not found" (weil localhost)

# 4. Mit ngrok oder ähnlichem Tool auf echter Domain testen
# Erwartet: "Service Worker registered" in Console
```

## Success Criteria

- ✅ Registration Script existiert
- ✅ Script wird in theme/index.mjs eingebunden
- ✅ Registration funktioniert auf echter Domain (nicht localhost)
- ✅ Keine Console Errors
- ✅ Build erfolgreich

## Notes

- Service Worker wird später in Phase 19-2 erstellt
- Aktuell wird die Registration vorbereitet, aber sw.js existiert noch nicht
- Das ist OK — Browser ignoriert fehlende sw.js mit 404 (kein Fehler)

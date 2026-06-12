# Plan 20-5: Progress-Bar für Pre-Caching

**Phase**: 20 Sprachauswahl (Runtime-Filter)  
**Status**: Pending  
**Dependencies**: 20-4 ✅

## Ziel

Bei PWA-Installation (Klick auf "App installieren") soll der User eine Progress-Bar sehen, die den Download-Fortschritt der aktiven Sprachen anzeigt.

## Background

Laut Entscheidung **D8** (CONTEXT.md):
- Pre-Cache ist **aggressiv** (alles beim Install, ~70MB, ~30-60s)
- User sieht Fortschrittsanzeige unten-rechts
- Erwartetes Verhalten: User klickt "Installieren" → App ist danach offline voll nutzbar

## Deliverables

1. Modifikation: `docs/.vitepress/theme/index.mjs` (Install-Prompt-Block)
2. CSS in `docs/.vitepress/theme/custom.css` (Progress-Bar-Styles)
3. Modifikation: `docs/public/sw.js` (Progress-Events an Client)

## Implementation

### 20-5.1: Progress-Bar UI

```html
<div class="pwa-progress-overlay" style="display: none;">
  <div class="pwa-progress-container">
    <div class="pwa-progress-title">App wird vorbereitet...</div>
    <div class="pwa-progress-bar">
      <div class="pwa-progress-fill" style="width: 0%"></div>
    </div>
    <div class="pwa-progress-info">
      <span class="pwa-progress-percent">0%</span>
      <span class="pwa-progress-detail">Initialisiere...</span>
    </div>
  </div>
</div>
```

### 20-5.2: CSS in custom.css

```css
.pwa-progress-overlay {
  position: fixed;
  bottom: 16px;
  right: 16px;
  z-index: 10000;
  background: var(--vp-c-bg);
  border: 1px solid var(--vp-c-divider);
  border-radius: 8px;
  padding: 16px 20px;
  min-width: 320px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
  font-family: 'Inter', sans-serif;
}

.pwa-progress-title {
  font-size: 14px;
  font-weight: 600;
  color: var(--vp-c-text-1);
  margin-bottom: 12px;
}

.pwa-progress-bar {
  height: 6px;
  background: var(--vp-c-divider);
  border-radius: 3px;
  overflow: hidden;
  margin-bottom: 8px;
}

.pwa-progress-fill {
  height: 100%;
  background: #03192e;
  border-radius: 3px;
  transition: width 200ms ease-out;
}

.dark .pwa-progress-fill {
  background: #4a9eff;
}

.pwa-progress-info {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  color: var(--vp-c-text-2);
}

.pwa-progress-percent {
  font-weight: 600;
}
```

### 20-5.3: Integration in Install-Prompt-Flow

In `index.mjs`, den `beforeinstallprompt` Handler erweitern:

```javascript
import { getActiveLocales } from './lang-settings.js'

// Install-Button Click Handler
btn.addEventListener('click', async () => {
  if (!deferredPrompt) return
  
  // Overlay anzeigen
  const overlay = document.querySelector('.pwa-progress-overlay')
  overlay.style.display = 'block'
  
  // Aktive Locales ermitteln (Fallback auf defaults)
  const activeLocales = getActiveLocales()
  
  // Manifest-URLs für alle aktiven Locales sammeln
  const urlsToCache = []
  for (const locale of activeLocales) {
    try {
      const manifestUrl = locale === 'de' ? '/manifest-de.json' : `/manifest-${locale}.json`
      const response = await fetch(manifestUrl)
      const manifest = await response.json()
      urlsToCache.push(...manifest.urls)
    } catch (err) {
      console.warn('[PWA] Could not load manifest for', locale, err)
    }
  }
  
  // Pre-Caching via SW starten
  const cacheStart = Date.now()
  navigator.serviceWorker.controller.postMessage({
    type: 'PREFETCH_LOCALE_BATCH',
    urls: urlsToCache,
    reportProgress: true
  })
  
  // Progress-Handler
  navigator.serviceWorker.addEventListener('message', (event) => {
    if (event.data?.type === 'PREFETCH_PROGRESS') {
      const { cached, total, currentUrl } = event.data
      const percent = Math.round((cached / total) * 100)
      
      document.querySelector('.pwa-progress-fill').style.width = `${percent}%`
      document.querySelector('.pwa-progress-percent').textContent = `${percent}%`
      document.querySelector('.pwa-progress-detail').textContent = 
        `${cached}/${total} Seiten`
    }
    
    if (event.data?.type === 'PREFETCH_COMPLETE_BATCH') {
      document.querySelector('.pwa-progress-detail').textContent = 'Fertig!'
      setTimeout(() => {
        overlay.style.display = 'none'
      }, 2000)
    }
  })
  
  // Browser-Install-Prompt zeigen
  deferredPrompt.prompt()
  await deferredPrompt.userChoice
  deferredPrompt = null
  btn.style.display = 'none'
})
```

### 20-5.4: Service Worker Progress-Reporting

```javascript
// In sw.js

self.addEventListener('message', (event) => {
  if (event.data?.type === 'PREFETCH_LOCALE_BATCH') {
    const { urls, reportProgress } = event.data
    const total = urls.length
    let cached = 0
    
    prefetchWithProgress(urls, (url) => {
      cached++
      if (reportProgress && event.source) {
        event.source.postMessage({
          type: 'PREFETCH_PROGRESS',
          cached,
          total,
          currentUrl: url
        })
      }
    }).then(() => {
      if (event.source) {
        event.source.postMessage({
          type: 'PREFETCH_COMPLETE_BATCH',
          total,
          cached
        })
      }
    })
  }
})

async function prefetchWithProgress(urls, onProgress) {
  const cache = await caches.open(CACHE_NAME)
  
  // Sequentiell für sauberen Progress
  for (const url of urls) {
    try {
      const response = await fetch(url)
      if (response.ok) {
        await cache.put(url, response)
      }
    } catch (err) {
      console.warn('[SW] Prefetch failed:', url, err.message)
    }
    onProgress(url)
  }
}
```

## Alternative: Web Worker für schnelleres Pre-Caching

**Sequentielles Prefetch** ist langsam aber robust (~30-60s für 70MB).

**Paralleles Prefetch** (4-6 Requests gleichzeitig):
- Schneller: ~10-20s
- Komplexer: Progress-Berechnung schwieriger
- Network-Overhead: könnte Server belasten

**Empfehlung**: Sequentiell starten, später optimieren wenn nötig.

## Verification

```bash
npm run docs:build
npm run docs:dev

# Chrome DevTools öffnen, Application → Manifest prüfen
# Installation-Trigger (z.B. über Lighthouse "Installability checks")
# Oder Chrome-Feature-Flag: chrome://flags → "PWA install" forcieren

# Erwartet:
# 1. "App installieren" Button erscheint
# 2. Klick → Overlay mit Progress-Bar erscheint
# 3. Bar füllt sich 0% → 100%
# 4. Text: "32/183 Seiten", "183/183 Seiten", "Fertig!"
# 5. Browser zeigt nativen Install-Dialog
# 6. Nach Installation: Overlay verschwindet
# 7. App öffnen offline → alle aktiven Sprachen verfügbar
```

## Success Criteria

- ✅ Progress-Bar Overlay erscheint beim Install-Klick
- ✅ Prozent-Counter aktualisiert live
- ✅ Detail-Anzeige zeigt "N/Total Seiten"
- ✅ Prefetch läuft im Hintergrund während Browser Install-Dialog zeigt
- ✅ Nach Installation: alle aktiven Sprachen im Cache
- ✅ Cache-Größe nach Installation: ~70MB (für 3 aktive Sprachen)
- ✅ Build erfolgreich

## Performance-Ziele

| Aktiv | Sprachen | URLs | Zeit | Größe |
|-------|----------|------|------|-------|
| 1 Sprache (DE) | de | ~183 Seiten | ~10s | ~23 MB |
| 3 Sprachen | de/en/it | ~549 Seiten | ~30s | ~70 MB |
| 5 Sprachen | de/en/it/fr/es | ~915 Seiten | ~50s | ~115 MB |

**Timeout nach 2 Minuten**: Wenn Prefetch nicht fertig wird, Installation trotzdem erlauben, User sieht "Download im Hintergrund" Hinweis.

## Error Handling

**Keine aktive Sprache ausgewählt**:
- Fallback auf Defaults (de, en, it)
- Progress zeigt "Initialisiere..." bevor Manifests geladen sind

**Manifest 404**:
- Sprache wird übersprungen (Console-Warnung)
- Progress-Bar läuft weiter mit anderen Sprachen
- Post-Install: "Einige Sprachen konnten nicht geladen werden" Hinweis

**Netzwerk-Abbruch mitten im Prefetch**:
- Bereits gecachte URLs bleiben im Cache
- Rest wird beim nächsten Online-Besuch nachgeladen (Plan 20-4)
- Installation wird trotzdem abgeschlossen

## Notes

- Progress-Reporting ist approximativ (SW cacht was er kriegt, nicht zwingend alles)
- Installation-Prompt kann vom Browser jederzeit geschlossen werden — Prefetch läuft weiter im SW
- Overlay hat `z-index: 10000` um über allem zu sein
- Post-Install: Install-Button wird ausgeblendet (Plan 18-3)

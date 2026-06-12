# Plan 18-3 Summary: Install-Prompt UI

**Phase:** 18-pwa-offline-app  
**Plan:** 03  
**Status:** ✅ Complete  
**Completed:** 2026-06-12

## Deliverable

PWA Install-Prompt UI in `docs/.vitepress/theme/` (JS + CSS).

## Implementation

### index.mjs (docs/.vitepress/theme/index.mjs)

- `onMounted` von Vue importiert
- PWA Install-Prompt Block in `setup()`:
  - `beforeinstallprompt` → fängt Event ab, verhindert nativen Browser-Banner
  - `appinstalled` → versteckt Button nach Installation
  - `(display-mode: standalone)` → Button bleibt versteckt wenn App schon installiert ist
  - Button wird mit `document.createElement` + `document.body.appendChild` erzeugt
  - `aria-label` für Accessibility gesetzt
- Integration in bestehende `setup()` Logik

### custom.css (docs/.vitepress/theme/custom.css)

- `.pwa-install-btn` Styles:
  - Position: fixed, bottom-right, z-index: 9999
  - Colors: #03192e bg, #fcf9f2 text (scholarly design system konform)
  - Font: Inter / system sans-serif, 14px
  - Border-radius: 8px
  - Animation: `pwa-fadeIn` 200ms ease-out
- Dark Mode overrides (`.dark .pwa-install-btn`)
- Hover State: hellerer Blau-Ton

## Verification

- 10 Matches für PWA-Keywords in index.mjs ✅
- Build erfolgreich (132.12s) ✅
- CSS enthält alle relevanten Styles ✅

## Notes

- Der Button wird erst erscheinen wenn ein Service Worker aktiv ist (Phase 19)
- Aktuell: Manifest + Meta-Tags sind da, aber ohne SW gibt Chrome keinen beforeinstallprompt
- Deshalb visuell erst verifizierbar nach Phase 19

## Files Modified

- `docs/.vitepress/theme/index.mjs` (onMounted import + PWA-Block in setup())
- `docs/.vitepress/theme/custom.css` (.pwa-install-btn + dark mode + fadeIn keyframes)

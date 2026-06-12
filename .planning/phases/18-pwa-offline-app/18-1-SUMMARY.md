# Plan 18-1 Summary: PWA Foundation & Manifest

**Phase:** 18-pwa-offline-app  
**Plan:** 01  
**Status:** ✅ Complete  
**Completed:** 2026-06-12

## Deliverables

### Artifacts
- `docs/public/pwa-icons/icon-192.png` (7.9 KB)
- `docs/public/pwa-icons/icon-256.png` (11 KB)
- `docs/public/pwa-icons/icon-384.png` (17 KB)
- `docs/public/pwa-icons/icon-512.png` (24 KB)
- `docs/public/manifest.json` (634 B)

### Design
- Background: `#03192e` (Deep Ink — Primary aus Design System)
- Foreground: `#fcf9f2` (Parchment), Devanāgarī "ॐ" (Om)
- Font: NotoSansDevanagari (variable, macOS system font)
- Generiert via ImageMagick (Fallback, da image_generate nicht verfügbar in diesem Environment)

## Verification

| Check | Status |
|-------|--------|
| 4 PNGs vorhanden (192/256/384/512) | ✅ |
| manifest.json valide (W3C) | ✅ |
| Alle Pflichtfelder (name, short_name, start_url, display, theme_color, background_color, icons) | ✅ |
| display: standalone | ✅ |
| start_url: / | ✅ |
| 4 Icons im Manifest referenziert | ✅ |
| npm run docs:build | ✅ (124.11s, 0 errors) |
| manifest.json in Build-Output (.vitepress/dist/) | ✅ |
| Alle 4 Icons in Build-Output | ✅ |

## Decisions

- **Fallback statt image_generate**: FAL_KEY nicht konfiguriert in diesem Environment.
  ImageMagick + system Font (NotoSansDevanagari) lieferte saubere, ikonische Icons.
- **Purpose-Feld weggelassen**: `maskable` wird nicht gesetzt — das Om-Zeichen ist zentriert,
  nicht im safe-zone-Bereich. Bots könnten `maskable` später hinzufügen wenn das Icon-Design verfeinert wird.
- **orientation: "any"**: PWA soll auf Mobile (Portrait) und Desktop (Landscape) funktionieren.

## Learnings

- VitePress kopiert `docs/public/` Inhalte 1:1 in `.vitepress/dist/` während Build.
- ImageMagick `convert -font ... -annotate` funktioniert mit variable `.ttf` auf macOS.
- Für PWA-Icons: 4 Größen (192, 256, 384, 512) sind Minimum für Chrome + Safari.

## Files Modified

- `docs/public/pwa-icons/` (created, 4 PNGs)
- `docs/public/manifest.json` (created)

## Next

Plan 18-2: PWA Meta-Tags in `config.mjs` `head` injizieren.

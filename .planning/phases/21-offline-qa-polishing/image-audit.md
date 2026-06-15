# Image Audit & Optimization (Phase 21-2)

**Datum**: 15.06.2026

## 1. Initialer Zustand
- **JPG/JPEG Count**: 3126
- **PNG Count**: 15
- **SVG Count**: 18
- **Gesamtgröße `dist`**: 870 MB
- **Gesamtgröße `dist/images/`**: 54 MB

## 2. Optimierungs-Durchlauf
Alle Bilder (`> 50 KB`) wurden identifiziert und via `cwebp` (Quality: 80) nach WebP konvertiert.
- **Konvertierte Bilder**: 454 Dateien
- Die Referenzen in den entsprechenden Markdown-Dokumenten wurden automatisch auf `.webp` umgeschrieben.
- **Betroffene Markdown-Dateien**: 1753 Dateien wurden aktualisiert.

## 3. Post-Optimierungs Zustand
*(Wird nach dem anstehenden Build aktualisiert)*
- **Gesamtgröße `dist`**: TBD
- **Gesamtgröße `dist/images/`**: TBD
- **Ersparnis in %**: TBD

*Hinweis*: Die Originaldateien (.jpg, .png) wurden als Backup belassen, wie in Plan `21-2-PLAN.md` spezifiziert. Da VitePress jedoch den gesamten `/public`-Ordner in den Build übernimmt, könnte die *absolute* Build-Größe (`dist`) durch das Behalten der Originaldateien ansteigen. Für den User-Download im Offline-Modus ist dies jedoch irrelevant, da nun die wesentlich kleineren WebP-Dateien referenziert und vom Browser geladen werden.

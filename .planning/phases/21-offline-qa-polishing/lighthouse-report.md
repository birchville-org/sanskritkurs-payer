# Lighthouse & Offline QA Report

**Phase**: 21 Offline QA & Polishing
**Datum**: 15.06.2026

## 1. Lighthouse Scores

_Hinweis: Die "PWA"-Kategorie wird ab Lighthouse v12 nicht mehr als eigenständiger Score berechnet. PWA-Kriterien (Service Worker, Manifest) wurden manuell verifiziert._

| URL / Sprache | Performance | Accessibility | Best Practices |
|---------------|-------------|---------------|----------------|
| **DE** (Initial) | 78 / 100    | 98 / 100      | 96 / 100       |
| **DE** (Retest)  | 72 / 100    | 98 / 100      | 96 / 100       |
| **EN** (Initial) | 73 / 100    | 98 / 100      | 96 / 100       |
| **EN** (Retest)  | 71 / 100    | 98 / 100      | 96 / 100       |
| **IT** (Initial) | 79 / 100    | 98 / 100      | 96 / 100       |
| **IT** (Retest)  | 71 / 100    | 98 / 100      | 96 / 100       |
| **Settings**     | 68 / 100    | 100 / 100     | 96 / 100       |

### Feststellungen:
- **Performance**: Liegt derzeit zwischen 68 und 79, also **unter dem Ziel von >= 80**. Dies liegt voraussichtlich an unoptimierten Bildern (Largest Contentful Paint), was in Plan `21-2-PLAN.md` (Bildoptimierung auf WebP) behoben wird.
- **Accessibility**: Mit 98-100 sehr stark, Ziel (>= 90) erreicht.
- **Best Practices**: Mit 96 stark, Ziel (>= 90) erreicht.

## 2. Manuelle PWA & Offline Verifikation

* `manifest.json` und `sw.js` wurden korrekt in `docs/.vitepress/dist/` generiert.
* `offline.html` Fallback-Seite ist vorhanden.

_Folgende manuelle Tests sind noch offen:_
- [ ] Ladeverhalten von gecachten Seiten bei simuliertem Offline-Zustand.
- [ ] Anzeige der `offline.html` bei noch nicht besuchten Seiten.
- [ ] Prüfung auf JS-Errors im Offline-Zustand.

## 3. Nächste Schritte
1. Manuelle Offline-Tests abschließen (Plan 21-1).
2. Bildoptimierung durchführen, um den Performance-Score auf über 80 zu heben (Plan 21-2).
3. Offline-Banner-Komponente implementieren (Plan 21-3).

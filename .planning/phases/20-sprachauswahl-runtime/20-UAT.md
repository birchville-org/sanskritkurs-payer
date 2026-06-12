# User Acceptance Testing — Phase 20 (Sprachauswahl Runtime-Filter)

**Date**: 2026-06-12
**Tester**: Product Owner / QA
**Environment**: Chrome 90+, Safari 16.4+, Firefox 90+
**Status**: ⏳ pending

## Preconditions

- ✅ Phase 18 complete (manifest.json, install button)
- ✅ Phase 19 complete (service worker, cache strategies, offline.html)
- ✅ Phase 20 code complete (6 von 6 plans)
- ✅ `npm run docs:build` + `postdocs:build` (manifest generation) erfolgreich

## Test Environment Setup

### Option A: Local Preview (HTTP localhost — PWA erlaubt)
```bash
npm run docs:preview
# Chrome → http://localhost:4173
```
→ Chrome akzeptiert `localhost` für SW auch ohne HTTPS.

### Option B: Deploy zu Staging (HTTPS erforderlich für echte Installation)
- Build: `npm run docs:build`
- Deploy via docker-compose zu payer-test.birchville.cc (o.ä.)
- HTTPS via Let's Encrypt / Caddy automatic HTTPS

### Chrome Flags für Dev (falls nötig)
- `chrome://flags` → "Insecure origins treated as secure" 
- Füge deine Test-URL hinzu (z.B. http://192.168.x.x:8080)

---

## Test Cases

### TC-1: Settings-Page Rendering (Plan 20-1)

**Setup**: Navigiere zu `/settings` (DE) oder `/en/settings` (EN)

| # | Action | Expected |
|---|---|---|
| 1.1 | Settings öffnen | Page rendert Checkboxen für alle 14 Sprachen |
| 1.2 | Checkboxen anklicken | Auswahl ändert sich visuell |
| 1.3 | Button "Speichern / Save" | Button ist disabled bis Änderung (dirty=true) |
| 1.4 | Änderung speichern | Progress message: "✓ Einstellungen gespeichert..." |
| 1.5 | Seite neu laden | Auswahl bleibt erhalten (localStorage) |
| 1.6 | Dark Mode toggle | Einstellungen sind lesbar in beiden Themes |
| 1.7 | DevTools → Application → Local Storage | `payer_active_locales` enthält JSON-Array |
| 1.8 | Versuche: alle Sprachen deaktivieren | Fehler: "Mindestens eine Sprache muss ausgewählt sein" |
| 1.9 | Cache-Größe-Anzeige | Zeigt ~23 MB pro aktiver Sprache |

**Pass-Kriterium**: 9/9 checks

### TC-2: Sidebar-Filter (Plan 20-2)

**Setup**: Default Settings = [de, en, it]

| # | Action | Expected |
|---|---|---|
| 2.1 | Sidebar öffnen (Desktop oder Mobile Hamburger) | DE, EN, IT Einträge sichtbar |
| 2.2 | Andere Sprachen (BG, RU, UK, HI, FR...) | Nicht sichtbar (display: none via .locale-hidden) |
| 2.3 | Language Switcher (top-nav, falls vorhanden) | Zeigt nur active locales |
| 2.4 | DevTools → Elements → `<a href="/ru/...">` | Element im DOM, aber hidden via CSS |
| 2.5 | Settings: aktiviere "Français" | Nach reload: Sidebar zeigt auch FR |
| 2.6 | Settings: deaktiviere "English" | Nach reload: EN Einträge verschwinden |
| 2.7 | Direkte URL navigation zu `/en/lektion/01/` nach EN-Deaktivierung | 1. Online: Seite lädt (URL ist erreichbar). 2. Offline: offline.html (wegen Cache-Eviction) |

**Pass-Kriterium**: 7/7 checks

### TC-3: Service Worker Caching (Plan 20-3)

**Setup**: DevTools → Application → Service Workers

| # | Action | Expected |
|---|---|---|
| 3.1 | Erstbesuch der Seite | SW wird registriert (Console: "[SW] Installed") |
| 3.2 | DevTools → Cache Storage → payer-cache-v20-r1 | Cache enthält /, offline.html, manifest.json |
| 3.3 | Navigiere zu `/lektion/01/` (DE) | Page wird im Cache gespeichert (NetworkFirst) |
| 3.4 | Navigiere zu `/en/lesson/01/` (EN, active) | Page wird im Cache gespeichert |
| 3.5 | Settings: deaktiviere "English" + save | Console: "[SW] Evicted N stale entries" |
| 3.6 | Cache-Check nach Deaktivierung | /en/... URLs sind aus Cache entfernt |
| 3.7 | Offline-Mode (DevTools → Network → Offline) | DE pages funktionieren (aus Cache) |
| 3.8 | Offline + deaktiviertes EN direkt aufrufen | offline.html erscheint |

**Pass-Kriterium**: 8/8 checks

### TC-4: Sprach-Nachladen (Plan 20-4)

**Setup**: Initial settings [de, en], dann "Français" hinzufügen

| # | Action | Expected |
|---|---|---|
| 4.1 | Settings: aktiviere "Français" → save | Progress: "⏳ Neue Sprachen werden heruntergeladen (0/1)..." |
| 4.2 | Per-Locale Indikator zeigt "⏳ Französisch" | Status: downloading (amber Farbe) |
| 4.3 | Warten bis Prefetch endet | Status: "✓ Französisch" (green) |
| 4.4 | Console: [SW] PREFETCH_LOCALE complete | ~143/145 URLs erfolgreich (oder ähnlich) |
| 4.5 | Cache-Check | /fr/ URLs sind jetzt im Cache |
| 4.6 | Offline + /fr/leçon/01/ | Seite lädt aus Cache |
| 4.7 | Während Prefetch: Settings wegklicken, zurückkommen | Status-Indikator ist noch da (reactive) |
| 4.8 | Mehrere Sprachen auf einmal hinzufügen (z.B. +FR, +RU, +BG) | Sequentieller Download: FR → RU → BG (nicht parallel) |

**Pass-Kriterium**: 7/8 checks (4.8 ist nice-to-have für Phase 21)

### TC-5: Install-Progress-Bar (Plan 20-5)

**Setup**: HTTPS-Deployment, erste Installation, active: [de, en, it]

| # | Action | Expected |
|---|---|---|
| 5.1 | Seite öffnen (HTTPS) | "App installieren"-Button erscheint |
| 5.2 | Button klicken | Overlay erscheint sofort mit Progress-Bar |
| 5.3 | Progress-Bar fillt sich | Smooth animation, 0% → ... → 100% |
| 5.4 | Text aktualisiert | "XX / YY Seiten" (tabular numeric) |
| 5.5 | Locale-Subtitle wechselt | "DE" → "EN" → "IT" (pro Locale) |
| 5.6 | Console: [SW] PREFETCH_BATCH events | Progress-Events fließen ~all 10 URLs |
| 5.7 | Browser zeigt nativen Install-Dialog | Nach Prefetch |
| 5.8 | Install bestätigen | Overlay wird nach 2.5s hidden |
| 5.9 | App öffnen (vom Icon) | Seiten funktionieren offline |
| 5.10 | Install canceln | Overlay wird nach 2.5s hidden, Button bleibt sichtbar |

**Pass-Kriterium**: 9/10 checks (5.9 optional, erfordert echte Installation)

### TC-6: README-Dokumentation (Plan 20-6)

**Setup**: README in Repo lesen

| # | Action | Expected |
|---|---|---|
| 6.1 | `## 📱 Progressive Web App (PWA)` Section | Existiert mit Install-Steps |
| 6.2 | Browser Compatibility Tabelle | Chrome/Safari/Firefox mit Versionen |
| 6.3 | Cache Management Section | Verweist auf Settings-Page |
| 6.4 | `## 🐳 Docker` Section | Existiert mit docker pull/run Befehlen |
| 6.5 | docker-compose.yml Beispiel | Gültig, kann kopiert werden |
| 6.6 | GHCR URL | ghcr.io/marcodem/sanskritkurs-payer |
| 6.7 | Local build Befehle | npm ci + docs:build + docker build |

**Pass-Kriterium**: 7/7 checks (keine Runtime-Verifikation nötig)

### TC-7: Multi-Language Settings-Page (Plan 20-1)

**Setup**: Einstellungen in jeder Sprache erreichbar

| # | Locale | URL | Titel |
|---|---|---|---|
| 7.1 | DE | `/settings` | "Einstellungen" |
| 7.2 | EN | `/en/settings` | "Settings" |
| 7.3 | IT | `/it/settings` | "Impostazioni" |
| 7.4 | BG | `/bg/settings` | "Настройки" |
| 7.5 | RU | `/ru/settings` | "Настройки" |
| 7.6 | UK | `/uk/settings` | "Налаштування" |
| 7.7 | HI | `/hi/settings` | "सेटिंग्स" |
| 7.8 | FR | `/fr/settings` | "Paramètres" |
| 7.9 | ES | `/es/settings` | "Configuración" |
| 7.10 | TA | `/ta/settings` | "அமைப்புகள்" |
| 7.11 | PA | `/pa/settings` | "ਸੈਟਿੰਗਾਂ" |
| 7.12 | LA | `/la/settings` | "Configurationes" |
| 7.13 | RM | `/rm/settings` | "Parameters" |
| 7.14 | RO | `/ro/settings` | "Setări" |

**Pass-Kriterium**: 14/14 Seiten laden (nur Rendering, keine Funktions-Tests)

---

## Integration Tests

### TC-I1: End-to-End Install-Flow

```
1. Neuer Browser, erster Besuch
2. "App installieren" Button klickt
3. Overlay mit Progress zeigt sich
4. Install im Dialog bestätigen
5. App-Icon auf Desktop
6. App öffnen (vom Icon)
7. DevTools → Network → Offline aktivieren
8. Navigation: / → /lektion/01/ → /en/lesson/01/
9. Alle Seiten funktionieren offline
10. DevTools → Application → Cache Storage: ~70 MB
```

### TC-I2: Migration von v1.3 (alte Cache-Keys)

```
1. User hat alte payer-cache-v19-r1 Cache (vor Upgrade)
2. Deploy mit v20-r1 SW
3. Beim nächsten Visit: SW upgrade → activate → alte Caches gelöscht
4. Neue Prefetch-Logik wird aktiv
```

### TC-I3: Settings-Änderung während Offline

```
1. Online: Settings öffnen, Einstellungen speichern
2. Offline schalten
3. Neue Sprache hinzufügen
4. Save klicken
5. Erwartet: "⚠ Download fehlgeschlagen" (kein Network)
6. Settings sind trotzdem gespeichert (localStorage)
7. Wieder online → Settings erneut öffnen
8. Sprache wird normal nachgeladen
```

---

## Regression Tests

### TC-R1: Keine Regression von Phase 15 (QA Viewer, Editor)
- QA Viewer (`/qa_viewer.html`) lädt noch
- Editor Tab rendert korrekt
- deleteme-box container funktioniert

### TC-R2: Keine Regression von Phase 16 (I18n)
- Alle 14 Locales funktionieren nach wie vor
- Language Switcher zeigt alle Sprachen wenn aktiv
- URL-Routing korrekt

### TC-R3: Keine Regression von Phase 17 (Scholarly Polish)
- Bildunterschriften korrekt
- licenses.md audit noch valide
- Comparison Mode (QA Viewer Split View) funktioniert

### TC-R4: Build-Output unverändert für User
- Lektionen rendern normal
- Sidebar Navigation funktioniert
- Search funktioniert (nur aktive Sprachen)

---

## Acceptance Criteria (overall)

- ✅ Settings-Page in allen 14 Sprachen verfügbar
- ✅ Sprachauswahl persisted in localStorage
- ✅ Sidebar filtert nicht-aktive Sprachen aus
- ✅ Service Worker cacht nur aktive Sprachen
- ✅ Neue Sprachen werden beim Aktivieren nachgeladen
- ✅ Install-Button mit Progress-Bar zeigt sich
- ✅ Progress-Bar visualisiert Batch-Prefetch
- ✅ README dokumentiert PWA- und Docker-Use Case
- ✅ Keine Regression von Phase 15-17
- ✅ npm run docs:build erfolgreich

**Minimum Pass**: 90% der Test Cases (ca. 45/50)
**Full Acceptance**: 100% der Critical Tests (TC-1 bis TC-5)

---

## Test Execution Notes

| # | TestCase | Result | Notes |
|---|---|---|---|
| 1 | TC-1 | ⏳ |  |
| 2 | TC-2 | ⏳ |  |
| 3 | TC-3 | ⏳ |  |
| 4 | TC-4 | ⏳ |  |
| 5 | TC-5 | ⏳ |  |
| 6 | TC-6 | ⏳ |  |
| 7 | TC-7 | ⏳ |  |
| I1 | TC-I1 | ⏳ |  |
| I2 | TC-I2 | ⏳ |  |
| I3 | TC-I3 | ⏳ |  |
| R1 | TC-R1 | ⏳ |  |
| R2 | TC-R2 | ⏳ |  |
| R3 | TC-R3 | ⏳ |  |
| R4 | TC-R4 | ⏳ |  |

**Executed at**: _pending_
**Tester**: _pending_
**Browser**: _pending_
**Result**: _pending_

---

## Issues Found

_List issues below during testing_

| Issue | Severity | TestCase | Reproduction |
|---|---|---|---|
| — | — | — | — |

# Project Context: v1.4 Offline-First PWA

## Vision

Eine Progressive Web App, die den gesamten Sanskritkurs offline verfügbar macht und nur ausgewählte Sprachen beinhaltet. Der User installiert die App einmal (via "Add to Home Screen" oder Browser-Install-Prompt) und kann danach ohne Internetverbindung auf alle Lektionen, Schriften und Übungen zugreifen.

## Zielgruppe

- **Desktop-User**: Studierende, die den Kurs auf dem Laptop als "App" installieren wollen
- **Mobile-User**: Lernen unterwegs (Zug, Flugzeug, ländliche Gebiete mit schlechter Konnektivität)
- **Selektive Nutzung**: User, die nur 2-3 Sprachen brauchen (z.B. DE + EN + IT), nicht alle 14

## Kernanforderungen

### 1. Vollständige Offline-Funktionalität
- Nach erstem Online-Besuch sind ALLE Inhalte offline verfügbar
- Navigation, Suche, Sidebar funktionieren ohne Netzwerk
- Keine teilweise offline / teilweise online Hybrid-Zustände

### 2. Selektive Sprachauswahl
- User wählt beim ersten Start aktive Sprachen aus
- Nur diese Sprachen werden in Sidebar, Navigation und Caches berücksichtigt
- Reduziert App-Größe von ~2GB (14 Sprachen) auf ~200MB (3 Sprachen)

### 3. Native App-Erfahrung
- "App installieren"-Button erscheint wenn PWA-Kriterien erfüllt
- Nach Installation: eigenes Fenster, kein Browser-UI
- Icon auf Home Screen / Desktop
- Splash Screen beim Start

### 4. Automatische Updates
- Bei neuem Deployment erkennt Service Worker die neue Version
- User wird informiert: "Update verfügbar"
- Ein Klick aktualisiert die App, alter Cache wird gelöscht

## Architektur-Entscheidungen

### ADR-1: Service Worker mit StaleWhileRevalidate

**Entscheidung**: Workbox-basierte Caching-Strategien
- HTML: NetworkFirst (immer frisch, Fallback auf Cache)
- CSS/JS/Fonts: CacheFirst (unveränderlich, schnell)
- Bilder: StaleWhileRevalidate (schnell + aktuell)

**Begründung**: 
- VitePress generiert statische HTML mit Content-Hashes in Dateinamen
- Bei neuen Builds ändert sich der Hash → neue Dateien, alte werden obsolete
- StaleWhileRevalidate zeigt sofort alte Version, aktualisiert im Hintergrund
- NetworkFirst für HTML stellt sicher, dass User immer neueste Lektionen sehen

**Alternativen**:
- CacheEverything: zu aggressiv, keine Updates mehr
- NetworkOnly: keine Offline-Funktionalität
- CacheOnly: keine Updates, manuelle Invalidation nötig

### ADR-2: Sprachauswahl via Build-Umgebungsvariable

**Entscheidung**: `LOCALES=de,en,it npm run docs:build`
- config.mjs liest `process.env.LOCALES`
- Nur konfigurierte Sprachen werden in `locales`-Objekt aufgenommen
- Sidebar-Generierung überspringt nicht-konfigurierte Sprachen

**Begründung**:
- VitePress compiliert alle konfigurierten Locales
- Kein Runtime-Filtering möglich (SSG generiert statische HTML)
- Build-time Selektion ist einzige Möglichkeit für reduzierte App-Größe

**Nachteil**: 
- Pro Sprach-Kombination ein separates Deployment nötig
- User kann nicht nachträglich Sprachen hinzufügen ohne Neuinstallation

**Alternative (verworfen)**:
- Runtime-Sprachauswahl mit localStorage: alle Sprachen werden gebaut, aber UI zeigt nur aktive
- Nachteil: App-Größe bleibt bei ~2GB, nur UI wird gefiltert

### ADR-3: Single Service Worker für alle Inhalte

**Entscheidung**: Ein sw.js cacht alles (HTML + Assets)

**Begründung**:
- VitePress generiert ~1500 HTML-Dateien (61 Lektionen × 14 Sprachen + Schriften + Übungen)
- Separate Service Worker pro Sprache wären zu komplex
- Cache-Storage API erlaubt keine granulare Selektion nach Sprache

**Kompromiss**: 
- Service Worker cacht ALLE Seiten (auch nicht ausgewählte Sprachen)
- Aber: Build erzeugt nur konfigurierte Sprachen → Cache bleibt klein

### ADR-4: Offline-Fallback Page

**Entscheidung**: `/offline.html` als Fallback für Netzwerk-Fehler

**Begründung**:
- User könnte versuchen, nicht-gecachte Seite zu öffnen (z.B. neue Lektion nach Update)
- Statt Browser-Fehler-Seite: freundliche App-eigene Offline-Page mit Erklärung

**Inhalt**:
- "Sie sind offline"
- "Diese Seite ist noch nicht verfügbar offline"
- "Bitte verbinden Sie sich mit dem Internet und laden Sie die Seite neu"
- Link zur Startseite (die immer gecacht ist)

## Offene Fragen

### Q1: Wie selektiv soll die Sprachauswahl sein?

**Entscheidung**: Option A (UI-gesteuert) + Option B als Fallback für fortgeschrittene User
- User wählt beim ersten Start via Settings-Page aus
- Fallback: `.env` Datei mit `LOCALES=de,en` für manuelle Konfiguration

### Q2: Wie groß darf die Offline-App sein?

**Berechnung**:
- 3 Sprachen × 61 Lektionen × ~50KB HTML = ~9MB
- 3 Sprachen × 61 Schriften × ~30KB HTML = ~5.5MB
- 3 Sprachen × 61 Übungen × ~20KB HTML = ~3.7MB
- CSS/JS/Fonts: ~2MB
- Bilder: ~50MB (komprimiert)
- **Gesamt: ~70MB**

**Akzeptabel für**:
- Desktop: ja (kein Problem)
- Mobile: ja (vergleichbar mit mittelgroßer App)
- Low-End Devices: grenzwertig (Cache-Storage Limit ~2GB auf iOS, ~10GB auf Android)

**Entscheidung**: 70MB ist akzeptabel. Keine weitere Kompression nötig.

### Q3: Update-Strategie bei neuen Lektionen

**Szenario**: Wir fügen Lektion 62 hinzu (derzeit 61)

**Aktuelle Architektur**:
- Service Worker erkennt neue HTML-Datei (nicht im Cache)
- NetworkFirst-Strategie lädt sie vom Server
- User sieht neue Lektion sofort

**Problem**: 
- User ist offline → Lektion 62 nicht verfügbar
- Keine automatische Benachrichtigung "Neue Inhalte verfügbar"

**Lösung**: 
- Service Worker vergleicht Manifest-Datei (list of all URLs)
- Bei Änderungen: "Neue Inhalte verfügbar" Notification
- User klickt → SW cacht neue Seiten im Hintergrund

**Implementierung**: Phase 21 (nicht in Phase 18-20)

## Technische Voraussetzungen

### VitePress-Kompatibilität
- Service Worker Integration via `public/sw.js`
- Manifest via `public/manifest.json`
- Meta-Tags via `head()` in config.mjs

### Browser-Support
- Chrome/Edge: volle Unterstützung
- Firefox: volle Unterstützung
- Safari: teilweise (iOS Safari hat Einschränkungen bei Service Worker Lifetime)
- **Minimum**: Chrome 80+, Firefox 75+, Safari 13+

### Hosting
- HTTPS erforderlich (Service Worker nur über HTTPS)
- Aktueller Hoster (Vercel/Netlify/GitHub Pages) unterstützt HTTPS automatisch

## Risiken und Mitigationen

### Risiko 1: Cache-Storage Quota
- **Problem**: Browser limitiert Cache-Storage (iOS: ~2GB, Android: ~10GB)
- **Mitigation**: 70MB App-Größe ist weit unter Limit
- **Monitoring**: `navigator.storage.estimate()` API zeigt genutztes Quota

### Risiko 2: Safari Service Worker Lifetime
- **Problem**: iOS Safari terminiert Service Worker nach 30 Minuten Inaktivität
- **Mitigation**: 
  - Alle wichtigen Assets werden beim ersten Besuch gecacht
  - Service Worker wird bei jeder Navigation reaktiviert
  - Offline-Funktionalität bleibt erhalten (Cache überlebt SW-Termination)

### Risiko 3: Inkonsistente Cache-Zustände
- **Problem**: User hat alte Version im Cache, neue Version auf Server
- **Mitigation**:
  - Cache-Versionierung (Cache-Name enthält Build-Revision)
  - Service Worker erkennt neue Version → "Update verfügbar"
  - User-gesteuertes Update (kein forced reload)

### Risiko 4: Selektiver Build vs. Full Deployment
- **Problem**: Production-Deployment hat alle 14 Sprachen, PWA nur 3
- **Mitigation**:
  - Zwei separate Deployments:
    - `payer.birchville.cc`: Full Build (Web-Version)
    - `pwa.payer.birchville.cc`: Selektiver Build (PWA-Version)
  - **Alternative**: Ein Deployment, PWA filtert zur Laufzeit (mehr Komplexität)
- **Entscheidung**: Zwei Deployments (einfacher, klar getrennt)

## Erfolgskriterien

1. **Offline-Test**: 
   - App wird einmal online geladen
   - Netzwerk wird deaktiviert
   - Alle 61 Lektionen + 11 Schriften + 61 Übungen sind weiterhin navigierbar
   - Suche funktioniert offline

2. **Install-Flow**:
   - Chrome zeigt "App installieren"-Button
   - Installation erfolgreich (Icon auf Desktop/Home Screen)
   - App startet im eigenen Fenster (kein Browser-UI)

3. **Performance**:
   - Lighthouse PWA Score ≥ 90
   - First Contentful Paint < 1.5s (online)
   - Time to Interactive < 3s (offline, aus Cache)

4. **Sprachauswahl**:
   - User wählt DE + EN + IT
   - Build-Output enthält nur diese 3 Sprachen (~70MB vs. ~2GB)
   - Sidebar zeigt nur DE + EN Navigation

5. **Update-Flow**:
   - Neuer Build deployed
   - Service Worker erkennt neue Version
   - User sieht "Update verfügbar" Notification
   - Nach Update: alle Inhalte aktualisiert

## Nächste Schritte

1. **Phase 18**: Web App Manifest + Service Worker Registrierung
2. **Phase 19**: Caching-Strategie + Offline-Fallback
3. **Phase 20**: Sprachauswahl-UI + selektiver Build
4. **Phase 21**: QA + Performance-Optimierung + Update-Notification

## Fragen zur Diskussion

> Alle Fragen geklärt — siehe **Entscheidungen** unten.

## Entscheidungen

### D1: Sprachauswahl-UI → Settings-Page
Eine dedizierte Settings-Page (statt Modal beim Erststart). User öffnet Settings, kreuzt aktive Sprachen an, Build-Trigger oder Runtime-Filter passt an.

### D2: Update-Notification → User-gesteuert
Kein automatischer Reload. Bei neuem build → Notification "Update verfügbar" mit Button "Jetzt aktualisieren". User entscheidet Zeitpunkt.

### D3: Deployment-Strategie → Eine Domain mit Service-Worker-Filter (REVISED)

Eine einzige Domain: `payer.birchville.cc`. Server hostet alle 14 Sprachen (~2GB).
Service Worker cacht beim Install **nur die vom User gewählten Sprachen** (~70MB).

**User-Flow:**
```
1. User öffnet payer.birchville.cc       (Web-Version, 14 Sprachen sichtbar)
2. Browser zeigt nativen Install-Prompt
3. Unsere Install-UI fängt ab: "Welche Sprachen benötigen Sie?"
4. Settings-Checkboxen: ☑ DE  ☑ EN  ☐ IT  ☐ FR ...
5. User wählt z.B. DE + EN + IT  →  Install klickt
6. SW lädt im Hintergrund ~70MB Cache-Paket
7. App-Icon auf Desktop/Home-Screen
8. Offline voll funktionsfähig. Sidebar zeigt NUR DE/EN/IT.
```

**Vorteile**:
- Ein Deployment, eine URL, stabile Bookmarks nach Installation
- Kein Subdomain-Wechsel, keine Verwirrung
- Server-Seite: ein einfacher statischer Hosting-Build
- SW-Filter macht App klein, nicht der Build

**Verworfen (altes D3)**: Zwei Subdomains (`pwa.payer.birchville.cc`).
Begründung Verwerfung: URL-Wechsel bei Installation, doppelte Wartung, Link-Sharing kaputt.

### D9: QA-Modus-Split → Zwei Builds, zwei Domains

**Entscheidung**: Build-time Trennung zwischen Public- und Authoring-Version.

```
Production Domain:      payer.birchville.cc
  └── npm run docs:build (config.mjs, ohne QA)
  └── 14 Sprachen, ~2GB
  └── PWA-Installation, Service Worker
  └── KEIN QA Viewer, Editor, deleteme-box

Authoring Domain:       author.payer.birchville.cc
  └── npm run docs:build:author (config.author.mjs, mit QA)
  └── Alle 14 Sprachen, ~2GB + QA-Tools
  └── Authelia Reverse Proxy (nur authentifizierte User)
  └── QA Viewer, Editor-Tab, deleteme-box Container
```

**Motivation**:
- QA-Code verschwindet aus Public-Bundle (Bundle-Size, Security)
- Authelia übernimmt Auth (keine App-seitige Auth-Logik)
- Saubere Trennung: Authoring vs. Konsum
- Kein Feature-Flag-Spaghetti im Client-Code

**Komponenten, die auf author.payer Domain wandern**:
1. QA Viewer (`docs/public/qa_viewer.html`)
2. Editor-Tab (Phase 15, Vue-Component `PayerEditorTab.vue`)
3. deleteme-box Container (Markdown-Container für Lizenzen/TODOs)
4. `docs/public/qa/` Verzeichnis (Legacy HTML für Vergleich)
5. `markdown.lineNumbers: true` in config.author.mjs
6. Ggf. weitere interne Tools (Debug-UI, Migration-Skripte)

**Status**: Geplant als **Phase 22** (Backlog, nach v1.4).

### D4: Safari-Compatibility → Graceful Degradation
- Pre-cache alles beim Erstbesuch
- Re-Registration bei jedem Page-Load (idempotent)
- Offline-Fallback zeigt klare Meldung wenn Cache purged wurde
- Keine speziellen iOS-Workarounds — Standard-Service-Worker-Verhalten akzeptiert
- 70MB ist weit unter iOS 1GB Cache-Limit

### D5: Cache-Size-Monitoring → OK (implementieren)
Settings-Page zeigt:
- Belegter Cache-Speicher (`navigator.storage.estimate()`)
- Anzahl gecachter Sprachen / Seiten
- Button "Cache leeren" für Troubleshooting

### D6: Navigation in installierter App → Nur gewählte Sprachen
- Installierte App zeigt in Sidebar **nur** gewählte Sprachen
- Was ich sehe = was offline funktioniert. Keine gemischten Zustände.
- Web-Version (vor Installation) zeigt weiterhin alle 14 Sprachen

### D7: Nachträglich Sprachen hinzufügen → In-App Settings + Online-Nachladen
- Settings-Page in installierter App
- User kreuzt zusätzliche Sprache an → SW lädt online nach, speichert in Cache
- Kein Reinstall nötig (außer bei korruptem Cache → "Cache leeren"-Button)

### D8: Erste Offline-Erfahrung → Aggressive Pre-Cache
- Beim Klick auf "Installieren" im Install-Dialog:
  - SW beginnt sofort im Hintergrund alle gewählten Sprachen zu cachen
  - ~70MB Download, ~30-60 Sekunden
  - User sieht Fortschrittsanzeige (progress bar unten rechts)
- Wenn User App sofort nach Installation offline öffnet: **alles da**
- Lazy-Loading verworfen (würde User expectation verletzen — "App installiert, aber offline fehlen Lektionen")

### D10: Sprachauswahl-Modell → B (Runtime-Filter, nicht Build)

**Zwei Modelle wurden evaluiert:**

**Modell A (Build-time):**
```
git push → CI mit LOCALES=de,en,it → VitePress baut nur 3 Sprachen → Docker-Image
```
- Sprachauswahl zum Deploy-Zeitpunkt (vom Entwickler)
- User kann keine anderen Sprachen öffnen
- Pro Sprach-Kombi ein separates Docker-Image

**Modell B (Runtime) — gewählt:**
```
git push → CI baut volle 14 Sprachen → Docker-Image (ein einziges)
         ↓
Server hostet alle 14 (~2GB)
         ↓
User wählt in Settings: de/en/it
         ↓
Service Worker cacht nur gewählte URLs (~70MB lokal)
         ↓
Sidebar zeigt nur gewählte (via Link-Hiding)
```
- Sprachauswahl zur Laufzeit (vom User)
- User kann Sprachen nachträglich hinzufügen/entfernen
- Ein einziges Docker-Image für alle User

**Warum Modell B gewinnt**:
- D3 (rev), D6, D7 setzen alle ein Runtime-Modell voraus
- Docker-Image ist Deployment-Artefakt (einmal pro Git-Push), nicht User-Artefakt
- Git-Push kann nicht wissen welche Sprachen ein spezifischer User später will
- Flexibilität für User (Sprachnachladen ohne Reinstall)
- Einfachere CI/CD (ein Workflow, ein Image)

**Build/Docker bleiben unverändert:**
- `npm run docs:build` → Full Build, 14 Sprachen
- `Dockerfile` → nginx:alpine mit dist/
- `deploy.yml` → ein Image, ein Push
- Nur der **Client** filtert zur Laufzeit

**Modell A (Build-time) bleibt als Future Option:**
- Für dedizierte PWA-Apps im Store (z.B. "Payer Sanskrit DE" auf Android)
- Für E-Book/PDF-Generierung
- Für sprach-spezifische Marketing-Landingpages

## Nächste Schritte

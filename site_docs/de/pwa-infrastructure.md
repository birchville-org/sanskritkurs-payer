# 📱 PWA & Infrastruktur

## 1. Progressive Web App (PWA) Architektur

Der Sanskritkurs ist als voll funktionsfähige Progressive Web App konzipiert. Nutzer können das gesamte Lehrwerk auf Desktop- und Mobilgeräten (iOS/Android/Windows/macOS/Linux) installieren und ohne aktive Internetverbindung lernen.

### 1.1. Caching-Strategie & Speicherverwaltung
- **Sprachspezifische Partitionierung:** Der Service Worker lädt und cacht Inhalte gezielt nach ausgewählten Sprachen. Jedes Sprachpaket umfasst ca. 23 MB an vorgerendertem HTML, CSS, JavaScript und Vektor-Grafiken.
- **Cache-Inspektion:** Über die Einstellungsseite (`settings.md`) kann der aktuelle Speicherverbrauch via `navigator.storage.estimate()` eingesehen und der Cache bei Bedarf bereinigt werden.
- **Offline-Fallback:** Nicht im Cache vorhandene Seiten zeigen eine responsive zweisprachige Offline-Hinweisseite an und laden automatisch neu, sobald eine Netzwerkverbindung erkannt wird.

---

## 2. VitePress SSG-Konfiguration

Das Projekt nutzt **VitePress 1.6** als Static Site Generator.

### 2.1. Dynamische Sidebar-Generierung
Für jede Sprache wird die Seitenleiste algorithmisch über `populateSidebar()` (`docs/.vitepress/utils.mjs`) aufgebaut:
- Automatische Gliederung in 10er-Blöcke (z.B. *Lektion 01–10*, *11–20* bis *51–61*).
- Lokalisierte Beschriftungen für *Lektion*, *Schrift* und *Übung*.

### 2.2. Lokale Volltextsuche & Sanskrit-Normalisierung
Integrierte MiniSearch-Engine mit IAST-Diakritika-Normalisierung (`docs/.vitepress/config.mjs`):
- Suchanfragen mit oder ohne Längenzeichen (`ā` vs. `a`, `ś` vs. `s`, `ṛ` vs. `r`) liefern identische Treffer.
- Automatische Sprachfilterung basierend auf dem URL-Präfix verhindert Sprachmischungen in den Suchresultaten.

---

## 3. Docker-Container & GHCR-Verteilung

Für den produktiven Einsatz im Webserver-Umfeld wird ein hochoptimiertes Docker-Image bereitgestellt:

- **Basis-Image:** `nginx:alpine` (Image-Größe: ~50 MB).
- **Multi-Architektur-Build:** Nativer Build für `linux/amd64` und `linux/arm64` via GitHub Actions (`.github/workflows/deploy.yml`).
- **Clean URLs:** Vorkonfigurierte `nginx.conf` für suchmaschinenfreundliches Routing ohne `.html`-Dateiendungen.

```bash
# Docker Image beziehen
docker pull ghcr.io/birchville-org/sanskritkurs-payer:latest

# Lokal starten
docker run -d -p 8080:80 ghcr.io/birchville-org/sanskritkurs-payer:latest
```

---

## 4. Desktop-Applikation (Tauri)

Über [Tauri](https://tauri.app/) steht der Kurs als native Desktop-App für macOS zur Verfügung:
- **Vorbereitung:** `python3 scripts/prepare_desktop_dist.py` (filtert Kernsprachen für minimale App-Größe).
- **Build:** `npx tauri build --bundles dmg`.

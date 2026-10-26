# Architekturplan: Vollständiges Hosting auf GitHub Pages (github.io)

> **Status:** Konzept / Machbarkeitsplan  
> **Projekt:** Sanskritkurs Payer (VitePress Multi-Language SSG)  
> **Datum:** Oktober 2026  
> **Ziel:** Vollständiger Betrieb des Kurses auf `github.io` ohne dedizierte Server-Infrastruktur

---

## 1. Ausgangslage & Zielsetzung

Der Sanskritkurs Payer basiert auf einem statischen VitePress-Setup (`docs/`) mit 47 Lokalisierungen und über 6.300 generierten HTML-Seiten. Zurzeit wird der Kurs primär als Multi-Arch Docker-Container (`ghcr.io/birchville-org/sanskritkurs-payer`) gebaut und auf lokaler Infrastruktur/Homelab betrieben, während auf GitHub Pages ([`birchville-org.github.io/sanskritkurs-payer`](https://birchville-org.github.io/sanskritkurs-payer/)) lediglich das MkDocs-Dokumentationsportal (`site_docs/`) ausgeliefert wird.

**Ziel:** Prüfung und Vorbereitung einer vollständigen Bereitstellung des eigentlichen Kurses via GitHub Pages, sodass keine externen Server für das Web-Frontend benötigt werden.

---

## 2. Technische Machbarkeit

### 2.1. Client-Side Autonomie
- **Reine SSG-Architektur:** VitePress generiert 100 % statisches HTML, CSS und JavaScript. Zur Laufzeit ist kein Applikations- oder Datenbankserver erforderlich.
- **QA-Viewer & Editor (`qa_viewer.html`):** Vollständig clientseitig lauffähig. Lokales Speichern erfolgt über die Browser File System Access API; Cloud-Saves/PRs nutzen die GitHub REST API mit Personal Access Token (PAT).
- **Semantische Suche (Vektor-RAG):** Die Indizes (`vector_index_<lang>.json`) werden statisch ausgeliefert und clientseitig im Web Worker verarbeitet.

### 2.2. Offline-/Homelab-Abgrenzung
Folgende Komponenten bleiben zwingend lokal und sind **nicht** Bestandteil des Web-Hostings:
- **KI-Übersetzungs-Pipeline (`scripts/lan_translate.py`):** Benötigt lokale LLM-Inferenz (`nyx.local:8000`) und bleibt ein reiner Entwicklungsprozess.
- **Tauri Desktop-App:** Wird lokal oder via CI als Binär-Asset (`.dmg`) gebaut.

---

## 3. Restriktionen & Rahmenbedingungen (GitHub Pages)

| Kriterium | GitHub Pages Limit | Aktueller Kursstand | Bewertung |
| :--- | :--- | :--- | :--- |
| **Site-Größe** | 1 GB (Soft/Hard Limit) | ~709 MB (`dist`) | **Kritisch nah** (Puffer ~290 MB) |
| **Downloads-Anteil** | — | 248 MB (`docs/public/downloads`) | Muss ausgelagert werden |
| **Bandbreite** | 100 GB / Monat | Vektor-Indizes: ~10 MB/Sprache | Bei hoher Nutzung zu überwachen |
| **Build-Dauer** | Max. 360 Min. pro Job | ~81 Min. (Runner `ubuntu-latest`) | Nur ereignisbasiert tragbar |
| **RAM (Runner)** | 7 GB physikalisch | OOM ohne 32 GB Swap | 32 GB Swap zwingend |
| **CI-Minuten** | 2.000 Min./Monat (Free) | ~85 Min. pro Build | Max. 23 Builds/Monat möglich |

---

## 4. 4-Phasen-Implementierungsplan

```
┌─────────────────────────────────┐
│ Phase 1: Asset-Entschlackung    │ -> Downloads auslagern, dist von 710 MB auf ~460 MB senken
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│ Phase 2: URL- & Domain-Strategie│ -> Routing klären (Custom Domain vs. Subpath /course/)
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│ Phase 3: CI/CD Pipeline Setup   │ -> Release-basierter GitHub Pages Workflow mit 32 GB Swap
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│ Phase 4: Validierung & QA Gate  │ -> 47 Sprachen, QA-Viewer, Vektorindizes und Links verifizieren
└─────────────────────────────────┘
```

### Phase 1: Asset-Entschlackung (1-GB-Garantie)
1. **Downloads aus dem Web-Tree entfernen:**
   - Große PDF- und EPUB-Pakete in `docs/public/downloads/` (derzeit 248 MB) aus Git und dem Build-Tree entfernen.
   - Download-Buttons im Frontend auf die offiziellen GitHub Release Assets (`https://github.com/birchville-org/sanskritkurs-payer/releases/latest/download/...`) umleiten.
   - **Ergebnis:** Reduziert die `dist`-Größe von ~709 MB auf ca. **460 MB** und schafft über **540 MB Puffer** bis zum 1-GB-Limit.

### Phase 2: URL-Routing & Domain-Strategie
Drei Umsetzungsoptionen:
- **Option A (Empfohlen): Custom Subdomain (`sanskrit.birchville.org`)**
  - CNAME-Record auf `birchville-org.github.io`.
  - Keine Pfad-Präfix-Probleme; `base: '/'` kann verwendet werden.
  - Das MkDocs-Portal verbleibt ungestört auf `birchville-org.github.io/sanskritkurs-payer/`.
- **Option B: Subpath-Betrieb (`/sanskritkurs-payer/course/`)**
  - VitePress `base: '/sanskritkurs-payer/course/'`.
  - Erfordert Anpassung aller relativen Pfade und des QA-Viewers.
- **Option C: Vollständige Übernahme des Root-Pfads**
  - VitePress löst MkDocs auf `birchville-org.github.io/sanskritkurs-payer/` ab.
  - Das Dokumentationsportal (`site_docs/`) wird als eigenes Kapitel in VitePress integriert.

### Phase 3: Release-basierte GitHub Actions Pipeline (`.github/workflows/deploy-pages.yml`)
Um das CI-Minuten-Kontingent nicht zu belasten, darf der Build **nicht** bei jedem Push auf `main` laufen.

**Pipeline-Spezifikation:**
```yaml
name: Deploy Sanskritkurs to GitHub Pages

on:
  release:
    types: [published]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages-deploy
  cancel-in-progress: false

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Swap Space (32 GB)
        uses: pierotofy/set-swap-space@master
        with:
          swap-size-gb: 32

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: 'npm'

      - name: Install dependencies
        run: npm ci

      - name: Build VitePress
        run: npm run docs:build
        env:
          NODE_OPTIONS: "--max-old-space-size=32768"

      - name: Setup Pages
        uses: actions/configure-pages@v5

      - name: Upload Pages Artifact
        uses: actions/upload-pages-artifact@v3
        with:
          path: docs/.vitepress/dist

      - name: Deploy to GitHub Pages
        id: deployment
        uses: actions/deploy-pages@v4
```

### Phase 4: Validierung & QA Gate
1. **Smoke-Test aller 47 Locales:** Sicherstellen, dass Deep-Links (`/<lang>/lektionen/lektionXX`) und Devanāgarī-Schriften sauber geladen werden.
2. **QA-Viewer Test:** Überprüfen, ob `qa_viewer.html` Lektionen remote via `fetch()` laden und bearbeiten kann.
3. **Bandbreiten-Monitoring:** Kontrolle des Verbrauchs der Vektordateien in den GitHub Pages Settings.

---

## 5. Risiken & Mitigation

| Risiko | Eintritts-Wahrscheinlichkeit | Auswirkung | Gegenmaßnahme |
| :--- | :--- | :--- | :--- |
| **Runner OOM Crash** | Hoch (ohne Swap) | Fatal (Build bricht ab) | 32 GB Swap via `pierotofy/set-swap-space` zwingend vorschreiben |
| **CI-Minuten-Erschöpfung** | Mittel | Hoch | Build ausschließlich bei Releases oder manueller Triggerung (`workflow_dispatch`) |
| **Seitenlimit > 1 GB** | Mittel | Fatal | Downloads (PDFs/EPUBs) auf GitHub Releases auslagern (Phase 1) |
| **Monatliches Bandbreitenlimit (100 GB)** | Niedrig | Mittel | Vektorindizes komprimiert ausliefern oder bei Bedarf On-Demand nachladen |

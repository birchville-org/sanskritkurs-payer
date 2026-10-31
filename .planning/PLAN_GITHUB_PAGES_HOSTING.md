# Architekturplan: Dual-Target Hosting (github.io + Docker/GHCR) & Authelia Zero-PAT Autoren-Pipeline

> **Status:** Phase 1 abgeschlossen (`v1.9.1` / `v1.10.1`); Dual-Target-Architektur (`github.io` + `ghcr.io`) & Architektur C (Authelia Zero-PAT Broker) spezifiziert  
> **Projekt:** Sanskritkurs Payer (VitePress Multi-Language SSG)  
> **Datum:** 31. Oktober 2026  
> **Ziel:** Serverloser Primärbetrieb auf `github.io`, vollwertiger Erhalt des Multi-Arch Docker-Images (`ghcr.io`) als „All-in-One"-Alternative/Failover und Authelia-geschützte Zero-PAT Autoren-Pipeline

---

## 1. Kernprinzip: „Build Once, Publish Everywhere" (Dual-Target)

Da das [Dockerfile](file:///Volumes/SanDisk1TB/proj/Payer/Dockerfile) selbst keinen Node.js-Build ausführt, sondern lediglich das fertig gebaute `docs/.vitepress/dist-public`-Verzeichnis in ein `nginx:alpine`-Image kopiert (~20 Sekunden Laufzeit), lassen sich **GitHub Pages (`github.io`)** und das **Docker-Image (`ghcr.io`)** aus **einem einzigen VitePress-Build-Lauf** in [.github/workflows/deploy.yml](file:///Volumes/SanDisk1TB/proj/Payer/.github/workflows/deploy.yml) speisen:

```
                   ┌──────────────────────────────────────────────┐
                   │ 1x VitePress Build (47 Sprachen, 32 GB Swap) │
                   │    Ergebnis: docs/.vitepress/dist-public     │
                   └──────────────────────┬───────────────────────┘
                                          │
                  ┌───────────────────────┴───────────────────────┐
                  ▼                                               ▼
┌───────────────────────────────────────┐       ┌───────────────────────────────────────┐
│ Ziel A: GitHub Pages (github.io)      │       │ Ziel B: Multi-Arch Docker (ghcr.io)   │
│ • actions/upload-pages-artifact@v3    │       │ • linux/amd64 + linux/arm64           │
│ • actions/deploy-pages@v4             │       │ • nginx:alpine + qa_auth_broker.py    │
│ • Primäres, serverloses CDN           │       │ • Gleichzeitig Autoren-Portal,        │
│   für öffentliche Leser               │       │   Homelab-Mirror & Instant-Failover   │
└───────────────────────────────────────┘       └───────────────────────────────────────┘
```

### Warum die Docker-Variante damit dauerhaft ohne Mehraufwand am Leben bleibt:
1. **0 zusätzliche Build-Zeit:** Der teure 47-Sprachen-VitePress-Build läuft pro Release nur **einmal**. Das anschließende Bauen und Pushen des Docker-Images dauert nur ~20–30 Sekunden.
2. **Bit-identischer Stand:** `github.io` und `ghcr.io/birchville-org/sanskritkurs-payer:latest` enthalten bei jedem Release exakt denselben HTML/JS/CSS-Stand.
3. **Einziger Container für Autoren-Broker UND Voll-Failover:**
   Indem das kleine Broker-Skript (`scripts/qa_auth_broker.py`) direkt in das Docker-Image integriert wird (gesteuert über die optionale Umgebungsvariable `GITHUB_TOKEN`), erfüllt **derselbe Docker-Container** drei Zwecke:
   - **Ohne `GITHUB_TOKEN`:** Klassischer Stand-Alone-Container (`docker run -p 8080:80 ...`) für Offline-/Eigenbetrieb oder als sofortiger DNS-Failover, falls GitHub Pages ausfällt.
   - **Mit `GITHUB_TOKEN` hinter Traefik + Authelia:** Dient als geschütztes Autoren-Portal (Architektur C) inklusive `/api/qa/*`-Broker – es muss **kein separater zweiter Container** für den Broker gebaut oder gewartet werden.
   - **Auf `nataraja.local:8080`:** Läuft weiterhin über [.github/workflows/ci.yml](file:///Volumes/SanDisk1TB/proj/Payer/.github/workflows/ci.yml) als lokales Live-Staging bei jedem Push auf `main`.

---

## 2. Detail-Spezifikation: Architektur C im „All-in-One" Docker-Container

### 2.1. Container-Aufbau (`Dockerfile` + `nginx.conf` + `docker-entrypoint.sh`)
- **Basis-Image:** `nginx:alpine` erweitert um `python3` (nur Standardbibliothek, ~12 MB zusätzlich, keine `pip`-Abhängigkeiten nötig).
- **Entrypoint-Logik (`docker-entrypoint.sh`):**
  - Ist `GITHUB_TOKEN` gesetzt, startet im Hintergrund `python3 /usr/local/bin/qa_auth_broker.py` auf `127.0.0.1:8081`.
  - Ist `GITHUB_TOKEN` **nicht** gesetzt, startet nur `nginx` (100 % abwärtskompatibel zu allen bisherigen Deployments).
- **Nginx-Routing ([nginx.conf](file:///Volumes/SanDisk1TB/proj/Payer/nginx.conf)):**
  ```nginx
  location /api/qa/ {
      proxy_pass http://127.0.0.1:8081/api/qa/;
      proxy_set_header Remote-User   $http_remote_user;
      proxy_set_header Remote-Name   $http_remote_name;
      proxy_set_header Remote-Email  $http_remote_email;
      proxy_set_header Remote-Groups $http_remote_groups;
  }
  ```

### 2.2. Authentifizierungs- & Header-Kontrakt (Traefik -> Authelia -> Container)
Traefik sichert den Autoren-Zugang mit der bestehenden Middleware `authelia@docker` ab. Authelia injiziert nach erfolgreichem Login:
- `Remote-User`: Benutzername (z. B. `m.muster`)
- `Remote-Name`: Anzeigename für den Git-Commit (z. B. `Maria Muster`)
- `Remote-Email`: E-Mail-Adresse für den Git-Commit (z. B. `maria@birchville.org`)
- `Remote-Groups`: Gruppenmitgliedschaften (z. B. `authors,lector-fr`)

### 2.3. REST-Endpunkte des Brokers (`scripts/qa_auth_broker.py`)

| Methode & Pfad | Funktion | Verhalten |
| :--- | :--- | :--- |
| `GET /api/qa/me` | Session-Info | Liefert `{ "user": Remote-User, "name": Remote-Name, "email": Remote-Email, "groups": [...] }`. Zeigt im Header des QA-Viewers den eingeloggten Autor an. |
| `GET /api/qa/file?path=docs/...` | Cloud-Load | Prüft Pfad-Whitelist, lädt die `.md`-Datei via GitHub API zuerst vom Branch `author-drafts` (Fallback: `main`) und gibt `{ "content": "...", "branch": "...", "sha": "..." }` zurück. |
| `PUT /api/qa/file` | Cloud-Save & PR | Nimmt `{ "path": "docs/<lang>/lektionen/lektionXX.md", "content": "..." }` entgegen, prüft Schreibrechte, committet in `author-drafts` (mit `author: { name: Remote-Name, email: Remote-Email }`) und öffnet/aktualisiert automatisch den Pull Request gegen `main`. |

### 2.4. Serverseitige Schutzregeln (TOTALBREMSE & Path-Guard)
1. **Pfad-Regex-Guard:** Erlaubt sind ausschließlich `^docs/([a-z]{2,3}(-[A-Z]{2})?/)?lektionen/(lektion|schrift|uebung|glossar|index)[a-z0-9_-]*\.md$`.
2. **TOTALBREMSE-Schutz:** Schreibzugriffe auf den deutschen Master (`docs/lektionen/*.md`) sind gesperrt, sofern der Benutzer nicht in `Remote-Groups: admins` ist.
3. **Optionale Sprach-Zuweisung:** Hat ein Lektor Gruppen wie `lector-fr`, erlaubt der Broker Schreibzugriffe nur unter `docs/fr/lektionen/*.md`.

---

## 3. Drei Betriebsmodi zur Auswahl (jederzeit per Traefik/DNS umschaltbar)

Weil sowohl `github.io` als auch der `ghcr.io`-Docker-Container bei jedem Release synchron aktualisiert werden, kannst du jederzeit ohne Codeänderung zwischen drei Betriebsmodi wechseln:

| Betriebsmodus | Öffentlicher Kurs (Leser) | Autoren-Pipeline (`/qa_viewer.html` & `/api/qa/*`) | Wann sinnvoll? |
| :--- | :--- | :--- | :--- |
| **Modus 1: Hybrid Subdomain** *(Empfohlen)* | `payer.birchville.org` -> direkt per CNAME auf `github.io` (0 % Serverlast) | `qa.payer.birchville.org` -> Traefik + Authelia -> lokaler Docker-Container | Maximaler Entlastungsgrad; öffentlicher Kurs läuft auch bei Wartung des eigenen Servers weiter. |
| **Modus 2: Hybrid Single-Domain** | `payer.birchville.org/*` -> Traefik routet Lese-Traffic als Reverse-Proxy auf `github.io` | `payer.birchville.org/qa_viewer.html` & `/api/qa/*` -> Traefik + Authelia -> lokaler Docker-Container | Alles unter einer einzigen URL (`payer.birchville.org`), statische Assets kommen von `github.io`. |
| **Modus 3: 100 % Docker Self-Hosted** *(wie heute + Zero-PAT)* | `payer.birchville.org/*` -> Traefik -> lokaler Docker-Container | `payer.birchville.org/qa_viewer.html` & `/api/qa/*` -> Traefik + Authelia -> **derselbe** lokale Docker-Container | Sofortiges Failover oder kompletter Eigenbetrieb, während `github.io` als öffentlicher Mirror mitläuft. |

---

## 4. 5-Phasen-Umsetzungsplan

### Phase 1: Asset-Entschlackung (1-GB-Garantie) — [ERLEDIGT]
- [x] PDFs und EPUBs via `srcExclude: ['**/*.pdf', '**/*.epub']` in [config.mjs](file:///Volumes/SanDisk1TB/proj/Payer/docs/.vitepress/config.mjs#L140) ausgeschlossen (`v1.10.1`), `dist`-Footprint auf ~450 MB reduziert.

### Phase 2: All-in-One Docker-Erweiterung & Authelia-Broker (Architektur C) — [OFFEN]
- [ ] **Schritt 2.1 (`scripts/qa_auth_broker.py`):** Implementierung des HTTP-Brokers (`/api/qa/me`, `GET/PUT /api/qa/file`) mit Pfad-Whitelist, TOTALBREMSE-Check und Git-Author-Mapping (`Remote-Name` / `Remote-Email`).
- [ ] **Schritt 2.2 ([Dockerfile](file:///Volumes/SanDisk1TB/proj/Payer/Dockerfile), [nginx.conf](file:///Volumes/SanDisk1TB/proj/Payer/nginx.conf), `scripts/docker-entrypoint.sh`):**
  - Einbettung von `python3` und `qa_auth_broker.py` in das bestehende Docker-Image.
  - Automatischer Start des Brokers auf `127.0.0.1:8081`, sobald `GITHUB_TOKEN` beim Container-Start übergeben wird.
  - Nginx-Location `/api/qa/` mit Weiterleitung der `Remote-*`-Header von Authelia.
- [ ] **Schritt 2.3 ([docs/public/qa_viewer.html](file:///Volumes/SanDisk1TB/proj/Payer/docs/public/qa_viewer.html)):**
  - Automatische Erkennung von `/api/qa/me` beim Start (Anzeige des eingeloggten Authelia-Nutzers im Header).
  - Nutzung von `/api/qa/file` in [`openCloudFile()`](file:///Volumes/SanDisk1TB/proj/Payer/docs/public/qa_viewer.html#L1873-L1921) und [`saveCloudFile()`](file:///Volumes/SanDisk1TB/proj/Payer/docs/public/qa_viewer.html#L1970-L2077) ohne PAT-Prompt.
  - Korrektur des Repository-Owners von `marcodem` auf `birchville-org` im lokalen Fallback.

### Phase 3: Vereinheitlichter Dual-Target CI/CD Workflow (`.github/workflows/deploy.yml`) — [OFFEN]
- [ ] Erweiterung von [.github/workflows/deploy.yml](file:///Volumes/SanDisk1TB/proj/Payer/.github/workflows/deploy.yml), sodass nach dem einmaligen `Build VitePress (Public)`-Schritt:
  1. das Multi-Arch Docker-Image (`linux/amd64`, `linux/arm64`) wie bisher auf `ghcr.io/birchville-org/sanskritkurs-payer` gepusht wird **und**
  2. parallel oder direkt im Anschluss `docs/.vitepress/dist-public` via `actions/upload-pages-artifact@v3` und `actions/deploy-pages@v4` auf GitHub Pages veröffentlicht wird.

### Phase 4: Traefik- & Authelia-Konfiguration — [OFFEN]
- [ ] Hinterlegen von `GITHUB_TOKEN` in der Docker-Compose-Konfiguration des Payer-Containers.
- [ ] Aktivieren der `authelia@docker`-Middleware in Traefik für `/qa_viewer.html` und `/api/qa/`.

### Phase 5: End-to-End Validierung — [OFFEN]
- [ ] Verifikation, dass ein Release-Run sowohl `ghcr.io/...:latest` als auch `github.io` synchron aktualisiert.
- [ ] End-to-End-Test: Authelia-Login -> Lektion im QA-Viewer laden -> Editieren -> Speichern -> Prüfung des Commits (mit Authelia-Namen) und PRs auf GitHub.

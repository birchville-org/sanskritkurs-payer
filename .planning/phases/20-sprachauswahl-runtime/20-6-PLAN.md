# Plan 20-6: README mit PWA & Docker Abschnitten

**Phase**: 20 Sprachauswahl (Runtime-Filter)  
**Status**: ✅ Complete  
**Completed**: 2026-06-12  
**Dependencies**: 20-1 bis 20-5 (konzeptionell — README dokumentiert bereits)

## Ziel

README.md in der Repo-Root um zwei neue Hauptabschnitte erweitern:
1. **📱 Progressive Web App (PWA)** — Installation, Offline-Nutzung, Browser-Support, Cache-Management
2. **🐳 Docker** — Image-Pull, lokale Ausführung, Reverse-Proxy-Deployment, Build

## Motivation

Die PWA-Funktionalität wird erst mit v1.4 ausgeliefert und braucht Dokumentation für End-User. Docker-Deployment ist seit v1.3 möglich, aber nicht in README dokumentiert. Das sind die zwei wichtigsten User-Einstiegspunkte:

- **User** → will wissen wie die App zu installieren ist
- **Admin/Ops** → will wissen wie das Image zu deployen ist

Beide brauchen klare, knappe Dokumentation im README, nicht in tief verschachtelten Docs.

## Deliverables

**Modifikation**: `README.md` (Repo-Root)

### Neue Abschnittsstruktur

```
# Sanskritkurs Payer (VitePress Migration)
## 🚀 Setup & Development          ← bestehend
## 📦 Deployment                   ← bestehend (Hosting on Web Server)
## 📱 Progressive Web App (PWA)    ← NEU
## 🐳 Docker                       ← NEU
```

## Implementation

### PWA-Abschnitt

Enthält:
- **Installation** — 4-Schritte-Guide (Browser öffnen, Button klicken, Sprachen wählen, Confirm)
- **Offline Usage** — Cache-Verhalten, Fallback-Page, Nachladen neuer Sprachen
- **Browser Compatibility** — Tabelle mit Chrome/Safari/Firefox Minimum-Versionen
- **Cache Management** — Settings-Page Features (Cache-Size, Clear, Add/Remove)

### Docker-Abschnitt

Enthält:
- **Pull the Image** — `docker pull` mit GHCR-URL
- **Available Tags** — `latest`, `v*.*.*` (SemVer), `sha-<commit>` (pin)
- **Run Locally** — einfacher `docker run` mit Port-Mapping
- **Deploy Behind a Reverse Proxy** — `docker-compose.yml` Beispiel
- **Image Internals** — nginx:alpine, Build in GH Actions, nur dist/ im Image
- **Build Locally (Optional)** — für User die kein GHCR wollen

## Sprachwahl

**Englisch** — konsistent mit der bestehenden README (die schon "Setup & Development", "Deployment" nutzt). Payer-Projekt-Docs dürfen Deutsch sein (Kurs), aber README als Dev-Facing-Dokument ist Englisch.

## Verification

```bash
# README Render-Check (Markdown-Syntax)
cat README.md | grep -E "^## " 
# Erwartet: Setup, Deployment, PWA, Docker

# Interne Links prüfen (alle lokal)
grep -oE "ghcr\.io/[a-z0-9/_-]+" README.md | sort -u
# Erwartet: ghcr.io/marcodem/sanskritkurs-payer

# Code-Blöcke Syntax
grep -c '```' README.md
# Erwartet: gerade Zahl (8 Blöcke = 16 Backticks, 7 Blöcke = 14)
```

## Success Criteria

- ✅ README hat 4 klar getrennte Hauptabschnitte
- ✅ PWA-Sektion nennt Install-Steps + Browser-Compatibility-Tabelle
- ✅ Docker-Sektion nennt GHCR-URL + Tags + Run-Command + compose-Beispiel
- ✅ Konsistenter englischer Ton über alle Abschnitte
- ✅ Keine gebrochenen Markdown-Elemente (Code-Blöcke, Tabellen, Links)

## Notes

- Keine Code-Änderungen, nur Dokumentation
- Phase 20-1 bis 20-5 implementieren die PWA-Funktionalität, Plan 20-6 beschreibt sie dem User
- Dockerfile und deploy.yml existieren bereits, wurden hier nur referenziert
- README wird bei jedem Push mitge-committed (nicht Teil des Build-Outputs)

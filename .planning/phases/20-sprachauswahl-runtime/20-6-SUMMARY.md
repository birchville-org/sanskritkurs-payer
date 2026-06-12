# Plan 20-6 Summary: README PWA & Docker Sections

**Phase**: 20 Sprachauswahl (Runtime-Filter)  
**Plan**: 06  
**Status**: ✅ Complete  
**Completed**: 2026-06-12

## Deliverable

`README.md` (Repo-Root) — 2 neue Hauptabschnitte hinzugefügt

## Struktur

Vorher:
```
1. Setup & Development
2. Deployment (Hosting on Web Server)
```

Nachher:
```
1. Setup & Development
2. Deployment (Hosting on Web Server)
3. 📱 Progressive Web App (PWA)    ← neu
4. 🐳 Docker                         ← neu
```

## PWA-Sektion (Inhalt)

- **Installation**: 4-Schritt-Guide
  - Browser öffnen
  - "App installieren" Button (oder Add to Home Screen)
  - Settings → Sprachen wählen
  - Confirm
- **Offline Usage**: Cache-Verhalten, Fallback-Page, Nachladen
- **Browser Compatibility Tabelle**: Chrome/Edge 90+, Safari 16.4+, Firefox 90+
- **Cache Management**: Size-Check, Clear, Add/Remove in Settings

## Docker-Sektion (Inhalt)

- **Pull**: `docker pull ghcr.io/marcodem/sanskritkurs-payer:latest`
- **Tags**: `latest`, `v*.*.*` (SemVer), `sha-<commit>`
- **Run Locally**: `docker run -d -p 8080:80 ...`
- **Reverse Proxy**: docker-compose.yml Beispiel
- **Image Internals**: nginx:alpine, ~50MB, Build in GH Actions
- **Build Locally**: Fallback für User ohne GHCR-Zugang

## Technical Notes

- Sprache: Englisch (konsistent mit bestehender README)
- Keine Änderungen an bestehendem Content
- Code-Blöcke: bash (5x), yaml (2x)
- Tabellen: 1 (Browser Compatibility)

## Files Modified

- `README.md` (+88 Zeilen)

## Verification

- ✅ Markdown-Syntax gültig
- ✅ GHCR-URL korrekt (ghcr.io/marcodem/sanskritkurs-payer)
- ✅ Docker-Tags existieren in aktuellem deploy.yml
- ✅ Browser-Versionen konsistent mit Phase 19-4 (Safari iOS 11.3+, Push 16.4+)

## Integration mit anderen Phase 20 Plans

- **20-1 (Settings-Page)**: README verweist auf Settings für Sprachwahl
- **20-5 (Progress-Bar)**: README erwähnt Installation-Flow
- **20-2/20-3/20-4**: werden von End-User nicht direkt wahrgenommen → nicht in README

## Nächste Schritte

- README wird bei nächstem Commit mitgenommen
- Bei Phase 21 Deployment-Test: README-Examples manuell durchprobieren
- Bei v1.4 Release: README als Release-Notes-Quelle nutzen

# Release Notes — v1.5 «Hebrew & PWA Stability»

**Veröffentlicht:** 2026-06-21  
**Vorherige Version:** v1.4.1  
**Phasen:** 22–23

---

## 15. Sprache: Hebräisch (HE)

Das Projekt unterstützt nun eine vollständige RTL-Sprache (Right-To-Left). Hebräisch wurde vollumfänglich übersetzt und in das System integriert:
- 61 Lektionen
- 61 Übungen
- Einführung in die Schrift
- Komplettes alphabetisches Glossar und Wortliste
- Inhaltsverzeichnis und Themenregister

**RTL-Integration & UI**
- Das Hebräische Layout greift nativ auf `dir="rtl"` zurück.
- Die Einstellungsseite (`/he/settings`) wurde vollständig lokalisiert, sodass Nutzer das Interface komplett auf Hebräisch bedienen können.

---

## PWA & Offline-Caching (Bugfix)

**Fehlende Offline-Manifeste behoben**  
Es wurde ein Fehler im Build-Post-Skript (`scripts/gen_locale_manifests.mjs`) behoben, der verhinderte, dass neue Sprachen wie Bahasa Indonesia (ID) und Hebräisch (HE) in den Service-Worker-Cache aufgenommen wurden. 
- Das Skript iteriert nun automatisch über **alle 19 konfigurierten Locales**.
- *Offline First:* Die `manifest-he.json` (143 URLs) und `manifest-id.json` (144 URLs) werden nun nach jedem Build sauber generiert, womit die PWA-Fähigkeit für diese Sprachen vollumfänglich hergestellt ist.

---

## UI & Navigation

**Bulgarisch (Beta) versteckt**  
Die Bulgarisch-Übersetzung (BG) wies strukturelle Schwächen auf. Die Sprache wurde im System (`config.mjs`) belassen, damit bestehende Bookmarks und das Caching weiterhin funktionieren, sie wurde jedoch mittels `custom.css` global aus allen Navigations-Dropdowns ausgeblendet.

**Settings-Page Refactoring**  
Die Einstellungsseite (`PayerLanguageSettings.vue`) trennt nun übersichtlich zwischen:
- *Aktiven Sprachen* (Bereits sichtbar / offline gespeichert)
- *Weitere Sprachen hinzufügen* (Zum Herunterladen verfügbar)

---

## Syntax Cleanup (Container)

Ein dediziertes Python-Bereinigungsskript wurde über **alle 14 Übersetzungssprachen** (`>500 .md` Dateien) angewandt. 
- Veraltete Syntax (`::: container`) wurde strikt zu `:::container` migriert.
- Die "Diese Übersicht beruht auf..." Altlasten in `grammatik.md` wurden ausnahmslos restlos entfernt.
- **Resultat:** Keine CSS-Hiccups oder Parse-Fehler im finalen VitePress-Build mehr.

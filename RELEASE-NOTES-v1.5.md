# Release Notes — v1.5 «Hebrew, Arabic, Aramaic & PWA Stability»

**Veröffentlicht:** 2026-07-10  
**Vorherige Version:** v1.4.1  
**Phasen:** 22–23

---

## 🌎 Neue Sprachen: Hebräisch, Arabisch, Aramäisch & Chinesisch (zh-CN)

Das Projekt wurde um vier wichtige Weltsprachen erweitert. Hebräisch (HE), Arabisch (AR), Aramäisch (ARC) und Vereinfachtes Chinesisch (zh-CN) wurden vollumfänglich übersetzt und nahtlos integriert:
- **Jeweils 61 Lektionen, 61 Übungen und Einführungen in die Schrift.**
* **Komplette Glossare und alphabetische Wortlisten.**
* **Inhaltsverzeichnisse und Themenregister.**

**RTL-Integration (Arabisch & Hebräisch)**
- Die arabischen und hebräischen Layouts greifen nativ auf `dir="rtl"` zurück, um eine korrekte Rechts-nach-Links-Leserichtung zu gewährleisten.
- Die Einstellungsseiten wurden vollständig lokalisiert, sodass Nutzer das Interface komplett in ihrer Landessprache bedienen können.

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

---

## QA Viewer & Fallback System

**KI-Fallback-Architektur für Massenübersetzungen**  
Das Backend-Skript für die Massenübersetzungen (`lan_translate.py`) wurde mit einer dynamischen Fallback-Logik ausgestattet:
- Standardmäßig wird ressourcenschonend auf das lokale **Qwen 3.6 35B** am Mac Studio (`nyx.local`) zugegriffen.
- Schlägt die Qualitätskontrolle bei schwierigen Lektionen dreimal hintereinander fehl, schaltet das System für den jeweiligen fehlerhaften Block automatisch auf **Qwen 2.5 72B via OpenRouter** um.
- Dieses Failover-System garantiert ununterbrochene Übersetzungsdurchläufe über Nacht in höchster Qualität, ohne dass der Prozess bei Formatierungsfehlern stehen bleibt.

**English-Only QA Interface**  
Das Autoren-Werkzeug (QA Viewer) wurde vollständig ins Englische übersetzt, um internationalen Korrektoren und externen Autoren eine einheitliche Bedienung zu ermöglichen.
- **Save-Safeguard:** Der "END QA" Button blockiert nun das versehentliche Schließen des Fensters, wenn ungespeicherte Änderungen vorliegen. Zudem wird der "Save"-Button visuell deaktiviert, falls keine Änderungen seit dem letzten Speichern erkannt wurden.
- **Scroll-Sync:** Editor und Markdown-Vorschau scrollen nun perfekt synchron und proportional mit.


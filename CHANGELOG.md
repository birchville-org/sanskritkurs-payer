# Revision History (Changelog)

Alle wesentlichen Änderungen in diesem Projekt werden in dieser Datei nachgehalten.
Wir orientieren uns am Prinzip des [Semantic Versioning](https://semver.org/lang/de/).

## [1.5.0] - 2026-07-10
### Hinzugefügt
- **Neue Sprachen (HE, AR, ARC, zh-CN):** Vollständige Integration von Hebräisch, Arabisch, Aramäisch und Vereinfachtem Chinesisch über alle 61 Lektionen, Schriften, Übungen und Glossare.
- **RTL UI & Layout:** Unterstützung für `dir="rtl"` in hebräischen und arabischen Ansichten sowie Lokalisierung der Einstellungsseiten.
- **PWA Caching & Manifeste:** Automatisierte Erstellung von PWA-Manifesten für alle 21 Locales zur Gewährleistung der Offline-Fähigkeit aller aktiven Sprachen.

### Geändert
- **QA-Viewer & Lokales Editing:** Lokalisierung des Autoren-Interfaces ins Englische und Integration eines automatischen OpenRouter-Fallback-Systems bei lokalen QC-Fehlern.
- **Settings-Page Refactoring:** Aufteilung in aktive und herunterladbare/hinzufügbare Sprachen.

### Behoben
- **Syntax-Bereinigung:** Umfassender Cleanup veralteter `::: container` Direktiven zu `:::container` zur Beseitigung von Parse-Fehlern im VitePress-Build.
- **Sanskritrot-Styling:** Behebung von CSS-Hiccups bezüglich roter Sanskrit-Zeichen in Tabellen und HTML-Überschreibungen.

## [1.4.0] - 2026-06-15
### Hinzugefügt
- **Offline-First PWA:** Integration eines Service Workers zur vollständigen Offline-Nutzung aller Kursinhalte und Lektionen.
- **Laufzeit-Sprachfilter:** Dynamische Sprachauswahl und Caching-Einstellungen direkt über die Benutzeroberfläche.

## [1.3.0] - 2026-06-03
### Hinzugefügt
- **Markdown-Editor:** Integration eines Split-Pane-Editors mit Live-Vorschau und bidirektionalem, prozentualem Scroll-Sync im QA-Viewer.
- **5 neue Sprachen:** Vollständige Übersetzung des Kurses in Latein (LA), Rumantsch Grischun (RM), Rumänisch (RO), Punjabi (PA) und Indonesisch (ID).
- **Qualitätssicherung:** Einführung des `pre_push_check.py` Skripts zur automatischen Validierung der Markdown-Syntax, Links und HTML-Richtlinien vor Git-Commits.

## [1.2.0] - 2026-05-27
### Hinzugefügt
- **IAST-Suche:** Intelligentes Diakritikafolding zur Suche von Sanskrit-Begriffen ohne Sonderzeichen (z. B. `samskrta` findet `Saṃskṛta`).
- **Modulare Konfiguration:** Aufteilung der VitePress-Konfiguration in sprachspezifische Locale-Dateien zur besseren Wartbarkeit.
- **Thematisches Register:** Dynamischer VitePress Data Loader zur vollautomatischen Generierung eines alphabetischen Themenindexes.
- **Verwandte Lektionen:** Integration der `PayerRelatedLessons`-Komponente unter Einhaltung des Scholarly Synthesis Designs.
- **Russisch & Ukrainisch:** Erweiterung um die locales `/ru/` und `/uk/`.

## [1.1.2] - 2026-04-22
### Behoben
- **Tabellen-Layout:** Fehlerhafte Markdown-Tabellen in Lektion 52 (DE) korrigiert, um eine saubere Darstellung in VitePress zu gewährleisten.

## [1.1.1] - 2026-04-21
### Behoben
- **Build-Fehler:** Unmaskiertes `<Absolutive>`-Tag in `docs/en/lektionen/uebung37.md` korrigiert, das den Vue-Compiler blockierte.

## [1.1.0] - 2026-04-19
### Hinzugefügt
- **Interaktive Quiz-Module:** Einführung der `PayerQuiz`-Komponente zur Selbstdokumentation und Prüfung des Lernfortschritts.
- **Layout-Flexibilität:** Neuer "Wide Mode"-Toggle für die Desktop-Ansicht zur besseren Lesbarkeit langer Sanskrit-Sätze.
- **Internationalisierung (i18n):** Aufbau der englischen Version (`/en/`) inklusive strukturierter Übersetzung der Lektionen und Übungen.
- **Zustandsspeicherung:** Lokale Speicherung von UI-Präferenzen (z.B. Wide Mode) via `localStorage`.

### Geändert
- **Übersetzungsprozess:** Automatisierung der Batch-Übersetzungen von Übungstexten unter Beibehaltung der Devanagari- und IAST-Formatierung.
- **Navigation:** Optimierung der Seitenleiste für die mehrsprachige Struktur.

## [1.0.0] - 2026-04-13
### Hinzugefügt
- Komplette Migration des originalen statischen HTML-Sanskritkurses von Alois Payer.
- Aufbau der Infrastruktur mit **VitePress** für eine moderne, schnelle Applikationsumgebung.
- Akademisches "Scholarly Synthesis" Design in `.vitepress/theme/custom.css` (inkl. Diakritika-Fonts "Source Serif 4" und Inter).
- Automatisiertes Konvertierungs-Skript (`scripts/convert.js`) zur Umwandlung des Payer-HTML-Codes in reines Markdown mittels Turndown und JSDOM.

### Geändert
- **Restrukturierung:** Alle 61 Lektionen und Übungen wurden in handliche Sidebar-Menüblöcke gruppiert (z.B. "Lektion 11 - 20").
- **Navigation:** Implementierung einer maßgeschneiderten, synchronen Akkordeon-Seitenleiste durch Modulation der Vue 3 Engine (`.vitepress/theme/index.mjs`).

### Behoben
- Beseitigung redundanter H1-Titel und Autoren-Vermerke, die Herr Payer in seinen Original-Dateien verstreut hatte.
- Vue-AST-Blockade bei unmaskierten `<caption>` und `<colgroup>` Tabs.
- Visuelles Entfernen alter toter Creative-Commons Bilder aus 2008 von Yahoo/Flickr (Hotlinks wurden neutralisiert).

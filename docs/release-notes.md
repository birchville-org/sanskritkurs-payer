---
layout: doc
title: Release-Notes & Versionsverlauf
description: Übersicht über alle Aktualisierungen, neuen Funktionen und Verbesserungen im Sanskritkurs.
---

# Release-Notes & Versionsverlauf

Auf dieser Seite finden Sie eine Übersicht aller Veröffentlichungen, neuen Funktionen und technischen Optimierungen des Sanskritkurses.

---

## 🚀 Version 1.6.4 (August 2026)

**Schwerpunkt:** *100% Completion in Schlüssel-Zielsprachen, Offline-First PWA & UI-Politur*

### ✨ Neuerungen & Highlights
- **100% Completion ohne Fallbacks**: Englische (`en`) und Russische (`ru`) Sprachversionen sind zu 100% sauber übersetzt (136/136 Dateien, 0 Fallbacks) und schreibgeschützt.
- **Vollständige UI-Lokaliserung (SSOT)**: Sämtliche Navigations- und Steuerelemente (Vorherige/Nächste Lektion, Übungen, Inhaltsverzeichnis) werden in allen aktiven Sprachen dynamisch über ein zentrales Sprachregister bereitgestellt.
- **Typografie & Qualitätssicherung**: Aufrechte Devanāgarī-Typografie ohne Kursivverzerrung, entwirrte Signalrot-Tags und bereinigte Textstellen über alle fertigen Sprachversionen hinweg.
- **PWA & Offline-First**: Vollständige Offline-Nutzung sämtlicher Kursinhalte über alle aktiven Sprachversionen hinweg.
- **Design & Layout**: Optimierte Hero-Darstellung und Kartenlayouts ohne störende Trennlinien.

---

## 🛠 Version 1.6.1 (Juli 2026)

**Schwerpunkt:** *QA-Viewer Parität & Sidebar-Integrität*

- **QA-Viewer Synchronisation**: `#left-lang` und `#right-lang` im QA-Viewer entsprechen exakt der Sprachkonfiguration aus `config.mjs`.
- **Sidebar-Gruppierung**: Behebung von Verschachtelungsfehlern in der Lektions- und Kapitelübersicht.
- **Container-Syntax**: Durchgängige Überprüfung und Absicherung verschachtelter `grammar-box`-Container.

---

## ⚙️ Version 1.6.0 (Juli 2026)

**Schwerpunkt:** *Chirurgische Fallback-Reparaturen & Stabilität*

- **Chirurgische Fallback-Logik**: Automatische Wiederherstellung und Block-für-Block-Neuübersetzung unvollständiger Chunks.
- **Integritätsprüfungen**: Automatisierter Pre-Push Build-Gate zur Verhinderung von fehlerhaften Markdowns.
- **Wortlisten & Glossar**: Vollständige Synchronisation aller Wortlisten und Fachbegriffe über das Gesamtsystem.

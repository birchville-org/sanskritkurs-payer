# 📖 Sanskritkurs Payer — Dokumentation & Projektarchitektur

> **Wissenschaftliche Digitalisierung, Modernisierung und KI-gestützte Übersetzung des Sanskritkurses von Prof. Dr. Alois Payer in über 38 Zielsprachen.**

![License](https://img.shields.io/badge/license-MIT-green)
![Node](https://img.shields.io/badge/node-20%2B-blue)
![VitePress](https://img.shields.io/badge/SSG-VitePress%201.6-purple)
![PWA](https://img.shields.io/badge/PWA-Offline%20Ready-brightgreen)
![Docker](https://img.shields.io/badge/docker-multi--arch-blue)

---

## 🌟 Über das Projekt

Der von **Prof. Dr. Alois Payer** verfasste Sanskritkurs gehört zu den fundiertesten und didaktisch anspruchsvollsten deutschsprachigen Lehrwerken für das klassische Sanskrit. Er zeichnet sich durch außergewöhnliche grammatikalische Präzision, ausführliche Übungen und reichhaltige philologische Erläuterungen aus.

Das Projekt **Sanskritkurs Payer** überführt dieses historische Werk aus dem statischen HTML-Zustand der 1990er Jahre in ein modernes, hochperformantes digitales Ökosystem:
- **Algorithmisches Bereinigen & Standardisieren:** Konvertierung alter HTML-Seiten in valides, strukturiertes Markdown mit typografischen Erweiterungen (`markdown-it-extensible`).
- **Modernes Frontend:** Eine blitzschnelle **VitePress Progressive Web App (PWA)**, die komplett offline nutzbar ist.
- **Autonome KI-Übersetzungspipeline:** Mehrsprachige Ausrollung in über 38 Zielsprachen bei vollständiger Wahrung von Devanāgarī-Schriftzeichen, IAST-Transliteration und Tabellenstrukturen.

---

## 🏛️ Kernartefakte & Projektergebnisse

| Artefakt | Beschreibung | Technologie / Pfad |
| :--- | :--- | :--- |
| **Interaktiver Sanskritkurs** | Vollständiges Lehrbuch mit über 60 Lektionen, Übungen und Schriftlehrgängen | VitePress PWA in `docs/` |
| **Mehrsprachige Editionen** | 35+ vollständig validierte Zielsprachen (140/140 Dateien je Sprache) | LLM-Pipeline (`nyx.local:8000`) |
| **Docker-Container** | Multi-Architektur-Produktionsimages (`linux/amd64`, `linux/arm64`) | `ghcr.io/birchville-org/sanskritkurs-payer:latest` |
| **PWA & Offline-Engine** | Sprachspezifisches Caching (~23 MB pro Sprache), Fallback-Offline-Seiten | Service Worker (`workbox`) |
| **Desktop-Bundles** | Eigenständige native Desktop-Applikation | Tauri DMG (`src-tauri`) |
| **Technische Wiki-Dokumentation** | Systemarchitektur, Übersetzungsstrategie & Sprachkriterien | GitHub Wiki & diese MkDocs-Seite |

---

## 🗺️ Dokumentationsübersicht

1. **[Systemarchitektur](system-architecture.md):**
   Die verteilte 3-Node-Topologie (Workstation `nike.local`, LLM-Server `nyx.local`, Staging/Runner `nataraja.local`), Mermaid-Systemdiagramm und Concurrency-Modell.
2. **[KI-Translations-Pipeline](ai-translation.md):**
   Das Weg-B-Übersetzungskonzept, Translation Memory (TM) mit MD5-Hashing, Devanāgarī-Schutzfilter und 3-Stufen-Modell (Lokal, Sonnet, Gemini).
3. **[Sprachauswahl & Kriterien](languages.md):**
   Quantitative Erkenntnisse aus dem 248,3-Stunden-Benchmark, das 3-Stufen-Ausschlussframework und die 38+ Zielsprachen.
4. **[PWA & Infrastruktur](pwa-infrastructure.md):**
   Service Worker Caching-Strategie, VitePress-Konfiguration, Docker Staging und Release-Workflows.
5. **[Entwickler-Richtlinien](guidelines.md):**
   Devanāgarī/IAST-Satzregeln, grammatikalische Box-Hierarchien (`::: grammar-box`), QA-Gates und Code-Governance.
6. **[Wiki-Übersicht](wiki-home.md):**
   Direkter Zugriff auf das offizielle GitHub-Wiki des Projekts.

---

## 🔗 Externe Links & Repositories

- **Quellcode Repository:** [github.com/birchville-org/sanskritkurs-payer](https://github.com/birchville-org/sanskritkurs-payer)
- **Projekt-Wiki:** [github.com/birchville-org/sanskritkurs-payer/wiki](https://github.com/birchville-org/sanskritkurs-payer/wiki)
- **Container Registry:** [ghcr.io/birchville-org/sanskritkurs-payer](https://ghcr.io/birchville-org/sanskritkurs-payer)
- **Referenzprojekte:**
  - [AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich) — Hybrid-OCR und Buchdigitalisierung
  - [boethlingk](https://github.com/birchville-org/boethlingk) — Pāṇinis Grammatik (1887) Editions-Pipeline

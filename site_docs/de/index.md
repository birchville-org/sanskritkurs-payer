<div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; padding: 1rem 1.25rem; background: var(--md-default-bg-color--light); border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px;">
  <img src="../assets/birchville_logo.png" alt="Birchville Wappen" style="height: 2.4rem; border-radius: 4px; filter: drop-shadow(0 1px 3px rgba(0,0,0,0.18));">
  <div>
    <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--md-accent-fg-color); font-weight: 700;">Birchville Scholarly Synthesis</div>
    <div style="font-size: 0.95rem; font-weight: 600; color: var(--md-default-fg-color);">Kanonische Editionen klassischer philologischer Referenzwerke</div>
  </div>
</div>

# 📖 Sanskritkurs Payer — Dokumentation & Projektarchitektur

**Wissenschaftliche Digitalisierung, Modernisierung und KI-gestützte Übersetzung des Sanskritkurses von Prof. Dr. Alois Payer in über 38 Zielsprachen.**

---

## ⚡ Schnellzugriff & Applikationen

<div class="quick-access-grid">
  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">📦</span>
        <span class="quick-card-title">Releases & Versionen</span>
      </div>
      <div class="quick-card-body">
        Versionshistorie, Release Notes, Quellcode-Archive und Produktions-Builds auf GitHub.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="https://github.com/birchville-org/sanskritkurs-payer/releases/latest" class="quick-btn quick-btn-primary" target="_blank" rel="noopener">
        <span>➔</span> Releases (v1.10.1)
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">🏛️</span>
        <span class="quick-card-title">Systemarchitektur</span>
      </div>
      <div class="quick-card-body">
        Verteilte 3-Node-Topologie mit Workstation (`nike`), LLM-Server (`nyx`) und Staging/Runner (`nataraja`).
      </div>
    </div>
    <div class="quick-card-action">
      <a href="system-architecture/" class="quick-btn quick-btn-outline">
        <span>➔</span> Architektur ansehen
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">🤖</span>
        <span class="quick-card-title">KI-Translations-Pipeline</span>
      </div>
      <div class="quick-card-body">
        Weg-B-Übersetzungskonzept mit Translation Memory, Devanāgarī-Schutzfiltern und 3-Stufen-Modell.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="ai-translation/" class="quick-btn quick-btn-outline">
        <span>➔</span> Pipeline ansehen
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">💻</span>
        <span class="quick-card-title">Quellcode & Pipeline</span>
      </div>
      <div class="quick-card-body">
        Open-Source-Code, Markdown-Parser (`markdown-it-extensible`), Service Worker und Docker-Konfiguration auf GitHub.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="https://github.com/birchville-org/sanskritkurs-payer" class="quick-btn quick-btn-outline" target="_blank" rel="noopener">
        <span>➔</span> GitHub Repository
      </a>
    </div>
  </div>
</div>

---

## 🌟 Über das Projekt

Der von **Prof. Dr. Alois Payer** verfasste Sanskritkurs gehört zu den fundiertesten und didaktisch anspruchsvollsten deutschsprachigen Lehrwerken für das klassische Sanskrit. Er zeichnet sich durch außergewöhnliche grammatikalische Präzision, ausführliche Übungen und reichhaltige philologische Erläuterungen aus.

Das Projekt **Sanskritkurs Payer** überführt dieses historische Werk aus dem statischen HTML-Zustand der 1990er Jahre in ein modernes, hochperformantes digitales Ökosystem:
- **Algorithmisches Bereinigen & Standardisieren:** Konvertierung alter HTML-Seiten in valides, strukturiertes Markdown mit typografischen Erweiterungen (`markdown-it-extensible`).
- **Modernes Frontend:** Eine blitzschnelle **VitePress Progressive Web App (PWA)**, die komplett offline nutzbar ist.
- **Autonome KI-Übersetzungspipeline:** Mehrsprachige Ausrollung in über 38 Zielsprachen bei vollständiger Wahrung von Devanāgarī-Schriftzeichen, IAST-Transliteration und Tabellenstrukturen.

---

## 🏛️ Kernartefakte & Projektergebnisse

- **Interaktiver Sanskritkurs (PWA)** (`docs/`)  
  Vollständiges Lehrbuch mit über 60 Lektionen, interaktiven Übungen und Schriftlehrgängen in einer offlinefähigen VitePress Progressive Web App.  
  [:octicons-tag-16: Release v1.10.1](https://github.com/birchville-org/sanskritkurs-payer/releases/latest) · [:octicons-mark-github-16: Quellcode in `docs/`](https://github.com/birchville-org/sanskritkurs-payer/tree/main/docs)

- **Mehrsprachige Editionen (38+ Zielsprachen)**  
  35+ vollständig validierte Zielsprachen (140/140 Dateien je Sprache) mit strikter Wahrung von Devanāgarī-Graphemen und IAST-Diakritika via LLM-Pipeline (`nyx.local:8000`).  
  [:octicons-book-16: Sprachauswahl & Kriterien](languages.md) · [:octicons-cpu-16: KI-Translations-Pipeline](ai-translation.md)

- **Produktions-Docker-Images** (`ghcr.io/birchville-org/sanskritkurs-payer:latest`)  
  Multi-Architektur-Produktionsimages (`linux/amd64`, `linux/arm64`) für lokale und containerisierte Serverbereitstellung.  
  [:octicons-container-16: GitHub Container Registry](https://ghcr.io/birchville-org/sanskritkurs-payer)

- **PWA & Offline-Engine** (`workbox`)  
  Sprachspezifisches Caching (~23 MB pro Sprache) für vollständig autarke Offline-Nutzung inklusive Fallback-Seiten.  
  [:octicons-workflow-16: PWA & Infrastruktur](pwa-infrastructure.md)

- **Desktop-Bundles** (`src-tauri`)  
  Eigenständige native Desktop-Applikation für macOS und Linux mit nativer Menüführung und Offline-Assets.  
  [:octicons-device-desktop-16: Quellcode in `src-tauri`](https://github.com/birchville-org/sanskritkurs-payer/tree/main/src-tauri)

- **Technische Dokumentation (GitHub Pages)**  
  Vollständige technische Architektur-, Translations- und Richtlinien-Dokumentation.  
  [:octicons-repo-16: GitHub Repository](https://github.com/birchville-org/sanskritkurs-payer)

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

## 📜 Lizenz & Urheberschaft

- **Originalwerk**: Prof. Dr. Alois Payer (Tübingen).
- **Digitale Neufassung, KI-Pipeline & Web-App**: [MIT License](https://github.com/birchville-org/sanskritkurs-payer/blob/main/LICENSE) (Copyright (c) 2026 Marco Demarmels / Birchville Foundation).
- **Referenzprojekte**:
  - [AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich) — Hybrid-OCR und Buchdigitalisierung
  - [macdonell](https://github.com/birchville-org/macdonell) — A Vedic Grammar for Students (1916) 1:1 Neusatz
  - [boethlingk](https://github.com/birchville-org/boethlingk) — Pāṇinis Grammatik (1887) Editions-Pipeline

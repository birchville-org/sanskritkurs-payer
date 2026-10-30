<div style="display: flex; align-items: center; gap: 1rem; margin-bottom: 1.5rem; padding: 1rem 1.25rem; background: var(--md-default-bg-color--light); border: 1px solid var(--md-default-fg-color--lightest); border-radius: 8px;">
  <img src="../assets/birchville_logo.png" alt="Birchville Coat of Arms" style="height: 2.4rem; border-radius: 4px; filter: drop-shadow(0 1px 3px rgba(0,0,0,0.18));">
  <div>
    <div style="font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.08em; color: var(--md-accent-fg-color); font-weight: 700;">Birchville Scholarly Synthesis</div>
    <div style="font-size: 0.95rem; font-weight: 600; color: var(--md-default-fg-color);">Canonical Editions of Classical Indological Reference Works</div>
  </div>
</div>

# 📖 Sanskritkurs Payer — Documentation & Architecture

**Scholarly digitization, modernization, and AI-powered translation of Prof. Dr. Alois Payer's Sanskrit Course across 38+ target languages.**

---

## ⚡ Quick Access & Applications

<div class="quick-access-grid">
  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">📦</span>
        <span class="quick-card-title">Releases & Versions</span>
      </div>
      <div class="quick-card-body">
        Version history, release notes, source archives, and production builds on GitHub.
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
        <span class="quick-card-title">System Architecture</span>
      </div>
      <div class="quick-card-body">
        Distributed 3-node topology with workstation (`nike`), dedicated LLM server (`nyx`), and staging runner (`nataraja`).
      </div>
    </div>
    <div class="quick-card-action">
      <a href="system-architecture/" class="quick-btn quick-btn-outline">
        <span>➔</span> System Architecture
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">🤖</span>
        <span class="quick-card-title">AI Translation Pipeline</span>
      </div>
      <div class="quick-card-body">
        Weg-B translation strategy with Translation Memory, Devanāgarī protection filters, and 3-stage model hierarchy.
      </div>
    </div>
    <div class="quick-card-action">
      <a href="ai-translation/" class="quick-btn quick-btn-outline">
        <span>➔</span> Translation Pipeline
      </a>
    </div>
  </div>

  <div class="quick-card">
    <div>
      <div class="quick-card-header">
        <span class="quick-card-icon">💻</span>
        <span class="quick-card-title">Source Code & Pipeline</span>
      </div>
      <div class="quick-card-body">
        Open-source repository, Markdown parser (`markdown-it-extensible`), Service Worker, and Docker setups on GitHub.
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

## 🌟 About the Project

The Sanskrit course authored by **Prof. Dr. Alois Payer** is one of the most comprehensive and academically rigorous German-language resources for learning classical Sanskrit. It is distinguished by its meticulous grammatical structure, extensive exercise sets, and rich philological commentary.

The **Sanskritkurs Payer** project transitions this academic resource from static 1990s HTML manuscripts into a modern, high-performance digital publishing platform:
- **Algorithmic Cleanup & Standardization:** Transforming raw HTML into structured, future-proof Markdown with custom typographical extensions (`markdown-it-extensible`).
- **Modern Web Architecture:** An ultra-fast **VitePress Progressive Web App (PWA)** capable of running completely offline.
- **Autonomous AI Translation Pipeline:** Multilingual expansion across 38+ target languages while strictly preserving Devanāgarī characters, IAST transliterations, and complex grammar tables.

---

## 🏛️ Core Artifacts & Deliverables

- **Interactive Sanskrit Course (PWA)** (`docs/`)  
  Complete digital textbook with 60+ lessons, interactive exercises, and script guides in an offline-ready VitePress Progressive Web App.  
  [:octicons-tag-16: Release v1.10.1](https://github.com/birchville-org/sanskritkurs-payer/releases/latest) · [:octicons-mark-github-16: Source Code in `docs/`](https://github.com/birchville-org/sanskritkurs-payer/tree/main/docs)

- **Multilingual Editions (38+ Target Languages)**  
  35+ fully validated target languages (140/140 files per language) preserving Devanāgarī graphemes and IAST diacritics via LLM pipeline (`nyx.local:8000`).  
  [:octicons-book-16: Language Selection & Criteria](languages.md) · [:octicons-cpu-16: AI Translation Pipeline](ai-translation.md)

- **Production Docker Containers** (`ghcr.io/birchville-org/sanskritkurs-payer:latest`)  
  Multi-architecture production images (`linux/amd64`, `linux/arm64`) for local and server-side deployment.  
  [:octicons-container-16: GitHub Container Registry](https://ghcr.io/birchville-org/sanskritkurs-payer)

- **PWA & Offline Engine** (`workbox`)  
  Language-partitioned caching (~23 MB per language) for autonomous offline execution including fallback mechanisms.  
  [:octicons-workflow-16: PWA & Infrastructure](pwa-infrastructure.md)

- **Desktop Applications** (`src-tauri`)  
  Standalone native desktop application for macOS and Linux with system menu integration and local asset storage.  
  [:octicons-device-desktop-16: View Source in `src-tauri`](https://github.com/birchville-org/sanskritkurs-payer/tree/main/src-tauri)

- **Technical Documentation (GitHub Pages)**  
  Comprehensive system architecture, translation methodology, and developer guidelines.  
  [:octicons-repo-16: GitHub Repository](https://github.com/birchville-org/sanskritkurs-payer)

---

## 🗺️ Documentation Overview

1. **[System Architecture](system-architecture.md):**  
   Distributed 3-node topology (Workstation `nike.local`, LLM engine `nyx.local`, Staging/Runner `nataraja.local`), Mermaid system diagrams, and concurrency constraints.
2. **[AI Translation Pipeline](ai-translation.md):**  
   The Weg B translation strategy, Translation Memory (TM) with MD5 hashing, Devanāgarī protection filters, and 3-stage model hierarchy (Local, Sonnet, Gemini).
3. **[Language Selection & Criteria](languages.md):**  
   Empirical findings from the 248.3-hour GPU benchmark, the 3-tier exclusion framework, and the 38+ language matrix.
4. **[PWA & Infrastructure](pwa-infrastructure.md):**  
   Service Worker caching strategies, VitePress multi-lingual setup, Docker staging, and release pipelines.
5. **[Developer Guidelines](guidelines.md):**  
   Devanāgarī/IAST typographical rules, grammar-box syntax conventions (`::: grammar-box`), QA gates, and code governance.
6. **[Wiki Index](wiki-home.md):**  
   Direct index of all reference articles in the official GitHub Wiki.

---

## 📜 License & Provenance

- **Original Work**: Prof. Dr. Alois Payer (Tübingen).
- **Digital Edition, AI Pipeline & Web App**: [MIT License](https://github.com/birchville-org/sanskritkurs-payer/blob/main/LICENSE) (Copyright (c) 2026 Marco Demarmels / Birchville Foundation).
- **Referenced Projects**:
  - [AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich) — Hybrid OCR & Book Digitization Pipeline
  - [macdonell](https://github.com/birchville-org/macdonell) — A Vedic Grammar for Students (1916) 1:1 Digital Typeset
  - [boethlingk](https://github.com/birchville-org/boethlingk) — Pāṇini's Grammar (1887) Edition Pipeline

# 📖 Sanskritkurs Payer — Documentation & Architecture

> **Scholarly digitization, modernization, and AI-powered translation of Prof. Dr. Alois Payer's Sanskrit Course across 38+ target languages.**

![License](https://img.shields.io/badge/license-MIT-green)
![Node](https://img.shields.io/badge/node-20%2B-blue)
![VitePress](https://img.shields.io/badge/SSG-VitePress%201.6-purple)
![PWA](https://img.shields.io/badge/PWA-Offline%20Ready-brightgreen)
![Docker](https://img.shields.io/badge/docker-multi--arch-blue)

---

## 🌟 About the Project

The Sanskrit course authored by **Prof. Dr. Alois Payer** is one of the most comprehensive and academically rigorous German-language resources for learning classical Sanskrit. It is distinguished by its meticulous grammatical structure, extensive exercise sets, and rich philological commentary.

The **Sanskritkurs Payer** project transitions this academic resource from static 1990s HTML manuscripts into a modern, high-performance digital publishing platform:
- **Algorithmic Cleanup & Standardization:** Transforming raw HTML into structured, future-proof Markdown with custom typographical extensions (`markdown-it-extensible`).
- **Modern Web Architecture:** An ultra-fast **VitePress Progressive Web App (PWA)** capable of running completely offline.
- **Autonomous AI Translation Pipeline:** Multilingual expansion across 38+ target languages while strictly preserving Devanāgarī characters, IAST transliterations, and complex grammar tables.

---

## 🏛️ Core Artifacts & Deliverables

| Artifact | Description | Technology / Path |
| :--- | :--- | :--- |
| **Interactive Sanskrit Course** | Comprehensive textbook with 60+ lessons, exercise modules, and writing guides | VitePress PWA in `docs/` |
| **Multilingual Editions** | 35+ fully validated target languages (140/140 files per language) | LLM Pipeline (`nyx.local:8000`) |
| **Docker Containers** | Multi-architecture production container images (`linux/amd64`, `linux/arm64`) | `ghcr.io/birchville-org/sanskritkurs-payer:latest` |
| **PWA & Offline Engine** | Language-partitioned cache (~23 MB per language), offline fallback system | Service Worker (`workbox`) |
| **Desktop Bundles** | Standalone native desktop application | Tauri DMG (`src-tauri`) |
| **Technical Documentation** | System architecture, translation strategy & language evaluation criteria | GitHub Wiki & this MkDocs site |

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

## 🔗 External Links & Repositories

- **Source Code Repository:** [github.com/birchville-org/sanskritkurs-payer](https://github.com/birchville-org/sanskritkurs-payer)
- **Project Wiki:** [github.com/birchville-org/sanskritkurs-payer/wiki](https://github.com/birchville-org/sanskritkurs-payer/wiki)
- **Container Registry:** [ghcr.io/birchville-org/sanskritkurs-payer](https://ghcr.io/birchville-org/sanskritkurs-payer)
- **Related Projects:**
  - [AlexandriaSandwich](https://github.com/birchville-org/AlexandriaSandwich) — Hybrid OCR & Book Digitization Pipeline
  - [boethlingk](https://github.com/birchville-org/boethlingk) — Pāṇini's Grammar (1887) Edition Pipeline

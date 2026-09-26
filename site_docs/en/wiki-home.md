# 📚 Project Wiki Index

The official technical wiki for the **Sanskritkurs Payer** project is maintained and synchronized as an independent Git repository (`payer.wiki`). It provides in-depth treatises on system architecture, historical background, and empirical research findings.

---

## 📑 Wiki Articles Overview

### 1. [System Architecture & Multi-Node Topology](system-architecture.md)
*Wiki Original: `System-Architecture.md`*  
Comprehensive architectural specification covering hardware distribution across three dedicated nodes (**Workstation: `nike.local`**, **`nyx.local` LLM engine**, and **`nataraja.local` Linux server/runner**), complete with Mermaid topology diagrams, staging servers, and concurrency models.

### 2. [AI Translation Methods & Weg B Pipeline](ai-translation.md)
*Wiki Original: `AI-Translation-Methods.md`*  
In-depth documentation of the 3-stage model hierarchy (Local 35B model, Claude Sonnet, Gemini 2.5 Pro), Devanāgarī protection filters, TM cache hashing, and deadlock recovery routines.

### 3. [Prof. Payer's Sanskrit Course — Vision & Heritage](index.md)
*Wiki Original: `Prof-Payers-Sanskrit-Course.md`*  
The origins of the original course, legacy 1990s HTML conversion challenges, and the architectural transition to a modern VitePress Progressive Web App (PWA).

### 4. [Language Selection & Exclusion Criteria](languages.md)
*Wiki Original: `Language-Selection-and-Exclusion-Criteria.md`*  
Empirical metrics from the 248.3-hour GPU benchmark, root-cause analysis of bottleneck languages (token penalty, vocabulary sparsity), and the formal 3-tier exclusion framework.

---

## 🔄 Wiki Synchronization

Technical documentation updates are synchronized between this documentation portal and the GitHub Wiki.

- **GitHub Wiki:** [github.com/birchville-org/sanskritkurs-payer/wiki](https://github.com/birchville-org/sanskritkurs-payer/wiki)
- **Local Clone:** `/Volumes/SanDisk1TB/proj/payer.wiki`

# 📐 System Architecture

## 1. Overview & Objectives

The **Payer Sanskritkurs Translation & Publishing System** is built on a distributed 3-node topology designed for zero-cost local AI inference, continuous quality assurance, automated web publishing, and semantic vector indexing.

By physically decoupling **interactive pair-programming**, **compute-heavy LLM inference**, and **CI/CD background builds**, the architecture maximizes throughput, guarantees stability, and prevents memory deadlocks.

> [!IMPORTANT]
> All automated translation operations adhere to the strict **Single-Process Constraint**: At any given time, exactly one translation process (`lan_translate.py`) communicates with `nyx.local` to maintain 100% VRAM efficiency and a stable throughput of ~20 tokens/sec.

---

## 2. Distributed Topology (Mermaid Diagram)

```mermaid
flowchart TB
    subgraph Workstation["💻 Workstation (nike.local - Mac M2, 24GB VRAM)"]
        IDE["Antigravity IDE / Pair Programmer"]
        SSD["Local NVMe Storage\n(/Volumes/SanDisk1TB/proj/Payer)"]
        GIT["Git Workspace & Control Scripts"]
    end

    subgraph Nyx["🚀 Nyx (Dedicated LLM Server - nyx.local - MacBook Air M4, 32GB VRAM)"]
        MLX["mlx_lm.server (Port 8000)"]
        MODEL["Qwen3.6-35B-A3B-4bit-DWQ\n(24GB VRAM allocated)"]
    end

    subgraph Nataraja["☸️ Nataraja (Pop!_OS Intel Mac - nataraja.local, 32GB RAM)"]
        GHR["GitHub Self-Hosted Runner (nataraja)"]
        DOCKER["Docker Staging Web Server\n• Public: Port 8080\n• Author: Port 8081"]
        OLLAMA["Ollama Server (Port 11434)\n• nomic-embed-text\n• qwen2.5:7b"]
        AUDIT["Mobile Link Auditor & Quality Scorer"]
        EXPORT["PDF & EPUB Exporter"]
        VAULT["TM Cache & Session Vault"]
    end

    subgraph GitHub["☁️ GitHub Remote"]
        GH_REPO["birchville-org/sanskritkurs-payer (main)"]
        GHCR["GitHub Container Registry (ghcr.io)"]
        GH_PAGES["GitHub Pages (Documentation)"]
        GH_REL["GitHub Release Assets (.epub / .pdf)"]
    end

    IDE -->|Local Development| SSD
    GIT -->|Push / Commit| GH_REPO
    GIT -->|HTTP Chunks / Weg B| MLX
    MLX -->|Inference| MODEL
    GH_REPO -->|Long-Polling WebSocket| GHR
    GHR -->|VitePress Build (38 Locales)| DOCKER
    GHR -->|Vector Indexing| OLLAMA
    GHR -->|Quality Audit| AUDIT
    GHR -->|Export Generation| EXPORT
    GHR -->|Backup Vaulting| VAULT
    GHR -->|Push Multi-Arch Images| GHCR
    EXPORT -->|Upload Release Assets| GH_REL

    style Workstation fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style Nyx fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style Nataraja fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style GitHub fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
```

---

## 3. Dedicated Hardware Nodes

### Node 1: Workstation (`nike.local`)
- **Hardware:** Apple Silicon M2, 24 GB Unified Memory.
- **Role:** Primary development host, Git repository management, and translation controller (`scripts/lan_translate.py`, `scripts/translation_qa.py`).
- **Responsibilities:** File operations, text chunking, TM persistence, and manual QA validation.

### Node 2: Dedicated LLM Engine (`nyx.local`)
- **Hardware:** Apple Silicon M4 MacBook Air, 32 GB Unified Memory.
- **Role:** Local neural inference daemon running `mlx_lm.server` (Port 8000).
- **Model:** `Qwen3.6-35B-A3B-4bit-DWQ` (dedicated 24 GB VRAM allocation).
- **Throughput:** Delivers consistent ~20–22 tokens/sec for chunk sizes under 1,500 characters without thermal throttling.

### Node 3: Linux Server & Runner (`nataraja.local`)
- **Hardware:** Apple Intel Mac (Quad-Core i7, 32 GB RAM) running Pop!_OS Linux.
- **Role:** CI/CD backbone, Docker staging server, and GitHub self-hosted runner.
- **Responsibilities:**
  - Multi-locale VitePress full build (38 locales under 32 GB swap).
  - Staging servers on Port 8080 (Public) and Port 8081 (Author/Review).
  - Semantic embeddings via Ollama (`nomic-embed-text`).
  - Automated Translation Memory backup routines and snapshot vaults.

---

## 4. Software Pipeline & Data Flow

```text
[Master Markdown (docs/lektionen/*.md)]
             │
             ▼
[scripts/translation_qa.py] ── (Status Validation & Queue Generation)
             │
             ▼
[scripts/lan_translate.py] ── (Chunking < 1500 chars, YAML Frontmatter)
             │
             ├──► [TM Cache: .payer/tm/<lang>.json] (MD5 Hash Hit? ──► Skip)
             │
             ▼ (Cache Miss)
[HTTP Inference Request] ──► http://nyx.local:8000/v1/chat/completions
             │
             ▼
[Sanitization & Devanāgarī Protection] (scripts/file_processor.py)
             │
             ├──► [TM Storage]
             ▼
[Target Markdown: docs/<lang>/lektionen/*.md]
```

---

## 5. Quality Gates & Verification Standards

1. **Gate A: Tag & Devanāgarī Invariance:**
   Every translated chunk must preserve all Devanāgarī wrappers (`⟪...⟫`) and signal-red markers (`:sig[...]`) without alteration.
2. **Gate B: Residue Scanner:**
   Automated detection of untranslated German fragments (`scan_german_residues`). Files containing residual text are rejected immediately.
3. **Gate C: Single Source of Truth (`translation_qa.py`):**
   The QA queue script is the sole authority on status determination. Ad-hoc heuristics in custom scripts are strictly prohibited.

# System Architecture Specification

## 1. Executive Summary

The **Payer Sanskritkurs Translation & Publishing System** is a distributed, multi-node architecture designed for high-performance AI translation, continuous quality assurance, automated web publishing, and vector-search indexing.

The system decouples **interactive development/pair-programming**, **heavy LLM inference**, and **CI/CD background builds** across three dedicated nodes in the local network.

> [!IMPORTANT]
> All automated translation tasks adhere strictly to the **Single-Process Constraint** (`ps aux | grep lan_translate`) to guarantee 100% VRAM efficiency and maximum throughput (~20 t/s) on `nyx.local`.

---

## 2. Distributed System Topology (Mermaid Diagram)

```mermaid
flowchart TB
    subgraph Workstation["💻 Workstation (nike.local - Mac M2, 24GB VRAM)"]
        IDE["Antigravity IDE / Pair Programmer"]
        SSD["Local NVMe Storage\n(/Volumes/SanDisk1TB/proj/Payer)"]
        GIT["Git Local Workspace & Control Scripts"]
    end

    subgraph Nyx["🚀 Nyx (Dedicated LLM Engine - nyx.local - MacBook Air M4, 32GB VRAM)"]
        MLX["mlx_lm.server (Port 8000)"]
        MODEL["Qwen3.6-35B-A3B-4bit-DWQ\n(24GB allocated)"]
    end

    subgraph Nataraja["☸️ Nataraja (Pop!_OS Intel Mac - nataraja.local, 32GB RAM)"]
        GHR["GitHub Self-Hosted Runner (nataraja)"]
        DOCKER["Docker Staging Web Server\n• Public: Port 8080\n• Author: Port 8081"]
        OLLAMA["Ollama Server (Port 11434)\n• nomic-embed-text\n• qwen2.5:7b"]
        AUDIT["Mobile Link Auditor & Quality Scorer\n• audit_mobile_links.py\n• score_translation_quality.py"]
        EXPORT["PDF & EPUB Exporter\n(export_pdf_epub.py)"]
        VAULT["TM Cache & Session Vault\n(/home/marco/payer_backups)"]
        VEC["Vector Indexing Engine\n(build_vector_index.py)"]
    end

    subgraph GitHub["☁️ GitHub Remote"]
        GH_REPO["marcodem/sanskritkurs-payer (main)"]
        GHCR["GitHub Container Registry (ghcr.io)"]
        GH_REL["GitHub Release Assets (.epub / .pdf)"]
    end

    %% Interactions & Styling
    IDE -->|Local Dev & Editing| SSD
    GIT -->|Push Code / Commit| GH_REPO
    GIT -->|HTTP Chunks / Weg B| MLX
    MLX -->|Inference| MODEL
    GH_REPO -->|Long-Polling WebSocket| GHR
    GHR -->|Build VitePress 35 Locales| DOCKER
    GHR -->|Execute Vector Indexing| OLLAMA
    GHR -->|Execute Mobile & Quality Audit| AUDIT
    GHR -->|Build PDF & EPUB Artifacts| EXPORT
    GHR -->|Create Backups| VAULT
    GHR -->|Build & Push Multi-Arch Images| GHCR
    EXPORT -->|Upload Artifacts to Releases| GH_REL

    style Workstation fill:#03192e,color:#fff,stroke:#48626e,stroke-width:2px
    style Nyx fill:#241500,color:#fff,stroke:#e67e22,stroke-width:2px
    style Nataraja fill:#1b4332,color:#fff,stroke:#2d6a4f,stroke-width:2px
    style GitHub fill:#2d3748,color:#fff,stroke:#4a5568,stroke-width:2px
```

---

## 3. Node Specifications & Role Distribution

| Node | OS & Hardware | Primary Responsibilities | Network Endpoints |
| :--- | :--- | :--- | :--- |
| **nike.local** | macOS (Apple Silicon M2, 24GB Unified Memory/VRAM) | • Interactive Pair Programming with Antigravity IDE<br>• Code Editing & Git Control<br>• Translation Runner Trigger (`lan_translate.py`) | Local NVMe (`/Volumes/SanDisk1TB/proj/Payer`) |
| **nyx.local** | macOS (MacBook Air M4, 32GB Unified Memory/VRAM) | • Dedicated 35B Heavy LLM Mass Translation Server<br>• Zero-Cost Local Inference (~20 tokens/sec) | `http://nyx.local:8000` |
| **nataraja.local** | Pop!_OS 24.04 Linux (Intel Core i7-8700B, 32GB RAM, NVMe SSD) | • GitHub Self-Hosted Runner (`nataraja`)<br>• VitePress 35-Locale Quality Gate & Build Server<br>• Local Live-Staging Container Host (Public :8080, Author :8081)<br>• Mobile Link Auditor & Quality Benchmark Engine<br>• Automated PDF & EPUB Course Book Exporter<br>• Auxiliary Ollama LLM & Vector Search Engine<br>• Automated TM & Session Vault Manager | • SSH: `marco@nataraja.local`<br>• Public Staging: `http://nataraja.local:8080`<br>• Author Staging: `http://nataraja.local:8081`<br>• Ollama: `http://nataraja.local:11434` |

---

## 4. Pipeline Execution Workflows

### 4.1. AI Mass Translation Pipeline (Weg B Strategy)
- **Sequential 1-to-1 Translation**: Strict single-process rule to prevent VRAM context-switching stalls on `nyx.local`.
- **Completion Criteria**: 100% clean files (136/136) with 0 fallbacks before transitioning to the next language.
- **Priority Queue Overrides**: Priority order configured via `priority_override = ["en", "bg"]` in `generate_report.py`, automatically falling back to highest completion % descending.
- **Force Session (Weg B)**: Full fresh translations (`-f`) bypass legacy cached fallbacks.

### 4.2. CI/CD Quality Gate & Staging Pipeline (`ci.yml`)
When code is pushed to `main`:
1. **GitHub Runner Event**: GitHub triggers `ci.yml` via outbound long-polling to `nataraja`.
2. **Integrity Validation**: Runs `python3 scripts/pre_push_check.py` to enforce zero-HTML, YAML frontmatter, container boundaries (`::::`), and QA dropdown parity.
3. **35-Locale Site Generation**: Compiles VitePress for both `public` and `author` environments utilizing 32GB physical RAM on Nataraja.
4. **Live Staging Containers**: Restarts Nginx containers `payer-staging` (Port 8080) and `payer-author-staging` (Port 8081).
5. **Mobile & Link Audit**: Executes `scripts/audit_mobile_links.py` to verify internal links and PWA manifest integrity.
6. **Quality Benchmark**: Executes `scripts/score_translation_quality.py` to compute Devanāgarī preservation ratios.
7. **Auxiliary QA & Remnant Scan**: Executes `scripts/qa_german_remnants.py`.
8. **Vector Indexing**: Runs `scripts/build_vector_index.py` against Ollama `nomic-embed-text` on Nataraja.
9. **Vault Archiving**: Archives `.payer/tm/` to `/home/marco/payer_backups/tm_backup_<timestamp>.tar.gz`.

### 4.3. Release Asset Pipeline (`deploy.yml`)
When an official release tag (e.g. `v1.6.5`) is pushed:
1. Multi-platform Docker builds for `linux/amd64` and `linux/arm64` pushed to `ghcr.io`.
2. PDF & EPUB exporter (`scripts/export_pdf_epub.py`) builds consolidated course books.
3. Uploads generated `.epub` and `.pdf` files directly as GitHub Release Assets via `gh release upload`.

---

## 5. Architectural Log & Change History

| Date | Category | Description | Impact |
| :--- | :--- | :--- | :--- |
| **2026-08-11** | **Artifact Exporter** | Added automated PDF & EPUB exporter (`export_pdf_epub.py`) and release asset uploader. | Publishes EPUB & PDF course books on GitHub Releases. |
| **2026-08-11** | **Auditing & QA** | Added Mobile Link Auditor (`audit_mobile_links.py`) and Quality Scorer (`score_translation_quality.py`). | Automated link, PWA, and Devanāgarī preservation scoring. |
| **2026-08-11** | **Staging Server** | Deployed `payer-author-staging` container on port 8081. | Provides dedicated author/QA staging host alongside public site on 8080. |
| **2026-08-11** | **Node Hardware** | Specified `nyx.local` as MacBook Air M4 (32GB Unified Memory/VRAM). | Documented exact M4 generation architecture. |
| **2026-08-11** | **Workstation** | Identified primary Mac workstation as `nike.local` (M2, 24GB VRAM). | Documented node hostname and Apple Silicon M2 specs. |
| **2026-08-11** | **Infrastructure** | Added `nataraja` (Pop!_OS Intel Mac 32GB RAM) as dedicated GitHub Self-Hosted Runner. | Shifted site builds and Docker multi-arch builds off Workstation Mac. |
| **2026-08-11** | **Staging Suite** | Integrated Local Staging Web Server (`http://nataraja.local:8080`) into Nataraja CI workflow. | Enables instant local network preview of built site on any device. |
| **2026-08-11** | **AI Infrastructure** | Provisioned Ollama (`nomic-embed-text`, `qwen2.5:7b`) on Nataraja. | Offloaded embeddings & secondary checks from `nyx.local:8000`. |
| **2026-08-11** | **Backup System** | Activated automated TM Cache Vault archiving on Nataraja. | Guaranteed 100% recovery safety for translation memory files. |
| **2026-08-11** | **Pipeline Logic** | Configured `generate_report.py` priority queue sequence (`EN` ➔ `BG`). | Enforced exact Weg B sequence override requested by user. |

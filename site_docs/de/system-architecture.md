# 📐 Systemarchitektur

## 1. Übersicht & Zielsetzung

Das **Payer Sanskritkurs Übersetzungs- und Publikationssystem** basiert auf einer verteilten 3-Node-Topologie, die für lokale KI-Inferenz, kontinuierliche Qualitätssicherung, automatisierte Web-Generierung und semantische Vektorsuche optimiert ist.

Durch die physische Entkopplung von **interaktiver Entwicklung**, **rechenintensiver LLM-Inferenz** und **Hintergrund-Builds/Staging** werden Ressourcen optimal ausgelastet und Deadlocks vermieden.

> [!IMPORTANT]
> Für alle automatisierten Übersetzungsaufgaben gilt die strikte **Single-Process Constraint**: Es darf zu jedem Zeitpunkt maximal ein Übersetzungsprozess (`lan_translate.py`) auf `nyx.local` zugreifen, um 100 % VRAM-Effizienz und einen kontinuierlichen Durchsatz von ~20 Tokens/s zu garantieren.

---

## 2. Verteilte Topologie (Mermaid-Diagramm)

```mermaid
flowchart TB
    subgraph Workstation["💻 Workstation (nike.local - Mac M2, 24GB VRAM)"]
        IDE["Antigravity IDE / Pair Programmer"]
        SSD["Lokaler NVMe-Speicher\n(/Volumes/SanDisk1TB/proj/Payer)"]
        GIT["Git Workspace & Steuerungs-Skripte"]
    end

    subgraph Nyx["🚀 Nyx (Dedicated LLM Server - nyx.local - MacBook Air M4, 32GB VRAM)"]
        MLX["mlx_lm.server (Port 8000)"]
        MODEL["Qwen3.6-35B-A3B-4bit-DWQ\n(24GB VRAM allokiert)"]
    end

    subgraph Nataraja["☸️ Nataraja (Pop!_OS Intel Mac - nataraja.local, 32GB RAM)"]
        GHR["GitHub Self-Hosted Runner (nataraja)"]
        DOCKER["Docker Staging Webserver\n• Public: Port 8080\n• Author: Port 8081"]
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

    IDE -->|Lokale Entwicklung| SSD
    GIT -->|Push / Commit| GH_REPO
    GIT -->|HTTP Chunks / Weg B| MLX
    MLX -->|Inferenz| MODEL
    GH_REPO -->|Long-Polling WebSocket| GHR
    GHR -->|VitePress Build (38 Locales)| DOCKER
    GHR -->|Vektor-Indexierung| OLLAMA
    GHR -->|Qualitäts-Audit| AUDIT
    GHR -->|Export-Generierung| EXPORT
    GHR -->|Backup & Archivierung| VAULT
    GHR -->|Multi-Arch Images pushen| GHCR
    EXPORT -->|Releases hochladen| GH_REL

    style Workstation fill:#e3f2fd,stroke:#1976d2,stroke-width:2px
    style Nyx fill:#fff3e0,stroke:#f57c00,stroke-width:2px
    style Nataraja fill:#e8f5e9,stroke:#2e7d32,stroke-width:2px
    style GitHub fill:#f3e5f5,stroke:#7b1fa2,stroke-width:2px
```

---

## 3. Die drei Hardware-Nodes

### Node 1: Workstation (`nike.local`)
- **Hardware:** Apple M2, 24 GB Unified Memory.
- **Rolle:** Primäre Entwicklungsumgebung, Git-Repository-Verwaltung, Steuerungsskripte (`scripts/lan_translate.py`, `scripts/translation_qa.py`).
- **Aufgabe:** Dateisystem-Operationen, Vorbereitung der Chunks, Translation-Memory-Persistierung und manuelle QA.

### Node 2: Dedicated LLM Engine (`nyx.local`)
- **Hardware:** MacBook Air M4, 32 GB Unified Memory.
- **Rolle:** Lokaler Inferenz-Daemon via `mlx_lm.server` (Port 8000).
- **Modell:** `Qwen3.6-35B-A3B-4bit-DWQ` (dedizierte 24 GB VRAM-Allokation).
- **Leistung:** Erreicht bei Chunk-Größen unter 1.500 Zeichen konstante ~20–22 Tokens/s ohne thermisches Drosseln.

### Node 3: Linux Server & Runner (`nataraja.local`)
- **Hardware:** Apple Intel Mac (Quad-Core i7, 32 GB RAM) unter Pop!_OS Linux.
- **Rolle:** CI/CD-Backbone, Docker-Staging-Host und Self-Hosted GitHub Runner.
- **Aufgaben:**
  - VitePress Full-Build (38 Sprachen parallel unter 32 GB Swap).
  - Staging-Server auf Port 8080 (Public) und Port 8081 (Author/Review).
  - Lokale Embeddings via Ollama (`nomic-embed-text`).
  - Nächtliche TM-Backups und Snapshot-Vaults.

---

## 4. Software-Architektur & Datenfluss

```text
[Master-Markdown (docs/lektionen/*.md)]
             │
             ▼
[scripts/translation_qa.py] ── (Status-Prüfung & Queue-Bildung)
             │
             ▼
[scripts/lan_translate.py] ── (Chunking < 1500 Zeichen, YAML-Frontmatter)
             │
             ├──► [TM-Cache: .payer/tm/<lang>.json] (MD5-Hash-Hit? ──► Fertig)
             │
             ▼ (Cache-Miss)
[HTTP Inferenz Request] ──► http://nyx.local:8000/v1/chat/completions
             │
             ▼
[Sanitization & Devanāgarī-Filter] (scripts/file_processor.py)
             │
             ├──► [TM-Speicherung]
             ▼
[Zieldokument: docs/<lang>/lektionen/*.md]
```

---

## 5. Qualitäts-Gates & Verifikationsregeln

1. **Gate A: Syntax- und Tag-Integrität:**
   Jeder übersetzte Chunk muss Devanāgarī-Tags (`⟪...⟫`) und Signalrot-Syntax (`:sig[...]`) 1:1 unverändert beibehalten.
2. **Gate B: Residuen-Filter:**
   Automatische Erkennung unübersetzter deutscher Rest-Fragmente (`scan_german_residues`). Dateien mit Rückständen werden sofort abgelehnt.
3. **Gate C: Single Source of Truth (`translation_qa.py`):**
   Nur die offizielle QA-Queue bestimmt den Status. Eigene heuristische Prüfungen sind in Skripten untersagt.

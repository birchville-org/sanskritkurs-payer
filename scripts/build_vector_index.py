#!/usr/bin/env python3
"""
Build vector embeddings for Payer Sanskritkurs lessons using local Ollama nomic-embed-text.
Stores index in .payer/vector_index.json for fast semantic search.
"""
import os
import sys
import json
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
INDEX_FILE = ROOT / ".payer" / "vector_index.json"
PUBLIC_INDEX_FILE = DOCS / "public" / "vector_index.json"
def get_working_ollama_url():
    hosts = ["http://nataraja.local:11434", os.environ.get("OLLAMA_HOST"), "http://localhost:11434"]
    for host in hosts:
        if not host: continue
        try:
            url = f"{host.rstrip('/')}/api/version"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=1) as resp:
                if resp.status == 200:
                    return host.rstrip('/')
        except Exception:
            pass
    return "http://nataraja.local:11434"

OLLAMA_URL = get_working_ollama_url()

def l2_normalize(vec):
    if not vec:
        return vec
    norm = sum(x * x for x in vec) ** 0.5
    if norm == 0:
        return vec
    return [x / norm for x in vec]

def get_embedding(text, model="nomic-embed-text"):
    """Get L2-normalized vector embedding from Ollama instance."""
    url = f"{OLLAMA_URL.rstrip('/')}/api/embeddings"
    payload = json.dumps({"model": model, "prompt": text}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            raw_vec = data.get("embedding")
            return l2_normalize(raw_vec) if raw_vec else None
    except Exception as e:
        return None

def build_index(lang="de"):
    print(f"🧠 Building vector embedding index for [{lang}] via {OLLAMA_URL}...")
    
    if lang == "de" or lang == "root":
        target_dir = DOCS / "lektionen"
        out_name = "vector_index.json"
    else:
        target_dir = DOCS / lang / "lektionen"
        out_name = f"vector_index_{lang}.json"

    idx_file = ROOT / ".payer" / out_name
    pub_file = DOCS / "public" / out_name

    if not idx_file.parent.exists():
        idx_file.parent.mkdir(parents=True, exist_ok=True)
    if not pub_file.parent.exists():
        pub_file.parent.mkdir(parents=True, exist_ok=True)

    if not target_dir.exists():
        print(f"[{lang}] Directory not found: {target_dir}")
        return

    master_files = sorted(list(target_dir.glob("lektion*.md")))
    records = []
    success_count = 0

    for fidx, fpath in enumerate(master_files, 1):
        content = fpath.read_text(encoding="utf-8", errors="ignore")
        sections = content.split("\n## ")
        for idx, sec in enumerate(sections):
            text_snippet = sec[:1000].strip()
            if not text_snippet:
                continue
            heading = text_snippet.split("\n")[0].strip("# ").strip() if idx > 0 else fpath.stem
            vec = get_embedding(text_snippet)
            if vec:
                records.append({
                    "file": fpath.name,
                    "section": idx,
                    "heading": heading,
                    "snippet": text_snippet[:200].replace("\n", " "),
                    "embedding": vec
                })
                success_count += 1
        
        print(f"[{lang}] [{fidx}/{len(master_files)}] Embedded {fpath.name} ({success_count} total sections)", flush=True)

        payload_json = json.dumps({
            "lang": lang,
            "total_sections": len(records),
            "embedded_sections": success_count,
            "records": records
        }, indent=2, ensure_ascii=False)

        idx_file.write_text(payload_json, encoding="utf-8")
        pub_file.write_text(payload_json, encoding="utf-8")

    print(f"✅ Vector index for [{lang}] complete: {success_count} sections embedded in {pub_file.name}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Build vector embeddings index for Sanskritkurs lessons")
    parser.add_argument("--lang", default="de", help="Language code (e.g. de, ru, en)")
    args = parser.parse_args()
    build_index(args.lang)

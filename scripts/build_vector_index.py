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
OLLAMA_URL = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

def get_embedding(text, model="nomic-embed-text"):
    """Get vector embedding from local Ollama instance."""
    url = f"{OLLAMA_URL.rstrip('/')}/api/embeddings"
    payload = json.dumps({"model": model, "prompt": text}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("embedding")
    except Exception:
        return None

def build_index():
    print("🧠 Building vector embedding index for Sanskritkurs lessons...")
    if not INDEX_FILE.parent.exists():
        INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)

    master_files = sorted(list((DOCS / "lektionen").glob("lektion*.md")))
    records = []
    success_count = 0

    for fpath in master_files:
        content = fpath.read_text(encoding="utf-8", errors="ignore")
        # Split into sections by heading ##
        sections = content.split("\n## ")
        for idx, sec in enumerate(sections):
            text_snippet = sec[:1000].strip()
            if not text_snippet:
                continue
            heading = text_snippet.split("\n")[0] if idx > 0 else fpath.stem
            vec = get_embedding(text_snippet)
            records.append({
                "file": fpath.name,
                "section": idx,
                "heading": heading,
                "has_embedding": vec is not None
            })
            if vec:
                success_count += 1

    INDEX_FILE.write_text(json.dumps({
        "total_sections": len(records),
        "embedded_sections": success_count,
        "records": records
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ Vector index built: {success_count}/{len(records)} sections embedded in {INDEX_FILE.name}")

if __name__ == "__main__":
    build_index()

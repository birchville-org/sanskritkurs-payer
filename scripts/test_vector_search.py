#!/usr/bin/env python3
"""
Test Semantic Vector Search against .payer/vector_index.json using nomic-embed-text.
"""
import os
import sys
import json
import urllib.request
from pathlib import Path

ROOT = Path(__file__).parent.parent
INDEX_FILE = ROOT / ".payer" / "vector_index.json"
OLLAMA_URL = "http://nataraja.local:11434"

def l2_normalize(vec):
    norm = sum(x * x for x in vec) ** 0.5
    return [x / norm for x in vec] if norm > 0 else vec

def get_embedding(query):
    url = f"{OLLAMA_URL.rstrip('/')}/api/embeddings"
    payload = json.dumps({"model": "nomic-embed-text", "prompt": query}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return l2_normalize(data.get("embedding"))
    except Exception as e:
        print(f"Error fetching query embedding: {e}")
        return None

def dot_product(vecA, vecB):
    return sum(a * b for a, b in zip(vecA, vecB))

def search(query, lang="de", top_k=5):
    if lang == "de" or lang == "root":
        idx_file = ROOT / "docs" / "public" / "vector_index.json"
    else:
        idx_file = ROOT / "docs" / "public" / f"vector_index_{lang}.json"

    if not idx_file.exists():
        idx_file = ROOT / ".payer" / f"vector_index_{lang}.json" if lang != "de" else ROOT / ".payer" / "vector_index.json"

    if not idx_file.exists():
        print(f"❌ Vector index file not found at {idx_file}. Build it first with: python3 scripts/build_vector_index.py --lang {lang}")
        return

    data = json.loads(idx_file.read_text(encoding="utf-8"))
    records = data.get("records", [])
    print(f"\n🔍 Query: '{query}' [{lang}]")
    print(f"📊 Searching across {len(records)} embedded sections...\n")

    q_vec = get_embedding(query)
    if not q_vec:
        print("❌ Failed to generate embedding for query.")
        return

    results = []
    for rec in records:
        emb = rec.get("embedding")
        if emb:
            score = dot_product(q_vec, emb)
            results.append((score, rec))

    results.sort(key=lambda x: x[0], reverse=True)

    print(f"🏆 Top-{top_k} Semantic Search Results:")
    print("─" * 70)
    for idx, (score, rec) in enumerate(results[:top_k], 1):
        percentage = round(score * 100, 1)
        print(f"{idx}. [{percentage}% Match] File: {rec['file']} (Section {rec['section']})")
        print(f"   Heading: {rec['heading']}")
        print(f"   Snippet: {rec['snippet'][:120]}...\n")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Test Semantic Vector Search")
    parser.add_argument("query", nargs="?", default="Vergangenheit im Sanskrit", help="Search query")
    parser.add_argument("--lang", default="de", help="Language code (e.g. de, ru, en)")
    parser.add_argument("--top-k", type=int, default=5, help="Number of results")
    args = parser.parse_args()

    search(args.query, lang=args.lang, top_k=args.top_k)

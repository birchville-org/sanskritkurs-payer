#!/usr/bin/env python3
"""
scripts/test_rag_search.py — RAG Semantic Search Test via Nataraja (nomic-embed-text + qwen2.5:7b)

Demonstriert das zweistufige RAG-Prinzip (Retrieval-Augmented Generation):
1. Vektorsuche: Findet die relevantesten Lektionsabschnitte via nomic-embed-text
2. KI-Erklärung: Generiert eine präzise Antwort via qwen2.5:7b auf nataraja.local

Usage:
  python3 scripts/test_rag_search.py "Wie drücke ich 'müssen' im Sanskrit aus?"
  python3 scripts/test_rag_search.py --lang ru "Как образуется страдательный залог?"
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from pathlib import Path

ROOT = Path(__file__).parent.parent

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

NATARAJA_URL = get_working_ollama_url()

def l2_normalize(vec):
    if not vec: return vec
    norm = sum(x * x for x in vec) ** 0.5
    return [x / norm for x in vec] if norm > 0 else vec

def get_embedding(text, model="nomic-embed-text"):
    """Berechnet Vektor-Embedding über Ollama auf nataraja.local."""
    url = f"{NATARAJA_URL}/api/embeddings"
    payload = json.dumps({"model": model, "prompt": text}).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return l2_normalize(data.get("embedding"))
    except Exception as e:
        print(f"❌ Fehler bei Vektor-Embedding ({NATARAJA_URL}): {e}")
        return None

def generate_answer(prompt, model="qwen2.5:7b"):
    """Generiert Antwort über qwen2.5:7b auf nataraja.local."""
    url = f"{NATARAJA_URL}/api/generate"
    payload = json.dumps({
        "model": model,
        "prompt": prompt,
        "stream": False,
        "options": {"temperature": 0.3, "num_predict": 120}
    }).encode("utf-8")
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            return data.get("response", "").strip()
    except Exception as e:
        print(f"⚠️ Versuch mit {model} fehlgeschlagen ({e}). Versuche qwen2.5-coder:3b...")
        if model != "qwen2.5-coder:3b":
            return generate_answer(prompt, model="qwen2.5-coder:3b")
        return None

def dot_product(vecA, vecB):
    return sum(a * b for a, b in zip(vecA, vecB))

def run_rag_search(query, lang="de", top_k=3):
    print("=" * 70)
    print(f"🤖 RAG SEMANTIC SEARCH TEST (nataraja.local)")
    print(f"🌐 Sprache: [{lang}] | Frage: '{query}'")
    print("=" * 70)

    # 1. Index-Datei ermitteln
    if lang in ("de", "root"):
        idx_file = ROOT / "docs" / "public" / "vector_index.json"
    else:
        idx_file = ROOT / "docs" / "public" / f"vector_index_{lang}.json"

    if not idx_file.exists():
        # Fallback auf .payer/
        idx_file = ROOT / ".payer" / f"vector_index_{lang}.json" if lang != "de" else ROOT / ".payer" / "vector_index.json"

    if not idx_file.exists():
        print(f"❌ Vektorindex-Datei für [{lang}] nicht gefunden: {idx_file}")
        print(f"   Generiere den Index mit: python3 scripts/build_vector_index.py --lang {lang}")
        return

    data = json.loads(idx_file.read_text(encoding="utf-8"))
    records = data.get("records", [])

    # 2. Vektorsuche (Retrieval)
    print(f"\n1️⃣  SUCHE (nomic-embed-text): Berechne Vektor-Ähnlichkeit über {len(records)} Abschnitte...")
    q_vec = get_embedding(query)
    if not q_vec:
        return

    scored = []
    for r in records:
        emb = r.get("embedding")
        if emb:
            score = dot_product(q_vec, emb)
            scored.append((score, r))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_matches = scored[:top_k]

    print("\n🏆 Top Relevante Lektionsabschnitte:")
    context_blocks = []
    for idx, (score, rec) in enumerate(top_matches, 1):
        percentage = round(score * 100, 1)
        print(f"   {idx}. [{percentage}% Match] {rec['file']} ➔ {rec['heading']}")
        print(f"      Snippet: {rec['snippet'][:110]}...")
        context_blocks.append(f"--- Lektion: {rec['file']} ({rec['heading']}) ---\n{rec['snippet']}")

    # 3. LLM Generierung (Augmented Generation)
    print(f"\n2️⃣  ERKLÄRUNG (qwen2.5:7b): Formuliere Antwort auf nataraja.local...")
    context_str = "\n\n".join(context_blocks)
    prompt = f"""Du bist ein kompetenter Indologie-Tutor für den Sanskritkurs.
Beantworte die Frage des Nutzers präzise, sachlich und verständlich basierend auf den folgenden Kurs-Lektionen.

RELEVANTE LEKTIONS-ABSCHNITTE:
{context_str}

FRAGE DES NUTZERS:
{query}

ANTWORT:"""

    answer = generate_answer(prompt)
    
    print("\n" + "─" * 70)
    print("💬 GENERIERTE ANTWORT (qwen2.5:7b):")
    print("─" * 70)
    if answer:
        print(answer)
    else:
        print("Fehler beim Abrufen der Antwort von qwen2.5:7b.")
    print("─" * 70 + "\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test RAG Semantic Search via nataraja.local (nomic-embed-text + qwen2.5:7b)")
    parser.add_argument("query", nargs="?", default="Wie drücke ich müssen im Sanskrit aus?", help="Suchanfrage / Frage")
    parser.add_argument("--lang", default="de", help="Sprach-Code (de, ru, en...)")
    parser.add_argument("--top-k", type=int, default=3, help="Anzahl einzubeziehender Lektionen")

    args = parser.parse_args()
    run_rag_search(args.query, lang=args.lang, top_k=args.top_k)

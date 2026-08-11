#!/usr/bin/env python3
"""
Automated Translation Quality Scoring & Coherence Benchmark.
Scores Devanāgarī conservation ratio, container preservation, and generates .payer/quality_scores.json.
"""
import os
import sys
import re
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
SCORES_FILE = ROOT / ".payer" / "quality_scores.json"

DEVA_RE = re.compile(r'[\u0900-\u097F]+')
CONTAINER_RE = re.compile(r':::\s*[a-zA-Z0-9_-]+')

def score_languages():
    print("📊 Running Translation Quality Scoring Benchmark...")
    if not SCORES_FILE.parent.exists():
        SCORES_FILE.parent.mkdir(parents=True, exist_ok=True)

    de_lessons = sorted(list((DOCS / "lektionen").glob("lektion*.md")))
    deva_master_count = 0
    for f in de_lessons:
        content = f.read_text(encoding="utf-8", errors="ignore")
        deva_master_count += len(DEVA_RE.findall(content))

    lang_dirs = [d for d in DOCS.iterdir() if d.is_dir() and d.name not in ("lektionen", "public", ".vitepress")]
    results = {}

    for ldir in sorted(lang_dirs, key=lambda d: d.name):
        code = ldir.name
        t_lessons = list((ldir / "lektionen").glob("lektion*.md"))
        if not t_lessons:
            continue

        deva_found = 0
        container_count = 0
        file_count = len(t_lessons)

        for tf in t_lessons:
            txt = tf.read_text(encoding="utf-8", errors="ignore")
            deva_found += len(DEVA_RE.findall(txt))
            container_count += len(CONTAINER_RE.findall(txt))

        # Devanāgarī preservation ratio compared to DE master
        deva_ratio = round(min((deva_found / max(deva_master_count, 1)) * 100.0, 100.0), 1)
        score = round((deva_ratio * 0.7) + (min(file_count / 61.0, 1.0) * 30.0), 1)

        results[code] = {
            "files": file_count,
            "devanagari_count": deva_found,
            "devanagari_preservation_pct": deva_ratio,
            "container_structures": container_count,
            "quality_score": score
        }

    SCORES_FILE.write_text(json.dumps({
        "master_devanagari_count": deva_master_count,
        "evaluated_locales": len(results),
        "scores": results
    }, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"✅ Evaluated {len(results)} target locales. Report saved to {SCORES_FILE.name}")
    for code, data in list(results.items())[:5]:
        print(f"  - [{code.upper()}]: Score {data['quality_score']}/100 | Devanāgarī Preserved: {data['devanagari_preservation_pct']}% | Files: {data['files']}/61")

if __name__ == "__main__":
    score_languages()

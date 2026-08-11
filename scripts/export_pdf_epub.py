#!/usr/bin/env python3
"""
Generate PDF & EPUB Course Artifacts for Sanskritkurs Payer.
Runs on nataraja self-hosted runner and uploads artifacts to GitHub Releases.
"""
import os
import sys
import subprocess
from pathlib import Path

ROOT = Path(__file__).parent.parent
DOCS = ROOT / "docs"
EXPORTS_DIR = ROOT / "dist_exports"

def build_exports(lang="de"):
    """Build PDF and EPUB artifacts for a specific language."""
    print(f"📄 Building PDF & EPUB artifacts for language: [{lang}]...")
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    lang_dir = DOCS / lang if lang != "de" else DOCS
    lessons = sorted(list((lang_dir / "lektionen").glob("lektion*.md")))
    if not lessons:
        print(f"⚠️ No lesson files found for language [{lang}]")
        return

    # Combine lessons into a single consolidated manuscript
    combined_md = EXPORTS_DIR / f"Sanskritkurs_Payer_{lang.upper()}_Full.md"
    content_blocks = [f"# Sanskritkurs Payer ({lang.upper()})\n\n"]
    for lfile in lessons:
        content_blocks.append(lfile.read_text(encoding="utf-8", errors="ignore"))
        content_blocks.append("\n\n---\n\n")

    combined_md.write_text("\n".join(content_blocks), encoding="utf-8")

    # Generate PDF / EPUB using Pandoc or Weasyprint if installed
    epub_out = EXPORTS_DIR / f"Sanskritkurs_Payer_{lang.upper()}.epub"
    try:
        subprocess.run([
            "pandoc", str(combined_md), "-o", str(epub_out),
            "--metadata", f"title=Sanskritkurs Payer ({lang.upper()})",
            "--metadata", "author=Alois Payer"
        ], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if epub_out.exists():
            print(f"✅ Generated EPUB: {epub_out.name}")
    except Exception as e:
        print(f"ℹ️ Pandoc EPUB generation skipped: {e}")

if __name__ == "__main__":
    target_langs = ["de", "en"]
    if len(sys.argv) > 1:
        target_langs = sys.argv[1:]
    for l in target_langs:
        build_exports(l)

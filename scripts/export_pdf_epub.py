#!/usr/bin/env python3
"""
Generate PDF & EPUB Course Artifacts for Sanskritkurs Payer.
Includes official Impressum & Copyright Notice page right after title page.
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
    """Build PDF and EPUB artifacts for a specific language with title and impressum page."""
    print(f"📄 Building PDF & EPUB artifacts for language: [{lang}]...")
    EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

    lang_dir = DOCS / lang if lang != "de" else DOCS
    lessons = sorted(list((lang_dir / "lektionen").glob("lektion*.md")))
    if not lessons:
        print(f"⚠️ No lesson files found for language [{lang}]")
        return

    # Title & Impressum / Copyright Page Block
    impressum_block = (
        f"# Sanskritkurs Payer ({lang.upper()})\n"
        f"## Ein vollständiger Lehrgang von Alois Payer\n\n"
        f"---\n\n"
        f"### Impressum & Copyright / Notice\n\n"
        f"- **Autor:** Alois Payer (Tüpfli's Global Village Library)\n"
        f"- **Herausgeber & Digitalisierung:** Sanskritkurs Payer Project\n"
        f"- **Webmaster & Kontakt:** webmaster@birchville.cc\n"
        f"- **Lektorat & Mitarbeit:** onboarding@birchville.cc\n"
        f"- **Open-Source Standalone Editor:** https://github.com/marcodem/zentauri\n"
        f"- **Lizenz & Quellen:** Siehe Vollständiges Lizenzverzeichnis (`licenses.md`)\n"
        f"- **Dokument-Typ:** Offizielles E-Book & PDF-Artefakt (Sanskritkurs Payer Project)\n\n"
        f"---\n\n"
    )

    content_blocks = [impressum_block]
    for lfile in lessons:
        content_blocks.append(lfile.read_text(encoding="utf-8", errors="ignore"))
        content_blocks.append("\n\n---\n\n")

    combined_md = EXPORTS_DIR / f"Sanskritkurs_Payer_{lang.upper()}_Full.md"
    combined_md.write_text("\n".join(content_blocks), encoding="utf-8")

    # Generate EPUB / PDF using Pandoc if installed
    epub_out = EXPORTS_DIR / f"Sanskritkurs_Payer_{lang.upper()}.epub"
    try:
        subprocess.run([
            "pandoc", str(combined_md), "-o", str(epub_out),
            "--metadata", f"title=Sanskritkurs Payer ({lang.upper()})",
            "--metadata", "author=Alois Payer",
            "--metadata", "rights=Copyright Alois Payer / Sanskritkurs Payer Project",
            "--metadata", "publisher=Sanskritkurs Payer Project"
        ], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if epub_out.exists():
            print(f"✅ Generated EPUB with Impressum & Copyright page: {epub_out.name}")
    except Exception as e:
        print(f"ℹ️ Pandoc EPUB generation skipped: {e}")

if __name__ == "__main__":
    target_langs = ["de", "en"]
    if len(sys.argv) > 1:
        target_langs = sys.argv[1:]
    for l in target_langs:
        build_exports(l)

#!/usr/bin/env python3
"""
add_image_descriptions.py

Inserts descriptive text back into media blocks in lektion markdown files.

For each file that contains a deleteme-box, the script:
  1. Parses every **lektXXXX:** entry to extract the explanatory preamble
     (text that appears before the source-attribution bracket).
  2. Walks every media block and, where the license-link line follows the
     caption line immediately (= no extra text yet), inserts the preamble.

Safe to run multiple times: blocks that already carry extra text are skipped.

Usage:
  python3 scripts/add_image_descriptions.py           # apply changes
  python3 scripts/add_image_descriptions.py --dry-run # preview only
"""

import re
import sys
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"

# Language subdirectories; empty string = root (German)
LANG_SUBDIRS = ["", "bg", "en", "es", "fr", "hi", "it", "ru", "uk"]

# Caption prefixes used in media blocks across all languages
CAPTION_PREFIXES = [
    "Abb.:",
    "Fig. :",
    "Fig.:",
    "Рис.:",
    "Ик.:",
    "Ил.:",
    "अभ.:",
]

# Matches the opening of a source-attribution bracket in deleteme entries.
# All languages start their attribution with one of these phrases.
SOURCE_RE = re.compile(
    r"\[(?:"
    r"Bildquelle"
    r"|Image source"
    r"|Fuente de la imagen"
    r"|Source de l"          # covers "Source de l'image"
    r"|छवि स्रोत"
    r"|चित्र स्रोत"
    r"|Fonte dell"           # covers "Fonte dell'immagine"
    r"|Источник изображени"
    r"|Джерело зображ"
    r"|Източник на изображ"
    r"|Public domain"
    r"|GNU FDL"
    r"|Gemeinfrei"
    r")",
    re.IGNORECASE,
)

# Image reference inside a media block
IMG_RE = re.compile(r"!\[\]\(/images/(lekt\w+)\.(?:jpg|png|gif|webp)\)")

# Caption line: starts with one of the known caption prefixes
CAP_RE = re.compile(r"^(?:Abb\.|Fig\.\s|Fig\.|Рис\.|Ик\.|Ил\.|अभ\.)")

# License-link line: always contains /licenses# or /licenses/lekt
LIC_RE = re.compile(r"/licenses(?:#|/lekt)")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def strip_caption_prefix(text: str) -> str:
    """Remove a leading caption prefix (Abb.:, Fig.:, …) from text."""
    for prefix in CAPTION_PREFIXES:
        if text.startswith(prefix):
            return text[len(prefix):].strip()
    return text


def normalize(text: str) -> str:
    """Strip ⟪⟫ translation markers and surrounding whitespace for comparison."""
    return re.sub(r"[⟪⟫]", "", text).strip()


# ---------------------------------------------------------------------------
# Deleteme parsing
# ---------------------------------------------------------------------------

def parse_deleteme(content: str) -> dict:
    """
    Return {image_id: extra_text} extracted from the deleteme-box.

    extra_text is the preamble of the entry after stripping:
      - the source-attribution bracket and everything after it
      - any leading caption prefix (Abb.:, Fig.:, …)
    """
    entries: dict[str, str] = {}
    in_box = False

    for line in content.splitlines():
        stripped = line.strip()

        # Detect box open/close (3 or 4 colons)
        if re.match(r":{3,} deleteme-box", stripped):
            in_box = True
            continue
        if in_box and re.match(r":{3,}\s*$", stripped):
            in_box = False
            continue
        if not in_box:
            continue

        m = re.match(r"^\*\*(lekt\w+):\*\*\s*(.*)", line)
        if not m:
            continue

        image_id = m.group(1)
        raw = m.group(2).strip()

        # Cut off source attribution
        src = SOURCE_RE.search(raw)
        preamble = raw[: src.start()].strip() if src else raw.strip()

        # Strip caption prefix (Abb.:, Fig.:, …)
        preamble = strip_caption_prefix(preamble)

        # Strip trivial trailing punctuation left by the split
        preamble = preamble.rstrip(" ,")

        entries[image_id] = preamble

    return entries


# ---------------------------------------------------------------------------
# File processing
# ---------------------------------------------------------------------------

def process_file(path: Path, dry_run: bool = False) -> int:
    """
    Insert extra descriptions into media blocks where missing.
    Returns the number of insertions made (0 = file unchanged).
    """
    text = path.read_text(encoding="utf-8")

    if "deleteme-box" not in text:
        return 0

    entries = parse_deleteme(text)
    if not entries:
        return 0

    # Work line-by-line, preserving original line endings
    lines = text.splitlines(keepends=True)
    result: list[str] = []
    changes = 0
    i = 0

    while i < len(lines):
        line = lines[i]
        raw = line.rstrip("\r\n")

        img_m = IMG_RE.search(raw)
        if img_m and i + 2 < len(lines):
            image_id = img_m.group(1)
            cap_raw = lines[i + 1].rstrip("\r\n")
            lic_raw = lines[i + 2].rstrip("\r\n")

            # Only act when: caption line is next AND license link is the line after that
            if CAP_RE.match(cap_raw.strip()) and LIC_RE.search(lic_raw):
                extra = entries.get(image_id, "").strip()

                if extra:
                    cap_text = normalize(strip_caption_prefix(cap_raw.strip()))
                    extra_text = normalize(extra)

                    # Insert only when preamble differs from the caption already shown
                    if extra_text != cap_text:
                        result.append(line)           # image line  (i)
                        result.append(lines[i + 1])   # caption     (i+1)
                        result.append(extra + "\n")   # NEW preamble
                        result.append(lines[i + 2])   # license     (i+2)
                        i += 3
                        changes += 1
                        continue

        result.append(line)
        i += 1

    if changes and not dry_run:
        path.write_text("".join(result), encoding="utf-8")

    return changes


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main() -> None:
    dry_run = "--dry-run" in sys.argv

    if dry_run:
        print("DRY RUN — no files will be written\n")

    total_files = 0
    total_changes = 0

    for sub in LANG_SUBDIRS:
        ldir = DOCS_DIR / sub / "lektionen" if sub else DOCS_DIR / "lektionen"
        if not ldir.is_dir():
            continue

        for md in sorted(ldir.glob("lektion*.md")):
            n = process_file(md, dry_run=dry_run)
            if n:
                rel = md.relative_to(DOCS_DIR)
                print(f"  {rel}: {n} insertion{'s' if n != 1 else ''}")
                total_files += 1
                total_changes += n

    print(f"\nTotal: {total_changes} insertions across {total_files} files")


if __name__ == "__main__":
    main()

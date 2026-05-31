#!/usr/bin/env python3
"""
sync_wortliste.py — Sync wortliste sections from individual lektion files
to the global docs/lektionen/wortliste.md.

Each lektion's "## N.X. Wortliste" section is extracted and used to replace
the corresponding "## Lektion N" block in the global file.

Usage:
  python3 scripts/sync_wortliste.py all      # sync all lektionen
  python3 scripts/sync_wortliste.py 52       # sync lektion 52 only
  python3 scripts/sync_wortliste.py 6 12 42  # sync specific lektionen
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).parent.parent
LEKTIONEN_DIR = ROOT / "docs" / "lektionen"
WORTLISTE_PATH = LEKTIONEN_DIR / "wortliste.md"


def find_lektion_file(n: int) -> Path | None:
    p = LEKTIONEN_DIR / f"lektion{n:02d}.md"
    return p if p.exists() else None


def extract_wortliste_content(path: Path) -> str | None:
    """Return the body of the wortliste section (heading line excluded),
    stripped of trailing whitespace. Returns None if no wortliste section."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r'^## \d+(?:\.\d+)*\. Wortliste[ \t]*\n', text, re.MULTILINE)
    if not m:
        return None
    start = m.end()
    next_m = re.search(r'^## ', text[start:], re.MULTILINE)
    end = start + next_m.start() if next_m else len(text)
    return text[start:end].rstrip()


def sync_wortliste(lektion_nums: list[int]) -> None:
    wortliste_text = WORTLISTE_PATH.read_text(encoding="utf-8")
    changed = 0

    for n in lektion_nums:
        path = find_lektion_file(n)
        if not path:
            print(f"  L{n:02d}: file not found, skipping")
            continue

        new_content = extract_wortliste_content(path)
        if new_content is None:
            print(f"  L{n:02d}: no wortliste section, skipping")
            continue

        # Locate "## Lektion N" section header in wortliste.md
        m = re.search(rf'^## Lektion {n}\s*\n', wortliste_text, re.MULTILINE)
        if not m:
            print(f"  L{n:02d}: '## Lektion {n}' not found in wortliste.md, skipping")
            continue

        body_start = m.end()

        # Section ends at next "## " heading OR a "::: deleteme-box" (footer guard)
        next_m = re.search(r'^(?:## |::: deleteme-box)', wortliste_text[body_start:], re.MULTILINE)
        body_end = body_start + next_m.start() if next_m else len(wortliste_text)

        old_body = wortliste_text[body_start:body_end]
        new_body = "\n" + new_content + "\n\n"

        if old_body == new_body:
            print(f"  L{n:02d}: up to date")
        else:
            wortliste_text = (
                wortliste_text[:body_start] + new_body + wortliste_text[body_end:]
            )
            print(f"  L{n:02d}: updated")
            changed += 1

    WORTLISTE_PATH.write_text(wortliste_text, encoding="utf-8")
    print(f"\nDone. {changed} section(s) updated.")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print("Usage: python3 scripts/sync_wortliste.py <all|lesson_num [...]>")
        print("Example: python3 scripts/sync_wortliste.py all")
        print("Example: python3 scripts/sync_wortliste.py 52")
        print("Example: python3 scripts/sync_wortliste.py 6 12 42")
        sys.exit(1)
    if args[0] == "all":
        nums = list(range(1, 62))
    else:
        nums = []
        for a in args:
            try:
                nums.append(int(a))
            except ValueError:
                print(f"Warning: ignoring non-numeric argument '{a}'")
    sync_wortliste(nums)


if __name__ == "__main__":
    main()

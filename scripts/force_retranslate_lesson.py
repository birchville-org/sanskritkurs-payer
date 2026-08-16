import sys
import os
from pathlib import Path

if len(sys.argv) < 3:
    print("Usage: python3 force_retranslate_lesson.py <lang> <lesson_num>")
    sys.exit(1)

lang = sys.argv[1]
lesson_num = int(sys.argv[2])
filename = f"lektion{lesson_num:02d}.md"

target_path = Path(f"/Volumes/SanDisk1TB/proj/Payer/docs/{lang}/lektionen/{filename}")

if target_path.exists():
    target_path.unlink()
    print(f"Removed {target_path} for fresh, clean translation into {lang}.")
else:
    print(f"{target_path} does not exist; ready for translation.")


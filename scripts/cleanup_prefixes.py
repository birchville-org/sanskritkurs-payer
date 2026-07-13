import os
import re
from pathlib import Path

ROOT = Path("/Volumes/SanDisk1TB/proj/Payer/docs")
pattern = re.compile(r'^\[[LЛlл]?\d+\](?:>>)?\s*')

fixed_count = 0
file_count = 0

for lang_dir in ROOT.iterdir():
    if not lang_dir.is_dir() or lang_dir.name.startswith('.'):
        continue
        
    lektionen_dir = lang_dir / "lektionen"
    if not lektionen_dir.exists():
        continue
        
    for md_file in lektionen_dir.glob("*.md"):
        content = md_file.read_text(encoding='utf-8')
        
        # Check if file has any broken prefixes
        if pattern.search(content):
            lines = content.split('\n')
            new_lines = []
            file_changed = False
            
            for line in lines:
                new_line = pattern.sub('', line)
                if new_line != line:
                    file_changed = True
                new_lines.append(new_line)
                
            if file_changed:
                md_file.write_text('\n'.join(new_lines), encoding='utf-8')
                fixed_count += 1
                
    # Also check qa files if they exist
    qa_dir = lang_dir / "qa"
    if qa_dir.exists():
        for md_file in qa_dir.glob("*.md"):
            content = md_file.read_text(encoding='utf-8')
            if pattern.search(content):
                lines = content.split('\n')
                new_lines = [pattern.sub('', line) for line in lines]
                md_file.write_text('\n'.join(new_lines), encoding='utf-8')
                fixed_count += 1

print(f"Cleanup complete! Fixed {fixed_count} files.")

import sys
import os
import re

if len(sys.argv) < 3:
    print("Usage: python3 force_retranslate_lesson.py <lang> <lesson_num>")
    sys.exit(1)

lang = sys.argv[1]
lesson_num = int(sys.argv[2])
filename = f"lektion{lesson_num:02d}.md"

de_path = f"/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/{filename}"
target_path = f"/Volumes/SanDisk1TB/proj/Payer/docs/{lang}/lektionen/{filename}"

if not os.path.exists(de_path):
    print(f"Error: {de_path} not found.")
    sys.exit(1)

with open(de_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

in_frontmatter = False
new_lines = []
for line in lines:
    stripped = line.strip()
    if stripped == '---':
        in_frontmatter = not in_frontmatter
        new_lines.append(line)
        continue
        
    if in_frontmatter:
        new_lines.append(line)
    elif stripped and not stripped.startswith(':::') and not stripped.startswith('---'):
        new_lines.append(line.rstrip() + " <!-- TODO: Fallback translation -->\n")
    else:
        new_lines.append(line)

os.makedirs(os.path.dirname(target_path), exist_ok=True)
with open(target_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Prepared {target_path} for 100% fresh translation into {lang}.")

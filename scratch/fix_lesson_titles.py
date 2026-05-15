import os
import re

directory = '/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/'

# Regex to match "X. Lektion X" or "X. Lektion XX"
# Case 1: title: X. Lektion X
# Case 2: # X. Lektion X
pattern_title = re.compile(r'^title: (\d+)\. Lektion \1', re.MULTILINE)
pattern_h1 = re.compile(r'^# (\d+)\. Lektion \1', re.MULTILINE)

files_fixed = []

for filename in os.listdir(directory):
    if filename.endswith('.md'):
        filepath = os.path.join(directory, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        
        # Replace frontmatter title
        new_content = pattern_title.sub(r'title: Lektion \1', new_content)
        
        # Replace H1 heading
        new_content = pattern_h1.sub(r'# Lektion \1', new_content)
        
        if new_content != content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_content)
            files_fixed.append(filename)

print(f"Fixed titles in {len(files_fixed)} files:")
for f in sorted(files_fixed):
    print(f" - {f}")

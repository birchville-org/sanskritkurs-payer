import os
import re

def clean_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    skip_until_next_delimiter = False
    
    # 1. First pass: Handle YAML and basic normalization
    content = "".join(lines)
    
    # Normalize YAML Title
    content = re.sub(r'^title:\s*["\']Lektion\s*(\d+)["\']', r'title: Lektion \1', content, flags=re.MULTILINE)
    content = re.sub(r'^title:\s*Lektion\s*(\d+)', r'title: Lektion \1', content, flags=re.MULTILINE)
    
    # Normalize H1
    match = re.search(r'lektion(\d+)\.md', filepath)
    if match:
        num = str(int(match.group(1)))
        content = re.sub(r'^#\s*.*Lektion.*', f'# Lektion {num}', content, flags=re.MULTILINE)

    # Decouple 'Quellen' from TOC
    content = re.sub(r'^###\s*Quellen', r'**Quellen**', content, flags=re.MULTILINE)

    # Purge HTML anchors and scripts
    content = re.sub(r'<script.*?</script>', '', content, flags=re.DOTALL | re.IGNORECASE)
    content = re.sub(r'&lt;a id=".*?"&gt;&lt;/a&gt;', '', content)
    content = re.sub(r'<a id=".*?"\s*></a>', '', content)
    content = re.sub(r'<a id=".*?"\s*/>', '', content)

    # 2. Second pass: Line-by-line block removal to prevent over-deletion
    lines = content.splitlines(keepends=True)
    final_lines = []
    skip_depth = 0
    
    for line in lines:
        stripped = line.strip()
        
        # Start skipping if we find the specific Zitierweise box
        if stripped.startswith(':::') and ('Zitierweise' in line or 'Copyright' in line or 'Rights' in line):
            skip_depth = 1
            continue
            
        if skip_depth > 0:
            if stripped == ':::':
                skip_depth -= 1
                continue
            elif stripped.startswith('::: '): # Nested box start
                skip_depth += 1
                continue
            elif stripped.startswith('#'): # Safety: never skip headers
                skip_depth = 0
                final_lines.append(line)
                continue
            else:
                continue # Skip content
        
        # Remove Overview sections
        if stripped.startswith('## Übersicht'):
            skip_depth = 1 # We'll skip until the next delimiter or header
            continue

        final_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(final_lines)

import sys
if len(sys.argv) > 1:
    clean_file(sys.argv[1])
else:
    lessons_dir = 'docs/lektionen'
    for filename in os.listdir(lessons_dir):
        if filename.startswith('lektion') and filename.endswith('.md'):
            clean_file(os.path.join(lessons_dir, filename))

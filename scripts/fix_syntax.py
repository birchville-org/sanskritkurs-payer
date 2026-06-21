import os
import re

def fix_container_syntax(directory):
    for root, dirs, files in os.walk(directory):
        if ".vitepress" in root or "public" in root:
            continue
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace "::: container" with ":::container"
                # Replace ":::: container" with "::::container"
                new_content = re.sub(r'^(::+)\s+', r'\1', content, flags=re.MULTILINE)
                
                if new_content != content:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Fixed {filepath}")

fix_container_syntax('docs')

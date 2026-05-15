import os
import re
import sys

directory = sys.argv[1] if len(sys.argv) > 1 else 'docs/lektionen'
# Valid tags we want to keep
valid_tags = ['br', 'u', 'span', 'sup', 'img', 'a', 'hr', 'table', 'thead', 'tbody', 'tr', 'td', 'th', 'grammar-box', 'script', 'div']

def escape_malformed(content):
    # Split by anything that looks like a tag
    parts = re.split(r'(<[^>]+?>)', content)
    new_parts = []
    for part in parts:
        if part.startswith('<') and part.endswith('>'):
            # Check if it's a valid tag
            tag_content = part[1:-1].lower().strip()
            # Handle closing tags and self-closing tags
            tag_name = tag_content.split(' ')[0].replace('/', '')
            
            if tag_name in valid_tags:
                new_parts.append(part)
            else:
                # Escape it
                new_parts.append('&lt;' + part[1:-1] + '&gt;')
        else:
            # Check for stray < or > in the text
            part = part.replace('<', '&lt;').replace('>', '&gt;')
            new_parts.append(part)
    
    return ''.join(new_parts)

for root, dirs, files in os.walk(directory):
    for filename in files:
        if filename.endswith('.md'):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = escape_malformed(content)
            
            if new_content != content:
                print(f"Escaped malformed tags in {filepath}")
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)

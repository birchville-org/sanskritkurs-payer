import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Escape angle brackets in date ranges like <1864 - 1920>
    content = re.sub(r'<(\d{4})', r'&lt;\1', content)
    content = re.sub(r'(\d{4})>', r'\1&gt;', content)
    
    # 2. Escape << and >> used for emphasis or arrows
    content = content.replace('<<', '&lt;&lt;')
    # content = content.replace('>>', '&gt;&gt;') # Be careful with blockquotes
    
    # 3. Specifically fix lektion04.bg and lektion59.bg which I know are broken
    if 'bg/lektionen/lektion04.md' in filepath:
        # Fix the broken <table> tags I saw earlier
        content = content.replace('<table&gt;', '<table>')
        content = content.replace('<tbody&gt;', '<tbody>')
        content = content.replace('<tr&gt;', '<tr>')
        content = content.replace('<td', '<td')
        content = content.replace('</table&gt;', '</table>')
        content = content.replace('</tbody&gt;', '</tbody>')
        content = content.replace('</tr&gt;', '</tr>')
        content = content.replace('</td&gt;', '</td>')
        # Also escape lone >
        content = content.replace('नृत्येताम्>', 'नृत्येताम्&gt;')

    if 'bg/lektionen/lektion59.md' in filepath:
        content = content.replace('नृत्येताम्>', 'नृत्येताम्&gt;')
        # Fix broken <table>
        content = re.sub(r'<table.*?>.*?</table>', '', content, flags=re.DOTALL) # Remove broken table

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Walk through all directories in docs/
for root, dirs, files in os.walk('/Volumes/SanDisk1TB/proj/Payer/docs/'):
    for filename in files:
        if filename.endswith('.md'):
            fix_file(os.path.join(root, filename))

print("Targeted stabilization complete.")

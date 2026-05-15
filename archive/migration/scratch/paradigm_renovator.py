import os
import re

directory = '/Volumes/SanDisk1TB/proj/Payer/docs/lektionen'

def fix_content(content):
    # 1. Ersetze ** durch <strong> innerhalb von <table> Tags
    def table_bold_fix(match):
        table_content = match.group(0)
        # Ersetze **text** durch <strong>text</strong>
        fixed = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', table_content)
        # Sicherstellen, dass die Tabelle in einer grammar-box ist
        if '<div class="grammar-box">' not in content[max(0, match.start()-100):match.start()]:
            return f'<div class="grammar-box">\n\n{fixed}\n\n</div>'
        return fixed

    new_content = re.sub(r'<table>.*?</table>', table_bold_fix, content, flags=re.DOTALL)
    
    # 2. Repariere "zerstückelte" Boxen (Überreste von alten Skripten)
    # Muster: </div> --- <div class="grammar-box">
    new_content = re.sub(r'</div>\s*---\s*<div class="grammar-box">', '\n', new_content)
    new_content = re.sub(r'</div>\s*---\s*\|?\s*---\s*\|?\s*<div class="grammar-box">', '\n', new_content)
    
    # 3. Doppelte Boxen vermeiden
    new_content = re.sub(r'<div class="grammar-box">\s*<div class="grammar-box">', '<div class="grammar-box">', new_content)
    new_content = re.sub(r'</div>\s*</div>', '</div>', new_content)

    return new_content

for filename in os.listdir(directory):
    if filename.endswith('.md'):
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = fix_content(content)
        
        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Renoviert: {filename}")

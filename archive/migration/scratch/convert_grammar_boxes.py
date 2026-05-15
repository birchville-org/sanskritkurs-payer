import os
import re

directory = '/Volumes/SanDisk1TB/proj/Payer/docs/lektionen'

# Muster für eine "Ein-Spalten-Tabelle", die oft für Boxen missbraucht wurde
# Wir suchen nach: | Text | \n | --- | \n | Text |
table_pattern = re.compile(r'\|(.*?)\|\n\| *--- *\|\n\|(.*?)\|', re.DOTALL)

# Muster für einfache Ein-Zellen-Tabellen: | Text | \n | --- |
single_cell_pattern = re.compile(r'\|(.*?)\|\n\| *--- *\|(?!\n\|)', re.DOTALL)

for filename in os.listdir(directory):
    if filename.endswith('.md'):
        path = os.path.join(directory, filename)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content = content
        
        # 1. Konvertiere 2-teilige Boxen
        def replace_box(match):
            top = match.group(1).strip()
            bottom = match.group(2).strip()
            # Bereinige eventuelle Reste von Pipes am Zeilenende
            top = re.sub(r' *\|$', '', top, flags=re.MULTILINE)
            bottom = re.sub(r' *\|$', '', bottom, flags=re.MULTILINE)
            return f'<div class="grammar-box">\n\n{top}\n\n{bottom}\n\n</div>'

        new_content = table_pattern.sub(replace_box, new_content)
        
        # 2. Konvertiere einfache Boxen
        def replace_single(match):
            text = match.group(1).strip()
            text = re.sub(r' *\|$', '', text, flags=re.MULTILINE)
            return f'<div class="grammar-box">\n\n{text}\n\n</div>'
            
        new_content = single_cell_pattern.sub(replace_single, new_content)

        if new_content != content:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"Konvertiert: {filename}")

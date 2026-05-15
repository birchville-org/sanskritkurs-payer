import os
import re

def sync_licenses(de_path, target_path, target_lang):
    if not os.path.exists(de_path) or not os.path.exists(target_path):
        return

    with open(de_path, 'r', encoding='utf-8') as f:
        de_content = f.read()
    with open(target_path, 'r', encoding='utf-8') as f:
        target_content = f.read()

    # Map filename to its entire row (including anchor) from German
    row_map = {}
    for line in de_content.split('\n'):
        if 'lekt' in line and '|' in line:
            match = re.search(r'<span id="([^"]+)"></span> \[`([^`]+)`\]', line)
            if match:
                lekt_id = match.group(1)
                filename = match.group(2)
                row_map[filename] = (lekt_id, line)

    new_lines = []
    for line in target_content.split('\n'):
        if 'lekt' in line and '|' in line:
            # Extract filename from target
            name_match = re.search(r'[`\[](lekt\d+\.jpg)[`\]]', line)
            if name_match:
                filename = name_match.group(1)
                if filename in row_map:
                    lekt_id, de_row = row_map[filename]
                    # Get anchor and link from German row
                    # Example German row: | <span id="lekt0101"></span> [`lekt0101.jpg`](/lektionen/lektion01#_lektion-1) | ... |
                    # Extract the first column from DE
                    de_cols = de_row.split('|')
                    if len(de_cols) >= 2:
                        first_col = de_cols[1].strip()
                        # Localize the link in first_col if it's not root
                        if target_lang != 'de':
                            first_col = first_col.replace('(/lektionen/', f'(/{target_lang}/lektionen/')
                        
                        target_cols = line.split('|')
                        if len(target_cols) >= 2:
                            target_cols[1] = f" {first_col} "
                            line = '|'.join(target_cols)
            
        new_lines.append(line)

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(new_lines))

def main():
    docs_root = "/Volumes/SanDisk1TB/proj/Payer/docs"
    de_path = os.path.join(docs_root, "licenses.md")
    
    langs = ['en', 'it', 'es', 'bg', 'ru', 'uk']
    for lang in langs:
        target_path = os.path.join(docs_root, lang, "licenses.md")
        if os.path.exists(target_path):
            sync_licenses(de_path, target_path, lang)
            print(f"Synced anchors to {lang}")

if __name__ == "__main__":
    main()

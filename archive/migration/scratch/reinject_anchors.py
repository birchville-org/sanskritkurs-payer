import os
import re

def find_image_location(docs_root, filename):
    lekt_dir = os.path.join(docs_root, "lektionen")
    for lesson_file in os.listdir(lekt_dir):
        if lesson_file.endswith(".md"):
            with open(os.path.join(lekt_dir, lesson_file), 'r', encoding='utf-8') as f:
                content = f.read()
                if filename in content:
                    # Find nearest header above
                    lines = content.split('\n')
                    header = ""
                    for line in lines:
                        if filename in line:
                            break
                        if line.startswith('#'):
                            header = line.lstrip('#').strip()
                    
                    # Convert header to anchor link
                    anchor = header.lower().replace(' ', '-').replace('.', '').replace('(', '').replace(')', '').replace(':', '').replace('?', '')
                    return f"/lektionen/{lesson_file[:-3]}#_{anchor}"
    return None

def inject_anchors_de(filepath, docs_root):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if 'lekt' in line and '|' in line:
            match = re.search(r'`(lekt\d+\.jpg)`', line)
            if match:
                filename = match.group(1)
                lekt_id = os.path.splitext(filename)[0]
                link = find_image_location(docs_root, filename)
                if link:
                    new_line = line.replace(f"`{filename}`", f'<span id="{lekt_id}"></span> [`{filename}`]({link})')
                    new_lines.append(new_line)
                    continue
        new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def main():
    docs_root = "/Volumes/SanDisk1TB/proj/Payer/docs"
    filepath = os.path.join(docs_root, "licenses.md")
    inject_anchors_de(filepath, docs_root)
    print("Re-injected anchors into German licenses.md")

if __name__ == "__main__":
    main()

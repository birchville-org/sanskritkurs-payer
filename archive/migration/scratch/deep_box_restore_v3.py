import os
import re

# Pfade
html_dir = '/Volumes/SanDisk1TB/proj/Payer/sanskritkurs'
md_dir = '/Volumes/SanDisk1TB/proj/Payer/docs/lektionen'

def normalize(text):
    """Normalisiert Text für den Vergleich (entfernt HTML, Markdown-Marker, Sonderzeichen)"""
    text = re.sub(r'<[^>]+>', '', text) # HTML Tags
    text = re.sub(r'[\*\_\~\`]+', '', text) # Markdown Marker
    text = re.sub(r'[\s\-\|]+', '', text) # Whitespace und Pipes
    return text.lower()

def extract_yellow_boxes_re(html_path):
    try:
        with open(html_path, 'r', encoding='iso-8859-1') as f:
            content = f.read()
    except:
        return []
    
    table_pattern = re.compile(r'<table[^>]*bgcolor=["\']#(ffffcc|FFFFCC)["\'][^>]*>(.*?)</table>', re.DOTALL | re.IGNORECASE)
    
    boxes = []
    for match in table_pattern.finditer(content):
        inner_html = match.group(2)
        text = re.sub(r'<[^>]+>', ' ', inner_html)
        text = " ".join(text.split())
        if len(text) > 15: # Etwas kleinerer Schwellenwert
            boxes.append(text)
    return boxes

def process_lesson(num):
    html_file = f'lektion{num:02d}.htm'
    md_file = f'lektion{num:02d}.md'
    
    html_path = os.path.join(html_dir, html_file)
    md_path = os.path.join(md_dir, md_file)
    
    if not os.path.exists(html_path) or not os.path.exists(md_path):
        return

    yellow_boxes = extract_yellow_boxes_re(html_path)
    if not yellow_boxes:
        return

    with open(md_path, 'r', encoding='utf-8') as f:
        md_content = f.read()

    new_content = md_content
    found_count = 0

    # Suche in Fenstern von Absätzen
    paragraphs = re.split(r'\n\n+', new_content)
    
    for box_text in yellow_boxes:
        norm_box = normalize(box_text)
        
        box_matched = False
        for i in range(len(paragraphs)):
            for j in range(i, min(i + 15, len(paragraphs))):
                combined = " ".join(paragraphs[i:j+1])
                if norm_box in normalize(combined):
                    match_content = "\n\n".join(paragraphs[i:j+1])
                    if '<div class="grammar-box">' in match_content:
                        box_matched = True
                        break
                    
                    replacement = f'<div class="grammar-box">\n\n{match_content.strip()}\n\n</div>'
                    new_content = new_content.replace(match_content, replacement)
                    found_count += 1
                    box_matched = True
                    break
            if box_matched: break

    if found_count > 0:
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Lektion {num}: {found_count} zusätzliche Boxen restauriert.")

# Hauptschleife
for n in range(1, 62):
    process_lesson(n)

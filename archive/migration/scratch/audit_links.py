import os
import re

def slugify(text):
    # Remove dots
    text = text.replace('.', '')
    # Convert to lowercase
    text = text.lower()
    # Replace spaces with hyphens
    text = text.replace(' ', '-')
    # Remove redundant hyphens
    text = re.sub(r'-+', '-', text)
    return text

def find_image_header(lesson_path, image_name):
    if not os.path.exists(lesson_path):
        return None
    
    with open(lesson_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the image
    image_line_idx = -1
    for i, line in enumerate(lines):
        if image_name in line:
            image_line_idx = i
            break
    
    if image_line_idx == -1:
        return None
    
    # Search backwards for a header
    for i in range(image_line_idx, -1, -1):
        line = lines[i].strip()
        if line.startswith('## ') or line.startswith('### '):
            header_text = line.lstrip('#').strip()
            return header_text
    
    return None

def process_licenses(licenses_path, lektionen_dir):
    with open(licenses_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    changes = 0
    
    for line in lines:
        # Match pattern: | <span id="lektXXYY"></span> [`lektXXYY.jpg`](URL) |
        match = re.search(r'\[`(lekt(\d{2})\d{2})\.jpg`\]\(([^)]+)\)', line)
        if match:
            image_name = match.group(1) + ".jpg"
            lesson_num = match.group(2)
            current_url = match.group(3)
            
            lesson_file = f"lektion{lesson_num}.md"
            lesson_path = os.path.join(lektionen_dir, lesson_file)
            
            header = find_image_header(lesson_path, image_name)
            if header:
                anchor = "#_" + slugify(header)
                # VitePress links usually don't need the full path if it's already in the same dir, 
                # but licenses.md is in docs/ and lektionen is in docs/lektionen/
                new_url = f"/lektionen/lektion{lesson_num}{anchor}"
                
                # Special case: images in wortliste.md
                # If current URL points to wortliste, and we found it in lektionXX.md, 
                # we should probably prefer the lesson link as per user request.
                
                if current_url != new_url:
                    line = line.replace(current_url, new_url)
                    changes += 1
        
        new_lines.append(line)
    
    return "".join(new_lines), changes

if __name__ == "__main__":
    licenses_path = "/Volumes/SanDisk1TB/proj/Payer/docs/licenses.md"
    lektionen_dir = "/Volumes/SanDisk1TB/proj/Payer/docs/lektionen"
    
    new_content, count = process_licenses(licenses_path, lektionen_dir)
    print(f"Proposed changes: {count}")
    
    with open("/Volumes/SanDisk1TB/proj/Payer/scratch/licenses_updated.md", "w", encoding="utf-8") as f:
        f.write(new_content)

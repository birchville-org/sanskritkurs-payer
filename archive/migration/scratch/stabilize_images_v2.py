import os
import re

def fix_image_links(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Match anything that looks like an image link containing "/images/"
    # even if it has weird spaces or prefixes
    img_pattern = re.compile(r'(!\[.*?\]\(.*?(?:/images/|/images/)[^)]+\))|(<img[^>]+src=".*?(?:/images/|/images/)[^"]+"[^>]*>)', re.IGNORECASE)

    def check_link(match):
        full_match = match.group(0)
        
        # Extract the path
        if full_match.startswith('!'):
            m = re.search(r'\((.*?)\)', full_match)
            img_path = m.group(1) if m else ""
        else:
            m = re.search(r'src="(.*?)"', full_match)
            img_path = m.group(1) if m else ""
            
        # Clean up the path (remove leading spaces, dots, etc.)
        cleaned_path = re.search(r'/images/[^" )]+', img_path)
        if not cleaned_path:
            return f"<!-- Broken image link format: {full_match} -->"
            
        img_file_path = cleaned_path.group(0)
        
        # Check if it exists in docs/public
        abs_path = os.path.join('/Volumes/SanDisk1TB/proj/Payer/docs/public', img_file_path.lstrip('/'))
        if not os.path.exists(abs_path):
            print(f"Broken link in {filepath}: {img_path} (cleaned: {img_file_path})")
            return f"<!-- Broken image: {full_match} -->"
        
        # If it exists, we should probably normalize the link to be exactly /images/...
        if full_match.startswith('!'):
            alt_text = re.search(r'!\[(.*?)\]', full_match).group(1)
            return f"![{alt_text}]({img_file_path})"
        else:
            return f'<img src="{img_file_path}">'

    new_content = img_pattern.sub(check_link, content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

for root, dirs, files in os.walk('/Volumes/SanDisk1TB/proj/Payer/docs/'):
    for filename in files:
        if filename.endswith('.md'):
            fix_image_links(os.path.join(root, filename))

print("Image links stabilized (v2).")

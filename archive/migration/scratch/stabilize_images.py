import os
import re

def fix_image_links(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Find all ![](/images/...) or <img src="/images/...">
    # Note: After my sanitization, <img might be escaped.
    
    def check_link(match):
        full_match = match.group(0)
        img_path = match.group(1)
        
        # Check if it exists in docs/public
        abs_path = os.path.join('/Volumes/SanDisk1TB/proj/Payer/docs/public', img_path.lstrip('/'))
        if not os.path.exists(abs_path):
            print(f"Broken link in {filepath}: {img_path}")
            # Replace with a dummy or comment it out
            return f"<!-- Broken image: {full_match} -->"
        return full_match

    # Markdown links
    new_content = re.sub(r'!\[.*?\]\((/images/[^)]+)\)', check_link, content)
    
    # HTML links (in case they weren't escaped)
    new_content = re.sub(r'<img[^>]+src="(/images/[^"]+)"[^>]*>', check_link, new_content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

for root, dirs, files in os.walk('/Volumes/SanDisk1TB/proj/Payer/docs/'):
    for filename in files:
        if filename.endswith('.md'):
            fix_image_links(os.path.join(root, filename))

print("Image links stabilized.")

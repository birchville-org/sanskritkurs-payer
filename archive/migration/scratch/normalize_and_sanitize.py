import os
import re

# List of tags we want to keep
VALID_TAGS = [
    'br', 'div', 'script', 'img', 'span', 'info', 'tip', 'warning', 'danger', 
    'details', 'summary', 'media', 'grammar-box', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td',
    'blockquote', 'hr', 'sub', 'sup', 'b', 'i', 'u', 's', 'em', 'strong', 'code', 'pre', 'cite'
]

TAG_RE = re.compile(r'</?(?:' + '|'.join(VALID_TAGS) + r')(?:\s+[^>]*?)?>|<!--.*?-->', re.IGNORECASE | re.DOTALL)

def normalize_and_sanitize(content):
    # 1. Normalize: Convert escaped brackets back to raw
    content = content.replace('&lt;', '<')
    content = content.replace('&gt;', '>')
    
    # 2. Sanitize: Hide valid tags
    placeholders = []
    def replace_tag(match):
        placeholders.append(match.group(0))
        return f"__TAG_PLACEHOLDER_{len(placeholders)-1}__"
    
    safe_content = TAG_RE.sub(replace_tag, content)
    
    # 3. Escape all remaining raw brackets
    safe_content = safe_content.replace('<', '&lt;')
    safe_content = safe_content.replace('>', '&gt;')
    
    # 4. Restore valid tags
    for i, tag in enumerate(placeholders):
        safe_content = safe_content.replace(f"__TAG_PLACEHOLDER_{i}__", tag)
        
    return safe_content

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = normalize_and_sanitize(content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

# Walk through all directories in docs/
for root, dirs, files in os.walk('/Volumes/SanDisk1TB/proj/Payer/docs/'):
    for filename in files:
        if filename.endswith('.md'):
            # Skip images and other binary stuff
            fix_file(os.path.join(root, filename))

print("Normalization and Sanitization complete.")

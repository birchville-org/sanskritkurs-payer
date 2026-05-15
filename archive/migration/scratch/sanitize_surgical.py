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

def sanitize_content(content):
    # Find all valid tags and placeholders
    placeholders = []
    def replace_tag(match):
        placeholders.append(match.group(0))
        return f"__TAG_PLACEHOLDER_{len(placeholders)-1}__"
    
    # Temporarily hide valid tags
    safe_content = TAG_RE.sub(replace_tag, content)
    
    # Now escape all remaining < and >
    safe_content = safe_content.replace('<', '&lt;')
    safe_content = safe_content.replace('>', '&gt;')
    
    # Restore tags
    for i, tag in enumerate(placeholders):
        safe_content = safe_content.replace(f"__TAG_PLACEHOLDER_{i}__", tag)
        
    return safe_content

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = sanitize_content(content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

# Walk through all directories in docs/
for root, dirs, files in os.walk('/Volumes/SanDisk1TB/proj/Payer/docs/'):
    for filename in files:
        if filename.endswith('.md'):
            fix_file(os.path.join(root, filename))

print("Surgical sanitization complete.")

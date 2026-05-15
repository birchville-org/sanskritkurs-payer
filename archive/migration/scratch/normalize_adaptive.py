import os
import re

# Global list of potentially valid tags
ALL_VALID_TAGS = [
    'br', 'div', 'script', 'img', 'span', 'info', 'tip', 'warning', 'danger', 
    'details', 'summary', 'media', 'grammar-box', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td',
    'blockquote', 'hr', 'sub', 'sup', 'b', 'i', 'u', 's', 'em', 'strong', 'code', 'pre', 'cite'
]

def get_balanced_tags(content):
    balanced = []
    for tag in ALL_VALID_TAGS:
        # Simple count check for balancing
        # Note: This doesn't check for nesting order, but it's a good first pass
        c_open = content.count(f'<{tag}')
        c_close = content.count(f'</{tag}>')
        
        # Self-closing tags are always balanced
        if tag in ['br', 'img', 'hr', '!--']:
            balanced.append(tag)
        elif c_open == c_close and c_open > 0:
            balanced.append(tag)
    return balanced

def normalize_and_sanitize(content):
    # 1. Normalize: Convert escaped brackets back to raw
    content = content.replace('&lt;', '<')
    content = content.replace('&gt;', '>')
    
    # 2. Identify balanced tags to preserve in this specific content
    preserved_tags = get_balanced_tags(content)
    
    # 3. Sanitize: Hide ONLY balanced tags
    tag_pattern = r'</?(?:' + '|'.join(preserved_tags + ['!--']) + r')(?:\s+[^>]*?)?>|<!--.*?-->|:::.*'
    if not preserved_tags:
        tag_pattern = r'<!--.*?-->|:::.*'
        
    tag_re = re.compile(tag_pattern, re.IGNORECASE | re.DOTALL)
    
    placeholders = []
    def replace_tag(match):
        placeholders.append(match.group(0))
        return f"__TAG_PLACEHOLDER_{len(placeholders)-1}__"
    
    safe_content = tag_re.sub(replace_tag, content)
    
    # 4. Escape all remaining raw brackets
    safe_content = safe_content.replace('<', '&lt;')
    safe_content = safe_content.replace('>', '&gt;')
    
    # 5. Restore valid tags
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
            fix_file(os.path.join(root, filename))

print("Adaptive Normalization and Sanitization complete.")

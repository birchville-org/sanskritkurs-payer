import re

VALID_TAGS = [
    'br', 'div', 'script', 'img', 'span', 'info', 'tip', 'warning', 'danger', 
    'details', 'summary', 'media', 'grammar-box', 'a', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6',
    'p', 'ul', 'ol', 'li', 'table', 'thead', 'tbody', 'tfoot', 'tr', 'th', 'td',
    'blockquote', 'hr', 'sub', 'sup', 'b', 'i', 'u', 's', 'em', 'strong', 'code', 'pre', 'cite'
]

TAG_RE = re.compile(r'</?(?:' + '|'.join(VALID_TAGS) + r')(?:\s+[^>]*?)?>|<!--.*?-->', re.IGNORECASE | re.DOTALL)

test_str = '<table><tbody><tr><td colspan="4">**Основи**</td></tr>'
placeholders = []
def replace_tag(match):
    placeholders.append(match.group(0))
    return f"__TAG_PLACEHOLDER_{len(placeholders)-1}__"

safe_content = TAG_RE.sub(replace_tag, test_str)
print(f"Safe: {safe_content}")
print(f"Placeholders: {placeholders}")

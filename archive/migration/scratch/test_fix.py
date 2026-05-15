import re

ALL_VALID_TAGS = ['td', 'tr', 'table']

def get_balanced_tags(content):
    balanced = []
    for tag in ALL_VALID_TAGS:
        c_open = content.count(f'<{tag}')
        c_close = content.count(f'</{tag}>')
        if c_open == c_close and c_open > 0:
            balanced.append(tag)
    return balanced

def normalize_and_sanitize(content):
    content = content.replace('&lt;', '<')
    content = content.replace('&gt;', '>')
    preserved_tags = get_balanced_tags(content)
    tag_pattern = r'</?(?:' + '|'.join(preserved_tags + ['!--']) + r')(?:\s+[^>]*?)?>'
    tag_re = re.compile(tag_pattern, re.IGNORECASE)
    placeholders = []
    def replace_tag(match):
        placeholders.append(match.group(0))
        return f"__TAG_PLACEHOLDER_{len(placeholders)-1}__"
    safe_content = tag_re.sub(replace_tag, content)
    safe_content = safe_content.replace('<', '&lt;')
    safe_content = safe_content.replace('>', '&gt;')
    for i, tag in enumerate(placeholders):
        safe_content = safe_content.replace(f"__TAG_PLACEHOLDER_{i}__", tag)
    return safe_content

test_str = "**3. **</td><td>--- / -"
print(f"Result: {normalize_and_sanitize(test_str)}")

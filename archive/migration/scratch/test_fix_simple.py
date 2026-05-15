import re

def normalize_and_sanitize(content):
    content = content.replace('&lt;', '<')
    content = content.replace('&gt;', '>')
    print(f"DEBUG: after normalize: {content}")
    # We'll just simplify for test
    safe_content = content.replace('<', '&lt;')
    safe_content = safe_content.replace('>', '&gt;')
    print(f"DEBUG: after replace: {safe_content}")
    return safe_content

test_str = "**3. **</td><td>--- / -"
normalize_and_sanitize(test_str)

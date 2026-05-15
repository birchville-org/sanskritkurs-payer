import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Escape all < that are not start of a known tag or comment
    # Known tags: br, div, script, img, span, info, tip, warning, danger, details, summary, media, grammar-box, a, b, i, u, s, em, strong, code, pre, h1-6, p, ul, ol, li, table, thead, tbody, tfoot, tr, th, td, blockquote, hr, sub, sup, cite, !--
    tags = r'/?(?:br|div|script|img|span|info|tip|warning|danger|details|summary|media|grammar-box|a|h[1-6]|p|ul|ol|li|table|thead|tbody|tfoot|tr|th|td|blockquote|hr|sub|sup|b|i|u|s|em|strong|code|pre|cite|!--)'
    content = re.sub(r'<(?!' + tags + r'\b)', r'&lt;', content)
    
    # 2. Escape all > that are not part of a tag
    # A > is part of a tag if it's preceded by a tag name or an attribute
    # We'll just escape > if it's preceded by a non-tag character (like a letter or space)
    # AND it's not at the start of a line (blockquote)
    
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if line.startswith('>'):
            # It's a blockquote. Escape > inside the line, but keep the first one.
            first_char = line[0]
            rest = line[1:]
            # Escape > in rest if not closing a tag
            # We use a simple rule: if it follows a tag name, it's likely fine.
            # But here, we'll just escape > if it's after a non-tag char.
            rest = re.sub(r'(?<!' + tags + r')>', r'&gt;', rest)
            new_lines.append(first_char + rest)
        else:
            # Not a blockquote. Escape > if not closing a tag.
            line = re.sub(r'(?<!' + tags + r')>', r'&gt;', line)
            new_lines.append(line)
    
    content = '\n'.join(new_lines)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Walk through all directories in docs/
for root, dirs, files in os.walk('/Volumes/SanDisk1TB/proj/Payer/docs/'):
    for filename in files:
        if filename.endswith('.md'):
            fix_file(os.path.join(root, filename))

print("Aggressive global sanitization complete.")

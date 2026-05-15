import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Escape < if not start of known tag
    tags = r'/?(?:br|div|script|img|span|info|tip|warning|danger|details|summary|media|grammar-box|a|h[1-6]|p|ul|ol|li|table|thead|tbody|tfoot|tr|th|td|blockquote|hr|sub|sup|b|i|u|s|em|strong|code|pre|cite|!--)'
    content = re.sub(r'<(?!' + tags + r'\b)', r'&lt;', content)
    
    # 2. Escape > if it follows something that is NOT a tag ending
    # We'll just escape ALL > that are followed by a space or end of line, or at end of line
    # Except if it's start of line (blockquote)
    
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if line.startswith('>'):
            # Blockquote. Escape other >
            first = line[0]
            rest = line[1:]
            # Only escape > if not immediately preceded by / or " or a tag name
            # For simplicity, escape > if it's preceded by a space or a word
            rest = re.sub(r'([a-zA-Z0-9\s])>', r'\1&gt;', rest)
            new_lines.append(first + rest)
        else:
            # Not blockquote
            line = re.sub(r'([a-zA-Z0-9\s])>', r'\1&gt;', line)
            new_lines.append(line)
            
    content = '\n'.join(new_lines)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Walk through all directories in docs/
for root, dirs, files in os.walk('/Volumes/SanDisk1TB/proj/Payer/docs/'):
    for filename in files:
        if filename.endswith('.md'):
            fix_file(os.path.join(root, filename))

print("Safe global sanitization complete.")

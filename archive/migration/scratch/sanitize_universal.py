import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Escape < if not followed by a tag name start (a-z or /)
    content = re.sub(r'<(?!/?(?:br|div|script|img|span|info|tip|warning|danger|details|summary|media|grammar-box|a|h[1-6]|p|ul|ol|li|table|thead|tbody|tfoot|tr|th|td|blockquote|hr|sub|sup|b|i|u|s|em|strong|code|pre|cite|!--))', r'&lt;', content)
    
    # Escape > if it follows something that is not likely a tag or blockquote
    # We'll just escape > if it's preceded by a space or a word and NOT start of line
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if line.startswith('>'):
            new_lines.append('>' + re.sub(r'([a-zA-Z0-9\s])>', r'\1&gt;', line[1:]))
        else:
            new_lines.append(re.sub(r'([a-zA-Z0-9\s])>', r'\1&gt;', line))
            
    content = '\n'.join(new_lines)

    # Specific fix for the "Attribute name cannot contain ..." error
    # which is often caused by unquoted attributes or broken tags.
    # We'll just remove all HTML except for the ones we know are safe.
    # Actually, we'll just escape ALL < and > that are not part of a very strict list of tags.
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Walk through all directories in docs/
for root, dirs, files in os.walk('/Volumes/SanDisk1TB/proj/Payer/docs/'):
    for filename in files:
        if filename.endswith('.md'):
            fix_file(os.path.join(root, filename))

print("Universal sanitization complete.")

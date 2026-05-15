import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Escape < followed by a letter or digit (that isn't a known tag)
    tags = r'/?(?:br|div|script|img|span|info|tip|warning|danger|details|summary|media|grammar-box|a|h[1-6]|p|ul|ol|li|table|thead|tbody|tfoot|tr|th|td|blockquote|hr|sub|sup|b|i|u|s|em|strong|code|pre|cite|!--)'
    content = re.sub(r'<(?!' + tags + r'\b)', r'&lt;', content)
    
    # Escape << as well
    content = content.replace('<<', '&lt;&lt;')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

# Walk through all directories in docs/
for root, dirs, files in os.walk('/Volumes/SanDisk1TB/proj/Payer/docs/'):
    for filename in files:
        if filename.endswith('.md'):
            fix_file(os.path.join(root, filename))

print("Global sanitization complete.")

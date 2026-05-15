import os
import re

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Escape angle brackets in date ranges like <1864 - 1920>
    # and other non-tag usages like <ūde> or << ta-tas
    
    # Negative lookahead for common tags we want to keep
    # (br, div, script, img, span, info, tip, warning, danger, details, summary, media, grammar-box)
    # Also keep </tags>
    
    # This regex finds < if NOT followed by a valid tag name or /tag name
    # We'll be conservative and only escape if followed by a digit or if it's isolated
    
    # 1. Escape < followed by a digit
    content = re.sub(r'<(\d)', r'&lt;\1', content)
    
    # 2. Escape > preceded by a digit
    content = re.sub(r'(\d)>', r'\1&gt;', content)
    
    # 3. Escape isolated < (followed by space or at end of line)
    content = re.sub(r'<(\s|$)', r'&lt;\1', content)
    
    # 4. Escape <<
    content = content.replace('<<', '&lt;&lt;')
    
    # 5. Escape < followed by non-tag chars (like ū in <ūde>)
    # Valid tag start: [a-zA-Z/]
    # So if it's < followed by something else, escape it.
    # Except for ::: which are not <
    content = re.sub(r'<(?!/?(?:br|div|script|img|span|info|tip|warning|danger|details|summary|media|grammar-box|a|h[1-6]|p|ul|ol|li|table|tr|td|th|thead|tbody|tfoot|sub|sup|b|i|u|s|em|strong|code|pre|blockquote|cite|hr|br|!--))', r'&lt;', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

base_dir = '/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/'
for filename in os.listdir(base_dir):
    if filename.endswith('.md'):
        fix_file(os.path.join(base_dir, filename))

print("Sanitization complete.")

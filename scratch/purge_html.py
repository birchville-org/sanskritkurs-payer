import os
import re
import sys

directory = 'docs/lektionen'

def purge_html(content):
    # 1. First, convert ::: info and > [!INFO] to ::: deleteme-box
    content = re.sub(r'::: info', '::: deleteme-box', content, flags=re.I)
    # Target the blockquote style: > [!INFO] ... till end of paragraph or next empty line
    content = re.sub(r'>\s*\[!INFO\].*?(\n\s*\n|\Z)', '::: deleteme-box\n\\g<0>\n:::\n\n', content, flags=re.I | re.S)
    
    # 2. Remove common HTML tags but keep content
    # We target tags that are definitely illegal in the Zero-HTML policy
    content = re.sub(r'</?(div|span|strong|u|sup|sub|table|thead|tbody|tr|td|th|blockquote|p)( [^>]*?)?>', '', content, flags=re.I)
    
    # 3. Handle <br> - replace with space
    content = re.sub(r'<br\s*/?>', ' ', content, flags=re.I)
    
    # 4. Clean up any &lt; and &gt; that should be actual < and > for Markdown syntax
    # But only for VitePress containers and images
    # Actually, it's safer to just fix the characters in specific contexts
    
    # Escape ALL < and > that are NOT part of ::: or ::::
    # We protect the colons first
    content = content.replace('::::', 'PLACEHOLDER_QUAD_COLON')
    content = content.replace(':::', 'PLACEHOLDER_TRI_COLON')
    
    # Protect blockquotes at start of line
    content = re.sub(r'^> ', 'PLACEHOLDER_BLOCKQUOTE ', content, flags=re.M)
    content = re.sub(r'^>\[!INFO\]', 'PLACEHOLDER_BLOCKQUOTE_INFO', content, flags=re.M)
    
    # Now escape
    content = content.replace('<', '&lt;').replace('>', '&gt;')
    
    # Restore protected syntax
    content = content.replace('PLACEHOLDER_QUAD_COLON', '::::')
    content = content.replace('PLACEHOLDER_TRI_COLON', ':::')
    content = content.replace('PLACEHOLDER_BLOCKQUOTE ', '> ')
    content = content.replace('PLACEHOLDER_BLOCKQUOTE_INFO', '>[!INFO]')
    
    return content

# Also process docs/it/lektionen if it exists
directories = ['docs/lektionen', 'docs/it/lektionen', 'docs/es/lektionen', 'docs/bg/lektionen', 'docs/ru/lektionen', 'docs/uk/lektionen']

for directory in directories:
    if not os.path.exists(directory):
        continue
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.md'):
                filepath = os.path.join(root, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                new_content = purge_html(content)
                
                if new_content != content:
                    print(f"Purged and Fixed HTML/Syntax in {filepath}")
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(new_content)

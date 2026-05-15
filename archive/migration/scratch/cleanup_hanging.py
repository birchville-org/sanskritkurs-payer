import os
import re

def cleanup_hanging_tags(content):
    # Find all table blocks
    table_blocks = []
    def hide_table(match):
        table_blocks.append(match.group(0))
        return f"__TABLE_BLOCK_{len(table_blocks)-1}__"
    
    # We'll use a greedy match for table blocks to be safe
    new_content = re.sub(r'<table>.*?</table>', hide_table, content, flags=re.IGNORECASE | re.DOTALL)
    
    # Now in the remaining content, escape all td, tr, tbody tags
    new_content = re.sub(r'</?(?:td|tr|tbody|table|th)(?:\s+[^>]*?)?>', lambda m: m.group(0).replace('<', '&lt;').replace('>', '&gt;'), new_content, flags=re.IGNORECASE)
    
    # Restore table blocks
    for i, block in enumerate(table_blocks):
        new_content = new_content.replace(f"__TABLE_BLOCK_{i}__", block)
        
    return new_content

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = cleanup_hanging_tags(content)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

for root, dirs, files in os.walk('/Volumes/SanDisk1TB/proj/Payer/docs/'):
    for filename in files:
        if filename.endswith('.md'):
            fix_file(os.path.join(root, filename))

print("Hanging tags cleanup complete.")

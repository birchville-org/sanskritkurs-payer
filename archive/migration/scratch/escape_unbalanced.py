import os

TAGS_TO_CHECK = ['table', 'tbody', 'tr', 'td', 'th', 'thead', 'tfoot', 'div', 'span', 'script', 'a', 'p', 'ul', 'ol', 'li']

def get_unbalanced(content):
    unbalanced = []
    for tag in TAGS_TO_CHECK:
        c_open = content.count(f'<{tag}')
        c_close = content.count(f'</{tag}>')
        if c_open != c_close:
            unbalanced.append(tag)
    return unbalanced

def fix_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    unbalanced = get_unbalanced(content)
    if not unbalanced:
        return False
    
    # Escape all unbalanced tags in this file
    new_content = content
    for tag in unbalanced:
        # Escape <tag and </tag>
        new_content = new_content.replace(f'<{tag}', f'&lt;{tag}')
        new_content = new_content.replace(f'</{tag}>', f'&lt;/{tag}&gt;')
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False

for root, dirs, files in os.walk('/Volumes/SanDisk1TB/proj/Payer/docs/'):
    for filename in files:
        if filename.endswith('.md'):
            fix_file(os.path.join(root, filename))

print("Unbalanced tags escaped.")

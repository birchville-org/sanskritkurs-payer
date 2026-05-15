import os

def check_tags(content):
    tags = ['table', 'tbody', 'tr', 'td', 'th', 'thead', 'tfoot', 'div', 'span', 'script', 'a', 'p', 'ul', 'ol', 'li']
    counts = {}
    for tag in tags:
        c_open = content.count(f'<{tag}')
        c_close = content.count(f'</{tag}>')
        if c_open != c_close:
            counts[tag] = (c_open, c_close)
    return counts

for root, dirs, files in os.walk('/Volumes/SanDisk1TB/proj/Payer/docs/'):
    for filename in files:
        if filename.endswith('.md'):
            filepath = os.path.join(root, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            unbalanced = check_tags(content)
            if unbalanced:
                print(f"Unbalanced tags in {filepath}: {unbalanced}")

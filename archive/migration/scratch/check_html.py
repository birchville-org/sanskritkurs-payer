import os

def check_tags(content):
    tags = ['table', 'tbody', 'tr', 'td', 'th', 'thead', 'tfoot']
    counts = {}
    for tag in tags:
        counts[tag] = content.count(f'<{tag}')
        counts[f'/{tag}'] = content.count(f'</{tag}>')
    return counts

filepath = '/Volumes/SanDisk1TB/proj/Payer/docs/bg/lektionen/lektion04.md'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

print(f"Stats for {filepath}:")
print(check_tags(content))

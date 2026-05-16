import os
import re

directory = '/Volumes/SanDisk1TB/proj/Payer/docs/lektionen'

# Patterns
# Note: Grep showed "::: deleteme-box Zitierweise & Rechte"
metadata_box_re = re.compile(r'::: deleteme-box Zitierweise & Rechte.*?:::', re.DOTALL)
# Also some use [!INFO] callout style in older migrations
info_callout_re = re.compile(r'> \[!INFO\] Zitierweise & Rechte.*?>.*?\[Impressum & Copyright\]\(/impressum\)\n?', re.DOTALL)

# Wortliste triple nesting fix
wortliste_top_re = re.compile(r'::: deleteme-box\n::: deleteme-box\n::: deleteme-box\n> \[!INFO\] Zitierweise & Rechte.*?:::\n:::\n:::', re.DOTALL)

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content

    # 1. Delete top metadata boxes
    if 'wortliste.md' in filepath:
        content = wortliste_top_re.sub('', content)
    else:
        # Try both patterns
        content = metadata_box_re.sub('', content)
        content = info_callout_re.sub('', content)

    # 2. Lektion 53 specific conversions
    if 'lektion53.md' in filepath:
        # Line 523 (Originaltabelle) -> tip
        content = content.replace('::: deleteme-box\nOriginaltabelle, Markdown Syntax muss noch verbessert werden.\n:::', 
                                  '::: tip\nOriginaltabelle, Markdown Syntax muss noch verbessert werden.\n:::')
        
        # Line 705 (Concluding note) -> info
        content = content.replace('::: deleteme-box\nFinitum feliciter', 
                                  '::: info\nFinitum feliciter')
        
        # Line 716 (Quellen) -> info
        content = content.replace('::: deleteme-box\n### Quellen', 
                                  '::: info\n### Quellen')

    # 3. Übungen specific conversions (Explanations)
    if 'uebung16.md' in filepath or 'uebung20.md' in filepath:
        content = content.replace('::: deleteme-box Erläuterungen', '::: info Erläuterungen')
        content = content.replace('::: deleteme-box Erläuterung', '::: info Erläuterung')

    # 4. Wortliste bottom Quellen conversion
    if 'wortliste.md' in filepath:
        content = content.replace(':::: deleteme-box\n### Quellen', '::: info\n### Quellen')
        content = content.replace('::: deleteme-box\n### Quellen', '::: info\n### Quellen')

    if content != original_content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Processed: {filepath}")

for filename in os.listdir(directory):
    if filename.endswith('.md'):
        process_file(os.path.join(directory, filename))

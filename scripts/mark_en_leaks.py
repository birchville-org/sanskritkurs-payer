import os
import re

safe_english_words = ['the', 'is', 'to', 'and', 'that', 'of', 'for', 'this', 'are', 'with']
en_pattern = re.compile(r'\b(' + '|'.join(safe_english_words) + r')\b', re.IGNORECASE)

docs_dir = 'docs'
langs = [d for d in os.listdir(docs_dir) if os.path.isdir(os.path.join(docs_dir, d)) and d not in ('de', 'en', 'public', '.vitepress')]

leak_count = 0
file_count = 0

for lang in langs:
    lang_dir = os.path.join(docs_dir, lang, 'lektionen')
    if not os.path.isdir(lang_dir): continue
    
    for filename in os.listdir(lang_dir):
        if not filename.endswith('.md'): continue
        filepath = os.path.join(lang_dir, filename)
        de_filepath = os.path.join(docs_dir, 'lektionen', filename)
        
        if not os.path.isfile(de_filepath): continue
        
        with open(de_filepath, 'r', encoding='utf-8') as f:
            de_blocks = f.read().split('\n\n')
            
        with open(filepath, 'r', encoding='utf-8') as f:
            lang_blocks = f.read().split('\n\n')
            
        # In case block counts don't match, we still do our best
        min_len = min(len(de_blocks), len(lang_blocks))
        modified = False
        
        for i in range(min_len):
            de_block = de_blocks[i]
            lang_block = lang_blocks[i]
            
            en_count = len(en_pattern.findall(lang_block))
            if en_count >= 3:
                de_en_count = len(en_pattern.findall(de_block))
                if en_count > de_en_count + 2:
                    if "TODO: Fallback translation" not in lang_block:
                        lang_blocks[i] = lang_block + ' <!-- TODO: Fallback translation -->'
                        modified = True
                        leak_count += 1
                        
        if modified:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write('\n\n'.join(lang_blocks))
            file_count += 1
            print(f"[{lang}] Marked leaks in {filename}")

print(f"\nDone. Marked {leak_count} individual blocks across {file_count} files.")

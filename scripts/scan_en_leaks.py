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
        
        # Original German file
        de_filepath = os.path.join(docs_dir, 'lektionen', filename)
        if not os.path.isfile(de_filepath): continue
        
        with open(de_filepath, 'r', encoding='utf-8') as f:
            de_text = f.read()
        de_en_count = len(en_pattern.findall(de_text))
        
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()
        
        en_count = len(en_pattern.findall(text))
        
        if en_count > de_en_count + 5:
            # Check if this file already has a fallback marker
            if "TODO: Fallback translation" not in text:
                print(f"[{lang}] {filename} -> {en_count} English words found (German had {de_en_count})")
                leak_count += 1

print(f"\nTotal leaks found: {leak_count}")

import os

LOCALES = ['bg', 'en', 'es', 'it', 'ru', 'uk']

def escape_all_brackets(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 1. Normalize: Convert escaped brackets back to raw
    content = content.replace('&lt;', '<')
    content = content.replace('&gt;', '>')
    
    # 2. Escape ALL < and >
    new_content = content.replace('<', '&lt;').replace('>', '&gt;')
    
    # 3. Restore VitePress containers (:::) which don't use brackets anyway
    # So no need to do anything for :::.
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)

# Restore locales first
for locale in LOCALES:
    if os.path.exists(locale):
        # Move it back to docs/ if it's currently outside
        import shutil
        if os.path.exists(f'docs/{locale}'):
            shutil.rmtree(f'docs/{locale}')
        shutil.move(locale, 'docs/')

# Sanitize locales
for locale in LOCALES:
    root_dir = f'docs/{locale}'
    for root, dirs, files in os.walk(root_dir):
        for filename in files:
            if filename.endswith('.md'):
                escape_all_brackets(os.path.join(root, filename))

print("Aggressive locale sanitization complete.")

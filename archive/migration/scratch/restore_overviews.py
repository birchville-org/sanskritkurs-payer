import re
import os

LANGS = ['root', 'en', 'it', 'es', 'bg', 'ru', 'uk']

def remove_overviews(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Regex to find ## [Number] Übersicht (or localized version) and everything until the next ## header
    # Note: Many files use the German 'Übersicht' even in translations, or the localized term.
    # We look for common patterns.
    overview_patterns = [
        r'##\s+(\d+\.\d+\.\s+)?Übersicht\s*?\n([\s\S]*?)(?=\n##\s+)',
        r'##\s+(\d+\.\d+\.\s+)?Overview\s*?\n([\s\S]*?)(?=\n##\s+)',
        r'##\s+(\d+\.\d+\.\s+)?Descrizione\s*?\n([\s\S]*?)(?=\n##\s+)',
        r'##\s+(\d+\.\d+\.\s+)?Descripción\s*?\n([\s\S]*?)(?=\n##\s+)',
        r'##\s+(\d+\.\d+\.\s+)?Преглед\s*?\n([\s\S]*?)(?=\n##\s+)',
        r'##\s+(\d+\.\d+\.\s+)?Обзор\s*?\n([\s\S]*?)(?=\n##\s+)',
        r'##\s+(\d+\.\d+\.\s+)?Огляд\s*?\n([\s\S]*?)(?=\n##\s+)'
    ]
    
    original = content
    for pattern in overview_patterns:
        content = re.sub(pattern, '', content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content.strip() + '\n')
        return True
    return False

def main():
    docs_root = "/Volumes/SanDisk1TB/proj/Payer/docs"
    count = 0
    for lang in LANGS:
        target_dir = os.path.join(docs_root, "lektionen") if lang == 'root' else os.path.join(docs_root, lang, "lektionen")
        if not os.path.exists(target_dir): continue
        
        for filename in os.listdir(target_dir):
            if filename.endswith(".md"):
                if remove_overviews(os.path.join(target_dir, filename)):
                    count += 1
    print(f"Removed redundant overviews from {count} files.")

if __name__ == "__main__":
    main()

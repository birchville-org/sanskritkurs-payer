import os
import re

# Precise replacements for Bulgarian files
BG_PHRASES = {
    'Weitere कृत्-Bildungen auf -a': 'Още कृत्-образувания на -a',
    'Zur Nominalbildung': 'Към именообразуване',
    'Wortbildung': 'думаобразуване',
    'Nominalbildung': 'именообразуване',
    'Desiderativstämme': 'дезидеративни основи',
    'Vergangenheitstempora': 'минали времена',
    'Bedeutungsunterschied': 'разлика в значението',
    'adverbialem Vorderglied': 'наречена предна част',
    'Ozean der Sanskritliteratur': 'океан на санскритската литература',
    'ist ein Gott': 'е бог',
    'Feuer) ist ein Gott': 'огън) е бог',
    'le फर्निश्डlektion05': 'lektion05',
    'le फर्निश्ड': 'lektion',
    'Suffixe': 'суфикси',
    'Suffix': 'суфикс',
    'Bildungen': 'образувания',
    'Bildung': 'образуване',
    'Komposita': 'композити',
    'Neutrum': 'среден род',
    'mask.': 'м.р.',
    'fem.': 'ж.р.',
    'Neutr.': 'ср.р.',
}

def repair_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    orig_content = content
    
    if '/bg/' in path:
        # 1. Phrases first
        for err, fix in sorted(BG_PHRASES.items(), key=lambda x: len(x[0]), reverse=True):
            content = content.replace(err, fix)
            
        # 2. Targeted word replacements with boundaries
        words_to_fix = {
            'Suffix': 'суфикс',
            'Suffixe': 'суфикси',
            'Bildung': 'образуване',
            'Bildungen': 'образувания',
            'Komposita': 'композити',
            'und': 'и',
            'auf': 'на',
            'an': 'към',
        }
        for err, fix in words_to_fix.items():
            # Only if surrounded by non-Latin characters or boundaries
            content = re.sub(r'(?<![a-zA-Z])' + err + r'(?![a-zA-Z])', fix, content)

    if content != orig_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    docs_dir = "/Volumes/SanDisk1TB/proj/Payer/docs"
    count = 0
    for root, dirs, files in os.walk(docs_dir):
        if 'node_modules' in root: continue
        for file in files:
            if file.endswith('.md'):
                if repair_file(os.path.join(root, file)):
                    count += 1
    print(f"Repaired {count} files.")

if __name__ == "__main__":
    main()

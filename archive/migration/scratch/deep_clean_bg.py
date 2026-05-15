import os
import re

# German to Bulgarian mapping for common phrases and terms
DE_TO_BG = {
    r"über rechtes Urinieren": "относно правилното уриниране",
    r"Среден род Nom\.Akk\.sg\. zu": "среден род, Им./Вин. ед.ч. на",
    r"wörtlich:": "буквално:",
    r"bzw\. alternativ": "или алтернативно",
    r"Man möge eintreten": "Нека се влезе",
    r"Bitte treten Sie ein": "Моля, влезте",
    r"Herein!": "Влез!",
    r"Man möge sich setzen": "Нека се седне",
    r"Bitte setzen Sie sich": "Моля, седнете",
    r"Bitte nehmen Sie Platz": "Моля, заемете място",
    r"im Sinne des deutschen": "в смисъла на немското",
    r"oder nur einer Möglichkeit": "или само възможност",
    r"nicht aber": "но не и",
    r"Gegensatz zu": "противоположно на",
    r"dritte падежокончание": "трети падеж",
    r"двitия": "Винителен",
    r"тृतीया": "Творителен",
    r"षष्ठी": "Шеста",
    r"सptами": "Локатив",
    r"т\.\. \*\* \*\*": "...",
    r"statt": "вместо",
    r"bes\.": "особено",
    r"напр\.": "напр.",
    r"вижте": "вижте",
    r"във": "в",
}

def deep_clean(content):
    # Apply phrase replacements
    for pattern, replacement in DE_TO_BG.items():
        content = re.sub(pattern, replacement, content)
        
    # Remove redundant lines that are just repeats of IAST/Sanskrit
    lines = content.split('\n')
    new_lines = []
    prev_line = None
    for line in lines:
        stripped = line.strip()
        if stripped and stripped == prev_line:
            continue
        new_lines.append(line)
        prev_line = stripped
    
    return '\n'.join(new_lines)

def main():
    docs_dir = "/Volumes/SanDisk1TB/proj/Payer/docs/bg/lektionen"
    count = 0
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                
                new_content = deep_clean(content)
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
    print(f"Deep cleaned {count} files.")

if __name__ == "__main__":
    main()

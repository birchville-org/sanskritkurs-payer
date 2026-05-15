import os
import re

# German to Bulgarian mapping for terminology
TERM_MAP = {
    "Maskulinum": "Мъжки род",
    "Femininum": "Женски род",
    "Neutrum": "Среден род",
    "Geschlecht": "род",
    "Geschlechter": "родове",
    "Kasus": "падеж",
    "Endungen": "окончания",
    "Endung": "окончание",
    "Numeri": "числа",
    "Numerus": "число",
    "Genera": "родове",
    "Genus": "род",
    "Zählformen": "бройни форми",
    "Einzahl": "единствено число",
    "Zweizahl": "двойно число",
    "Mehrzahl": "множествено число",
    "Fälle": "падежи",
    "Priesterstand": "съсловие на свещениците",
    "Adelsstand": "съсловие на благородниците",
    "Bauernstand": "съсловие на земеделците",
    "Taschenbuch": "евтино издание",
    "Originaltitel": "Оригинално заглавие",
    "Paperback": "меки корици",
    "männliches": "мъжки",
    "weibliches": "женски",
    "sächliches": "среден",
    "grammatische": "граматически",
    "grammatisches": "граматически",
}

def repair_content(content):
    # 1. Terminology replacement (more aggressive, no word boundaries for these specific terms)
    sorted_keys = sorted(TERM_MAP.keys(), key=len, reverse=True)
    for ger in sorted_keys:
        bul = TERM_MAP[ger]
        # Replace occurrences with various capitalizations
        content = content.replace(ger, bul)
        content = content.replace(ger.lower(), bul.lower())
        content = content.replace(ger.upper(), bul.upper())
        
    # 2. Handle specific mixed script characters globally in common words
    # This addresses the "Frankenstein" issue
    content = re.sub(r'([а-яА-Я])a([а-яА-Я]?)', r'\1а\2', content)
    content = re.sub(r'([а-яА-Я])e([а-яА-Я]?)', r'\1е\2', content)
    content = re.sub(r'([а-яА-Я])o([а-яА-Я]?)', r'\1о\2', content)
    content = re.sub(r'([а-яА-Я])c([а-яА-Я]?)', r'\1с\2', content)
    content = re.sub(r'([а-яА-Я])p([а-яА-Я]?)', r'\1р\2', content)
    
    # 3. Specific manual fixes
    content = content.replace("Раванаs", "Равана")
    content = content.replace("Рамаs", "Рама")
    content = content.replace("Кschatriya", "Кшатрия")
    content = content.replace("** **", "...")
    
    return content

def main():
    docs_dir = "/Volumes/SanDisk1TB/proj/Payer/docs/bg/lektionen"
    count = 0
    for root, dirs, files in os.walk(docs_dir):
        for file in files:
            if file.endswith('.md'):
                path = os.path.join(root, file)
                with open(path, 'r', encoding='utf-8', errors='replace') as f:
                    content = f.read()
                
                new_content = repair_content(content)
                
                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    count += 1
    print(f"Repaired {count} files.")

if __name__ == "__main__":
    main()

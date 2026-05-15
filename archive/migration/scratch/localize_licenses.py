import os

LOCALES = {
    'en': {'title': 'Image Licenses (Audit)', 'file': 'Filename', 'desc': 'Source/Description', 'fallback': 'No specific license/source found in text'},
    'it': {'title': 'Licenze delle immagini (Audit)', 'file': 'Nome file', 'desc': 'Fonte/Descrizione', 'fallback': 'Nessuna licenza/fonte specifica trovata nel testo'},
    'es': {'title': 'Licencias de imágenes (Audit)', 'file': 'Nombre de archivo', 'desc': 'Fuente/Descripción', 'fallback': 'No se encontró ninguna licencia/fuente específica en el texto'},
    'bg': {'title': 'Лицензи за изображения (Одит)', 'file': 'Име на файл', 'desc': 'Източник/Описание', 'fallback': 'В текста не е намерен конкретен лиценз/източник'},
    'ru': {'title': 'Лицензии на изображения (Аудит)', 'file': 'Имя файла', 'desc': 'Источник/Описание', 'fallback': 'В тексте не найдено конкретной лицензии/источника'},
    'uk': {'title': 'Ліцензії на зображення (Аудит)', 'file': 'Ім\'я файлу', 'desc': 'Джерело/Опис', 'fallback': 'У тексті не знайдено конкретної ліцензії/джерела'}
}

def localize_licenses(filepath, lang):
    if lang not in LOCALES: return
    info = LOCALES[lang]
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        if line.startswith('# '):
            new_lines.append(f"# {info['title']}\n")
        elif '| Filename |' in line or '| Nome file |' in line:
            new_lines.append(f"| {info['file']} | {info['desc']} |\n")
        elif 'No specific license' in line or 'Nessuna licenza' in line:
            # Replace placeholder text in table rows
            new_line = line.replace('No specific license/source found in text', info['fallback'])
            new_line = new_line.replace('Nessuna licenza/fonte specifica trovata nel testo', info['fallback'])
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

def main():
    docs_root = "/Volumes/SanDisk1TB/proj/Payer/docs"
    for lang in LOCALES.keys():
        path = os.path.join(docs_root, lang, "licenses.md")
        if os.path.exists(path):
            localize_licenses(path, lang)
            print(f"Localized licenses for {lang}")

if __name__ == "__main__":
    main()

import os
import re
import sys

# Supported languages
LANGUAGES = ["en", "it", "es", "ru", "uk", "bg"]

# Base directories
BASE_DIR = "/Volumes/SanDisk1TB/proj/Payer/docs"
SOURCE_DIR = os.path.join(BASE_DIR, "lektionen")

# Multi-language dictionary for grammatical and structural terms
GRAMMAR_DICT = {
    "en": {
        "Maskulinum": "Masculine",
        "Femininum": "Feminine",
        "Neutrum": "Neuter",
        "Mask.": "Masc.",
        "Fem.": "Fem.",
        "Singular": "Singular",
        "Plural": "Plural",
        "Dual": "Dual",
        "Nominativ": "Nominative",
        "Akkusativ": "Accusative",
        "Instrumentalis": "Instrumental",
        "Dativ": "Dative",
        "Ablativ": "Ablative",
        "Genetiv": "Genitive",
        "Lokativ": "Locative",
        "Vokativ": "Vocative",
        "Beispiel": "Example",
        "Beispiele": "Examples",
        "Wortliste": "Vocabulary List",
        "Übung": "Exercise",
        "Übungsübung": "Exercise",
        "Übersetzungsübung": "Translation Exercise",
        "Wurzel": "Root",
        "Stamm": "Stem",
        "Präsensstamm": "Present Stem",
        "Futurstamm": "Future Stem",
        "Endung": "Ending",
        "Präsens": "Present",
        "Futur": "Future",
        "Imperfekt": "Imperfect",
        "Imperativ": "Imperative",
        "Optativ": "Optative",
        "Wochenspruch": "Weekly Verse",
        "Erklärung": "Explanation",
        "Bildung": "Formation",
        "Gebrauch": "Usage",
        "Quellen": "Sources",
        "Abb.:": "Fig.:",
        "Bildquelle:": "Image source:",
        "Details": "Details"
    },
    "it": {
        "Maskulinum": "Maschile",
        "Femininum": "Femminile",
        "Neutrum": "Neutro",
        "Mask.": "Masch.",
        "Fem.": "Femm.",
        "Singular": "Singolare",
        "Plural": "Plurale",
        "Dual": "Duale",
        "Nominativ": "Nominativo",
        "Akkusativ": "Accusativo",
        "Instrumentalis": "Strumentale",
        "Dativ": "Dativo",
        "Ablativ": "Ablativo",
        "Genetiv": "Genitivo",
        "Lokativ": "Locativo",
        "Vokativ": "Vocativo",
        "Beispiel": "Esempio",
        "Beispiele": "Esempi",
        "Wortliste": "Lessico",
        "Übung": "Esercizio",
        "Übungsübung": "Esercizio",
        "Übersetzungsübung": "Esercizio di traduzione",
        "Wurzel": "Radice",
        "Stamm": "Tema",
        "Präsensstamm": "Tema del presente",
        "Futurstamm": "Tema del futuro",
        "Endung": "Desinenza",
        "Präsens": "Presente",
        "Futur": "Futuro",
        "Imperfekt": "Imperfetto",
        "Imperativ": "Imperativo",
        "Optativ": "Ottativo",
        "Wochenspruch": "Verso settimanale",
        "Erklärung": "Spiegazione",
        "Bildung": "Formazione",
        "Gebrauch": "Uso",
        "Quellen": "Fonti",
        "Abb.:": "Fig.:",
        "Bildquelle:": "Fonte dell'immagine:",
        "Details": "Dettagli"
    },
    "es": {
        "Maskulinum": "Masculino",
        "Femininum": "Femenino",
        "Neutrum": "Neutro",
        "Mask.": "Masc.",
        "Fem.": "Fem.",
        "Singular": "Singular",
        "Plural": "Plural",
        "Dual": "Dual",
        "Nominativ": "Nominativo",
        "Akkusativ": "Acusativo",
        "Instrumentalis": "Instrumental",
        "Dativ": "Dativo",
        "Ablativ": "Ablativo",
        "Genetiv": "Genitivo",
        "Lokativ": "Locativo",
        "Vokativ": "Vocativo",
        "Beispiel": "Ejemplo",
        "Beispiele": "Ejemplos",
        "Wortliste": "Vocabulario",
        "Übung": "Ejercicio",
        "Übungsübung": "Ejercicio",
        "Übersetzungsübung": "Ejercicio de traducción",
        "Wurzel": "Raíz",
        "Stamm": "Tema",
        "Präsensstamm": "Tema de presente",
        "Futurstamm": "Tema de futuro",
        "Endung": "Terminación",
        "Präsens": "Presente",
        "Futur": "Futuro",
        "Imperfekt": "Imperfecto",
        "Imperativ": "Imperativo",
        "Optativ": "Optativo",
        "Wochenspruch": "Verso semanal",
        "Erklärung": "Explicación",
        "Bildung": "Formación",
        "Gebrauch": "Uso",
        "Quellen": "Fuentes",
        "Abb.:": "Ilustración:",
        "Bildquelle:": "Origen de la imagen:",
        "Details": "Detalles"
    },
    "bg": {
        "Maskulinum": "Мъжки род",
        "Femininum": "Женски род",
        "Neutrum": "Среден род",
        "Mask.": "М.р.",
        "Fem.": "Ж.р.",
        "Singular": "Единствено число",
        "Plural": "Множествено число",
        "Dual": "Двойствено число",
        "Nominativ": "Номинатив",
        "Akkusativ": "Акузатив",
        "Instrumentalis": "Инструменталис",
        "Dativ": "Датив",
        "Ablativ": "Аблатив",
        "Genetiv": "Генетив",
        "Lokativ": "Локатив",
        "Vokativ": "Вокатив",
        "Beispiel": "Пример",
        "Beispiele": "Примери",
        "Wortliste": "Речник",
        "Übung": "Упражнение",
        "Übungsübung": "Упражнение",
        "Übersetzungsübung": "Упражнение за превод",
        "Wurzel": "Корен",
        "Stamm": "Основа",
        "Präsensstamm": "Сегашна основа",
        "Futurstamm": "Бъдеща основа",
        "Endung": "Окончание",
        "Präsens": "Сегашно време",
        "Futur": "Бъдеще време",
        "Imperfekt": "Имперфект",
        "Imperativ": "Императив",
        "Optativ": "Оптатив",
        "Wochenspruch": "Стих на седмицата",
        "Erklärung": "Обяснение",
        "Bildung": "Образоване",
        "Gebrauch": "Употреба",
        "Quellen": "Източници",
        "Abb.:": "Фиг.:",
        "Bildquelle:": "Източник на изображението:",
        "Details": "Подробности"
    },
    "ru": {
        "Maskulinum": "Мужской род",
        "Femininum": "Женский род",
        "Neutrum": "Средний род",
        "Mask.": "М.р.",
        "Fem.": "Ж.р.",
        "Singular": "Единственное число",
        "Plural": "Множественное число",
        "Dual": "Двойственное число",
        "Nominativ": "Именительный падеж",
        "Akkusativ": "Винительный падеж",
        "Instrumentalis": "Творительный падеж",
        "Dativ": "Дательный падеж",
        "Ablativ": "Отложительный падеж",
        "Genetiv": "Родительный падеж",
        "Lokativ": "Местный падеж",
        "Vokativ": "Звательный падеж",
        "Beispiel": "Пример",
        "Beispiele": "Примеры",
        "Wortliste": "Словарь",
        "Übung": "Упражнение",
        "Übungsübung": "Упражнение",
        "Übersetzungsübung": "Упражнение на перевод",
        "Wurzel": "Корень",
        "Stamm": "Основа",
        "Präsensstamm": "Презенс-основа",
        "Futurstamm": "Футур-основа",
        "Endung": "Окончание",
        "Präsens": "Настоящее время",
        "Futur": "Будущее время",
        "Imperfekt": "Имперфект",
        "Imperativ": "Императив",
        "Optativ": "Оптатив",
        "Wochenspruch": "Стих недели",
        "Erklärung": "Объяснение",
        "Bildung": "Образование",
        "Gebrauch": "Употребление",
        "Quellen": "Источники",
        "Abb.:": "Рис.:",
        "Bildquelle:": "Источник изображения:",
        "Details": "Подробности"
    },
    "uk": {
        "Maskulinum": "Чоловічий рід",
        "Femininum": "Жіночий рід",
        "Neutrum": "Середній рід",
        "Mask.": "Ч.р.",
        "Fem.": "Ж.р.",
        "Singular": "Однина",
        "Plural": "Множина",
        "Dual": "Двоїна",
        "Nominativ": "Називний відмінок",
        "Akkusativ": "Знахідний відмінок",
        "Instrumentalis": "Орудний відмінок",
        "Dativ": "Давальний відмінок",
        "Ablativ": "Аблатив",
        "Genetiv": "Родовий відмінок",
        "Lokativ": "Місцевий відмінок",
        "Vokativ": "Кличний відмінок",
        "Beispiel": "Приклад",
        "Beispiele": "Приклади",
        "Wortliste": "Словник",
        "Übung": "Вправа",
        "Übungsübung": "Вправа",
        "Übersetzungsübung": "Вправа на переклад",
        "Wurzel": "Корінь",
        "Stamm": "Основа",
        "Präsensstamm": "Основа презенсу",
        "Futurstamm": "Основа футуру",
        "Endung": "Закінчення",
        "Präsens": "Теперішній час",
        "Futur": "Майбутній час",
        "Imperfekt": "Імперфект",
        "Imperativ": "Імператив",
        "Optativ": "Оптатив",
        "Wochenspruch": "Вірш тижня",
        "Erklärung": "Пояснення",
        "Bildung": "Утворення",
        "Gebrauch": "Вживання",
        "Quellen": "Джерела",
        "Abb.:": "Рис.:",
        "Bildquelle:": "Джерело зображення:",
        "Details": "Деталі"
    }
}

def translate_phrase(text, lang):
    """Translate individual terms or cells using the GRAMMAR_DICT."""
    if not text.strip():
        return text
    
    translated = text
    # Order keys by length descending to prevent substring issues
    keys_sorted = sorted(GRAMMAR_DICT[lang].keys(), key=len, reverse=True)
    
    # Process replacements
    for key in keys_sorted:
        val = GRAMMAR_DICT[lang][key]
        # Match word boundaries or exact strings
        pattern = re.escape(key)
        translated = re.sub(pattern, val, translated)
        
    return translated

def extract_sanskrit_anchors(text):
    """Extract Sanskrit words (Devanagari or IAST) to act as semantic anchors."""
    # Find Devanagari script blocks
    deva = re.findall(r'[\u0900-\u097F]+', text)
    # Find bold IAST words (like **rāmaḥ**)
    iast = re.findall(r'\*\*([a-zA-Zāīūṛṝḷḹṁṃḥṅñṭḍṇśṣ]+)\*\*', text)
    return set(deva + iast)

def split_into_sections(content):
    """Split markdown content into sections starting with ## or #."""
    lines = content.split('\n')
    sections = []
    current_sec = []
    current_title = "Frontmatter"
    
    for line in lines:
        if line.startswith('# ') or line.startswith('## ') or line.startswith('### '):
            if current_sec or current_title != "Frontmatter":
                sections.append((current_title, '\n'.join(current_sec)))
            current_title = line
            current_sec = []
        else:
            current_sec.append(line)
            
    sections.append((current_title, '\n'.join(current_sec)))
    return sections

def parse_blocks(section_text):
    """Parse section body into structural blocks."""
    lines = section_text.split('\n')
    blocks = []
    
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # Blank line
        if not line.strip():
            blocks.append({'type': 'blank', 'content': ''})
            i += 1
            continue
            
        # Container boundary
        if line.strip().startswith(':::') or line.strip().startswith('::::'):
            blocks.append({'type': 'container', 'content': line})
            i += 1
            continue
            
        # Horizontal rule
        if line.strip() in ['---', '***', '___']:
            blocks.append({'type': 'hr', 'content': line})
            i += 1
            continue
            
        # Image link
        if line.strip().startswith('![]'):
            blocks.append({'type': 'image', 'content': line})
            i += 1
            continue
            
        # Table row
        if line.strip().startswith('|'):
            blocks.append({'type': 'table_row', 'content': line})
            i += 1
            continue
            
        # Blockquote or List Item
        m_bq = re.match(r'^(\s*>\s*)(.*)$', line)
        m_li = re.match(r'^(\s*[-*+]\s+|\s*\d+\.\s+)(.*)$', line)
        
        if m_bq:
            prefix, rest = m_bq.groups()
            blocks.append({'type': 'blockquote', 'prefix': prefix, 'content': rest})
            i += 1
            continue
        elif m_li:
            prefix, rest = m_li.groups()
            blocks.append({'type': 'list_item', 'prefix': prefix, 'content': rest})
            i += 1
            continue
            
        # Regular paragraph (runs until empty line or block marker)
        para_lines = [line]
        i += 1
        while i < len(lines):
            next_line = lines[i]
            if not next_line.strip() or next_line.strip().startswith(':::') or next_line.strip().startswith('::::') or next_line.strip().startswith('|') or next_line.strip().startswith('![]') or re.match(r'^(\s*>\s*)', next_line) or re.match(r'^(\s*[-*+]\s+|\s*\d+\.\s+)', next_line):
                break
            para_lines.append(next_line)
            i += 1
            
        blocks.append({'type': 'paragraph', 'content': '\n'.join(para_lines)})
        
    return blocks

def align_and_merge_blocks(german_blocks, target_blocks, lang):
    """Align and merge translated content into the German layout skeleton."""
    # Filter out translatable blocks
    translatable_types = ['paragraph', 'list_item', 'blockquote', 'table_row']
    
    g_trans = [b for b in german_blocks if b['type'] in translatable_types]
    t_trans = [b for b in target_blocks if b['type'] in translatable_types]
    
    # Map G blocks to T blocks
    mapping = {} # G index -> T index
    matched_t = set()
    
    # Step 1: Align using Sanskrit anchor matches
    for g_idx, g_block in enumerate(g_trans):
        g_anchors = extract_sanskrit_anchors(g_block['content'])
        if not g_anchors:
            continue
            
        best_t_idx = -1
        best_score = 0
        
        for t_idx, t_block in enumerate(t_trans):
            if t_idx in matched_t:
                continue
            t_anchors = extract_sanskrit_anchors(t_block['content'])
            score = len(g_anchors.intersection(t_anchors))
            
            if score > best_score:
                best_score = score
                best_t_idx = t_idx
                
        if best_t_idx != -1 and best_score >= 1:
            mapping[g_idx] = best_t_idx
            matched_t.add(best_t_idx)
            
    # Step 2: Fallback to Relative Position / Index Matching for unmatched items
    for g_idx, g_block in enumerate(g_trans):
        if g_idx in mapping:
            continue
            
        # Find the first unmatched target block
        matched = False
        for t_idx in range(len(t_trans)):
            if t_idx not in matched_t:
                # Basic sanity check: match by relative index
                mapping[g_idx] = t_idx
                matched_t.add(t_idx)
                matched = True
                break
                
        # If no target block remains, it remains unmatched (meaning we use German fallback)
        if not matched:
            pass

    # Build the merged blocks list
    merged_blocks = []
    g_count = 0 # Track index in g_trans
    
    for g_block in german_blocks:
        if g_block['type'] not in translatable_types:
            # Layout blocks (containers, images, blank lines, hr)
            # Just copy the German block but translate image captions/attributions!
            content = g_block['content']
            if g_block['type'] == 'container' and 'Abb.:' in content:
                content = translate_phrase(content, lang)
            elif g_block['type'] == 'paragraph' and ('Abb.:' in content or 'Bildquelle:' in content):
                content = translate_phrase(content, lang)
            merged_blocks.append({'type': g_block['type'], 'content': content})
            continue
            
        # Match translatable block
        t_idx = mapping.get(g_count, -1)
        g_count += 1
        
        if t_idx == -1:
            # Fallback: keep German block but translate header terms/lists if applicable
            content = g_block['content']
            if g_block['type'] == 'list_item':
                content = translate_phrase(content, lang)
            merged_blocks.append({
                'type': g_block['type'],
                'prefix': g_block.get('prefix', ''),
                'content': content + " <!-- TODO: Fallback translation -->"
            })
            continue
            
        t_block = t_trans[t_idx]
        
        # Merge logic based on block type
        if g_block['type'] == 'table_row':
            # Highly precise cell-level layout synchronization
            g_cells = [c.strip() for c in g_block['content'].split('|')]
            t_cells = [c.strip() for c in t_block['content'].split('|')]
            
            merged_cells = []
            for col_idx, g_cell in enumerate(g_cells):
                if not g_cell:
                    merged_cells.append('')
                    continue
                
                # Check if cell has Devanagari or IAST and is identical
                g_anchors = extract_sanskrit_anchors(g_cell)
                
                # If cell is purely grammatical (like 'Singular', 'Dativ'), translate it
                if not g_anchors and any(k in g_cell for k in GRAMMAR_DICT[lang].keys()):
                    merged_cells.append(translate_phrase(g_cell, lang))
                # If target cell exists at the same index, use it
                elif col_idx < len(t_cells) and t_cells[col_idx]:
                    # Keep translated content but align layout (like [[br]])
                    merged_cells.append(t_cells[col_idx])
                else:
                    merged_cells.append(translate_phrase(g_cell, lang))
                    
            merged_content = ' | '.join(merged_cells).strip()
            # Ensure outer pipes are kept
            if g_block['content'].startswith('|') and not merged_content.startswith('|'):
                merged_content = '| ' + merged_content
            if g_block['content'].endswith('|') and not merged_content.endswith('|'):
                merged_content = merged_content + ' |'
                
            merged_blocks.append({
                'type': 'table_row',
                'content': merged_content
            })
            
        elif g_block['type'] == 'list_item':
            merged_blocks.append({
                'type': 'list_item',
                'prefix': g_block['prefix'],
                'content': t_block['content']
            })
            
        elif g_block['type'] == 'blockquote':
            merged_blocks.append({
                'type': 'blockquote',
                'prefix': g_block['prefix'],
                'content': t_block['content']
            })
            
        else: # paragraph
            merged_blocks.append({
                'type': 'paragraph',
                'content': t_block['content']
            })
            
    return merged_blocks

def sync_lesson(lesson_num, lang):
    """Synchronize layout of a specific lesson from German to target language."""
    filename = f"lektion{lesson_num:02d}.md"
    source_path = os.path.join(SOURCE_DIR, filename)
    target_dir = os.path.join(BASE_DIR, lang, "lektionen")
    target_path = os.path.join(target_dir, filename)
    
    if not os.path.exists(source_path):
        print(f"German source not found: {source_path}")
        return False
        
    print(f"[{lang}] Synchronizing layout for {filename}...")
    
    with open(source_path, 'r', encoding='utf-8') as f:
        german_content = f.read()
        
    # Read target translation or initialize placeholder
    if os.path.exists(target_path) and os.path.getsize(target_path) > 100:
        with open(target_path, 'r', encoding='utf-8') as f:
            target_content = f.read()
    else:
        print(f"  -> Target translation not found or empty. Initializing empty translation layout skeleton.")
        target_content = ""
        
    g_sections = split_into_sections(german_content)
    t_sections = split_into_sections(target_content)
    
    t_sec_dict = {} # heading -> body
    for t_title, t_body in t_sections:
        t_sec_dict[t_title.strip()] = t_body
        
    synced_sections = []
    
    for g_title, g_body in g_sections:
        # Match section title using simple regex matching for lesson prefixes (e.g. 25.1.)
        g_title_clean = g_title.strip()
        matched_t_body = None
        
        # Direct heading match
        if g_title_clean in t_sec_dict:
            matched_t_body = t_sec_dict[g_title_clean]
        else:
            # Prefix heading match (like matching 25.1. in '## 25.1. Formation...')
            m_g_prefix = re.match(r'^(#+)\s*(\d+\.\d+\.?\d*?\.?)\s*(.*)$', g_title_clean)
            if m_g_prefix:
                g_prefix = m_g_prefix.group(2)
                for t_title_key, t_body_val in t_sec_dict.items():
                    if g_prefix in t_title_key:
                        matched_t_body = t_body_val
                        break
                        
        # Translate heading title itself if no direct match exists
        if g_title_clean == "Frontmatter":
            synced_title = ""
        else:
            synced_title = translate_phrase(g_title_clean, lang)
            
        g_blocks = parse_blocks(g_body)
        t_blocks = parse_blocks(matched_t_body) if matched_t_body else []
        
        merged_blocks = align_and_merge_blocks(g_blocks, t_blocks, lang)
        
        # Reconstruct section body
        section_lines = []
        for b in merged_blocks:
            if b['type'] == 'blank':
                section_lines.append('')
            elif b['type'] in ['list_item', 'blockquote']:
                section_lines.append(f"{b['prefix']}{b['content']}")
            else:
                section_lines.append(b['content'])
                
        section_text = '\n'.join(section_lines)
        if synced_title:
            synced_sections.append(f"{synced_title}\n{section_text}")
        else:
            synced_sections.append(section_text)
            
    synced_content = '\n\n'.join(synced_sections)
    
    # Post-process: ensure proper VitePress newlines and formatting
    synced_content = re.sub(r'\n{3,}', '\n\n', synced_content)
    
    os.makedirs(target_dir, exist_ok=True)
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(synced_content)
        
    print(f"[{lang}] Finished layout sync for {filename}.")
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 sync_layouts.py <lesson_number_or_all> [language]")
        print("Example: python3 sync_layouts.py 27")
        print("Example: python3 sync_layouts.py 27 en")
        print("Example: python3 sync_layouts.py all")
        sys.exit(1)
        
    lesson_arg = sys.argv[1]
    lang_arg = sys.argv[2] if len(sys.argv) > 2 else None
    
    langs = [lang_arg] if lang_arg else LANGUAGES
    
    if lesson_arg.lower() == "all":
        lessons = list(range(1, 62))
    else:
        try:
            lessons = [int(lesson_arg)]
        except ValueError:
            print(f"Invalid lesson number: {lesson_arg}")
            sys.exit(1)
            
    print(f"Starting multi-language layout synchronization for lessons: {lessons}...")
    
    for l_num in lessons:
        for lang in langs:
            sync_lesson(l_num, lang)
            
    print("All requested layout synchronizations completed successfully!")

if __name__ == "__main__":
    main()

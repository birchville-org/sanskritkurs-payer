import os
import re
import sys

# Supported languages
LANGUAGES = [
    "en", "it", "es", "ru", "uk", "bg", "hi", "fr", "rm", "ta",
    "ar", "arc", "he", "zh", "la", "grc", "el", "fa", "akk", "cop", "fi", "hu"
]

# Base directories
BASE_DIR = "/Volumes/SanDisk1TB/proj/Payer/docs"
SOURCE_DIR = os.path.join(BASE_DIR, "lektionen")

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
    "fi": {
        "Maskulinum": "maskuliini",
        "Femininum": "feminiini",
        "Neutrum": "neutri",
        "Mask.": "mask.",
        "Fem.": "fem.",
        "Singular": "yksikkö",
        "Plural": "monikko",
        "Dual": "duaali",
        "Nominativ": "nominatiivi",
        "Akkusativ": "akkusatiivi",
        "Instrumentalis": "instrumentaali",
        "Dativ": "datiivi",
        "Ablativ": "ablatiivi",
        "Genetiv": "genetiivi",
        "Lokativ": "lokatiivi",
        "Vokativ": "vokatiivi",
        "Beispiel": "Esimerkki",
        "Beispiele": "Esimerkkejä",
        "Wortliste": "Sanasto",
        "Übung": "Harjoitus",
        "Übungsübung": "Harjoitus",
        "Übersetzungsübung": "Käännösharjoitus",
        "Wurzel": "Juuri",
        "Stamm": "Vartalo",
        "Präsensstamm": "Preesensvartalo",
        "Futurstamm": "Futuurivartalo",
        "Endung": "Pääte",
        "Präsens": "Preesens",
        "Futur": "Futuuri",
        "Imperfekt": "Imperfekti",
        "Imperativ": "Imperatiivi",
        "Optativ": "Optatiivi",
        "Wochenspruch": "Viikon mietelause",
        "Erklärung": "Selitys",
        "Bildung": "Muodostus",
        "Gebrauch": "Käyttö",
        "Quellen": "Lähteet",
        "Abb.:": "Kuva:",
        "Bildquelle:": "Kuvalähde:",
        "Details": "Tiedot"
    },
    "hu": {
        "Maskulinum": "hímnem",
        "Femininum": "nőnem",
        "Neutrum": "semlegesnem",
        "Mask.": "hímn.",
        "Fem.": "nőn.",
        "Singular": "egyes szám",
        "Plural": "többes szám",
        "Dual": "kettes szám (dualis)",
        "Nominativ": "alanyeset (nominativus)",
        "Akkusativ": "tárgyeset (accusativus)",
        "Instrumentalis": "eszközhatározó eset (instrumentalis)",
        "Dativ": "részes eset (dativus)",
        "Ablativ": "ablativus",
        "Genetiv": "birtokos eset (genitivus)",
        "Lokativ": "lokativus",
        "Vokativ": "megszólító eset (vocativus)",
        "Beispiel": "Példa",
        "Beispiele": "Példák",
        "Wortliste": "Szójegyzék",
        "Übung": "Gyakorlat",
        "Übungsübung": "Gyakorlat",
        "Übersetzungsübung": "Fordítási gyakorlat",
        "Wurzel": "Tő",
        "Stamm": "Tő",
        "Präsensstamm": "Jelen idejű tő",
        "Futurstamm": "Jövő idejű tő",
        "Endung": "Végződés",
        "Präsens": "Jelen idő",
        "Futur": "Jövő idő",
        "Imperfekt": "Múlt idő (imperfektum)",
        "Imperativ": "Felszólító mód",
        "Optativ": "Kívánó mód (optativus)",
        "Wochenspruch": "Heti mondás",
        "Erklärung": "Magyarázat",
        "Bildung": "Képzés",
        "Gebrauch": "Használat",
        "Quellen": "Források",
        "Abb.:": "Ábra:",
        "Bildquelle:": "Képforrás:",
        "Details": "Részletek"
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
    if not text.strip():
        return text
    if lang not in GRAMMAR_DICT:
        return text
    translated = text
    keys_sorted = sorted(GRAMMAR_DICT[lang].keys(), key=len, reverse=True)
    for key in keys_sorted:
        val = GRAMMAR_DICT[lang][key]
        pattern = re.escape(key)
        translated = re.sub(pattern, val, translated)
    return translated

def extract_sanskrit_anchors(text):
    deva = re.findall(r'[\u0900-\u097F]+', text)
    iast = re.findall(r'\*\*([a-zA-Zāīūṛṝḷḹṁṃḥṅñṭḍṇśṣ]+)\*\*', text)
    return set(deva + iast)

def block_similarity(b1, b2):
    t1, t2 = b1['type'], b2['type']
    if t1 != t2:
        if not ((t1 == 'paragraph' and t2 == 'list_item') or (t1 == 'list_item' and t2 == 'paragraph')):
            return 0.0
        
    c1 = re.sub(r'\s*<!-- TODO: Fallback translation -->', '', b1['content'].strip())
    c2 = re.sub(r'\s*<!-- TODO: Fallback translation -->', '', b2['content'].strip())
    
    # 1. Hallucination filter for target block
    hallucinations = {'center', 'media', 'note-box', 'notebox', 'laut-table', 'lauttable', 'deleteme-box', 'grammar-box'}
    if c2.lower() in hallucinations:
        return 0.0

    # 2. Number anchoring (like 1.1. or 1.)
    m1_num = re.match(r'^#*\s*(\d+\.(?:\d+\.)*)\s+', c1)
    m2_num = re.match(r'^#*\s*(\d+\.(?:\d+\.)*)\s+', c2)
    if m1_num and m2_num:
        if m1_num.group(1) == m2_num.group(1):
            return 1.0
        else:
            return 0.0 # Strict mismatch on numbered outlines

    score = 0.5
    
    a1 = extract_sanskrit_anchors(c1)
    a2 = extract_sanskrit_anchors(c2)
    if a1 and a2:
        score = max(score, len(a1.intersection(a2)) / max(len(a1), len(a2)))
        
    b1_bold = len(re.findall(r'\*\*[^\*]+\*\*', c1))
    b2_bold = len(re.findall(r'\*\*[^\*]+\*\*', c2))
    if b1_bold > 0 and b1_bold == b2_bold:
        score = max(score, 0.8)
        
    if b1['type'] == 'heading' and b2['type'] == 'heading':
        m1 = re.match(r'^(#+)', c1)
        m2 = re.match(r'^(#+)', c2)
        if m1 and m2 and m1.group(1) == m2.group(1):
            score = max(score, 0.8)

    # Length and Line Count Penalty
    l1 = len(c1)
    l2 = len(c2)
    if l1 > 0 and l2 > 0:
        len_ratio = min(l1, l2) / max(l1, l2)
        if len_ratio < 0.2:
            score *= 0.1
        elif len_ratio < 0.5:
            score *= 0.5
            
    lines1 = len(c1.split('\n'))
    lines2 = len(c2.split('\n'))
    if lines1 > 0 and lines2 > 0:
        line_ratio = min(lines1, lines2) / max(lines1, lines2)
        if line_ratio < 0.3:
            score *= 0.1

    return score

def parse_blocks(content):
    lines = content.split('\n')
    blocks = []
    i = 0
    in_frontmatter = False
    if len(lines) > 0 and lines[0] == '---':
        in_frontmatter = True
        fm_lines = ['---']
        i += 1
        while i < len(lines):
            fm_lines.append(lines[i])
            if lines[i] == '---':
                i += 1
                break
            i += 1
        blocks.append({'type': 'frontmatter', 'content': '\n'.join(fm_lines)})
        
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            blocks.append({'type': 'blank', 'content': ''})
            i += 1
            continue
        if line.strip().startswith(':::') or line.strip().startswith('::::'):
            blocks.append({'type': 'container', 'content': line})
            i += 1
            continue
        if line.strip() in ['---', '***', '___']:
            blocks.append({'type': 'hr', 'content': line})
            i += 1
            continue
        if line.strip().startswith('![]'):
            blocks.append({'type': 'image', 'content': line})
            i += 1
            continue
        if line.strip().startswith('|'):
            blocks.append({'type': 'table_row', 'content': line})
            i += 1
            continue
        if re.match(r'^#+\s+', line):
            blocks.append({'type': 'heading', 'content': line})
            i += 1
            continue
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
            
        para_lines = [line]
        i += 1
        while i < len(lines):
            next_line = lines[i]
            if not next_line.strip() or next_line.strip().startswith(':::') or next_line.strip().startswith('::::') or next_line.strip().startswith('|') or next_line.strip().startswith('![]') or re.match(r'^#+\s+', next_line) or re.match(r'^(\s*>\s*)', next_line) or re.match(r'^(\s*[-*+]\s+|\s*\d+\.\s+)', next_line):
                break
            para_lines.append(next_line)
            i += 1
        blocks.append({'type': 'paragraph', 'content': '\n'.join(para_lines)})
    return blocks

class BlockMatcher:
    def __init__(self, g_list, t_list):
        self.g = g_list
        self.t = t_list
        
    def match(self):
        n = len(self.g)
        m = len(self.t)
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                sim = block_similarity(self.g[i-1], self.t[j-1])
                match_score = dp[i-1][j-1] + sim if sim >= 0.1 else -1.0
                delete_score = dp[i-1][j]
                insert_score = dp[i][j-1]
                dp[i][j] = max(match_score, delete_score, insert_score)
                
        mapping = {}
        i, j = n, m
        while i > 0 and j > 0:
            sim = block_similarity(self.g[i-1], self.t[j-1])
            if sim >= 0.1 and dp[i][j] == dp[i-1][j-1] + sim:
                mapping[i-1] = j-1
                i -= 1
                j -= 1
            elif dp[i][j] == dp[i-1][j]:
                i -= 1
            else:
                j -= 1
        return mapping

def align_and_merge_blocks(german_blocks, target_blocks, lang):
    translatable_types = ['heading', 'paragraph', 'list_item', 'blockquote', 'table_row', 'frontmatter']
    g_trans = [b for b in german_blocks if b['type'] in translatable_types]
    t_trans = [b for b in target_blocks if b['type'] in translatable_types]
    
    mapping = {}
    if t_trans:
        matcher = BlockMatcher(g_trans, t_trans)
        mapping = matcher.match()
        print(f"Total G trans: {len(g_trans)}, T trans: {len(t_trans)}, Mapped: {len(mapping)}")
        
    unmatched = len(g_trans) - len(mapping)
    if len(g_trans) > 0 and unmatched / len(g_trans) > 0.05:
        print(f"[{lang}] WARNING: {unmatched}/{len(g_trans)} blocks unmatched. Might have Fallbacks.")

    merged_blocks = []
    g_count = 0
    
    for g_block in german_blocks:
        if g_block['type'] not in translatable_types:
            content = g_block['content']
            if g_block['type'] == 'container' and 'Abb.:' in content:
                content = translate_phrase(content, lang)
            elif g_block['type'] == 'paragraph' and ('Abb.:' in content or 'Bildquelle:' in content):
                content = translate_phrase(content, lang)
            merged_blocks.append({'type': g_block['type'], 'content': content})
            continue
            
        t_idx = mapping.get(g_count, -1)
        g_count += 1
        
        if t_idx == -1:
            content = g_block['content']
            if g_block['type'] in ['list_item', 'table_row']:
                content = translate_phrase(content, lang)
            elif g_block['type'] == 'heading' and g_block['content'].startswith('# '):
                # Dont append fallback to H1
                pass
            merged_blocks.append({
                'type': g_block['type'],
                'prefix': g_block.get('prefix', ''),
                'content': content + " <!-- TODO: Fallback translation -->"
            })
            continue
            
        t_block = t_trans[t_idx]
        
        if g_block['type'] == 'table_row':
            g_cells = [c.strip() for c in g_block['content'].split('|')]
            t_cells = [c.strip() for c in t_block['content'].split('|')]
            merged_cells = []
            g_raw_cells = g_block['content'].split('|')
            
            for col_idx, g_raw_cell in enumerate(g_raw_cells):
                if not g_raw_cell.strip():
                    merged_cells.append(g_raw_cell)
                    continue
                g_cell = g_raw_cell.strip()
                t_cell = ""
                if col_idx < len(t_cells):
                    t_cell = t_cells[col_idx].strip()
                g_anchors = extract_sanskrit_anchors(g_cell)
                cell_val = ""
                g_cell_clean = g_cell.replace(':br', '')
                has_deva = any(c for c in g_cell_clean if '\u0900' <= c <= '\u097f')
                has_latin = any(c for c in g_cell_clean if 'a' <= c.lower() <= 'z')
                if has_deva and not has_latin:
                    cell_val = g_cell
                elif ':br' in g_cell and any(c for c in g_cell if '\u0900' <= c <= '\u097f'):
                    cell_val = translate_phrase(g_cell, lang)
                elif not g_anchors and any(k in g_cell for k in GRAMMAR_DICT.get(lang, {}).keys()):
                    cell_val = translate_phrase(g_cell, lang)
                elif re.match(r'^[-—\sØ]+$', g_cell):
                    cell_val = g_cell
                elif t_cell:
                    cell_val = t_cell
                else:
                    cell_val = translate_phrase(g_cell, lang)
                merged_cells.append(f" {cell_val} ")
            merged_content = '|'.join(merged_cells)
            merged_blocks.append({'type': 'table_row', 'content': merged_content})
            
        elif g_block['type'] == 'frontmatter':
            merged_blocks.append({'type': 'frontmatter', 'content': g_block['content']})
            
        else:
            g_cell = g_block['content']
            g_cell_clean = g_cell.replace(':br', '')
            has_deva = any(c for c in g_cell_clean if '\u0900' <= c <= '\u097f')
            has_latin = any(c for c in g_cell_clean if 'a' <= c.lower() <= 'z')
            content = g_cell if (has_deva and not has_latin) else t_block['content']
            merged_blocks.append({
                'type': g_block['type'],
                'prefix': g_block.get('prefix', ''),
                'content': content
            })
            
    return merged_blocks

def sync_lesson(lesson_num, lang):
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
        
    if os.path.exists(target_path) and os.path.getsize(target_path) > 100:
        with open(target_path, 'r', encoding='utf-8') as f:
            target_content = f.read()
    else:
        target_content = ""
        
    g_blocks = parse_blocks(german_content)
    t_blocks = parse_blocks(target_content) if target_content else []
    
    merged_blocks = align_and_merge_blocks(g_blocks, t_blocks, lang)
    
    section_lines = []
    for b in merged_blocks:
        if b['type'] == 'blank':
            section_lines.append('')
        elif b['type'] in ['list_item', 'blockquote']:
            section_lines.append(f"{b['prefix']}{b['content']}")
        else:
            section_lines.append(b['content'])
            
    synced_content = '\n'.join(section_lines)
    synced_content = re.sub(r'\n{3,}', '\n\n', synced_content)
    
    orig_mtime = None
    if os.path.exists(target_path):
        orig_mtime = os.path.getmtime(target_path)
        orig_atime = os.path.getatime(target_path)
    else:
        orig_mtime = os.path.getmtime(source_path) - 3600
        orig_atime = orig_mtime

    os.makedirs(target_dir, exist_ok=True)
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(synced_content)
        
    if orig_mtime is not None:
        os.utime(target_path, (orig_atime, orig_mtime))
        
    return True

def main():
    if len(sys.argv) < 2:
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
            sys.exit(1)
            
    for l_num in lessons:
        for lang in langs:
            sync_lesson(l_num, lang)

if __name__ == "__main__":
    main()

import re
import os

LANG_MAP = {
    'de': {'source': 'Bildquelle', 'details': 'Details', 'path': ''},
    'en': {'source': 'Source', 'details': 'Details', 'path': '/en'},
    'it': {'source': 'Fonte', 'details': 'Dettagli', 'path': '/it'},
    'es': {'source': 'Fuente', 'details': 'Detalles', 'path': '/es'},
    'bg': {'source': 'Източник', 'details': 'Подробности', 'path': '/bg'},
    'ru': {'source': 'Источник', 'details': 'Подробности', 'path': '/ru'},
    'uk': {'source': 'Джерело', 'details': 'Подробиці', 'path': '/uk'}
}

def get_balanced_metadata_end(text, start_pos):
    bracket_level = 0
    for i in range(start_pos, len(text)):
        if text[i] == '[':
            bracket_level += 1
        elif text[i] == ']':
            bracket_level -= 1
            if bracket_level <= 0:
                return i + 1
    return -1

def deep_clean_file(filepath, lang):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Strip ALL existing media blocks and artifacts to start fresh
    content = re.sub(r'::: media\n?', '', content)
    content = re.sub(r':::\n?', '', content)
    
    # Remove any existing localized source links (Source: [Details](...))
    source_phrases = [m['source'] for m in LANG_MAP.values()] + ['Bildquelle']
    details_phrases = [m['details'] for m in LANG_MAP.values()] + ['Details']
    source_pattern = r'\s?\((' + '|'.join(source_phrases) + r'): \[(' + '|'.join(details_phrases) + r')\]\([^)]+\)\)'
    content = re.sub(source_pattern, '', content)

    # 2. Aggressively remove ALL [Bildquelle: ...] blocks
    while True:
        match = re.search(r'\\?\[Bildquelle[:.]', content)
        if not match: break
        start = match.start()
        start_bracket = content.find('[', start)
        end = get_balanced_metadata_end(content, start_bracket)
        if end != -1:
            content = content[:start] + content[end:]
        else:
            # Fallback for unclosed brackets
            next_nl = content.find('\n\n', start)
            if next_nl == -1: next_nl = len(content)
            content = content[:start] + content[next_nl:]

    # 3. Rebuild Media Blocks
    img_pattern = re.compile(r'!\[\]\(/images/([^)]+)\)')
    new_content = ""
    last_pos = 0

    for match in img_pattern.finditer(content):
        img_filename = match.group(1)
        lekt_id = os.path.splitext(img_filename)[0]
        img_tag = match.group(0)
        start, end = match.span()
        
        # Add text before image
        new_content += content[last_pos:start]
        
        # Detect caption in the following text
        search_limit = min(end + 1000, len(content))
        search_area = content[end:search_limit]
        
        # Stop at next image or header
        next_obj = re.search(r'(!\[\]\(/images/|\n## )', search_area)
        if next_obj: search_area = search_area[:next_obj.start()]
        
        # Collect lines that look like a caption
        caption_lines = []
        raw_lines = search_area.split('\n')
        for line in raw_lines:
            s_line = line.strip().replace('\xa0', ' ')
            if not s_line: continue
            
            # STOP CONDITIONS:
            # 1. Starts with a blockquote
            if s_line.startswith('>'): break
            # 2. Starts with a header (already handled by search_area, but double check)
            if s_line.startswith('#'): break
            # 3. Starts with a bullet point
            if s_line.startswith('*') or s_line.startswith('-'): break
            # 4. If we already have lines, and this one looks like a new term (ends with colon and followed by Sanskrit)
            if caption_lines and ':' in s_line and any(c >= '\u0900' and c <= '\u097f' for c in s_line):
                break
            
            # If it's the first line and doesn't start with Abb/Fig/Illu, it's NOT a caption
            if not caption_lines and not any(s_line.startswith(p) for p in ['Abb.:', 'Fig.:', 'Illustration:', 'Abb:', 'Fig:', 'Illustration']):
                break
                
            caption_lines.append(s_line)
        
        caption_str = " ".join(caption_lines).strip()
        # Clean up "Abb.: " prefix
        caption_str = re.sub(r'^(?:Abb\.|Fig\.|Illustration):?\s*', '', caption_str).strip()
        
        # Advance last_pos past the consumed caption lines
        if caption_lines:
            # We need to find how many lines of raw_lines we actually consumed
            # including empty ones in between.
            lines_to_consume = 0
            captions_found = 0
            for line in raw_lines:
                lines_to_consume += 1
                s_line = line.strip().replace('\xa0', ' ')
                if s_line:
                    captions_found += 1
                if captions_found == len(caption_lines):
                    break
            
            current_offset = 0
            for i in range(lines_to_consume):
                line = raw_lines[i]
                # Find the line exactly as it was split
                pos = search_area.find(line, current_offset)
                current_offset = pos + len(line)
                # Also consume the newline if it's not the last one
                if current_offset < len(search_area) and search_area[current_offset] == '\n':
                    current_offset += 1
            
            last_pos = end + current_offset
        else:
            last_pos = end

        # Construct new minimalist block
        source = LANG_MAP[lang]['source']
        details = LANG_MAP[lang]['details']
        l_path = LANG_MAP[lang]['path']
        
        final_caption = f"Abb.: {caption_str}. " if caption_str else "Abb.: "
        # Fix: Ensure no double space if caption_str is empty
        if not caption_str: final_caption = "Abb.: "
        
        new_block = f"\n\n::: media\n{img_tag}\n{final_caption}({source}: [{details}]({l_path}/licenses#{lekt_id}))\n:::\n\n"
        new_content += new_block

    new_content += content[last_pos:]
    
    # Final cleanup: double newlines and trailing spaces
    new_content = re.sub(r'\n{3,}', '\n\n', new_content)
    new_content = re.sub(r'[ \t]+\n', '\n', new_content)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

def main():
    docs_root = "/Volumes/SanDisk1TB/proj/Payer/docs"
    # Process all languages + German (root)
    for lang, info in LANG_MAP.items():
        if lang == 'de':
            target_dir = os.path.join(docs_root, "lektionen")
        else:
            target_dir = os.path.join(docs_root, lang, "lektionen")
            
        if not os.path.exists(target_dir): continue
        print(f"Deep Cleaning: {lang} in {target_dir}")
        for filename in os.listdir(target_dir):
            if filename.endswith(".md") and filename != "licenses.md":
                deep_clean_file(os.path.join(target_dir, filename), lang)

if __name__ == "__main__":
    main()

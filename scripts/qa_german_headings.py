import glob, os, re, sys

# Mapping of language codes to their native unicode ranges (if non-Latin)
NON_LATIN_SCRIPTS = {
    'ar': r'[\u0600-\u06FF]',
    'arc': r'[\u0700-\u074F]',
    'bg': r'[\u0400-\u04FF]',
    'ru': r'[\u0400-\u04FF]',
    'uk': r'[\u0400-\u04FF]',
    'cop': r'[\u2C80-\u2CFF]',
    'el': r'[\u0370-\u03FF\u1F00-\u1FFF]',
    'grc': r'[\u0370-\u03FF\u1F00-\u1FFF]',
    'fa': r'[\u0600-\u06FF]',
    'he': r'[\u0590-\u05FF]',
    'hi': r'[\u0900-\u097F]',
    'pa': r'[\u0A00-\u0A7F]',
    'ta': r'[\u0B80-\u0BFF]',
    'th': r'[\u0E00-\u0E7F]',
    'zh-CN': r'[\u4E00-\u9FFF]'
}

# Known German terms used in headings
GERMAN_HEADING_WORDS = [
    "Wortliste", "Übung", "Komposita", "Akkusativ", "Nominativ", "Infinitiv", 
    "Neutrum", "Präsensklasse", "Aorist", "Zahlen", "Endungen", "Verwendung", 
    "Wörterverzeichnis", "Partizip", "Schema", "Leseverstehen", "Übersetzungsübung",
    "Fragepronomen", "Demonstrativpronomina", "Adverb", "Plural", "Singular", "Passiv",
    "Steigerung", "Dual", "Nomina", "Maskulinum", "Femininum"
]
GERMAN_WORDS_REGEX = re.compile(r'\b(' + '|'.join(GERMAN_HEADING_WORDS) + r')\b', re.IGNORECASE)

def check_heading(lang, original_heading):
    # Remove Devanagari blocks
    cleaned = re.sub(r'⟪[^⟫]*⟫', '', original_heading)
    # Remove markup like *, _, #
    cleaned = re.sub(r'[*_#]', '', cleaned)
    # Remove chapter numbers like 5.3.1.
    cleaned = re.sub(r'\b\d+\.\d+(\.\d+)*\.?\b', '', cleaned)
    
    # Check non-Latin
    if lang in NON_LATIN_SCRIPTS:
        script_pattern = NON_LATIN_SCRIPTS[lang]
        # If it has Latin letters
        has_latin = bool(re.search(r'[A-Za-z]', cleaned))
        # But lacks the native script
        has_native = bool(re.search(script_pattern, cleaned))
        
        if has_latin and not has_native:
            # Let's verify it's not just a pure transliteration like "Dvandva" without a german word?
            # Actually, if it lacks native script entirely and has Latin, it's very suspicious.
            # But wait, sometimes it's just "Dvandva" (wait, dvandva would be in ⟪⟫ or transliteration).
            # If the LLM didn't translate it, it's bad.
            return True, "No native script found"
            
    # For Latin languages, or as a fallback for non-Latin
    if GERMAN_WORDS_REGEX.search(cleaned):
        match = GERMAN_WORDS_REGEX.search(cleaned).group(1)
        return True, f"German keyword '{match}' found"
        
    return False, ""

def main():
    if not os.path.exists('docs'):
        print("Must be run from project root")
        return

    suspicious_count = 0
    
    # Iterate over all languages
    for lang_dir in glob.glob('docs/*/'):
        lang = os.path.basename(os.path.normpath(lang_dir))
        if lang in ['lektionen', 'images', 'public', '.vitepress', 'arc_old']:
            continue
            
        print(f"\n--- Checking language: {lang} ---")
        
        md_files = glob.glob(f'{lang_dir}lektionen/*.md') + glob.glob(f'{lang_dir}*.md')
        lang_suspicious = 0
        
        for f in md_files:
            try:
                with open(f, 'r', encoding='utf-8') as file:
                    lines = file.readlines()
            except:
                continue
                
            for i, line in enumerate(lines):
                if line.startswith('#'):
                    is_suspicious, reason = check_heading(lang, line)
                    if is_suspicious:
                        # Print file path relative, line number, reason, and the heading
                        print(f"[{f}:{i+1}] ({reason}) -> {line.strip()}")
                        lang_suspicious += 1
                        suspicious_count += 1
                        
        if lang_suspicious == 0:
            print("  ✅ All clean!")
            
    print(f"\nTotal suspicious headings found: {suspicious_count}")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import os
import re
import argparse
import glob
from lingua import Language, LanguageDetectorBuilder

def clean_markdown(text):
    """Remove HTML, markdown tokens, and VitePress specific tags to get raw text for language detection."""
    # Remove YAML frontmatter & ::: deleteme-box blocks (to end of file)
    text = re.sub(r'^---.*?---\n', '', text, flags=re.DOTALL)
    text = re.sub(r':::\s*deleteme-box\b.*', '', text, flags=re.DOTALL)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Remove VitePress containers (::: info, ::: indent, etc.)
    text = re.sub(r'^:::.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'^::::.*$', '', text, flags=re.MULTILINE)
    # Remove markdown headers
    text = re.sub(r'^#+\s+', '', text, flags=re.MULTILINE)
    # Remove markdown blockquotes
    text = re.sub(r'^>\s+', '', text, flags=re.MULTILINE)
    # Remove list asterisks/dashes
    text = re.sub(r'^[\*\-]\s+', '', text, flags=re.MULTILINE)
    # Remove bold/italic markers
    text = re.sub(r'\*\*', '', text)
    text = re.sub(r'\*', '', text)
    text = re.sub(r'__', '', text)
    text = re.sub(r'_', '', text)
    # Remove inline code or code blocks
    text = re.sub(r'`[^`]+`', '', text)
    # Remove links [text](url)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    
    return text.strip()

def process_file(filepath, detector):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = content.split('\n\n')
    modified = False
    new_blocks = []

    for block in blocks:
        if "<!-- TODO: Fallback translation -->" in block:
            new_blocks.append(block)
            continue
            
        is_heading = bool(re.match(r'^#+\s+', block.strip()))
        clean_text = clean_markdown(block)
        
        # Remove punctuation to accurately count words (e.g. "Einsilbige," -> "Einsilbige")
        import string
        translator = str.maketrans('', '', string.punctuation + '„“«»()[]{}⟨⟩⟪⟫-–—')
        words = [w.translate(translator) for w in clean_text.split()]
        words = [w for w in words if w.isalpha()]
        
        min_words = 1 if is_heading else 4
        
        # Skip if block contains non-Latin target scripts (Cyrillic, Devanagari, Arabic, Hebrew, Thai, Tamil, Gurmukhi, Greek)
        if re.search(r'[\u0400-\u04FF\u0900-\u097F\u0600-\u06FF\u0590-\u05FF\u0E00-\u0E7F\u0B80-\u0BFF\u0A00-\u0A7F\u0370-\u03FF]', clean_text):
            new_blocks.append(block)
            continue

        if len(words) >= min_words:
            # We want to check if the block is predominantly German
            lang = detector.detect_language_of(clean_text)
            if lang == Language.GERMAN:
                print(f"    [GERMAN REMNANT DETECTED]: {clean_text[:60]}...")
                block = block + " <!-- TODO: Fallback translation -->"
                modified = True

        new_blocks.append(block)

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(new_blocks))
            
    return modified

def main():
    parser = argparse.ArgumentParser(description="Find German remnants in translated Markdown files and tag them for auto-repair.")
    parser.add_argument('-l', '--lang', required=True, help="Target language code (e.g. en)")
    args = parser.parse_args()

    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    target_dir = os.path.join(base_dir, 'docs', args.lang, 'lektionen')
    
    if not os.path.exists(target_dir):
        print(f"Error: Directory {target_dir} does not exist.")
        return

    print("Loading Lingua Language Detector (Restricted Languages)...")
    from lingua import Language
    detector = LanguageDetectorBuilder.from_languages(
        Language.GERMAN, Language.ENGLISH, Language.CHINESE, 
        Language.HINDI, Language.RUSSIAN, Language.SPANISH, 
        Language.FRENCH, Language.ITALIAN
    ).build()
    
    md_files = glob.glob(os.path.join(target_dir, '*.md'))
    md_files.sort()
    
    modified_count = 0
    for filepath in md_files:
        filename = os.path.basename(filepath)
        if process_file(filepath, detector):
            modified_count += 1
            print(f"  -> Flagged fallbacks in {filename}")
            
    print(f"\n[QA] Checked {len(md_files)} files. Flagged remnants in {modified_count} files.")
    
    # Return exit code based on whether modifications occurred (useful for wrapper script)
    # Exit 0 if clean, Exit 1 if remnants were found and tagged.
    import sys
    if modified_count > 0:
        sys.exit(1)
    else:
        sys.exit(0)

if __name__ == '__main__':
    main()

import os
import re
import glob

# Words that are highly indicative of English and unlikely to appear frequently in Italian, French, Spanish, Latin, Rumantsch, etc.
# Note: 'the' can sometimes appear in some names, but multiple occurrences strongly indicate English.
EN_MARKERS = re.compile(r'\b(the|this|that|these|those|what|where|when|which|how|why|because|although|therefore|however|would|could|should|shall|will|they|their|them)\b', re.IGNORECASE)

LOCALES_TO_SKIP = ['de', 'en']

def scan_file_for_english(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        
    in_frontmatter = False
    in_deleteme = False
    frontmatter_count = 0
    
    english_score = 0
    leaks = []
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped == '---' and i < 5:
            frontmatter_count += 1
            in_frontmatter = frontmatter_count == 1
            if frontmatter_count == 2:
                in_frontmatter = False
            continue
        if in_frontmatter:
            continue
            
        if '::: deleteme-box' in stripped or ':::deleteme-box' in stripped:
            in_deleteme = True
        if in_deleteme and stripped == ':::':
            in_deleteme = False
            continue
        if in_deleteme:
            continue
            
        # Skip pure html or markdown links/images
        if stripped.startswith('<') or stripped.startswith('!['):
            continue
            
        # Count English markers
        matches = EN_MARKERS.findall(line)
        if len(matches) >= 2: # At least 2 markers in a single line is highly suspicious
            leaks.append((i+1, line.strip(), matches))
            english_score += len(matches)
            
    return leaks, english_score

def main():
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "docs")
    locales = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d not in LOCALES_TO_SKIP and not d.startswith('.')]
    
    total_leaks = 0
    for loc in locales:
        loc_dir = os.path.join(base_dir, loc)
        files = glob.glob(os.path.join(loc_dir, '**/*.md'), recursive=True)
        for filepath in files:
            # Only scan lektionen
            if 'lektion' not in filepath.lower():
                continue
                
            leaks, score = scan_file_for_english(filepath)
            if score > 0:
                print(f"--- LEAK FOUND IN: {filepath} (Score: {score}) ---")
                for line_num, text, matches in leaks[:3]: # show first 3 lines
                    print(f"L{line_num}: {text} (Matches: {matches})")
                total_leaks += 1
                print()

    print(f"Total files with English leaks: {total_leaks}")

if __name__ == '__main__':
    main()

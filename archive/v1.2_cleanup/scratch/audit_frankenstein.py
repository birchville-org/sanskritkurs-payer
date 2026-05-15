import os
import re

# Regex for Devanagari range
DEVANAGARI_RANGE = r'[\u0900-\u097F]'
# Regex for Latin characters (simple)
LATIN_RANGE = r'[a-zA-Z]'
# Regex for Cyrillic characters
CYRILLIC_RANGE = r'[\u0400-\u04FF]'

def find_frankensteins(directory):
    results = {}
    
    # Combined regex to find words that contain mixed scripts
    # We look for continuous sequences of non-whitespace characters
    word_pattern = re.compile(r'\S+')
    
    for root, dirs, files in os.walk(directory):
        if 'node_modules' in dirs:
            dirs.remove('node_modules')
        if '.vitepress' in root and 'dist' in root:
            continue
            
        for filename in files:
            if filename.endswith('.md'):
                path = os.path.join(root, filename)
                rel_path = os.path.relpath(path, directory)
                
                with open(path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    
                for line_num, line in enumerate(lines, 1):
                    words = word_pattern.findall(line)
                    for word in words:
                        # Strip common punctuation from ends
                        clean_word = word.strip('.,;()[]{}!?"\'')
                        
                        has_deva = bool(re.search(DEVANAGARI_RANGE, clean_word))
                        has_lat = bool(re.search(LATIN_RANGE, clean_word))
                        has_cyr = bool(re.search(CYRILLIC_RANGE, clean_word))
                        
                        # Case 1: Devanagari mixed with Latin
                        # Case 2: Devanagari mixed with Cyrillic
                        # Case 3: Latin mixed with Cyrillic (in Sanskrit context usually a bug)
                        if (has_deva and has_lat) or (has_deva and has_cyr) or (has_lat and has_cyr):
                            if rel_path not in results:
                                results[rel_path] = []
                            results[rel_path].append({
                                'line': line_num,
                                'word': clean_word,
                                'context': line.strip()
                            })
    return results

if __name__ == "__main__":
    docs_dir = "/Volumes/SanDisk1TB/proj/Payer/docs"
    print(f"Scanning {docs_dir} for Frankenstein words...")
    
    audit_results = find_frankensteins(docs_dir)
    
    output_file = "/Volumes/SanDisk1TB/proj/Payer/scratch/frankenstein_audit.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Frankenstein Word Audit Results\n\n")
        f.write("This audit identifies words with mixed scripts (Devanagari, Latin, Cyrillic).\n\n")
        
        if not audit_results:
            f.write("No Frankenstein words found! Great job.\n")
        else:
            for file, matches in sorted(audit_results.items()):
                f.write(f"## {file}\n\n")
                f.write("| Line | Word | Context |\n")
                f.write("|------|------|---------|\n")
                for m in matches:
                    f.write(f"| {m['line']} | `{m['word']}` | `{m['context'][:100]}` |\n")
                f.write("\n")
                
    print(f"Audit complete. Results saved to {output_file}")

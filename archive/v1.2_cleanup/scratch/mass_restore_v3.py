import sys
import re
import difflib

def is_sanskrit(word):
    if not word: return False
    # Contains Devanagari
    if re.search(r'[\u0900-\u097F]', word):
        return True
    # Contains IAST diacritics
    if re.search(r'[āīūṛṝḷḹṅñṭḍṇśṣḥṃ]', word):
        return True
    # Catch mixed Devanagari/Cyrillic explicitly
    if re.search(r'[अ-ह][\u0400-\u04FF]|[\u0400-\u04FF][अ-ह]', word):
        return True
    return False

def restore_integrity(de_path, bg_path):
    with open(de_path, "r", encoding="utf-8") as f:
        de_content = f.read()
    with open(bg_path, "r", encoding="utf-8") as f:
        bg_content = f.read()

    de_lines = de_content.splitlines()
    bg_lines = bg_content.splitlines()

    new_bg_lines = []
    
    de_ptr = 0
    for l_idx, bg_line in enumerate(bg_lines):
        window_size = 15
        window = de_lines[max(0, de_ptr-window_size):min(len(de_lines), de_ptr+window_size)]
        best_de_line = ""
        best_score = 0
        best_idx = -1
        
        for i, de_l in enumerate(window):
            score = difflib.SequenceMatcher(None, bg_line, de_l).ratio()
            if score > best_score:
                best_score = score
                best_de_line = de_l
                best_idx = max(0, de_ptr-window_size) + i
        
        if best_score > 0.2: # Lower threshold to catch more
            bg_tokens = re.split(r'(\s+|[|,.()!?;:\"\'\[\]])', bg_line)
            de_tokens = re.split(r'(\s+|[|,.()!?;:\"\'\[\]])', best_de_line)
            
            de_sanskrit_tokens = [t for t in de_tokens if is_sanskrit(t)]
            de_tok_ptr = 0
            
            new_tokens = []
            for bg_t in bg_tokens:
                if is_sanskrit(bg_t):
                    if de_tok_ptr < len(de_sanskrit_tokens):
                        # DEBUG
                        if bg_t != de_sanskrit_tokens[de_tok_ptr]:
                            pass # print(f"Replacing {bg_t} with {de_sanskrit_tokens[de_tok_ptr]}")
                        new_tokens.append(de_sanskrit_tokens[de_tok_ptr])
                        de_tok_ptr += 1
                    else:
                        new_tokens.append(bg_t)
                else:
                    new_tokens.append(bg_t)
            new_bg_lines.append("".join(new_tokens))
            de_ptr = best_idx + 1
        else:
            new_bg_lines.append(bg_line)

    with open(bg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_bg_lines))

if __name__ == "__main__":
    restore_integrity("/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/lektion27.md", "/Volumes/SanDisk1TB/proj/Payer/docs/bg/lektionen/lektion27.md")
    print("Mass Restoration v3 finished for lektion27.md")

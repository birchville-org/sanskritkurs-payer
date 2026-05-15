import sys
import re
import difflib

def is_sanskrit(word):
    # Contains Devanagari or IAST diacritics
    if re.search(r'[\u0900-\u097F]', word):
        return True
    if re.search(r'[āīūṛṝḷḹṅñṭḍṇśṣḥṃ]', word):
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
    
    # Use a simple line-by-line alignment but allow for small drifts
    de_ptr = 0
    for bg_line in bg_lines:
        # Find best matching DE line in a window
        window = de_lines[max(0, de_ptr-5):min(len(de_lines), de_ptr+5)]
        best_de_line = ""
        best_score = 0
        for de_l in window:
            score = difflib.SequenceMatcher(None, bg_line, de_l).ratio()
            if score > best_score:
                best_score = score
                best_de_line = de_l
        
        if best_score > 0.4:
            # Try to restore Sanskrit tokens
            # Split into tokens (keeping delimiters)
            bg_tokens = re.split(r'(\s+|[|,.()!?;:\"\'\[\]])', bg_line)
            de_tokens = re.split(r'(\s+|[|,.()!?;:\"\'\[\]])', best_de_line)
            
            # Align tokens
            new_tokens = []
            for bg_t in bg_tokens:
                if is_sanskrit(bg_t) or re.search(r'[अ-ह][\u0400-\u04FF]|[\u0400-\u04FF][अ-ह]', bg_t):
                    # Find a matching token in de_tokens
                    found = False
                    for de_t in de_tokens:
                        # Character similarity (ignoring script for a moment)
                        # Actually, just find the token that has the same length or is similar
                        if is_sanskrit(de_t):
                            new_tokens.append(de_t)
                            found = True
                            break
                    if not found:
                        new_tokens.append(bg_t) # Keep if not found
                else:
                    new_tokens.append(bg_t)
            new_bg_lines.append("".join(new_tokens))
            # Update pointer
            for i, de_l in enumerate(de_lines):
                if de_l == best_de_line:
                    de_ptr = i + 1
                    break
        else:
            new_bg_lines.append(bg_line)

    with open(bg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_bg_lines))

if __name__ == "__main__":
    restore_integrity("/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/lektion27.md", "/Volumes/SanDisk1TB/proj/Payer/docs/bg/lektionen/lektion27.md")
    print("Mass Restoration pilot finished for lektion27.md")

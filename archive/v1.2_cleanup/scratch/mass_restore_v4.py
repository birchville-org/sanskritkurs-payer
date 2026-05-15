import sys
import re
import difflib

def is_mostly_sanskrit(word):
    if not word: return False
    # Count Sanskrit-like chars (Devanagari or diacritics)
    s_chars = len(re.findall(r'[\u0900-\u097Fāīūṛṝḷḹṅñṭḍṇśṣḥṃ]', word))
    # Count Cyrillic chars
    c_chars = len(re.findall(r'[\u0400-\u04FF]', word))
    
    if s_chars > 0 and s_chars >= c_chars:
        return True
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
    
    # Simple line alignment using difflib for robustness
    s = difflib.SequenceMatcher(None, de_lines, bg_lines)
    matches = s.get_matching_blocks()
    
    # We'll build a map of BG lines to DE lines
    bg_to_de = {}
    for m in matches:
        for i in range(m.size):
            bg_to_de[m.b + i] = m.a + i
            
    # For non-matches, try to find a similar line
    for i in range(len(bg_lines)):
        if i not in bg_to_de:
            # Search in a window
            best_a = -1
            best_score = 0
            for a in range(max(0, i-20), min(len(de_lines), i+20)):
                score = difflib.SequenceMatcher(None, bg_lines[i], de_lines[a]).ratio()
                if score > best_score:
                    best_score = score
                    best_a = a
            if best_score > 0.3:
                bg_to_de[i] = best_a

    for i, bg_line in enumerate(bg_lines):
        if i in bg_to_de:
            de_line = de_lines[bg_to_de[i]]
            
            # Split both into tokens (keeping delimiters)
            bg_tokens = re.split(r'(\s+|[|,.()!?;:\"\'\[\]])', bg_line)
            de_tokens = re.split(r'(\s+|[|,.()!?;:\"\'\[\]])', de_line)
            
            # Filter out whitespace-only tokens for alignment but keep them for reconstruction
            bg_tokens_val = [(idx, t) for idx, t in enumerate(bg_tokens) if t.strip() and t not in "|,.()!?;:\"\'[]"]
            de_tokens_val = [(idx, t) for idx, t in enumerate(de_tokens) if t.strip() and t not in "|,.()!?;:\"\'[]"]
            
            # Map bg tokens to de tokens
            new_bg_tokens = list(bg_tokens)
            for bg_idx, bg_t in bg_tokens_val:
                if is_mostly_sanskrit(bg_t):
                    # Find closest de_token in terms of position and similarity
                    best_de_t = None
                    best_sim = 0
                    for de_idx, de_t in de_tokens_val:
                        # Position similarity + Character similarity
                        pos_sim = 1.0 - abs(bg_idx/len(bg_tokens) - de_idx/len(de_tokens))
                        char_sim = difflib.SequenceMatcher(None, bg_t, de_t).ratio()
                        total_sim = pos_sim * 0.3 + char_sim * 0.7
                        if total_sim > best_sim:
                            best_sim = total_sim
                            best_de_t = de_t
                    
                    if best_sim > 0.4:
                        new_bg_tokens[bg_idx] = best_de_t
            
            new_bg_lines.append("".join(new_bg_tokens))
        else:
            new_bg_lines.append(bg_line)

    with open(bg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_bg_lines))

if __name__ == "__main__":
    restore_integrity("/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/lektion27.md", "/Volumes/SanDisk1TB/proj/Payer/docs/bg/lektionen/lektion27.md")
    print("Mass Restoration v4 (Token Similarity) finished for lektion27.md")

import sys
import re
import difflib
import os

def is_sanskrit_token(t):
    if not t: return False
    # Devanagari
    if re.search(r'[\u0900-\u097F]', t):
        return True
    # IAST with diacritics
    if re.search(r'[āīūṛṝḷḹṅñṭḍṇśṣḥṃ]', t):
        return True
    # Common IAST words that might not have diacritics but are Sanskrit
    # This is harder, but let's stick to the obvious ones first.
    return False

def restore_integrity(de_path, bg_path):
    if not os.path.exists(de_path): return
    with open(de_path, "r", encoding="utf-8") as f:
        de_content = f.read()
    with open(bg_path, "r", encoding="utf-8") as f:
        bg_content = f.read()

    de_lines = de_content.splitlines()
    bg_lines = bg_content.splitlines()

    new_bg_lines = []
    
    # Track alignment using difflib
    s = difflib.SequenceMatcher(None, de_lines, bg_lines)
    matches = s.get_matching_blocks()
    
    bg_to_de = {}
    for m in matches:
        for i in range(m.size):
            bg_to_de[m.b + i] = m.a + i

    # Fill gaps for alignment
    for i in range(len(bg_lines)):
        if i not in bg_to_de:
            best_a = -1
            best_score = 0
            # Narrower window for better accuracy
            for a in range(max(0, i-5), min(len(de_lines), i+5)):
                score = difflib.SequenceMatcher(None, bg_lines[i], de_lines[a]).ratio()
                if score > best_score:
                    best_score = score
                    best_a = a
            if best_score > 0.2:
                bg_to_de[i] = best_a

    for i, bg_line in enumerate(bg_lines):
        if i in bg_to_de:
            de_line = de_lines[bg_to_de[i]]
            
            # Split with delimiters
            bg_tokens = re.split(r'(\s+|[|,.()!?;:\"\'\[\]\-\*])', bg_line)
            de_tokens = re.split(r'(\s+|[|,.()!?;:\"\'\[\]\-\*])', de_line)
            
            # Identify Sanskrit tokens in DE
            de_s_indices = [idx for idx, t in enumerate(de_tokens) if is_sanskrit_token(t)]
            
            # If DE has Sanskrit, we need to find where they should be in BG
            if de_s_indices:
                # Use SequenceMatcher on tokens to align
                ts = difflib.SequenceMatcher(None, de_tokens, bg_tokens)
                t_matches = ts.get_matching_blocks()
                
                # Check which DE Sanskrit tokens were NOT matched
                matched_de_s = set()
                for tm in t_matches:
                    for j in range(tm.size):
                        if (tm.a + j) in de_s_indices:
                            matched_de_s.add(tm.a + j)
                
                unmatched_de_s = [idx for idx in de_s_indices if idx not in matched_de_s]
                
                # For unmatched DE Sanskrit, try to find "corrupted" BG equivalents
                new_bg_tokens = list(bg_tokens)
                for de_idx in unmatched_de_s:
                    de_t = de_tokens[de_idx]
                    # Find closest BG token that looks corrupted or is at similar position
                    rel_pos = de_idx / len(de_tokens)
                    bg_target_idx = int(rel_pos * len(bg_tokens))
                    
                    # Search around bg_target_idx for a token that is NOT whitespace/punct
                    # and might be a corruption (e.g. contains mixed script or is just phonetic)
                    best_bg_idx = -1
                    best_score = 0
                    for b_idx in range(max(0, bg_target_idx-3), min(len(bg_tokens), bg_target_idx+3)):
                        bg_t = bg_tokens[b_idx]
                        if not bg_t.strip() or bg_t in "|,.()!?;:\"\'[]-*": continue
                        
                        # A corruption is a token that has SOME similarity but is different
                        # or contains Devanagari mixed with Cyrillic
                        score = difflib.SequenceMatcher(None, de_t, bg_t).ratio()
                        if re.search(r'[\u0900-\u097F]', bg_t): score += 0.5 # Devanagari in BG is a strong signal
                        
                        if score > best_score:
                            best_score = score
                            best_bg_idx = b_idx
                    
                    if best_bg_idx != -1 and best_score > 0.3:
                        new_bg_tokens[best_bg_idx] = de_t
                
                new_bg_lines.append("".join(new_bg_tokens))
            else:
                new_bg_lines.append(bg_line)
        else:
            new_bg_lines.append(bg_line)

    with open(bg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_bg_lines))

if __name__ == "__main__":
    bg_dir = "/Volumes/SanDisk1TB/proj/Payer/docs/bg/lektionen/"
    de_dir = "/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/"
    for f in os.listdir(bg_dir):
        if f.endswith(".md"):
            restore_integrity(os.path.join(de_dir, f), os.path.join(bg_dir, f))

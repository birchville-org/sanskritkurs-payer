import sys
import re
import difflib
import os

def has_mixed_script(text):
    return re.search(r'[अ-ह][\u0400-\u04FF]|[\u0400-\u04FF][अ-ह]', text)

def is_sanskrit_token(t):
    if not t: return False
    if re.search(r'[\u0900-\u097F]', t): return True
    if re.search(r'[āīūṛṝḷḹṅñṭḍṇśṣḥṃ]', t): return True
    return False

def get_sanskrit_ratio(text):
    tokens = re.findall(r'\w+', text)
    if not tokens: return 0
    s_count = sum(1 for t in tokens if is_sanskrit_token(t))
    return s_count / len(tokens)

def restore_integrity(de_path, bg_path):
    if not os.path.exists(de_path): return
    with open(de_path, "r", encoding="utf-8") as f:
        de_lines = f.read().splitlines()
    with open(bg_path, "r", encoding="utf-8") as f:
        bg_lines = f.read().splitlines()

    # Align lines robustly
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
            for a in range(max(0, i-30), min(len(de_lines), i+30)):
                # Use a script-agnostic similarity check for alignment
                # e.g. check punctuation and whitespace pattern
                de_pat = re.sub(r'[^\s|,.()!?;:\"\'\[\]\-*]', 'X', de_lines[a])
                bg_pat = re.sub(r'[^\s|,.()!?;:\"\'\[\]\-*]', 'X', bg_lines[i])
                score = difflib.SequenceMatcher(None, de_pat, bg_pat).ratio()
                if score > best_score:
                    best_score = score
                    best_a = a
            if best_score > 0.4:
                bg_to_de[i] = best_a

    new_bg_lines = []
    for i, bg_l in enumerate(bg_lines):
        # RULE 1: If BG line has mixed script, replace with DE line if possible
        if has_mixed_script(bg_l):
            if i in bg_to_de:
                new_bg_lines.append(de_lines[bg_to_de[i]])
                continue
            else:
                # Try to find ANY DE line with same Sanskrit content
                # (This is a bit risky but good for corrupted files)
                pass

        # RULE 2: If DE line is High Sanskrit, use it
        if i in bg_to_de:
            de_l = de_lines[bg_to_de[i]]
            if get_sanskrit_ratio(de_l) > 0.5:
                new_bg_lines.append(de_l)
                continue

        new_bg_lines.append(bg_l)

    with open(bg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_bg_lines))

if __name__ == "__main__":
    bg_dir = "/Volumes/SanDisk1TB/proj/Payer/docs/bg/lektionen/"
    de_dir = "/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/"
    for f in os.listdir(bg_dir):
        if f.endswith(".md"):
            restore_integrity(os.path.join(de_dir, f), os.path.join(bg_dir, f))

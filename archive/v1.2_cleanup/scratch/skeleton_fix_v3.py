import sys
import re
import difflib
import os

def has_mixed_script(text):
    return re.search(r'[\u0900-\u097F][\u0400-\u04FF]|[\u0400-\u04FF][\u0900-\u097F]', text)

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

    s = difflib.SequenceMatcher(None, de_lines, bg_lines)
    matches = s.get_matching_blocks()
    
    bg_to_de = {}
    for m in matches:
        for i in range(m.size):
            bg_to_de[m.b + i] = m.a + i

    for i in range(len(bg_lines)):
        if i not in bg_to_de:
            best_a = -1
            best_score = 0
            # Increase window to 100 for better catch
            for a in range(max(0, i-100), min(len(de_lines), i+100)):
                de_pat = re.sub(r'[^\s|,.()!?;:\"\'\[\]\-*]', 'X', de_lines[a])
                bg_pat = re.sub(r'[^\s|,.()!?;:\"\'\[\]\-*]', 'X', bg_lines[i])
                score = difflib.SequenceMatcher(None, de_pat, bg_pat).ratio()
                if score > best_score:
                    best_score = score
                    best_a = a
            if best_score > 0.25:
                bg_to_de[i] = best_a

    new_bg_lines = []
    for i, bg_l in enumerate(bg_lines):
        # If local alignment failed but it's mixed, do a GLOBAL search in DE
        if has_mixed_script(bg_l) and i not in bg_to_de:
            best_global_a = -1
            best_global_score = 0
            bg_s_toks = [t for t in re.split(r'(\s+|[|,.()!?;:\"\'\[\]\-\*])', bg_l) if is_sanskrit_token(t)]
            for a_idx, de_l in enumerate(de_lines):
                de_s_toks = [t for t in re.split(r'(\s+|[|,.()!?;:\"\'\[\]\-\*])', de_l) if is_sanskrit_token(t)]
                if de_s_toks:
                    # Score based on matching Sanskrit tokens
                    matches = sum(1 for t in de_s_toks if any(difflib.SequenceMatcher(None, t, bt).ratio() > 0.7 for bt in bg_s_toks))
                    score = matches / max(len(de_s_toks), len(bg_s_toks), 1)
                    if score > best_global_score:
                        best_global_score = score
                        best_global_a = a_idx
            if best_global_score > 0.5:
                bg_to_de[i] = best_global_a

        if i in bg_to_de:
            de_l = de_lines[bg_to_de[i]]
            if has_mixed_script(bg_l) or get_sanskrit_ratio(de_l) > 0.35:
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

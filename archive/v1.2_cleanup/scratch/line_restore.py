import sys
import re
import difflib
import os

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

    # Align lines
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
            for a in range(max(0, i-10), min(len(de_lines), i+10)):
                score = difflib.SequenceMatcher(None, bg_lines[i], de_lines[a]).ratio()
                if score > best_score:
                    best_score = score
                    best_a = a
            if best_score > 0.2:
                bg_to_de[i] = best_a

    new_bg_lines = []
    for i, bg_l in enumerate(bg_lines):
        if i in bg_to_de:
            de_l = de_lines[bg_to_de[i]]
            
            # If the German line has Sanskrit tokens and Bulgarian line is different
            # or if German line is VERY Sanskrit, we overwrite.
            # Special case: if German line has >0 Sanskrit, and Bulgarian line has mixed scripts.
            de_ratio = get_sanskrit_ratio(de_l)
            bg_has_mixed = re.search(r'[अ-ह][\u0400-\u04FF]|[\u0400-\u04FF][अ-ह]', bg_l)
            
            if de_ratio > 0.1 or bg_has_mixed:
                # If the line is mostly a translation (quotes), we shouldn't overwrite the whole line.
                # BUT if it's a Sanskrit block (starts with > or * or is in a table), we can.
                if de_l.strip().startswith(">") or de_l.strip().startswith("*") or de_l.strip().startswith("|") or de_ratio > 0.5:
                    new_bg_lines.append(de_l)
                else:
                    # Token-level replacement
                    bg_toks = re.split(r'(\s+|[|,.()!?;:\"\'\[\]\-\*])', bg_l)
                    de_toks = re.split(r'(\s+|[|,.()!?;:\"\'\[\]\-\*])', de_l)
                    de_s_toks = [t for t in de_toks if is_sanskrit_token(t)]
                    dt_ptr = 0
                    new_toks = []
                    for bt in bg_toks:
                        if is_sanskrit_token(bt) or (re.search(r'[\u0400-\u04FF]', bt) and de_ratio > 0):
                            if dt_ptr < len(de_s_toks):
                                new_toks.append(de_s_toks[dt_ptr])
                                dt_ptr += 1
                            else:
                                new_toks.append(bt)
                        else:
                            new_toks.append(bt)
                    new_bg_lines.append("".join(new_toks))
            else:
                new_bg_lines.append(bg_l)
        else:
            new_bg_lines.append(bg_l)

    with open(bg_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_bg_lines))

if __name__ == "__main__":
    bg_dir = "/Volumes/SanDisk1TB/proj/Payer/docs/bg/lektionen/"
    de_dir = "/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/"
    for f in os.listdir(bg_dir):
        if f.endswith(".md"):
            restore_integrity(os.path.join(de_dir, f), os.path.join(bg_dir, f))

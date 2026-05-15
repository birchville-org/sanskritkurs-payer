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

def get_anchor(line):
    line = line.strip()
    if not line: return None
    if line.startswith("#"): return "header"
    if line.startswith("*"): return "list"
    if line.startswith(">"): return "quote"
    if line.startswith("|"): return "table"
    return "text"

def restore_integrity(de_path, bg_path):
    if not os.path.exists(de_path): return
    with open(de_path, "r", encoding="utf-8") as f:
        de_lines = f.read().splitlines()
    with open(bg_path, "r", encoding="utf-8") as f:
        bg_lines = f.read().splitlines()

    # Anchor-based alignment
    de_anchors = [(i, get_anchor(l), l) for i, l in enumerate(de_lines) if get_anchor(l) in ["header", "list", "quote", "table"]]
    bg_anchors = [(i, get_anchor(l), l) for i, l in enumerate(bg_lines) if get_anchor(l) in ["header", "list", "quote", "table"]]
    
    # Align anchor lines themselves using similarity
    bg_to_de = {}
    de_idx = 0
    for bg_idx, bg_type, bg_l in bg_anchors:
        # Search for best matching anchor in DE window
        best_a = -1
        best_score = 0
        for a_idx, de_type, de_l in de_anchors:
            if de_type == bg_type:
                score = difflib.SequenceMatcher(None, bg_l, de_l).ratio()
                if score > best_score:
                    best_score = score
                    best_a = a_idx
        if best_score > 0.15:
            bg_to_de[bg_idx] = best_a

    # Fill in the gaps between anchors
    for i in range(len(bg_lines)):
        if i not in bg_to_de:
            # Find closest anchors
            prev_bg = [idx for idx in bg_to_de.keys() if idx < i]
            next_bg = [idx for idx in bg_to_de.keys() if idx > i]
            
            de_range_start = bg_to_de[max(prev_bg)] + 1 if prev_bg else 0
            de_range_end = bg_to_de[min(next_bg)] if next_bg else len(de_lines)
            
            best_a = -1
            best_score = 0
            for a in range(de_range_start, de_range_end):
                score = difflib.SequenceMatcher(None, bg_lines[i], de_lines[a]).ratio()
                if score > best_score:
                    best_score = score
                    best_a = a
            if best_score > 0.1:
                bg_to_de[i] = best_a

    new_bg_lines = []
    for i, bg_l in enumerate(bg_lines):
        if i in bg_to_de:
            de_l = de_lines[bg_to_de[i]]
            de_ratio = get_sanskrit_ratio(de_l)
            
            # FORCE OVERWRITE for high-Sanskrit or anchor-matched lines that are clearly Sanskrit
            if de_ratio > 0.3 or bg_l.strip().startswith("*") or bg_l.strip().startswith(">"):
                # If German has Sanskrit and Bulgarian looks phonetic or mixed
                if de_ratio > 0:
                    new_bg_lines.append(de_l)
                else:
                    new_bg_lines.append(bg_l)
            elif re.search(r'[अ-ह][\u0400-\u04FF]|[\u0400-\u04FF][अ-ह]', bg_l):
                new_bg_lines.append(de_l)
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

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
        de_content = f.read()
    with open(bg_path, "r", encoding="utf-8") as f:
        bg_content = f.read()

    # Split into paragraphs/blocks (separated by double newlines)
    de_blocks = de_content.split("\n\n")
    bg_blocks = bg_content.split("\n\n")

    # Align blocks
    s = difflib.SequenceMatcher(None, de_blocks, bg_blocks)
    matches = s.get_matching_blocks()
    
    bg_to_de = {}
    for m in matches:
        for i in range(m.size):
            bg_to_de[m.b + i] = m.a + i

    # Fallback alignment for changed blocks
    for i in range(len(bg_blocks)):
        if i not in bg_to_de:
            best_a = -1
            best_score = 0
            for a in range(max(0, i-5), min(len(de_blocks), i+5)):
                score = difflib.SequenceMatcher(None, bg_blocks[i], de_blocks[a]).ratio()
                if score > best_score:
                    best_score = score
                    best_a = a
            if best_score > 0.2:
                bg_to_de[i] = best_a

    new_bg_blocks = []
    for i, bg_b in enumerate(bg_blocks):
        if i in bg_to_de:
            de_b = de_blocks[bg_to_de[i]]
            
            # If the German block is VERY Sanskrit, and Bulgarian is mixed/phonetic
            # we overwrite the Bulgarian one.
            if get_sanskrit_ratio(de_b) > 0.3:
                # Overwrite
                new_bg_blocks.append(de_b)
            else:
                # Otherwise, try token-level restoration (from deep_restore)
                bg_lines = bg_b.splitlines()
                de_lines = de_b.splitlines()
                # Simplified line-by-line for within block
                res_lines = []
                for j, bl in enumerate(bg_lines):
                    if j < len(de_lines):
                        dl = de_lines[j]
                        # Replace tokens
                        bg_toks = re.split(r'(\s+|[|,.()!?;:\"\'\[\]\-\*])', bl)
                        de_toks = re.split(r'(\s+|[|,.()!?;:\"\'\[\]\-\*])', dl)
                        de_s_toks = [t for t in de_toks if is_sanskrit_token(t)]
                        dt_ptr = 0
                        new_toks = []
                        for bt in bg_toks:
                            if is_sanskrit_token(bt) or (re.search(r'[\u0400-\u04FF]', bt) and dt_ptr < len(de_s_toks) and get_sanskrit_ratio(dl) > 0.2):
                                # If it looks like a corruption or BG token in a Sanskrit line
                                if dt_ptr < len(de_s_toks):
                                    new_toks.append(de_s_toks[dt_ptr])
                                    dt_ptr += 1
                                else:
                                    new_toks.append(bt)
                            else:
                                new_toks.append(bt)
                        res_lines.append("".join(new_toks))
                    else:
                        res_lines.append(bl)
                new_bg_blocks.append("\n".join(res_lines))
        else:
            new_bg_blocks.append(bg_b)

    with open(bg_path, "w", encoding="utf-8") as f:
        f.write("\n\n".join(new_bg_blocks))

if __name__ == "__main__":
    bg_dir = "/Volumes/SanDisk1TB/proj/Payer/docs/bg/lektionen/"
    de_dir = "/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/"
    for f in os.listdir(bg_dir):
        if f.endswith(".md"):
            restore_integrity(os.path.join(de_dir, f), os.path.join(bg_dir, f))

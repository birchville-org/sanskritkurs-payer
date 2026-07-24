import os
import re
import argparse

def get_lektion_name(lang, base_dir):
    # Try to find the translated word for "Lektion" from lektion02.md heading
    path = os.path.join(base_dir, lang, "lektionen", "lektion02.md")
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                m = re.match(r'^#\s+([^\d]+)\s+\d+', line)
                if m:
                    return m.group(1).strip()
    return 'Lesson'

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--lang', required=True)
    args = parser.parse_args()
    
    lang = args.lang
    base_dir = "/Volumes/SanDisk1TB/proj/Payer/docs"
    
    # 1. Read master German wortliste.md
    with open(os.path.join(base_dir, "lektionen", "wortliste.md"), 'r', encoding='utf-8') as f:
        master_content = f.read()
        
    header_match = re.split(r'^## Lektion \d+', master_content, flags=re.MULTILINE)
    german_header = header_match[0]
    
    headers = {
        'en': """---
outline: 2
---

::: deleteme-box
**Citation Style & Rights**

:::
# Word List (Complete Overview)

*All new words from the course in the order of their introduction, with thematic explanations.*""",
        'el': """---
outline: 2
---

::: deleteme-box
**Τρόπος αναφοράς & Δικαιώματα**

:::
# Λίστα λέξεων (Γενική επισκόπηση)

*Όλες οι νέες λέξεις από το μάθημα με τη σειρά εισαγωγής τους, με θεματικές επεξηγήσεις.*"""
    }
    
    header = headers.get(lang)
    if not header:
        header = headers.get('en', german_header)
        
    # 2. Extract lesson sections structure from German wortliste.md
    master_sections = []
    current_lektion = None
    current_lines = []
    
    for line in master_content.splitlines():
        m = re.match(r'^## Lektion (\d+)', line)
        if m:
            if current_lektion is not None:
                master_sections.append((current_lektion, "\n".join(current_lines).strip()))
            current_lektion = int(m.group(1))
            current_lines = []
        elif current_lektion is not None:
            current_lines.append(line)
    if current_lektion is not None:
        master_sections.append((current_lektion, "\n".join(current_lines).strip()))
        
    # 3. Read German lessons to determine vocabulary heading index in each lesson
    lesson_sections = {}
    for i in range(1, 62):
        de_path = os.path.join(base_dir, "lektionen", f"lektion{i:02d}.md")
        target_path = os.path.join(base_dir, lang, "lektionen", f"lektion{i:02d}.md")
        if not os.path.exists(de_path) or not os.path.exists(target_path):
            continue
            
        with open(de_path, 'r', encoding='utf-8') as f:
            de_content = f.read()
        with open(target_path, 'r', encoding='utf-8') as f:
            target_content = f.read()
            
        # Find all ## headings in German lesson
        de_lines = de_content.splitlines()
        de_headings = []
        for idx, line in enumerate(de_lines):
            if re.match(r'^##\s', line):
                de_headings.append((idx, line))
                
        # Find heading containing "Wortliste"
        vocab_idx = -1
        for h_idx, (line_num, heading_text) in enumerate(de_headings):
            if "Wortliste" in heading_text:
                vocab_idx = h_idx
                break
                
        if vocab_idx == -1:
            continue
            
        # Find all ## headings in target lesson
        target_lines = target_content.splitlines()
        target_headings = []
        for idx, line in enumerate(target_lines):
            if re.match(r'^##\s', line):
                target_headings.append((idx, line))
                
        if vocab_idx < len(target_headings):
            start_line_idx = target_headings[vocab_idx][0] + 1
            # Go until next ## heading or end of file
            end_line_idx = len(target_lines)
            if vocab_idx + 1 < len(target_headings):
                end_line_idx = target_headings[vocab_idx + 1][0]
                
            vocab_content = "\n".join(target_lines[start_line_idx:end_line_idx]).strip()
            lesson_sections[i] = vocab_content
            
    # 4. Extract and translate image credits from German wortliste.md
    image_credit_keys = []
    for line in master_content.splitlines():
        # Match pattern: **lekt5210**: ⟪खिलः⟫ Tambhol... or **lekt5210**: Tambhol...
        m = re.match(r'^\*\*(lekt\d{4})\*\*:\s*(⟪[^⟫]+⟫)?\s*(.*)', line)
        if m:
            key = m.group(1)
            sanskrit = m.group(2)
            desc = m.group(3)
            # Find lesson number from key (lektXXYY -> XX)
            lek_num = int(key[4:6])
            image_credit_keys.append((key, sanskrit, desc, lek_num, line))
            
    # For each key, find the translated line in the target lesson
    translated_credits = {}
    for key, sanskrit, desc, lek_num, orig_line in image_credit_keys:
        path = os.path.join(base_dir, lang, "lektionen", f"lektion{lek_num:02d}.md")
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip().startswith(f"**{key}"):
                        target_desc = re.sub(r'^\*\*?' + key + r'[:*]*\s*', '', line.strip())
                        sansk_prefix = sanskrit + " " if sanskrit else ""
                        translated_credits[key] = f"**{key}**: {sansk_prefix}{target_desc}"
                        break
                        
    # 5. Assemble the translated wortliste.md
    lektion_word = get_lektion_name(lang, base_dir)
    print(f"Using translation for 'Lektion': '{lektion_word}'")
    
    output_lines = [header.strip()]
    
    for lek_num, _ in master_sections:
        if lang == 'zh-CN':
            heading = f"## 第 {lek_num} 课"
        elif lang == 'th':
            heading = f"## บทที่ {lek_num}"
        else:
            heading = f"## {lektion_word} {lek_num}"
            
        output_lines.append("\n\n" + heading + "\n")
        
        if lek_num in lesson_sections:
            output_lines.append(lesson_sections[lek_num])
        else:
            print(f"Warning: Lektion {lek_num} not found/extracted in {lang} lessons.")
            
    # Append translated image credits to output_lines
    if image_credit_keys:
        output_lines.append("\n") # Separate from last lesson
        for key, sanskrit, desc, lek_num, orig_line in image_credit_keys:
            if key in translated_credits:
                output_lines.append("\n" + translated_credits[key])
            else:
                output_lines.append("\n" + orig_line)
                
    output_content = "\n".join(output_lines) + "\n"
    
    target_path = os.path.join(base_dir, lang, "lektionen", "wortliste.md")
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(output_content)
    print(f"Successfully assembled and wrote {target_path}")

if __name__ == "__main__":
    main()

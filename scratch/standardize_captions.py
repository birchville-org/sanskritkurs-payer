import re
import os

def standardize_images(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        match = re.search(r'!\[\]\(/images/(lekt(\d+))\.(?:jpg|png|gif)\)', line)
        if match:
            img_full_id = match.group(1)
            img_id = match.group(2)
            
            caption_lines = []
            j = i + 1
            while j < len(lines):
                next_line = lines[j].strip()
                # Stop if blank line, new header, or container starts
                if not next_line or next_line.startswith('#') or next_line.startswith(':::') or next_line.startswith('>'):
                    break
                
                # Skip source lines
                if next_line.startswith('[Bildquelle:') or next_line.startswith('[Quelle:') or next_line.startswith('\[Bildquelle:'):
                    j += 1
                    continue
                
                caption_lines.append(next_line.strip(' -. '))
                j += 1
            
            if not caption_lines:
                caption_lines = [img_full_id]
                
            # Formatting the caption
            first = caption_lines[0]
            if first.startswith('Abb.:'):
                label = first[5:].strip()
                rest = " ".join(caption_lines[1:])
                if rest:
                    final_caption = f"Abb.: {label} • {rest}"
                else:
                    final_caption = f"Abb.: {label}"
            else:
                final_caption = "Abb.: " + " • ".join(caption_lines)
            
            new_lines.append("::: media\n")
            new_lines.append(f"![](/images/{img_full_id}.jpg)\n")
            new_lines.append(f"{final_caption}\n")
            new_lines.append(f"(Bildquelle: [Details](/licenses#lekt{img_id}))\n")
            new_lines.append(":::\n")
            
            i = j
        else:
            new_lines.append(line)
            i += 1
            
    return "".join(new_lines)

target_file = '/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/lektion51.md'
updated_content = standardize_images(target_file)

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(updated_content)

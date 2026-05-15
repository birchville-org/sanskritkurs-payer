import re
import sys

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    sources = []
    i = 0
    while i < len(lines):
        line = lines[i]
        # Match image line
        match = re.search(r'!\[\]\(/images/(lekt(\d+))\.(?:jpg|png|gif)\)', line)
        if match:
            img_full_id = match.group(1)
            img_id = match.group(2)
            
            # Find caption lines: everything until a blank line or start of a block
            caption_lines = []
            source_info = None
            j = i + 1
            while j < len(lines):
                next_raw = lines[j]
                next_line = next_raw.strip()
                if not next_line or next_line.startswith('#') or next_line.startswith(':::') or next_line.startswith('>') or '![]' in next_line:
                    break
                
                # Skip detailed source lines if they are already in the deleteme-box pattern
                if next_line.startswith('[Bildquelle:') or next_line.startswith('[Quelle:') or next_line.startswith('\[Bildquelle:'):
                    source_info = next_line
                    j += 1
                    continue
                
                caption_lines.append(next_line.strip(' -. '))
                j += 1
            
            if not caption_lines:
                caption_lines = [img_full_id]
            
            # Formatting
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
            
            if source_info:
                sources.append(f"**lekt{img_id}:** {source_info}")
            
            i = j
        else:
            new_lines.append(line)
            i += 1
            
    if sources:
        print("\n### Quellen für deleteme-box:")
        for s in sources:
            print(s)
            
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

if __name__ == "__main__":
    process_file(sys.argv[1])

import os
import re
import sys

def strip_non_devanagari(caption):
    # Strips typical German translations in parentheses or trailing descriptions from the visible caption
    # Standard format: Abb.: [Devanagari] (with any German/English text removed)
    caption = caption.strip()
    if not caption.startswith("Abb.:") and not caption.startswith("Abb. :"):
        return caption
        
    prefix = "Abb.:"
    body = caption[caption.find(":")+1:].strip()
    
    # Strip any trailing parenthesis containing German translations (like (उदर n. "Bauch"))
    # Also strip any German translation parts separated by = or - or with Latin characters
    body = re.sub(r'\s*\([^)]*[a-zA-ZäöüßÄÖÜ][^)]*\)', '', body)
    
    # If there is a '=' or '-' or '/' followed by Latin chars, let's split and keep only the Devanagari part
    parts = re.split(r'\s*(?:=|-|/)\s*', body)
    clean_parts = []
    for part in parts:
        if re.search(r'[\u0900-\u097F]', part):
            part_cleaned = re.sub(r'[a-zA-Z].*$', '', part).strip()
            if part_cleaned:
                clean_parts.append(part_cleaned)
                
    if clean_parts:
        body = " ".join(clean_parts)
    else:
        body = re.sub(r'[a-zA-Z].*$', '', body).strip()
        
    return f"{prefix} {body}".strip()

def migrate_images_in_file(filepath, dry_run=True):
    print(f"\nProcessing {filepath}...")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    lines = content.split('\n')
    new_lines = []
    
    i = 0
    collected_sources = []
    changed = False
    
    has_sources_box = False
    for line in lines:
        if '### Quellen' in line:
            has_sources_box = True
            break
            
    while i < len(lines):
        line = lines[i]
        
        # Match standard markdown image tag
        image_match = re.match(r'^\s*!\[\]\((/images/(lekt\d{4})\.jpg)\)\s*$', line)
        if image_match:
            is_inside_media = False
            for prev_line in reversed(new_lines[-3:]):
                if '::: media' in prev_line:
                    is_inside_media = True
                    break
            
            if is_inside_media:
                new_lines.append(line)
                i += 1
                continue
                
            image_url = image_match.group(1)
            image_id = image_match.group(2)
            
            caption_line = ""
            attribution_lines = []
            
            next_idx = i + 1
            # Skip empty lines immediately after image
            while next_idx < len(lines) and not lines[next_idx].strip():
                next_idx += 1
                
            # Check if next line is caption
            if next_idx < len(lines) and (lines[next_idx].strip().startswith("Abb.:") or lines[next_idx].strip().startswith("Abb. :")):
                caption_line = lines[next_idx].strip()
                next_idx += 1
                
                # Check for attribution lines directly after the caption
                while next_idx < len(lines):
                    next_line = lines[next_idx].strip()
                    if not next_line:
                        # Empty line signals the end of the attribution!
                        next_idx += 1
                        break
                    if next_line.startswith("###") or next_line.startswith("##") or next_line.startswith("![]") or next_line.startswith(":::"):
                        break
                    attribution_lines.append(lines[next_idx].strip())
                    next_idx += 1
            
            clean_caption = strip_non_devanagari(caption_line) if caption_line else ""
            full_attr_text = " ".join(attribution_lines)
            full_attr_text = full_attr_text.replace('\\[', '[').replace('\\]', ']')
            
            if full_attr_text:
                collected_sources.append((image_id, full_attr_text))
            
            media_block = []
            media_block.append("::: media")
            media_block.append(f"![]{image_url}")
            if clean_caption:
                media_block.append(clean_caption)
            media_block.append(f"(Bildquelle: [Details](/licenses#{image_id}))")
            media_block.append(":::")
            
            new_lines.extend(media_block)
            changed = True
            print(f"  Merged legacy image {image_id} into ::: media container.")
            i = next_idx
        else:
            new_lines.append(line)
            i += 1
            
    if collected_sources and not has_sources_box:
        if new_lines and new_lines[-1].strip():
            new_lines.append("")
            
        new_lines.append("::: deleteme-box")
        new_lines.append("### Quellen")
        new_lines.append("")
        for img_id, attr_text in collected_sources:
            new_lines.append(f"**{img_id}:** {attr_text}")
            new_lines.append("")
        new_lines.append(":::")
        changed = True
        print(f"  Added sources to deleteme-box at the bottom.")
        
    if changed and not dry_run:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("\n".join(new_lines))
        print("  Changes written successfully!")
    else:
        print("  Dry-run active or no changes needed.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 scholarly_image_migrator.py <filepath> [--apply]")
        sys.exit(1)
        
    path = sys.argv[1]
    dry_run = "--apply" not in sys.argv
    
    if os.path.isfile(path):
        migrate_images_in_file(path, dry_run)
    else:
        for root, dirs, files in os.walk(path):
            for filename in files:
                if filename.endswith(".md") and "lektion" in filename:
                    filepath = os.path.join(root, filename)
                    if "bak" in filepath or "experiment" in filepath or "refactored" in filepath:
                        continue
                    migrate_images_in_file(filepath, dry_run)

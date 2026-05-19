import os
import re

html_pattern = re.compile(r"<(?!(br|!--|/br|/!--|!|a\s|/a|strong|/strong|span|/span|code|/code|p\s|/p|em|/em|li\s|/li|ul\s|/ul|ol\s|/ol))[a-zA-Z/]+[^>]*>")
legacy_br_pattern = re.compile(r"<br\s*/?>")

print("| Lesson | Status | HTML Violations | Legacy Image Violations | Non-compliant Captions | Notes / Key Issues |")
print("|--------|--------|-----------------|-------------------------|------------------------|--------------------|")

for i in range(1, 62):
    filename = f"lektion{i:02d}.md"
    filepath = os.path.join("docs", "lektionen", filename)
    if not os.path.exists(filepath):
        print(f"| Lektion {i:02d} | ❌ Missing | - | - | - | File does not exist |")
        continue
        
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # 1. Parse frontmatter status
    status = "Pending"
    frontmatter_match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if frontmatter_match:
        fm_text = frontmatter_match.group(1)
        status_match = re.search(r"status:\s*\"?([^\n\"]+)\"?", fm_text)
        if status_match:
            status = status_match.group(1)
            
    # 2. Check for HTML tags
    # Let's count occurrences of standard html tags like <table>, <p>, <br>, <font>, <div>, etc.
    html_tags = re.findall(r"</?(?:table|tr|td|th|tbody|font|div|span|p|br|ol|ul|li|hr|b|i|h\d)[^>]*>", content, re.IGNORECASE)
    html_count = len(html_tags)
    
    # 3. Check for standard markdown images not wrapped in ::: media
    # We find all '![' in the file, and check if they are preceded by '::: media' within reasonable distance, or parse blocks
    lines = content.split('\n')
    image_violations = 0
    non_devanagari_captions = 0
    
    in_media = False
    for idx, line in enumerate(lines):
        if '::: media' in line:
            in_media = True
        elif ':::' in line and in_media:
            in_media = False
        
        if '![' in line and not in_media:
            image_violations += 1
            
        # Check if caption is non-compliant (e.g. contains German translations instead of pure Devanagari)
        # Standard format is: Abb.: [Devanagari]
        if line.strip().startswith('Abb.:') or line.strip().startswith('Abb. :'):
            caption_text = line.replace('Abb.:', '').replace('Abb. :', '').strip()
            # If caption contains latin characters (excluding specific markdown links/attributions), it might be non-compliant
            # Let's check if it contains German words or typical latin text
            if re.search(r'[a-zA-ZäöüßÄÖÜ]', caption_text):
                # But wait, it might contain image link details. Let's see if the first line itself has German text.
                # If there's German words like "und", "der", "die", "das", "von", "in", "mit"
                if any(w in caption_text.lower() for w in ["und ", "der ", "die ", "das ", "von ", "in ", "mit ", "bild ", "quelle"]):
                    non_devanagari_captions += 1
                    
    # Summarize violations
    notes = []
    if html_count > 0:
        notes.append(f"{html_count} legacy HTML tag(s)")
    if image_violations > 0:
        notes.append(f"{image_violations} image(s) outside ::: media")
    if non_devanagari_captions > 0:
        notes.append(f"{non_devanagari_captions} German text in caption")
        
    notes_str = ", ".join(notes) if notes else "Fully Compliant"
    
    # Special status overrides for known clean lessons
    display_status = status
    if status == "stable":
        display_status = "✅ Stable"
    elif not notes:
        display_status = "✨ Ready for final QA"
    else:
        display_status = "⚠️ Needs Work"
        
    print(f"| Lektion {i:02d} | {display_status} | {html_count} | {image_violations} | {non_devanagari_captions} | {notes_str} |")

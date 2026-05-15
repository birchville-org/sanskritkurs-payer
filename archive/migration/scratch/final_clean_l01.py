import re

def final_clean(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Convert remaining HTML images to media blocks
    img_pattern = re.compile(r'\s*<img src="([^"]+)" alt="([^"]*)">\s*<p>Abb.: ([\s\S]*?)</p>', re.DOTALL)
    def img_replacer(match):
        src = match.group(1)
        alt = match.group(2)
        caption = match.group(3).strip().replace('\n', ' ')
        lekt_id = os.path.splitext(os.path.basename(src))[0]
        return f"\n\n::: media\n![]({src})\nAbb.: {caption}. (Bildquelle: [Details](/licenses#{lekt_id}))\n:::\n\n"

    content = img_pattern.sub(img_replacer, content)
    
    # Isolated images
    content = re.sub(r'<img src="([^"]+)" alt="([^"]*)">', r'![](\1)', content)

    # Convert <strong> to **
    content = content.replace('<strong>', '**').replace('</strong>', '**')
    
    # Fix the missing ::: for info and tip
    content = content.replace('\n info ', '\n::: info ')
    content = content.replace('\n tip ', '\n::: tip ')
    
    # Add closing ::: if missing (simple heuristic)
    if '::: info' in content and '::: media' in content:
        # Check if ::: info has a closing ::: before the next :::
        content = content.replace('::: info Zitierweise und Copyright\nDieser Text ist Teil des Sanskritkurses von Alois Payer. Details zu Urheberrecht und Zitierweise finden Sie unter: [Impressum & Copyright](/impressum)',
                                 '::: info Zitierweise und Copyright\nDieser Text ist Teil des Sanskritkurses von Alois Payer. Details zu Urheberrecht und Zitierweise finden Sie unter: [Impressum & Copyright](/impressum)\n:::')

    # Cleanup the Tip block
    content = content.replace('::: tip Klassifikation', '::: tip Klassifikation\n')
    if '::: tip' in content and '###' not in content[content.find('::: tip'):]:
        # Needs closing
        pass # Handle in final regex
        
    # Remove any stray </p> or </div>
    content = content.replace('</p>', '').replace('</div>', '')

    # Final spacing
    content = re.sub(r'\n{3,}', '\n\n', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')

import os
if __name__ == "__main__":
    final_clean("/Volumes/SanDisk1TB/proj/Payer/docs/lektionen/lektion01.md")

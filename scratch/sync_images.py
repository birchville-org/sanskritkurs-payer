import os
import re

def sync_image_links():
    root_dir = 'docs/lektionen'
    locales = ['bg', 'it', 'en', 'es', 'ru', 'uk']
    
    for file in os.listdir(root_dir):
        if not file.endswith('.md'):
            continue
        
        root_path = os.path.join(root_dir, file)
        with open(root_path, 'r', encoding='utf-8') as f:
            root_content = f.read()
        
        # Extract all image links in order
        root_images = re.findall(r'!\[.*?\]\((/images/.*?)\)', root_content)
        
        for locale in locales:
            locale_path = os.path.join('docs', locale, 'lektionen', file)
            if not os.path.exists(locale_path):
                continue
                
            with open(locale_path, 'r', encoding='utf-8') as f:
                locale_content = f.read()
            
            # Find all image links in locale file
            locale_images = re.findall(r'!\[.*?\]\((/images/.*?)\)', locale_content)
            
            if len(root_images) == len(locale_images):
                new_locale_content = locale_content
                for root_img, loc_img in zip(root_images, locale_images):
                    if root_img != loc_img:
                        print(f"Syncing image: {loc_img} -> {root_img} in {locale_path}")
                        new_locale_content = new_locale_content.replace(loc_img, root_img)
                
                if new_locale_content != locale_content:
                    with open(locale_path, 'w', encoding='utf-8') as f:
                        f.write(new_locale_content)
            else:
                print(f"Warning: Image count mismatch in {locale_path} ({len(locale_images)} vs {len(root_images)})")
                # Fallback: fix obvious corruptions like lekt0_01
                fixed_content = re.sub(r'/images/lekt(\d)_(\d+)\.jpg', lambda m: f'/images/lekt0{m.group(1)}{m.group(2)}.jpg', locale_content)
                fixed_content = re.sub(r'/images/ue[\u0900-\u09FF]+ung', '/images/uebung', fixed_content)
                if fixed_content != locale_content:
                    with open(locale_path, 'w', encoding='utf-8') as f:
                        f.write(fixed_content)

if __name__ == '__main__':
    sync_image_links()

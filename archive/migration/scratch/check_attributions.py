import os
import re

def check_lesson_attributions(lektionen_dir):
    missing_attributions = []
    
    for filename in sorted(os.listdir(lektionen_dir)):
        if filename.endswith(".md") and filename.startswith("lektion"):
            filepath = os.path.join(lektionen_dir, filename)
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Find all images: ![](/images/lektXXXX.jpg)
            images = re.findall(r'!\[\]\(/images/(lekt\d{4})\.jpg\)', content)
            
            for img in images:
                # Check if the next few lines contain (/licenses#lektXXXX)
                # We look for the pattern following the image
                pattern = rf'!\[\]\(/images/{img}\.jpg\).*?\(/licenses#{img}\)'
                if not re.search(pattern, content, re.DOTALL):
                    missing_attributions.append((filename, img))
    
    return missing_attributions

if __name__ == "__main__":
    lektionen_dir = "/Volumes/SanDisk1TB/proj/Payer/docs/lektionen"
    missing = check_lesson_attributions(lektionen_dir)
    print(f"Total missing attributions: {len(missing)}")
    for file, img in missing:
        print(f"{file}: {img}")

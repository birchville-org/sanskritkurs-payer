import os
import re

def check_cyrillic(directory):
    cyrillic_regex = re.compile(r'[\u0400-\u04FF]')
    for root, dirs, files in os.walk(directory):
        if "bg" in root or ".vitepress" in root: continue
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = cyrillic_regex.findall(content)
                    if matches:
                        print(f"CYRILLIC FOUND in {path}: {set(matches)}")

if __name__ == "__main__":
    check_cyrillic("/Volumes/SanDisk1TB/proj/Payer/docs/")

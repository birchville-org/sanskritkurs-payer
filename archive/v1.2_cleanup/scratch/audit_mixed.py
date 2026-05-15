import os
import re

def check_mixed_script(directory):
    mixed_regex = re.compile(r'[\u0900-\u097F][\u0400-\u04FF]|[\u0400-\u04FF][\u0900-\u097F]')
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    matches = mixed_regex.findall(content)
                    if matches:
                        print(f"FOUND in {path}: {matches[:5]}")

if __name__ == "__main__":
    check_mixed_script("/Volumes/SanDisk1TB/proj/Payer/docs/bg/")

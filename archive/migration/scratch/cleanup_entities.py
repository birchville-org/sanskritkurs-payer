import os

def cleanup_entities(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    if '&nbsp;' in content:
        print(f"Cleaning entities in: {filepath}")
        # Replace &nbsp; with actual non-breaking space \u00A0
        content = content.replace('&nbsp;', '\u00A0')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

def main():
    docs_root = "/Volumes/SanDisk1TB/proj/Payer/docs"
    for root, dirs, files in os.walk(docs_root):
        for filename in files:
            if filename.endswith(".md"):
                cleanup_entities(os.path.join(root, filename))

if __name__ == "__main__":
    main()

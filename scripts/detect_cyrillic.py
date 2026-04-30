import sys
import unicodedata

def detect_cyrillic(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    cyrillic_chars = []
    for char in content:
        if 'CYRILLIC' in unicodedata.name(char, ''):
            cyrillic_chars.append(char)
            
    if cyrillic_chars:
        print(f"❌ {file_path}: Found {len(cyrillic_chars)} Cyrillic characters: {''.join(set(cyrillic_chars))}")
        return False
    else:
        print(f"✅ {file_path}: No Cyrillic characters found.")
        return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python detect_cyrillic.py <file_path>")
        sys.exit(1)
    
    success = True
    for arg in sys.argv[1:]:
        if not detect_cyrillic(arg):
            success = False
            
    if not success:
        sys.exit(1)

import os
import re

# Final cleanup for mangled compound words in Bulgarian
FINAL_BG_FIXES = {
    'именообразуванеen': 'именообразувания',
    'именообразуванеn': 'именообразуване',
    'образуванеstypen': 'типове образуване',
    'образуванеs': 'образуване',
    'unкъм': 'към', # mangled 'an ' -> 'към ' inside words?
    'tкъм': 'към',
    '-mкъм': '-an', # likely a mangled suffix -an
    '-vкъм': '-van',
    'Indiкъм': 'India',
    'Ozeкъм': 'океан',
    'гlaсnata': 'гласната',
    'склонеniя': 'склонения',
    'дезидераtiв': 'дезидератив',
    'интензиtiв': 'интензитив',
    'дезидеративni': 'дезидеративни',
}

def repair_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    orig_content = content
    
    if '/bg/' in path:
        for err, fix in FINAL_BG_FIXES.items():
            content = content.replace(err, fix)
            
        # Fix the "-an" vs "към" mess
        # If we see "-an" followed by Bulgarian text, it's likely correct.
        # If we see "-към", it might be a mangled "-an".
        content = content.replace('-към', '-an')
        
    if content != orig_content:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

def main():
    docs_dir = "/Volumes/SanDisk1TB/proj/Payer/docs"
    count = 0
    for root, dirs, files in os.walk(docs_dir):
        if 'node_modules' in root: continue
        for file in files:
            if file.endswith('.md'):
                if repair_file(os.path.join(root, file)):
                    count += 1
    print(f"Repaired {count} files.")

if __name__ == "__main__":
    main()

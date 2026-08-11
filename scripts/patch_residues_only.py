import os
import sys
import time

# Add the scripts directory to the path so we can import lan_translate
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from translation.quality_control import scan_german_residues, sonnet_patch_residues, log_failure
from translation.config import BASE_DIR

# The 8 languages that have residues
langs = ['bg', 'uk', 'hi', 'ar', 'ta', 'la', 'rm', 'arc']

def main():
    print("Starting Sonnet patch for existing residues...")
    for lang in langs:
        print(f"\n=== Processing {lang} ===")
        lesson_dir = os.path.join(BASE_DIR, lang, "lektionen")
        if not os.path.isdir(lesson_dir):
            continue
        
        for l_num in range(1, 62):
            filename = f"lektion{l_num:02d}.md"
            filepath = os.path.join(lesson_dir, filename)
            if not os.path.exists(filepath):
                continue
                
            with open(filepath, encoding='utf-8') as f:
                content = f.read()
                
            flagged = scan_german_residues(content)
            if not flagged:
                continue
                
            print(f"[{lang}] {filename}: {len(flagged)} residues found.")
            patched = sonnet_patch_residues(content, flagged, lang)
            
            flagged_after = scan_german_residues(patched)
            
            # Write patched content atomically
            import tempfile
            tmp_fd, tmp_p = tempfile.mkstemp(dir=lesson_dir, suffix='.tmp')
            with os.fdopen(tmp_fd, 'w', encoding='utf-8') as wf:
                wf.write(patched)
            os.replace(tmp_p, filepath)
            
            resolved = len(flagged) - len(flagged_after)
            print(f"  ✓ Patched {resolved}/{len(flagged)} residues. {len(flagged_after)} remaining.")
            
            if flagged_after:
                log_failure(lang, filename, 'RESIDUE', flagged_after, f"After Sonnet patch: {len(flagged_after)} unresolved")
                
            time.sleep(0.5)  # small pause to avoid hitting rate limits

if __name__ == "__main__":
    main()

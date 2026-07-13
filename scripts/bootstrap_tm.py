import os
import sys
import glob
import json

# Add scripts directory to path so we can import lan_translate
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lan_translate

BASE_DIR = lan_translate.BASE_DIR
LANGUAGES = lan_translate.LANGUAGES

def bootstrap():
    print("Starting TM Bootstrapping...")
    de_files = glob.glob(os.path.join(BASE_DIR, "lektionen/*.md"))
    
    total_files = 0
    mapped_chunks = 0
    skipped_files = 0
    
    for de_file in de_files:
        filename = os.path.basename(de_file)
        with open(de_file, "r", encoding="utf-8") as f:
            de_content = f.read()
            
        # Strip YAML if present
        if de_content.startswith("---\n"):
            end_idx = de_content.find("\n---\n", 4)
            if end_idx != -1:
                de_content = de_content[end_idx+5:]
                
        de_chunks = lan_translate.chunk_content(de_content)
        
        for lang in LANGUAGES:
            if lang == "de": continue
            if lang in ["th", "el", "cop"]: continue # Skipped languages
            
            target_file = os.path.join(BASE_DIR, f"{lang}/lektionen/{filename}")
            if not os.path.exists(target_file):
                continue
                
            with open(target_file, "r", encoding="utf-8") as f:
                target_content = f.read()
                
            if target_content.startswith("---\n"):
                end_idx = target_content.find("\n---\n", 4)
                if end_idx != -1:
                    target_content = target_content[end_idx+5:]
                    
            target_chunks = lan_translate.chunk_content(target_content)
            
            if len(de_chunks) == len(target_chunks):
                # Perfect match!
                tm_cache = lan_translate.load_tm(lang)
                updated = False
                for d_chunk, t_chunk in zip(de_chunks, target_chunks):
                    if not d_chunk.strip(): continue
                    h = lan_translate.hash_chunk(d_chunk)
                    if h not in tm_cache:
                        tm_cache[h] = t_chunk
                        updated = True
                        mapped_chunks += 1
                if updated:
                    lan_translate.save_tm(lang, tm_cache)
                total_files += 1
            else:
                print(f"Mismatch in {lang}/{filename}: {len(de_chunks)} vs {len(target_chunks)}")
                skipped_files += 1
                
    print(f"Bootstrapping complete.")
    print(f"Successfully mapped {total_files} file pairs.")
    print(f"Skipped {skipped_files} file pairs due to chunk boundary mismatch.")
    print(f"Total TM entries added: {mapped_chunks}")

if __name__ == "__main__":
    bootstrap()

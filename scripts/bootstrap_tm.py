import os
import sys
import glob
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from translation.config import BASE_DIR, LANGUAGES
from translation.file_processor import chunk_content, load_tm, save_tm, hash_chunk

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

        if de_content.startswith("---\n"):
            end_idx = de_content.find("\n---\n", 4)
            if end_idx != -1:
                de_content = de_content[end_idx+5:]

        de_chunks = chunk_content(de_content)

        for lang in LANGUAGES:
            if lang == "de": continue
            if lang in ["th", "el", "cop"]: continue

            target_file = os.path.join(BASE_DIR, f"{lang}/lektionen/{filename}")
            if not os.path.exists(target_file):
                continue

            with open(target_file, "r", encoding="utf-8") as f:
                target_content = f.read()

            if target_content.startswith("---\n"):
                end_idx = target_content.find("\n---\n", 4)
                if end_idx != -1:
                    target_content = target_content[end_idx+5:]

            target_chunks = chunk_content(target_content)

            if len(de_chunks) == len(target_chunks):
                tm_cache = load_tm(lang)
                updated = False
                for d_chunk, t_chunk in zip(de_chunks, target_chunks):
                    if not d_chunk.strip(): continue
                    h = hash_chunk(d_chunk)
                    if h not in tm_cache:
                        tm_cache[h] = t_chunk
                        updated = True
                        mapped_chunks += 1
                if updated:
                    save_tm(lang, tm_cache)
                total_files += 1
            else:
                skipped_files += 1

    print(f"Bootstrapping complete: {mapped_chunks} chunks mapped across {total_files} file-language pairs ({skipped_files} skipped due to mismatch).")

if __name__ == "__main__":
    bootstrap()

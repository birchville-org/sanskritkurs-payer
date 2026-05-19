import os
import json
import urllib.request
import time
import sys

# Configuration
API_URL = "http://192.168.1.22:8000/v1/chat/completions"
MODEL = "mlx-community/Qwen3.6-35B-A3B-4bit"
LANGUAGES = ["en", "it", "es", "ru", "uk", "bg"]
LESSONS = list(range(1, 62))
BASE_DIR = "/Volumes/SanDisk1TB/proj/Payer/docs"
SOURCE_DIR = os.path.join(BASE_DIR, "lektionen")

def translate_text(text, target_lang):
    prompt = f"""You are a professional scholarly translator. Translate the following Sanskrit course material from German into {target_lang}.
STRICT RULES:
1. PRESERVE all Markdown syntax (headers, lists, tables).
2. PRESERVE all VitePress containers (::: grammar-box, ::: media, ::: deleteme-box).
3. DO NOT translate Sanskrit text in Devanagari script.
4. DO NOT translate Sanskrit transliteration (IAST).
5. DO NOT translate technical identifiers in YAML frontmatter (like lesson_id, status).
6. Maintain the editorial, scholarly tone of the 'Scholarly Synthesis' design system.

German Source:
{text}
"""
    
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": f"You are a professional translator specializing in scholarly Sanskrit education materials. You translate from German to {target_lang}."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 4096
    }
    
    max_retries = 5
    for attempt in range(max_retries):
        req = urllib.request.Request(
            API_URL, 
            data=json.dumps(data).encode('utf-8'), 
            headers={'Content-Type': 'application/json'}
        )
        try:
            with urllib.request.urlopen(req, timeout=600) as response:
                res_data = json.loads(response.read().decode('utf-8'))
                return res_data['choices'][0]['message']['content']
        except Exception as e:
            wait_time = (2 ** attempt) * 5  # 5s, 10s, 20s, 40s, 80s
            msg = f"[{target_lang}] Connection failed (attempt {attempt+1}/{max_retries}): {str(e)}. Retrying in {wait_time}s...\n"
            sys.stdout.write(msg)
            sys.stdout.flush()
            time.sleep(wait_time)
            
    return f"ERROR: Failed to translate after {max_retries} attempts."

def chunk_content(content):
    # Splits content into safe, manageable chunks of max ~3000 characters
    # respecting markdown boundaries (headers, containers) to avoid LLM context issues.
    lines = content.split('\n')
    chunks = []
    current_chunk = []
    current_size = 0
    
    for line in lines:
        is_header = line.startswith('## ') or line.startswith('### ')
        is_break_point = (current_size > 3000 and (not line.strip() or line.startswith(':::') or line.startswith('|')))
        
        if (is_header or is_break_point) and current_chunk:
            chunks.append('\n'.join(current_chunk))
            current_chunk = []
            current_size = 0
            
        current_chunk.append(line)
        current_size += len(line) + 1
        
    if current_chunk:
        chunks.append('\n'.join(current_chunk))
        
    return chunks

def main():
    print(f"Starting translation process using {MODEL} at {API_URL}...")
    for lang in LANGUAGES:
        target_dir = os.path.join(BASE_DIR, lang, "lektionen")
        os.makedirs(target_dir, exist_ok=True)
        
        for l_num in LESSONS:
            filename = f"lektion{l_num:02d}.md"
            source_path = os.path.join(SOURCE_DIR, filename)
            target_path = os.path.join(target_dir, filename)
            
            if not os.path.exists(source_path):
                print(f"Source not found: {source_path}")
                continue
            
            # Smart check: skip only if target exists, is valid (>500 bytes), and is newer than source
            if os.path.exists(target_path) and os.path.getsize(target_path) > 500:
                if os.path.getmtime(target_path) > os.path.getmtime(source_path):
                    print(f"[{lang}] Skipping {filename} (already up to date).")
                    continue
                else:
                    print(f"[{lang}] Outdated translation detected for {filename} (source modified). Re-translating...")
            
            print(f"[{lang}] Translating {filename}...")
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Smart chunking to prevent LLM generation token limits
            chunks = chunk_content(content)
                
            translated_chunks = []
            total_chunks = len(chunks)
            failed = False
            for i, chunk in enumerate(chunks, 1):
                if chunk.strip():
                    print(f"  -> Translating section {i}/{total_chunks}...")
                    translated_chunk = translate_text(chunk, lang)
                    if translated_chunk.startswith("ERROR:"):
                        print(f"  [!] Translation failed for chunk {i}: {translated_chunk}")
                        failed = True
                        break
                    translated_chunks.append(translated_chunk)
                else:
                    translated_chunks.append(chunk)
            
            if failed:
                print(f"[{lang}] Skipping write for {filename} due to translation errors.")
                continue
                    
            translated_content = '\n\n'.join(translated_chunks)
            
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            print(f"[{lang}] Finished {filename}.")
            time.sleep(2) # Safe delay between files

if __name__ == "__main__":
    main()

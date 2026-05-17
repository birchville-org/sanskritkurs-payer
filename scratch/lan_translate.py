import os
import json
import urllib.request
import time
import sys

# Configuration
API_URL = "http://192.168.1.22:8000/v1/chat/completions"
MODEL = "mlx-community/Qwen3.6-35B-A3B-4bit"
LANGUAGES = ["it", "es", "en", "ru", "uk", "bg"]
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
        "temperature": 0.3
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
            
            # Smart check: skip if file already successfully translated (size > 500 bytes)
            if os.path.exists(target_path) and os.path.getsize(target_path) > 500:
                print(f"[{lang}] Skipping {filename} (already translated).")
                continue
            
            print(f"[{lang}] Translating {filename}...")
            with open(source_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            translated_content = translate_text(content, lang)
            
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(translated_content)
            
            print(f"[{lang}] Finished {filename}.")
            time.sleep(3) # Safe delay between files

if __name__ == "__main__":
    main()

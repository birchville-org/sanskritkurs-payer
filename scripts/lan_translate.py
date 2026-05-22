import os
import json
import urllib.request
import time
import sys
import re

# Configuration
API_URL = "http://192.168.1.22:8000/v1/chat/completions"
MODEL = "mlx-community/Qwen3.6-35B-A3B-4bit"
LANGUAGES = ["en", "it", "es", "ru", "uk", "bg"]
LANG_NAMES = {
    "en": "English", "it": "Italian", "es": "Spanish",
    "ru": "Russian", "uk": "Ukrainian", "bg": "Bulgarian",
}
LESSONS = list(range(1, 62))
MAIN_PAGES = ["index.md", "grammatik.md", "themen.md", "impressum.md", "licenses.md"]
BASE_DIR = "/Volumes/SanDisk1TB/proj/Payer/docs"
SOURCE_DIR = os.path.join(BASE_DIR, "lektionen")

def translate_text(text, target_lang):
    lang_name = LANG_NAMES.get(target_lang, target_lang)
    system = (
        f"You are a scholarly translator. Translate German Sanskrit-education markdown to {lang_name}. "
        "Rules: preserve all Markdown syntax, VitePress containers (:::), Devanāgarī script, IAST transliterations, "
        "and YAML frontmatter keys unchanged. Keep the editorial scholarly tone."
    )
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": text}
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

def escape_angle_brackets_in_tables(text):
    # LLMs sometimes convert &lt;form&gt; → <form>, breaking Vue (HTML is forbidden).
    # Fix: re-escape raw <...> on all lines, skipping already-escaped entities.
    lines = text.split('\n')
    result = []
    for line in lines:
        line = line.replace('&lt;', '\x00LT\x00').replace('&gt;', '\x00GT\x00')
        line = re.sub(r'<([^>\s][^>]*)>', r'&lt;\1&gt;', line)
        line = line.replace('\x00LT\x00', '&lt;').replace('\x00GT\x00', '&gt;')
        result.append(line)
    return '\n'.join(result)

def fix_home_links(content, lang):
    """Prefix bare absolute links in index.md YAML frontmatter with /lang/."""
    def replace_link(m):
        path = m.group(1)
        if path.startswith(f'/{lang}/'):
            return m.group(0)
        return f'link: /{lang}{path}'
    return re.sub(r'link:\s*(/[^\s\n]+)', replace_link, content)


def translate_file(source_path, target_path, lang, post_process=None):
    """Translate a single file with mtime-based skip and chunking. Returns True on success."""
    filename = os.path.basename(source_path)
    if os.path.exists(target_path) and os.path.getsize(target_path) > 500:
        if os.path.getmtime(target_path) > os.path.getmtime(source_path):
            print(f"[{lang}] Skipping {filename} (up to date).")
            return True
        print(f"[{lang}] Outdated {filename} — re-translating...")

    print(f"[{lang}] Translating {filename}...")
    with open(source_path, encoding="utf-8") as f:
        content = f.read()

    chunks = chunk_content(content)
    translated_chunks = []
    for i, chunk in enumerate(chunks, 1):
        if not chunk.strip():
            translated_chunks.append(chunk)
            continue
        print(f"  -> section {i}/{len(chunks)}...")
        result = translate_text(chunk, lang)
        if result.startswith("ERROR:"):
            print(f"  [!] Failed chunk {i}: {result}")
            return False
        translated_chunks.append(result)

    translated = escape_angle_brackets_in_tables('\n\n'.join(translated_chunks))
    if post_process:
        translated = post_process(translated)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(translated)
    print(f"[{lang}] Done {filename}.")
    time.sleep(2)
    return True


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
        # ── Lektionen ────────────────────────────────────────────────────────
        lesson_dir = os.path.join(BASE_DIR, lang, "lektionen")
        os.makedirs(lesson_dir, exist_ok=True)
        for l_num in LESSONS:
            filename = f"lektion{l_num:02d}.md"
            source_path = os.path.join(SOURCE_DIR, filename)
            if not os.path.exists(source_path):
                print(f"Source not found: {source_path}")
                continue
            translate_file(source_path, os.path.join(lesson_dir, filename), lang)

        # ── Hauptseiten ──────────────────────────────────────────────────────
        lang_dir = os.path.join(BASE_DIR, lang)
        os.makedirs(lang_dir, exist_ok=True)
        for filename in MAIN_PAGES:
            source_path = os.path.join(BASE_DIR, filename)
            if not os.path.exists(source_path):
                continue
            post = (lambda t: fix_home_links(t, lang)) if filename == "index.md" else None
            translate_file(source_path, os.path.join(lang_dir, filename), lang, post_process=post)

if __name__ == "__main__":
    main()

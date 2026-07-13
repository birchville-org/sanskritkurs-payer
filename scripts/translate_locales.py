import os
import glob
import json
import subprocess
import time

API_URL = "http://nyx.local:8088/v1/chat/completions"
MODEL = "mlx-community--Qwen3.6-35B-A3B-4bit"

LANG_NAMES = {
    'zh-CN': 'Simplified Chinese',
    'th': 'Thai',
    'el': 'Modern Greek',
    'cop': 'Coptic (Bohairic)',
    'hi': 'Hindi',
    'rm': 'Romansh Grischun',
    'ru': 'Russian',
    'it': 'Italian',
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'bg': 'Bulgarian',
    'uk': 'Ukrainian',
    'ta': 'Tamil',
    'pa': 'Punjabi',
    'la': 'Latin',
    'ro': 'Romanian',
    'he': 'Hebrew',
    'id': 'Indonesian',
    'ar': 'Arabic',
    'arc': 'Aramaic'
}

def translate_mjs(filepath, lang_code):
    lang_name = LANG_NAMES.get(lang_code, lang_code)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    system_prompt = (
        f"You are a translator for a VitePress JS configuration file. "
        f"Translate the UI strings (values for text, label, description, returnToTopLabel, docFooter, etc.) "
        f"from English to {lang_name}. DO NOT translate keys, variable names, link paths, or HTML class names. "
        f"Return ONLY the valid JavaScript code. No markdown wrapping if possible."
    )
    
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": content}
        ],
        "temperature": 0.0
    }

    try:
        curl_cmd = ['curl', '-s', '-X', 'POST', API_URL, '-H', 'Content-Type: application/json', '-H', 'Authorization: Bearer local']
        curl_cmd.extend(['-d', json.dumps(payload), '--max-time', '600'])
        
        print(f"Translating {lang_code} ({lang_name})...")
        proc = subprocess.run(curl_cmd, capture_output=True, text=True)
        if proc.returncode == 0:
            resp = json.loads(proc.stdout)
            if 'choices' in resp:
                reply = resp['choices'][0]['message']['content'].strip()
                if reply.startswith("```javascript"):
                    reply = reply[13:-3].strip()
                elif reply.startswith("```js"):
                    reply = reply[5:-3].strip()
                elif reply.startswith("```"):
                    reply = reply[3:-3].strip()
                    
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(reply + "\n")
                print(f"  -> Successfully translated {os.path.basename(filepath)}")
            else:
                print(f"  -> API Error: {resp}")
        else:
            print(f"  -> Curl Error: {proc.stderr}")
    except Exception as e:
        print(f"  -> Exception: {e}")

def main():
    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs', '.vitepress', 'locales'))
    mjs_files = glob.glob(os.path.join(target_dir, '*.mjs'))
    
    for filepath in mjs_files:
        lang_code = os.path.basename(filepath).replace('.mjs', '')
        if lang_code in ['de', 'en']:
            continue
            
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if it needs translation by looking for English keys that should be translated
        if "'Table of Contents'" in content or "'Grammar Topics'" in content:
            translate_mjs(filepath, lang_code)
        else:
            print(f"Skipping {lang_code} (already translated)")

if __name__ == "__main__":
    main()

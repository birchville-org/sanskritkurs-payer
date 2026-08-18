import os
import sys
import json
import urllib.request
import urllib.error
import time
import re

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from translation.protector import (
    protect_devanagari, restore_devanagari,
    protect_iast_lines, restore_iast_lines,
    protect_br, restore_br,
    protect_structure, restore_structure
)
from translation.config import LANG_NAMES

API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print("ERROR: GEMINI_API_KEY environment variable not set.")
    sys.exit(1)

def call_gemini(system_instruction, user_prompt, temperature=0.3):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={API_KEY}"
    
    payload = {
        "system_instruction": {
            "parts": [{"text": system_instruction}]
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_prompt}]
            }
        ],
        "generationConfig": {
            "temperature": temperature,
            "maxOutputTokens": 8192
        }
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    
    try:
        with urllib.request.urlopen(req, timeout=120) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            try:
                return res_json["candidates"][0]["content"]["parts"][0]["text"]
            except (KeyError, IndexError):
                print("Unexpected API response format:", res_json)
                return None
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.read().decode('utf-8')}")
        return None
    except Exception as e:
        print(f"Request Error: {e}")
        return None

def translate_file(target_lang, file_name, temperature):
    print(f"--- Starting Gemini Experiment for {target_lang} / {file_name} (Temp: {temperature}) ---")
    source_path = os.path.join("/Volumes/SanDisk1TB/proj/Payer/docs/lektionen", file_name)
    target_path = os.path.join("/Volumes/SanDisk1TB/proj/Payer/docs", target_lang, "lektionen", file_name)
    
    if not os.path.exists(source_path):
        print(f"Source file {source_path} not found.")
        return
        
    with open(source_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    lang_name = LANG_NAMES.get(target_lang, target_lang)
    _mark_skt = (target_lang == 'hi')
    
    # 1. Apply Protectors
    protected, deva_registry = protect_devanagari(text)
    protected, iast_registry = protect_iast_lines(protected)
    protected = protect_br(protected)
    protected, struct_registry = protect_structure(protected)
    
    # 2. Add Line Numbers to force 1:1 mapping
    source_lines = protected.split('\n')
    indexed_lines = []
    for idx, l in enumerate(source_lines):
        if l.strip():
            indexed_lines.append(f"[L{idx}] {l}")
        else:
            indexed_lines.append(l)
    indexed_protected = '\n'.join(indexed_lines)
    
    # 3. Prepare Prompts
    system = (
        f"You are a scholarly translator. Translate ALL German text in this Sanskrit-education markdown to {lang_name}. "
        "Rules: "
        "(1) Translate every German word — including captions, image descriptions, verse translations, and prose. "
        "(2) Preserve unchanged: Markdown syntax, IAST transliterations, YAML frontmatter keys, HTML comments, ⟨DEVA_N⟩ placeholders, ⟨IAST_L_N⟩ placeholders, ⟨BR⟩ placeholders, and ⟨STRUCT_N⟩ placeholders. "
        "(3) NEVER add TODO comments, fallback markers, or any annotations of your own. If unsure, translate into English. "
        "(4) Keep the scholarly editorial tone. "
        "(5) CRITICAL: Preserve the exact line count of the source. Every source line must appear as exactly one output line. NEVER delete, merge, or collapse lines. "
        "(6) CRITICAL: Each non-empty line of the input is prefixed with a bracketed identifier like [L0], [L1]... You MUST preserve these identifiers exactly at the start of each translated line. Do not translate, modify, or remove them. "
        "(7) CRITICAL: Copy every ⟨DEVA_N⟩ and ⟨IAST_L_N⟩ placeholder character-for-character. Do not interpret them. "
        "(8) CRITICAL: Lines consisting ONLY of ⟨DEVA_N⟩ tokens are Sanskrit verses. Copy every token on that line verbatim. "
    )
    
    # 4. Call API
    print("Calling Gemini 1.5 Pro...")
    start_t = time.time()
    raw_result = call_gemini(system, indexed_protected, temperature=temperature)
    print(f"API Call finished in {time.time()-start_t:.1f}s")
    
    if not raw_result:
        print("Failed to get response.")
        return
        
    # 5. Parse and Restore Lines
    result_lines = raw_result.split('\n')
    restored_lines = [None] * len(source_lines)
    unmatched_lines = []
    
    for r_line in result_lines:
        m = re.match(r'^\s*\[?[LЛlл]?\s*(\d+)\s*\]?[\s:\.\-]*\s*(.*)$', r_line, re.IGNORECASE)
        if m:
            idx = int(m.group(1))
            content = m.group(2)
            if 0 <= idx < len(source_lines):
                restored_lines[idx] = content
            else:
                unmatched_lines.append(r_line)
        else:
            if r_line.strip() and not r_line.strip() == "```markdown" and not r_line.strip() == "```":
                unmatched_lines.append(r_line)
                
    unmatched_idx = 0
    for idx, src_l in enumerate(source_lines):
        if src_l.strip():
            if restored_lines[idx] is None:
                if unmatched_idx < len(unmatched_lines):
                    clean_line = re.sub(r'^\s*\[?[LЛlл]?\s*\d+\s*\]?[\s:\.\-]*\s*', '', unmatched_lines[unmatched_idx], flags=re.IGNORECASE)
                    restored_lines[idx] = clean_line
                    unmatched_idx += 1
                else:
                    print(f"Warning: Dropped line {idx}: {src_l}")
                    restored_lines[idx] = src_l
        else:
            restored_lines[idx] = ''
            
    result = '\n'.join(restored_lines)
    
    # 6. Restore Placeholders
    missing = [k for k in deva_registry if k not in result]
    if missing:
        print(f"Warning: Dropped {len(missing)} DEVA placeholders!")
        
    result = restore_devanagari(result, deva_registry, _mark_skt)
    result = restore_iast_lines(result, iast_registry)
    result = restore_br(result)
    result = restore_structure(result, struct_registry)
    
    # 7. Write to Target
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        f.write(result)
        
    print(f"Success! Translated and saved to {target_path}")

if __name__ == "__main__":
    translate_file("pa", "lektion57.md", temperature=0.4)

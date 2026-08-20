#!/usr/bin/env python3
import sys
import os
import json
import urllib.request
import urllib.parse
import re
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from translation.config import BASE_DIR, SOURCE_DIR, ANTHROPIC_API_KEY, ANTHROPIC_API_URL, ANTHROPIC_MODEL, LANG_NAMES
from translation.file_processor import load_tm, save_tm, chunk_content, hash_chunk
from translation.quality_control import scan_german_residues
from translation.protector import protect_devanagari, restore_devanagari, protect_iast_lines, restore_iast_lines, protect_br, restore_br, protect_structure, restore_structure

def translate_chunk_sonnet(text, target_lang):
    """Translates a single chunk using exclusively Claude 3.5 Sonnet."""
    lang_name = LANG_NAMES.get(target_lang, target_lang)
    _mark_skt = (target_lang == 'hi')
    
    protected, deva_registry = protect_devanagari(text)
    protected, iast_registry = protect_iast_lines(protected)
    protected = protect_br(protected)
    protected, struct_registry = protect_structure(protected)
    
    heading_mappings = {
        'en': "e.g. '# Lesson N'", 'zh-CN': "e.g. '# 第N课'", 'zh': "e.g. '# 第N課'",
        # add others if needed
    }
    target_example = heading_mappings.get(target_lang, "")
    if target_example:
        target_example = f" ({target_example})"
        
    system = (
        f"You are a scholarly translator. Translate ALL German text in this Sanskrit-education markdown to {lang_name}. "
        "Rules: "
        "(1) Translate every German word — including captions, image descriptions, verse translations, and prose. "
        "(2) Preserve unchanged: Markdown syntax, IAST transliterations, YAML frontmatter keys, HTML comments, ⟨DEVA_N⟩ placeholders, ⟨IAST_L_N⟩ placeholders, ⟨BR⟩ placeholders, and ⟨STRUCT_N⟩ placeholders. "
        f"(3) Translate '# Lektion N' headings to the target-language equivalent{target_example}. "
        "(4) NEVER add TODO comments, fallback markers, or any annotations of your own. If unsure how to translate a word or sentence into the target language, translate it into English as a fallback (NEVER leave it in German). "
        "(5) Keep the scholarly editorial tone throughout. "
        "(6) CRITICAL: Preserve the exact line count of the source. Every source line must appear as exactly one output line. NEVER delete, merge, or collapse lines. "
        "(6a) CRITICAL: Each non-empty line of the input is prefixed with a bracketed identifier like [L0], [L1], [L2]... You MUST preserve these identifiers exactly at the start of each translated line. Do not translate, modify, or remove them. "
        "(7) CRITICAL: Copy every ⟨DEVA_N⟩ and ⟨IAST_L_N⟩ placeholder character-for-character. They are replaced with Devanāgarī and IAST text after translation — do NOT interpret, transliterate, or remove them. "
        "(7a) CRITICAL: Lines consisting ONLY of ⟨DEVA_N⟩ tokens (and spaces/punctuation like ।  ॥) are Sanskrit verse lines. Copy every token on that line verbatim. NEVER transliterate Sanskrit verses into the target script — the placeholders will be restored to Devanāgarī automatically. "
        "(7b) CRITICAL: Preserve ALL Markdown image syntax exactly: ![alt](/path/to/image.jpg) — never drop the parentheses around the image path. "
        "(8) Numbered exercise sentences (e.g. '3. Śūdras erlangen...', '4. Die Kṣatriyas...') MUST be translated to the target language even when they begin with Sanskrit proper nouns in IAST notation. The IAST proper noun is preserved as-is; only the surrounding German words are translated."
    )
    
    system_claude = (
        system + 
        "\n\nCRITICAL INSTRUCTION: You are the final fallback tier. "
        "Previous translations failed because they left German words untranslated or dropped placeholders. "
        "You MUST translate literally every single German word to the target language, no exceptions. "
        "If you don't know a word, translate it to English. Never leave German words in the output. "
        "Maintain exact line counts and placeholders."
    )
    
    source_lines = protected.split('\n')
    indexed_lines = []
    for idx, l in enumerate(source_lines):
        if l.strip():
            indexed_lines.append(f"[L{idx}] {l}")
        else:
            indexed_lines.append(l)
    indexed_protected = '\n'.join(indexed_lines)
    
    data_claude = {
        "model": ANTHROPIC_MODEL,
        "max_tokens": 8192,
        "system": system_claude,
        "messages": [
            {"role": "user", "content": indexed_protected}
        ]
    }
    
    req_claude = urllib.request.Request(
        ANTHROPIC_API_URL,
        data=json.dumps(data_claude).encode('utf-8'),
        headers={
            'x-api-key': ANTHROPIC_API_KEY,
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json'
        }
    )
    
    try:
        with urllib.request.urlopen(req_claude, timeout=120) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            text_blocks = [b['text'] for b in res_data.get('content', []) if b.get('type') == 'text']
            if not text_blocks:
                return f"ERROR: API Request failed - No text block in response. Full: {res_data}", False
            result_str = "".join(text_blocks)
    except Exception as e:
        import traceback
        return f"ERROR: API Request failed - {e}\n{traceback.format_exc()}", False
        
    claude_lines = result_str.split('\n')
    c_restored_lines = [None] * len(source_lines)
    c_unmatched = []
    for r_line in claude_lines:
        m = re.match(r'^\s*\[?[LЛlл]?\s*(\d+)\s*\]?[\s:\.\-]*\s*(.*)$', r_line, re.IGNORECASE)
        if m:
            idx = int(m.group(1))
            if 0 <= idx < len(source_lines):
                c_restored_lines[idx] = m.group(2)
            else:
                c_unmatched.append(r_line)
        else:
            if r_line.strip(): c_unmatched.append(r_line)
            
    c_unmatched_idx = 0
    for idx, src_l in enumerate(source_lines):
        if src_l.strip():
            if c_restored_lines[idx] is None:
                if c_unmatched_idx < len(c_unmatched):
                    c_restored_lines[idx] = re.sub(r'^\s*\[?[LЛlл]?\s*\d+\s*\]?[\s:\.\-]*\s*', '', c_unmatched[c_unmatched_idx], flags=re.IGNORECASE)
                    c_unmatched_idx += 1
                else:
                    c_restored_lines[idx] = src_l
        else:
            c_restored_lines[idx] = ''
            
    c_res = '\n'.join(c_restored_lines)
    
    # QC checks
    if len([l for l in source_lines if l.strip()]) != len([l for l in c_res.split('\n') if l.strip()]):
        return "ERROR: Line count mismatch", False
        
    c_missing_struct = [k for k in struct_registry if k not in c_res]
    if c_missing_struct:
        return f"ERROR: Missing structure {c_missing_struct}", False
        
    c_missing_deva = [k for k in deva_registry if k not in c_res]
    if c_missing_deva:
        return f"ERROR: Dropped {len(c_missing_deva)} Devanagari placeholders", False
        
    result = restore_devanagari(c_res, deva_registry, _mark_skt)
    result = restore_iast_lines(result, iast_registry)
    result = restore_br(result)
    result = restore_structure(result, struct_registry)
    
    return result, True

from translation_qa import check_has_de_phrases

def main():
    if len(sys.argv) < 3:
        print("Usage: python3 patch_with_sonnet.py <lang> <filename>")
        sys.exit(1)
        
    lang = sys.argv[1]
    filename = sys.argv[2]
    
    source_path = os.path.join(SOURCE_DIR, filename)
    if not os.path.exists(source_path):
        print(f"File not found: {source_path}")
        sys.exit(1)
        
    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    body = content
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            body = parts[2]
            
    source_chunks = chunk_content(body)
    tm = load_tm(lang)
    
    print(f"Scanning {len(source_chunks)} chunks for {lang}/{filename}...")
    
    patched_count = 0
    for idx, s_chunk in enumerate(source_chunks):
        c_hash = hash_chunk(s_chunk)
        if c_hash in tm and not tm[c_hash].startswith("ERROR:"):
            target_chunk = tm[c_hash]
            if check_has_de_phrases(target_chunk, lang):
                print(f"--> Chunk {idx+1}/{len(source_chunks)} has residues. Sending to Sonnet...")
                
                result, success = translate_chunk_sonnet(s_chunk, lang)
                if success:
                    if check_has_de_phrases(result, lang):
                        print(f"    [!] Sonnet translation STILL has residues! Not saving.")
                    else:
                        print(f"    [✓] Sonnet translation successful and clean! Updating TM.")
                        tm[c_hash] = result
                        patched_count += 1
                else:
                    print(f"    [!] Sonnet translation failed: {result}")
                    
    if patched_count > 0:
        save_tm(lang, tm)
        print(f"Successfully patched {patched_count} chunks.")
        print(f"Run 'python3 scripts/lan_translate.py -l {lang} {filename.replace('.md', '')}' to apply.")
    else:
        print("No chunks were patched.")

if __name__ == "__main__":
    main()

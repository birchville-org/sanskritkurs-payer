"""
File translation orchestration, chunking, frontmatter translation, link fixes, TM hashing, licenses generation, and main page synchronization.
"""

import os
import re
import sys
import glob
import time
import json
import hashlib
from .config import (
    BASE_DIR, SOURCE_DIR, LANGUAGES, LANG_NAMES, LESSONS, MAIN_PAGES,
    LICENSES_LABELS, LICENSES_PHRASES, DELETEME_TITLE
)
from .client import translate_text
from .quality_control import scan_german_residues, sonnet_patch_residues, log_failure
from .chunker import chunk_content, hash_chunk, touch_progress_heartbeat
from .session_manager import (
    get_force_session_path, get_force_session_start_time, clear_force_session, is_language_completed
)

GLOSSARY_CLEANUP_MAPS = {
    "rm": [
        ("Indikativ Präsens", "Indicativ preschent"),
        ("Passiv Präsens", "Passiv preschent"),
        ("Imperfekt", "Imperfect"),
        ("Maskulinum", "Masculin"),
        ("maskulinum", "masculin"),
        ("Femininum", "Feminin"),
        ("femininum", "feminin"),
        ("Wortbildung", "Furmaziun da pleds"),
        ("Auslautendes", "Final"),
        ("auslautendes", "final"),
        ("Stammvokal", "Vocala da stramps"),
        ("Passivsatz", "Frasa passiva"),
        ("dritte Person", "terza persuna"),
        ("dritte", "terza"),
        ("Furmaiziun", "Furmaziun"),
        ("furmaiziun", "furmaziun"),
        ("questa frase", "questa frasa"),
        ("completamente", "cumpletamain"),
        ("frase", "frasa"),
        ("della", "da la"),
        ("richtig:", "gueldig:"),
        ("Erklärung:", "Explicaziun:"),
    ]
}

def escape_angle_brackets_in_tables(text):
    lines = text.split('\n')
    result = []
    for line in lines:
        line = line.replace('&lt;', '\x00LT\x00').replace('&gt;', '\x00GT\x00')
        line = re.sub(r'<([^>\s][^>]*)>', r'&lt;\1&gt;', line)
        line = line.replace('\x00LT\x00', '&lt;').replace('\x00GT\x00', '&gt;')
        result.append(line)
    return '\n'.join(result)

def fix_home_links(content, lang):
    if not content.startswith('---'):
        return content
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content

    fm = parts[1]
    body = parts[2]

    fm = re.sub(r'^[a-zA-Z0-9_\u0080-\uFFFF]+:\s*tuis\b', 'layout: home', fm, flags=re.M)
    fm = re.sub(r'^layout:\s*[a-zA-Z0-9_\u0080-\uFFFF]+\b', 'layout: home', fm, flags=re.M)
    fm = re.sub(r'^\s*(?:detagls|uitleg|விவரம்|جزئیات):\s*', '    details: ', fm, flags=re.M)

    fm = re.sub(r'/lessons/', '/lektionen/', fm)
    fm = re.sub(r'/lesson(\d+)', r'/lektion\1', fm)
    fm = re.sub(r'/grammar\b', '/grammatik', fm)

    def replace_link(m):
        path = m.group(1)
        if path.startswith(f'/{lang}/'):
            return m.group(0)
        elif path.startswith('/'):
            return f'link: /{lang}{path}'
        return f'link: /{lang}/{path}'

    fm = re.sub(r'link:\s*([^\s\n]+)', replace_link, fm)

    lines = fm.splitlines()
    new_lines = []
    in_hero = False
    in_actions = False
    in_features = False

    for line in lines:
        sline = line.strip()
        if not sline:
            new_lines.append('')
            continue
        if sline.startswith('layout:'):
            new_lines.append('layout: home')
            in_hero = False; in_actions = False; in_features = False
        elif sline.startswith('hero:') or sline.startswith('قهرمان:'):
            new_lines.append('hero:')
            in_hero = True; in_actions = False; in_features = False
        elif in_hero and any(sline.startswith(k) for k in ['name:', 'text:', 'tagline:', 'نام:', 'متن:', 'زیرعنوان:']):
            k, v = sline.split(':', 1)
            key_map = {'نام': 'name', 'متن': 'text', 'زیرعنوان': 'tagline'}
            clean_k = key_map.get(k.strip(), k.strip())
            new_lines.append(f'  {clean_k}:{v}')
        elif sline.startswith('actions:') or sline.startswith('اقدامات:'):
            new_lines.append('  actions:')
            in_actions = True; in_hero = False; in_features = False
        elif in_actions and (sline.startswith('- theme:') or sline.startswith('- تم:')):
            _, v = sline.split(':', 1)
            v_map = {'برند': 'brand', 'جایگزین': 'alt'}
            clean_v = v_map.get(v.strip(), v.strip())
            new_lines.append(f'    - theme: {clean_v}')
        elif in_actions and any(sline.startswith(k) for k in ['text:', 'link:', 'متن:', 'پیوند:']):
            k, v = sline.split(':', 1)
            key_map = {'متن': 'text', 'پیوند': 'link'}
            clean_k = key_map.get(k.strip(), k.strip())
            new_lines.append(f'      {clean_k}:{v}')
        elif sline.startswith('features:') or sline.startswith('ویژگی‌ها:'):
            new_lines.append('features:')
            in_features = True; in_hero = False; in_actions = False
        elif in_features and (sline.startswith('- title:') or sline.startswith('- عنوان:')):
            _, v = sline.split(':', 1)
            new_lines.append(f'  - title:{v}')
        elif in_features and (sline.startswith('details:') or sline.startswith('جزئیات:')):
            _, v = sline.split(':', 1)
            new_lines.append(f'    details:{v}')
        else:
            new_lines.append(line)

    repaired_fm = '\n'.join(new_lines)
    return f'---{repaired_fm}\n---{body}'

def fix_lesson_links(content, lang):
    def replace(m):
        path = m.group(1)
        if path.startswith(f'/{lang}/'):
            return f'({path})'
        return f'(/{lang}{path})'
    return re.sub(r'\((/licenses[^)]*)\)', replace, content)

def fix_main_page_links(content, lang):
    def replace(m):
        path = m.group(1)
        if path.startswith(f'/{lang}/') or path == f'/{lang}':
            return f'({path})'
        if path.startswith('http') or path.startswith('#') or path.startswith('/images/') or not path.startswith('/'):
            return f'({path})'
        return f'(/{lang}{path})'
    return re.sub(r'\((/[^)]*)\)', replace, content)

def get_tm_path(lang):
    tm_dir = os.path.join(BASE_DIR, ".payer", "tm")
    os.makedirs(tm_dir, exist_ok=True)
    return os.path.join(tm_dir, f"{lang}.json")

def load_tm(lang):
    p = get_tm_path(lang)
    if os.path.exists(p):
        try:
            with open(p, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_tm(lang, tm):
    p = get_tm_path(lang)
    with open(p, 'w', encoding='utf-8') as f:
        json.dump(tm, f, ensure_ascii=False, indent=2)

def sanitize_translation_output(text, lang):
    """Sanitize translated content: purge empty containers, repair container nesting, enforce glossary maps, and align indented container lines."""
    if not text:
        return text

    # 1. Apply glossary and DE grammar terms map if available for language
    if lang in GLOSSARY_CLEANUP_MAPS:
        glossary = GLOSSARY_CLEANUP_MAPS[lang]
        items = glossary.items() if isinstance(glossary, dict) else glossary
        for src, target in items:
            text = text.replace(src, target)

    # 2. Purge empty container blocks
    text = re.sub(r':::\s*(?:note-box|indent|grammar-box|deleteme-box)\s*\n\s*:::\n?', '', text)

    # 3. Auto-fix container colon nesting (upgrade outer container to :::: if it contains inner ::: indent/box)
    lines = text.split('\n')
    fixed_nesting = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m_outer = re.match(r'^( +)?:::\s*(grammar-box|note-box|deleteme-box)', line)
        if m_outer:
            indent = m_outer.group(1) or ""
            box_type = m_outer.group(2)
            j = i + 1
            has_inner = False
            closing_idx = -1
            while j < len(lines):
                if re.match(r'^( +)?:::\s*(indent|grammar-box|note-box)', lines[j]):
                    has_inner = True
                elif re.match(r'^( +)?:::\s*$', lines[j]):
                    closing_idx = j
                    if not has_inner:
                        break
                j += 1
            
            if has_inner and closing_idx > i:
                fixed_nesting.append(f"{indent}:::: {box_type}")
                for k in range(i + 1, closing_idx):
                    fixed_nesting.append(lines[k])
                fixed_nesting.append(f"{indent}::::")
                i = closing_idx + 1
                continue

        fixed_nesting.append(line)
        i += 1

    lines = fixed_nesting

    # 4. Auto-align indented container contents to prevent layout breaks in Markdown-it
    in_container = False
    container_indent = 0
    fixed_lines = []
    for line in lines:
        m_start = re.match(r'^( +):::+\s*(note-box|indent|grammar-box|deleteme-box)', line)
        if m_start:
            in_container = True
            container_indent = len(m_start.group(1))
            fixed_lines.append(line)
            continue
        m_end = re.match(r'^( +):::+\s*$', line)
        if in_container and m_end:
            in_container = False
            fixed_lines.append(line)
            continue
        if in_container and line.strip():
            leading = len(line) - len(line.lstrip(' '))
            if leading < container_indent:
                fixed_lines.append(' ' * (container_indent - leading) + line)
            else:
                fixed_lines.append(line)
        else:
            fixed_lines.append(line)

    return '\n'.join(fixed_lines)

def translate_yaml_frontmatter(yaml_content, target_lang):
    """Safely translates only string values in a YAML frontmatter block in a single bundled LLM call."""
    translatable_keys = {'name', 'text', 'tagline', 'title', 'subtitle', 'description', 'details'}
    lines = yaml_content.split('\n')

    indices = []
    values = []

    for i, line in enumerate(lines):
        m = re.match(r'^(\s*(?:-\s*)?[a-zA-Z0-9_-]+:\s*)(.+)$', line)
        if m:
            raw_key = m.group(1)
            key_str = re.sub(r'^\s*-\s*', '', raw_key).strip().strip(':')
            val_str = m.group(2).strip().strip('"').strip("'")
            if key_str in translatable_keys and val_str and not val_str.startswith('/'):
                indices.append(i)
                values.append(val_str)

    if not values:
        return yaml_content

    source_text = "\n\n".join(values)
    res_tuple = translate_text(source_text, target_lang)
    translated_text = res_tuple[0]

    if not translated_text or translated_text.startswith("ERROR:"):
        return yaml_content

    translated_vals = [p.strip() for p in translated_text.split('\n\n') if p.strip()]
    if len(translated_vals) != len(values):
        translated_vals = [p.strip() for p in translated_text.split('\n') if p.strip()]

    if len(translated_vals) == len(values):
        for idx, new_val in zip(indices, translated_vals):
            m = re.match(r'^(\s*(?:-\s*)?[a-zA-Z0-9_-]+:\s*)(.+)$', lines[idx])
            prefix = m.group(1) if m else lines[idx].split(':', 1)[0] + ': '
            
            # Format string safely for YAML
            if '"' in new_val and "'" not in new_val:
                lines[idx] = f"{prefix}'{new_val}'"
            elif '"' in new_val:
                escaped = new_val.replace('"', '\\"')
                lines[idx] = f'{prefix}"{escaped}"'
            else:
                lines[idx] = f'{prefix}"{new_val}"'

    return '\n'.join(lines)

def translate_file(source_path, target_path, lang, post_process=None, force=False):
    filename = os.path.basename(source_path)
    src_mtime = os.path.getmtime(source_path)
    tgt_mtime = os.path.getmtime(target_path) if os.path.exists(target_path) else 0

    # TOTALBREMSE: Absolute write lock for DE master and 100% completed languages
    if not force and is_language_completed(lang):
        sys.stdout.write(f"[{lang}] 🔒 TOTALBREMSE: Language '{lang}' is 100% completed & write-locked.\n")
        sys.stdout.flush()
        return

    if force:
        session_start = get_force_session_start_time(lang, init_if_missing=True)
        if os.path.exists(target_path) and tgt_mtime >= session_start:
            sys.stdout.write(f"[{lang}] Skipping {filename} (already completed in current force session)\n")
            sys.stdout.flush()
            return
    elif os.path.exists(target_path) and tgt_mtime >= src_mtime:
        try:
            from translation_qa import is_file_fallback
            is_fb, reason = is_file_fallback(target_path, lang)
            if not is_fb:
                sys.stdout.write(f"[{lang}] Skipping {filename} (up to date & clean)\n")
                sys.stdout.flush()
                return True
            else:
                sys.stdout.write(f"[{lang}] Queue Item: {filename} has residues/fallbacks ({reason}). Re-translating...\n")
                sys.stdout.flush()
        except Exception:
            pass

    sys.stdout.write(f"[{lang}] Translating {filename}...\n")
    sys.stdout.flush()

    with open(source_path, 'r', encoding='utf-8') as f:
        content = f.read()

    tm = load_tm(lang)
    frontmatter = ""
    body = content

    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            frontmatter = parts[1]
            body = parts[2]

    if frontmatter.strip():
        sys.stdout.write("  -> translating YAML frontmatter safely...\n")
        sys.stdout.flush()
        tr_fm = translate_yaml_frontmatter(frontmatter, lang)
        tr_fm_clean = []
        for line in tr_fm.split('\n'):
            line = re.sub(r'^(title|author|description|lesson|script|exercise):\s*""$', r'\1: ""', line)
            tr_fm_clean.append(line)
        tr_fm = '\n'.join(tr_fm_clean)
    else:
        tr_fm = ""

    chunks = chunk_content(body)
    translated_chunks = []

    # Preserve clean sections: Seed TM from clean chunks in existing target file
    if not force and os.path.exists(target_path):
        try:
            with open(target_path, 'r', encoding='utf-8', errors='ignore') as tf:
                existing_tgt_content = tf.read()
            if existing_tgt_content.startswith('---'):
                parts = existing_tgt_content.split('---', 2)
                existing_tgt_body = parts[2] if len(parts) >= 3 else existing_tgt_content
            else:
                existing_tgt_body = existing_tgt_content
            tgt_chunks = chunk_content(existing_tgt_body)
            if len(tgt_chunks) == len(chunks):
                for s_chunk, t_chunk in zip(chunks, tgt_chunks):
                    s_h = hash_chunk(s_chunk)
                    if s_h not in tm and not scan_german_residues(t_chunk, target_lang=lang):
                        tm[s_h] = t_chunk
        except Exception:
            pass

    for idx, chunk in enumerate(chunks):
        c_hash = hash_chunk(chunk)
        if not force and c_hash in tm and not tm[c_hash].startswith("ERROR:"):
            cached_tr = tm[c_hash]
            if not scan_german_residues(cached_tr, target_lang=lang):
                sys.stdout.write(f"    [✓ TM Cache] Sektion {idx+1}/{len(chunks)} sauber & verifiziert.\n")
                sys.stdout.flush()
                translated_chunks.append(cached_tr)
                continue
            else:
                sys.stdout.write(f"  [!] TM Cache Invalidation: Chunk {idx+1}/{len(chunks)} hat DE-Reste. Re-Übersetzung läuft...\n")
                sys.stdout.flush()

        start_t = time.time()
        tr_chunk, ph_used = translate_text(chunk, lang)

        # GUARD AGAINST ERROR STRINGS: Never store or output ERROR messages
        if not tr_chunk or tr_chunk.startswith("ERROR:"):
            # Adaptive Sub-Chunking: Split failed chunk in half and retry sub-chunks
            sub_chunks = chunk_content(chunk, max_chunk_size=max(500, len(chunk) // 2))
            if len(sub_chunks) > 1:
                sys.stdout.write(f"  [!] Chunk {idx+1}/{len(chunks)} failed ({tr_chunk[:40] if tr_chunk else 'Empty'}). Splitting into {len(sub_chunks)} smaller sub-chunks...\n")
                sys.stdout.flush()
                sub_tr_list = []
                sub_failed = False
                for s_idx, s_chunk in enumerate(sub_chunks):
                    s_tr, s_ph = translate_text(s_chunk, lang)
                    if not s_tr or s_tr.startswith("ERROR:"):
                        sub_failed = True
                        break
                    s_tr = sanitize_translation_output(s_tr, lang)
                    sub_tr_list.append(s_tr)
                if not sub_failed:
                    tr_chunk = '\n'.join(sub_tr_list)
                    ph_used = 1
                else:
                    sys.stdout.write(f"  [!] ABORT: Chunk {idx+1}/{len(chunks)} sub-chunks failed for {filename}. Refusing to save.\n")
                    sys.stdout.flush()
                    return False
            else:
                sys.stdout.write(f"  [!] ABORT: Chunk {idx+1}/{len(chunks)} failed for {filename} ({tr_chunk[:60] if tr_chunk else 'Empty'}). Refusing to save.\n")
                sys.stdout.flush()
                return False

        tr_chunk = sanitize_translation_output(tr_chunk, lang)
        elapsed_t = time.time() - start_t
        sys.stdout.write(f"    Sektion {idx+1}/{len(chunks)} Chunks fertig ({elapsed_t:.1f}s, Tries={ph_used+1})\n")
        sys.stdout.flush()

        tm[c_hash] = tr_chunk
        save_tm(lang, tm)
        touch_progress_heartbeat(filename, idx + 1, len(chunks), lang)
        translated_chunks.append(tr_chunk)

    final_body = '\n'.join(translated_chunks)
    if tr_fm:
        final_content = f"---{tr_fm}\n---{final_body}"
    else:
        final_content = final_body

    if post_process:
        final_content = post_process(final_content, lang)

    os.makedirs(os.path.dirname(target_path), exist_ok=True)

    flagged = scan_german_residues(final_content, target_lang=lang)
    if flagged:
        sys.stdout.write(f"  [!] {len(flagged)} German residue(s) detected — running local auto-heal pass...\n")
        sys.stdout.flush()

        final_content = sonnet_patch_residues(final_content, flagged, lang)
        still_flagged = scan_german_residues(final_content, target_lang=lang)

        if still_flagged:
            sys.stdout.write(f"  [!] {len(still_flagged)} residue(s) remained — logging to translation_failures.md\n")
            sys.stdout.flush()
            log_failure(
                lang=lang,
                filename=filename,
                failure_code="DE_RESIDUE_UNRESOLVED",
                flagged_lines=still_flagged,
                note=f"{len(still_flagged)} German residue(s) remained after auto-heal pass."
            )
        else:
            sys.stdout.write("  [✓] All German residues cleanly resolved by local auto-heal pass!\n")
            sys.stdout.flush()

    # Back-sync final (and auto-healed) chunks into TM Cache under source chunk hashes
    try:
        body_for_tm = final_content
        if final_content.startswith('---'):
            parts = final_content.split('---', 2)
            if len(parts) >= 3:
                body_for_tm = parts[2]
        healed_chunks = chunk_content(body_for_tm)
        if len(healed_chunks) == len(chunks):
            for s_chunk, hc in zip(chunks, healed_chunks):
                s_hash = hash_chunk(s_chunk)
                if not scan_german_residues(hc, target_lang=lang):
                    tm[s_hash] = hc
            save_tm(lang, tm)
    except Exception as e:
        sys.stderr.write(f"  [!] Warning: Failed to back-sync healed TM chunks: {e}\n")

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(final_content)

    sys.stdout.write(f"  [✓] Wrote {target_path}\n")
    sys.stdout.flush()
    return True

def generate_licenses(lang):
    de_licenses_path = os.path.join(BASE_DIR, "licenses.md")
    if not os.path.exists(de_licenses_path):
        return

    lang_dir = os.path.join(BASE_DIR, lang)
    target_path = os.path.join(lang_dir, "licenses.md")
    os.makedirs(lang_dir, exist_ok=True)

    with open(de_licenses_path, 'r', encoding='utf-8') as f:
        content = f.read()

    labels = LICENSES_LABELS.get(lang, LICENSES_LABELS["en"])
    phrases = LICENSES_PHRASES.get(lang, {})

    content = re.sub(
        r'# Bildlizenzen Audit',
        f'# {labels["title"]}',
        content
    )
    content = re.sub(
        r'\| Datei \| Gefundene Quellinformation \| Vorschau \|',
        f'| {labels["col1"]} | {labels["col2"]} | {labels["col3"]} |',
        content
    )

    for de_phrase, tr_phrase in phrases.items():
        content = content.replace(de_phrase, tr_phrase)

    def replace_image_link(m):
        img_filename = m.group(1)
        return f'<img src="/{img_filename}" style="max-height: 80px;" />'

    content = re.sub(r'<img src="/([^"]+)" style="max-height: 80px;" />', replace_image_link, content)
    content = fix_main_page_links(content, lang)

    with open(target_path, 'w', encoding='utf-8') as f:
        f.write(content)

    sys.stdout.write(f"[{lang}] Generated {target_path} (deterministic license table)\n")
    sys.stdout.flush()

def sync_missing_master_files(lang):
    if lang == 'de':
        return

    de_dir = os.path.join(BASE_DIR, "lektionen")
    target_dir = os.path.join(BASE_DIR, lang, "lektionen")
    os.makedirs(target_dir, exist_ok=True)

    de_files = set(glob.glob(os.path.join(de_dir, "*.md")))

    for de_file in sorted(de_files):
        fname = os.path.basename(de_file)
        tgt_file = os.path.join(target_dir, fname)

        if not os.path.exists(tgt_file):
            with open(de_file, 'r', encoding='utf-8') as f:
                content = f.read()

            parts = content.split('---', 2)
            if len(parts) >= 3:
                fm = parts[1]
                body = parts[2]

                clean_fm = []
                for line in fm.split('\n'):
                    if line.startswith('title:'):
                        clean_fm.append('title: ""')
                    elif line.startswith('description:'):
                        clean_fm.append('description: ""')
                    else:
                        clean_fm.append(line)
                new_fm = '\n'.join(clean_fm)
                new_content = f"---{new_fm}\n---{body}"
            else:
                new_content = content

            with open(tgt_file, 'w', encoding='utf-8') as f:
                f.write(new_content)

            sys.stdout.write(f"[{lang}] Synced missing master file template: {fname}\n")
            sys.stdout.flush()

def translate_main_pages(lang, force=False):
    lang_dir = os.path.join(BASE_DIR, lang)
    os.makedirs(lang_dir, exist_ok=True)

    for page in MAIN_PAGES:
        if page == "licenses.md":
            generate_licenses(lang)
            continue

        source_path = os.path.join(BASE_DIR, page)
        target_path = os.path.join(lang_dir, page)

        if not os.path.exists(source_path):
            continue

        if page == "index.md":
            post_proc = fix_home_links
        else:
            post_proc = fix_main_page_links

        translate_file(source_path, target_path, lang, post_process=post_proc, force=force)

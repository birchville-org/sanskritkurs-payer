#!/usr/bin/env python3
"""
Autonomous Background Healer for Payer Sanskritkurs Translations.
Systematically clears German/English residues and fallbacks in unfinished languages.
Guaranteed safe:
- TOTALBREMSE enforced: Completed languages and German master files are strictly read-only.
- Strict verification gate: Target files are ONLY overwritten if tqa.is_file_fallback() returns (False, '').
- Uses OpenRouter API (google/gemini-2.5-flash) with batched XML requests for high speed and zero local lock contention.
"""

import os
import sys
import re
import json
import time
import socket
import argparse
import urllib.request
from pathlib import Path
from lingua import Language

socket.setdefaulttimeout(30)

# Ensure scripts directory is in sys.path
SCRIPTS_DIR = Path(__file__).resolve().parent
ROOT_DIR = SCRIPTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

import translation_qa as tqa
from translation.config import LANGUAGES, LANG_NAMES

LANG_CONFIG = {
    'si': {
        'name': 'Sinhala (සිංහල)',
        'script_range': (0x0D80, 0x0DFF),
        'heading_prefix': '# අභ්‍යාසය'
    },
    'is': {
        'name': 'Icelandic (Íslenska)',
        'heading_prefix': '# Æfing'
    },
    'sl': {
        'name': 'Slovenian (Slovenščina)',
        'heading_prefix': '# Vaja'
    },
    'sv': {
        'name': 'Swedish (Svenska)',
        'heading_prefix': '# Övning'
    },
    'gez': {
        'name': "Ge'ez (ግዕዝ)",
        'script_range': (0x1200, 0x137F),
        'heading_prefix': '# ልምම්ድ'
    },
    'et': {
        'name': 'Estonian (Eesti)',
        'heading_prefix': '# Harjutus'
    },
    'zu': {
        'name': 'isiZulu (Zulu)',
        'heading_prefix': '# Isivivinyo'
    },
    'am': {
        'name': 'Amharic (አማርኛ)',
        'script_range': (0x1200, 0x137F),
        'heading_prefix': '# ልምምድ'
    },
    'fa': {
        'name': 'Persian (فارسی)',
        'script_range': (0x0600, 0x06FF),
        'heading_prefix': '# تمرین'
    }
}

OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "google/gemini-2.5-flash"

CITATIONS = [
    'Dümmler', 'Berlin', 'Kielhorn', 'Solomons', 'Monier-Williams',
    'Stenzler', 'Image source:', 'Fig.:', 'Lüders', 'Alsdorf',
    'Weber, Max', 'Tübingen', 'Tüpfli', 'Bussmann', 'Payer, Alois', 'Hoffmann, Karl'
]


def call_llm(prompt: str, api_key: str, max_retries: int = 3) -> str:
    """Send translation prompt to OpenRouter with automatic retry and backoff."""
    payload = {
        'model': MODEL,
        'messages': [{'role': 'user', 'content': prompt}],
        'temperature': 0.1
    }
    data = json.dumps(payload).encode('utf-8')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {api_key}'
    }

    for attempt in range(1, max_retries + 1):
        try:
            req = urllib.request.Request(OPENROUTER_URL, data=data, headers=headers)
            with urllib.request.urlopen(req, timeout=45) as resp:
                res = json.loads(resp.read().decode('utf-8'))
                return res['choices'][0]['message']['content']
        except Exception as e:
            if attempt == max_retries:
                raise RuntimeError(f"OpenRouter API call failed after {max_retries} attempts: {e}")
            time.sleep(2 * attempt)
    return ""


def preprocess_text(txt: str, lang: str = "") -> str:
    """Normalize container boundaries, strip duplicate arrow residues, and fix known tokens."""
    # 1. Known unresolved placeholder tokens
    txt = txt.replace('⟨IAST_L_6⟩', '⟪सावित्री⟫')
    
    # 2. Arrow lines cleanup: "A -> B" or "A → B" where left is German and right is target
    lines = txt.splitlines()
    new_lines = []
    for l in lines:
        if re.search(r'\s*(?:->|→)\s*', l) and not l.strip().startswith('|'):
            parts = re.split(r'\s*(?:->|→)\s*', l)
            new_lines.append(parts[-1].strip())
        else:
            new_lines.append(l)
    txt = '\n'.join(new_lines)
    
    # 3. Normalize container boundaries (crucial for paragraph splitting)
    txt = re.sub(r'(?<!\n)\n(:::[^\n]*)', r'\n\n\1', txt)
    txt = re.sub(r'(:::[^\n]*)\n(?!\n)', r'\1\n\n', txt)
    
    # 4. Normalize media caption blocks (ensure blank line around images and captions)
    txt = re.sub(r'(!\[.*?\]\(.*?\))\n(?!\n)', r'\1\n\n', txt)
    txt = re.sub(r'(Abb\.:[^\n]+)\n(?!\n)', r'\1\n\n', txt)

    # 5. Language-specific caption normalization
    if lang in ('gez', 'am'):
        txt = re.sub(r'\(Bildquelle:', '(የምስል ምንጭ:' if lang == 'am' else '(ምንጭ ምስሊ:', txt)
        txt = re.sub(r'Bildquelle:', 'የምስል ምንጭ:' if lang == 'am' else 'ምንጭ ምስሊ:', txt)
        txt = re.sub(r'Abb\.:', 'ምስል:' if lang == 'am' else 'ስዕሊ:', txt)
    elif lang == 'et':
        txt = re.sub(r'\(Bildquelle:', '(Pildi allikas:', txt)
        txt = re.sub(r'Bildquelle:', 'Pildi allikas:', txt)
        txt = re.sub(r'Abb\.:', 'Joonis:', txt)
    elif lang == 'zu':
        txt = re.sub(r'\(Bildquelle:', '(Umthombo wesithombe:', txt)
        txt = re.sub(r'Bildquelle:', 'Umthombo wesithombe:', txt)
        txt = re.sub(r'Abb\.:', 'Umfanekiso:', txt)
        txt = re.sub(r'\bse-Präsens\b', 'sesikhathi esiyimanje', txt)
        txt = re.sub(r'\bPräsens\b', 'isikhathi esiyimanje', txt)
    elif lang == 'fa':
        txt = re.sub(r'\(Bildquelle:', '(منبع تصویر:', txt)
        txt = re.sub(r'Bildquelle:', 'منبع تصویر:', txt)
        txt = re.sub(r'Abb\.:', 'تصویر:', txt)
    return txt


def extract_items_to_heal(txt: str, lang: str, detector, filepath: Path = None):
    """
    Identify problematic elements (headings, YAML frontmatter, paragraphs) that need translation.
    Returns:
      updated_txt: str (e.g. after direct heading fixes)
      items_to_translate: list of dicts: {'type': 'yaml'|'para', 'key': ..., 'index': ..., 'original': str}
    """
    txt = preprocess_text(txt, lang)
    cfg = LANG_CONFIG.get(lang, {})
    heading_prefix = cfg.get('heading_prefix')
    script_range = cfg.get('script_range')

    # Build German master sentence set if filepath is provided
    de_sent_set = set()
    if filepath and lang not in tqa.DE_FALLBACK_ALLOWED:
        fp = Path(filepath)
        de_file = ROOT_DIR / "docs" / "lektionen" / fp.name
        if not de_file.exists():
            de_file = ROOT_DIR / "docs" / fp.name
        if de_file.exists():
            de_sent_set = tqa.get_de_sent_set(de_file)

    # 1. Direct fix for Exercise headings: # Übung \d+ or # Exercise \d+
    if heading_prefix:
        txt = re.sub(
            r'^#\s+(?:Übung|Exercise)\s+(\d+)',
            lambda m: f"{heading_prefix} {m.group(1)}",
            txt,
            flags=re.MULTILINE
        )

    items = []

    # 2. YAML frontmatter check
    yaml_m = re.match(r'^---\n(.*?)\n---\n', txt, flags=re.DOTALL)
    if yaml_m:
        for y_line in yaml_m.group(1).splitlines():
            km = re.search(r'^(subtitle|description|title):\s*["\']?(.*?)["\']?\s*$', y_line, re.IGNORECASE)
            if km:
                field_name = km.group(1).lower()
                y_val = km.group(2).strip()
                y_clean = re.sub(r'[\u0900-\u097F]+', '', y_val)
                y_clean = re.sub(r'⟪.*?⟫', '', y_clean).strip()
                if script_range and any(script_range[0] <= ord(c) <= script_range[1] for c in y_clean):
                    # Already in target script
                    continue
                is_problematic = False
                # 1. Verbatim German master check in frontmatter
                if de_sent_set:
                    y_clean_line = re.sub(r'[\u0900-\u097F]+', '', y_line.strip())
                    y_clean_line = re.sub(r'⟪.*?⟫', '', y_clean_line).strip()
                    y_clean_line = re.sub(r'^[0-9\.\s\\=\-/*>\(\)]+', '', y_clean_line).strip()
                    y_val_prose = re.sub(r'[\u0900-\u097F]+', '', y_val)
                    y_val_prose = re.sub(r'⟪.*?⟫', '', y_val_prose).strip()
                    if y_clean_line in de_sent_set or y_val_prose in de_sent_set:
                        is_problematic = True
                if not is_problematic and len(y_clean) >= 6 and not tqa.is_sanskrit_iast(y_clean):
                    # Check keywords
                    for kw in tqa.STRICT_DE_GRAMMAR_KEYWORDS + tqa.GERMAN_KEYWORDS:
                        if re.search(r'(?<!\w)' + re.escape(kw) + r'(?!\w)', y_clean, re.IGNORECASE):
                            is_problematic = True
                            break
                    if not is_problematic and detector:
                        try:
                            det_lang = detector.detect_language_of(y_clean)
                            if det_lang == Language.GERMAN:
                                is_problematic = True
                            elif lang not in tqa.DE_FALLBACK_ALLOWED:
                                if det_lang in (Language.SPANISH, Language.ENGLISH, Language.FRENCH, Language.ITALIAN):
                                    is_problematic = True
                        except Exception:
                            pass
                if is_problematic:
                    items.append({
                        'type': 'yaml',
                        'field': field_name,
                        'original': y_val
                    })

    # 3. Paragraphs
    paras = txt.split('\n\n')
    for idx, raw_p in enumerate(paras):
        if raw_p.startswith('```') or raw_p.startswith('---'):
            continue
        clean_p = tqa.clean_markdown_for_lid(raw_p)

        # 3a. Keyword detection (Strict + General)
        kw_hit = False
        strict_kw = tqa.STRICT_DE_GRAMMAR_KEYWORDS
        gen_kw = tqa.GERMAN_KEYWORDS
        if lang in tqa.LATIN_TOLERANT_LANGS:
            strict_kw = [k for k in strict_kw if k not in tqa.LATIN_GRAMMAR_TERMS]
            gen_kw = [k for k in gen_kw if k not in tqa.LATIN_GRAMMAR_TERMS]

        for kw in strict_kw + gen_kw:
            if re.search(r'(?<!\w)' + re.escape(kw) + r'(?!\w)', clean_p, re.IGNORECASE):
                kw_hit = True
                break

        if kw_hit:
            items.append({
                'type': 'para',
                'index': idx,
                'original': raw_p
            })
            continue

        # 3b. Unresolved placeholders
        if re.search(r'(?:⟨|&lang;)?(?:DEVA|IAST_L|STRUCT)_[0-9\u0966-\u096F\u0660-\u0669N]+(?:⟩|&rang;)?', raw_p):
            items.append({
                'type': 'para',
                'index': idx,
                'original': raw_p
            })
            continue

        # 3c. Lingua LID (paragraph level)
        p_chk = re.sub(r'^[#|\s:-]+', '', clean_p, flags=re.M)
        p_chk = re.sub(r':br', ' ', p_chk).strip()
        lid_hit = False
        if len(p_chk) >= 30 and not tqa.is_sanskrit_iast(p_chk):
            # Check script density for non-Latin target scripts
            if script_range:
                script_count = sum(1 for c in p_chk if script_range[0] <= ord(c) <= script_range[1])
                if script_count >= len(p_chk) * 0.35:
                    continue

            words = set(re.findall(r'\b[a-zäöüß]+\b', p_chk.lower()))
            if words.intersection(tqa.COMMON_DE_WORDS) and detector:
                try:
                    if detector.detect_language_of(p_chk) == Language.GERMAN:
                        if not any(cit in p_chk for cit in CITATIONS):
                            lid_hit = True
                except Exception:
                    pass

        if lid_hit:
            items.append({
                'type': 'para',
                'index': idx,
                'original': raw_p
            })
            continue

        # 3d. Line-level German residue & instruction detection
        line_hit = False
        for line in raw_p.splitlines():
            l_clean = re.sub(r'^[0-9\.\s\\=\-/*>\(\)]+', '', line.strip()).strip()
            if len(l_clean) >= 12 and not l_clean.startswith('#') and not l_clean.startswith('|') and not l_clean.startswith('!'):
                l_prose = re.sub(r'[\u0900-\u097F]+', '', l_clean)
                l_prose = re.sub(r'⟪.*?⟫', '', l_prose).strip()
                words = set(re.findall(r'\b[a-zäöüß]+\b', l_prose.lower()))
                if words.intersection(tqa.COMMON_DE_WORDS | {'übersetzen', 'bilden', 'setzen', 'formt', 'ergänzen', 'bestimmen', 'schreiben', 'möglichkeiten'}):
                    if detector:
                        try:
                            if detector.detect_language_of(l_prose) == Language.GERMAN:
                                if not any(cit in l_prose for cit in CITATIONS):
                                    line_hit = True
                                    break
                        except Exception:
                            pass
        if line_hit:
            items.append({
                'type': 'para',
                'index': idx,
                'original': raw_p
            })
            continue

        # 3e. Verbatim German Master Sentence Check
        if de_sent_set:
            de_line_hit = False
            for line in raw_p.splitlines():
                l_clean = line.strip()
                if len(l_clean) >= 15 and not l_clean.startswith('|') and not l_clean.startswith(':::') and not l_clean.startswith('!['):
                    l_prose = re.sub(r'[\u0900-\u097F]+', '', l_clean)
                    l_prose = re.sub(r'⟪.*?⟫', '', l_prose).strip()
                    l_prose = re.sub(r'^[0-9\.\s\\=\-/*>\(\)]+', '', l_prose).strip()
                    if l_prose and l_prose in de_sent_set:
                        de_line_hit = True
                        break
            if de_line_hit:
                items.append({
                    'type': 'para',
                    'index': idx,
                    'original': raw_p
                })
                continue

    return txt, items


def heal_file_pass(txt: str, lang: str, api_key: str, detector, de_exact: bool = False, filepath: Path = None) -> str:
    """Execute a single healing translation pass on text content."""
    target_lang_name = LANG_CONFIG.get(lang, {}).get('name') or LANG_NAMES.get(lang, lang)
    txt, items = extract_items_to_heal(txt, lang, detector, filepath=filepath)

    if not items and not de_exact:
        return txt

    if de_exact:
        paras = txt.split('\n\n')
        items = [{'type': 'para', 'index': i, 'original': p} for i, p in enumerate(paras) if not p.startswith('---')]

    # Process items in batches of up to 12 items
    batch_size = 12
    paras = txt.split('\n\n')

    for b_start in range(0, len(items), batch_size):
        batch = items[b_start:b_start + batch_size]
        items_xml = [f'<item id="{i}">\n{it["original"]}\n</item>' for i, it in enumerate(batch)]

        prompt = f"""You are an expert scholarly translator for Sanskrit instructional materials.
Translate the text within each <item id="..."> block from German to {target_lang_name}.

CRITICAL RULES:
1. Preserve all Markdown formatting, container colons (:::), tables (:br), lists, and line breaks exactly.
2. Preserve Sanskrit transliteration in IAST (e.g. vidyā, deva, yoga) and Devanagari ⟪...⟫ exactly as given.
3. Translate all German grammatical terms into natural {target_lang_name} terms (do not retain German/Latin terms like "Pronomina"; use the target language equivalent e.g. "fornöfn" in Icelandic).
4. Do NOT translate technical markers, code blocks, or HTML tags.
5. Output ONLY the translated items enclosed in matching XML tags:
<item id="0">...</item>

{chr(10).join(items_xml)}
"""
        resp_content = call_llm(prompt, api_key)
        item_pattern = re.compile(r'<item id="?(\d+)"?>\s*(.*?)\s*</item>', re.DOTALL)
        matches = item_pattern.findall(resp_content)

        translated_map = {int(idx): val.strip() for idx, val in matches}

        for i, it in enumerate(batch):
            if i in translated_map:
                trans_val = translated_map[i]
                if it['type'] == 'para':
                    paras[it['index']] = trans_val
                elif it['type'] == 'yaml':
                    field = it['field']
                    yaml_pattern = re.compile(rf'^({field}:\s*["\']?).*?(["\']?\s*)$', re.MULTILINE | re.IGNORECASE)
                    for p_i in range(len(paras)):
                        if re.search(rf'^{field}:', paras[p_i], re.MULTILINE | re.IGNORECASE):
                            paras[p_i] = yaml_pattern.sub(rf'\g<1>{trans_val}\g<2>', paras[p_i], count=1)
                            break

    txt_healed = '\n\n'.join(paras)
    cfg = LANG_CONFIG.get(lang, {})
    heading_prefix = cfg.get('heading_prefix')
    if heading_prefix:
        txt_healed = re.sub(
            r'^#\s+(?:Übung|Exercise)\s+(\d+)',
            lambda m: f"{heading_prefix} {m.group(1)}",
            txt_healed,
            flags=re.MULTILINE
        )
    return txt_healed


def heal_file(filepath: Path, lang: str, api_key: str, detector, dry_run: bool = False) -> bool:
    """
    Attempt to heal a single file with up to 2 passes and strict verification.
    """
    txt = filepath.read_text(encoding='utf-8', errors='ignore')
    txt = preprocess_text(txt, lang)

    tmp_dir = Path(f"/tmp/payer_healer_verify_{lang}_{os.getpid()}")
    tmp_dir.mkdir(parents=True, exist_ok=True)
    tmp_path = tmp_dir / filepath.name

    # Check if preprocessing alone resolved the fallback
    tmp_path.write_text(txt, encoding='utf-8')
    fb_pre, _ = tqa.is_file_fallback(tmp_path, lang)
    if not fb_pre:
        if not dry_run:
            filepath.write_text(txt, encoding='utf-8')
        tmp_path.unlink(missing_ok=True)
        return True

    # Check exact copy of German master
    de_file = ROOT_DIR / "docs" / "lektionen" / filepath.name
    if not de_file.exists():
        de_file = ROOT_DIR / "docs" / filepath.name
    is_exact_copy = False
    if de_file.exists():
        de_txt = de_file.read_text(encoding="utf-8", errors="ignore")
        txt_body = re.sub(r'^---\n.*?\n---\n', '', txt, flags=re.DOTALL).strip()
        de_body = re.sub(r'^---\n.*?\n---\n', '', de_txt, flags=re.DOTALL).strip()
        if txt_body == de_body and len(txt_body) > 0:
            is_exact_copy = True

    # Pass 1
    healed_txt = heal_file_pass(txt, lang, api_key, detector, de_exact=is_exact_copy, filepath=filepath)
    tmp_path.write_text(healed_txt, encoding='utf-8')
    fb, reason = tqa.is_file_fallback(tmp_path, lang)
    if not fb:
        if not dry_run:
            filepath.write_text(healed_txt, encoding='utf-8')
        tmp_path.unlink(missing_ok=True)
        return True

    # Pass 2 (Retry on remaining residues)
    healed_txt_2 = heal_file_pass(healed_txt, lang, api_key, detector, de_exact=False, filepath=filepath)
    tmp_path.write_text(healed_txt_2, encoding='utf-8')
    fb2, reason2 = tqa.is_file_fallback(tmp_path, lang)
    tmp_path.unlink(missing_ok=True)

    if not fb2:
        if not dry_run:
            filepath.write_text(healed_txt_2, encoding='utf-8')
        return True
    else:
        return False


def run_healer(lang: str, dry_run: bool = False, max_files: int = 0, reverse: bool = False, skip_files: list = None, verbose: bool = False):
    """Run autonomous healer for a specific language."""
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        print("[ERROR] OPENROUTER_API_KEY environment variable is missing!", file=sys.stderr)
        sys.exit(1)

    if lang == 'de' or tqa.is_language_completed(lang):
        print(f"[TOTALBREMSE] Language '{lang}' is 100% complete or master. Read-only.")
        return

    queue = tqa.get_translation_queue(lang)
    if not queue:
        print(f"[OK] Language '{lang}' has 0 items in queue.")
        return

    print(f"=== Starting Autonomous Healer for '{lang}' ({len(queue)} files in queue) ===")
    detector = tqa.get_lingua_detector(lang)

    healed_count = 0
    failed_count = 0

    files_to_process = list(queue)
    if skip_files:
        files_to_process = [item for item in files_to_process if item[0] not in skip_files]
    if reverse:
        files_to_process = files_to_process[::-1]
    if max_files > 0:
        files_to_process = files_to_process[:max_files]

    docs_dir = ROOT_DIR / "docs" / lang

    for fname, reason in files_to_process:
        target_path = docs_dir / "lektionen" / fname
        if not target_path.exists():
            target_path = docs_dir / fname

        if not target_path.exists():
            print(f"  [SKIP] {fname}: target file does not exist ({target_path})")
            failed_count += 1
            continue

        # Check if file was already healed by another worker or already clean
        is_fb, _ = tqa.is_file_fallback(target_path, lang)
        if not is_fb:
            print(f"  [ALREADY CLEAN] {fname}")
            healed_count += 1
            continue

        print(f"  [HEALING] {fname} (initial: {reason[:40]})...", end='', flush=True)
        start_t = time.time()

        try:
            success = heal_file(target_path, lang, api_key, detector, dry_run=dry_run)
            dur = time.time() - start_t
            if success:
                healed_count += 1
                print(f" [DONE in {dur:.1f}s]", flush=True)
            else:
                failed_count += 1
                print(f" [FAILED GATE in {dur:.1f}s]", flush=True)
        except Exception as e:
            dur = time.time() - start_t
            failed_count += 1
            print(f" [ERROR in {dur:.1f}s: {e}]", flush=True)

    remaining_queue = tqa.get_translation_queue(lang)
    status = tqa.get_language_status(lang)
    print(f"\n=== Healer Summary for '{lang}' ===")
    print(f"  Healed: {healed_count} | Failed: {failed_count}")
    print(f"  Queue: {len(queue)} -> {len(remaining_queue)}")
    print(f"  Status: {status['pct']}% clean ({status['sauber']}/{status['total_files']})\n")


def main():
    parser = argparse.ArgumentParser(description="Autonomous Translation Healer")
    parser.add_argument("--lang", type=str, required=True, help="Target language code (e.g. si, is, sl, sv, gez) or 'all'")
    parser.add_argument("--dry-run", action="store_true", help="Simulate without overwriting files")
    parser.add_argument("--max-files", type=int, default=0, help="Maximum files to heal per language")
    parser.add_argument("--reverse", action="store_true", help="Process queue in reverse order")
    parser.add_argument("--skip", nargs="*", default=[], help="File names to skip")
    parser.add_argument("--verbose", action="store_true", help="Verbose log output")
    args = parser.parse_args()

    if args.lang == 'all':
        target_langs = list(LANGUAGES)
    elif ',' in args.lang:
        target_langs = [l.strip() for l in args.lang.split(',') if l.strip()]
    else:
        target_langs = [args.lang]

    for l in target_langs:
        run_healer(l, dry_run=args.dry_run, max_files=args.max_files, reverse=args.reverse, skip_files=args.skip, verbose=args.verbose)


if __name__ == "__main__":
    main()
